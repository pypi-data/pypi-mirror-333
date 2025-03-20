from fs.path import dirname
from PIL import Image, ImageOps
from flask import current_app
from geovisio import utils
from geovisio.utils import db, sequences, upload_set
import psycopg
from psycopg.rows import dict_row
from psycopg.sql import SQL
from psycopg.types.json import Jsonb
import sentry_sdk
from geovisio import errors
from dataclasses import dataclass
import logging
from contextlib import contextmanager
from enum import Enum
from typing import Any, Dict, Optional
import threading
from uuid import UUID
from croniter import croniter
from datetime import datetime, timezone
import geovisio.utils.filesystems

log = logging.getLogger("geovisio.runner_pictures")

PROCESS_MAX_RETRY = 5  # Number of times a job will be retryed if there is a `RecoverableProcessException` during process (like if the blurring api is not reachable).


class PictureBackgroundProcessor(object):
    def __init__(self, app):
        nb_threads = app.config["EXECUTOR_MAX_WORKERS"]
        self.enabled = nb_threads != 0

        if self.enabled:
            from flask_executor import Executor

            self.executor = Executor(app, name="PicProcessor")
        else:
            import sys

            if "run" in sys.argv or "waitress" in sys.argv or "gunicorn" in sys.argv:  # hack not to display a frightening warning uselessly
                log.warning("No picture background processor run, no picture will be processed unless another separate worker is run")
                log.warning("A separate process can be run with:")
                log.warning("flask picture-worker")

    def process_pictures(self):
        """
        Ask for a background picture process that will run until not pictures need to be processed
        """
        if self.enabled:
            worker = PictureProcessor(app=current_app)
            return self.executor.submit(worker.process_jobs)


class ProcessTask(str, Enum):
    prepare = "prepare"
    delete = "delete"
    dispatch = "dispatch"
    finalize = "finalize"


@dataclass
class DbPicture:
    id: UUID
    metadata: dict
    skip_blurring: bool

    def blurred_by_author(self):
        return self.metadata.get("blurredByAuthor", False)


@dataclass
class DbSequence:
    id: UUID


@dataclass
class DbUploadSet:
    id: UUID


@dataclass
class DbJob:
    reporting_conn: psycopg.Connection
    job_history_id: UUID  # ID of the job in the job_history
    job_queue_id: UUID  # ID in the job_queue
    pic: Optional[DbPicture]
    upload_set: Optional[DbUploadSet]
    seq: Optional[DbSequence]

    task: ProcessTask

    def label(self):
        impacted_object = ""
        if self.pic:
            impacted_object = f"picture {self.pic.id}"
        elif self.seq:
            impacted_object = f"sequence {self.seq.id}"
        elif self.upload_set:
            impacted_object = f"upload set {self.upload_set.id}"
        else:
            impacted_object = "unknown object"

        return f"{self.task} for {impacted_object}"


def processPictureFiles(pic: DbPicture, config):
    """Generates the files associated with a sequence picture.

    If needed the image is blurred before the tiles and thumbnail are generated.

    Parameters
    ----------
    db : psycopg.Connection
            Database connection
    dbPic : DbPicture
            The picture metadata extracted from database
    config : dict
            Flask app.config (passed as param to allow using ThreadPoolExecutor)
    """
    skipBlur = pic.skip_blurring or config.get("API_BLUR_URL") is None
    fses = config["FILESYSTEMS"]
    fs = fses.permanent if skipBlur else fses.tmp
    picHdPath = utils.pictures.getHDPicturePath(pic.id)

    if not fs.exists(picHdPath):
        # if we were looking for the picture in the temporary fs ans it's not here, we check if it's in the permanent one
        # it can be the case when we try to reprocess an already processed picture
        if fs != fses.permanent and fses.permanent.exists(picHdPath):
            fs = fses.permanent
        else:
            raise Exception(f"Impossible to find picture file: {picHdPath}")

    with fs.openbin(picHdPath) as pictureBytes:
        # Create picture folders for this specific picture
        picDerivatesFolder = utils.pictures.getPictureFolderPath(pic.id)
        fses.derivates.makedirs(picDerivatesFolder, recreate=True)
        fses.permanent.makedirs(dirname(picHdPath), recreate=True)

        # Create blurred version if required
        if not skipBlur:
            with sentry_sdk.start_span(description="Blurring picture"):
                try:
                    picture = utils.pictures.createBlurredHDPicture(
                        fses.permanent,
                        config.get("API_BLUR_URL"),
                        pictureBytes,
                        picHdPath,
                    )
                except Exception as e:
                    log.exception(f"impossible to blur picture {pic.id}")
                    raise RecoverableProcessException("Blur API failure: " + errors.getMessageFromException(e)) from e

                # Delete original unblurred file
                geovisio.utils.filesystems.removeFsEvenNotFound(fses.tmp, picHdPath)

                # Cleanup parent folders
                parentFolders = picHdPath.split("/")
                parentFolders.pop()
                checkFolder = parentFolders.pop()
                while checkFolder:
                    currentFolder = "/".join(parentFolders) + "/" + checkFolder
                    if fses.tmp.exists(currentFolder) and fses.tmp.isempty(currentFolder):
                        geovisio.utils.filesystems.removeFsTreeEvenNotFound(fses.tmp, currentFolder)
                        checkFolder = parentFolders.pop()
                    else:
                        checkFolder = False

        else:
            # Make sure image rotation is always applied
            #  -> Not necessary on pictures from blur API, as SGBlur ensures rotation is always applied
            picture = Image.open(pictureBytes)
            picture = ImageOps.exif_transpose(picture)

        # Always pre-generate thumbnail
        utils.pictures.createThumbPicture(
            fses.derivates,
            picture,
            picDerivatesFolder + "/thumb.jpg",
            pic.metadata["type"],
        )

        # Create SD and tiles
        if config.get("PICTURE_PROCESS_DERIVATES_STRATEGY") == "PREPROCESS":
            utils.pictures.generatePictureDerivates(
                fses.derivates,
                picture,
                pic.metadata,
                picDerivatesFolder,
                pic.metadata["type"],
                skipThumbnail=True,
            )


class RecoverableProcessException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class RetryLaterProcessException(Exception):
    """Exception raised when we want to retry later, even if it's not an error"""

    def __init__(self, msg):
        super().__init__(msg)


class PictureProcessor:
    stop: bool
    config: dict[Any, Any]
    waiting_time: float

    def __init__(self, app, stop=True) -> None:
        self.app = app
        self.stop = stop
        if threading.current_thread() is threading.main_thread():
            # if worker is in daemon mode, register signals to gracefully stop it
            self._register_signals()
        self.next_periodic_task_dt = None
        self.cron = croniter(self.app.config["PICTURE_PROCESS_REFRESH_CRON"])

        # Note: in tests, we don't want to wait between each picture processing
        waiting_time = 0 if app.config.get("TESTING") is True else 1
        self.waiting_time = waiting_time

    def process_jobs(self):
        try:
            with self.app.app_context():
                while True:
                    if self.app.pool.closed and self.stop:
                        # in some tests, the pool is closed before the worker is stopped, we check this here
                        return
                    self.check_periodic_tasks()
                    r = process_next_job(self.app)
                    if not r:
                        if self.stop:
                            return
                        # no more picture to process
                        # wait a bit until there are some
                        import time

                        time.sleep(self.waiting_time)

        except:
            log.exception("Exiting thread")

    def _register_signals(self):
        import signal

        signal.signal(signal.SIGINT, self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)

    def _graceful_shutdown(self, *args):
        log.info("Stoping worker, waiting for last picture processing to finish...")
        self.stop = True

    def check_periodic_tasks(self):
        """
        Check if a periodic task needs to be done, and do it if necessary
        This method ensure only one picture worker will do the needed periodic task
        """
        if self.next_periodic_task_dt is None:
            with db.conn(self.app) as conn:
                self.next_periodic_task_dt = self.get_next_periodic_task_dt(conn)

        if datetime.now(timezone.utc) >= self.next_periodic_task_dt:
            with db.conn(self.app) as conn:
                # since the next_periodic_task_dt can have been changed by another process, we check again that the task needs to be done
                self.next_periodic_task_dt = self.get_next_periodic_task_dt(conn)
                if datetime.now(timezone.utc) >= self.next_periodic_task_dt:
                    if not self.refresh_database():
                        # another refresh is in progress, we'll check again later and ask for the next refresh date considering it's in progress
                        self.next_periodic_task_dt = self.cron.get_next(datetime, datetime.now(timezone.utc))
                        logging.getLogger("geovisio.periodic_task").info(
                            f"Refresh in progress, checking after = {self.next_periodic_task_dt}"
                        )

    def get_next_periodic_task_dt(self, conn) -> datetime:
        r = conn.execute("SELECT refreshed_at, NOW() FROM refresh_database").fetchone()
        assert r  # the table always has exactly one row

        refreshed_at, db_time = r
        current_time = datetime.now(timezone.utc)
        if refreshed_at is None:
            # if the db has never been updated, we need to update it now
            return current_time
        next_schedule_date = self.cron.get_next(datetime, refreshed_at)

        # if the db time and the app time is not the same, we need to apply an offset on the scheduled time
        next_schedule_date += db_time - current_time
        logging.getLogger("geovisio.periodic_task").info(f"Next database refresh = {next_schedule_date}")
        return next_schedule_date

    def refresh_database(self):
        with sentry_sdk.start_transaction(op="task", name="refresh_database"):
            # Note: there is a mechanism in `sequences.update_pictures_grid` to ensure that only one refresh can be done at one time, and it will update the `refreshed_at` value
            return utils.sequences.update_pictures_grid()


def process_next_job(app):
    with sentry_sdk.start_transaction(op="task", name="process_next_picture"):
        with _get_next_job(app) as job:
            if job is None:
                return False
            if job.task == ProcessTask.prepare and job.pic:
                with sentry_sdk.start_span(description="Processing picture") as span:
                    span.set_data("pic_id", job.pic.id)
                    with utils.time.log_elapsed(f"Processing picture {job.pic.id}"):
                        # open another connection for reporting and queries
                        processPictureFiles(job.pic, app.config)
            elif job.task == ProcessTask.delete and job.pic:
                with sentry_sdk.start_span(description="Deleting picture") as span:
                    span.set_data("pic_id", job.pic.id)
                    with utils.time.log_elapsed(f"Deleting picture {job.pic.id}"):
                        _delete_picture(job.pic)
            elif job.task == ProcessTask.dispatch and job.upload_set:
                with utils.time.log_elapsed(f"Dispatching upload set {job.upload_set.id}"):
                    try:
                        upload_set.dispatch(job.upload_set.id)
                    except Exception as e:
                        log.exception(f"impossible to dispatch upload set {job.upload_set.id}")
                        raise RecoverableProcessException("Upload set dispatch error: " + errors.getMessageFromException(e)) from e
            elif job.task == ProcessTask.finalize and job.seq:
                with utils.time.log_elapsed(f"Finalizing sequence {job.seq.id}"):
                    with job.reporting_conn.cursor(row_factory=dict_row) as cursor:
                        sequences.finalize(cursor, job.seq.id)
            else:
                raise RecoverableProcessException(f"Unhandled process task: {job.task}")

    return True


@contextmanager
def _get_next_job(app):
    """
    Open a new connection and return the next job to process
    Note: the job should be used as a context manager to close the connection when we stop using the returned job.

    The new connection is needed because we lock the `job_queue` for the whole transaction for another worker not to process the same job
    """
    error = None
    with app.pool.connection() as locking_transaction:
        with locking_transaction.transaction(), locking_transaction.cursor(row_factory=dict_row) as cursor:
            r = cursor.execute(
                """SELECT j.id, j.picture_id, j.upload_set_id, j.sequence_id, j.task, j.picture_to_delete_id, p.metadata, j.args
                FROM job_queue j
                LEFT JOIN pictures p ON p.id = j.picture_id
                ORDER by
                    j.nb_errors,
                    j.ts
                FOR UPDATE of j SKIP LOCKED
                LIMIT 1"""
            ).fetchone()
            if r is None:
                # Nothing to process
                yield None
            else:
                log.debug(f"Processing {r['id']}")

                # picture id can either be in `picture_id` (and it will be a foreign key to picture) or in `picture_to_delete_id`
                # (and it will not a foreign key since the picture's row will already have been deleted from the db)
                pic_id = r["picture_id"] or r["picture_to_delete_id"]
                db_pic = (
                    DbPicture(id=pic_id, metadata=r["metadata"], skip_blurring=(r["args"] or {}).get("skip_blurring", False))
                    if pic_id is not None
                    else None
                )
                db_seq = DbSequence(id=r["sequence_id"]) if r["sequence_id"] is not None else None
                db_upload_set = DbUploadSet(id=r["upload_set_id"]) if r["upload_set_id"] is not None else None

                with app.pool.connection() as reporting_conn:
                    job = _initialize_job(
                        reporting_conn,
                        job_queue_id=r["id"],
                        db_pic=db_pic,
                        db_seq=db_seq,
                        db_upload_set=db_upload_set,
                        task=ProcessTask(r["task"]),
                        args=r["args"],
                    )
                    try:
                        yield job

                        # Finalize the picture process, set the picture status and remove the picture from the queue process
                        _finalize_job(locking_transaction, job)
                        log.debug(f"Job {job.label()} processed")
                    except RecoverableProcessException as e:
                        _mark_process_as_error(locking_transaction, job, e, recoverable=True)
                    except RetryLaterProcessException as e:
                        _mark_process_as_error(
                            locking_transaction,
                            job,
                            e,
                            recoverable=True,
                            mark_as_error=False,
                        )
                    except InterruptedError as interruption:
                        log.error(f"Interruption received, stoping job {job.label()}")
                        # starts a new connection, since the current one can be corrupted by the exception
                        with app.pool.connection() as t:
                            _mark_process_as_error(t, job, interruption, recoverable=True)
                        error = interruption
                    except Exception as e:
                        log.exception(f"Impossible to finish job {job.label()}")
                        _mark_process_as_error(locking_transaction, job, e, recoverable=False)

                        # try to finalize the sequence anyway
                        _finalize_sequence(job)
                        error = e

    # we raise an error after the transaction has been comited to be sure to have the state persisted in the database
    if error:
        raise error


def _finalize_sequence(job: DbJob):
    # on picture preparation finalization, we add a sequence/upload_set finalization job
    if job.task != "prepare" or not job.pic:
        return

    with job.reporting_conn.cursor(row_factory=dict_row) as cursor:
        r = cursor.execute(
            "SELECT upload_set_id, seq_id FROM pictures p LEFT JOIN sequences_pictures sp on sp.pic_id = p.id WHERE p.id = %(pic_id)s",
            {"pic_id": job.pic.id},
        ).fetchone()

        if not r or not r["seq_id"]:
            # if the associated upload set has not yet been dispatch, the picture might not be associated to a sequence
            return

        if r["upload_set_id"]:
            # if the picture is part of the upload set, the sequence finalization will be done when the upload set is dispatched
            return

        # Add a task to finalize the sequence/upload_set
        sequences.add_finalization_job(cursor, r["seq_id"])


def _finalize_job(conn, job: DbJob):
    try:
        # we try to see if our job_history row is still here.
        # It can have been removed if the object this job was preparing has been deleted during the process (since the job_history table store foreign keys)
        job.reporting_conn.execute(
            "SELECT id FROM job_history WHERE id = %(id)s FOR UPDATE NOWAIT",
            {"id": job.job_history_id},
        )
    except psycopg.errors.LockNotAvailable:
        logging.info(
            f"The job {job.job_history_id} ({job.label()}) has likely been deleted during the process (it can happen if the picture/upload_set/sequence has been deleted by another process), we don't need to finalize it"
        )
        return
    job.reporting_conn.execute(
        "UPDATE job_history SET finished_at = CURRENT_TIMESTAMP WHERE id = %(id)s",
        {"id": job.job_history_id},
    )
    if job.task == ProcessTask.prepare and job.pic:
        # Note: the status is slowly been deprecated by replacing it with more precise status, and in the end it will be removed
        job.reporting_conn.execute(
            "UPDATE pictures SET status = (CASE WHEN status = 'hidden' THEN 'hidden' ELSE 'ready' END)::picture_status, preparing_status = 'prepared' WHERE id = %(pic_id)s",
            {"pic_id": job.pic.id},
        )

        # Add a task to finalize the sequence
        _finalize_sequence(job)

    conn.execute("DELETE FROM job_queue WHERE id = %(job_id)s", {"job_id": job.job_queue_id})


def _initialize_job(
    reporting_conn: psycopg.Connection,
    job_queue_id: UUID,
    db_pic: Optional[DbPicture],
    db_seq: Optional[DbSequence],
    db_upload_set: Optional[DbUploadSet],
    task: ProcessTask,
    args: Optional[Dict[Any, Any]],
) -> DbJob:
    r = reporting_conn.execute(
        """INSERT INTO job_history(job_id, picture_id, sequence_id, upload_set_id, picture_to_delete_id, job_task, args)
    VALUES (%(job_id)s, %(pic_id)s, %(seq_id)s, %(us_id)s, %(pic_to_delete)s, %(task)s, %(args)s)
    RETURNING id""",
        {
            "job_id": job_queue_id,
            "pic_id": db_pic.id if db_pic and task != ProcessTask.delete else None,
            "seq_id": db_seq.id if db_seq else None,
            "pic_to_delete": db_pic.id if db_pic and task == ProcessTask.delete else None,
            "us_id": db_upload_set.id if db_upload_set else None,
            "task": task.value,
            "args": Jsonb(args),
        },
    ).fetchone()

    if not r:
        raise Exception("impossible to insert task in database")

    return DbJob(
        reporting_conn=reporting_conn,
        job_queue_id=job_queue_id,
        pic=db_pic,
        seq=db_seq,
        upload_set=db_upload_set,
        task=task,
        job_history_id=r[0],
    )


def _mark_process_as_error(
    conn,
    job: DbJob,
    e: Exception,
    recoverable: bool = False,
    mark_as_error: bool = True,
):
    job.reporting_conn.execute(
        """UPDATE job_history SET
			error = %(err)s, finished_at = CURRENT_TIMESTAMP
		WHERE id = %(id)s""",
        {"err": str(e), "id": job.job_history_id},
    )
    if recoverable:
        if mark_as_error:
            nb_error = conn.execute(
                """UPDATE job_queue SET
                    nb_errors = nb_errors + 1
                WHERE id = %(id)s
                RETURNING nb_errors""",
                {"err": str(e), "id": job.job_queue_id},
            ).fetchone()
            if nb_error and nb_error[0] > PROCESS_MAX_RETRY:
                logging.info(f"Job {job.label()} has failed {nb_error} times, we stop trying to process it.")
                recoverable = False
        else:
            # it's not a real error, we just want to retry later
            conn.execute(
                SQL("UPDATE job_queue SET ts = NOW() WHERE id = %(id)s"),
                {"err": str(e), "id": job.job_queue_id},
            )

    if not recoverable:
        # Note: the status is slowly been deprecated by replacing it with more precise status, and in the end it will be removed
        if job.task == "prepare" and job.pic:
            job.reporting_conn.execute(
                """UPDATE pictures SET
                    preparing_status = 'broken', status = 'broken'
                WHERE id = %(id)s""",
                {"id": job.pic.id},
            )
        # on unrecoverable error, we remove the job from the queue
        conn.execute("DELETE FROM job_queue WHERE id = %(id)s", {"id": job.job_queue_id})


def _delete_picture(pic: DbPicture):
    """Delete a picture from the filesystem"""
    log.debug(f"Deleting picture files {pic.id}")
    utils.pictures.removeAllFiles(pic.id)

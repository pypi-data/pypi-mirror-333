import psycopg
from flask import current_app, url_for
from flask_babel import gettext as _
from psycopg.types.json import Jsonb
from psycopg.sql import SQL, Composable
from psycopg.rows import dict_row
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
import datetime
from uuid import UUID
from enum import Enum
from geovisio.utils import db
from geovisio.utils.auth import Account
from geovisio.utils.fields import FieldMapping, SortBy, SQLDirection, BBox, Bounds
from geopic_tag_reader import reader
from pathlib import PurePath
from geovisio import errors, utils
import logging
import sentry_sdk


def createSequence(metadata, accountId, user_agent: Optional[str] = None) -> UUID:
    with db.execute(
        current_app,
        "INSERT INTO sequences(account_id, metadata, user_agent) VALUES(%s, %s, %s) RETURNING id",
        [accountId, Jsonb(metadata), user_agent],
    ) as r:
        seqId = r.fetchone()
        if seqId is None:
            raise Exception("impossible to insert sequence in database")
        return seqId[0]


# Mappings from stac name to SQL names
STAC_FIELD_MAPPINGS = {
    p.stac: p
    for p in [
        FieldMapping(sql_column=SQL("inserted_at"), stac="created"),
        FieldMapping(sql_column=SQL("updated_at"), stac="updated"),
        FieldMapping(sql_column=SQL("computed_capture_date"), stac="datetime"),
        FieldMapping(sql_column=SQL("status"), stac="status"),
    ]
}
STAC_FIELD_TO_SQL_FILTER = {p.stac: p.sql_filter.as_string(None) for p in STAC_FIELD_MAPPINGS.values()}


@dataclass
class Collections:
    """
    Collections as queried from the database
    """

    collections: List[Dict[Any, Any]] = field(default_factory=lambda: [])
    # Bounds of the field used by the first field of the `ORDER BY` (usefull especially for pagination)
    query_first_order_bounds: Optional[Bounds] = None


@dataclass
class CollectionsRequest:
    sort_by: SortBy
    min_dt: Optional[datetime.datetime] = None
    max_dt: Optional[datetime.datetime] = None
    created_after: Optional[datetime.datetime] = None
    created_before: Optional[datetime.datetime] = None
    user_id: Optional[UUID] = None
    bbox: Optional[BBox] = None
    user_filter: Optional[SQL] = None
    pagination_filter: Optional[SQL] = None
    limit: int = 100
    userOwnsAllCollections: bool = False  # bool to represent that the user's asking for the collections is the owner of them

    def filters(self):
        return [f for f in (self.user_filter, self.pagination_filter) if f is not None]


def get_collections(request: CollectionsRequest) -> Collections:
    # Check basic parameters
    seq_filter: List[Composable] = []
    seq_params: dict = {}

    # Sort-by parameter
    # Note for review: I'm not sure I understand this non nullity constraint, but if so, shouldn't all sortby fields be added ?
    # for s in request.sort_by.fields:
    #     sqlConditionsSequences.append(SQL("{field} IS NOT NULL").format(field=s.field.sql_filter))
    seq_filter.append(SQL("{field} IS NOT NULL").format(field=request.sort_by.fields[0].field.sql_filter))
    seq_filter.extend(request.filters())

    if request.user_id is not None:
        seq_filter.append(SQL("s.account_id = %(account)s"))
        seq_params["account"] = request.user_id

    user_filter_str = request.user_filter.as_string(None) if request.user_filter is not None else None
    if user_filter_str is None or "status" not in user_filter_str:
        # if the filter does not contains any `status` condition, we want to show only 'ready' collection to the general users, and non deleted one for the owner
        if not request.userOwnsAllCollections:
            seq_filter.append(SQL("status = 'ready'"))
        else:
            seq_filter.append(SQL("status != 'deleted'"))
    else:
        if not request.userOwnsAllCollections and "'deleted'" not in user_filter_str:
            # if there are status filter and we ask for deleted sequence, we also include hidden one and consider them as deleted
            seq_filter.append(SQL("status <> 'hidden'"))

    status_field = None
    if request.userOwnsAllCollections:
        # only logged users can see detailed status
        status_field = SQL("s.status AS status")
    else:
        # hidden sequence are marked as deleted, this way crawler can update their catalog
        status_field = SQL("CASE WHEN s.status IN ('hidden', 'deleted') THEN 'deleted' ELSE s.status END AS status")

    # Datetime
    if request.min_dt is not None:
        seq_filter.append(SQL("s.computed_capture_date >= %(cmindate)s::date"))
        seq_params["cmindate"] = request.min_dt
    if request.max_dt is not None:
        seq_filter.append(SQL("s.computed_capture_date <= %(cmaxdate)s::date"))
        seq_params["cmaxdate"] = request.max_dt

    if request.bbox is not None:
        seq_filter.append(SQL("ST_Intersects(s.geom, ST_MakeEnvelope(%(minx)s, %(miny)s, %(maxx)s, %(maxy)s, 4326))"))
        seq_params["minx"] = request.bbox.minx
        seq_params["miny"] = request.bbox.miny
        seq_params["maxx"] = request.bbox.maxx
        seq_params["maxy"] = request.bbox.maxy

    # Created after/before
    if request.created_after is not None:
        seq_filter.append(SQL("s.inserted_at > %(created_after)s::timestamp with time zone"))
        seq_params["created_after"] = request.created_after

    if request.created_before:
        seq_filter.append(SQL("s.inserted_at < %(created_before)s::timestamp with time zone"))
        seq_params["created_before"] = request.created_before

    with utils.db.cursor(current_app, row_factory=dict_row) as cursor:
        sqlSequencesRaw = SQL(
            """
            SELECT
                s.id,
                s.status,
                s.metadata->>'title' AS name,
                s.inserted_at AS created,
                s.updated_at AS updated,
                ST_XMin(s.bbox) AS minx,
                ST_YMin(s.bbox) AS miny,
                ST_XMax(s.bbox) AS maxx,
                ST_YMax(s.bbox) AS maxy,
                accounts.name AS account_name,
                s.account_id AS account_id,
                ST_X(ST_PointN(ST_GeometryN(s.geom, 1), 1)) AS x1,
                ST_Y(ST_PointN(ST_GeometryN(s.geom, 1), 1)) AS y1,
                s.min_picture_ts AS mints,
                s.max_picture_ts AS maxts,
                s.nb_pictures AS nbpic,
                {status},
                s.computed_capture_date AS datetime,
                s.user_agent,
                ROUND(ST_Length(s.geom::geography)) / 1000 AS length_km,
                s.computed_h_pixel_density,
                s.computed_gps_accuracy,
                t.semantics
            FROM sequences s
            LEFT JOIN accounts on s.account_id = accounts.id
            LEFT JOIN (
                    SELECT sequence_id, json_agg(json_strip_nulls(json_build_object(
                        'key', key,
                        'value', value
                    ))) AS semantics
                    FROM sequences_semantics
                    GROUP BY sequence_id
                ) t ON t.sequence_id = s.id
            WHERE {filter}
            ORDER BY {order1}
            LIMIT {limit}
        """
        )
        sqlSequences = sqlSequencesRaw.format(
            filter=SQL(" AND ").join(seq_filter),
            order1=request.sort_by.as_sql(),
            limit=request.limit,
            status=status_field,
        )

        # Different request if we want the last n sequences
        #  Useful for paginating from last page to first
        if request.pagination_filter and (
            (
                request.sort_by.fields[0].direction == SQLDirection.ASC
                and request.pagination_filter.as_string(None).startswith(f"({request.sort_by.fields[0].field.sql_filter.as_string(None)} <")
            )
            or (
                request.sort_by.fields[0].direction == SQLDirection.DESC
                and request.pagination_filter.as_string(None).startswith(f"({request.sort_by.fields[0].field.sql_filter.as_string(None)} >")
            )
        ):
            base_query = sqlSequencesRaw.format(
                filter=SQL(" AND ").join(seq_filter),
                order1=request.sort_by.revert(),
                limit=request.limit,
                status=status_field,
            )
            sqlSequences = SQL(
                """
                SELECT *
                FROM ({base_query}) s
                ORDER BY {order2}
            """
            ).format(
                order2=request.sort_by.as_sql(),
                base_query=base_query,
            )

        records = cursor.execute(sqlSequences, seq_params).fetchall()

        query_bounds = None
        for s in records:
            first_order_val = s.get(request.sort_by.fields[0].field.stac)
            if first_order_val is None:
                continue
            if query_bounds is None:
                query_bounds = Bounds(first_order_val, first_order_val)
            else:
                query_bounds.update(first_order_val)

        return Collections(
            collections=records,
            query_first_order_bounds=query_bounds,
        )


def get_pagination_links(
    route: str,
    routeArgs: dict,
    field: str,
    direction: SQLDirection,
    datasetBounds: Bounds,
    dataBounds: Optional[Bounds],
    additional_filters: Optional[str],
) -> List:
    """Computes STAC links to handle pagination"""

    sortby = f"{'+' if direction == SQLDirection.ASC else '-'}{field}"
    links = []
    if dataBounds is None:
        return links

    # Check if first/prev links are necessary
    if (direction == SQLDirection.ASC and datasetBounds.min < dataBounds.min) or (
        direction == SQLDirection.DESC and dataBounds.max < datasetBounds.max
    ):
        links.append(
            {
                "rel": "first",
                "type": "application/json",
                "href": url_for(route, _external=True, **routeArgs, filter=additional_filters, sortby=sortby),
            }
        )
        page_filter = f"{field} {'<' if direction == SQLDirection.ASC else '>'} '{dataBounds.min if direction == SQLDirection.ASC else dataBounds.max}'"
        links.append(
            {
                "rel": "prev",
                "type": "application/json",
                "href": url_for(
                    route,
                    _external=True,
                    **routeArgs,
                    sortby=sortby,
                    filter=additional_filters,
                    page=page_filter,
                ),
            }
        )

    # Check if next/last links are required
    if (direction == SQLDirection.ASC and dataBounds.max < datasetBounds.max) or (
        direction == SQLDirection.DESC and datasetBounds.min < dataBounds.min
    ):
        next_filter = f"{field} {'>' if direction == SQLDirection.ASC else '<'} '{dataBounds.max if direction == SQLDirection.ASC else dataBounds.min}'"
        last_filter = f"{field} {'<=' if direction == SQLDirection.ASC else '>='} '{datasetBounds.max if direction == SQLDirection.ASC else datasetBounds.min}'"
        links.append(
            {
                "rel": "next",
                "type": "application/json",
                "href": url_for(
                    route,
                    _external=True,
                    **routeArgs,
                    sortby=sortby,
                    filter=additional_filters,
                    page=next_filter,
                ),
            }
        )
        links.append(
            {
                "rel": "last",
                "type": "application/json",
                "href": url_for(
                    route,
                    _external=True,
                    **routeArgs,
                    sortby=sortby,
                    filter=additional_filters,
                    page=last_filter,
                ),
            }
        )

    return links


class Direction(Enum):
    """Represent the sort direction"""

    ASC = "+"
    DESC = "-"

    def is_reverse(self):
        return self == Direction.DESC


class CollectionSortOrder(Enum):
    """Represent the sort order"""

    FILE_DATE = "filedate"
    FILE_NAME = "filename"
    GPS_DATE = "gpsdate"


@dataclass
class CollectionSort:
    order: CollectionSortOrder
    direction: Direction

    def as_str(self) -> str:
        return f"{self.direction.value}{self.order.value}"


def sort_collection(db, collectionId: UUID, sortby: CollectionSort):
    """
    Sort a collection by a given parameter

    Note: the transaction is not commited at the end, you need to commit it or use an autocommit connection
    """

    # Remove existing order, and keep list of pictures IDs
    picIds = db.execute(
        SQL(
            """
            DELETE FROM sequences_pictures
            WHERE seq_id = %(id)s
            RETURNING pic_id
            """
        ),
        {"id": collectionId},
    ).fetchall()
    picIds = [p["pic_id"] for p in picIds]

    # Fetch metadata and EXIF tags of concerned pictures
    picMetas = db.execute(SQL("SELECT id, metadata, exif FROM pictures WHERE id = ANY(%s)"), [picIds]).fetchall()
    usedDateField = None
    isFileNameNumeric = False

    if sortby.order == CollectionSortOrder.FILE_NAME:
        # Check if filenames are numeric
        try:
            for pm in picMetas:
                int(PurePath(pm["metadata"]["originalFileName"] or "").stem)
            isFileNameNumeric = True
        except ValueError:
            pass

    if sortby.order == CollectionSortOrder.FILE_DATE:
        # Look out what EXIF field is used for storing dates in this sequence
        for field in [
            "Exif.Image.DateTimeOriginal",
            "Exif.Photo.DateTimeOriginal",
            "Exif.Image.DateTime",
            "Xmp.GPano.SourceImageCreateTime",
        ]:
            if field in picMetas[0]["exif"]:
                usedDateField = field
                break

        if usedDateField is None:
            raise errors.InvalidAPIUsage(
                _("Sort by file date is not possible on this sequence (no file date information available on pictures)"),
                status_code=422,
            )

    for pm in picMetas:
        # Find value for wanted sort
        if sortby.order == CollectionSortOrder.GPS_DATE:
            if "ts_gps" in pm["metadata"]:
                pm["sort"] = pm["metadata"]["ts_gps"]
            else:
                pm["sort"] = reader.decodeGPSDateTime(pm["exif"], "Exif.GPSInfo", _)[0]
        elif sortby.order == CollectionSortOrder.FILE_DATE:
            if "ts_camera" in pm["metadata"]:
                pm["sort"] = pm["metadata"]["ts_camera"]
            else:
                assert usedDateField  # nullity has been checked before
                pm["sort"] = reader.decodeDateTimeOriginal(pm["exif"], usedDateField, _)[0]
        elif sortby.order == CollectionSortOrder.FILE_NAME:
            pm["sort"] = pm["metadata"].get("originalFileName")
            if isFileNameNumeric:
                pm["sort"] = int(PurePath(pm["sort"]).stem)

        # Fail if sort value is missing
        if pm["sort"] is None:
            raise errors.InvalidAPIUsage(
                _(
                    "Sort using %(sort)s is not possible on this sequence, picture %(pic)s is missing mandatory metadata",
                    sort=sortby,
                    pic=pm["id"],
                ),
                status_code=422,
            )

    # Actual sorting of pictures
    picMetas.sort(key=lambda p: p["sort"], reverse=sortby.direction.is_reverse())
    picForDb = [(collectionId, i + 1, p["id"]) for i, p in enumerate(picMetas)]

    # Inject back pictures in sequence
    db.executemany(
        SQL(
            """
            INSERT INTO sequences_pictures(seq_id, rank, pic_id)
            VALUES (%s, %s, %s)
            """
        ),
        picForDb,
    )


def update_headings(
    db,
    sequenceId: UUID,
    editingAccount: Optional[UUID] = None,
    relativeHeading: int = 0,
    updateOnlyMissing: bool = True,
):
    """Defines pictures heading according to sequence path.
    Database is not committed in this function, to make entry definitively stored
    you have to call db.commit() after or use an autocommit connection.

    Parameters
    ----------
    db : psycopg.Connection
            Database connection
    sequenceId : uuid
            The sequence's uuid, as stored in the database
    relativeHeading : int
            Camera relative orientation compared to path, in degrees clockwise.
            Example: 0° = looking forward, 90° = looking to right, 180° = looking backward, -90° = looking left.
    updateOnlyMissing : bool
            If true, doesn't change existing heading values in database
    """

    db.execute(
        SQL(
            """
		WITH h AS (
			SELECT
				p.id,
                p.heading AS old_heading,
				CASE
					WHEN LEAD(sp.rank) OVER othpics IS NULL AND LAG(sp.rank) OVER othpics IS NULL
						THEN NULL
					WHEN LEAD(sp.rank) OVER othpics IS NULL
						THEN (360 + FLOOR(DEGREES(ST_Azimuth(LAG(p.geom) OVER othpics, p.geom)))::int + (%(diff)s %% 360)) %% 360
					ELSE
						(360 + FLOOR(DEGREES(ST_Azimuth(p.geom, LEAD(p.geom) OVER othpics)))::int + (%(diff)s %% 360)) %% 360
				END AS heading
			FROM pictures p
			JOIN sequences_pictures sp ON sp.pic_id = p.id AND sp.seq_id = %(seq)s
			WINDOW othpics AS (ORDER BY sp.rank)
		) 
		UPDATE pictures p
		SET heading = h.heading, heading_computed = true {editing_account}
		FROM h
		WHERE h.id = p.id {update_missing}
		"""
        ).format(
            update_missing=SQL(" AND (p.heading IS NULL OR p.heading = 0 OR p.heading_computed)") if updateOnlyMissing else SQL(""),
            editing_account=SQL(", last_account_to_edit = %(account)s") if editingAccount is not None else SQL(""),
        ),  # lots of camera have heading set to 0 for unset heading, so we recompute the heading when it's 0 too, even if this could be a valid value
        {"seq": sequenceId, "diff": relativeHeading, "account": editingAccount},
    )


def add_finalization_job(cursor, seqId: UUID):
    """
    Add a sequence finalization job in the queue.
    If there is already a finalization job, do nothing (changing it might cause a deadlock, since a worker could be processing this job)
    """
    cursor.execute(
        """INSERT INTO 
        job_queue(sequence_id, task)
        VALUES (%(seq_id)s, 'finalize')
        ON CONFLICT (sequence_id) DO NOTHING""",
        {"seq_id": seqId},
    )


def finalize(cursor, seqId: UUID, logger: logging.Logger = logging.getLogger()):
    """
    Finalize a sequence, by updating its status and computed fields.
    """
    with sentry_sdk.start_span(description="Finalizing sequence") as span:
        span.set_data("sequence_id", seqId)
        logger.debug(f"Finalizing sequence {seqId}")

        with utils.time.log_elapsed(f"Finalizing sequence {seqId}"):
            # Complete missing headings in pictures
            update_headings(cursor, seqId)

            # Change sequence database status in DB
            # Also generates data in computed columns
            cursor.execute(
                """WITH
aggregated_pictures AS (
SELECT
    sp.seq_id, 
    MIN(p.ts::DATE) AS day,
    ARRAY_AGG(DISTINCT TRIM(
        CONCAT(p.metadata->>'make', ' ', p.metadata->>'model')
    )) AS models,
    ARRAY_AGG(DISTINCT p.metadata->>'type') AS types,
    ARRAY_AGG(DISTINCT p.h_pixel_density) AS reshpd,
    PERCENTILE_CONT(0.9) WITHIN GROUP(ORDER BY p.gps_accuracy_m) AS gpsacc
FROM sequences_pictures sp
JOIN pictures p ON sp.pic_id = p.id
WHERE sp.seq_id = %(seq)s
GROUP BY sp.seq_id
)
UPDATE sequences
SET
status = CASE WHEN status = 'hidden' THEN 'hidden'::sequence_status ELSE 'ready'::sequence_status END, -- we don't want to change status if it's hidden
geom = compute_sequence_geom(id),
bbox = compute_sequence_bbox(id),
computed_type = CASE WHEN array_length(types, 1) = 1 THEN types[1] ELSE NULL END,
computed_model = CASE WHEN array_length(models, 1) = 1 THEN models[1] ELSE NULL END,
computed_capture_date = day,
computed_h_pixel_density = CASE WHEN array_length(reshpd, 1) = 1 THEN reshpd[1] ELSE NULL END,
computed_gps_accuracy = gpsacc
FROM aggregated_pictures
WHERE id = %(seq)s
            """,
                {"seq": seqId},
            )

            logger.info(f"Sequence {seqId} is ready")


def update_pictures_grid() -> Optional[datetime.datetime]:
    """Refreshes the pictures_grid materialized view for an up-to-date view of pictures availability on map.

    Parameters
    ----------
    db : psycopg.Connection
            Database connection

    Returns
    -------
    bool : True if the view has been updated else False
    """
    from geovisio.utils import db

    logger = logging.getLogger("geovisio.picture_grid")

    # get a connection outside of the connection pool in order to avoid
    # the default statement timeout as this query can be very long
    with db.long_queries_conn(current_app) as conn, conn.transaction():
        try:
            conn.execute("SELECT refreshed_at FROM refresh_database FOR UPDATE NOWAIT").fetchone()
        except psycopg.errors.LockNotAvailable:
            logger.info("Database refresh already in progress, nothing to do")
            return False

        with sentry_sdk.start_span(description="Refreshing database"):
            with utils.time.log_elapsed("Refreshing database", logger=logger):
                logger.info("Refreshing database")
                conn.execute("UPDATE refresh_database SET refreshed_at = NOW()")
                conn.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY pictures_grid")

    return True


def delete_collection(collectionId: UUID, account: Optional[Account]) -> int:
    """
    Mark a collection as deleted and delete all it's pictures.

    Note that since the deletion as asynchronous, some workers need to be run in order for the deletion to be effective.
    """
    with db.conn(current_app) as conn:
        with conn.transaction(), conn.cursor() as cursor:
            sequence = cursor.execute(
                "SELECT status, account_id FROM sequences WHERE id = %s AND status != 'deleted'", [collectionId]
            ).fetchone()

            # sequence not found
            if not sequence:
                raise errors.InvalidAPIUsage(_("Collection %(c)s wasn't found in database", c=collectionId), status_code=404)

            # Account associated to sequence doesn't match current user
            if account is not None and account.id != str(sequence[1]):
                raise errors.InvalidAPIUsage("You're not authorized to edit this sequence", status_code=403)

            logging.info(f"Asking for deletion of sequence {collectionId} and all its pictures")

            # mark all the pictures as waiting for deletion for async removal as this can be quite long if the storage is slow and there are lots of pictures
            # Note: To avoid a deadlock if some workers are currently also working on those picture to prepare them,
            # the SQL queries are split in 2:
            # - First a query to remove jobs preparing those pictures
            # - Then a query deleting those pictures from the database (and a trigger will add async deletion tasks to the queue)
            #
            # Since the workers lock their job_queue row when working, at the end of this query, we know that there are no more workers working on those pictures,
            # so we can delete them without fearing a deadlock.
            cursor.execute(
                """WITH pic2rm AS (
                    SELECT pic_id FROM sequences_pictures WHERE seq_id = %(seq)s
                ),
                picWithoutOtherSeq AS (
                    SELECT pic_id FROM pic2rm
                    EXCEPT
                    SELECT pic_id FROM sequences_pictures WHERE pic_id IN (SELECT pic_id FROM pic2rm) AND seq_id != %(seq)s
                )
                DELETE FROM job_queue WHERE picture_id IN (SELECT pic_id FROM picWithoutOtherSeq)""",
                {"seq": collectionId},
            ).rowcount
            # if there was a finalize task for this collection in the queue, we remove it, it's useless
            cursor.execute("""DELETE FROM job_queue WHERE sequence_id = %(seq)s""", {"seq": collectionId})

            # after the task have been added to the queue, delete the pictures, and db triggers will ensure the correct deletion jobs are added
            nb_updated = cursor.execute(
                """WITH pic2rm AS (
                    SELECT pic_id FROM sequences_pictures WHERE seq_id = %(seq)s
                ),
                picWithoutOtherSeq AS (
                    SELECT pic_id FROM pic2rm
                    EXCEPT
                    SELECT pic_id FROM sequences_pictures WHERE pic_id IN (SELECT pic_id FROM pic2rm) AND seq_id != %(seq)s
                )
                DELETE FROM pictures WHERE id IN (SELECT pic_id FROM picWithoutOtherSeq)""",
                {"seq": collectionId},
            ).rowcount

            cursor.execute("UPDATE sequences SET status = 'deleted' WHERE id = %s", [collectionId])
            return nb_updated

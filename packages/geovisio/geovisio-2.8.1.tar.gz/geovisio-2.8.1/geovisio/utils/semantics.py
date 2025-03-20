from dataclasses import dataclass
from uuid import UUID
from psycopg import Cursor
from psycopg.sql import SQL, Identifier
from psycopg.types.json import Jsonb
from psycopg.errors import UniqueViolation
from pydantic import BaseModel, ConfigDict, Field
from typing import List
from enum import Enum

from geovisio import errors


class TagAction(str, Enum):
    """Actions to perform on a tag list"""

    add = "add"
    delete = "delete"


class SemanticTagUpdate(BaseModel):
    """Parameters used to update a tag list"""

    action: TagAction = Field(default=TagAction.add)
    """Action to perform on the tag list. The default action is `add` which will add the given tag to the list.
    The action can also be to `delete` the key/value"""
    key: str = Field(max_length=256)
    """Key of the tag to update limited to 256 characters"""
    value: str = Field(max_length=2048)
    """Value of the tag to update limited ot 2048 characters"""

    model_config = ConfigDict(use_attribute_docstrings=True)


class SemanticTag(BaseModel):
    key: str
    """Key of the tag"""
    value: str
    """Value of the tag"""


class EntityType(Enum):

    pic = "picture_id"
    seq = "sequence_id"
    annotation = "annotation_id"

    def entitiy_id_field(self) -> Identifier:
        return Identifier(self.value)


@dataclass
class Entity:
    type: EntityType
    id: UUID

    def get_table(self) -> Identifier:
        match self.type:
            case EntityType.pic:
                return Identifier("pictures_semantics")
            case EntityType.seq:
                return Identifier("sequences_semantics")
            case EntityType.annotation:
                return Identifier("annotations_semantics")
            case _:
                raise ValueError(f"Unknown entity type: {self.type}")

    def get_history_table(self) -> Identifier:
        match self.type:
            case EntityType.pic:
                return Identifier("pictures_semantics_history")
            case EntityType.seq:
                return Identifier("sequences_semantics_history")
            case EntityType.annotation:
                return Identifier("annotations_semantics_history")
            case _:
                raise ValueError(f"Unknown entity type: {self.type}")


def update_tags(cursor: Cursor, entity: Entity, actions: List[SemanticTagUpdate], account: UUID) -> SemanticTag:
    """Update tags for an entity
    Note: this should be done inside an autocommit transaction
    """
    table_name = entity.get_table()
    fields = [entity.type.entitiy_id_field(), Identifier("key"), Identifier("value")]
    tag_to_add = [t for t in actions if t.action == TagAction.add]
    tag_to_delete = [t for t in actions if t.action == TagAction.delete]
    try:
        if tag_to_delete:
            cursor.execute(SQL("CREATE TEMPORARY TABLE tags_to_delete(key TEXT, value TEXT) ON COMMIT DROP"))
            with cursor.copy(SQL("COPY tags_to_delete (key, value) FROM STDIN")) as copy:
                for tag in tag_to_delete:
                    copy.write_row((tag.key, tag.value))
            cursor.execute(
                SQL(
                    """DELETE FROM {table}
    WHERE {entity_id} = %(entity)s 
    AND (key, value) IN (
        SELECT key, value FROM tags_to_delete
    )"""
                ).format(table=table_name, entity_id=entity.type.entitiy_id_field()),
                {"entity": entity.id, "key_values": [(t.key, t.value) for t in tag_to_delete]},
            )
        if tag_to_add:
            with cursor.copy(SQL("COPY {table} ({fields}) FROM STDIN").format(table=table_name, fields=SQL(",").join(fields))) as copy:
                for tag in tag_to_add:
                    copy.write_row((entity.id, tag.key, tag.value))
        if tag_to_add or tag_to_delete:
            # we track the history changes of the semantic tags
            cursor.execute(
                SQL("INSERT INTO {history_table} ({entity_id_field}, account_id, updates) VALUES (%(id)s, %(account)s, %(tags)s)").format(
                    history_table=entity.get_history_table(), entity_id_field=entity.type.entitiy_id_field()
                ),
                {"id": entity.id, "account": account, "tags": Jsonb([t.model_dump() for t in tag_to_add + tag_to_delete])},
            )
    except UniqueViolation as e:
        # if the tag already exists, we don't want to add it again
        raise errors.InvalidAPIUsage(
            "Impossible to add semantic tags because of duplicates", payload={"details": {"duplicate": e.diag.message_detail}}
        )

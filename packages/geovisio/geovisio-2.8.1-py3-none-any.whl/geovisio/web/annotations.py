from geovisio.utils import auth
from psycopg.rows import dict_row, class_row
from psycopg.sql import SQL
from geovisio.utils.semantics import Entity, EntityType, SemanticTagUpdate, update_tags
from geovisio.web.utils import accountIdOrDefault
from psycopg.types.json import Jsonb
from geovisio.utils import db
from geovisio.utils.params import validation_error
from geovisio import errors
from pydantic import BaseModel, ConfigDict, ValidationError
from uuid import UUID
from typing import List, Optional
from flask import Blueprint, request, current_app
from flask_babel import gettext as _


bp = Blueprint("annotations", __name__, url_prefix="/api")

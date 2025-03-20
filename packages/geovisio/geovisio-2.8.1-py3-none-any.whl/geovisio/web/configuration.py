import flask
from typing import Dict, Any
from flask import jsonify
from flask_babel import get_locale
from geovisio.web.utils import get_api_version

bp = flask.Blueprint("configuration", __name__, url_prefix="/api")


@bp.route("/configuration")
def configuration():
    """Return instance configuration informations
    ---
    tags:
        - Metadata
    responses:
        200:
            description: Information about the instance configuration
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioConfiguration'
    """

    apiSum = flask.current_app.config["API_SUMMARY"]
    userLang = get_locale().language
    return jsonify(
        {
            "name": _get_translated(apiSum.name, userLang),
            "description": _get_translated(apiSum.description, userLang),
            "geo_coverage": _get_translated(apiSum.geo_coverage, userLang),
            "logo": apiSum.logo,
            "color": str(apiSum.color),
            "email": apiSum.email,
            "auth": _auth_configuration(),
            "license": _license_configuration(),
            "version": get_api_version(),
            "pages": _get_pages(),
        }
    )


def _get_translated(prop: Dict[str, str], userLang) -> Dict[str, Any]:
    return {"label": prop.get(userLang, prop.get("en")), "langs": prop}


def _auth_configuration():
    from geovisio.utils import auth

    if auth.oauth_provider is None:
        return {"enabled": False}
    else:
        return {
            "enabled": True,
            "user_profile": {"url": auth.oauth_provider.user_profile_page_url()},
            "enforce_tos_acceptance": flask.current_app.config["API_ENFORCE_TOS_ACCEPTANCE"],
        }


def _license_configuration():
    l = {"id": flask.current_app.config["API_PICTURES_LICENSE_SPDX_ID"]}
    u = flask.current_app.config.get("API_PICTURES_LICENSE_URL")
    if u:
        l["url"] = u
    return l


def _get_pages():
    from geovisio.utils import db
    from flask import current_app

    pages = db.fetchall(current_app, "SELECT distinct(name) FROM pages")

    return [p[0] for p in pages]

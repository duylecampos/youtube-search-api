import json
from flask import Blueprint, jsonify, request

from app.services.youtube import Youtube

blueprint = Blueprint("movies", __name__)


@blueprint.route("/search", methods=["GET"])
def list():
    if "term" not in request.args:
        return jsonify({"error": "Search term is a required parameter"}), 403
    youtube = Youtube(request.args["term"])
    availability = json.loads(request.args.get("availability", []))

    return (
        jsonify(
            {
                "items": youtube.get_all(),
                "common_words": youtube.common_words(),
                "days_to_watch_all": youtube.days_to_watch_all(availability),
            }
        ),
        200,
    )

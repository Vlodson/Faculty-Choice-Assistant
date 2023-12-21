from flask import Blueprint, request, jsonify, abort

from backend.ontology.predef_queries_dict import PREDEF_QUERIES
from backend.ontology.queries import apply_query, query_results_to_table


bp = Blueprint("predef_queries", __name__)


@bp.route("/", methods=["GET"])
def predef_query():
    query = request.args.get("query", default=None)

    if query:
        return jsonify(query_results_to_table(apply_query(PREDEF_QUERIES[query])))

    return abort(400, '"query" parameter not faund')

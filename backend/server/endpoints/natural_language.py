from flask import Blueprint, abort, request, jsonify

from backend.llm.threads import (
    make_thread_for_user,
    retrieve_thread_for_user,
    send_setup_message,
    send_user_message,
    create_run_for_thread,
    retrieve_run_for_user,
    get_last_message,
    get_query_from_message,
)
from backend.ontology.queries import apply_query, query_results_to_table
from backend.server.endpoints.custom_types import SendMessageRequest, SetupUserResponse


bp = Blueprint("llm", __name__)


@bp.route("/setup", methods=["GET"])
def setup_user() -> SetupUserResponse:
    thread = make_thread_for_user()
    _ = send_setup_message(thread)
    run = create_run_for_thread(thread)  # for easier expansion of the API

    return jsonify({"thread_id": thread.id, "run_id": run.id})


@bp.route("/message", methods=["POST"])
def send_message():
    body: SendMessageRequest = request.get_json()

    if "thread_id" not in body or "run_id" not in body or "msg" not in body:
        return abort(400, "thread_id, run_id or msg not found in POST body")

    thread = retrieve_thread_for_user(body["thread_id"])
    run = retrieve_run_for_user(body["run_id"], body["thread_id"])

    _ = send_user_message(thread=thread, msg=body["msg"])
    run = create_run_for_thread(thread, run)

    return jsonify({"thread_id": thread.id, "run_id": run.id})


@bp.route("/query_results", methods=["GET"])
def get_query_results():
    thread_id = request.args.get("thread_id", default=None)
    run_id = request.args.get("run_id", default=None)

    if not thread_id or not run_id:
        return abort(400, "thread_id or run_id not found in GET parameters")

    thread = retrieve_thread_for_user(thread_id)
    run = retrieve_run_for_user(run_id, thread_id)

    query = get_query_from_message(get_last_message(thread, run))
    if query:
        return jsonify(query_results_to_table(apply_query(query)))

    return jsonify("No answer for query")

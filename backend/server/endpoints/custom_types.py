from typing import TypedDict


class SetupUserResponse(TypedDict):
    thread_id: str
    run_id: str


class SendMessageRequest(TypedDict):
    thread_id: str
    run_id: str
    msg: str

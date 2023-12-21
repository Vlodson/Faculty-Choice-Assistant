from typing import Optional
from openai.types.beta.thread import Thread
from openai.types.beta.threads import ThreadMessage, Run
from backend.llm.assistant import CLIENT, ASSISTANT


def make_thread_for_user() -> Thread:
    return CLIENT.beta.threads.create()


def retrieve_thread_for_user(thread_id: str) -> Thread:
    return CLIENT.beta.threads.retrieve(thread_id=thread_id)


def __contextualize_user_message(msg: str) -> str:
    return f'Write a SPARQL query for the following question: "{msg}"'


def send_setup_message(thread: Thread) -> ThreadMessage:
    msg = (
        "The file ontology.ttl has an RDF ontology in turtle syntax. "
        + "Please review the contents of the file. "
        + "After that each prompt will ask you to create a SPARQL query for a certain question, "
        + "using ONLY information from ontology.ttl. "
        + "Always add: PREFIX edu: <file:///C:/Users/vlada/Desktop/Faks/SW/source/ontology/ontology.ttl#> to your queries"
    )
    return CLIENT.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=msg
    )


def send_user_message(thread: Thread, msg: str) -> ThreadMessage:
    return CLIENT.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=__contextualize_user_message(msg)
    )


def create_run_for_thread(thread: Thread, run: Optional[Run] = None) -> Run:
    if not run:
        return CLIENT.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=ASSISTANT.id
        )

    run_info = retrieve_run_for_user(run_id=run.id, thread_id=thread.id)
    while run.status != "completed":
        run_info = retrieve_run_for_user(run_id=run_info.id, thread_id=thread.id)

    return CLIENT.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=ASSISTANT.id
    )


def retrieve_run_for_user(run_id: str, thread_id: str) -> Run:
    return CLIENT.beta.threads.runs.retrieve(run_id=run_id, thread_id=thread_id)


def get_last_message(thread: Thread, run: Run) -> ThreadMessage:
    # wait untill the message is done writing
    # this does not have any fail exits
    run_info = CLIENT.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread.id)
    while run_info.status != "completed":
        run_info = CLIENT.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread.id)

    return list(msg for msg in CLIENT.beta.threads.messages.list(thread.id))[0]


def get_query_from_message(msg: ThreadMessage) -> Optional[str]:
    raw_msg = msg.content[0].text.value
    start_delim = r"```sparql"
    end_delim = r"```"

    start_index = raw_msg.find(start_delim)
    end_index = raw_msg.find(end_delim, start_index + len(start_delim))

    if start_index != -1 and end_index != -1:
        return raw_msg[start_index + len(start_delim) : end_index]

    return None

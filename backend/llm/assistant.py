# there also exists AsyncOpenAI, but all creates now have to await
from openai import OpenAI


API_KEY = r"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"
CLIENT = OpenAI(api_key=API_KEY)

# assistant made from browser
ASSISTANT = CLIENT.beta.assistants.retrieve(
    assistant_id="asst_zXpm82uj8S0tokdy6pEmUp7s"
)

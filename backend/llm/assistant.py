# there also exists AsyncOpenAI, but all creates now have to await
from openai import OpenAI


API_KEY = r"YOUR OPEN AI API KEY HERE"
CLIENT = OpenAI(api_key=API_KEY)

# assistant made from browser
ASSISTANT = CLIENT.beta.assistants.retrieve(
    assistant_id="YOUR ASSISTANT ID HERE"
)

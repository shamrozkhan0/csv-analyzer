from openai import OpenAI
from dotenv import load_dotenv
import logging as log

import os


load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def get_resposne(data, prompt):

    initial_message = [{
        "role": "system",
        "content" : f"You are an AI Assistant that  {data}"
    },
        {
            "role" : "user",
            "content" : prompt
        }
    ]

    # response = client.responses.create(
    #     input="Explain the importance of fast language models",
    #     model="openai/gpt-oss-20b",
    # )

    # print(initial_message)
    # print(prompt)

    log.info("successfully fetch response")

    return data
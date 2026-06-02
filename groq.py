from openai import OpenAI
import os
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def resposne(data, prompt):

    initial_message = [{
        "role": "system",
        "content" : f"You are an AI Assistant that  {data}"
    },
        {
            "role" : "user",
            "content" : prompt
        }
    ]

    response = client.responses.create(
        input="Explain the importance of fast language models",
        model="openai/gpt-oss-20b",
    )
# print(response.output_text)

from dotenv import load_dotenv
from openai import OpenAI
import logging as log
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def get_resposne(analytics, prompt):

    system_prompt = f"""
    # analytics = build_analytics_summary(df)

    You are a data analyst assistant. The user has uploaded a CSV file.
    Here is the complete analytics summary of their dataset:
    
    --- DATASET SUMMARY ---
    {analytics}
    --- END SUMMARY ---

    RULES:
    - Answer ONLY questions related to this dataset.
    - If asked something unrelated (e.g. general coding, recipes, news), respond:
    "That question isn't related to the uploaded file. I can only answer questions about your dataset."
    - Be concise. Prioritize numbers and patterns.
    - Format all responses in Markdown (use tables, bold, bullet points where helpful).
    - Never make up data. If you're unsure, say so."""

    initial_message = [{
        "role": "system",
        "content": system_prompt
    },
        {
            "role" : "user",
            "content" : prompt
        }
    ]

    # response = client.responses.create(
    #     input=initial_message,
    #     model="openai/gpt-oss-20b",
    # )
    response = "wowwwww"

    print(system_prompt)

    log.info(response)
    log.info("successfully fetch response")
    return response

    # return  response.output[1].content[0].text




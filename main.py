import json
from plistlib import InvalidFileException

from fastapi.middleware.cors import CORSMiddleware
from database import Database as database, Database
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from Cleaner import start
from pathlib import Path
import logging as log
import random
import groq
import os


log.basicConfig(level=log.INFO, format="%(asctime)s %(levelname)s %(message)s")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials= False,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()


@app.get("/")
def show_home_page():
    return {"message": "Hello world"}



@app.post("/uploads")
async def uploads_files(file: UploadFile = File(...)):

    log.info("File upload request received")
    allowed_extension = [".csv"]
    file_extension = Path(file.filename).suffix.lower()

    try:

        if file_extension not in allowed_extension:
            raise InvalidFileException("File is not valid")

        id = int(random.random() * 10000000)
        filename = str(id) + '.csv' # Later this will changed to the following file extension
        file_path = f"{os.getenv('UPLOAD_PATH')}{filename}"

        with open(file_path, "wb") as file_writer:
            log.info(f"Saving to: {file_writer.name}")
            content = await file.read()
            file_writer.write(content)

        summary = start(filename)

        log.info("Successfully cleaned the file and generate analytics")

        d = Database()
        d.insert_analytics_into_database(summary,id)

        return {
            "status" : 200,
            "body": {
                "id": id,
            }
        }

    except InvalidFileException as e:
        log.error("")



@app.post("/ai/{file_id}")
def get_ai_response(file_id:int, prompt:str = Form(...)):
    try:

        d = Database()
        content = d.get_content_by_id(file_id)

        if content is None or content == "" or file_id is None:
            raise ValueError(f"Argument not found content or file id is empty")


        response = groq.get_resposne(content, prompt)

        conversation_json = {"prompt": prompt,"response": response}
        conversations = d.update_conversation_into_database(conversation_json, file_id)


        return {
            "status" : 200,
            "body" : {
                "response" : response,
                "conversations" : conversations
            }
        }

    except ValueError as e:
        log.info(f"Error: {e}")
        return {
            "status" : 404,
            "message" : e
        }


@app.get("/download/{filename}")
def download_file(filename: str):
    path = f"E:/CsvAnalyzer/cleaned/{filename}"
    return FileResponse(path, filename=filename)


@app.get("/get-conversation/{id}")
def get_conversations(id:int):
    d = Database()
    return d.get_conversation_by_id(id)





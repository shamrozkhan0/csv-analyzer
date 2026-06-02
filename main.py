from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File
from Cleaner import start
from dotenv import load_dotenv
from pathlib import Path
import groq

import logging as log
import random
import os

log.basicConfig(level=log.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


    if file_extension not in allowed_extension:
        return {"message": "File is not valid"}


    filename = f"{int(random.random() * 10000000)}.csv"
    file_path = f"{os.getenv('UPLOAD_PATH')}{filename}"

    with open(file_path, "wb") as file_writer:
        log.info(f"Saving to: {file_writer.name}")
        content = await file.read()
        file_writer.write(content)

    summary = start(filename)

    # return {"status": 200, "body": {
    #     "filename" : filename,
    #     "summary" : summary
    # }}

    response = groq.resposne(summary, )



# def ai_response():
#     summary = resposne()
#     return summary


@app.get("/download/{filename}")
def download_file(filename: str):
    path = f"E:/CsvAnalyzer/cleaned/{filename}"
    return FileResponse(path, filename=filename)





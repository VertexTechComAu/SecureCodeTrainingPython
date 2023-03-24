from fastapi import FastAPI, status, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
import os
import mimetypes
import sqlite3

# Initialize app
app = FastAPI()

app.mount("/storage", StaticFiles(directory="./"), name="public")


templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return "Upload Vulnerability"



@app.post("/upload")
def upload(file: UploadFile = File(...)):
    allowwed_mime_type = "text/plain"

    try:
        if file.content_type == allowwed_mime_type:
            contents = file.file.read()
        
            with open(file.filename, 'wb') as f:
                f.write(contents)
        else:
            return 'Invalid File Type, Only accept txt file'
    
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

@app.get("/upload", response_class=HTMLResponse)
async def read(request: Request):
    
    return templates.TemplateResponse("upload.html", {"request": request})  

@app.get("/file/{id}")
def read_todo(id ):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    #raw_sql = "SELECT * FROM todos WHERE user_id = "+user_id+" AND id = "+id

    query = """SELECT * FROM todos WHERE user_id = ? AND  id = ?"""
    tuple1 = (user_id, id)
    todo = cursor.execute(query, tuple1).fetchmany()

    #todo = cursor.execute(raw_sql).fetchmany()

    return f"task: {todo}"  


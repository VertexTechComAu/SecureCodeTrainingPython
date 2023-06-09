from fastapi import FastAPI, status, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
import os
import mimetypes


# Initialize app
app = FastAPI()

app.mount("/storage", StaticFiles(directory="./"), name="public")


templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return "Upload Vulnerability"

@app.get("/upload", response_class=HTMLResponse)
async def read(request: Request):
    
    return templates.TemplateResponse("upload.html", {"request": request})    


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    allowed_mime_type = "text/plain"

    try:
        mime_type = mimetypes.guess_type(file.filename)[0]
        if mime_type == allowed_mime_type:
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
import os
import tempfile
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import  RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import aiofiles


from utils.hf_inference import hf_inference_vid, hf_inference_img
from utils.save_file import save_file
from utils.config import white_list
from reports.reports import router


app = FastAPI()
origins = white_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)

# In a real application, consider using a database instead
videos = []


@app.post("/inference/general")
async def infer_general(file: UploadFile):
    vid_inference = False
    if  file.filename.lower().endswith(('.mp4', '.avi', '.mov')):
        vid_inference= True
    elif not file.filename.lower().endswith(('.jpeg', '.jpg', '.png','webm')):
        raise HTTPException(status_code=400, detail="Invalid file type")
    try:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        await save_file(file_path,file)
        res= hf_inference_vid(file_path) if vid_inference else hf_inference_img(file_path)
        return {"code":"success", "url":res}
    except Exception as e:
        print(f'exception {e}')


@app.post("/inference/image")
async def infer_image(file: UploadFile):
    print(file.filename)

    try:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        await save_file(file_path,file)
        res= hf_inference_img(file_path)
        return {"code":"success", "url":res}
    except Exception as e:
        print(f'exception {e}')


@app.get("/test")
def test_endpoints():
    return {"aa":"bb"}  


@app.post("/inference/video")
async def video_inference(video:UploadFile= File(...)):
    print("im here")
    # Validate file type
    if not video.filename.lower().endswith(('.mp4', '.avi', '.mov')):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Generate a unique filename
    file_extension = os.path.splitext(video.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    try:
        # Asynchronously save the file
        await save_file(file_path,video)
       
        # Process the video (implement this function according to your needs)
        inference_path = hf_inference_vid(file_path)
        if inference_path is not None:
            return {"status":"success", "url":inference_path}
        return {"status":"error", "msg":"error in file uploading" }
   

    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))
    


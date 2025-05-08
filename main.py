from fastapi import FastAPI, UploadFile, File, Form
from operations import save_file
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    save_to_supabase: bool = Form(False)
):

    result = await save_file(file, save_to_supabase)
    return result
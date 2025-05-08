import os
import uuid
from fastapi import UploadFile
from dotenv import load_dotenv
import aiofiles
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY=os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
SUPABASE_BUCKET=os.getenv("SUPABASE_BUCKET")


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def upload_file(file: UploadFile, filename:str):
    content = await file.read()
    file_name = f"image/{filename}"
    res = supabase.storage.from_(SUPABASE_BUCKET).upload(file_name, content,{"content-type":file.content_type})

    ##if res:
      ##  return {"error": res["error"]["message"]}

    file_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_name)

    return file_url


async def save_file(file: UploadFile, to_supabase: bool):
    if not file.content_type.startswith("image/"):
        return {"error": "Solo se permiten imágenes"}

    new_filename = f"{uuid.uuid4().hex}_{file.filename}"

    if to_supabase:
        return await upload_file(file, new_filename)
    else:
        return await save_to_local(file, new_filename)


async def save_to_local(file: UploadFile, filename: str):

    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", filename)

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    return {"filename": filename, "local_path": file_path}
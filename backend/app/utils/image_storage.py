import os
from typing import Optional
from fastapi import UploadFile
from PIL import Image
from io import BytesIO

BASE_UPLOAD_DIR = os.path.join("static", "uploads")

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

async def save_upload_file_as_jpg(upload: UploadFile, subdir: Optional[str] = None) -> str:
    # Ensure directory exists
    ensure_dir(BASE_UPLOAD_DIR if not subdir else os.path.join(BASE_UPLOAD_DIR, subdir))
    dir_path = BASE_UPLOAD_DIR if not subdir else os.path.join(BASE_UPLOAD_DIR, subdir)

    # Base filename (without extension)
    base, _ = os.path.splitext(upload.filename or "upload")
    dest_path = os.path.join(dir_path, f"{base}.jpg")

    # Avoid overwriting existing file
    i = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(dir_path, f"{base}_{i}.jpg")
        i += 1

    # Read and convert to JPEG
    content = await upload.read()
    img = Image.open(BytesIO(content))
    rgb_img = img.convert("RGB")  # ensures JPG is valid (removes alpha channel)
    rgb_img.save(dest_path, format="JPEG", quality=90)

    return dest_path

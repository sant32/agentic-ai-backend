from pathlib import Path

from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


async def save_upload_file(file: UploadFile):

    filename = Path(file.filename).suffix

    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)
    
    await file.close()

    return str(file_path)
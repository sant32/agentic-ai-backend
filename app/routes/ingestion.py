from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File
from app.core.dependencies import get_ingestion_service
from app.services.ingestion_service import IngestionService
from app.tasks.document_task import process_pdf
from app.utils.file_storage import save_upload_file
from app.core.auth_dependencies import get_current_user
from app.models.user import User


router = APIRouter()

@router.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    service: IngestionService = Depends(get_ingestion_service),
):
    
    return await service.ingest(file)


@router.post("/ingest-background")
async def ingest_background(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    pdf_path = await save_upload_file(file)

    # job_id = str(uuid4())

    task = await process_pdf.kiq(pdf_path=pdf_path, user_id=current_user.id)
    print("Task queued:", task)
    return {
        "status": "queued"
    }
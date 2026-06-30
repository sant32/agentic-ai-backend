from pathlib import Path
from app.tasks.broker import broker
from app.core.dependencies import create_ingestion_service

@broker.task
async def process_pdf(pdf_path: str, user_id: int,):


    service = create_ingestion_service()

    print("proceess")

    await service.ingest(pdf_path=pdf_path, user_id=user_id)

        
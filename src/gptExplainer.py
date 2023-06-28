import asyncio

from db_session import create_session
from models import Upload
from src.explainer.presentation_processing import process_presentation

session = create_session()


async def process_uploads():
    """
    Processes the pending uploads and generates explanations for each PowerPoint presentation.

    The function runs indefinitely, scanning the database for pending uploads and processing them.
    """
    while True:
        print("Scanning pending uploads...\n")

        pending_uploads = session.query(Upload).filter_by(status="pending").all()

        for upload in pending_uploads:
            upload_id = upload.id
            await process_presentation(upload_id)

        print("Sleeping for 10 seconds...\n")
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(process_uploads())

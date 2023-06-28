import json
import os
import asyncio

import openai
from src.explainer.presentation_processing import process_presentation
from src.explainer.exceptions import OpenAIError, PresentationProcessingError, SlideProcessingError


API_KEY = "API_KEY"
UPLOADS_DIR = "../uploads"
OUTPUTS_DIR = "../outputs"


async def process_file(file_path):
    """
    Processes a file by generating explanations for each slide in the PowerPoint presentation.

    Args:
        file_path (str): The path to the PowerPoint presentation file.
    """
    try:
        output_file = os.path.join(OUTPUTS_DIR, os.path.splitext(os.path.basename(file_path))[0] + ".json")

        openai.api_key = API_KEY

        print(f"Processing file: {file_path}\n")

        explanations = await process_presentation(file_path)

        # Save explanations to a JSON file
        with open(output_file, "w") as f:
            json.dump(explanations, f, indent=4)

        print(f"Explanations saved successfully for file: {file_path}")
    except OpenAIError as e:
        print(f"OpenAI error occurred while processing file {file_path}: {str(e)}")
    except PresentationProcessingError as e:
        print(f"Presentation processing error occurred while processing file {file_path}: {str(e)}")
    except SlideProcessingError as e:
        print(f"Slide processing error occurred while processing file {file_path}, slide {e.slide_num}: {str(e.message)}")


async def process_uploads_folder():
    """
    Processes the files in the 'uploads' folder and generates explanations for each PowerPoint presentation.

    The function runs indefinitely, scanning the 'uploads' folder every few seconds and processing new files.
    """
    while True:
        print("Scanning uploads folder...\n")
        files = os.listdir(UPLOADS_DIR)

        for file in files:
            file_path = os.path.join(UPLOADS_DIR, file)
            if file.endswith(".pptx") and not file.startswith("processed_"):
                await process_file(file_path)
                os.rename(file_path, os.path.join(UPLOADS_DIR, "processed_" + file))

        print("Sleeping for 10 seconds...\n")
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(process_uploads_folder())

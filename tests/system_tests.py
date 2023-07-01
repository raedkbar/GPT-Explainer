import asyncio
import os
import argparse
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
PRESENTATION_PATH = os.path.join(BASE_DIR, "..", "2slides.pptx").replace("\\", "/")


async def start_web_api():
    """
    Start the Web API by running the flask_web_API.py.py script.
    """
    print("Starting Web API...")
    path = os.path.abspath(os.path.join(BASE_DIR, "..", "src", "flask_web_API.py"))
    subprocess.Popen(["python", path], cwd=os.path.join(BASE_DIR, "..", "src"))


async def start_explainer():
    """
    Start the Explainer by running the gpt_explainer.py script.
    """
    print("Starting Explainer...")
    path = os.path.abspath(os.path.join(BASE_DIR, "..", "src", "gpt_explainer.py"))
    subprocess.Popen(["python", path], cwd=os.path.join(BASE_DIR, "..", "src"))


async def upload_presentation(presentation_path):
    """
    Upload the sample presentation using the user_client.py script.
    """
    await asyncio.sleep(5)  # Delay to ensure the API has started
    print("Uploading sample presentation...")
    path = os.path.abspath(os.path.join(BASE_DIR, "..", "src", "user_client.py"))
    subprocess.Popen(["python", path, presentation_path])


async def system_test(presentation_path):
    """
    Perform the system test by starting the Web API, uploading the presentation, and starting the Explainer.
    """
    await start_web_api()
    await asyncio.sleep(2)
    await upload_presentation(presentation_path)
    await asyncio.sleep(2)
    await start_explainer()


def main():
    """
    Parse command-line arguments and start the system test.
    """
    parser = argparse.ArgumentParser(description="System Test")
    parser.add_argument(
        "--presentation-path",
        type=str,
        default=PRESENTATION_PATH,
        help="Path to the presentation file",
    )
    args = parser.parse_args()

    presentation_path = os.path.abspath(args.presentation_path)

    print("System Test")
    asyncio.run(system_test(presentation_path))
    print("System test complete.")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(current_dir, ".."))
    main()

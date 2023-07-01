import argparse
import asyncio
import aiohttp
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Status:
    """Represents the status of an upload."""
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    def is_done(self):
        """Check if the upload is done."""
        return self.status == "completed"


class WebAppClient:
    """Client for interacting with a web application."""
    def __init__(self, base_url):
        """
        Initialize the WebAppClient.

        Args:
            base_url (str): The base URL of the web application.
        """
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    async def upload(self, file_path, email=None):
        """
        Upload a file to the web application.

        Args:
            file_path (str): The path to the file to upload.
            email (str, optional): The email to attach to the upload.

        Returns:
            str: The unique ID assigned to the upload.
        """
        url = f"{self.base_url}/upload"

        form = aiohttp.FormData()
        form.add_field("email", email) if email else None
        form.add_field("file", open(file_path, "rb"))

        async with self.session.post(url, data=form) as response:
            if response.status != 200:
                raise Exception(f"Upload failed with status code: {response.status}")

            data = await response.json()
            uid = data["uid"]
            return uid

    async def status(self, uid=None, filename=None, email=None):
        """
        Check the status of an upload.

        Args:
            uid (str, optional): The unique ID of the upload.
            filename (str, optional): The filename of the upload.
            email (str, optional): The email associated with the upload.

        Returns:
            Status: The status of the upload.
        """
        url = f"{self.base_url}/status"
        params = {}

        if uid:
            params["uid"] = uid
        elif filename and email:
            params["filename"] = filename
            params["email"] = email

        async with self.session.get(url, params=params) as response:
            if response.status == 404:
                raise Exception("Upload not found")

            if response.status != 200:
                raise Exception(f"Status check failed with status code: {response.status}")

            data = await response.json()
            status = Status(
                status=data["status"],
                filename=data["filename"],
                timestamp=datetime.strptime(data["timestamp"], "%a, %d %b %Y %H:%M:%S %Z"),
                explanation=data["explanation"]
            )
            return status

    async def __aenter__(self):
        """Enter the context."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the context and close the session."""
        await self.session.close()


async def main(file_path, email=None):
    """
    Perform the main logic of the script.

    Args:
        file_path (str): The path to the PowerPoint presentation file.
        email (str, optional): The email to attach to the upload.
    """
    async with WebAppClient("http://localhost:5000") as client:
        uid = await client.upload(file_path, email)
        print(f"Upload successful. UID: {uid}")

        while True:
            status_task = asyncio.create_task(client.status(uid))
            await asyncio.sleep(1)
            status = await status_task

            if status.is_done():
                print("Status: Completed")
                print(f"Filename: {status.filename}")
                print(f"Timestamp: {status.timestamp}")
                print(f"Explanation: {status.explanation}")
                break
            else:
                print("Status: Processing")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PowerPoint presentation slides.")
    parser.add_argument("presentation_path", type=str, help="Path to the PowerPoint presentation file.")
    parser.add_argument("email", type=str, nargs="?", default=None, help="Email to attach to the upload")
    args = parser.parse_args()

    asyncio.run(main(args.presentation_path, args.email))

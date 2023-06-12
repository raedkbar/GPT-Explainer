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
        return self.status == "done"


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

    async def upload(self, file_path):
        """
        Upload a file to the web application.

        Args:
            file_path (str): The path to the file to upload.

        Returns:
            str: The unique ID assigned to the upload.
        """
        url = f"{self.base_url}/upload"

        with open(file_path, "rb") as file:
            async with self.session.post(url, data={"file": file}) as response:
                if response.status != 200:
                    raise Exception(f"Upload failed with status code: {response.status}")

                data = await response.json()
                uid = data["uid"]
                return uid

    async def status(self, uid):
        """
        Check the status of an upload.

        Args:
            uid (str): The unique ID of the upload.

        Returns:
            Status: The status of the upload.
        """
        url = f"{self.base_url}/status/{uid}"

        async with self.session.get(url) as response:
            if response.status == 404:
                raise Exception(f"Upload with UID '{uid}' not found")

            if response.status != 200:
                raise Exception(f"Status check failed with status code: {response.status}")

            data = await response.json()
            status = Status(
                status=data["status"],
                filename=data["filename"],
                timestamp=datetime.strptime(data["timestamp"], "%Y%m%d%H%M%S"),
                explanation=data["explanation"]
            )
            return status

    async def close(self):
        """Close the session."""
        await self.session.close()


async def main(file_path):
    """
    Perform the main logic of the script.

    Args:
        file_path (str): The path to the PowerPoint presentation file.
    """
    client = WebAppClient("http://localhost:5000")

    uid = await client.upload(file_path)
    print(f"Upload successful. UID: {uid}")

    while True:
        status = await client.status(uid)
        if status.is_done():
            print("Status: Done")
            print(f"Filename: {status.filename}")
            print(f"Timestamp: {status.timestamp}")
            print(f"Explanation: {status.explanation}")
            break
        else:
            print("Status: Pending")
            await asyncio.sleep(1)

    await client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PowerPoint presentation slides.")
    parser.add_argument("presentation_path", type=str, help="Path to the PowerPoint presentation file.")
    args = parser.parse_args()

    asyncio.run(main(args.presentation_path))

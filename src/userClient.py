import asyncio
import aiohttp
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    def is_done(self):
        return self.status == "done"


class WebAppClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    async def upload(self, file_path):
        url = f"{self.base_url}/upload"

        with open(file_path, "rb") as file:
            async with self.session.post(url, data={"file": file}) as response:
                if response.status != 200:
                    raise Exception(f"Upload failed with status code: {response.status}")

                data = await response.json()
                uid = data["uid"]
                return uid

    async def status(self, uid):
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
        await self.session.close()


# Usage example
async def main():
    client = WebAppClient("http://localhost:5000")

    # Upload a file
    file_path = "3slides.pptx"
    uid = await client.upload(file_path)
    print(f"Upload successful. UID: {uid}")

    # Check status
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
    asyncio.run(main())

import os
from typing import Union, List, Tuple
import aiohttp
from dotenv import load_dotenv

from botrun_hatch.models.hatch import Hatch

load_dotenv()


class HatchClient:
    def __init__(self):
        self.base_url = os.getenv(
            "BOTRUN_FLOW_LANG_URL",
            "https://botrun-flow-lang-fastapi-dev-36186877499.asia-east1.run.app",
        )
        self.api_url = f"{self.base_url}/api/hatch"
        self.hatches_url = f"{self.base_url}/api/hatches"

    async def get_hatch(self, item_id: str) -> Union[Hatch, None]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/{item_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    return Hatch(**data)
                else:
                    print(
                        f">============Getting hatch {item_id} failed with status code {response.status}"
                    )
                    return None

    async def set_hatch(self, item: Hatch):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=item.model_dump()) as response:
                if response.status == 200:
                    return True, item
                else:
                    print(
                        f"Error setting hatch {item.id}: Status code {response.status}"
                    )
                    return False, None

    async def delete_hatch(self, item_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self.api_url}/{item_id}") as response:
                if response.status == 200:
                    return True
                else:
                    print(
                        f"Error deleting hatch {item_id}: Status code {response.status}"
                    )
                    return False

    async def get_hatches(self, user_id: str) -> List[Hatch]:
        async with aiohttp.ClientSession() as session:
            params = {"user_id": user_id}
            async with session.get(self.hatches_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [Hatch(**item) for item in data]
                else:
                    print(
                        f"Error getting hatches for user {user_id}: Status code {response.status}"
                    )
                    return []

    async def get_default_hatch(self, user_id: str) -> Union[Hatch, None]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/default/{user_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    return Hatch(**data)
                elif response.status == 404:
                    print(f"No default hatch found for user {user_id}")
                    return None
                else:
                    print(
                        f"Error getting default hatch for user {user_id}: Status code {response.status}"
                    )
                    return None

    async def set_default_hatch(self, user_id: str, hatch_id: str) -> Tuple[bool, str]:
        async with aiohttp.ClientSession() as session:
            data = {"user_id": user_id, "hatch_id": hatch_id}
            async with session.post(
                f"{self.api_url}/set_default", json=data
            ) as response:
                response_data = await response.json()
                if response.status == 200 and response_data.get("success"):
                    return True, "Default hatch set successfully"
                else:
                    error_message = response_data.get(
                        "message", "Unknown error occurred"
                    )
                    return False, f"Failed to set default hatch: {error_message}"

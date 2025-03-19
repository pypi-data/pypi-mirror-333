from freeapihub.core.logger import logger
from freeapihub.core.config import API_URL
from freeapihub.core.http_client import async_client


async def get_all_users():
    try:
        response = await async_client.get(f"{API_URL}/api/v1/randomusers")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch users: {e}")
        return None


async def get_user_by_id(user_id: str):
    try:
        response = await async_client.get(f"{API_URL}/api/v1/randomusers/{user_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch user with ID {user_id}: {e}")
        return None

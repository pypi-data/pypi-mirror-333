from freeapihub.core.logger import logger
from freeapihub.core.config import API_URL
from freeapihub.core.http_client import async_client


async def get_all_jokes():
    try:
        response = await async_client.get(f"{API_URL}/api/v1/jokes")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch jokes: {e}")
        return None


async def get_joke_by_id(joke_id: str):
    try:
        response = await async_client.get(f"{API_URL}/api/v1/jokes/{joke_id}")
        response.raise_for_status()
        return response.json()

    except Exception as e:
        logger.error(f"Failed to fetch joke with ID {joke_id}: {e}")
        return None

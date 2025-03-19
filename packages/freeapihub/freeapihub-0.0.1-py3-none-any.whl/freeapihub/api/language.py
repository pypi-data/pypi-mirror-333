from freeapihub.core.logger import logger
from freeapihub.core.config import API_URL
from freeapihub.core.http_client import async_client


async def get_all_programming_languages():
    try:
        response = await async_client.get(f"{API_URL}/api/v1/programming-languages")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get programming languages: {e}")
        return None


async def get_programming_language_by_id(language_id: str):
    try:
        response = await async_client.get(
            f"{API_URL}/api/v1/programming-languages/{language_id}"
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch programming language with ID {language_id}: {e}")
        return None

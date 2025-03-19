from freeapihub.core.logger import logger
from freeapihub.core.config import API_URL
from freeapihub.core.http_client import async_client


async def get_all_quotes():
    try:
        response = await async_client.get(f"{API_URL}/api/v1/quotes")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch quotes: {e}")
        return None


async def get_quote_by_id(quote_id: str):
    try:
        response = await async_client.get(f"{API_URL}/api/v1/quotes/{quote_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch quote with ID {quote_id}: {e}")
        return None

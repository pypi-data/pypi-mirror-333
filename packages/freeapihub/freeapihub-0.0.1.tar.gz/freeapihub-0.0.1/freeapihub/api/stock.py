from freeapihub.core.logger import logger
from freeapihub.core.config import API_URL
from freeapihub.core.http_client import async_client


async def get_all_stocks():
    try:
        response = await async_client.get(f"{API_URL}/api/v1/stocks")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch stocks: {e}")
        return None


async def get_stock_by_id(stock_id: str):
    try:
        response = await async_client.get(f"{API_URL}/api/v1/stocks/{stock_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch stock with ID {stock_id}: {e}")
        return None

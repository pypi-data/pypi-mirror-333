from freeapihub.core.logger import logger
from freeapihub.core.config import API_URL
from freeapihub.core.http_client import async_client


async def get_all_products():
    try:
        response = await async_client.get(f"{API_URL}/api/v1/products")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch products: {e}")
        return None


async def get_product_by_id(product_id: str):
    try:
        response = await async_client.get(f"{API_URL}/api/v1/products/{product_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch product with ID {product_id}: {e}")
        return None

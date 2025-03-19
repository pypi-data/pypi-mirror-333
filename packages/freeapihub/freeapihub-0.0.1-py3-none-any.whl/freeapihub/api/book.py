from freeapihub.core.logger import logger
from freeapihub.core.config import API_URL
from freeapihub.core.http_client import async_client


async def get_all_books():
    try:
        response = await async_client.get(f"{API_URL}/api/v1/books")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching books: {e}")
        return None


async def get_book_by_id(book_id: str):
    try:
        response = await async_client.get(f"{API_URL}/api/v1/books/{book_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching book with ID {book_id}: {e}")
        return None

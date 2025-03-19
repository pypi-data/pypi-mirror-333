from freeapihub.api.user import get_all_users, get_user_by_id
from freeapihub.api.book import get_all_books, get_book_by_id
from freeapihub.api.joke import get_all_jokes, get_joke_by_id
from freeapihub.api.stock import get_all_stocks, get_stock_by_id
from freeapihub.api.quote import get_all_quotes, get_quote_by_id
from freeapihub.api.product import get_all_products, get_product_by_id
from freeapihub.api.language import (
    get_all_programming_languages,
    get_programming_language_by_id,
)


__all__ = [
    "get_all_users",
    "get_user_by_id",
    "get_all_books",
    "get_book_by_id",
    "get_all_jokes",
    "get_joke_by_id",
    "get_all_products",
    "get_product_by_id",
    "get_all_quotes",
    "get_quote_by_id",
    "get_all_stocks",
    "get_stock_by_id",
    "get_all_programming_languages",
    "get_programming_language_by_id",
]

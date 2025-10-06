from request_helpers import fetch_url_with_proxy
from models import GooglebooksResponse
from utils.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

GOOGLEBOOKS_ISBN_SEARCH_URL = (
    "https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
)


def get_items_by_isbn(isbn: str) -> GooglebooksResponse | None:
    url = GOOGLEBOOKS_ISBN_SEARCH_URL.format(isbn=isbn)
    response = fetch_url_with_proxy(url)
    if response is None:
        logger.error(f"Failed to fetch Googlebooks ISBN search URL {url}")
        return None
    return response.json()

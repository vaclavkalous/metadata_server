from typing import Optional
from models import MotherCandidate
from .googlebooks import client as googlebooks_client, adapter as googlebooks_adapter

from utils.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


class MetadataService:
    def get_mother_candidates_by_isbn(self, isbn: str) -> Optional[MotherCandidate]:
        try:
            raw_data = googlebooks_client.get_items_by_isbn(isbn)
            if raw_data:
                return googlebooks_adapter.adapt_googlebooks_response(raw_data)
        except Exception as e:
            logger.error(f"Googlebooks metadata provider failed: {e}")

        return None

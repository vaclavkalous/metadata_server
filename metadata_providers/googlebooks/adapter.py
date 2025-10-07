import re
import json
from models import MotherCandidate, GooglebooksResponse, GooglebooksVolume

from utils.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

with open("mappings/language_mapping.json", "r") as f:
    LANGUAGE_MAPPING = json.load(f)

with open("mappings/tag_mapping.json", "r") as f:
    TAG_MAPPING = json.load(f)


def adapt_googlebooks_response(
    response: GooglebooksResponse,
) -> list[MotherCandidate] | None:
    return [adapt_googlebooks_item(item) for item in response["items"]]


def adapt_googlebooks_item(item: GooglebooksVolume) -> MotherCandidate:
    volume_info = item.get("volumeInfo", {})
    industry_identifiers = volume_info.get("industryIdentifiers", [])

    def get_identifier(identifiers, id_type):
        for identifier in identifiers:
            if identifier.get("type") == id_type:
                return identifier.get("identifier")
        return None

    def extract_year(published_date):
        if not published_date:
            return None
        match = re.search(r"\d{4}", published_date)
        return int(match.group(0)) if match else None

    mother = MotherCandidate(
        edition_id=item.get("id"),
        title=volume_info.get("title"),
        subtitle=volume_info.get("subtitle"),
        annotation=volume_info.get("description"),
        authors=", ".join(volume_info.get("authors", []))
        if volume_info.get("authors")
        else None,
        image_url=volume_info.get("imageLinks", {}).get("thumbnail"),
        year=extract_year(volume_info.get("publishedDate")),
        isbn13=get_identifier(industry_identifiers, "ISBN_13"),
        isbn10=get_identifier(industry_identifiers, "ISBN_10"),
        page_count=volume_info.get("pageCount"),
        publisher=volume_info.get("publisher"),
        language_ids=[LANGUAGE_MAPPING.get(volume_info.get("language"))],
        node_ids=[
            TAG_MAPPING.get(tag.lower().strip().rstrip("."))
            for tag in volume_info.get("categories", [])
        ],
        tag_node_ids=[
            TAG_MAPPING.get(tag.lower().strip().rstrip("."))
            for tag in volume_info.get("categories", [])
        ],
        binding_id=0,  # bindings are not available in googlebooks
        source="googlebooks",
    )

    return mother

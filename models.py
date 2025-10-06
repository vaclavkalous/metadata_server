from dataclasses import dataclass
from typing import Optional, List


@dataclass
class MotherCandidate:
    title: str
    subtitle: Optional[str] = None
    annotation: Optional[str] = None
    authors: Optional[str] = None
    image_url: Optional[str] = None
    source: Optional[str] = None
    edition_id: Optional[str] = None
    year: Optional[int] = None
    isbn13: Optional[str] = None
    isbn10: Optional[str] = None
    page_count: Optional[int] = None
    publisher: Optional[str] = None
    binding_id: Optional[int] = None
    language_ids: Optional[list[int]] = None
    node_ids: Optional[list[int]] = None
    tag_node_ids: Optional[list[int]] = None


@dataclass
class GooglebooksIndustryIdentifier:
    type: str
    identifier: str


@dataclass
class GooglebooksReadingModes:
    text: bool
    image: bool


@dataclass
class GooglebooksImageLinks:
    smallThumbnail: Optional[str] = None
    thumbnail: Optional[str] = None


@dataclass
class GooglebooksVolumeInfo:
    title: str
    authors: Optional[List[str]] = None
    publisher: Optional[str] = None
    publishedDate: Optional[str] = None
    description: Optional[str] = None
    industryIdentifiers: Optional[List[GooglebooksIndustryIdentifier]] = None
    readingModes: Optional[GooglebooksReadingModes] = None
    pageCount: Optional[int] = None
    printType: Optional[str] = None
    categories: Optional[List[str]] = None
    maturityRating: Optional[str] = None
    allowAnonLogging: Optional[bool] = None
    contentVersion: Optional[str] = None
    imageLinks: Optional[GooglebooksImageLinks] = None
    language: Optional[str] = None
    previewLink: Optional[str] = None
    infoLink: Optional[str] = None
    canonicalVolumeLink: Optional[str] = None


@dataclass
class GooglebooksSaleInfo:
    country: str
    saleability: str
    isEbook: bool


@dataclass
class GooglebooksEpubInfo:
    isAvailable: bool


@dataclass
class GooglebooksPdfInfo:
    isAvailable: bool


@dataclass
class GooglebooksAccessInfo:
    country: str
    viewability: str
    embeddable: bool
    publicDomain: bool
    textToSpeechPermission: str
    epub: GooglebooksEpubInfo
    pdf: GooglebooksPdfInfo
    webReaderLink: str
    accessViewStatus: str
    quoteSharingAllowed: bool


@dataclass
class GooglebooksSearchInfo:
    textSnippet: Optional[str] = None


@dataclass
class GooglebooksVolume:
    kind: str
    id: str
    etag: str
    selfLink: str
    volumeInfo: GooglebooksVolumeInfo
    saleInfo: GooglebooksSaleInfo
    accessInfo: GooglebooksAccessInfo
    searchInfo: Optional[GooglebooksSearchInfo] = None


@dataclass
class GooglebooksResponse:
    kind: str
    totalItems: int
    items: Optional[List[GooglebooksVolume]] = None

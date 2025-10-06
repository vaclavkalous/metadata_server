import requests
import os
import random
from pathlib import Path
from utils.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


DEDICATED_PROXY_URL = os.getenv("BUYPROXIES_DEDICATED_PROXY_LIST")
SEMIDEDICATED_PROXY_URL = os.getenv("BUYPROXIES_SEMIDEDICATED_PROXY_LIST")
PROXY_LIST_OUTPUT_PATH = "/tmp/proxy_list.txt"


def get_proxy_list() -> list[str] | None:
    proxy_file = Path(PROXY_LIST_OUTPUT_PATH)

    # Check if proxy list file exists
    if proxy_file.exists():
        logger.info("Loading proxy list from cache file")
        try:
            with open(proxy_file, "r") as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            if proxies:
                logger.info(f"Loaded {len(proxies)} proxies from cache")
                return proxies
            else:
                logger.warning("Cache file is empty, fetching from API")
        except Exception as e:
            logger.error(f"Failed to read proxy cache file: {e}")
            logger.info("Falling back to API fetch")

    # Fetch from API if file doesn't exist or is empty/corrupted
    logger.info("Fetching proxy list from API")
    if not DEDICATED_PROXY_URL or not SEMIDEDICATED_PROXY_URL:
        raise ValueError("No dedicated proxy list URL found in environment variables")

    response_dedicated = requests.get(DEDICATED_PROXY_URL)
    response_semidedicated = requests.get(SEMIDEDICATED_PROXY_URL)
    try:
        response_dedicated.raise_for_status()
        response_semidedicated.raise_for_status()
    except Exception:
        logger.error("Failed to fetch proxy list from Buyproxies API")
        return None

    responses = response_dedicated.text + response_semidedicated.text
    proxies = list()
    for proxy in responses.splitlines():
        if proxy.strip():  # Skip empty lines
            ip, port, username, password = proxy.split(":")
            proxies.append(f"http://{username}:{password}@{ip}:{port}")

    # Write proxies to cache file
    try:
        proxy_file.parent.mkdir(parents=True, exist_ok=True)
        with open(proxy_file, "w") as f:
            for proxy in proxies:
                f.write(proxy + "\n")
        logger.info(f"Cached {len(proxies)} proxies to {PROXY_LIST_OUTPUT_PATH}")
    except Exception as e:
        logger.error(f"Failed to write proxy cache file: {e}")

    return proxies


def fetch_url_with_proxy(url: str) -> requests.Response | None:
    proxies = get_proxy_list()
    if not proxies:
        raise ValueError("No proxies found")
    proxy = random.choice(proxies)
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy})
        response.raise_for_status()
    except Exception:
        logger.error(f"Failed to fetch URL {url} with proxy {proxy}")
        return None
    return response

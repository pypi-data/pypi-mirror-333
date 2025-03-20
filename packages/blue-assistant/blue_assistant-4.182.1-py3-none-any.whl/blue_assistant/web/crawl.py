from typing import List, Dict, Set
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from blueness import module


from blue_assistant import NAME
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)


def fetch_links_and_content(url, base_url, original_path):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return set(), ""

    soup = BeautifulSoup(response.text, "html.parser")
    links = set()

    for a_tag in soup.find_all("a", href=True):
        full_url = urljoin(base_url, a_tag["href"])
        parsed_url = urlparse(full_url)

        # Ensure link is from the same domain and in the same directory tree
        if parsed_url.netloc == urlparse(
            base_url
        ).netloc and parsed_url.path.startswith(original_path):
            links.add(full_url)

    plain_text = soup.get_text(separator=" ", strip=True)

    return links, plain_text


def crawl_list_of_urls(
    seed_urls: List[str],
    object_name: str,
    max_iterations: int = 10,
) -> Dict[str, str]:
    logger.info(
        "{}.crawl_list_of_urls({}): {} -> {}".format(
            NAME,
            len(seed_urls),
            ", ".join(seed_urls),
            object_name,
        )
    )

    visited: Dict[str, str] = {}
    queue: Set[str] = set(seed_urls)
    base_url = urlparse(seed_urls[0]).scheme + "://" + urlparse(seed_urls[0]).netloc
    original_path = (
        urlparse(seed_urls[0]).path.rsplit("/", 1)[0] + "/"
    )  # Get base directory

    iteration: int = 0
    while queue:
        current_url = queue.pop()
        if current_url in visited:
            continue

        logger.info(f"🔗  {current_url} ...")
        new_links, content = fetch_links_and_content(
            current_url, base_url, original_path
        )
        visited[current_url] = content
        queue.update(new_links - visited.keys())

        iteration += 1
        if max_iterations != -1 and iteration >= max_iterations:
            logger.warning(f"max iteration of {max_iterations} reached.")
            break

    if queue:
        logger.warning(f"queue: {len(queue)}")

    return visited

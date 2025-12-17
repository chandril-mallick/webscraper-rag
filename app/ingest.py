import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def scrape_website(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=15)

    # ❌ don't crash the server on block
    if response.status_code != 200:
        return ""

    soup = BeautifulSoup(response.text, "lxml")

    # Remove junk
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # Wikipedia main content
    content = soup.find("div", {"id": "mw-content-text"})
    if content:
        return content.get_text(separator="\n")

    return soup.get_text(separator="\n")


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks for better retrieval."""
    if not text.strip():
        return []
    
    # Clean up text
    text = re.sub(r'\s+', ' ', text).strip()
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:])
            break
        
        # Try to break at sentence boundary
        chunk = text[start:end]
        last_sentence = chunk.rfind('. ')
        if last_sentence > chunk_size * 0.7:  # Only break if we have enough content
            end = start + last_sentence + 2
            chunk = text[start:end]
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return [chunk for chunk in chunks if chunk.strip()]

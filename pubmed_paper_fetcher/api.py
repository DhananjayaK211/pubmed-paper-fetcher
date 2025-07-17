import requests
import time

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_pubmed_ids(query: str, max_results: int = 50) -> list[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    return _request_with_retries(BASE_URL, params)["esearchresult"]["idlist"]

def fetch_paper_details(pubmed_ids: list[str]) -> str:
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    return _request_with_retries(DETAILS_URL, params, text=True)

def _request_with_retries(url: str, params: dict, text=False, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.text if text else response.json()
        except Exception as e:
            if attempt < retries - 1:
                print(f"[WARN] Request failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise RuntimeError(f"[ERROR] Failed after {retries} attempts: {e}")

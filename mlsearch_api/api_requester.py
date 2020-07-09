import os, math, html, logging
from typing import Dict
from github import Github


logger = logging.getLogger(__name__)


def _unescape(text: str):
    """Unescape Html Script."""
    if text and isinstance(text, str):
        return html.unescape(text)
    return text


def fetch_github(query: str) -> Dict[str, str]:
    GITHUB_ACC_TOKEN = os.environ.get("GITHUB_ACC_TOKEN") or None
    GITHUB_URL = os.environ.get("GITHUB_URL") or 'in:readme+in:description'
    logger.info(f'github token: {GITHUB_ACC_TOKEN}')
    logger.info(f'github url: {GITHUB_URL}')

    query = '+'.join([query, GITHUB_URL])

    github = Github(GITHUB_ACC_TOKEN, per_page=10)
    response = github.search_repositories(query, 'stars', 'desc')

    fields = ['name', 'description', 'language', 'stargazers_count', 'clone_url']
    results = [
        {
            field: getattr(repo, field) for field in fields
        } for repo in response.get_page(0)
    ]
    logger.info(f'fetched results: {results}')
    return results

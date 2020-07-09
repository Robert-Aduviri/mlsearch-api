import os, math, html, logging
from typing import Dict, List
import boto3
from github import Github


logger = logging.getLogger(__name__)


def _unescape(text: str) -> str:
    """Unescape Html Script."""
    if text and isinstance(text, str):
        return html.unescape(text)
    return text


def make_dynamo_payload(item: Dict[str, str]) -> Dict[str, Dict]:
    assert 'url' in item and 'source' in item, 'Missing keys'
    payload = {
        field: {'S': str(item[field])} for field in item
    }
    return payload


def store_dynamodb(item: Dict[str, str]):
    dynamodb = boto3.resource('dynamodb')
    db = dynamodb.Table('ml-resources')
    print('Payload: ', item)
    db.put_item(Item=item)
    logger.info('Write succeeded')


def store_batch_dynamodb(items: List[Dict[str, str]]):
    dynamodb = boto3.resource('dynamodb')
    db = dynamodb.Table('ml-resources')
    with db.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)
    logger.info('Batch write succeeded')


def fetch_github(query: str) -> Dict[str, str]:
    GITHUB_ACC_TOKEN = os.environ.get("GITHUB_ACC_TOKEN") or None
    GITHUB_URL = os.environ.get("GITHUB_URL") or 'in:readme+in:description'
    logger.info(f'Github token: {GITHUB_ACC_TOKEN}')
    logger.info(f'Github url: {GITHUB_URL}')

    query = '+'.join([query, GITHUB_URL])

    github = Github(GITHUB_ACC_TOKEN, per_page=10)
    response = github.search_repositories(query, 'stars', 'desc')

    fields = ['name', 'description', 'language', 'stargazers_count', 'clone_url']
    results = [
        {
            **{field: getattr(repo, field) for field in fields},
            'url': getattr(repo, 'clone_url').replace('.git', ''),
            'source': 'github'
        } for repo in response.get_page(0)
    ]
    logger.info(f'Fetched results: {results}')

    store_batch_dynamodb(results)

    return results

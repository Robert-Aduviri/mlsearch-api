import logging
from flask import Flask, jsonify, request
from mlsearch_api.api_requester import fetch_github


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/')
def ping():
    return 'ML Search: It Works!'


@app.route('/search')
def search():
    query = request.args.get('query', '')
    logger.info(f'request query: {query}')
    results = jsonify(fetch_github(query))
    logger.info(f'response json {results}')
    return results


if __name__ == '__main__':
    import json, os
    json_data = open('zappa_settings.json')
    env_vars = json.load(json_data)['dev']['aws_environment_variables']
    for key, val in env_vars.items():
        os.environ[key] = val
    app.run()
    
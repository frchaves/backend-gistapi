"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

import requests
import re
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


def gists_for_user(username: str):
    """Provides the list of gist metadata for a given user.

    This abstracts the /users/:username/gist endpoint from the Github API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        The dict parsed from the json response from the Github API.  See
        the above URL for details of the expected structure.
    """
    gists_url = 'https://api.github.com/users/{username}/gists'.format(username=username)
    response = requests.get(gists_url)
    return response.json()


@app.route("/api/v1/search", methods=['POST'])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    post_data = request.get_json()
    if not post_data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    username = post_data.get('username', '')
    pattern = post_data.get('pattern', '')
    if not username or not pattern or not isinstance(username, str) or not isinstance(pattern, str):
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400


    # Set up pagination
    page_num = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    start_idx = (page_num - 1) * page_size
    end_idx = start_idx + page_size

    result = {}
    gists = gists_for_user(username)
    matching_gists = []

    for gist in gists:
        for file_name, file_data in gist['files'].items():
            file_content = requests.get(file_data['raw_url']).text
            if re.search(pattern, file_content):
                matching_gists.append({
                    'url': gist['html_url'],
                    'file_name': file_name
                })

    result['status'] = 'success'
    result['username'] = username
    result['pattern'] = pattern
    result['matches'] = matching_gists[start_idx:end_idx]

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9876)

import pytest
import json

from unittest import mock
from gistapi import app


def test_ping():
    client = app.test_client()
    response = client.get('/ping')
    assert response.data == b'pong'


@pytest.mark.parametrize('username, pattern, expected_url, expected_textfile',
                         [('frchaves', 'import requests',
                           'https://gist.github.com/cc9201c159c26e6b0854d9050d9aed7a', 'test2'), (
                          'justdionysus', 'import requests',
                          'https://gist.github.com/65e6162d99c2e2ea8049b0584dd00912', 'john_waters.py.nosecrets')])
def test_search_real_data(username, pattern, expected_url, expected_textfile):
    # Create a test client and send a POST request with some JSON data
    client = app.test_client()
    response = client.post('/api/v1/search', data=json.dumps({
        'username': username,
        'pattern': pattern
    }), content_type='application/json')

    # Check that the response is valid JSON and has the expected keys
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'status' in data
    assert 'username' in data
    assert 'pattern' in data
    assert 'matches' in data

    # Check that the matches list contains the expected data
    assert len(data['matches']) == 1
    assert data['matches'][0]['url'] == expected_url
    assert data['matches'][0]['file_name'] == expected_textfile


# mock version
@mock.patch('requests.get')
def test_search(mock_get):
    mock_response = [
        {
            "html_url": "https://gist.github.com/testuser/1234",
            "raw_url": "https://gist.github.com/testuser/1234", "files": {
            "testfile.txt": {
                "filename": "testfile.txt",
                "raw_url": "https://example.com/files/testfile.txt",
                }
            }
        }]
    mock_get.return_value.json.return_value = mock_response

    mock_get.return_value.text = 'test content'
    # mock_get.return_value.json.return_value = [{'id': '1234'}, {'id': '5678'}]

    # Create a test client and send a POST request with some JSON data
    client = app.test_client()
    response = client.post('/api/v1/search', data=json.dumps({
        'username': 'testuser',
        'pattern': 'test'
    }), content_type='application/json')

    # Check that the response is valid JSON and has the expected keys
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'status' in data
    assert 'username' in data
    assert 'pattern' in data
    assert 'matches' in data

    # Check that the matches list contains the expected data
    assert len(data['matches']) == 1
    assert data['matches'][0]['url'] == 'https://gist.github.com/testuser/1234'
    assert data['matches'][0]['file_name'] == 'testfile.txt'

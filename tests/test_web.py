import io

import pytest

from web import decode_text, allowed_file


def flatten(grid):
    return [cell for row in grid for cell in row]


def upload(client, filename, content):
    return client.post(
        '/file-upload',
        data={'file': (io.BytesIO(content), filename)},
        content_type='multipart/form-data')


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Random Bingo Generator' in response.data


class TestCustom:
    def test_returns_grid(self, client):
        response = client.post('/custom', json={'values': list('abcd')})
        assert response.status_code == 200
        grid = response.get_json()
        assert len(grid) == 2
        assert sorted(flatten(grid)) == list('abcd')

    def test_blank_values_are_dropped_and_stripped(self, client):
        response = client.post('/custom', json={'values': ['a', '', ' b ']})
        assert sorted(flatten(response.get_json())) == ['a', 'b']

    @pytest.mark.parametrize('payload', [
        {},
        {'values': 'abc'},
        {'values': [1, 2, 3]},
        {'values': ['a', None]},
        ['a', 'b'],
        None,
    ])
    def test_invalid_payload(self, client, payload):
        response = client.post('/custom', json=payload)
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_non_json_body(self, client):
        response = client.post('/custom', data='a\nb', content_type='text/plain')
        assert response.status_code == 400


class TestFileUpload:
    def test_txt_upload(self, client):
        response = upload(client, 'values.txt', b'a\nb\nc\nd\n')
        assert response.status_code == 200
        assert sorted(flatten(response.get_json())) == list('abcd')

    def test_csv_extension_is_case_insensitive(self, client):
        response = upload(client, 'VALUES.CSV', b'a\nb\nc\nd')
        assert response.status_code == 200

    def test_windows_line_endings(self, client):
        response = upload(client, 'values.txt', b'a\r\nb\r\nc\r\nd\r\n')
        assert sorted(flatten(response.get_json())) == list('abcd')

    def test_umlauts_in_cp1252(self, client):
        content = 'Bär\nÖl\nÜbung\nStraße'.encode('cp1252')
        response = upload(client, 'values.csv', content)
        assert sorted(flatten(response.get_json())) == sorted(
            ['Bär', 'Öl', 'Übung', 'Straße'])

    def test_missing_file(self, client):
        response = client.post('/file-upload')
        assert response.status_code == 400

    def test_empty_filename(self, client):
        response = upload(client, '', b'a\nb')
        assert response.status_code == 400

    def test_disallowed_extension(self, client):
        response = upload(client, 'values.exe', b'a\nb')
        assert response.status_code == 415


def test_too_large_request_gets_json_error(client):
    from web import app
    old = app.config['MAX_CONTENT_LENGTH']
    app.config['MAX_CONTENT_LENGTH'] = 10
    try:
        response = client.post('/custom', json={'values': ['x' * 100]})
    finally:
        app.config['MAX_CONTENT_LENGTH'] = old
    assert response.status_code == 413
    assert 'error' in response.get_json()


@pytest.mark.parametrize('filename, expected', [
    ('a.txt', True),
    ('a.CSV', True),
    ('a.tar.txt', True),
    ('a.png', False),
    ('txt', False),
    ('.txt', False),
])
def test_allowed_file(filename, expected):
    assert allowed_file(filename) is expected


def test_decode_text_utf8_with_bom():
    assert decode_text('﻿äö'.encode('utf-8')) == 'äö'


def test_decode_text_falls_back_to_cp1252():
    assert decode_text('äö'.encode('cp1252')) == 'äö'

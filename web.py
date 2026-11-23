import os.path

from flask import Flask, request, render_template, jsonify

from logic import bingo_from_iterable

ALLOWED_EXTENSIONS = {'.txt', '.csv'}


app = Flask(__name__)
app.config.update(
    title='Random Bingo Generator',
    # limit upload size to 16 Megabyte
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,
)


def allowed_file(filename):
    _, ext = os.path.splitext(filename)
    return '.' in filename and ext.lower() in ALLOWED_EXTENSIONS


def decode_text(data):
    """Decode uploaded bytes: UTF-8 (BOM allowed), else Windows-1252.

    Windows-1252 is what e.g. Excel writes for German umlauts in CSV files.
    """
    try:
        return data.decode('utf-8-sig')
    except UnicodeDecodeError:
        return data.decode('cp1252', errors='replace')


@app.route('/')
def index():
    return render_template('index.html', config=app.config)


@app.route('/custom', methods=['POST'])
def custom_bingo():
    data = request.get_json(silent=True)
    values = data.get('values') if isinstance(data, dict) else None
    if not isinstance(values, list) or not all(
            isinstance(value, str) for value in values):
        return jsonify(error='Erwartet wird eine Liste von Werten.'), 400
    return jsonify(list(bingo_from_iterable(values)))


@app.errorhandler(413)
def too_large(error):
    return jsonify(error='Die Eingabe ist zu groß (maximal 16 MB).'), 413


@app.route('/file-upload', methods=['POST'])
def bingo_by_uploaded_file():
    file = request.files.get('file')
    if file is None or file.filename == '':
        return jsonify(error='Keine Datei übermittelt.'), 400
    if not allowed_file(file.filename):
        return jsonify(error='Nur .txt- und .csv-Dateien sind erlaubt.'), 415
    # read the upload straight from the request stream: nothing is
    # written to disk, so concurrent uploads can't collide
    text = decode_text(file.stream.read())
    return jsonify(list(bingo_from_iterable(text.splitlines())))

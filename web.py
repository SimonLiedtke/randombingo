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
    values = request.form.getlist('values[]')
    return jsonify(list(bingo_from_iterable(values)))


@app.route('/file-upload', methods=['POST'])
def bingo_by_uploaded_file():
    file = request.files['file']
    if file.filename == '':
        return ''
    if file and allowed_file(file.filename):
        # read the upload straight from the request stream: nothing is
        # written to disk, so concurrent uploads can't collide
        text = decode_text(file.stream.read())
        return jsonify(list(bingo_from_iterable(text.splitlines())))
    return jsonify([])

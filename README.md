# Random Bingo

A small Flask web app that generates a random bingo card. Enter your own
values or upload a `.txt`/`.csv` file (one value per line, drag & drop
supported), and the values are shuffled into a grid.

## Requirements

- Python 3
- Dependencies from `requirements.txt` (Flask, gunicorn)

```sh
pip install -r requirements.txt
```

## Run locally

```sh
./rundevserver
```

Then open http://localhost:5000.

## Deploy

The `Procfile` runs the app with gunicorn, so it can be deployed to any
Procfile-based platform (e.g. Heroku):

```
web: gunicorn web:app --log-file=-
```

Or run it directly on a server:

```sh
gunicorn web:app
```

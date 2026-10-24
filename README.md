# Back-End-Development-Pictures

Flask REST API for the band website. Based on the official IBM Skills Network
`luggb-Back-End-Development-Pictures` template.

## Development environment

Use Python 3.9 in an isolated virtual environment. The course Cloud IDE also
provides `bash ./bin/setup.sh` to initialize its Linux environment.

```sh
python3.9 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
python -m flask run --host 0.0.0.0 --port 3000
```

On Windows, activate `.venv/Scripts/activate`. Python 3.9 on Windows can install
a compatible binary dependency with `pip install -r requirements.txt greenlet==3.1.1`.

## API

- GET /health: 200 with status OK.
- GET /count: 200 with the resource count.
- GET /picture: list all records.
- GET /picture/id: return a record, or 404 if absent.
- POST /picture: create a record (201), or reject a duplicate id (302).
- PUT /picture/id: update an existing record, or return 404 if absent.
- DELETE /picture/id: delete a record (204), or return 404 if absent.

Invalid JSON and conflicting resource ids return 400.

## Container

```sh
docker build -t pictures .
docker run --rm -p 3000:3000 pictures
```

## Validation and storage

Verified with Python 3.9.25: all 11 supplied pytest tests passed. PUT returns
200 with the updated representation. Pictures are stored in memory; restart
restores the original ten records. Deploy the container to IBM Cloud Code Engine.

# FastAPI Demo

## Environment Variables
| Name | Required | Description | Example |
|---|---|---|---|
| DATABASE_URL | yes | | `duckdb:///database.de` |

## Build
```bash
podman build -t localhost/fastapi-demo:main .
podman run --detach --publish 8080:8080 --volume database.db:/code/database.db --env-file .env localhost/fastapi-demo:main
```
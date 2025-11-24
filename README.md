# FastAPI Demo

## Environment Variables

| Name                        | Required | Description | Example                                                         |
| --------------------------- | -------- | ----------- | --------------------------------------------------------------- |
| DATABASE_URL                | yes      |             | `postgresql+psycopg://postgres:postgres@postgres:5432/postgres` |
| ACCESS_TOKEN_SECRET         | yes      |             |                                                                 |
| ACCESS_TOKEN_ALGORITHM      | yes      |             | `HS256`                                                         |
| ACCESS_TOKEN_EXPIRE_MINUTES | yes      |             | `30`                                                            |

## Build

```bash
podman build -t localhost/fastapi-demo:main .
podman run --detach --publish 8080:8080 --volume database.db:/code/database.db --env-file .env localhost/fastapi-demo:main
```

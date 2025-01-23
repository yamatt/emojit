# Emojit

Upload an emoji and it returns you an animated version based on your selection.

## Supported Animations

- Rainbow party
- Woop! Woop!
- Turn me around
- And then… explode

## Running Locally

### CLI

```sh
uv run fastapi run src/app/app.py
```

### Docker

```sh
docker build --tag 'emojit' .
```

## Local Testing

```bash
curl -X 'POST' 'http://localhost:8000/rainbow' \
        -H 'accept: application/json' \
        -H 'Content-Type: multipart/form-data' \
        -F 'image=@test/img/text2.png;type=image/png' \
        -o output.gif
```

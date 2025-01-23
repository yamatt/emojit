from typing import Annotated, Union

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from magic import Magic

from animations.rainbow import create_hue_rotation_gif
from animations.rotate import create_rotating_gif

from log import log

app = FastAPI()

SUPPORTED_INPUT_IMAGE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
]


def file_check(uploaded_file: bytes):
    """
    Checks file content to ensure it is a valid image.
    """
    if uploaded_file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File is too large. Max size is 10MB.")

    mime = Magic(mime=True)
    mime_type = mime.from_buffer(uploaded_file.file.read())

    if mime_type not in SUPPORTED_INPUT_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="The file is not a supported image.")

    log.info("File check passed", mime_type=mime_type)


def process(uploaded_file: UploadFile, func: callable) -> Response:
    file_check(uploaded_file)

    log.debug("Processing image", filename=uploaded_file.filename)
    animated_gif = func(uploaded_file.file)
    log.info("Image processed", filename=uploaded_file.filename, size=len(animated_gif))

    return Response(animated_gif, media_type="image/gif")


@app.post("/rainbow")
def rainbow(image: UploadFile = File(...)) -> Response:
    """
    Rotate through all the colours. Party style.
    """
    return process(image, create_hue_rotation_gif)


@app.post("/rotate")
def rotate(image: UploadFile = File(...)) -> Response:
    """
    Make an image spin around. Like a record baby.
    """
    return process(image, create_rotating_gif)

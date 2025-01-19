from typing import Annotated, Union

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
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


def file_check(byte_array: bytes):
    """
    Checks file content to ensure it is an image.
    """
    mime = Magic(mime=True)
    mime_type = mime.from_buffer(byte_array)

    if mime_type not in SUPPORTED_INPUT_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="The file is not a supported image.")

    log.info("File check passed", mime_type=mime_type)


def process(image: UploadFile, func: callable) -> FileResponse:
    byte_array = image.file.read()

    file_check(byte_array)

    log.info("Processing image", filename=image.filename)
    animated_gif = func(byte_array)
    log.info("Image processed", filename=image.filename, size=len(animated_gif))

    return FileResponse(animated_gif, media_type="image/gif")


@app.post("/rainbow")
def rainbow(image: UploadFile = File(...)) -> FileResponse:
    return process(image, create_hue_rotation_gif)


@app.post("/rotate")
def rotate(image: UploadFile = File(...)) -> FileResponse:
    return process(image, create_rotating_gif)

from typing import Annotated, Union

from fastapi import FastAPI, File, UploadFile, HTTPException
from magic import Magic

from animations.rainbow import create_hue_rotation_gif
from animations.rotate import create_rotating_gif

app = FastAPI()


def file_check(f: File):
    """
    Checks file content to ensure it is an image.
    """
    mime = Magic(mime=True)
    mime_type = mime.from_buffer(f.read(1024))

    if not mime_type.startswith("image"):
        raise HTTPException(status_code=400, detail="The file is not an image.")


def process(image: File, func: callable) -> bytes:
    file_check(image)

    f.seek(0)
    animated_gif = func(f)

    return StreamingResponse(animated_gif, media_type="image/gif")


@app.post("/rainbow")
def rainbow(image: UploadFile = File(...)):
    return process(image, create_hue_rotation_gif)


@app.post("/rotate")
def rotate(image: UploadFile = File(...)):
    return process(image, create_rotating_gif)

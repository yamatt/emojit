import imageio.v3 as iio
import numpy as np
from PIL import Image, ImageOps
import io

from fastapi import File


def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    """
    Rotate an image while retaining the alpha channel and avoiding clipping.
    The image will be padded to fit the rotated version.
    Args:
        image (np.ndarray): Input image (RGBA).
        angle (float): Angle to rotate the image (in degrees).
    Returns:
        np.ndarray: Rotated image with the alpha channel preserved.
    """
    pil_image = Image.fromarray(image, "RGBA")

    # Get the size of the original image
    width, height = pil_image.size

    # Rotate the image with a transparent background to retain the full image size
    rotated_image = pil_image.rotate(angle, expand=True, resample=Image.BICUBIC)

    # Return the rotated image as a numpy array
    return np.array(rotated_image)


def create_rotating_gif(input_image_bytes: File, frames: int = 36):
    """
    Create an animated GIF with rotating images from an in-memory image.
    Args:
        input_image_bytes (bytes): In-memory image data.
        frames (int): Number of frames in the GIF.
    Returns:
        bytes: The resulting animated GIF data in memory.
    """
    # Load image from bytes
    image = iio.imread(io.BytesIO(input_image_bytes))

    if image.shape[-1] == 4:  # RGBA
        # Generate frames with rotating image
        gif_frames = []
        for i in range(frames):
            angle = 360 * i / frames
            rotated_image = rotate_image(image, angle)
            gif_frames.append(rotated_image)

        # Save as GIF to memory
        gif_output = io.BytesIO()
        iio.imwrite(gif_output, gif_frames, format="GIF", loop=0, duration=100)
        gif_output.seek(0)  # Go to the beginning of the BytesIO buffer
        return gif_output.read()
    else:
        raise ValueError("Image must have an alpha channel (RGBA).")

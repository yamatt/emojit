import io 
from typing import BinaryIO

import imageio.v3 as iio
import numpy as np
from PIL import Image


def bounce(uploaded_image: BinaryIO, frames_count: int = 36, min_hue: int = 0, max_hue: int = 255) -> bytes:
    first_half_frame_count = frames_count // 2
    second_half_frame_count = frames_count - first_half_frame_count

def range_gif(uploaded_image: BinaryIO, frames_count: int = 36, min_hue: int = 0, max_hue: int = 255) -> bytes:
    gif_frames = generate_frames(uploaded_image, frames_count, min_hue, max_hue)

    with io.BytesIO() as gif_output:
        iio.imwrite(gif_output, gif_frames, format="GIF", loop=0, duration=100)
        return gif_output.getvalue()


def generate_frames(uploaded_image: BinaryIO, frames_count: int = 36, min_hue: int = 0, max_hue: int = 255) -> bytes:
    """
    Create an animated GIF with rotating hue from an in-memory image.
    Args:
        input_image_bytes (bytes): In-memory image data.
        frames (int): Number of frames in the GIF.
    Returns:
        bytes: The resulting animated GIF data in memory.
    """
    # Load image from bytes
    image = iio.imread(uploaded_image)

    # Ensure the image has an alpha channel
    if image.shape[-1] == 4:  # RGBA
        alpha = image[..., 3]  # Extract existing alpha channel
        image_rgb = image[..., :3]  # Extract RGB channels
    elif image.shape[-1] == 3:  # RGB
        image_rgb = image
    else:
        raise ValueError("Unsupported image format. Image must be RGB or RGBA.")

    # Generate frames with rotating hue
    gif_frames = []
    for i in range(frames_count):
        hue = max_hue * i / frames_count
        frame = rotate_hue(image, hue)

        if image.shape[-1] == 4:
            frame[..., 3] = alpha
        gif_frames.append(frame)
    return gif_frames

def rotate_hue(image: np.ndarray, hue: int) -> np.ndarray:
    """
    Rotate the hue of an image.
    Args:
        image (np.ndarray): Image in RGB format.
        angle (float): Angle to rotate the hue (in degrees).
    Returns:
        np.ndarray: Image with adjusted hue.
    """
    # Convert RGB to HSV
    hsv_image = np.array(Image.fromarray(image).convert("HSV"))
    _, sat, val = hsv_image[..., 0], hsv_image[..., 1], hsv_image[..., 2]

    hsv_image[..., 0] = hue

    # Convert back to RGB
    return np.array(Image.fromarray(hsv_image, "HSV").convert("RGBA"))

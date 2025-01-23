import io 
from typing import BinaryIO

import imageio.v3 as iio
import numpy as np
from PIL import Image


def rotate_hue(image: np.ndarray, angle: float) -> np.ndarray:
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
    hue, sat, val = hsv_image[..., 0], hsv_image[..., 1], hsv_image[..., 2]

    # Rotate hue
    hue = (hue + int(angle / 360 * 255)) % 255
    hsv_image[..., 0] = hue

    # Convert back to RGB
    return np.array(Image.fromarray(hsv_image, "HSV").convert("RGBA"))


def create_hue_rotation_gif(uploaded_image: BinaryIO, frames: int = 36) -> bytes:
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

    if image.shape[-1] == 4:  # RGBA
        alpha = image[..., 3]
        image_rgb = image[..., :3]
    else:
        raise ValueError("Image must have an alpha channel (RGBA).")

    # Generate frames with rotating hue
    gif_frames = []
    for i in range(frames):
        angle = 360 * i / frames
        rotated_image = rotate_hue(image_rgb, angle)

        # Reattach the alpha channel
        rotated_image[..., 3] = alpha
        gif_frames.append(rotated_image)

    with io.BytesIO() as gif_output:
        iio.imwrite(gif_output, gif_frames, format="GIF", loop=0, duration=100)
        return gif_output.getvalue()

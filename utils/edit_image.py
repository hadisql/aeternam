import os
from PIL import Image, ImageOps
from django.core.files.images import ImageFile
from io import BytesIO

def resize_image(image_file, size_limit=1024*1024):
    """
    Resize an image to fit within a size limit (in bytes).

    Args:
        image_file (File): The file-like object representing the image.
        size_limit (int): The maximum size limit in bytes (default is 1MB).

    Returns:
        bytes: The resized image data.
    """
    original_image_data = image_file.read()
    image = Image.open(BytesIO(original_image_data))

    # Check if the image size exceeds the size limit
    if len(original_image_data) > size_limit:
        # Calculate a new quality value to get the image size under the limit
        quality = int((size_limit / len(original_image_data)) * 100)

        # Create a BytesIO object to store the modified image data
        image_io = BytesIO()
        image.save(image_io, format='JPEG', quality=quality)
        image_io.seek(0)

        return image_io.getvalue()

    # If the image is already under the size limit, return the original data
    image_file.seek(0)
    return original_image_data

def rotate_image(image_file, rotation_angle):
    image = Image.open(image_file)
    rotated_image = image.rotate(-rotation_angle, expand=True)
    rotated_image_io = BytesIO()
    rotated_image.save(rotated_image_io, format='JPEG')
    return ImageFile(rotated_image_io)


def flip_image(image_file):
    image = Image.open(image_file)
    flipped_image = ImageOps.mirror(image)
    flipped_image_io = BytesIO()
    flipped_image.save(flipped_image_io, format='JPEG')
    return ImageFile(flipped_image_io)

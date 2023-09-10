import os
from PIL import Image
from io import BytesIO

def resize_image(image_path, size_limit=1024*1024):
    """
    Resize an image to fit within a size limit (in bytes).

    Args:
        image_path (str): The path to the image file.
        size_limit (int): The maximum size limit in bytes (default is 1MB).

    Returns:
        bytes: The resized image data.
    """
    image = Image.open(image_path)

    # Check if the image size exceeds the size limit
    if os.path.getsize(image_path) > size_limit:
        # Calculate a new quality value to get the image size under the limit
        quality = int((size_limit / os.path.getsize(image_path)) * 100)

        # Create a BytesIO object to store the modified image data
        image_io = BytesIO()
        image.save(image_io, format='JPEG', quality=quality)
        image_io.seek(0)

        return image_io.getvalue()

    # If the image is already under the size limit, return the original data
    with open(image_path, 'rb') as image_file:
        return image_file.read()

from .variables import msg_allowed
from .rescale import rescale_percent
from .utils import display_msg
from PIL import Image
import os
from pathlib import Path

def compress(input_path, selected_output_path, images, can_resize, want_force, max_size):
  input_path = Path(input_path)  # Convert to Path object
  selected_output_path = Path(selected_output_path)  # Convert to Path object
  max_size = int(max_size[:-2])

  base_dir = Path(__file__).resolve().parent.parent  # Go up two directories

  for image in images:
    resize_size_percent = 75
    user_is_info = False
    # Full output path for the file
    output_path_copy = base_dir / selected_output_path / image

    # Ensure the output directory exists
    output_path_copy.parent.mkdir(parents=True, exist_ok=True)

    image_path = input_path / image  # Correct way to join paths
    image_open = Image.open(image_path)

    extension = os.path.splitext(image)[1][1:]
    extension = "jpeg" if extension == "jpg" else extension

    width, height = image_open.size

    quality = 100
    min_quality_resize = 40
    min_quality_no_resize = 20 if not can_resize else 5
    min_quality = (min_quality_resize - 15) if not want_force else min_quality_no_resize

    if (width >= Image.MAX_IMAGE_PIXELS or height >= Image.MAX_IMAGE_PIXELS) and can_resize:
      image_open = rescale_percent(image_open, 90)
      image_open.save(output_path_copy, format=extension, quality=quality, optimize=True)

    image_size = os.path.getsize(image_path) / 1024  # Size in KB

    if image_size < max_size:
      display_msg("Image " + str(image) + " already had a size below the specified KB limit. (Actual size: " + str(round(image_size, 2)) + " KB)", msg_allowed["INFO"], False)
      user_is_info = True

    # If the size is greater than the maximum allowed, adjust the quality
    while image_size > max_size and quality >= min_quality:
        # Reduce the image quality by 5% per iteration
        if can_resize and quality <= min_quality_resize:
          if (resize_size_percent == 75):
            image_open = rescale_percent(image_open, resize_size_percent)
            resize_size_percent = 50
          elif (resize_size_percent == 50):
            image_open = rescale_percent(image_open, resize_size_percent)
            resize_size_percent = 35
          elif (resize_size_percent == 35):
            resize_size_percent = 10
            image_open = rescale_percent(image_open, resize_size_percent)

        quality -= 5

        # Save the image with the new quality
        image_open.save(output_path_copy, format=extension, quality=quality, optimize=True)

        # Check the file size again
        image_size = os.path.getsize(output_path_copy) / (1024)  # Size in KB

    if not user_is_info:
      if image_size > max_size:
        display_msg("Image " + str(image) + " could not reach the specified maximum size, it has been reduced to a weight of " + str(round(image_size, 2)) + " KB.", msg_allowed["WARNING"], False)
      else:
        display_msg("Image " + str(image) + " now has a file size of " + str(round(image_size, 2)) + " KB.", msg_allowed["SUCCESS"], False)

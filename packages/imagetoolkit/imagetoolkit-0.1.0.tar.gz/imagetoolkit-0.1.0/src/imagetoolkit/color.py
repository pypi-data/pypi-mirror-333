from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import os
from pathlib import Path
from .utils import display_msg
from .variables import msg_allowed

# Function to apply a filter to images
def apply_filter_to_images(input_path, selected_output_path, images, filter_choice):
    filters = {
        "SEPIA": apply_sepia,
        "INVERT": invert_colors,
        "GRAYSCALE": grayscale_filter,
        "BLUR": blur_filter,
        "CONTOUR": contour_filter,
        "DETAIL": detail_filter,
        "SHARPEN": sharpen_filter,
        "EMBOSS": emboss_filter,
        "EDGE_ENHANCE": edge_enhance_filter,
        "SMOOTH": smooth_filter,
        "POSTERIZE": posterize_filter,
        "SOLARIZE": solarize_filter,
        "EQUALIZE": equalize_filter,
        "BRIGHTNESS_INC": lambda img: adjust_brightness(img, 1.5),
        "BRIGHTNESS_DEC": lambda img: adjust_brightness(img, 0.7),
        "CONTRAST_INC": lambda img: adjust_contrast(img, 1.5),
        "CONTRAST_DEC": lambda img: adjust_contrast(img, 0.7),
        "SATURATION_INC": lambda img: adjust_saturation(img, 1.5),
        "SATURATION_DEC": lambda img: adjust_saturation(img, 0.7),
        "ROTATE_90": lambda img: img.rotate(90, expand=True),
        "ROTATE_180": lambda img: img.rotate(180, expand=True),
        "FLIP_HORIZONTAL": ImageOps.mirror,
        "FLIP_VERTICAL": ImageOps.flip,
        "CROP_CENTER": crop_center
    }

    input_path = Path(input_path)  # Convert to Path object
    selected_output_path = Path(selected_output_path)  # Convert to Path object

    for image in images:
        try:
            image_path = input_path / image  # Correct way to join paths
            with Image.open(image_path) as img:
                # Apply the selected filter
                filtered_img = filters[filter_choice](img)

                # Save the processed image
                output_image_path = os.path.join(selected_output_path, image)
                filtered_img.save(output_image_path)

                display_msg(f"Filter {filter_choice} applied to {image} and saved to {selected_output_path}", msg_allowed["SUCCESS"], False)
        except Exception as e:
            display_msg(f"Error processing image {image}: {e}", msg_allowed["ERROR"], False)


# Specific functions for each filter
def apply_sepia(image):
    sepia_filter = ImageOps.colorize(
        image.convert("L"), black="#704214", white="#C0A080"
    )
    return sepia_filter

def invert_colors(image):
    return ImageOps.invert(image.convert("RGB"))

def grayscale_filter(image):
    return image.convert("L")

def blur_filter(image):
    return image.filter(ImageFilter.BLUR)

def contour_filter(image):
    return image.filter(ImageFilter.CONTOUR)

def detail_filter(image):
    return image.filter(ImageFilter.DETAIL)

def sharpen_filter(image):
    return image.filter(ImageFilter.SHARPEN)

def emboss_filter(image):
    return image.filter(ImageFilter.EMBOSS)

def edge_enhance_filter(image):
    return image.filter(ImageFilter.EDGE_ENHANCE)

def smooth_filter(image):
    return image.filter(ImageFilter.SMOOTH)

def posterize_filter(image):
    return ImageOps.posterize(image, 4)

def solarize_filter(image):
    return ImageOps.solarize(image, threshold=128)

def equalize_filter(image):
    return ImageOps.equalize(image)

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def adjust_saturation(image, factor):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def crop_center(image):
    width, height = image.size
    new_width = int(width * 0.8)
    new_height = int(height * 0.8)
    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = (width + new_width) // 2
    bottom = (height + new_height) // 2
    return image.crop((left, top, right, bottom))

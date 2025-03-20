from prompt_toolkit.styles import Style

# Define valid image file extensions
valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

# Define the style for customizing margins and spacing in the user interface
style = Style([
  ('qmark', 'fg:#32cf4c bold'),       # Token in front of the question
  ('question', 'bold'),               # Style for the question text
  ('answer', 'fg:#32cf4c bold'),      # Submitted answer text behind the question
  ('pointer', 'fg:#673ab7 bold'),     # Pointer used in select and checkbox prompts
  ('highlighted', 'fg:white bg:#673ab7 bold'), # Pointed-at choice in select and checkbox prompts
  ('selected', 'fg:#32cf4c'),         # Style for a selected item in a checkbox
  ('separator', 'fg:#cc5454'),        # Separator in lists
  ('instruction', ''),                # User instructions for select, rawselect, checkbox
  ('text', ''),                       # Plain text style
  ('disabled', 'fg:#858585 italic')   # Disabled choices for select and checkbox prompts
])

# Main menu options with their corresponding descriptions
options_main_menu = {
  'REDUCE': 'Reduce the file size of the image(s)',
  'RESIZE': 'Resize and scale the image(s)',
  'FORMATS': 'Convert image formats (PNG, JPG, JPEG, etc.) or rename the file',
  'FILTERS': 'Apply image filters',
  'TEXT': 'Add text to the image(s)',
  'THUMBNAILS': 'Create image thumbnails',
  'EXIT': 'Exit',
}

# List of available filters for image manipulation
available_filters = [
  "SEPIA", "INVERT", "GRAYSCALE", "BLUR", "CONTOUR", "DETAIL",
  "SHARPEN", "EMBOSS", "EDGE_ENHANCE", "SMOOTH", "POSTERIZE",
  "SOLARIZE", "EQUALIZE", "BRIGHTNESS_INC", "BRIGHTNESS_DEC",
  "CONTRAST_INC", "CONTRAST_DEC", "SATURATION_INC", "SATURATION_DEC",
  "ROTATE_90", "ROTATE_180", "FLIP_HORIZONTAL", "FLIP_VERTICAL",
  "CROP_CENTER"
]

# Predefined messages for different types of output
msg_allowed = {
  'ERROR': 'error',
  'WARNING': 'warning',
  'INFO': 'info',
  'SUCCESS': 'success'
}

# Directory containing fonts for text customization
fonts_dir = 'fonts/'

# Allowed file size limits (in kilobytes)
allowed_limits_kb = ["2048 KB", "1500 KB", "1024 KB", "512 KB", "256 KB"]

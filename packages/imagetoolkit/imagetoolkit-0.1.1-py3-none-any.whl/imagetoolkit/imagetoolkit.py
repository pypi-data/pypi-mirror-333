'''
--------------------
IMAGETOOLKIT APP v0.1
--------------------
Author GitHub name: jedahee
Author name: Jesús Daza

Image Toolkit is a console application offering multiple tools
for quickly and easily editing one or more images.

What can Image Toolkit do for you?

1) Reduce the size of the image(s)
2) Resize and scale
3) File extension converter (png, jpg, jpeg...)
4) Convert to black and white
5) Apply filters
6) Add text to the image
7) Create thumbnails

---

Image Toolkit Workflow:

-> Entry into the script
  -> Welcome message
  -> (User selects the correct option from the menu) - (Displays list)
  -> (User specifies the path containing the images)
  -> (User specifies the output path)
  -> (User selects the images they want to edit)

  If the user chose:
  -> Reduce the size of the image(s)
    -> What is the maximum size you want Image Toolkit to reduce it to? (e.g., 512KB | always in KB)
    -> If there are images that are too large, can Image Toolkit rescale them to make them smaller?
    -> If the image is too large, would you like to force the size reduction to the specified KB limit, sacrificing some quality?
  -> Resize (fixed value) or rescale (proportional value)
    -> Resize
      -> Show a warning that resizing to a larger size than the original image may result in quality loss
      -> Ask for width + height
      -> Ask for quality type (warning about processing time)
    -> Change scale
      -> Ask for the proportion of the new image (50%, 75%, or 150%...)
  -> File extension converter (png, jpg, jpeg...) - You can also change the name
    -> Show available placeholders for filenames (e.g., index with -INDEX, -INDEX_START to indicate the start of the index content)
    -> Ask for the new (or new) filenames
    -> Ask for the new extension
  -> Apply filters
    -> Show filter catalog
    -> Ask for filter
  -> Add text to the image
    -> Ask for text to add
    -> Ask for font (show catalog)
    -> Ask for color (show catalog)
    -> Ask for text position in the image
  -> Create thumbnails (favicon)
    -> Show thumbnail size catalog (e.g., 16px, 32px, 48px, 64px)
    -> Ask if you want to transform the files into .ICO format
    -> Ask for the thumbnail size

-> Display status information for the executed option
-> Exit the script

---

Project Structure (PyPI):

imagetoolkit/
├── src/                # Main module of the tool
│   ├── imagetoolkit/
│   ├── __init__.py     # Package initializer
│   ├── cli.py          # Code for the command-line interface (arguments and execution)
│   ├── imagetoolkit.py   # Main file
│   ├── compress.py     # Functions for resizing/compressing images
│   ├── rescale.py      # Functions related to resizing images
│   ├── extension.py    # Functions for editing the name and extension of images
│   ├── color.py        # Functions for manipulating colors (color adjustments, black & white, etc.)
│   ├── addtext.py      # Functions for adding text to images
│   ├── utils.py        # Auxiliary functions and general tools (e.g., path validation, error handling)
│   └── variables.py    # Global variables
├── requirements.txt    # Project dependencies (Pillow, click, etc.)
├── README.md           # Project documentation
├── setup.py            # Package configuration if you plan to distribute it
└── .gitignore          # Files to ignore in version control (environment, etc.)

'''

import questionary
import warnings
from PIL import Image
from time import sleep
import os, sys

# Internal imports for image manipulation, options, and utility functions
from .utils import welcome, select_option, ask_for_path, ask_for_images, qselect, display_msg
from .compress import compress
from .extension import new_format
from .variables import style, options_main_menu, allowed_limits_kb, msg_allowed, available_filters
from .color import apply_filter_to_images
from .rescale import thumbnails, process_images_resize
from .addtext import get_available_fonts, add_text_to_image
from .cli import cli

# Main function to run the interactive application
def run_interactive_app():
  # Variables to store user selections
  images_selected = []  # List of selected images
  option_menu = ""  # Menu option selected by user
  format_selected = ""  # Selected image format (JPEG, PNG, BMP)
  selected_path = ""  # Path to the images
  selected_output_path = "" # Output images
  base_name = ""  # Base name for renaming images (if applicable)

  # Suppress warnings for large images that might be decompressed
  warnings.simplefilter('ignore', Image.DecompressionBombWarning)

  # Main loop to keep the app running until the user chooses to exit
  while option_menu != options_main_menu["EXIT"]:
    welcome()  # Display a welcome message
    option_menu = select_option()  # Let the user select an option from the menu

    # If the user didn't choose to exit, proceed with image processing
    if option_menu != options_main_menu["EXIT"]:
      selected_path = ask_for_path()  # Ask the user to specify the folder containing images

      # If the user provided a valid path, proceed with further selections
      if selected_path != ".." and selected_path != "":
        images_selected = ask_for_images(selected_path)  # Ask the user to select images to edit
        selected_output_path = ask_for_path(True)  # Ask the user to specify the folder containing images

        # If the user chose the "Reduce size" option
        if option_menu == options_main_menu["REDUCE"]:
          max_size = qselect("Choose the maximum image size:", allowed_limits_kb)  # Ask for the maximum allowed size in KB
          can_resize = qselect("If the image exceeds an appropriate size, can Image Toolkit rescale it to make it smaller?", ["Yes", "No"])  # Ask if rescaling is allowed
          want_force = qselect("If the image is too large, would you like to force the size reduction to the specified KB limit, sacrificing some quality?", ["Yes", "No"])  # Ask if forced size reduction is acceptable

          # Convert user inputs into boolean values
          can_resize = True if can_resize.lower() == "yes" else False
          want_force = True if want_force.lower() == "yes" else False

          print()  # Print an empty line for clarity

          # Call the compress function to reduce the size of the selected images
          compress(selected_path, selected_output_path, images_selected, can_resize, want_force, max_size)

        # If the user chose the "Resize" option
        elif option_menu == options_main_menu["RESIZE"]:
          resize_mode = qselect(
            "Choose resize mode:",
            ["Fixed size", "Proportional scale"]
          ).lower()  # Ask if they want fixed resizing or proportional scaling

          if resize_mode == "fixed size":
            display_msg(
                "Note: Resizing to larger dimensions may result in quality loss",
                msg_allowed["INFO"], False
            )

            try:
              # Ask for new width and height values
              new_width = int(questionary.text("Enter the new width (px):").ask())
              new_height = int(questionary.text("Enter the new height (px):").ask())

              # Ask for the quality type (faster processing or better quality)
              quality_type = qselect(
                "Choose image quality (faster processing or better quality):",
                ["Normal (fast)", "High (slower processing)"]
              ).lower()

              # Map the quality type to a specific resampling method
              quality_mapping = {
                  "normal (fast)": Image.Resampling.BICUBIC,
                  "high (slower processing)": Image.Resampling.LANCZOS,
              }

              quality = quality_mapping[quality_type]  # Set the quality to the selected method

              # Call the function to resize the images based on the specified dimensions and quality
              process_images_resize(
                  selected_path, selected_output_path, images_selected, "fixed",
                  (new_width, new_height), quality
              )
            except Exception as e:
              print()  # Print an empty line for clarity
              display_msg(f"Invalid input! Please enter a valid numeric value for the width and height", msg_allowed["ERROR"], False)
              print()  # Print an empty line for clarity

          elif resize_mode == "proportional scale":
            try:
              # Ask for the scaling percentage (e.g., 50%, 75%, 150%)
              scale_percent = int(
                  questionary.text(
                      "Enter the scaling percentage (e.g., 50, 75, 150):"
                  ).ask()
              )

              # Call the function to rescale the images by the specified percentage
              process_images_resize(
                selected_path, selected_output_path, images_selected, "percent",
                scale_percent, None
              )
            except Exception as e:
              print()  # Print an empty line for clarity
              display_msg(f"Invalid input! Please enter a valid numeric value for the width and height", msg_allowed["ERROR"], False)
              print()  # Print an empty line for clarity

        # If the user chose the "Convert file format" option
        elif option_menu == options_main_menu["FORMATS"]:
          # Ask the user to select the format they want to convert the images to
          format_selected = qselect("Select the format to convert to:", ["JPEG", "PNG", "BMP"])

          # Ask if the user wants to rename the files during conversion
          change_name = qselect("Do you want to rename the files?", ["Yes", "No"])
          change_name = True if change_name.lower() == "yes" else False

          if change_name:
            # Show the available placeholders for filenames (e.g., adding indexes)
            print("\nYou can use the following placeholders:")
            print(" --INDEX: Adds an index to the end of the new file name, starting from 1. (default)")
            print(" --START <number>: Adds an index to the end of the new file name, starting from the specified <number>.")

            while base_name == "":
              # Ask the user for the new base name for the files
              base_name = questionary.text("Enter the new base name for your files:", style=style).ask()

          # Call the function to convert the images to the selected format
          new_format(selected_path, selected_output_path, images_selected, format_selected, change_name, base_name)
          base_name = ""  # Reset the base name for future use

        # If the user chose to apply a filter
        elif option_menu == options_main_menu["FILTERS"]:
          # Ask the user to select a filter from the available list
          filter_choice = qselect(
            "Choose a filter to apply:",
            available_filters
          )

          # Call the function to apply the selected filter to the images
          apply_filter_to_images(selected_path, selected_output_path, images_selected, filter_choice)

        # If the user chose the "Add text to image" option
        elif option_menu == options_main_menu["TEXT"]:
          # Ask the user for the text they want to add to the images
          text_to_add = questionary.text("Enter the text to add to the image:").ask()

          # Get a list of available fonts from the fonts directory
          available_fonts = get_available_fonts()

          # If no fonts are available, set a default font
          if not available_fonts:
            display_msg("No fonts found in the fonts directory!", msg_allowed["ERROR"], False)
            font_choice = "Anton.ttf"  # Default font if no fonts are found
          else:
            # Ask the user to select a font from the available list
            font_choice = qselect("Choose the font for the text:", available_fonts)

          try:
            # Ask the user for the font size ratio as a percentage of the image width
            font_size_ratio = float(questionary.text(
              "Enter the font size ratio (e.g., 5%, 15%, 30% of image width):"
            ).ask())
          except Exception as e:
            font_size_ratio = 25  # Default font size ratio if input is invalid
            display_msg(f"Invalid input! Please enter a valid numeric value for the width and height", msg_allowed["ERROR"], False)

          # Ask the user for the text color
          color_choice = qselect(
            "Choose the color of the text:",
            ["black", "white", "red", "blue", "green"]
          )

          # Define possible text positions on the image
          position_choices = {
            "Top Left": "Top Left",
            "Top Right": "Top Right",
            "Center": "Center",
            "Bottom Left": "Bottom Left",
            "Bottom Right": "Bottom Right"
          }

          # Ask the user for the text position
          position_choice = qselect(
            "Choose the position of the text:",
            list(position_choices.keys())
          )

          # Get the coordinates for the selected position
          position = position_choices[position_choice]

          # Call the function to add the text to the images
          add_text_to_image(selected_path, selected_output_path, images_selected, text_to_add, position, font_choice, font_size_ratio, color_choice)

        # If the user chose to create thumbnails
        elif option_menu == options_main_menu["THUMBNAILS"]:
          # Ask for the desired thumbnail size
          thumbnail_size = qselect("Choose the desired size for your favicon or thumbnail:", ["16px", "24px", "32px", "48px", "64px", "92px", "128px"])

          # Ask if the user wants to convert the images to .ICO format for favicons
          want_favicon = qselect(
            "Would you like to convert the images to .ico format for use as favicons?",
            ["Yes", "No"]
          ).lower()

          # Call the function to create the thumbnails
          thumbnails(selected_path, selected_output_path, images_selected, want_favicon, thumbnail_size)

      sleep(1)  # Give the user a moment to see the results before the app loops again

    else:

      if selected_output_path != "":
        display_msg(f"All new images are saved in {selected_output_path}", msg_allowed["INFO"])
      display_msg("Bye! :)", msg_allowed["INFO"], False)


def main():

    # Verify args
    if len(sys.argv) > 1:
      cli()  # Script executing cli args mode
    else:
      # Script executing interactuve cli mode
      run_interactive_app()

if __name__ == "__main__":
    main()

import questionary
import os
from pathlib import Path
from sys import exit
from .variables import valid_extensions, style, options_main_menu, msg_allowed

# Welcome function that displays an introductory ASCII art and text
def welcome():
  print("""
 █████
░░███
 ░███  █████████████    ██████    ███████  ██████
 ░███ ░░███░░███░░███  ░░░░░███  ███░░███ ███░░███
 ░███  ░███ ░███ ░███   ███████ ░███ ░███░███████
 ░███  ░███ ░███ ░███  ███░░███ ░███ ░███░███░░░
 █████ █████░███ █████░░████████░░███████░░██████
░░░░░ ░░░░░ ░░░ ░░░░░  ░░░░░░░░  ░░░░░███ ░░░░░░
                                 ███ ░███
                                ░░██████
                                 ░░░░░░
 ███████████                   ████
░█░░░███░░░█                  ░░███
░   ░███  ░   ██████   ██████  ░███   █████
    ░███     ███░░███ ███░░███ ░███  ███░░
    ░███    ░███ ░███░███ ░███ ░███ ░░█████
    ░███    ░███ ░███░███ ░███ ░███  ░░░░███
    █████   ░░██████ ░░██████  █████ ██████
   ░░░░░     ░░░░░░   ░░░░░░  ░░░░░ ░░░░░░
""")

# Function to select an option from the main menu
def select_option():
  option = questionary.select(
    "What do you want ImageToolkit to do for you?",
    choices=list(options_main_menu.values()),
    style=style
  ).ask()

  return select_option() if option == None else option

# Function to ask the user for a directory path
def ask_for_path(output=False):

  if not output:
    display_msg("Note: Type '..' to back menu list", msg_allowed["INFO"])

  msg=""

  try:
    msg = "Please enter the directory path:" if not output else "Please enter the directory path for the new images:"
    q_path = questionary.text(msg, style=style).ask()

    if q_path == "..":
      return q_path

    input_path = Path(q_path)
  except TypeError:
    display_msg("There was an error with the path", msg_allowed["ERROR"])
    return ask_for_path()

  if input_path.exists():
    return input_path
  else:
    display_msg("The path does not exist. Please enter a valid path.", msg_allowed["ERROR"])
    return ask_for_path()

# Function to ask the user to select image files from a specified directory
def ask_for_images(path):
  images_dir = []
  selected_images_dir = []

  try:
    object_path = Path(path)
  except:
    display_msg("There seems to be an issue with this path. Please try again later or verify that it exists.", msg_allowed["ERROR"])

  # Iterate through all files in the directory
  for file_path in path.iterdir():
      # Check if the file has a valid image extension
      if file_path.suffix.lower() in valid_extensions:
        images_dir.append(file_path.name)

  if len(images_dir) == 0:
    display_msg("Sorry! No images found in this path :C", msg_allowed["ERROR"])
    exit()

  # Prompt the user to select images from the valid ones found in the directory
  selected_images_dir = questionary.checkbox(
    'Select image files',
    choices=images_dir,
    style=style
  ).ask()

  return ask_for_images(path) if selected_images_dir == None else selected_images_dir

# Function to select a single option from a list of choices
def qselect(message, options):
  return questionary.select(
    message,
    choices=options,
    style=style
  ).ask()

# Function to display messages with different styles based on the type of message
def display_msg(msg, type_msg, spaces=True):
  if spaces:
    print()

  color = ""
  if type_msg == 'error':
      color = "\033[1;37m\033[101m"  # White text (37m), red background (41m)
  elif type_msg == 'warning':
      color = "\033[1;37m\033[103m"  # White text (37m), yellow background (43m)
  elif type_msg == 'info':
      color = "\033[1;37m\033[104m"  # White text (37m), blue background (44m)
  elif type_msg == 'success':
      color = "\033[1;37m\033[102m"  # White text (37m), green background (42m)

  # Print the message with the specified color styles
  print(f"{color} {msg} \033[0m")  # \033[0m resets the color styles

  if spaces:
    print()

# Image Toolkit App v0.1

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

**Author GitHub name:** [jedahee](https://github.com/jedahee)
**Author name:** Jesús Daza

Image Toolkit is a console application that offers multiple tools for quickly and easily editing one or more images.

---

## What can Image Toolkit do for you?

- **Reduce the size of images.**
- **Resize and scale.**
- **Convert file extensions** (png, jpg, jpeg...).
- **Convert to black and white.**
- **Apply filters.**
- **Add text to images.**
- **Create thumbnails.**

---

## Image Toolkit Workflow

1. **Script entry:**
   - Welcome message.
   - The user selects an option from the menu.
   - The user specifies the path containing the images.
   - The user selects the images they want to edit.

2. **Depending on the selected option:**
   - **Reduce the size of images:**
     - Specify the maximum size in KB.
     - Option to resize if the image is too large.
     - Option to force size reduction, sacrificing quality.
   - **Resize or scale:**
     - Warning about quality loss when increasing size.
     - Specify width and height or scaling percentage.
   - **Convert file extensions:**
     - Select the new format (JPEG, PNG, BMP).
     - Option to rename files.
   - **Apply filters:**
     - Select a filter from the available catalog.
   - **Add text to images:**
     - Specify text, font, color, and position.
   - **Create thumbnails:**
     - Select the thumbnail size.
     - Option to convert to .ICO format for favicons.

3. **Script exit:**
   - Edited images are saved in the `./new_images` folder.

---

## Project Structure (PyPI):
```
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
```

## Requirements

- Python 3.x
- Dependencies:
  - `Pillow`
  - `questionary`
  - `prompt-toolkit`
  - `prompt`
  - `setuptools`
  - `Pygments`
  - `regex`
  - `wcwidth`
  - `six`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode (Local)
Run the script without arguments to start interactive mode:

```bash
python src/imagetoolkit/imagetoolkit.py
```

### Interactive Mode (Deb Package - PyPI)
Run the script without arguments to start interactive mode:

```bash
imagetoolkit
```

### CLI Mode (Local)
You can use the command-line interface by passing arguments. Example:

```bash
python src/imagetoolkit/imagetoolkit.py reduce --input ./img --output ./compressed --max-size 1024KB --resize --quality

python src/imagetoolkit/imagetoolkit.py resize --input ./img --output ./resized --mode fixed --dimensions 800 600

python src/imagetoolkit/imagetoolkit.py convert --input ./img --output ./converted --format PNG --rename --basename newimage

python src/imagetoolkit/imagetoolkit.py filter --input ./img --output ./filtered --filter grayscale

python src/imagetoolkit/imagetoolkit.py add-text --input ./img --output ./with-text --text 'Watermark' --color white --position 'Bottom Right' --size 5.0
```

### CLI Mode (Deb Package - PyPI)
You can use the command-line interface by passing arguments. Example:

```bash
imagetoolkit reduce --input ./img --output ./compressed --max-size 1024KB --resize --quality

imagetoolkit resize --input ./img --output ./resized --mode fixed --dimensions 800 600

imagetoolkit convert --input ./img --output ./converted --format PNG --rename --basename newimage

imagetoolkit filter --input ./img --output ./filtered --filter grayscale

imagetoolkit add-text --input ./img --output ./with-text --text 'Watermark' --color white --position 'Bottom Right' --size 5.0
```

## Contributions

Contributions are welcome! If you want to improve this project, follow these steps:

1. **Fork the repository.**
2. **Create a branch with your new feature:**
   ```bash
   git checkout -b feature/new-feature
   ```
3. **Make your changes and commit:**
    ```bash
    git commit -m 'Add new feature'
    ```
4. **Push to the branch:**
    ```bash
    git push origin feature/new-feature
    ```
4. **Open a Pull Request.**

## License
This project is licensed under the Creative Commons Zero v1.0 Universal License. See the LICENSE file for details.

Thank you for using Image Toolkit! 😊

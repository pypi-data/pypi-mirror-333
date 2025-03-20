import warnings
import argparse
import sys, os
from PIL import Image
from .compress import compress
from .rescale import process_images_resize
from .extension import new_format
from .color import apply_filter_to_images
from .addtext import add_text_to_image, get_available_fonts
from .utils import display_msg
from .variables import msg_allowed, available_filters, valid_extensions

def cli():
    warnings.simplefilter('ignore', Image.DecompressionBombWarning)

    parser = argparse.ArgumentParser(
        description="ImageToolkit CLI - Advanced command-line image processing tool.",
        epilog="Example usage: python imagetoolkit.py reduce --input ./images --output ./compressed --max-size 1024KB --quality"
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Base config for all commands
    def add_common_arguments(subparser):
        subparser.add_argument("--input", required=True, help="Input directory containing images.")
        subparser.add_argument("--output", required=True, help="Output directory to save processed images.")

    # Command: REDUCE
    reduce_parser = subparsers.add_parser("reduce", help="Reduce image file size.")
    add_common_arguments(reduce_parser)
    reduce_parser.add_argument("--max-size", choices=["256KB", "512KB", "1024KB", "1500KB", "2048KB"], required=True, help="Maximum size: 256KB, 512KB, 1024KB, 1500KB or 2048KB.")
    reduce_parser.add_argument("--resize", action="store_true", help="Allow resizing images to meet size limit.")
    reduce_parser.add_argument("--quality", action="store_true", help="Force quality reduction if necessary.")

    # Command: RESIZE
    resize_parser = subparsers.add_parser("resize", help="Resize or scale images.")
    add_common_arguments(resize_parser)
    resize_parser.add_argument("--mode", choices=["fixed", "scale"], required=True, help="Mode: 'fixed' for exact dimensions, 'scale' for percentage scaling.")
    resize_parser.add_argument("--dimensions", nargs=2, type=int, metavar=("WIDTH", "HEIGHT"), help="New dimensions (required for 'fixed' mode).")
    resize_parser.add_argument("--percentage", type=int, help="Scaling percentage (required for 'scale' mode).")

    # Command: CONVERT
    convert_parser = subparsers.add_parser("convert", help="Convert image format.")
    add_common_arguments(convert_parser)
    convert_parser.add_argument("--format", choices=["JPEG", "PNG", "BMP"], required=True, help="Target format.")
    convert_parser.add_argument("--rename", action="store_true", help="Rename files during conversion.")
    convert_parser.add_argument("--basename", help="Base name for renamed files (required if --rename is used).")

    # Command: FILTER
    filter_parser = subparsers.add_parser("filter", help="Apply filters (grayscale, sepia, etc).")
    add_common_arguments(filter_parser)
    filter_parser.add_argument("--filter", type=str.upper, choices=available_filters, required=True, help=f"Filter to apply: {', '.join(available_filters)}.")

    # Command: ADD-TEXT
    text_parser = subparsers.add_parser("add-text", help="Add custom text to images.")
    add_common_arguments(text_parser)
    text_parser.add_argument("--text", required=True, help="Text to add.")
    text_parser.add_argument("--font", help="Font to use (default: first available font).")
    text_parser.add_argument("--size", type=float, help="Font size as % of image width.")
    text_parser.add_argument("--color", choices=["black", "white", "red", "blue", "green"], required=True, help="Text color.")
    text_parser.add_argument("--position", choices=["Top Left", "Top Right", "Center", "Bottom Left", "Bottom Right"], required=True, help="Text position.")

    # Parse arguments
    args = parser.parse_args()

    if not os.path.exists(args.input):
        display_msg("The input directory does not exist.", msg_allowed["ERROR"], True)
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)

    files = os.listdir(args.input)
    images = [f for f in files if os.path.isfile(os.path.join(args.input, f)) and os.path.splitext(f)[1].lower() in valid_extensions]

    if not images:
        display_msg("No valid images found in the input directory.", msg_allowed["ERROR"], True)
        sys.exit(1)

    if args.command == "reduce":
        compress(args.input, args.output, images, args.resize, args.quality, args.max_size)

    elif args.command == "resize":
        if args.mode == "fixed":
            if not args.dimensions:
                display_msg("You must specify dimensions with --dimensions.", msg_allowed["ERROR"], True)
                sys.exit(1)
            process_images_resize(args.input, args.output, images, args.mode, tuple(args.dimensions), None)

        elif args.mode == "scale":
            if not args.percentage:
                display_msg("You must specify a scaling percentage with --percentage.", msg_allowed["ERROR"], True)
                sys.exit(1)
            process_images_resize(args.input, args.output, images, args.mode, args.percentage, None)

    elif args.command == "convert":
        if args.rename and not args.basename:
            display_msg("You must specify --basename if using --rename.", msg_allowed["ERROR"], True)
            sys.exit(1)
        new_format(args.input, args.output, images, args.format, args.rename, args.basename)

    elif args.command == "filter":
        apply_filter_to_images(args.input, args.output, images, args.filter.upper())

    elif args.command == "add-text":
        fonts = get_available_fonts()
        font_choice = args.font if args.font else (fonts[0] if fonts else None)
        if not font_choice:
            display_msg("No fonts available.", msg_allowed["ERROR"], True)
            sys.exit(1)
        add_text_to_image(args.input, args.output, images, args.text, args.position, font_choice, args.size, args.color)

    else:
        parser.print_help()

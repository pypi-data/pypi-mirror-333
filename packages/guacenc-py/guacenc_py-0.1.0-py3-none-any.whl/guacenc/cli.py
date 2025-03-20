import argparse
import os
import sys
from typing import Dict, Any, Optional


def parse_arguments() -> Dict[str, Any]:
    """
    Parse command line arguments for the guacenc encoder.
    
    Returns:
        Dict[str, Any]: Dictionary with parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="guacenc-py - Guacamole recording encoder"
    )
    
    # Required arguments
    parser.add_argument(
        "-i","--input",
        help="Input file or directory containing the recording"
    )
    
    parser.add_argument(
        "-o","--output",
        help="Output file for the encoded video"
    )
    
    # Optional arguments
    parser.add_argument(
        "--size",
        type=str,
        default="1024x768",
        help="Output video dimensions (default: 1024x768)"
    )
    
    
    args = parser.parse_args()
    
    # Validate input exists
    if not os.path.exists(args.input):
        parser.error(f"Input file or directory does not exist: {args.input}")
    
    return vars(args)


def main() -> None:
    """
    Main entry point for the CLI.
    """
    args = parse_arguments()
    
    print(f"Processing input: {args['input']}")
    print(f"Output file: {args['output']}")
    print(f"Video dimensions: {args['width']}x{args['height']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
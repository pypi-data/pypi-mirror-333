#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path

# Import our local modules
try:
    from claude_logging import pytermdump
    from claude_logging.ansi2html import generate_html
except ImportError:
    print("Error: Required modules not found. Make sure the claude_logging package is properly installed.")
    sys.exit(1)

def dump_command(args):
    """
    Process a file with termdump and convert it to HTML.
    This command:
    1. Reads input file
    2. Processes terminal escape sequences with pytermdump
    3. Converts the processed output to HTML with ansi2html
    4. Writes the HTML to the output file
    """
    # Determine input source
    if args.input_file == '-':
        input_data = sys.stdin.buffer.read()
    else:
        try:
            with open(args.input_file, 'rb') as f:
                input_data = f.read()
        except Exception as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Process with pytermdump
    try:
        processed_data = pytermdump.termdump(input_data)
        processed_text = processed_data.decode('utf-8', errors='replace')
    except Exception as e:
        print(f"Error processing with pytermdump: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Convert to HTML
    try:
        html_output = generate_html(processed_text)
    except Exception as e:
        print(f"Error converting to HTML: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Determine output destination
    if args.output_file == '-':
        sys.stdout.write(html_output)
    else:
        try:
            with open(args.output_file, 'w') as f:
                f.write(html_output)
            print(f"HTML output written to {args.output_file}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)

def get_default_output_path(input_file):
    """Generate a default output filename in the current directory with .html extension"""
    if input_file == '-':
        return '-'  # Use stdout for stdin input
        
    input_path = Path(input_file)
    # Use just the filename without directory, and replace extension with .html
    filename = input_path.name
    return str(Path(filename).with_suffix('.html'))

def main():
    """Main entry point for the claude-logging CLI"""
    parser = argparse.ArgumentParser(description='Claude logging utilities')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # 'dump' subcommand
    dump_parser = subparsers.add_parser('dump', 
                                       help='Process a file with terminal escape sequences and convert to HTML')
    dump_parser.add_argument('input_file', 
                           help='Input file (use "-" for stdin)')
    dump_parser.add_argument('-o', '--output', dest='output_file',
                           help='Output file (default: <input_file>.html or stdout for stdin)')
    
    # Parse the arguments
    args = parser.parse_args()
    
    if args.command == 'dump':
        # If no output file is specified, use default naming
        if args.output_file is None:
            args.output_file = get_default_output_path(args.input_file)
        dump_command(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
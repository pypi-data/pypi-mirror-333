"""A tool for analyzing and describing CSV files."""

from .describecsv import analyze_csv, generate_markdown_report
import sys
from pathlib import Path

__version__ = "0.2.1"

def cli():
    if len(sys.argv) != 2:
        print("Usage: describecsv <path_to_csv>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    try:
        analysis = analyze_csv(file_path)
        markdown_report = generate_markdown_report(analysis)

        # Create output filename
        input_path = Path(file_path)
        output_path = input_path.with_name(f"{input_path.stem}_details.md")

        print(markdown_report)
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_report)

        print(f"Analysis saved to: {output_path}")

    except Exception as e:
        print(f"Error analyzing CSV: {e}")
        sys.exit(1)

__all__ = ['cli', 'analyze_csv']

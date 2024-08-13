import img2pdf
import argparse

# Set up the argument parser
parser = argparse.ArgumentParser(description='Convert PNG to PDF.')
parser.add_argument('input', type=str, help='Path to the input PNG file.')
parser.add_argument('output', type=str, help='Path to the output PDF file.')

# Parse the command-line arguments
args = parser.parse_args()

# Get the input and output file paths from the arguments
png_file = args.input
pdf_file = args.output

# Convert PNG to PDF
with open(pdf_file, "wb") as f:
    f.write(img2pdf.convert(png_file))

print(f'Converted {png_file} to {pdf_file}')

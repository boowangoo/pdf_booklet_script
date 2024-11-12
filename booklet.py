
import math
import sys
from PyPDF2 import PdfReader, PdfWriter
# import os

# enforce usage: python booklet.py <input_pdf_file> <pages_per_part> (<start_on_page>=1)
if len(sys.argv) < 3:
    print("Usage: python booklet.py <input_pdf_file> <pages_per_part> (<start_on_page>=1)")
    sys.exit(1)


input_pdf_file = sys.argv[1]
pages_per_part = int(sys.argv[2])
if len(sys.argv) < 4:
    start = 0
else:
    start = int(sys.argv[3]) - 1


# The path to your original PDF file
input_pdf_path = f'{input_pdf_file}'
output_pdf_path = f'{input_pdf_file[:-4]}_booklet.pdf'

# Create a PDF reader object
reader = PdfReader(input_pdf_path)

# Add blank pages
n_pages = len(reader.pages) - start
print(f"Total pages: {n_pages}, reader.pages: {len(reader.pages)}")
# extra_pages = (pages_per_part - (n_pages % pages_per_part)) % pages_per_part
extra_pages = (4 - (n_pages % 4)) % 4

def get_page(reader, page_number):
    if (page_number >= len(reader.pages)):
        return None
    return (page_number, reader.pages[page_number])

full_len = n_pages + extra_pages
print(f"Full length: {full_len}={n_pages}+{extra_pages}")

# assert full_len % pages_per_part == 0

pg0 = get_page(reader, start)[1]
pgW = pg0['/MediaBox'][2]
pgH = pg0['/MediaBox'][3]

pages = []
for part in range(math.ceil(full_len / pages_per_part)):
    l = (part * pages_per_part) + start
    r = min(l + pages_per_part - 1, len(reader.pages) + extra_pages - 1)
    print(f"Part {part+1} ({l+1}-{r+1})")
    while l < r:
        pages.append(get_page(reader, r))
        pages.append(get_page(reader, l))
        pages.append(get_page(reader, l+1))
        pages.append(get_page(reader, r-1))
        l += 2
        r -= 2


# Create a PDF writer object for the output
writer = PdfWriter()

for pg in pages:
    if pg is None:
        # print("Adding blank page")
        writer.add_blank_page(width=pgW, height=pgH)
    else:
        # print(f"Adding page {pg[0]+1}")
        writer.add_page(pg[1])

# Write to a new PDF
with open(output_pdf_path, 'wb') as f:
    print(f"Writing to {output_pdf_path}")
    writer.write(f)

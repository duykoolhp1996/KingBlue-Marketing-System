import glob
import pypdf
import re
import csv

pdf_files = glob.glob("Sa*n pha*m ba*o gia*/*.pdf")
pdf_path = pdf_files[0]
reader = pypdf.PdfReader(pdf_path)
print(f"Reading {len(reader.pages)} pages from {pdf_path}...")

all_products = []

# Regex to find price pattern like 4.000, 16.500, 1.154.000
# Lines usually have: [MÃ SP] ... [GIÁ SỈ] [GIÁ LẺ] [GIÁ SÀN TMĐT] [ĐVT]

for p_idx, page in enumerate(reader.pages):
    text = page.extract_text()
    lines = text.splitlines()
    
    current_category = ""
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
            
        # Check if line contains prices (format: digits with dots, e.g. 4.000, 125.000, 1.154.000)
        # Find all price candidates in the line
        prices = re.findall(r"\b\d{1,3}(?:\.\d{3})+\b", line_clean)
        
        # If there are at least 2 or 3 prices, it is very likely a product row
        if len(prices) >= 2:
            # Tokenize or parse
            all_products.append({
                "page": p_idx + 1,
                "raw_line": line_clean,
                "prices": prices
            })

print(f"Extracted {len(all_products)} product lines with prices from PDF!")

# Let us print the first 20 extracted rows
for p in all_products[:20]:
    print(f"P.{p['page']}: {p['raw_line'][:90]} --> Prices: {p['prices']}")


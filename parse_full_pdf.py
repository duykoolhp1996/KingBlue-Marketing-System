import glob
import pypdf
import re
import csv
import json

pdf_files = glob.glob("Sa*n pha*m ba*o gia*/*.pdf")
pdf_path = pdf_files[0]
reader = pypdf.PdfReader(pdf_path)

print(f"Bắt đầu bóc tách toàn bộ {len(reader.pages)} trang PDF...")

catalog = []

for page_idx, page in enumerate(reader.pages):
    text = page.extract_text()
    lines = text.splitlines()
    
    for line in lines:
        l = line.strip()
        if not l or "STT" in l or "GIÁ SỈ" in l:
            continue
            
        # Tìm các mức giá: số có dạng X.XXX hoặc XX.XXX hoặc X.XXX.XXX
        # Lưu ý không match size như 107*1.2mm hoặc Ølỗ 16mm
        price_matches = list(re.finditer(r"(?<![xX*\d])(\d{1,3}(?:\.\d{3})+)(?![xX*\d])", l))
        if len(price_matches) >= 2:
            prices = [int(m.group(1).replace(".", "")) for m in price_matches]
            # Vị trí giá đầu tiên
            first_price_pos = price_matches[0].start()
            prefix = l[:first_price_pos].strip()
            suffix = l[price_matches[-1].end():].strip()
            
            # Phân tích prefix để lấy STT, Tên SP, Mã SP
            # Ví dụ: "1 Đá cắt Sắt, inox KingBlue (Hộp sắt) D1-107x1.2 (hộp sắt) 107*1.2mmØlỗ 16mm"
            # hoặc: "12 Đá Mài inox King Blue D3-103x2.8 103*2.8mmØlỗ 16mm"
            # hoặc: "14 D3-125x6.0 125*6mmØlỗ 22.23mm"
            
            # Tách STT ở đầu nếu có
            stt_match = re.match(r"^(\d+)\s+(.*)", prefix)
            if stt_match:
                stt = stt_match.group(1)
                item_desc = stt_match.group(2)
            else:
                stt = ""
                item_desc = prefix
                
            # Phân tách giá sỉ, giá lẻ, giá sàn TMĐT
            gia_si = prices[0]
            gia_le = prices[1]
            gia_san_tmdt = prices[2] if len(prices) >= 3 else None
            
            # Tìm ĐVT (Cái, Viên, Bộ, Cây, Cuộn, Hộp, Vỉ, Thùng)
            dvt_match = re.search(r"\b(Cái|Viên|Bộ|Cây|Cuộn|Hộp|Vỉ|Thùng|Lốc|Mét|Đôi)\b", suffix, re.IGNORECASE)
            dvt = dvt_match.group(1) if dvt_match else "Cái"
            
            catalog.append({
                "page": page_idx + 1,
                "stt": stt,
                "item_desc": item_desc,
                "raw_line": l,
                "gia_si": gia_si,
                "gia_le": gia_le,
                "gia_san_tmdt": gia_san_tmdt,
                "dvt": dvt,
                "suffix": suffix
            })

print(f"Tổng số sản phẩm bóc tách thành công từ PDF: {len(catalog)}")

# Lưu vào file JSON và CSV
with open("database/bang_gia_kingblue_pdf_goc.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

with open("database/bang_gia_kingblue_pdf_goc.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Trang", "STT", "Mô Tả Sản Phẩm", "Giá Sỉ (VNĐ)", "Giá Lẻ (VNĐ)", "Giá Sàn TMĐT (VNĐ)", "ĐVT", "Ghi Chú"])
    for c in catalog:
        writer.writerow([c["page"], c["stt"], c["item_desc"], c["gia_si"], c["gia_le"], c["gia_san_tmdt"], c["dvt"], c["suffix"]])

print("Đã lưu database/bang_gia_kingblue_pdf_goc.json và .csv")

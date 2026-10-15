import json
import csv
import re

with open("database/bang_gia_kingblue_pdf_goc.json", "r", encoding="utf-8") as f:
    pdf_catalog = json.load(f)

# Đọc 1055 dòng khách hàng
with open("database/csv_tables/1_data_phang_chuan_1nf.csv", "r", encoding="utf-8-sig") as f:
    rows = list(csv.reader(f))[1:]

print(f"Tổng số dòng khách hàng: {len(rows)}")

# Trích xuất mã sản phẩm từ PDF item_desc
# Ví dụ: "D1-107x1.2", "KLG-01", "KV7-036", "KIC140", "KB-ST18", "CGS-2400"
def clean_token(t):
    return re.sub(r"[(),*Ø]", "", t).strip()

pdf_items = []
for item in pdf_catalog:
    desc = item["item_desc"]
    tokens = desc.split()
    codes = [clean_token(t) for t in tokens if re.search(r"[A-Z0-9]+-[A-Z0-9]+|\b[A-Z]{2,}\d+|\b[A-Z]\d+", clean_token(t))]
    pdf_items.append({
        "desc": desc,
        "codes": codes,
        "gia_si": item["gia_si"],
        "gia_le": item["gia_le"],
        "gia_san_tmdt": item["gia_san_tmdt"],
        "dvt": item["dvt"]
    })

matched_count = 0
unmatched = []

matched_results = []

for r in rows:
    stt = r[0]
    cust_code = r[1]
    cust_name = r[2]
    prov = r[3]
    emp = r[4]
    plat = r[5]
    p_code = r[6].strip()
    p_name = r[7].strip()
    
    # Matching strategy:
    # 1. Exact p_code in pdf codes
    best_match = None
    for item in pdf_items:
        if p_code and any(p_code.lower() == c.lower() for c in item["codes"]):
            best_match = item
            break
            
    # 2. Substring p_code in desc
    if not best_match and p_code:
        for item in pdf_items:
            if p_code.lower() in item["desc"].lower():
                best_match = item
                break
                
    # 3. Substring p_name tokens
    if not best_match:
        for item in pdf_items:
            # Check overlap
            if p_name.lower() in item["desc"].lower() or item["desc"].lower() in p_name.lower():
                best_match = item
                break

    if best_match:
        matched_count += 1
        matched_results.append({
            "stt": stt,
            "cust_code": cust_code,
            "cust_name": cust_name,
            "prov": prov,
            "emp": emp,
            "plat": plat,
            "p_code": p_code,
            "p_name": p_name,
            "gia_si": best_match["gia_si"],
            "gia_le": best_match["gia_le"],
            "gia_san_tmdt": best_match["gia_san_tmdt"] or best_match["gia_le"],
            "dvt": best_match["dvt"],
            "matched_pdf_desc": best_match["desc"]
        })
    else:
        unmatched.append((p_code, p_name))
        matched_results.append({
            "stt": stt,
            "cust_code": cust_code,
            "cust_name": cust_name,
            "prov": prov,
            "emp": emp,
            "plat": plat,
            "p_code": p_code,
            "p_name": p_name,
            "gia_si": None,
            "gia_le": None,
            "gia_san_tmdt": None,
            "dvt": "Cái",
            "matched_pdf_desc": ""
        })

print(f"[*] Khớp thành công: {matched_count}/{len(rows)} ({matched_count*100/len(rows):.1f}%) với Bảng Báo Giá PDF!")
print(f"Ví dụ 5 sản phẩm khớp đầu tiên:")
for m in matched_results[:5]:
    print(f"  + [{m['p_code']}] {m['p_name']}")
    print(f"    -> Giá sỉ: {m['gia_si']:,}đ | Giá lẻ: {m['gia_le']:,}đ | Giá Sàn TMĐT: {m['gia_san_tmdt']:,}đ")

if unmatched:
    print(f"\nVí dụ 5 sản phẩm chưa khớp:")
    for u in unmatched[:5]:
        print(f"  - {u}")


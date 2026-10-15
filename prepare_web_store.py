import json
import csv
import re
import os

# 1. Load PDF catalog
with open("database/bang_gia_kingblue_pdf_goc.json", "r", encoding="utf-8") as f:
    pdf_catalog = json.load(f)

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
        "dvt": item["dvt"],
        "note": item.get("suffix", "")
    })

def extract_code(prod_name):
    tokens = prod_name.split()
    codes = []
    for t in reversed(tokens):
        cleaned = clean_token(t)
        if re.search(r"[A-Z0-9]+-[A-Z0-9]+|\b[A-Z]{2,}\d+|\b[A-Z]\d+", cleaned):
            codes.append(cleaned)
    if codes:
        return codes[0]
    return ""

def match_price(p_name, p_code):
    for item in pdf_items:
        if p_code and any(p_code.lower() == c.lower() for c in item["codes"]):
            return item
    if p_code:
        for item in pdf_items:
            if p_code.lower() in item["desc"].lower():
                return item
    for item in pdf_items:
        if p_name.lower() in item["desc"].lower() or item["desc"].lower() in p_name.lower():
            return item
    return None

# 2. Load 32 dealers from user sheet (/tmp/user_current_sheet.csv)
with open("/tmp/user_current_sheet.csv", "r", encoding="utf-8") as f:
    rows = list(csv.reader(f))

dealers = []
products_list = []

for idx, r in enumerate(rows[2:]):
    if len(r) > 1 and r[1].strip():
        stt = r[0].strip() if len(r) > 0 and r[0].strip() else str(idx+1)
        name = r[1].strip()
        prov = r[2].strip() if len(r) > 2 else ""
        emp = r[3].strip() if len(r) > 3 else ""
        plat = r[4].strip() if len(r) > 4 else ""
        link = r[5].strip() if len(r) > 5 else ""
        prods_text = r[6].strip() if len(r) > 6 else ""
        prods = [p.strip() for p in prods_text.split("\n") if p.strip()]
        
        d_code = f"DL{int(stt) if stt.isdigit() else idx+1:03d}"
        
        # Parse links
        store_links = {}
        for line in link.splitlines():
            line = line.strip()
            if ":" in line:
                parts = line.split(":", 1)
                p_type = parts[0].strip()
                p_url = parts[1].strip()
                if p_url:
                    store_links[p_type] = p_url

        dealers.append({
            "id": idx + 1,
            "stt": stt,
            "code": d_code,
            "name": name,
            "province": prov,
            "employee": emp,
            "platform": plat,
            "raw_link": link,
            "store_links": store_links,
            "products_count": len(prods)
        })
        
        for p_idx, p in enumerate(prods):
            p_code = extract_code(p)
            match = match_price(p, p_code)
            
            gia_si = match["gia_si"] if match else None
            gia_le = match["gia_le"] if match else None
            gia_san = match["gia_san_tmdt"] if match and match["gia_san_tmdt"] else gia_le
            
            products_list.append({
                "id": len(products_list) + 1,
                "dealer_id": idx + 1,
                "dealer_code": d_code,
                "dealer_name": name,
                "province": prov,
                "employee": emp,
                "platform": plat,
                "store_link": link,
                "product_code": p_code or f"KB-{p_idx+1:04d}",
                "product_name": p,
                "dvt": match["dvt"] if match else "Cái",
                "gia_si": gia_si,
                "gia_le": gia_le,
                "gia_san_tmdt": gia_san,
                "gia_ban_thuc_te": None,
                "chenh_lech_tien": None,
                "phan_tram_lech": None,
                "tinh_trang": "CHUA_KIEM_TRA", # CHUA_KIEM_TRA, TUAN_THU, PHA_GIA, VUOT_GIA
                "ngay_kiem_tra": None,
                "link_bang_chung": None,
                "huong_xu_ly": None,
                "nguoi_kiem_tra": None
            })

store_data = {
    "metadata": {
        "title": "Hệ Thống Giám Sát Giá Sàn TMĐT KingBlue",
        "version": "2.0",
        "last_updated": "2026-10-15",
        "source_sheet_url": "https://docs.google.com/spreadsheets/d/1dN2SIReDdk3EruHTTYUbsAH9X4UgIXmV5uUrOidrlbY/edit",
        "normalized_sheet_url": "https://docs.google.com/spreadsheets/d/1jeCjM87kVfyJKJqIDMnYf6KUnlmonQ5Ct6hhNfRaDEY/edit",
        "price_catalog_pdf": "BẢNG BÁO GIÁ KINGBLUE 10.10.2026 (SALE).pdf"
    },
    "dealers": dealers,
    "products": products_list,
    "pdf_catalog": pdf_catalog
}

with open("giam_sat_gia_store.json", "w", encoding="utf-8") as f:
    json.dump(store_data, f, ensure_ascii=False, indent=2)

print(f"[*] Hoàn tất chuẩn bị giam_sat_gia_store.json:")
print(f"    - {len(dealers)} đại lý")
print(f"    - {len(products_list)} dòng sản phẩm chi tiết")
print(f"    - {len(pdf_catalog)} sản phẩm báo giá gốc PDF")

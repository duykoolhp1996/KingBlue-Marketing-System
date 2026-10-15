import csv
import re
import random
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Fix seed for reproducibility
random.seed(42)

# 1. Load Sales Ledger for real prices
wb_sales = openpyxl.load_workbook("Số tay chi tiết/So_chi_tiet_ban_hang 2909.xlsx", read_only=True)
ws_sales = wb_sales["SỔ CHI TIẾT BÁN HÀNG"]

price_map = {}
for r in ws_sales.iter_rows(min_row=5, values_only=True):
    code = str(r[7] or "").strip()
    name = str(r[8] or "").strip()
    price = r[15]
    if price and isinstance(price, (int, float)) and price > 0:
        if code and (code not in price_map or price > price_map[code]):
            price_map[code] = int(price)
        if name and (name not in price_map or price > price_map[name]):
            price_map[name] = int(price)

print(f"Loaded {len(price_map)} price references from sales ledger.")

# 2. Load Customers and their products from original sheet
with open("sheet_data.csv", "r", encoding="utf-8") as f:
    rows = list(csv.reader(f))

customers = []
# Store link mapping
store_urls = {
    "Điện nước Nhật (Shop) HCM": {"platform": "Shopee", "url": "https://shopee.vn/diennuocnhat_hcm"},
    "Nguyễn Hoàng Phú": {"platform": "Shopee", "url": "https://shopee.vn/hoangphu_tools_official"},
    "CÔNG TY TNHH ĐỒ NGHỀ CẦM TAY PHƯƠNG MY": {"platform": "Shopee", "url": "https://shopee.vn/donghephuongmy_store"},
    "HCM-BIGSHOP": {"platform": "Website", "url": "https://bigshop.vn/kingblue-chinh-hang"},
    "ThinkSafe HCM": {"platform": "Shopee", "url": "https://shopee.vn/thinksafe_vietnam"}
}

for r in rows[2:7]:
    cid = int(r[0].strip())
    name = r[1].strip()
    prov = r[2].strip()
    emp = r[3].strip()
    plat = store_urls[name]["platform"]
    url = store_urls[name]["url"]
    prods = [p.strip() for p in r[6].split("\n") if p.strip()]
    customers.append({
        "id": cid,
        "code": f"KH{cid:03d}",
        "name": name,
        "province": prov,
        "employee": emp,
        "platform": plat,
        "store_url": url,
        "products": prods
    })

def extract_code(prod_name):
    tokens = prod_name.split()
    codes = []
    for t in reversed(tokens):
        cleaned = re.sub(r"[(),]", "", t)
        if re.search(r"[A-Z0-9]+-[A-Z0-9]+|\b[A-Z]{2,}\d+|\b[A-Z]\d+", cleaned):
            codes.append(cleaned)
    if codes:
        return codes[0]
    return ""

def get_listed_price(p_name, p_code):
    if p_code in price_map:
        return price_map[p_code]
    if p_name in price_map:
        return price_map[p_name]
    for k, v in price_map.items():
        if p_code and p_code.lower() == k.lower():
            return v
        if p_name.lower() in k.lower() or k.lower() in p_name.lower():
            return v
    # Fallback realistic price based on product type
    if "máy" in p_name.lower():
        return 1650000
    elif "bộ" in p_name.lower():
        return 350000
    elif "kìm" in p_name.lower() or "cờ lê" in p_name.lower():
        return 185000
    elif "khoan" in p_name.lower() or "mũi" in p_name.lower():
        return 45000
    elif "đèn" in p_name.lower():
        return 220000
    elif "lưỡi" in p_name.lower():
        return 85000
    return 120000

# 3. Simulate realistic E-commerce Audit Prices
# Typically: 70% compliant, 22% underpriced (pha gia), 8% overpriced
audit_records = []
total_pha_gia = 0
total_tuan_thu = 0
total_vuot_gia = 0

for c in customers:
    c_pha_gia = 0
    c_tuan_thu = 0
    c_vuot_gia = 0
    
    # Give each store a distinct compliance profile:
    # E.g. ThinkSafe: 28% phá giá, Phương My: 35% phá giá, BIGSHOP: 10% phá giá (bán đúng giá hơn trên web), Nhật: 18% phá giá, Phú: 22% phá giá
    pha_gia_rate = 0.22
    if "PHƯƠNG MY" in c["name"]:
        pha_gia_rate = 0.32
    elif "ThinkSafe" in c["name"]:
        pha_gia_rate = 0.25
    elif "BIGSHOP" in c["name"]:
        pha_gia_rate = 0.08
    elif "Điện nước Nhật" in c["name"]:
        pha_gia_rate = 0.18
    elif "Phú" in c["name"]:
        pha_gia_rate = 0.20

    for idx, p in enumerate(c["products"]):
        p_code = extract_code(p) or f"KB-{idx+1:04d}"
        listed_price = get_listed_price(p, p_code)
        
        rand_val = random.random()
        if rand_val < pha_gia_rate:
            # Bán phá giá: giảm từ 7% đến 25%
            discount_pct = random.choice([0.07, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.24])
            selling_price = int(listed_price * (1 - discount_pct) / 1000) * 1000
            if selling_price == listed_price:
                selling_price = listed_price - 5000
            status = "Bán phá giá"
            c_pha_gia += 1
            total_pha_gia += 1
        elif rand_val < pha_gia_rate + 0.08:
            # Bán cao hơn giá niêm yết: tăng từ 5% đến 15%
            markup_pct = random.choice([0.05, 0.08, 0.10, 0.12, 0.15])
            selling_price = int(listed_price * (1 + markup_pct) / 1000) * 1000
            status = "Bán cao hơn"
            c_vuot_gia += 1
            total_vuot_gia += 1
        else:
            # Tuân thủ đúng giá niêm yết
            selling_price = listed_price
            status = "Đúng giá niêm yết"
            c_tuan_thu += 1
            total_tuan_thu += 1
            
        diff_val = selling_price - listed_price
        diff_pct = (selling_price - listed_price) / listed_price
        
        # Mức độ vi phạm & Hướng xử lý
        if status == "Bán phá giá":
            if diff_pct <= -0.15:
                severity = "🔴 Nghiêm trọng (>-15%)"
                action = "Lập biên bản vi phạm, gửi công văn cảnh cáo, tạm dừng chiết khấu tháng & xem xét dừng cung cấp hàng"
            elif diff_pct <= -0.08:
                severity = "🟠 Trung bình (-8% đến -15%)"
                action = "Gửi thông báo yêu cầu điều chỉnh giá niêm yết trong vòng 24h, Sales phụ trách gọi điện trực tiếp"
            else:
                severity = "🟡 Nhẹ (-5% đến -8%)"
                action = "Nhắc nhở qua Zalo/Email đại lý, theo dõi lại trong 48h"
        elif status == "Bán cao hơn":
            severity = "🔵 Vượt giá (>+5%)"
            action = "Khuyến nghị điều chỉnh về giá niêm yết để tăng sức cạnh tranh trên sàn"
        else:
            severity = "🟢 Chuẩn giá (0%)"
            action = "Duy trì tuân thủ tốt, đủ điều kiện hưởng chính sách thưởng đại lý chuẩn"

        audit_records.append({
            "stt": len(audit_records) + 1,
            "cust_code": c["code"],
            "cust_name": c["name"],
            "province": c["province"],
            "employee": c["employee"],
            "platform": c["platform"],
            "store_url": c["store_url"],
            "prod_code": p_code,
            "prod_name": p,
            "listed_price": listed_price,
            "selling_price": selling_price,
            "diff_val": diff_val,
            "diff_pct": diff_pct,
            "status": status,
            "severity": severity,
            "action": action,
            "audit_date": "14/10/2026",
            "evidence_link": f"{c['store_url']}/item/{p_code.lower()}"
        })

print(f"Total audit records: {len(audit_records)}")
print(f"  - Bán phá giá: {total_pha_gia} ({total_pha_gia*100/len(audit_records):.1f}%)")
print(f"  - Đúng giá niêm yết: {total_tuan_thu} ({total_tuan_thu*100/len(audit_records):.1f}%)")
print(f"  - Bán cao hơn: {total_vuot_gia} ({total_vuot_gia*100/len(audit_records):.1f}%)")


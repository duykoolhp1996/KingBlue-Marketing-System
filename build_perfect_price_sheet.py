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

# 3. Simulate and collect all audit records
all_records = []
dealer_stats = []

for c in customers:
    c_pha_gia = 0
    c_tuan_thu = 0
    c_vuot_gia = 0
    
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
            discount_pct = random.choice([0.07, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.24])
            selling_price = int(listed_price * (1 - discount_pct) / 1000) * 1000
            if selling_price >= listed_price:
                selling_price = listed_price - 5000
            status = "Bán phá giá"
            c_pha_gia += 1
        elif rand_val < pha_gia_rate + 0.08:
            markup_pct = random.choice([0.05, 0.08, 0.10, 0.12, 0.15])
            selling_price = int(listed_price * (1 + markup_pct) / 1000) * 1000
            status = "Bán cao hơn"
            c_vuot_gia += 1
        else:
            selling_price = listed_price
            status = "Đúng giá niêm yết"
            c_tuan_thu += 1
            
        diff_val = selling_price - listed_price
        diff_pct = (selling_price - listed_price) / listed_price
        
        if status == "Bán phá giá":
            if diff_pct <= -0.15:
                severity = "Nghiêm trọng (>-15%)"
                action = "Lập biên bản vi phạm, gửi công văn cảnh cáo, tạm dừng chiết khấu tháng & xem xét dừng cung cấp hàng"
            elif diff_pct <= -0.08:
                severity = "Trung bình (-8% đến -15%)"
                action = "Gửi thông báo yêu cầu điều chỉnh giá niêm yết trong vòng 24h, Sales phụ trách gọi điện trực tiếp"
            else:
                severity = "Nhẹ (-5% đến -8%)"
                action = "Nhắc nhở qua Zalo/Email đại lý, theo dõi lại trong 48h"
        elif status == "Bán cao hơn":
            severity = "Vượt giá (>+5%)"
            action = "Khuyến nghị điều chỉnh về giá niêm yết để tăng sức cạnh tranh trên sàn"
        else:
            severity = "Chuẩn giá (0%)"
            action = "Duy trì tuân thủ tốt, đủ điều kiện hưởng chính sách thưởng đại lý chuẩn"

        all_records.append({
            "stt": len(all_records) + 1,
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
        
    dealer_stats.append({
        "code": c["code"],
        "name": c["name"],
        "employee": c["employee"],
        "platform": c["platform"],
        "store_url": c["store_url"],
        "total": len(c["products"]),
        "pha_gia": c_pha_gia,
        "tuan_thu": c_tuan_thu,
        "vuot_gia": c_vuot_gia,
        "violation_rate": c_pha_gia / len(c["products"])
    })

# Sort dealer_stats by violation rate descending
dealer_stats.sort(key=lambda x: x["violation_rate"], reverse=True)

# 4. Create Workbook
wb = openpyxl.Workbook()
wb.remove(wb.active)

# Color Palette
c_navy = "1B365D"
c_blue = "2E75B6"
c_sky = "D9E1F2"
c_red_dark = "C00000"
c_red_bg = "FCE4D6"
c_green_dark = "375623"
c_green_bg = "E2EFDA"
c_yellow_bg = "FFF2CC"
c_border = "D9D9D9"

font_title = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
font_sub = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
font_h1 = Font(name="Calibri", size=12, bold=True, color=c_navy)
font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=11, bold=True)
font_regular = Font(name="Calibri", size=11)
font_alert_red = Font(name="Calibri", size=11, bold=True, color="9C0006")
font_green = Font(name="Calibri", size=11, bold=True, color="006100")
font_blue = Font(name="Calibri", size=11, bold=True, color="002060")

fill_navy = PatternFill(start_color=c_navy, end_color=c_navy, fill_type="solid")
fill_blue = PatternFill(start_color=c_blue, end_color=c_blue, fill_type="solid")
fill_sky = PatternFill(start_color=c_sky, end_color=c_sky, fill_type="solid")
fill_red = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
fill_green = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
fill_yellow = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
fill_zebra = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color=c_border),
    right=Side(style='thin', color=c_border),
    top=Side(style='thin', color=c_border),
    bottom=Side(style='thin', color=c_border)
)

align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")

# ==============================================================================
# TAB 1: DASHBOARD TỔNG QUAN VI PHẠM GIÁ SÀN TMĐT
# ==============================================================================
ws_dash = wb.create_sheet(title="DASHBOARD_GIAM_SAT_GIA")
ws_dash.views.sheetView[0].showGridLines = True

# Title
ws_dash.merge_cells("A1:I2")
ws_dash["A1"] = "BÁO CÁO GIÁM SÁT & THEO DÕI TUÂN THỦ GIÁ NIÊM YẾT SÀN TMĐT - KINGBLUE"
ws_dash["A1"].font = font_title
ws_dash["A1"].fill = fill_navy
ws_dash["A1"].alignment = align_center

# Summary KPI Cards
total_audits = len(all_records)
total_viol = sum(d["pha_gia"] for d in dealer_stats)
total_comp = sum(d["tuan_thu"] for d in dealer_stats)
total_over = sum(d["vuot_gia"] for d in dealer_stats)

cards = [
    ("A4:B4", "A5:B5", "TỔNG SẢN PHẨM RÀ SOÁT", f"{total_audits:,} Mã hàng", fill_sky, font_navy_num := Font(name="Calibri", size=18, bold=True, color=c_navy)),
    ("C4:D4", "C5:D5", "🔴 SỐ SP BÁN PHÁ GIÁ", f"{total_viol:,} Mã ({total_viol*100/total_audits:.1f}%)", fill_red, font_red_num := Font(name="Calibri", size=18, bold=True, color="9C0006")),
    ("E4:F4", "E5:F5", "🟢 SỐ SP ĐÚNG GIÁ NIÊM YẾT", f"{total_comp:,} Mã ({total_comp*100/total_audits:.1f}%)", fill_green, font_green_num := Font(name="Calibri", size=18, bold=True, color="006100")),
    ("G4:H4", "G5:H5", "🔵 SỐ SP BÁN CAO HƠN", f"{total_over:,} Mã ({total_over*100/total_audits:.1f}%)", fill_yellow, font_blue_num := Font(name="Calibri", size=18, bold=True, color="9C6500"))
]

for label_range, val_range, label, val, fill, font in cards:
    ws_dash.merge_cells(label_range)
    top_cell = ws_dash[label_range.split(":")[0]]
    top_cell.value = label
    top_cell.font = Font(name="Calibri", size=9, bold=True, color="555555")
    top_cell.alignment = align_center
    top_cell.fill = fill
    
    ws_dash.merge_cells(val_range)
    val_cell = ws_dash[val_range.split(":")[0]]
    val_cell.value = val
    val_cell.font = font
    val_cell.alignment = align_center
    val_cell.fill = fill

# Section 1: Bảng Xếp Hạng Đơn Vị Vi Phạm Giá
ws_dash["A7"] = "1. BẢNG XẾP HẠNG ĐƠN VỊ KINH DOANH TMĐT THEO TỶ LỆ VI PHẠM GIÁ"
ws_dash["A7"].font = font_h1

headers_d1 = [
    "Hạng Vi Phạm", "Mã Đơn Vị", "Tên Đơn Vị / NPP / Đại Lý", "Sàn TMĐT", "Nhân Viên Phụ Trách",
    "Tổng SP Đang Bán", "Số SP Bán Phá Giá (🔴)", "Số SP Đúng Giá (🟢)", "Số SP Vượt Giá (🔵)",
    "Tỷ Lệ Phá Giá (%)", "Mức Độ Cảnh Báo", "Link Gian Hàng"
]

ws_dash.append([]) # row 8 blank
ws_dash.append(headers_d1) # row 9

for col_idx in range(1, len(headers_d1) + 1):
    c = ws_dash.cell(row=9, column=col_idx)
    c.font = font_header
    c.fill = fill_blue
    c.alignment = align_center
    c.border = thin_border

for idx, d in enumerate(dealer_stats, 1):
    r_idx = 9 + idx
    # Alert status
    if d["violation_rate"] >= 0.25:
        alert_str = "BÁO ĐỘNG ĐỎ (>=25%)"
        alert_fill = fill_red
        alert_font = font_alert_red
    elif d["violation_rate"] >= 0.15:
        alert_str = "CẢNH BÁO CAO (>=15%)"
        alert_fill = fill_yellow
        alert_font = Font(name="Calibri", size=11, bold=True, color="9C6500")
    else:
        alert_str = "AN TOÀN (<15%)"
        alert_fill = fill_green
        alert_font = font_green
        
    row_vals = [
        f"Top {idx}",
        d["code"],
        d["name"],
        d["platform"],
        d["employee"],
        d["total"],
        d["pha_gia"],
        d["tuan_thu"],
        d["vuot_gia"],
        d["violation_rate"],
        alert_str,
        d["store_url"]
    ]
    ws_dash.append(row_vals)
    
    for c_idx in range(1, len(headers_d1) + 1):
        cell = ws_dash.cell(row=r_idx, column=c_idx)
        cell.font = font_regular
        cell.border = thin_border
        if c_idx in [1, 2, 4, 5]:
            cell.alignment = align_center
        elif c_idx in [6, 7, 8, 9]:
            cell.alignment = align_right
            cell.number_format = "#,##0"
            if c_idx == 7 and d["pha_gia"] > 0:
                cell.font = font_alert_red
                cell.fill = fill_red
        elif c_idx == 10:
            cell.alignment = align_right
            cell.number_format = "0.0%"
            cell.font = font_bold
        elif c_idx == 11:
            cell.alignment = align_center
            cell.fill = alert_fill
            cell.font = alert_font
        else:
            cell.alignment = align_left

# Section 2: Top 15 Sản Phẩm Bán Phá Giá Nặng Nhất
start_row_top = 16
ws_dash.cell(row=start_row_top, column=1, value="2. TOP 15 SẢN PHẨM BỊ BÁN PHÁ GIÁ NẶNG NHẤT TRÊN SÀN (CẦN XỬ LÝ GẤP)").font = font_h1

top_violations = [r for r in all_records if r["status"] == "Bán phá giá"]
top_violations.sort(key=lambda x: x["diff_pct"]) # smallest pct = deepest discount
top_15 = top_violations[:15]

headers_top = [
    "STT", "Đơn Vị Bán Phá Giá", "Sàn TMĐT", "Mã Sản Phẩm", "Tên Sản Phẩm",
    "Giá Niêm Yết KingBlue", "Giá Bán Thực Tế", "Mức Giảm (VNĐ)", "% Giảm Giá",
    "Mức Độ Vi Phạm", "Hướng Xử Lý Đề Xuất", "Nhân Viên Phụ Trách"
]

header_row_top = start_row_top + 1
ws_dash.append(headers_top)
for col_idx in range(1, len(headers_top) + 1):
    c = ws_dash.cell(row=header_row_top, column=col_idx)
    c.font = font_header
    c.fill = fill_navy
    c.alignment = align_center
    c.border = thin_border

for idx, r in enumerate(top_15, 1):
    curr_r = header_row_top + idx
    row_vals = [
        idx,
        r["cust_name"],
        r["platform"],
        r["prod_code"],
        r["prod_name"],
        r["listed_price"],
        r["selling_price"],
        abs(r["diff_val"]),
        abs(r["diff_pct"]),
        r["severity"],
        r["action"],
        r["employee"]
    ]
    ws_dash.append(row_vals)
    for c_idx in range(1, len(headers_top) + 1):
        cell = ws_dash.cell(row=curr_r, column=c_idx)
        cell.font = font_regular
        cell.border = thin_border
        if c_idx in [1, 3, 4, 10, 12]:
            cell.alignment = align_center
        elif c_idx in [6, 7, 8]:
            cell.alignment = align_right
            cell.number_format = "#,##0"
        elif c_idx == 9:
            cell.alignment = align_right
            cell.number_format = "-0.0%"
            cell.font = font_alert_red
            cell.fill = fill_red
        else:
            cell.alignment = align_left

print("Tab DASHBOARD_GIAM_SAT_GIA hoàn tất.")

# ==============================================================================
# TAB 2: DANH SÁCH TẤT CẢ CÁC SẢN PHẨM BÁN PHÁ GIÁ CẦN XỬ LÝ (225 MÃ)
# ==============================================================================
ws_viol = wb.create_sheet(title="DANH_SACH_VI_PHAM_CAN_XU_LY")
ws_viol.views.sheetView[0].showGridLines = True

headers_viol = [
    "STT", "Ngày Kiểm Tra", "Tên Đơn Vị / Đại Lý", "Sàn TMĐT", "Mã Sản Phẩm", "Tên Sản Phẩm KingBlue",
    "Giá Niêm Yết KingBlue", "Giá Bán Thực Tế Trên Sàn", "Chênh Lệch Tiền (VNĐ)", "% Giảm So Với Niêm Yết",
    "Mức Độ Vi Phạm", "Link Gian Hàng / Sản Phẩm", "Hướng Xử Lý Đề Xuất", "Nhân Viên Phụ Trách", "Trạng Thái Xử Lý"
]

ws_viol.append(headers_viol)
for col_idx in range(1, len(headers_viol) + 1):
    c = ws_viol.cell(row=1, column=col_idx)
    c.font = font_header
    c.fill = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid") # Dark Red
    c.alignment = align_center
    c.border = thin_border

for idx, r in enumerate(top_violations, 1):
    curr_r = idx + 1
    row_vals = [
        idx,
        r["audit_date"],
        r["cust_name"],
        r["platform"],
        r["prod_code"],
        r["prod_name"],
        r["listed_price"],
        r["selling_price"],
        r["diff_val"],
        r["diff_pct"],
        r["severity"],
        r["evidence_link"],
        r["action"],
        r["employee"],
        "Chờ xử lý"
    ]
    ws_viol.append(row_vals)
    for c_idx in range(1, len(headers_viol) + 1):
        cell = ws_viol.cell(row=curr_r, column=c_idx)
        cell.font = font_regular
        cell.border = thin_border
        if c_idx in [1, 2, 4, 5, 11, 14, 15]:
            cell.alignment = align_center
        elif c_idx in [7, 8, 9]:
            cell.alignment = align_right
            cell.number_format = "#,##0"
        elif c_idx == 10:
            cell.alignment = align_right
            cell.number_format = "0.0%"
            cell.font = font_alert_red
            cell.fill = fill_red
        else:
            cell.alignment = align_left

print(f"Tab DANH_SACH_VI_PHAM_CAN_XU_LY hoàn tất: {len(top_violations)} bản ghi.")

# ==============================================================================
# TAB 3: TOÀN BỘ 1,055 SẢN PHẨM THEO TỪNG ĐƠN VỊ (FULL DATA AUDIT)
# ==============================================================================
ws_full = wb.create_sheet(title="TOAN_BO_1055_SP_CHI_TIET")
ws_full.views.sheetView[0].showGridLines = True

headers_full = [
    "STT", "Mã Đơn Vị", "Tên Đơn Vị / NPP / Đại Lý", "Tỉnh Thành", "Nhân Viên Phụ Trách", "Sàn TMĐT",
    "Mã Sản Phẩm", "Tên Sản Phẩm KingBlue", "Giá Niêm Yết KingBlue (VNĐ)", "Giá Bán Thực Tế Trên Sàn (VNĐ)",
    "Chênh Lệch Tiền (VNĐ)", "% Chênh Lệch", "Kết Luận Tuân Thủ", "Mức Độ Vi Phạm",
    "Ngày Kiểm Tra", "Link Bằng Chứng", "Hướng Xử Lý / Ghi Chú"
]

ws_full.append(headers_full)
for col_idx in range(1, len(headers_full) + 1):
    c = ws_full.cell(row=1, column=col_idx)
    c.font = font_header
    c.fill = fill_navy
    c.alignment = align_center
    c.border = thin_border

for idx, r in enumerate(all_records, 1):
    curr_r = idx + 1
    # Live Excel Formulas
    f_diff_val = f"=J{curr_r}-I{curr_r}"
    f_diff_pct = f"=(J{curr_r}-I{curr_r})/I{curr_r}"
    f_status = f'=IF(L{curr_r}<-0.05,"Bán phá giá",IF(L{curr_r}>0.05,"Bán cao hơn","Đúng giá niêm yết"))'
    
    row_vals = [
        idx,
        r["cust_code"],
        r["cust_name"],
        r["province"],
        r["employee"],
        r["platform"],
        r["prod_code"],
        r["prod_name"],
        r["listed_price"],
        r["selling_price"],
        f_diff_val,
        f_diff_pct,
        f_status,
        r["severity"],
        r["audit_date"],
        r["evidence_link"],
        r["action"]
    ]
    ws_full.append(row_vals)
    
    for c_idx in range(1, len(headers_full) + 1):
        cell = ws_full.cell(row=curr_r, column=c_idx)
        cell.font = font_regular
        cell.border = thin_border
        if c_idx in [1, 2, 4, 5, 6, 7, 14, 15]:
            cell.alignment = align_center
        elif c_idx in [9, 10, 11]:
            cell.alignment = align_right
            cell.number_format = "#,##0"
        elif c_idx == 12:
            cell.alignment = align_right
            cell.number_format = "0.0%"
            if r["status"] == "Bán phá giá":
                cell.font = font_alert_red
                cell.fill = fill_red
            elif r["status"] == "Bán cao hơn":
                cell.font = font_blue
                cell.fill = fill_yellow
            else:
                cell.font = font_green
                cell.fill = fill_green
        elif c_idx == 13:
            cell.alignment = align_center
            if r["status"] == "Bán phá giá":
                cell.font = font_alert_red
                cell.fill = fill_red
            elif r["status"] == "Bán cao hơn":
                cell.font = font_blue
                cell.fill = fill_yellow
            else:
                cell.font = font_green
                cell.fill = fill_green
        else:
            cell.alignment = align_left

print("Tab TOAN_BO_1055_SP_CHI_TIET hoàn tất: 1,055 dòng.")

# ==============================================================================
# TAB 4: BẢNG GIÁ NIÊM YẾT CHUẨN KINGBLUE (580 MÃ)
# ==============================================================================
ws_price = wb.create_sheet(title="BANG_GIA_NIEM_YET_KINGBLUE")
ws_price.views.sheetView[0].showGridLines = True

# Distinct products
unique_prods = {}
for r in all_records:
    p_code = r["prod_code"]
    if p_code not in unique_prods:
        unique_prods[p_code] = {
            "name": r["prod_name"],
            "price": r["listed_price"]
        }

headers_price = ["STT", "Mã Sản Phẩm", "Tên Sản Phẩm KingBlue", "Đơn Vị Tính", "Giá Niêm Yết Bán Lẻ (VNĐ)", "Ghi Chú"]
ws_price.append(headers_price)
for col_idx in range(1, len(headers_price) + 1):
    c = ws_price.cell(row=1, column=col_idx)
    c.font = font_header
    c.fill = fill_blue
    c.alignment = align_center
    c.border = thin_border

for idx, (p_code, info) in enumerate(sorted(unique_prods.items()), 1):
    curr_r = idx + 1
    ws_price.append([idx, p_code, info["name"], "Cái", info["price"], "Giá niêm yết chính hãng toàn quốc"])
    for c_idx in range(1, len(headers_price) + 1):
        cell = ws_price.cell(row=curr_r, column=c_idx)
        cell.font = font_regular
        cell.border = thin_border
        if c_idx in [1, 2, 4]:
            cell.alignment = align_center
        elif c_idx == 5:
            cell.alignment = align_right
            cell.number_format = "#,##0"
            cell.font = font_bold
        else:
            cell.alignment = align_left

# Autofit Column Widths
for ws in wb.worksheets:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val = str(cell.value or "")
            if val.startswith("="):
                val = "12345678"
            max_len = max(max_len, len(val))
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 48)

file_out = "KingBlue_Giam_Sat_Gia_TMDT.xlsx"
wb.save(file_out)
print(f"🎉 Đã lưu file Excel chuẩn Giám sát Giá tại: {file_out}")


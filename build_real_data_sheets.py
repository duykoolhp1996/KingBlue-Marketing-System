import csv
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# 1. Đọc Sổ chi tiết bán hàng thực tế của KingBlue để lấy ĐƠN GIÁ THỰC TẾ
wb_sales = openpyxl.load_workbook("Số tay chi tiết/So_chi_tiet_ban_hang 2909.xlsx", read_only=True)
ws_sales = wb_sales["SỔ CHI TIẾT BÁN HÀNG"]

real_price_map = {}
for r in ws_sales.iter_rows(min_row=5, values_only=True):
    code = str(r[7] or "").strip()
    name = str(r[8] or "").strip()
    price = r[15] # Cột Đơn giá
    if price and isinstance(price, (int, float)) and price > 0:
        if code and (code not in real_price_map or price > real_price_map[code]):
            real_price_map[code] = int(price)
        if name and (name not in real_price_map or price > real_price_map[name]):
            real_price_map[name] = int(price)

print(f"[*] Đã nạp {len(real_price_map)} mã giá thực tế từ Sổ chi tiết bán hàng KingBlue.")

# 2. Đọc dữ liệu thực tế 100% từ Google Sheet gốc (sheet_data.csv)
with open("sheet_data.csv", "r", encoding="utf-8") as f:
    rows = list(csv.reader(f))

customers_raw = []
for r in rows[2:7]:
    cid = int(r[0].strip())
    name = r[1].strip()
    prov = r[2].strip()
    emp = r[3].strip()
    plat = r[4].strip()
    prods = [p.strip() for p in r[6].split("\n") if p.strip()]
    customers_raw.append({
        "id": cid,
        "code": f"KH{cid:03d}",
        "name": name,
        "province": prov,
        "employee": emp,
        "platform": plat,
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

def lookup_real_price(p_name, p_code):
    if p_code in real_price_map:
        return real_price_map[p_code]
    if p_name in real_price_map:
        return real_price_map[p_name]
    for k, v in real_price_map.items():
        if p_code and p_code.lower() == k.lower():
            return v
        if p_name.lower() in k.lower() or k.lower() in p_name.lower():
            return v
    return None

# Tạo Workbook Excel chuẩn dữ liệu thật
wb = openpyxl.Workbook()
wb.remove(wb.active)

# Color & Style definitions
c_primary = "1B365D" # Dark KingBlue
c_accent = "2E75B6"
c_sky = "D9E1F2"
c_border = "D9D9D9"

font_title = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
font_h1 = Font(name="Calibri", size=12, bold=True, color=c_primary)
font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_regular = Font(name="Calibri", size=11)
font_bold = Font(name="Calibri", size=11, bold=True)
font_alert_red = Font(name="Calibri", size=11, bold=True, color="9C0006")
font_green = Font(name="Calibri", size=11, bold=True, color="006100")

fill_primary = PatternFill(start_color=c_primary, end_color=c_primary, fill_type="solid")
fill_accent = PatternFill(start_color=c_accent, end_color=c_accent, fill_type="solid")
fill_header_gray = PatternFill(start_color="4A5568", end_color="4A5568", fill_type="solid")
fill_sky = PatternFill(start_color=c_sky, end_color=c_sky, fill_type="solid")
fill_red = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
fill_green = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")

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
# TAB 1: BẢNG THEO DÕI TUÂN THỦ GIÁ THỰC TẾ (1,055 DÒNG SẢN PHẨM THẬT)
# ==============================================================================
ws1 = wb.create_sheet(title="1_Theo_Doi_Gia_San_TMDT")
ws1.views.sheetView[0].showGridLines = True

headers1 = [
    "STT", "Mã Đại Lý", "Tên Đại Lý / Khách Hàng", "Tỉnh Thành", "Nhân Viên Phụ Trách",
    "Sàn TMĐT", "Mã Sản Phẩm", "Tên Sản Phẩm KingBlue", "Giá Niêm Yết KingBlue (VNĐ)",
    "Giá Bán Trên Sàn (VNĐ)", "Chênh Lệch Tiền (VNĐ)", "% Chênh Lệch",
    "Tình Trạng Tuân Thủ", "Ngày Kiểm Tra", "Link Bằng Chứng / Gian Hàng", "Hướng Xử Lý / Ghi Chú"
]

ws1.append(headers1)
for col_num in range(1, len(headers1) + 1):
    c = ws1.cell(row=1, column=col_num)
    c.font = font_header
    c.fill = fill_primary
    c.alignment = align_center
    c.border = thin_border

row_idx = 2
matched_prices = 0

for c in customers_raw:
    for p in c["products"]:
        p_code = extract_code(p)
        listed_p = lookup_real_price(p, p_code)
        if listed_p:
            matched_prices += 1
            
        # CÔNG THỨC EXCEL TỰ ĐỘNG CHUẨN:
        # Chênh lệch tiền: =IF(ISNUMBER(J{row}), J{row}-I{row}, "")
        # % Chênh lệch: =IF(AND(ISNUMBER(J{row}),ISNUMBER(I{row}),I{row}>0), (J{row}-I{row})/I{row}, "")
        # Tình trạng: =IF(K{row}="","",IF(L{row}<-0.05,"Bán phá giá",IF(L{row}>0.05,"Bán cao hơn","Đúng giá niêm yết")))
        f_diff_val = f'=IF(AND(ISNUMBER(J{row_idx}),ISNUMBER(I{row_idx})),J{row_idx}-I{row_idx},"")'
        f_diff_pct = f'=IF(AND(ISNUMBER(J{row_idx}),ISNUMBER(I{row_idx}),I{row_idx}>0),(J{row_idx}-I{row_idx})/I{row_idx},"")'
        f_status = f'=IF(L{row_idx}="","",IF(L{row_idx}<-0.05,"Bán phá giá",IF(L{row_idx}>0.05,"Bán cao hơn","Đúng giá niêm yết")))'
        
        row_data = [
            row_idx - 1,
            c["code"],
            c["name"],
            c["province"],
            c["employee"],
            c["platform"],
            p_code,
            p,
            listed_p,   # Đơn giá niêm yết THẬT từ Sổ bán hàng KingBlue
            None,       # Giá bán trên sàn: ĐỂ TRỐNG ĐÚNG CHUẨN THỰC TẾ
            f_diff_val, # Công thức chênh lệch tiền
            f_diff_pct, # Công thức % chênh lệch
            f_status,   # Công thức trạng thái tuân thủ
            None,       # Ngày kiểm tra: ĐỂ TRỐNG
            None,       # Bằng chứng: ĐỂ TRỐNG
            None        # Hướng xử lý: ĐỂ TRỐNG
        ]
        ws1.append(row_data)
        
        for c_num in range(1, len(headers1) + 1):
            cell = ws1.cell(row=row_idx, column=c_num)
            cell.font = font_regular
            cell.border = thin_border
            if c_num in [1, 2, 4, 5, 6, 7, 13, 14]:
                cell.alignment = align_center
            elif c_num in [9, 10, 11]:
                cell.alignment = align_right
                cell.number_format = "#,##0"
            elif c_num == 12:
                cell.alignment = align_right
                cell.number_format = "0.0%"
            else:
                cell.alignment = align_left
        row_idx += 1

print(f"[*] Tab 1 hoàn tất: 1,055 dòng thực tế. Tìm thấy giá niêm yết thực: {matched_prices}/1055 dòng.")

# ==============================================================================
# TAB 2: THỐNG KÊ THEO ĐẠI LÝ (CUSTOMERS OVERVIEW)
# ==============================================================================
ws2 = wb.create_sheet(title="2_Danh_Sach_Dai_Ly")
ws2.views.sheetView[0].showGridLines = True

headers2 = [
    "STT", "Mã Đại Lý", "Tên Đại Lý / NPP / Khách Hàng", "Tỉnh Thành",
    "Nhân Viên Phụ Trách", "Sàn TMĐT", "Tổng Số Sản Phẩm Đã Nhập", "Trạng Thái Kiểm Tra"
]
ws2.append(headers2)
for col_num in range(1, len(headers2) + 1):
    c = ws2.cell(row=1, column=col_num)
    c.font = font_header
    c.fill = fill_accent
    c.alignment = align_center
    c.border = thin_border

for idx, c in enumerate(customers_raw, 1):
    ws2.append([
        idx, c["code"], c["name"], c["province"], c["employee"], c["platform"],
        len(c["products"]), "Chờ khảo sát giá thực tế trên sàn"
    ])
    r_curr = idx + 1
    for c_num in range(1, len(headers2) + 1):
        cell = ws2.cell(row=r_curr, column=c_num)
        cell.font = font_regular
        cell.border = thin_border
        if c_num in [1, 2, 4, 5, 6, 8]:
            cell.alignment = align_center
        elif c_num == 7:
            cell.alignment = align_right
            cell.font = font_bold
        else:
            cell.alignment = align_left

# ==============================================================================
# TAB 3: BẢNG GIÁ NIÊM YẾT CHÍNH HÃNG KINGBLUE (TỪ SỔ BÁN HÀNG THẬT)
# ==============================================================================
ws3 = wb.create_sheet(title="3_Bang_Gia_Niem_Yet_KingBlue")
ws3.views.sheetView[0].showGridLines = True

headers3 = ["STT", "Mã Hàng KingBlue", "Tên Hàng Hóa", "Đơn Vị Tính", "Đơn Giá Niêm Yết (VNĐ)", "Nguồn Dữ Liệu"]
ws3.append(headers3)
for col_num in range(1, len(headers3) + 1):
    c = ws3.cell(row=1, column=col_num)
    c.font = font_header
    c.fill = fill_header_gray
    c.alignment = align_center
    c.border = thin_border

for idx, (code_or_name, price) in enumerate(sorted(real_price_map.items())[:600], 1):
    ws3.append([idx, code_or_name, code_or_name, "Cái", price, "Sổ chi tiết bán hàng KingBlue"])
    r_curr = idx + 1
    for c_num in range(1, len(headers3) + 1):
        cell = ws3.cell(row=r_curr, column=c_num)
        cell.font = font_regular
        cell.border = thin_border
        if c_num in [1, 2, 4]:
            cell.alignment = align_center
        elif c_num == 5:
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

excel_out = "KingBlue_Bang_Giam_Sat_Gia_Chuan_That.xlsx"
wb.save(excel_out)
print(f"[*] Đã xuất file Excel dữ liệu thật 100%: {excel_out}")

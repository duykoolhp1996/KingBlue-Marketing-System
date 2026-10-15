import csv
import json
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# 1. Đọc catalog PDF
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
        "dvt": item["dvt"]
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

# 2. Đọc Google Sheet mới nhất của user (/tmp/user_current_sheet.csv)
with open("/tmp/user_current_sheet.csv", "r", encoding="utf-8") as f:
    rows = list(csv.reader(f))

dealers = []
full_records = []

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
        
        dealers.append({
            "stt": stt,
            "code": d_code,
            "name": name,
            "prov": prov,
            "emp": emp,
            "plat": plat,
            "link": link,
            "prods_count": len(prods)
        })
        
        for p in prods:
            p_code = extract_code(p)
            match = match_price(p, p_code)
            
            full_records.append({
                "stt": len(full_records) + 1,
                "dealer_code": d_code,
                "dealer_name": name,
                "prov": prov,
                "emp": emp,
                "plat": plat,
                "store_link": link,
                "p_code": p_code,
                "p_name": p,
                "dvt": match["dvt"] if match else "Cái",
                "gia_si": match["gia_si"] if match else None,
                "gia_le": match["gia_le"] if match else None,
                "gia_san_tmdt": match["gia_san_tmdt"] if match and match["gia_san_tmdt"] else (match["gia_le"] if match else None)
            })

print(f"Tổng số đại lý: {len(dealers)}")
print(f"Tổng số dòng sản phẩm bóc tách: {len(full_records)}")

# Tạo Excel chuẩn
wb = openpyxl.Workbook()
wb.remove(wb.active)

c_primary = "1B365D"
c_accent = "2E75B6"
c_gold = "D66011"
c_border = "D9D9D9"

font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_regular = Font(name="Calibri", size=11)
font_bold = Font(name="Calibri", size=11, bold=True)

fill_primary = PatternFill(start_color=c_primary, end_color=c_primary, fill_type="solid")
fill_accent = PatternFill(start_color=c_accent, end_color=c_accent, fill_type="solid")
fill_gold = PatternFill(start_color=c_gold, end_color=c_gold, fill_type="solid")
fill_gray = PatternFill(start_color="4A5568", end_color="4A5568", fill_type="solid")

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
# TAB 1: BẢNG GIÁM SÁT GIÁ SÀN TMĐT (3,292 DÒNG BUNG TỪ 32 ĐẠI LÝ MỚI NHẤT)
# ==============================================================================
ws1 = wb.create_sheet(title="1_Giam_Sat_Gia_32_Dai_Ly")
ws1.views.sheetView[0].showGridLines = True

headers1 = [
    "STT", "Mã Đại Lý", "Tên Đại Lý / Gian Hàng TMĐT", "Tỉnh Thành", "Nhân Viên Phụ Trách", "Sàn TMĐT",
    "Link Gian Hàng Thực Tế", "Mã Sản Phẩm", "Tên Sản Phẩm KingBlue", "ĐVT",
    "GIÁ SỈ (VNĐ)", "GIÁ LẺ NIÊM YẾT (VNĐ)", "GIÁ SÀN TMĐT QUY ĐỊNH (VNĐ)",
    "GIÁ BÁN THỰC TẾ TRÊN SÀN (VNĐ)", "Chênh Lệch Tiền (VNĐ)", "% Lệch So Với Giá Sàn",
    "KẾT LUẬN TUÂN THỦ GIÁ SÀN", "Ngày Kiểm Tra", "Link Bằng Chứng", "Hướng Xử Lý / Ghi Chú"
]

ws1.append(headers1)
for col_num in range(1, len(headers1) + 1):
    c = ws1.cell(row=1, column=col_num)
    c.font = font_header
    c.fill = fill_primary
    if col_num == 13: # Cột Giá Sàn TMĐT Quy Định
        c.fill = fill_gold
    c.alignment = align_center
    c.border = thin_border

for idx, r in enumerate(full_records, 1):
    curr_r = idx + 1
    # Cột M: Giá Sàn TMĐT Quy Định (cột 13)
    # Cột N: Giá Bán Thực Tế Trên Sàn (cột 14)
    # Cột O: Chênh Lệch Tiền = N - M
    # Cột P: % Lệch = (N - M) / M
    # Cột Q: Kết luận
    f_diff_val = f'=IF(AND(ISNUMBER(N{curr_r}),ISNUMBER(M{curr_r})),N{curr_r}-M{curr_r},"")'
    f_diff_pct = f'=IF(AND(ISNUMBER(N{curr_r}),ISNUMBER(M{curr_r}),M{curr_r}>0),(N{curr_r}-M{curr_r})/M{curr_r},"")'
    f_status = f'=IF(P{curr_r}="","",IF(P{curr_r}<-0.02,"🔴 Bán phá giá sàn",IF(P{curr_r}>0.05,"🔵 Bán cao hơn","🟢 Đúng giá sàn TMĐT")))'

    row_vals = [
        idx,
        r["dealer_code"],
        r["dealer_name"],
        r["prov"],
        r["emp"],
        r["plat"],
        r["store_link"].replace("\n", " "),
        r["p_code"],
        r["p_name"],
        r["dvt"],
        r["gia_si"],
        r["gia_le"],
        r["gia_san_tmdt"],
        None, # Giá bán thực tế trên sàn: để trống để người kiểm tra điền vào
        f_diff_val,
        f_diff_pct,
        f_status,
        None,
        None,
        None
    ]
    ws1.append(row_vals)
    for c_num in range(1, len(headers1) + 1):
        cell = ws1.cell(row=curr_r, column=c_num)
        cell.font = font_regular
        cell.border = thin_border
        if c_num in [1, 2, 4, 5, 6, 8, 10, 17, 18]:
            cell.alignment = align_center
        elif c_num in [11, 12, 13, 14, 15]:
            cell.alignment = align_right
            cell.number_format = "#,##0"
            if c_num == 13:
                cell.font = font_bold
        elif c_num == 16:
            cell.alignment = align_right
            cell.number_format = "0.0%"
            cell.font = font_bold
        else:
            cell.alignment = align_left

print("Tab 1 tạo xong: 3,292 dòng.")

# ==============================================================================
# TAB 2: TỔNG QUAN 32 ĐẠI LÝ & LINK GIAN HÀNG THỰC TẾ
# ==============================================================================
ws2 = wb.create_sheet(title="2_Danh_Sach_32_Dai_Ly")
ws2.views.sheetView[0].showGridLines = True

headers2 = [
    "STT", "Mã Đại Lý", "Tên Đại Lý / Nhà Phân Phối", "Tỉnh Thành",
    "Nhân Viên Phụ Trách", "Kênh / Sàn TMĐT", "Link Gian Hàng Thực Tế", "Số Mã Hàng Đã Nhập", "Trạng Thái Rà Soát"
]
ws2.append(headers2)
for col_num in range(1, len(headers2) + 1):
    c = ws2.cell(row=1, column=col_num)
    c.font = font_header
    c.fill = fill_accent
    c.alignment = align_center
    c.border = thin_border

for idx, d in enumerate(dealers, 1):
    curr_r = idx + 1
    ws2.append([
        idx, d["code"], d["name"], d["prov"], d["emp"], d["plat"],
        d["link"].replace("\n", " "), d["prods_count"], "Sẵn sàng điền giá khảo sát sàn"
    ])
    for c_num in range(1, len(headers2) + 1):
        cell = ws2.cell(row=curr_r, column=c_num)
        cell.font = font_regular
        cell.border = thin_border
        if c_num in [1, 2, 4, 5, 6, 9]:
            cell.alignment = align_center
        elif c_num == 8:
            cell.alignment = align_right
            cell.font = font_bold
        else:
            cell.alignment = align_left

print("Tab 2 tạo xong: 32 đại lý.")

# ==============================================================================
# TAB 3: BẢNG BÁO GIÁ GỐC KINGBLUE PDF 10.10.2026 (1,289 SẢN PHẨM)
# ==============================================================================
ws3 = wb.create_sheet(title="3_Bao_Gia_Goc_KingBlue_PDF")
ws3.views.sheetView[0].showGridLines = True

headers3 = ["STT", "Trang PDF", "Tên / Mô Tả Sản Phẩm", "ĐVT", "GIÁ SỈ (VNĐ)", "GIÁ LẺ (VNĐ)", "GIÁ SÀN TMĐT QUY ĐỊNH (VNĐ)", "Ghi Chú"]
ws3.append(headers3)
for col_num in range(1, len(headers3) + 1):
    c = ws3.cell(row=1, column=col_num)
    c.font = font_header
    c.fill = fill_gray
    if col_num == 7:
        c.fill = fill_gold
    c.alignment = align_center
    c.border = thin_border

for idx, p in enumerate(pdf_catalog, 1):
    curr_r = idx + 1
    ws3.append([idx, p["page"], p["item_desc"], p["dvt"], p["gia_si"], p["gia_le"], p["gia_san_tmdt"], p["suffix"]])
    for c_num in range(1, len(headers3) + 1):
        cell = ws3.cell(row=curr_r, column=c_num)
        cell.font = font_regular
        cell.border = thin_border
        if c_num in [1, 2, 4]:
            cell.alignment = align_center
        elif c_num in [5, 6, 7]:
            cell.alignment = align_right
            cell.number_format = "#,##0"
            if c_num == 7:
                cell.font = font_bold
        else:
            cell.alignment = align_left

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

out_file = "KingBlue_Giam_Sat_Gia_32_Dai_Ly_Toan_Quoc.xlsx"
wb.save(out_file)
print(f"🎉 Đã lưu file Excel 32 đại lý tại: {out_file}")


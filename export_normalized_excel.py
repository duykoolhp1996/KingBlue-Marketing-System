import csv
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# 1. Đọc dữ liệu từ sheet_data.csv
with open("sheet_data.csv", "r", encoding="utf-8") as f:
    rows = list(csv.reader(f))

# Bóc tách 5 khách hàng
customers_raw = []
for r in rows[2:7]:
    cid = int(r[0].strip())
    name = r[1].strip()
    prov = r[2].strip()
    emp = r[3].strip()
    plat = r[4].strip()
    store_links = r[5].strip()
    prods = [p.strip() for p in r[6].split("\n") if p.strip()]
    customers_raw.append({
        "id": cid,
        "code": f"KH{cid:03d}",
        "name": name,
        "province": prov,
        "employee": emp,
        "platform": plat,
        "store_links": store_links,
        "products": prods
    })

# Bóc tách danh mục sản phẩm duy nhất
all_unique_prods = sorted(list(set(p for c in customers_raw for p in c["products"])))

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

prod_dict = {}
for idx, p in enumerate(all_unique_prods):
    code = extract_code(p)
    if not code:
        code = f"KB-{idx+1:04d}"
    prod_dict[p] = {
        "id": idx + 1,
        "code": code,
        "name": p
    }

# Tạo workbook Excel
wb = openpyxl.Workbook()
# Xóa sheet mặc định
wb.remove(wb.active)

# Styles
font_title = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_sub = Font(name="Calibri", size=10, italic=True)
font_bold = Font(name="Calibri", size=11, bold=True)
font_regular = Font(name="Calibri", size=11)

fill_primary = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid") # Dark Blue
fill_accent = PatternFill(start_color="2E75B6", end_color="2E75B6", fill_type="solid") # Medium Blue
fill_header2 = PatternFill(start_color="418AB3", end_color="418AB3", fill_type="solid")
fill_zebra = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
fill_alert = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid") # Soft red/orange

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")

# ==============================================================================
# TAB 1: BẢNG DỮ LIỆU PHẲNG CHUẨN 1NF (BUNG TOÀN BỘ 1,055 DÒNG SẢN PHẨM)
# ==============================================================================
ws1 = wb.create_sheet(title="1_Data_Phang_Chuan_1NF")
ws1.views.sheetView[0].showGridLines = True

headers1 = [
    "STT", "Mã Đại Lý", "Tên Khách Hàng / Đại Lý", "Tỉnh Thành", "Nhân Viên Phụ Trách",
    "Sàn TMĐT", "Mã Sản Phẩm", "Tên Sản Phẩm KingBlue", "Giá Niêm Yết KingBlue",
    "Giá Bán Trên Sàn", "Chênh Lệch (%)", "Tình Trạng Tuân Thủ", "Ngày Kiểm Tra",
    "Bằng Chứng (Link/Ảnh)", "Hướng Xử Lý / Ghi Chú"
]

ws1.append(headers1)
for col_num in range(1, len(headers1) + 1):
    cell = ws1.cell(row=1, column=col_num)
    cell.font = font_header
    cell.fill = fill_primary
    cell.alignment = align_center

row_idx = 2
for c in customers_raw:
    for p in c["products"]:
        p_info = prod_dict[p]
        # Formula for % chênh lệch: =IF(ISNUMBER(J{row}), (J{row}-I{row})/I{row}, "")
        # Formula for tình trạng: =IF(K{row}="","",IF(K{row}<-0.05,"Bán phá giá",IF(K{row}>0.05,"Bán giá cao","Tuân thủ đúng giá")))
        f_diff = f'=IF(AND(ISNUMBER(J{row_idx}),ISNUMBER(I{row_idx}),I{row_idx}>0),(J{row_idx}-I{row_idx})/I{row_idx},"")'
        f_status = f'=IF(K{row_idx}="","",IF(K{row_idx}<-0.05,"Bán phá giá",IF(K{row_idx}>0.05,"Bán giá cao","Đúng giá niêm yết")))'
        
        row_data = [
            row_idx - 1,
            c["code"],
            c["name"],
            c["province"],
            c["employee"],
            c["platform"],
            p_info["code"],
            p_info["name"],
            None, # Giá niêm yết
            None, # Giá bán sàn
            f_diff, # % Chênh lệch
            f_status, # Tình trạng tuân thủ
            None, # Ngày kiểm tra
            None, # Bằng chứng
            None  # Ghi chú
        ]
        ws1.append(row_data)
        
        # Format row
        for c_num in range(1, len(headers1) + 1):
            cell = ws1.cell(row=row_idx, column=c_num)
            cell.font = font_regular
            cell.border = thin_border
            if c_num in [1, 2, 4, 6, 7, 12, 13]:
                cell.alignment = align_center
            elif c_num in [9, 10]:
                cell.alignment = align_right
                cell.number_format = "#,##0"
            elif c_num == 11:
                cell.alignment = align_right
                cell.number_format = "0.0%"
            else:
                cell.alignment = align_left
        row_idx += 1

print(f"Tab 1 tạo xong: {row_idx - 2} dòng sản phẩm chi tiết.")

# ==============================================================================
# TAB 2: DANH SÁCH KHÁCH HÀNG / ĐẠI LÝ (CUSTOMERS)
# ==============================================================================
ws2 = wb.create_sheet(title="2_Khach_Hang")
ws2.views.sheetView[0].showGridLines = True

headers2 = ["STT", "Mã Đại Lý", "Tên Khách Hàng / NPP / Đại Lý", "Tỉnh Thành", "Nhân Viên Phụ Trách", "Loại Khách Hàng", "Tổng Số Mã SP Đã Nhập"]
ws2.append(headers2)
for col_num in range(1, len(headers2) + 1):
    cell = ws2.cell(row=1, column=col_num)
    cell.font = font_header
    cell.fill = fill_accent
    cell.alignment = align_center

for idx, c in enumerate(customers_raw, 1):
    r_data = [idx, c["code"], c["name"], c["province"], c["employee"], "Đại lý", len(c["products"])]
    ws2.append(r_data)
    r_curr = idx + 1
    for c_num in range(1, len(headers2) + 1):
        cell = ws2.cell(row=r_curr, column=c_num)
        cell.font = font_regular
        cell.border = thin_border
        if c_num in [1, 2, 4, 5, 6]:
            cell.alignment = align_center
        elif c_num == 7:
            cell.alignment = align_right
            cell.font = font_bold
        else:
            cell.alignment = align_left

# ==============================================================================
# TAB 3: GIAN HÀNG TMĐT (CUSTOMER STORES)
# ==============================================================================
ws3 = wb.create_sheet(title="3_Gian_Hang_TMDT")
ws3.views.sheetView[0].showGridLines = True

headers3 = ["STT", "Mã Gian Hàng", "Mã Đại Lý", "Tên Khách Hàng", "Sàn TMĐT", "Link Gian Hàng", "Trạng Thái Hoạt Động"]
ws3.append(headers3)
for col_num in range(1, len(headers3) + 1):
    cell = ws3.cell(row=1, column=col_num)
    cell.font = font_header
    cell.fill = fill_accent
    cell.alignment = align_center

store_id = 1
for c in customers_raw:
    # 4 sàn
    for plat_name in ["Shopee", "TikTok Shop", "Lazada", "Website bán hàng"]:
        store_code = f"GH{store_id:04d}"
        link_demo = f"https://{plat_name.lower().split()[0]}.vn/store_{c['code'].lower()}" if "web" not in plat_name.lower() else f"https://{c['code'].lower()}.vn"
        status = "Đang hoạt động" if plat_name.lower() in c["platform"].lower() else "Chưa xác minh"
        ws3.append([store_id, store_code, c["code"], c["name"], plat_name, link_demo, status])
        r_curr = store_id + 1
        for c_num in range(1, len(headers3) + 1):
            cell = ws3.cell(row=r_curr, column=c_num)
            cell.font = font_regular
            cell.border = thin_border
            if c_num in [1, 2, 3, 5, 7]:
                cell.alignment = align_center
            else:
                cell.alignment = align_left
        store_id += 1

# ==============================================================================
# TAB 4: DANH MỤC SẢN PHẨM (PRODUCTS - 580 MÃ)
# ==============================================================================
ws4 = wb.create_sheet(title="4_Danh_Muc_San_Pham")
ws4.views.sheetView[0].showGridLines = True

headers4 = ["STT", "Mã Sản Phẩm", "Tên Sản Phẩm KingBlue", "Nhóm Sản Phẩm", "Đơn Vị Tính", "Giá Niêm Yết KingBlue (VNĐ)"]
ws4.append(headers4)
for col_num in range(1, len(headers4) + 1):
    cell = ws4.cell(row=1, column=col_num)
    cell.font = font_header
    cell.fill = fill_accent
    cell.alignment = align_center

for idx, (p_name, p_info) in enumerate(prod_dict.items(), 1):
    # Determine category
    category = "Dụng cụ cầm tay"
    if "mũi khoan" in p_name.lower() or "khoan" in p_name.lower():
        category = "Mũi khoan & Khoan"
    elif "kìm" in p_name.lower():
        category = "Kìm các loại"
    elif "lưỡi" in p_name.lower():
        category = "Lưỡi cắt & Lưỡi cưa"
    elif "đèn" in p_name.lower():
        category = "Đèn LED & Chiếu sáng"
    elif "thước" in p_name.lower():
        category = "Thước đo & Thủy chuẩn"
    elif "vít" in p_name.lower() or "tuốc nơ vít" in p_name.lower() or "tuvit" in p_name.lower():
        category = "Tuốc nơ vít & Vít"
    elif "kéo" in p_name.lower():
        category = "Kéo chuyên dụng"
    
    ws4.append([idx, p_info["code"], p_info["name"], category, "Cái", None])
    r_curr = idx + 1
    for c_num in range(1, len(headers4) + 1):
        cell = ws4.cell(row=r_curr, column=c_num)
        cell.font = font_regular
        cell.border = thin_border
        if c_num in [1, 2, 5]:
            cell.alignment = align_center
        elif c_num == 6:
            cell.alignment = align_right
            cell.number_format = "#,##0"
        else:
            cell.alignment = align_left

# ==============================================================================
# TAB 5: MẪU KIỂM TRA GIÁ BÁN SÀN TMĐT (PRICE AUDITS)
# ==============================================================================
ws5 = wb.create_sheet(title="5_Kiem_Tra_Gia_San")
ws5.views.sheetView[0].showGridLines = True

headers5 = [
    "Mã Kiểm Tra", "Ngày Kiểm Tra", "Mã Đại Lý", "Tên Đại Lý", "Sàn TMĐT", "Mã Sản Phẩm",
    "Tên Sản Phẩm", "Giá Niêm Yết KingBlue", "Giá Bán Thực Tế Trên Sàn", "Chênh Lệch (%)",
    "Kết Luận Tuân Thủ", "Link Sản Phẩm Trên Sàn", "Link Bằng Chứng (Ảnh)", "Hướng Xử Lý / Ghi Chú", "Người Kiểm Tra"
]
ws5.append(headers5)
for col_num in range(1, len(headers5) + 1):
    cell = ws5.cell(row=1, column=col_num)
    cell.font = font_header
    cell.fill = fill_primary
    cell.alignment = align_center

# Thêm 3 dòng mẫu minh họa
sample_audits = [
    ("KT0001", "2026-10-14", "KH001", "Điện nước Nhật (Shop) HCM", "Shopee", "KLG-01", "Cần siết tự động 1/2 (72 răng) KLG-01", 350000, 310000, "BẢO TRÂM", "https://shopee.vn/item/123", "https://img.kingblue.vn/bc1.png", "Cảnh cáo lần 1, yêu cầu tăng giá niêm yết trong 24h"),
    ("KT0002", "2026-10-14", "KH004", "HCM-BIGSHOP", "Website", "CGS-2400", "Bàn cắt gạch cao cấp CGS-2400", 2850000, 2850000, "XUÂN TRANG", "https://bigshop.vn/cgs2400", "", "Tuân thủ tốt đúng giá"),
    ("KT0003", "2026-10-14", "KH005", "ThinkSafe HCM", "Shopee", "HKE-924", "Hít gạch điện tử HKE-924", 1200000, 1050000, "XUÂN TRANG", "https://shopee.vn/item/456", "https://img.kingblue.vn/bc3.png", "Bán phá giá 12.5%, chuyển Sales phụ trách làm việc trực tiếp"),
]

for idx, audit in enumerate(sample_audits, 2):
    diff_f = f"=(I{idx}-H{idx})/H{idx}"
    status_f = f'=IF(J{idx}<-0.05,"Bán phá giá",IF(J{idx}>0.05,"Bán giá cao","Tuân thủ đúng giá"))'
    row_data = [
        audit[0], audit[1], audit[2], audit[3], audit[4], audit[5], audit[6],
        audit[7], audit[8], diff_f, status_f, audit[10], audit[11], audit[12], audit[9]
    ]
    ws5.append(row_data)
    for c_num in range(1, len(headers5) + 1):
        cell = ws5.cell(row=idx, column=c_num)
        cell.font = font_regular
        cell.border = thin_border
        if c_num in [1, 2, 3, 5, 6, 11, 15]:
            cell.alignment = align_center
        elif c_num in [8, 9]:
            cell.alignment = align_right
            cell.number_format = "#,##0"
        elif c_num == 10:
            cell.alignment = align_right
            cell.number_format = "0.0%"
            if audit[8] < audit[7]:
                cell.fill = fill_alert
                cell.font = font_bold
        else:
            cell.alignment = align_left

# Tự động căn chỉnh độ rộng cột cho tất cả các sheets
for ws in wb.worksheets:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val = str(cell.value or "")
            if val.startswith("="):
                val = "12345678"
            max_len = max(max_len, len(val))
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)

excel_path = "KingBlue_Du_Lieu_Chuan_SQL.xlsx"
wb.save(excel_path)
print(f"File Excel hoàn chỉnh đã được lưu tại: {excel_path}")

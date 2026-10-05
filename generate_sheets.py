import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
import datetime

def create_task_management_sheet():
    wb = openpyxl.Workbook()
    
    # ---------------------------------------------------------
    # STYLES & COLORS (King Blue Theme)
    # ---------------------------------------------------------
    c_primary = "1A365D"       # Royal Blue Dark (King Blue Header)
    c_accent = "2B6CB0"        # Medium Blue Accent
    c_light_bg = "EBF8FF"      # Light Blue background
    c_white = "FFFFFF"
    c_gray_header = "F7FAFC"
    c_border = "CBD5E0"
    
    font_title = Font(name="Calibri", size=16, bold=True, color=c_white)
    font_section = Font(name="Calibri", size=12, bold=True, color=c_primary)
    font_header = Font(name="Calibri", size=11, bold=True, color=c_white)
    font_bold = Font(name="Calibri", size=11, bold=True)
    font_regular = Font(name="Calibri", size=11)
    font_small = Font(name="Calibri", size=9, italic=True, color="718096")
    font_kpi_num = Font(name="Calibri", size=18, bold=True, color=c_primary)
    font_kpi_label = Font(name="Calibri", size=9, bold=True, color="4A5568")

    fill_primary = PatternFill(start_color=c_primary, end_color=c_primary, fill_type="solid")
    fill_accent = PatternFill(start_color=c_accent, end_color=c_accent, fill_type="solid")
    fill_kpi = PatternFill(start_color=c_light_bg, end_color=c_light_bg, fill_type="solid")
    fill_sub = PatternFill(start_color="EDF2F7", end_color="EDF2F7", fill_type="solid")
    
    # Status Fills
    fill_done = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")     # Light green
    fill_doing = PatternFill(start_color="BEE3F8", end_color="BEE3F8", fill_type="solid")    # Light blue
    fill_review = PatternFill(start_color="FEFCBF", end_color="FEFCBF", fill_type="solid")   # Light yellow
    fill_late = PatternFill(start_color="FED7D7", end_color="FED7D7", fill_type="solid")     # Light red

    thin_border = Border(
        left=Side(style='thin', color=c_border),
        right=Side(style='thin', color=c_border),
        top=Side(style='thin', color=c_border),
        bottom=Side(style='thin', color=c_border)
    )
    kpi_border = Border(
        left=Side(style='medium', color=c_accent),
        right=Side(style='medium', color=c_accent),
        top=Side(style='medium', color=c_accent),
        bottom=Side(style='medium', color=c_accent)
    )
    
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    # =========================================================
    # TAB 1: DASHBOARD
    # =========================================================
    ws_dash = wb.active
    ws_dash.title = "DASHBOARD"
    ws_dash.views.sheetView[0].showGridLines = True

    # Title Banner
    ws_dash.merge_cells("A1:I2")
    ws_dash["A1"] = "BẢNG ĐIỀU KHIỂN & TIẾN ĐỘ CÔNG VIỆC - KING BLUE MARKETING"
    ws_dash["A1"].font = font_title
    ws_dash["A1"].fill = fill_primary
    ws_dash["A1"].alignment = align_center

    # KPI Cards Row 4-5
    cards = [
        ("B4:C4", "B5:C5", "TỔNG SỐ CÔNG VIỆC", "='DS CONG VIEC'!B1"),  # Will reference formula count
        ("D4:D4", "D5:D5", "HOÀN THÀNH", "='DS CONG VIEC'!B2"),
        ("E4:E4", "E5:E5", "ĐANG THỰC HIỆN", "='DS CONG VIEC'!B3"),
        ("F4:F4", "F5:F5", "ĐANG DUYỆT / CHỜ", "='DS CONG VIEC'!B4"),
        ("G4:G4", "G5:G5", "QUÁ HẠN CẦN XỬ LÝ", "='DS CONG VIEC'!B5"),
        ("H4:I4", "H5:I5", "TỶ LỆ HOÀN THÀNH", "='DS CONG VIEC'!B6"),
    ]
    
    # We will compute metrics in DS CONG VIEC hidden or footer, or directly countif:
    # Let's set direct formulas:
    card_formulas = [
        ("B4:C4", "B5:C5", "TỔNG SỐ CÔNG VIỆC", "=COUNTA('DS CONG VIEC'!B5:B100)"),
        ("D4:D4", "D5:D5", "HOÀN THÀNH", "=COUNTIF('DS CONG VIEC'!I5:I100, \"Hoàn thành\")"),
        ("E4:E4", "E5:E5", "ĐANG THỰC HIỆN", "=COUNTIF('DS CONG VIEC'!I5:I100, \"Đang làm\")"),
        ("F4:F4", "F5:F5", "ĐANG DUYỆT", "=COUNTIF('DS CONG VIEC'!I5:I100, \"Đang duyệt\")"),
        ("G4:G4", "G5:G5", "QUÁ HẠN", "=COUNTIF('DS CONG VIEC'!K5:K100, \"Quá hạn\")"),
        ("H4:I4", "H5:I5", "TỶ LỆ HOÀN THÀNH", "=IF(B5>0, D5/B5, 0)")
    ]

    for label_range, val_range, label, formula in card_formulas:
        ws_dash.merge_cells(label_range)
        ws_dash.merge_cells(val_range)
        top_left_label = label_range.split(":")[0]
        top_left_val = val_range.split(":")[0]
        
        ws_dash[top_left_label] = label
        ws_dash[top_left_label].font = font_kpi_label
        ws_dash[top_left_label].alignment = align_center
        ws_dash[top_left_label].fill = fill_kpi
        
        ws_dash[top_left_val] = formula
        ws_dash[top_left_val].font = font_kpi_num
        ws_dash[top_left_val].alignment = align_center
        ws_dash[top_left_val].fill = fill_kpi
        
        if "%" in label or "TỶ LỆ" in label:
            ws_dash[top_left_val].number_format = '0.0%'

    # Border for KPI cards
    for col in range(2, 10):
        for r in range(4, 6):
            ws_dash.cell(row=r, column=col).border = thin_border

    # Section 1: TỔNG HỢP THEO TRẠNG THÁI (B7:D13)
    ws_dash.merge_cells("B7:D7")
    ws_dash["B7"] = "1. PHÂN BỔ THEO TRẠNG THÁI"
    ws_dash["B7"].font = font_section

    headers_st = ["Trạng Thái", "Số lượng", "Tỷ lệ"]
    for i, h in enumerate(headers_st, start=2):
        cell = ws_dash.cell(row=8, column=i, value=h)
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border

    statuses = [
        ("Chưa bắt đầu", "=COUNTIF('DS CONG VIEC'!I$5:I$100, B9)"),
        ("Đang làm", "=COUNTIF('DS CONG VIEC'!I$5:I$100, B10)"),
        ("Đang duyệt", "=COUNTIF('DS CONG VIEC'!I$5:I$100, B11)"),
        ("Hoàn thành", "=COUNTIF('DS CONG VIEC'!I$5:I$100, B12)"),
        ("Tạm hoãn", "=COUNTIF('DS CONG VIEC'!I$5:I$100, B13)")
    ]

    for idx, (st_name, f_cnt) in enumerate(statuses, start=9):
        ws_dash.cell(row=idx, column=2, value=st_name).font = font_regular
        ws_dash.cell(row=idx, column=2).alignment = align_left
        ws_dash.cell(row=idx, column=3, value=f_cnt).font = font_bold
        ws_dash.cell(row=idx, column=3).alignment = align_center
        
        ratio_cell = ws_dash.cell(row=idx, column=4, value=f"=IF($B$5>0, C{idx}/$B$5, 0)")
        ratio_cell.font = font_regular
        ratio_cell.alignment = align_center
        ratio_cell.number_format = '0.0%'
        
        for c in range(2, 5):
            ws_dash.cell(row=idx, column=c).border = thin_border

    # Section 2: PHÂN BỔ THEO MỨC ĐỘ ƯU TIÊN (F7:H12)
    ws_dash.merge_cells("F7:H7")
    ws_dash["F7"] = "2. PHÂN BỔ THEO ĐỘ ƯU TIÊN"
    ws_dash["F7"].font = font_section

    headers_pr = ["Mức độ", "Số lượng", "Tỷ lệ"]
    for i, h in enumerate(headers_pr, start=6):
        cell = ws_dash.cell(row=8, column=i, value=h)
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border

    priorities = [
        ("Khẩn cấp", "=COUNTIF('DS CONG VIEC'!L$5:L$100, F9)"),
        ("Cao", "=COUNTIF('DS CONG VIEC'!L$5:L$100, F10)"),
        ("Trung bình", "=COUNTIF('DS CONG VIEC'!L$5:L$100, F11)"),
        ("Thấp", "=COUNTIF('DS CONG VIEC'!L$5:L$100, F12)")
    ]

    for idx, (pr_name, f_cnt) in enumerate(priorities, start=9):
        ws_dash.cell(row=idx, column=6, value=pr_name).font = font_regular
        ws_dash.cell(row=idx, column=6).alignment = align_left
        ws_dash.cell(row=idx, column=7, value=f_cnt).font = font_bold
        ws_dash.cell(row=idx, column=7).alignment = align_center
        
        ratio_cell = ws_dash.cell(row=idx, column=8, value=f"=IF($B$5>0, G{idx}/$B$5, 0)")
        ratio_cell.font = font_regular
        ratio_cell.alignment = align_center
        ratio_cell.number_format = '0.0%'
        
        for c in range(6, 9):
            ws_dash.cell(row=idx, column=c).border = thin_border

    # Section 3: PHÂN BỔ THEO HẠNG MỤC / KÊNH (B15:D23)
    ws_dash.merge_cells("B15:D15")
    ws_dash["B15"] = "3. THEO HẠNG MỤC MARKETING"
    ws_dash["B15"].font = font_section

    headers_ch = ["Hạng mục / Kênh", "Số việc", "Hoàn thành"]
    for i, h in enumerate(headers_ch, start=2):
        cell = ws_dash.cell(row=16, column=i, value=h)
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border

    categories = [
        "Website & SEO",
        "Facebook Fanpage",
        "YouTube / Video",
        "TikTok & KOC",
        "Trade & POSM Đại lý",
        "Sàn TMĐT (Shopee/Lazada)",
        "Thiết kế & Media"
    ]
    for idx, cat in enumerate(categories, start=17):
        ws_dash.cell(row=idx, column=2, value=cat).font = font_regular
        ws_dash.cell(row=idx, column=2).alignment = align_left
        ws_dash.cell(row=idx, column=3, value=f"=COUNTIF('DS CONG VIEC'!D$5:D$100, B{idx})").font = font_bold
        ws_dash.cell(row=idx, column=3).alignment = align_center
        ws_dash.cell(row=idx, column=4, value=f"=COUNTIFS('DS CONG VIEC'!D$5:D$100, B{idx}, 'DS CONG VIEC'!I$5:I$100, \"Hoàn thành\")").font = font_regular
        ws_dash.cell(row=idx, column=4).alignment = align_center
        for c in range(2, 5):
            ws_dash.cell(row=idx, column=c).border = thin_border

    # Section 4: THEO DÕI THEO NHÂN SỰ PHỤ TRÁCH (F15:H22)
    ws_dash.merge_cells("F15:H15")
    ws_dash["F15"] = "4. TIẾN ĐỘ THEO NHÂN SỰ"
    ws_dash["F15"].font = font_section

    headers_team = ["Nhân sự", "Tổng task", "Đã xong"]
    for i, h in enumerate(headers_team, start=6):
        cell = ws_dash.cell(row=16, column=i, value=h)
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border

    team_members = [
        "Hoài Thương",
        "Kiều Thương",
        "Thụy Thương",
        "Thiện",
        "Tứ",
        "Thức",
        "Ngân",
        "Hùng",
        "Hùng Miền Bắc"
    ]
    for idx, member in enumerate(team_members, start=17):
        ws_dash.cell(row=idx, column=6, value=member).font = font_regular
        ws_dash.cell(row=idx, column=6).alignment = align_left
        ws_dash.cell(row=idx, column=7, value=f"=COUNTIF('DS CONG VIEC'!E$5:E$100, F{idx})").font = font_bold
        ws_dash.cell(row=idx, column=7).alignment = align_center
        ws_dash.cell(row=idx, column=8, value=f"=COUNTIFS('DS CONG VIEC'!E$5:E$100, F{idx}, 'DS CONG VIEC'!I$5:I$100, \"Hoàn thành\")").font = font_regular
        ws_dash.cell(row=idx, column=8).alignment = align_center
        for c in range(6, 9):
            ws_dash.cell(row=idx, column=c).border = thin_border

    # Column widths for Dashboard
    ws_dash.column_dimensions['A'].width = 3
    ws_dash.column_dimensions['B'].width = 24
    ws_dash.column_dimensions['C'].width = 12
    ws_dash.column_dimensions['D'].width = 14
    ws_dash.column_dimensions['E'].width = 16
    ws_dash.column_dimensions['F'].width = 22
    ws_dash.column_dimensions['G'].width = 14
    ws_dash.column_dimensions['H'].width = 14
    ws_dash.column_dimensions['I'].width = 14

    # =========================================================
    # TAB 2: DS CONG VIEC (TASK TRACKER)
    # =========================================================
    ws_tasks = wb.create_sheet(title="DS CONG VIEC")
    ws_tasks.views.sheetView[0].showGridLines = True
    ws_tasks.freeze_panes = "A5"

    # Header Title
    ws_tasks.merge_cells("A1:N2")
    ws_tasks["A1"] = "DANH SÁCH CHI TIẾT CÔNG VIỆC MARKETING - KING BLUE"
    ws_tasks["A1"].font = font_title
    ws_tasks["A1"].fill = fill_primary
    ws_tasks["A1"].alignment = align_center

    ws_tasks["A3"] = "💡 Hướng dẫn: Cập nhật Trạng thái và Tiến độ thường xuyên. Cột 'Tình trạng hạn' sẽ tự động cảnh báo theo Deadline."
    ws_tasks["A3"].font = font_small

    # Task Table Headers (Row 4)
    task_headers = [
        ("A4", "STT", 6),
        ("B4", "Mã Task", 13),
        ("C4", "Tên Công Việc", 35),
        ("D4", "Hạng Mục / Kênh", 20),
        ("E4", "Phụ Trách (Assignee)", 18),
        ("F4", "Người Phối Hợp", 18),
        ("G4", "Ngày Bắt Đầu", 14),
        ("H4", "Deadline", 14),
        ("I4", "Trạng Thái", 15),
        ("J4", "Tiến Độ (%)", 12),
        ("K4", "Tình Trạng Hạn", 15),
        ("L4", "Mức Độ Ưu Tiên", 15),
        ("M4", "Link Tài Liệu / Sản Phẩm", 30),
        ("N4", "Ghi Chú / Trở Ngại", 30)
    ]

    for cell_id, title, width in task_headers:
        cell = ws_tasks[cell_id]
        cell.value = title
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border
        col_letter = cell_id[0] if len(cell_id) == 2 else cell_id[:2]
        ws_tasks.column_dimensions[col_letter].width = width

    # Sample King Blue Tasks
    today = datetime.date.today()
    d_str = lambda days: (today + datetime.timedelta(days=days)).strftime("%Y-%m-%d")

    sample_tasks = [
        ("KB-MKT-01", "Quay video test tải máy khoan pin KM18QE", "YouTube / Video", "Tứ", "Kiều Thương", d_str(-3), d_str(2), "Đang làm", 0.6, "Cao", "https://drive.google.com/...", "Chuẩn bị mẫu bê tông và đá mài"),
        ("KB-MKT-02", "Chụp ảnh sản phẩm thùng đồ nghề KHD4233", "Thiết kế & Media", "Tứ", "Thiện", d_str(-5), d_str(-1), "Hoàn thành", 1.0, "Trung bình", "https://drive.google.com/...", "Đã retouched xong 8 góc ảnh"),
        ("KB-MKT-03", "Thiết kế banner & poster sự kiện triển lãm Vietbuild", "Trade & POSM Đại lý", "Thiện", "Thụy Thương", d_str(-2), d_str(4), "Đang làm", 0.4, "Khẩn cấp", "file:///Users/Admin/Documents/...", "Đang duyệt layout 3 phương án"),
        ("KB-MKT-04", "Viết bài chuẩn SEO giới thiệu công nghệ Brushless Motor", "Website & SEO", "Hoài Thương", "Admin", d_str(-4), d_str(-2), "Hoàn thành", 1.0, "Trung bình", "https://kingblue.vn/tin-tuc", "Đã index Google"),
        ("KB-MKT-05", "Lên kịch bản & liên hệ KOC test cờ lê lực King Blue", "TikTok & KOC", "Kiều Thương", "Tứ", d_str(-1), d_str(5), "Đang làm", 0.3, "Cao", "https://docs.google.com/...", "Đã gửi tin nhắn cho 3 KOC ngành cơ khí"),
        ("KB-MKT-06", "Cập nhật giá niêm yết và khuyến mãi đại lý lên kingtools.vn", "Sàn TMĐT (Shopee/Lazada)", "Thức", "Ngân", d_str(-1), d_str(1), "Đang duyệt", 0.9, "Cao", "https://kingtools.vn/...", "Chờ Giám đốc ký duyệt chính sách"),
        ("KB-MKT-07", "Thiết kế quầy kệ trưng bày POSM nhận diện cho Đại lý Cấp 1", "Trade & POSM Đại lý", "Thiện", "Thức", d_str(-7), d_str(7), "Đang làm", 0.5, "Khẩn cấp", "file:///Users/Admin/Documents/...", "Xưởng đang gửi báo giá đóng kệ"),
        ("KB-MKT-08", "Đăng bài Fanpage: Mẹo sử dụng đá cắt an toàn & tặng mã voucher", "Facebook Fanpage", "Hoài Thương", "Thiện", d_str(0), d_str(1), "Đang làm", 0.5, "Trung bình", "https://facebook.com/KingBlue-tools...", "Đã xong visual, chờ giờ vàng lên bài"),
        ("KB-MKT-09", "Trực chat sàn & tối ưu giỏ hàng TikTok Shop", "Sàn TMĐT (Shopee/Lazada)", "Ngân", "Thức", d_str(-6), d_str(-1), "Hoàn thành", 1.0, "Trung bình", "https://shopee.vn/...", "Tỷ lệ phản hồi chat đạt 98%"),
        ("KB-MKT-10", "Soạn nội dung cẩm nang sản phẩm & chính sách đại lý", "Trade & POSM Đại lý", "Thụy Thương", "Hoài Thương", d_str(-2), d_str(3), "Đang làm", 0.7, "Cao", "https://docs.google.com/...", "Đang rà soát danh mục máy pin"),
        ("KB-MKT-11", "Đóng gói 50 đơn hàng combo máy pin ra mắt (Kho Nam)", "Sàn TMĐT (Shopee/Lazada)", "Hùng", "Thức", d_str(0), d_str(1), "Đang làm", 0.4, "Cao", "file:///Users/Admin/Documents/...", "Đã dán tem bảo hành và đóng thùng"),
        ("KB-MKT-12", "Kiểm kê vật tư bao bì & đóng gói hàng kho Miền Bắc", "Sàn TMĐT (Shopee/Lazada)", "Hùng Miền Bắc", "Ngân", d_str(-1), d_str(2), "Đang làm", 0.5, "Trung bình", "file:///Users/Admin/Documents/...", "Bổ sung thùng carton cỡ M & màng co")
    ]

    for idx, task in enumerate(sample_tasks, start=5):
        stt = idx - 4
        code, name, cat, assignee, supporter, start_d, end_d, status, progress, priority, link, note = task
        
        ws_tasks.cell(row=idx, column=1, value=stt).alignment = align_center
        ws_tasks.cell(row=idx, column=2, value=code).alignment = align_center
        ws_tasks.cell(row=idx, column=3, value=name).alignment = align_left
        ws_tasks.cell(row=idx, column=4, value=cat).alignment = align_left
        ws_tasks.cell(row=idx, column=5, value=assignee).alignment = align_left
        ws_tasks.cell(row=idx, column=6, value=supporter).alignment = align_left
        ws_tasks.cell(row=idx, column=7, value=start_d).alignment = align_center
        ws_tasks.cell(row=idx, column=8, value=end_d).alignment = align_center
        
        # Status
        st_cell = ws_tasks.cell(row=idx, column=9, value=status)
        st_cell.alignment = align_center
        if status == "Hoàn thành":
            st_cell.fill = fill_done
        elif status == "Đang làm":
            st_cell.fill = fill_doing
        elif status == "Đang duyệt":
            st_cell.fill = fill_review

        # Progress
        prog_cell = ws_tasks.cell(row=idx, column=10, value=progress)
        prog_cell.alignment = align_center
        prog_cell.number_format = '0%'

        # Formula for Deadline Warning:
        f_deadline = f'=IF(I{idx}="Hoàn thành", "Đã xong", IF(ISBLANK(H{idx}), "", IF(H{idx}<TODAY(), "Quá hạn", IF(H{idx}-TODAY()<=2, "Sắp đến hạn", "Đúng hạn"))))'
        warn_cell = ws_tasks.cell(row=idx, column=11, value=f_deadline)
        warn_cell.alignment = align_center
        warn_cell.font = font_bold

        # Priority
        pr_cell = ws_tasks.cell(row=idx, column=12, value=priority)
        pr_cell.alignment = align_center
        if priority == "Khẩn cấp":
            pr_cell.font = Font(name="Calibri", size=11, bold=True, color="9B2C2C")

        # Link & Note
        ws_tasks.cell(row=idx, column=13, value=link).alignment = align_left
        ws_tasks.cell(row=idx, column=14, value=note).alignment = align_left

        for c in range(1, 15):
            cell_c = ws_tasks.cell(row=idx, column=c)
            cell_c.border = thin_border
            if c not in [11, 12]:
                cell_c.font = font_regular

    # =========================================================
    # TAB 3: DANH MUC CAU HINH (SETTINGS)
    # =========================================================
    ws_set = wb.create_sheet(title="CAU HINH")
    ws_set.views.sheetView[0].showGridLines = True

    ws_set["A1"] = "DANH MỤC CẤU HÌNH HỆ THỐNG"
    ws_set["A1"].font = font_section

    settings_cols = [
        ("A", "Trạng Thái", ["Chưa bắt đầu", "Đang làm", "Đang duyệt", "Hoàn thành", "Tạm hoãn"]),
        ("B", "Độ Ưu Tiên", ["Khẩn cấp", "Cao", "Trung bình", "Thấp"]),
        ("C", "Hạng Mục / Kênh", categories),
        ("D", "Nhân Sự", team_members)
    ]

    for col_letter, header, items in settings_cols:
        cell = ws_set[f"{col_letter}3"]
        cell.value = header
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border
        ws_set.column_dimensions[col_letter].width = 24
        
        for r_idx, item in enumerate(items, start=4):
            c = ws_set[f"{col_letter}{r_idx}"]
            c.value = item
            c.font = font_regular
            c.border = thin_border

    # Data Validations on DS CONG VIEC
    # Trạng thái (Col I)
    dv_status = DataValidation(type="list", formula1="='CAU HINH'!$A$4:$A$8", allow_blank=True)
    ws_tasks.add_data_validation(dv_status)
    dv_status.add("I5:I100")

    # Ưu tiên (Col L)
    dv_priority = DataValidation(type="list", formula1="='CAU HINH'!$B$4:$B$7", allow_blank=True)
    ws_tasks.add_data_validation(dv_priority)
    dv_priority.add("L5:L100")

    # Hạng mục (Col D)
    dv_cat = DataValidation(type="list", formula1="='CAU HINH'!$C$4:$C$10", allow_blank=True)
    ws_tasks.add_data_validation(dv_cat)
    dv_cat.add("D5:D100")

    # Nhân sự (Col E & F) - 9 members -> D4:D12
    dv_user = DataValidation(type="list", formula1="='CAU HINH'!$D$4:$D$12", allow_blank=True)
    ws_tasks.add_data_validation(dv_user)
    dv_user.add("E5:F100")

    wb.save("/Users/Admin/Documents/KIng BLue/Quan_Ly_Cong_Viec_KingBlue.xlsx")
    print("Created Quan_Ly_Cong_Viec_KingBlue.xlsx successfully!")


def create_work_report_sheet():
    wb = openpyxl.Workbook()
    
    c_primary = "1A365D"       # Royal Blue Dark (King Blue Header)
    c_accent = "2B6CB0"        # Medium Blue Accent
    c_light_bg = "EBF8FF"      # Light Blue background
    c_white = "FFFFFF"
    c_border = "CBD5E0"
    
    font_title = Font(name="Calibri", size=16, bold=True, color=c_white)
    font_section = Font(name="Calibri", size=12, bold=True, color=c_primary)
    font_header = Font(name="Calibri", size=11, bold=True, color=c_white)
    font_bold = Font(name="Calibri", size=11, bold=True)
    font_regular = Font(name="Calibri", size=11)
    font_small = Font(name="Calibri", size=9, italic=True, color="718096")

    fill_primary = PatternFill(start_color=c_primary, end_color=c_primary, fill_type="solid")
    fill_accent = PatternFill(start_color=c_accent, end_color=c_accent, fill_type="solid")
    fill_sub = PatternFill(start_color="EDF2F7", end_color="EDF2F7", fill_type="solid")
    fill_highlight = PatternFill(start_color="FEFCBF", end_color="FEFCBF", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color=c_border),
        right=Side(style='thin', color=c_border),
        top=Side(style='thin', color=c_border),
        bottom=Side(style='thin', color=c_border)
    )
    
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    # =========================================================
    # TAB 1: BAO CAO HANG NGAY (DAILY WORK REPORT)
    # =========================================================
    ws_daily = wb.active
    ws_daily.title = "BAO CAO HANG NGAY"
    ws_daily.views.sheetView[0].showGridLines = True
    ws_daily.freeze_panes = "A7"

    # Title
    ws_daily.merge_cells("A1:L2")
    ws_daily["A1"] = "NHẬT KÝ BÁO CÁO CÔNG VIỆC HÀNG NGÀY - PHÒNG MARKETING KING BLUE"
    ws_daily["A1"].font = font_title
    ws_daily["A1"].fill = fill_primary
    ws_daily["A1"].alignment = align_center

    ws_daily["A3"] = "💡 Quy định: Toàn bộ nhân sự hoàn thành và nộp báo cáo trước 17:30 mỗi ngày. Marketing Manager kiểm tra, phản hồi và duyệt trước 18:00."
    ws_daily["A3"].font = font_small

    today = datetime.date.today()
    font_kpi_num = Font(name="Calibri", size=18, bold=True, color=c_primary)
    font_kpi_label = Font(name="Calibri", size=9, bold=True, color="4A5568")
    fill_kpi = PatternFill(start_color=c_light_bg, end_color=c_light_bg, fill_type="solid")
    fill_done = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")
    fill_doing = PatternFill(start_color="BEE3F8", end_color="BEE3F8", fill_type="solid")

    # KPI Summary Row 4-5
    daily_kpis = [
        ("B4:C4", "B5:C5", "NGÀY BÁO CÁO", today.strftime("%d/%m/%Y")),
        ("D4:E4", "D5:E5", "NHÂN SỰ ĐÃ NỘP", "=COUNTA(C7:C30)"),
        ("F4:G4", "F5:G5", "HOÀN THÀNH 100%", "=COUNTIF(G7:G30, \"Hoàn thành 100%\")"),
        ("H4:I4", "H5:I5", "ĐANG XỬ LÝ (DANG LAM)", "=COUNTIF(G7:G30, \"Đang làm*\")"),
        ("J4:L4", "J5:L5", "TỶ LỆ HOÀN THÀNH", "=IF(D5>0, F5/D5, 0)")
    ]

    for lbl_range, val_range, lbl, val in daily_kpis:
        ws_daily.merge_cells(lbl_range)
        ws_daily.merge_cells(val_range)
        t_lbl = lbl_range.split(":")[0]
        t_val = val_range.split(":")[0]
        
        ws_daily[t_lbl] = lbl
        ws_daily[t_lbl].font = font_kpi_label
        ws_daily[t_lbl].alignment = align_center
        ws_daily[t_lbl].fill = fill_kpi
        
        ws_daily[t_val] = val
        ws_daily[t_val].font = font_kpi_num
        ws_daily[t_val].alignment = align_center
        ws_daily[t_val].fill = fill_kpi
        
        if "TỶ LỆ" in lbl:
            ws_daily[t_val].number_format = '0.0%'

    for col in range(2, 13):
        for r in range(4, 6):
            ws_daily.cell(row=r, column=col).border = thin_border

    # Headers for Daily Report Table (Row 6)
    daily_headers = [
        ("A6", "STT", 6),
        ("B6", "Ngày", 13),
        ("C6", "Họ và Tên Nhân Sự", 20),
        ("D6", "Chức Vụ / Vị Trí", 18),
        ("E6", "1️⃣ KẾT QUẢ ĐẠT ĐƯỢC (Nhiệm vụ 1, 2, 3...)", 42),
        ("F6", "2️⃣ KHÓ KHĂN / VƯỚNG MẮC", 28),
        ("G6", "3️⃣ BÀI HỌC / ĐỀ XUẤT", 30),
        ("H6", "4️⃣ KẾ HOẠCH NGÀY MAI", 30),
        ("I6", "Link Minh Chứng / Sản Phẩm", 24),
        ("J6", "Tình Trạng", 16),
        ("K6", "Marketing Manager Phản Hồi", 24),
        ("L6", "Giờ Nộp", 12)
    ]

    for cell_id, title, w in daily_headers:
        cell = ws_daily[cell_id]
        cell.value = title
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border
        col_letter = cell_id[0] if len(cell_id) == 2 else cell_id[:2]
        ws_daily.column_dimensions[col_letter].width = w

    today_str = today.strftime("%Y-%m-%d")
    daily_entries = [
        (1, today_str, "Võ Thị Hoài Thương", "Nhân viên MKT", "• Nhiệm vụ 1: Đề xuất hàng mẫu, liên hệ gặp KH\n• Nhiệm vụ 2: Tổng hợp thông tin chính sách, thông tin sản phẩm gửi KHM\n• Nhiệm vụ 3: Đi công tác: Đồng Nai, HCM", "Đại lý phân vân giữa kệ 2 tầng và 3 tầng do mặt bằng hẹp", "Đề xuất Design (Thiện) dựng thêm 1 phương án kệ module đứng tiết kiệm diện tích", "• Viết bài Fanpage máy mài mới\n• Theo dõi phản hồi của 3 KHM", "https://drive.google.com/...", "Hoàn thành 100%", "Đạt - Đã duyệt đề xuất kệ module", "17:15"),
        (2, today_str, "Kiều Thương", "Nhân viên MKT", "• Nhiệm vụ 1: Hoàn thiện kịch bản test máy khoan pin KM18QE\n• Nhiệm vụ 2: Gửi brief kịch bản cho KOC cờ lê lực", "KOC phản hồi chậm 1 ngày do bận lịch quay ngoại cảnh", "Nên gửi brief trước 3 ngày để KOC sắp xếp lịch quay", "• Chuẩn bị đạo cụ quay cùng Tứ tại xưởng\n• Chốt lịch test máy thứ 4", "https://docs.google.com/...", "Hoàn thành 100%", "Tốt - Nhắc KOC chốt lịch sớm", "17:20"),
        (3, today_str, "Thụy Thương", "Nhân viên MKT", "• Nhiệm vụ 1: Rà soát danh mục máy pin làm catalogue Vietbuild\n• Nhiệm vụ 2: Lập bảng giá chiết khấu cho đại lý cấp 1", "Chưa có thông số lực siết chuẩn cho dòng máy khoan rút lõi", "Cần bộ phận kỹ thuật cung cấp bảng thông số chính xác", "• Hoàn thiện mục thiết bị đo laser\n• Soạn thể lệ minigame đại lý", "https://docs.google.com/...", "Đang làm (70%)", "Đạt tiến độ - Sẽ gửi thông số", "17:22"),
        (4, today_str, "Thiện", "Nhân viên Design", "• Nhiệm vụ 1: Thiết kế visual bài viết FB đá cắt King Blue\n• Nhiệm vụ 2: Dựng phối cảnh 3D quầy kệ trưng bày đại lý", "Chờ kích thước mặt bằng chính xác của đại lý Đồng Nai", "Nên dựng sẵn thư viện 3D các model máy để render nhanh", "• Dựng phối cảnh quầy kệ module đứng\n• Thiết kế poster triển lãm Vietbuild", "file:///Users/Admin/Documents/...", "Đang làm (75%)", "Tốt - Phối cảnh đẹp mắt", "17:28"),
        (5, today_str, "Tứ", "Nhân viên Media", "• Nhiệm vụ 1: Chụp và retouch 8 ảnh thùng đồ nghề KHD4233\n• Nhiệm vụ 2: Chuẩn bị máy móc, pin sạc để quay test", "Thiếu phôi bê tông đá mác cao để test lực búa máy khoan", "Nên mượn xưởng đối tác để có đủ máy móc đo tải Ampe/Nm", "• 08h30: Bấm máy quay video test máy KM18QE\n• Buổi chiều: Dựng bản nháp Reels", "https://drive.google.com/...", "Hoàn thành 100%", "Xuất sắc - Ảnh rất nét", "17:10"),
        (6, today_str, "Thức", "Nhân viên Sàn TMĐT", "• Nhiệm vụ 1: Cập nhật giá khuyến mãi tháng 10 lên kingtools.vn\n• Nhiệm vụ 2: Rà soát tồn kho và setup deal Flash Sale Shopee", "Một số model máy rửa xe tạm thời hết hàng sẵn tại kho", "Nên đẩy mạnh combo máy pin kèm đầu bắn vít chống trượt", "• Theo dõi doanh số khung Flash Sale 12h\n• Phối hợp Ngân tối ưu SEO sàn", "https://kingtools.vn/...", "Hoàn thành 100%", "Đạt - Đã duyệt giá sàn", "17:25"),
        (7, today_str, "Ngân", "Nhân viên Sàn TMĐT", "• Nhiệm vụ 1: Trực chat tư vấn sàn Shopee (35 đơn thành công)\n• Nhiệm vụ 2: Chuẩn bị kịch bản livestream TikTok Shop 10/10", "Khách hỏi nhiều về tương thích chân pin Makita", "Nên làm bảng so sánh chân pin ghim vào bài viết sản phẩm", "• Hỗ trợ Thức setup deal Flash Sale\n• Lên kịch bản mini livestream", "https://shopee.vn/...", "Hoàn thành 100%", "Rất tốt - Chăm sóc chu đáo", "17:18"),
        (8, today_str, "Hùng", "Nhân viên Đóng gói", "• Nhiệm vụ 1: Đóng gói và dán tem 42 đơn hàng Shopee/Lazada\n• Nhiệm vụ 2: Bàn giao hàng hóa cho bưu cục SPX & GHTK", "Không có khó khăn", "Đề xuất cấp thêm 2 cuộn xốp bóng khí chuẩn bị Mega Sale", "• Đóng gói 20 kiện hàng gửi đại lý miền Tây\n• Kiểm kê thùng carton 30x20x15", "Phiếu xuất kho #KB1005", "Hoàn thành 100%", "Đạt chỉ tiêu đóng gói", "16:45"),
        (9, today_str, "Hùng Miền Bắc", "Nhân viên Đóng gói MB", "• Nhiệm vụ 1: Tiếp nhận và đóng gói 18 kiện đại lý Hà Nội\n• Nhiệm vụ 2: Kiểm kê kho bao bì và màng co tại chi nhánh", "Sắp hết màng quấn PE và băng keo King Blue", "Nên đặt in băng keo in logo King Blue số lượng lớn để tối ưu chi phí", "• Đóng đơn phát sinh sáng mai\n• Làm đề xuất cấp vật tư đóng gói", "Phiếu xuất kho #KBMB1005", "Hoàn thành 100%", "Đạt - Sẽ duyệt mua băng keo", "16:50")
    ]

    for idx, row_val in enumerate(daily_entries, start=7):
        for c_idx, val in enumerate(row_val, start=1):
            cell = ws_daily.cell(row=idx, column=c_idx, value=val)
            cell.border = thin_border
            cell.font = font_regular
            if c_idx in [1, 2, 12]:
                cell.alignment = align_center
            elif c_idx in [3, 4]:
                cell.alignment = align_left
                cell.font = font_bold if c_idx == 3 else font_regular
            elif c_idx in [5, 6, 7, 8]:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            elif c_idx == 10:
                cell.alignment = align_center
                if "100%" in str(val):
                    cell.fill = fill_done
                    cell.font = font_bold
                else:
                    cell.fill = fill_doing
                    cell.font = font_bold
            elif c_idx == 11:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                cell.font = Font(name="Calibri", size=11, bold=True, color="1A365D")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top")

    # =========================================================
    # TAB 2: BAO CAO TUAN (WEEKLY REPORT)
    # =========================================================
    ws_week = wb.create_sheet(title="BAO CAO TUAN")
    ws_week.views.sheetView[0].showGridLines = True

    # Title
    ws_week.merge_cells("A1:G2")
    ws_week["A1"] = "BÁO CÁO CÔNG VIỆC TUẦN - PHÒNG MARKETING KING BLUE"
    ws_week["A1"].font = font_title
    ws_week["A1"].fill = fill_primary
    ws_week["A1"].alignment = align_center

    # Info Block
    info_fields = [
        ("A4", "B4", "Người báo cáo:", "Nguyễn Văn A"),
        ("D4", "E4", "Bộ phận / Vị trí:", "Phòng Marketing & Media"),
        ("A5", "B5", "Tuần báo cáo:", "Tuần 41 (Tháng 10/2026)"),
        ("D5", "E5", "Thời gian:", "Từ 05/10/2026 đến 10/10/2026")
    ]
    for lbl_pos, val_pos, lbl, val in info_fields:
        ws_week[lbl_pos] = lbl
        ws_week[lbl_pos].font = font_bold
        ws_week[val_pos] = val
        ws_week[val_pos].font = font_regular
        ws_week[lbl_pos].alignment = align_left
        ws_week[val_pos].alignment = align_left

    # Section 1: KẾT QUẢ ĐÃ ĐẠT ĐƯỢC
    ws_week.cell(row=7, column=1, value="I. CÔNG VIỆC ĐÃ HOÀN THÀNH TRONG TUẦN").font = font_section
    headers_s1 = [("A8", "STT", 6), ("B8", "Công việc thực hiện", 35), ("C8", "Hạng mục / Kênh", 20), ("D8", "Kết quả đầu ra cụ thể", 35), ("E8", "Tình trạng", 15), ("F8", "Link tài liệu / sản phẩm", 28), ("G8", "Đánh giá", 14)]
    for cell_id, title, w in headers_s1:
        cell = ws_week[cell_id]
        cell.value = title
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border
        col_letter = cell_id[0] if len(cell_id) == 2 else cell_id[:2]
        ws_week.column_dimensions[col_letter].width = w

    rows_s1 = [
        (1, "Chụp và chỉnh sửa ảnh bộ thùng đựng đồ nghề KHD4233", "Thiết kế & Media", "Hoàn thành 8 ảnh chuẩn sàn TMĐT & Banner", "100%", "https://drive.google.com/...", "Đạt chất lượng"),
        (2, "Viết bài chuẩn SEO giới thiệu công nghệ Brushless Motor", "Website & SEO", "Đã xuất bản bài viết lên website kingblue.vn", "100%", "https://kingblue.vn/tin-tuc", "Tốt"),
        (3, "Tối ưu hóa giao diện gian hàng Shopee Mall King Tools", "Sàn TMĐT", "Cập nhật banner khuyến mại tháng 10 và khung avatar", "100%", "https://shopee.vn/...", "Đạt tiến độ"),
        (4, "Lên kịch bản video test máy khoan pin KM18QE", "YouTube / Video", "Kịch bản chi tiết 3 phần (Mở hộp, Test bê tông, Đánh giá)", "100%", "https://docs.google.com/...", "Đã duyệt kịch bản")
    ]
    for r_idx, row_data in enumerate(rows_s1, start=9):
        for c_idx, val in enumerate(row_data, start=1):
            c = ws_week.cell(row=r_idx, column=c_idx, value=val)
            c.font = font_regular
            c.border = thin_border
            c.alignment = align_center if c_idx in [1, 5, 7] else align_left

    # Section 2: CÁC VẤN ĐỀ TỒN ĐỌNG & TRỞ NGẠI
    start_r2 = 14
    ws_week.cell(row=start_r2, column=1, value="II. CÔNG VIỆC ĐANG XỬ LÝ & TRỞ NGẠI (PENDING / BLOCKERS)").font = font_section
    headers_s2 = [("A15", "STT"), ("B15", "Công việc đang tồn đọng"), ("C15", "Tiến độ hiện tại"), ("D15", "Nguyên nhân / Trở ngại"), ("E15", "Giải pháp khắc phục"), ("F15", "Người cần hỗ trợ"), ("G15", "Hạn hoàn thành mới")]
    for cell_id, title in headers_s2:
        cell = ws_week[cell_id]
        cell.value = title
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border

    rows_s2 = [
        (1, "Thi công kệ trưng bày POSM cho 5 đại lý miền Trung", "50%", "Xưởng mộc giao chậm khung sắt mẫu", "Đốc thúc xưởng giao gấp trước thứ 5", "Sales Miền Trung", "12/10/2026"),
        (2, "Video review cờ lê lực King Blue cùng KOC", "30%", "KOC bận lịch quay ngoại cảnh", "Đổi lịch quay sang ngày thứ 6 tại xưởng", "Marketing Manager", "15/10/2026")
    ]
    for r_idx, row_data in enumerate(rows_s2, start=16):
        for c_idx, val in enumerate(row_data, start=1):
            c = ws_week.cell(row=r_idx, column=c_idx, value=val)
            c.font = font_regular
            c.border = thin_border
            c.alignment = align_center if c_idx in [1, 3, 7] else align_left

    # Section 3: KẾ HOẠCH TUẦN TỚI
    start_r3 = 19
    ws_week.cell(row=start_r3, column=1, value="III. KẾ HOẠCH & MỤC TIÊU TUẦN TIẾP THEO").font = font_section
    headers_s3 = [("A20", "STT"), ("B20", "Nhiệm vụ trọng tâm"), ("C20", "Mục tiêu cần đạt"), ("D20", "Hạng mục / Kênh"), ("E20", "Người phối hợp"), ("F20", "Deadline dự kiến"), ("G20", "Mức ưu tiên")]
    for cell_id, title in headers_s3:
        cell = ws_week[cell_id]
        cell.value = title
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border

    rows_s3 = [
        (1, "Bấm máy quay video test thực tế máy khoan bê tông KM18QF", "Hoàn thành thô video + dựng bản nháp", "YouTube & TikTok", "Media / Photographer", "12/10/2026", "Cao"),
        (2, "Chốt thiết kế 3D gian hàng triển lãm Vietbuild sắp tới", "Ban Giám Đốc ký duyệt layout chính thức", "Trade & POSM", "Designer, Admin", "14/10/2026", "Khẩn cấp"),
        (3, "Tổ chức mini-game trên Fanpage King Blue Tools", "Tăng 500 followers và 200 lượt chia sẻ", "Facebook Fanpage", "Content MKT", "16/10/2026", "Trung bình")
    ]
    for r_idx, row_data in enumerate(rows_s3, start=21):
        for c_idx, val in enumerate(row_data, start=1):
            c = ws_week.cell(row=r_idx, column=c_idx, value=val)
            c.font = font_regular
            c.border = thin_border
            c.alignment = align_center if c_idx in [1, 6, 7] else align_left

    # Section 4: ĐỀ XUẤT KIẾN NGHỊ
    start_r4 = 25
    ws_week.cell(row=start_r4, column=1, value="IV. ĐỀ XUẤT & KIẾN NGHỊ VỚI QUẢN LÝ / BAN GIÁM ĐỐC").font = font_section
    ws_week.merge_cells("A26:G28")
    ws_week["A26"] = "1. Đề xuất cấp ngân sách chạy ads Facebook & TikTok 5.000.000 VNĐ cho chiến dịch ra mắt dòng máy pin thế hệ mới.\n2. Cần bộ phận Kỹ thuật hỗ trợ 01 bạn đồng hành trong buổi quay video test máy vào thứ 6 tuần tới để giải thích thông số lực siết (Nm)."
    ws_week["A26"].font = font_regular
    ws_week["A26"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    for r in range(26, 29):
        for c in range(1, 8):
            ws_week.cell(row=r, column=c).border = thin_border

    # =========================================================
    # TAB 2: CHI SO MARKETING (METRICS)
    # =========================================================
    ws_met = wb.create_sheet(title="CHI SO MARKETING")
    ws_met.views.sheetView[0].showGridLines = True

    ws_met.merge_cells("A1:H2")
    ws_met["A1"] = "BẢNG THEO DÕI CHỈ SỐ MARKETING & TĂNG TRƯỞNG KÊNH (KING BLUE)"
    ws_met["A1"].font = font_title
    ws_met["A1"].fill = fill_primary
    ws_met["A1"].alignment = align_center

    met_headers = [
        ("A4", "Kênh Truyền Thông", 22),
        ("B4", "Chỉ Số Đo Lường (KPI Metric)", 30),
        ("C4", "Đơn Vị Tính", 12),
        ("D4", "Mục Tiêu Tháng", 15),
        ("E4", "Thực Tế Đạt", 15),
        ("F4", "Tỷ Lệ Đạt (%)", 14),
        ("G4", "So Với Tháng Trước", 18),
        ("H4", "Đánh Giá / Ghi Chú", 26)
    ]
    for cell_id, title, w in met_headers:
        cell = ws_met[cell_id]
        cell.value = title
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border
        col_letter = cell_id[0] if len(cell_id) == 2 else cell_id[:2]
        ws_met.column_dimensions[col_letter].width = w

    metrics_data = [
        ("Facebook Fanpage", "Số lượng bài đăng mới", "Bài", 16, 18, "+12.5%", "Đạt và vượt chỉ tiêu bài viết"),
        ("Facebook Fanpage", "Lượt tiếp cận (Reach)", "Người", 50000, 58400, "+16.8%", "Tăng mạnh nhờ video mẹo cơ khí"),
        ("Facebook Fanpage", "Số tin nhắn hỏi làm Đại lý", "Inquiry", 25, 29, "+20.0%", "Đã chuyển giao cho bộ phận Sales"),
        ("YouTube Channel", "Số video mới xuất bản", "Video", 4, 3, "-25.0%", "Thiếu 1 video do dời lịch test máy"),
        ("YouTube Channel", "Lượt xem video (Views)", "Lượt xem", 15000, 18200, "+21.3%", "Video thước laser KNZ-80R viral"),
        ("TikTok & KOC", "Số lượt nhắc tên (#kingblue)", "Lượt xem", 100000, 142000, "+42.0%", "Hiệu ứng tích cực từ các KOC review"),
        ("Website (kingblue.vn)", "Tổng lượt truy cập (Sessions)", "Truy cập", 12000, 13500, "+12.5%", "Lượng tìm kiếm đá cắt & máy pin tăng"),
        ("Website (kingblue.vn)", "Số lượt tải Catalogue sản phẩm", "Lượt tải", 150, 185, "+23.3%", "Các đại lý tải để in ấn cho thợ"),
        ("Sàn TMĐT & Online", "Doanh số bán lẻ qua sàn ủy quyền", "Triệu VNĐ", 120, 135, "+12.5%", "Doanh số nhóm phụ kiện tăng trưởng tốt"),
        ("Trade & POSM", "Số điểm bán lắp đặt mới kệ King Blue", "Đại lý", 10, 12, "+20.0%", "Mở rộng đại lý tại Đồng Nai & Bình Dương")
    ]

    for idx, (ch, metric, unit, target, actual, comp, note) in enumerate(metrics_data, start=5):
        ws_met.cell(row=idx, column=1, value=ch).alignment = align_left
        ws_met.cell(row=idx, column=2, value=metric).alignment = align_left
        ws_met.cell(row=idx, column=3, value=unit).alignment = align_center
        ws_met.cell(row=idx, column=4, value=target).alignment = align_right
        ws_met.cell(row=idx, column=5, value=actual).alignment = align_right
        
        # Formula for % Achievement: =E/D
        pct_cell = ws_met.cell(row=idx, column=6, value=f"=IF(D{idx}>0, E{idx}/D{idx}, 0)")
        pct_cell.alignment = align_center
        pct_cell.number_format = '0.0%'
        pct_cell.font = font_bold
        
        ws_met.cell(row=idx, column=7, value=comp).alignment = align_center
        ws_met.cell(row=idx, column=8, value=note).alignment = align_left
        
        for c in range(1, 9):
            ws_met.cell(row=idx, column=c).border = thin_border
            if c != 6:
                ws_met.cell(row=idx, column=c).font = font_regular

    # =========================================================
    # TAB 3: DANH GIA THANG (MONTHLY OVERVIEW)
    # =========================================================
    ws_mon = wb.create_sheet(title="DANH GIA THANG")
    ws_mon.views.sheetView[0].showGridLines = True

    ws_mon.merge_cells("A1:G2")
    ws_mon["A1"] = "BẢNG ĐÁNH GIÁ HIỆU QUẢ CÔNG VIỆC THÁNG (MONTHLY REVIEW)"
    ws_mon["A1"].font = font_title
    ws_mon["A1"].fill = fill_primary
    ws_mon["A1"].alignment = align_center

    mon_headers = [
        ("A4", "STT", 6),
        ("B4", "Hạng Mục Đánh Giá", 30),
        ("C4", "Mục Tiêu Tháng", 30),
        ("D4", "Kết Quả Thực Hiện", 30),
        ("E4", "Tỷ Lệ Đạt", 14),
        ("F4", "Tự Đánh Giá", 15),
        ("G4", "Quản Lý Đánh Giá", 18)
    ]
    for cell_id, title, w in mon_headers:
        cell = ws_mon[cell_id]
        cell.value = title
        cell.font = font_header
        cell.fill = fill_accent
        cell.alignment = align_center
        cell.border = thin_border
        col_letter = cell_id[0] if len(cell_id) == 2 else cell_id[:2]
        ws_mon.column_dimensions[col_letter].width = w

    eval_data = [
        (1, "1. Sản xuất nội dung & Social Media", "16 bài Facebook, 4 video YouTube, 8 video TikTok", "Đạt 18 bài FB, 3 video YT, 10 video TikTok", 0.95, "Tốt", "Đạt - Cần tăng chất lượng YT"),
        (2, "2. Thiết kế & Bộ nhận diện POSM", "Hoàn thiện bộ nhận diện Vietbuild + kệ đại lý", "Đã xong 100% bản vẽ 3D và giao xưởng mộc", 1.00, "Xuất sắc", "Xuất sắc"),
        (3, "3. Hình ảnh & Video sản phẩm (Media)", "Chụp 12 bộ sản phẩm máy pin & phụ kiện", "Đã bàn giao đủ 12 bộ ảnh chuẩn nét", 1.00, "Tốt", "Tốt"),
        (4, "4. Hỗ trợ Sales & Kênh Đại lý", "Thu thập 20 leads đại lý mới từ Online", "Mang về 29 leads đại lý hợp lệ", 1.45, "Xuất sắc", "Vượt chỉ tiêu"),
        (5, "5. Kỷ luật & Tinh thần phối hợp", "Báo cáo đầy đủ, đúng deadline trên 90%", "Tỷ lệ đúng hạn đạt 92%", 0.92, "Tốt", "Tốt")
    ]
    for idx, (stt, item, target, actual, pct, self_ev, mgr_ev) in enumerate(eval_data, start=5):
        ws_mon.cell(row=idx, column=1, value=stt).alignment = align_center
        ws_mon.cell(row=idx, column=2, value=item).alignment = align_left
        ws_mon.cell(row=idx, column=3, value=target).alignment = align_left
        ws_mon.cell(row=idx, column=4, value=actual).alignment = align_left
        
        pct_c = ws_mon.cell(row=idx, column=5, value=pct)
        pct_c.alignment = align_center
        pct_c.number_format = '0%'
        pct_c.font = font_bold
        
        ws_mon.cell(row=idx, column=6, value=self_ev).alignment = align_center
        ws_mon.cell(row=idx, column=7, value=mgr_ev).alignment = align_center
        
        for c in range(1, 8):
            ws_mon.cell(row=idx, column=c).border = thin_border
            if c != 5:
                ws_mon.cell(row=idx, column=c).font = font_regular

    wb.save("/Users/Admin/Documents/KIng BLue/Bao_Cao_Cong_Viec_KingBlue.xlsx")
    print("Created Bao_Cao_Cong_Viec_KingBlue.xlsx successfully!")

if __name__ == "__main__":
    create_task_management_sheet()
    create_work_report_sheet()

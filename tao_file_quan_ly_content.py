# -*- coding: utf-8 -*-
"""
TẠO HỆ THỐNG QUẢN LÝ CONTENT - KING BLUE MARKETING
===================================================
Tạo file Excel offline: Quan_Ly_Content_KingBlue.xlsx
Và đồng bộ trực tiếp lên Google Drive tạo Google Sheet:
"Quản Lý Content - King Blue Marketing"
"""

import os
import sys
import json
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_FILE = os.path.join(BASE_DIR, "Quan_Ly_Content_KingBlue.xlsx")
TOKEN_FILE = os.path.join(BASE_DIR, "API", "token.json")
LINKS_FILE = os.path.join(BASE_DIR, "google_sheets_links.json")

# Màu nhận diện thương hiệu King Blue
C_NAVY_DARK = "0F172A"   # Slate 900
C_NAVY_HEAD = "1A365D"   # Royal Navy
C_BLUE_SUB  = "1E3A8A"   # Blue 900
C_BLUE_ACC  = "2563EB"   # Royal Blue
C_AMBER_ACC = "D97706"   # Gold Amber
C_AMBER_BG  = "FEF3C7"   # Amber 100
C_ZEBRA     = "F8FAFC"   # Slate 50
C_BORDER    = "CBD5E1"   # Slate 300
C_CARD_BG   = "F1F5F9"   # Slate 100

def create_excel_content():
    wb = openpyxl.Workbook()
    # Xoá sheet mặc định
    wb.remove(wb.active)

    font_title = Font(name="Arial", size=13, bold=True, color="FFFFFF")
    font_head = Font(name="Arial", size=9, bold=True, color="FFFFFF")
    font_body = Font(name="Arial", size=9, color="0F172A")
    font_bold = Font(name="Arial", size=9, bold=True, color="0F172A")
    font_stat_val = Font(name="Arial", size=12, bold=True, color="1E3A8A")
    font_stat_lbl = Font(name="Arial", size=8, bold=True, color="64748B")

    fill_title = PatternFill("solid", fgColor=C_NAVY_HEAD)
    fill_head = PatternFill("solid", fgColor=C_BLUE_SUB)
    fill_head_sec = PatternFill("solid", fgColor=C_NAVY_DARK)
    fill_zebra = PatternFill("solid", fgColor=C_ZEBRA)
    fill_card = PatternFill("solid", fgColor=C_CARD_BG)
    fill_amber_card = PatternFill("solid", fgColor=C_AMBER_BG)

    thin_border_side = Side(style="thin", color=C_BORDER)
    border_cell = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    border_card = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")
    align_wrap_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # -------------------------------------------------------------
    # TAB 1: TONG HOP CONTENT (Master Content Calendar)
    # -------------------------------------------------------------
    ws1 = wb.create_sheet("TONG HOP CONTENT")
    ws1.views.sheetView[0].showGridLines = True

    # Title Banner (Row 1)
    ws1.merge_cells("A1:Q1")
    t1 = ws1.cell(row=1, column=1, value="🏢 KẾ HOẠCH & LỊCH BIÊN TẬP NỘI DUNG ĐA KÊNH - KING BLUE MARKETING")
    t1.font = font_title
    t1.fill = fill_title
    t1.alignment = align_center
    ws1.row_dimensions[1].height = 36

    # Thẻ thống kê KPI (Row 2 & 3)
    stat_cards = [
        ("A", "C", "TỔNG NỘI DUNG THÁNG", "=COUNTA(B6:B100)", fill_card),
        ("D", "F", "ĐÃ HOÀN THÀNH / ĐÃ ĐĂNG", '=COUNTIF(L6:L100, "Đã đăng")', fill_card),
        ("G", "I", "ĐANG SẢN XUẤT / CHỜ DUYỆT", '=COUNTIF(L6:L100, "Đang làm") + COUNTIF(L6:L100, "Đang duyệt")', fill_card),
        ("J", "L", "TỔNG LƯỢT XEM (VIEWS)", "=SUM(O6:O100)", fill_amber_card),
        ("M", "O", "TỔNG TƯƠNG TÁC (ENGAGEMENT)", "=SUM(P6:P100)", fill_amber_card),
        ("P", "Q", "TIẾN ĐỘ HOÀN THÀNH", '=IF(COUNTA(B6:B100)>0, COUNTIF(L6:L100, "Đã đăng")/COUNTA(B6:B100), 0)', fill_card),
    ]

    for start_col, end_col, label, formula, bg in stat_cards:
        ws1.merge_cells(f"{start_col}2:{end_col}2")
        ws1.merge_cells(f"{start_col}3:{end_col}3")
        c_lbl = ws1[f"{start_col}2"]
        c_lbl.value = label
        c_lbl.font = font_stat_lbl
        c_lbl.alignment = align_center
        c_lbl.fill = bg
        
        c_val = ws1[f"{start_col}3"]
        c_val.value = formula
        c_val.font = font_stat_val
        c_val.alignment = align_center
        c_val.fill = bg
        if "%" in label or "TIẾN ĐỘ" in label:
            c_val.number_format = "0.0%"
        elif "VIEWS" in label or "TƯƠNG TÁC" in label:
            c_val.number_format = "#,##0"

    ws1.row_dimensions[2].height = 18
    ws1.row_dimensions[3].height = 24

    # Header Row 5
    headers_master = [
        "STT", "Mã Content", "Tiêu đề / Chủ đề nội dung", "Kênh đăng",
        "Định dạng", "Trụ cột nội dung", "Dòng sản phẩm", "Người phụ trách",
        "Người phối hợp", "Ngày đăng", "Khung giờ", "Trạng thái",
        "Link tài liệu / Drive", "Link bài live", "Lượt Views / Reach",
        "Lượt Tương tác", "Ghi chú & Đánh giá"
    ]
    ws1.row_dimensions[5].height = 28
    for col_idx, h in enumerate(headers_master, start=1):
        c = ws1.cell(row=5, column=col_idx, value=h)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    # Dữ liệu mẫu thực tế của King Blue
    sample_master = [
        [1, "KB-CNT-01", "Video Test tải máy khoan pin Brushless KM18QE khoan bê tông 5 lỗ", "TikTok", "Video ngắn (Reels/TikTok)", "Mẹo thợ & Trải nghiệm", "Máy pin Brushless", "Kiều Thương", "Tứ", "05/10/2026", "11:30", "Đã đăng", "https://drive.google.com/...", "https://tiktok.com/@kingblue/...", 4200, 156, "Tương tác tốt, nhiều thợ hỏi giá pin 18V"],
        [2, "KB-CNT-02", "Album 5 góc chụp sắc nét thùng đồ nghề chống va đập KHD4233", "Facebook Fanpage", "Album ảnh", "Giới thiệu sản phẩm", "Dụng cụ cầm tay", "Võ Thị Hoài Thương", "Thiện", "06/10/2026", "19:30", "Đã đăng", "https://drive.google.com/...", "https://facebook.com/kingblue/...", 2850, 94, "Thiện thiết kế banner layout bắt mắt"],
        [3, "KB-CNT-03", "Kịch bản test súng siết bu lông KBA-I1500 mở ốc xe tải 5 tấn", "YouTube Video", "Video dài (Youtube)", "Mẹo thợ & Trải nghiệm", "Máy pin Brushless", "Kiều Thương", "Tứ", "08/10/2026", "20:00", "Đang làm", "https://docs.google.com/...", "", 0, 0, "Tứ đang hẹn gara xe tải để quay thực tế"],
        [4, "KB-CNT-04", "Bài chuẩn SEO: Hướng dẫn chọn đá cắt sắt an toàn và tiết kiệm 30% hao mòn", "Website SEO", "Bài viết chuẩn SEO", "Giáo dục kỹ thuật", "Đá cắt & Đá mài", "Võ Thị Hoài Thương", "Thiện", "09/10/2026", "09:00", "Đang duyệt", "https://docs.google.com/...", "", 0, 0, "Từ khóa chính: đá cắt sắt King Blue"],
        [5, "KB-CNT-05", "Mini Game dự đoán thông số lực siết máy KM18 - Tặng 3 áo thun & mũ King Blue", "Facebook Fanpage", "Single Post / Ảnh đơn", "Minigame & Tương tác", "Máy pin Brushless", "Thương Thương", "Thiện", "10/10/2026", "11:30", "Sẵn sàng đăng", "https://drive.google.com/...", "", 0, 0, "Thiện đã xong visual quà tặng"],
        [6, "KB-CNT-06", "TikTok Shorts: Mẹo căn cốt tường phẳng tuyệt đối với máy cân bằng Laser 12 tia xanh", "TikTok", "Video ngắn (Reels/TikTok)", "Mẹo thợ & Trải nghiệm", "Thiết bị đo Laser", "Kiều Thương", "Tứ", "11/10/2026", "18:30", "Lên ý tưởng", "https://docs.google.com/...", "", 0, 0, "Quay cận cảnh tia laser ngoài trời nắng"],
        [7, "KB-CNT-07", "Thông báo chính sách ưu đãi chiết khấu & quầy kệ POSM dành cho Đại lý mới", "Facebook Fanpage", "Infographic / POSM", "Đại lý & Phân phối", "Chính sách B2B", "Thương Thương", "Thiện", "12/10/2026", "09:30", "Đang làm", "https://drive.google.com/...", "", 0, 0, "Hỗ trợ đội ngũ Sales đại lý toàn quốc"],
        [8, "KB-CNT-08", "Reviewer Cơ Khí Booking: Đồ Nghề Tự Chọn unboxing combo máy mài & máy khoan King Blue", "KOC & Reviewer", "Video dài (Youtube)", "KOC & Reviewer", "Máy pin Brushless", "Kiều Thương", "Tứ", "15/10/2026", "19:00", "Đang làm", "https://docs.google.com/...", "", 0, 0, "Đã gửi máy mẫu, chờ KOC duyệt lịch quay"],
    ]

    for row_idx, r_data in enumerate(sample_master, start=6):
        ws1.row_dimensions[row_idx].height = 22
        for col_idx, val in enumerate(r_data, start=1):
            c = ws1.cell(row=row_idx, column=col_idx, value=val)
            c.font = font_body
            c.border = border_cell
            if col_idx in [1, 10, 11, 12]:
                c.alignment = align_center
            elif col_idx in [4, 5, 6, 7, 8, 9]:
                c.alignment = align_center
            elif col_idx in [15, 16]:
                c.alignment = align_right
                c.number_format = "#,##0"
            else:
                c.alignment = align_left
            if row_idx % 2 == 1:
                c.fill = fill_zebra

    # Kẻ thêm dòng trống chuẩn bị sẵn
    for row_idx in range(len(sample_master) + 6, 40):
        ws1.row_dimensions[row_idx].height = 20
        for col_idx in range(1, 18):
            c = ws1.cell(row=row_idx, column=col_idx)
            c.border = border_cell
            if row_idx % 2 == 1:
                c.fill = fill_zebra

    # Độ rộng cột Tab 1
    col_widths_1 = {
        "A": 6, "B": 14, "C": 42, "D": 18, "E": 22, "F": 22, "G": 20,
        "H": 20, "I": 16, "J": 14, "K": 12, "L": 16, "M": 24, "N": 24,
        "O": 18, "P": 18, "Q": 32
    }
    for col_letter, w in col_widths_1.items():
        ws1.column_dimensions[col_letter].width = w

    ws1.freeze_panes = "C6"

    # -------------------------------------------------------------
    # TAB 2: FACEBOOK FANPAGE
    # -------------------------------------------------------------
    ws2 = wb.create_sheet("FACEBOOK FANPAGE")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("A1:N1")
    t2 = ws2.cell(row=1, column=1, value="📘 KẾ HOẠCH NỘI DUNG CHI TIẾT - FACEBOOK FANPAGE KING BLUE TOOLS")
    t2.font = font_title
    t2.fill = fill_title
    t2.alignment = align_center
    ws2.row_dimensions[1].height = 36

    headers_fb = [
        "STT", "Mã Post", "Ngày đăng", "Khung giờ", "Chủ đề / Hook chính",
        "Trụ cột nội dung", "Dàn ý Caption / Thông điệp chính", "Brief Visual (Ảnh/Video)",
        "Hashtags", "CTA (Kêu gọi)", "Phụ trách viết", "Trạng thái", "Link bài live", "Ghi chú"
    ]
    ws2.row_dimensions[3].height = 26
    for col_idx, h in enumerate(headers_fb, start=1):
        c = ws2.cell(row=3, column=col_idx, value=h)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    sample_fb = [
        [1, "FB-01", "06/10/2026", "19:30", "Thùng Đồ Nghề KHD4233: Đập không bể, rơi không móp!", "Giới thiệu sản phẩm", "1. Nỗi đau đồ nghề bừa bãi thất lạc\n2. Đặc điểm chịu lực nhựa dẻo cao cấp\n3. Khay chia thông minh", "Album 5 ảnh thực tế chụp tại xưởng, kèm kích thước", "#KingBlue #ThungDoNghe #KHD4233", "Inbox để nhận giá ưu đãi đại lý", "Võ Thị Hoài Thương", "Đã đăng", "https://facebook.com/...", "Do Thiện thiết kế visual"],
        [2, "FB-02", "08/10/2026", "11:30", "Cảnh báo 3 sai lầm khiến máy khoan pin nhanh chai pin, hỏng motor", "Giáo dục kỹ thuật", "1. Dùng sạc kém chất lượng\n2. Để máy trong môi trường ẩm ướt\n3. Ép tải quá mức quy định", "Infographic 3 bước đồ họa trực quan tông xanh", "#KingBlue #MeoTho #MayKhoanPin", "Chia sẻ ngay cho anh em thợ cùng xem!", "Thương Thương", "Sẵn sàng đăng", "", "Chờ giờ vàng đăng bài"],
        [3, "FB-03", "10/10/2026", "19:00", "Đoán lực siết rinh quà khủng - Mini Game King Blue", "Minigame & Tương tác", "Luật chơi dự đoán lực Nm của máy bu lông KBA-I1500, comment số may mắn 2 số", "Banner poster quà tặng áo thun + nón bảo hộ", "#MiniGame #KingBlueTools", "Comment ngay để nhận quà!", "Kiều Thương", "Đang viết bài", "", "Thiện đang làm poster"]
    ]

    for row_idx, r_data in enumerate(sample_fb, start=4):
        ws2.row_dimensions[row_idx].height = 28
        for col_idx, val in enumerate(r_data, start=1):
            c = ws2.cell(row=row_idx, column=col_idx, value=val)
            c.font = font_body
            c.border = border_cell
            c.alignment = align_center if col_idx in [1, 3, 4, 11, 12] else (align_wrap_left if col_idx in [5, 7, 8] else align_left)
            if row_idx % 2 == 1:
                c.fill = fill_zebra

    col_widths_2 = {
        "A": 6, "B": 12, "C": 14, "D": 12, "E": 30, "F": 20, "G": 40,
        "H": 34, "I": 24, "J": 26, "K": 20, "L": 16, "M": 24, "N": 26
    }
    for col_letter, w in col_widths_2.items():
        ws2.column_dimensions[col_letter].width = w
    ws2.freeze_panes = "C4"

    # -------------------------------------------------------------
    # TAB 3: TIKTOK & SHORTS
    # -------------------------------------------------------------
    ws3 = wb.create_sheet("TIKTOK & SHORTS")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("A1:O1")
    t3 = ws3.cell(row=1, column=1, value="🎵 KẾ HOẠCH SẢN XUẤT VIDEO NGẮN - TIKTOK & YOUTUBE SHORTS KING BLUE")
    t3.font = font_title
    t3.fill = fill_title
    t3.alignment = align_center
    ws3.row_dimensions[1].height = 36

    headers_tt = [
        "STT", "Mã Video", "Ngày đăng", "Tiêu đề video / Hook 3s đầu", "Sản phẩm test",
        "Nội dung phân cảnh (Script)", "Âm thanh / Nhạc nền", "Người quay (Media)", "Người lên hình / Voice",
        "Trạng thái quay dựng", "TikTok Shop / Giỏ hàng", "Hashtags", "Lượt Views", "Tương tác", "Ghi chú viral"
    ]
    ws3.row_dimensions[3].height = 26
    for col_idx, h in enumerate(headers_tt, start=1):
        c = ws3.cell(row=3, column=col_idx, value=h)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    sample_tt = [
        [1, "TT-01", "05/10/2026", "Khoan thủng bê tông 10cm trong 5 giây? Thử ngay KM18QE!", "Máy khoan KM18QE", "Hook: Cầm máy khoan thẳng vào khối bê tông mác 300. Body: Quay cận cảnh tốc độ khoan và không bị giật tay. CTA: Gắn giỏ hàng", "Nhạc dồn dập, sound effect đục phá", "Tứ (Media)", "Kiều Thương", "Đã đăng", "Gắn mã sản phẩm KM18QE", "#kingblue #maykhoanpin #meotho", 4200, 156, "Khán giả quan tâm giá thân máy"],
        [2, "TT-02", "07/10/2026", "Thợ cơ khí bất ngờ khi test độ phẳng của thước cuộn tự hãm 7.5m", "Thước cuộn tự hãm", "Hook: Kéo dài thước 3m không gãy gập. Body: Thả rơi tự do từ độ cao 2m xem độ chịu va đập. Kết: Rất chắc chắn.", "Voiceover dí dỏm, chân thực", "Tứ (Media)", "Kiều Thương", "Đang dựng", "Gắn mã Thước cuộn 7.5m", "#kingblue #thuoccuon #reviewdochoi", 0, 0, "Dựng video nhịp nhanh dưới 35s"],
        [3, "TT-03", "09/10/2026", "Máy siết bu lông 1500Nm mở ốc bánh xe container có nổi không?", "Súng siết bu lông 1500Nm", "Hook: 'Liệu con máy nhỏ này có mở được ốc rỉ sét 5 năm?'. Test thực tế tại bãi xe container.", "Âm thanh máy gầm uy lực", "Tứ (Media)", "Thợ gara khách mời", "Đang quay", "Gắn link giỏ hàng máy bu lông", "#kingblue #mayxietbulong #garaoto", 0, 0, "Cần an toàn lao động khi quay bãi xe"]
    ]

    for row_idx, r_data in enumerate(sample_tt, start=4):
        ws3.row_dimensions[row_idx].height = 28
        for col_idx, val in enumerate(r_data, start=1):
            c = ws3.cell(row=row_idx, column=col_idx, value=val)
            c.font = font_body
            c.border = border_cell
            c.alignment = align_center if col_idx in [1, 3, 8, 9, 10] else (align_wrap_left if col_idx in [4, 6] else align_left)
            if col_idx in [13, 14]:
                c.alignment = align_right
                c.number_format = "#,##0"
            if row_idx % 2 == 1:
                c.fill = fill_zebra

    col_widths_3 = {
        "A": 6, "B": 12, "C": 14, "D": 36, "E": 22, "F": 44, "G": 22,
        "H": 18, "I": 20, "J": 18, "K": 24, "L": 24, "M": 14, "N": 14, "O": 28
    }
    for col_letter, w in col_widths_3.items():
        ws3.column_dimensions[col_letter].width = w
    ws3.freeze_panes = "C4"

    # -------------------------------------------------------------
    # TAB 4: KOC & REVIEWER
    # -------------------------------------------------------------
    ws4 = wb.create_sheet("KOC & REVIEWER")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells("A1:N1")
    t4 = ws4.cell(row=1, column=1, value="🤝 DANH SÁCH & TIẾN ĐỘ HỢP TÁC KOC / REVIEWER NGÀNH CƠ KHÍ")
    t4.font = font_title
    t4.fill = fill_title
    t4.alignment = align_center
    ws4.row_dimensions[1].height = 36

    headers_koc = [
        "STT", "Kênh / Tên KOC", "Nền tảng", "Followers / Subs", "Người liên hệ (KOC)",
        "Số điện thoại / Zalo", "Dòng máy gửi trải nghiệm", "Hình thức hợp tác", "Chi phí / Thù lao",
        "Trạng thái hợp tác", "Ngày gửi mẫu", "Ngày dự kiến lên clip", "Link clip review", "Đánh giá hiệu quả"
    ]
    ws4.row_dimensions[3].height = 26
    for col_idx, h in enumerate(headers_koc, start=1):
        c = ws4.cell(row=3, column=col_idx, value=h)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    sample_koc = [
        [1, "Đồ Nghề Tự Chọn", "YouTube & TikTok", "280,000", "Anh Vũ", "090xxxxxxx", "Máy khoan KM18 + Bộ mũi đa năng", "Tặng máy trải nghiệm + Affiliate", "0 VNĐ (Affiliate hoa hồng)", "Đã chốt & Gửi máy", "02/10/2026", "12/10/2026", "https://youtube.com/...", "Kênh uy tín cao, tệp thợ chuẩn"],
        [2, "Thích Tự Làm", "TikTok & Facebook", "350,000", "Team Admin", "098xxxxxxx", "Máy cân bằng Laser 12 tia", "Tặng sản phẩm + Booking video", "2,500,000 VNĐ", "Đang liên hệ", "", "18/10/2026", "", "Chờ KOC gửi báo giá chính thức"],
        [3, "Máy Móc Việt Nam", "YouTube", "190,000", "Anh Hưng", "091xxxxxxx", "Súng siết bu lông 1500Nm KBA-I1500", "Video so sánh đập hộp", "3,000,000 VNĐ", "Đang làm clip", "04/10/2026", "15/10/2026", "", "Chờ bản nháp duyệt trước khi public"]
    ]

    for row_idx, r_data in enumerate(sample_koc, start=4):
        ws4.row_dimensions[row_idx].height = 26
        for col_idx, val in enumerate(r_data, start=1):
            c = ws4.cell(row=row_idx, column=col_idx, value=val)
            c.font = font_body
            c.border = border_cell
            c.alignment = align_center if col_idx in [1, 3, 10, 11, 12] else align_left
            if row_idx % 2 == 1:
                c.fill = fill_zebra

    col_widths_4 = {
        "A": 6, "B": 24, "C": 18, "D": 16, "E": 18, "F": 18, "G": 32,
        "H": 26, "I": 22, "J": 20, "K": 14, "L": 18, "M": 26, "N": 30
    }
    for col_letter, w in col_widths_4.items():
        ws4.column_dimensions[col_letter].width = w
    ws4.freeze_panes = "C4"

    # -------------------------------------------------------------
    # TAB 5: WEBSITE & SEO
    # -------------------------------------------------------------
    ws5 = wb.create_sheet("WEBSITE & SEO")
    ws5.views.sheetView[0].showGridLines = True

    ws5.merge_cells("A1:M1")
    t5 = ws5.cell(row=1, column=1, value="🌐 KẾ HOẠCH BÀI VIẾT CHUẨN SEO WEBSITE KINGBLUE.VN")
    t5.font = font_title
    t5.fill = fill_title
    t5.alignment = align_center
    ws5.row_dimensions[1].height = 36

    headers_seo = [
        "STT", "Mã bài", "Tiêu đề bài viết (H1)", "Từ khóa chính", "Từ khóa phụ",
        "Search Intent", "Số từ dự kiến", "Meta Description", "URL Slug dự kiến",
        "Người viết", "Trạng thái bài", "Tình trạng Index Google", "Ghi chú kỹ thuật"
    ]
    ws5.row_dimensions[3].height = 26
    for col_idx, h in enumerate(headers_seo, start=1):
        c = ws5.cell(row=3, column=col_idx, value=h)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    sample_seo = [
        [1, "SEO-01", "Top 5 Máy Khoan Pin Không Chổi Than Đáng Mua Nhất 2026", "máy khoan pin không chổi than", "máy khoan pin king blue, máy khoan brushless", "Mua hàng / Tìm hiểu", 1800, "Đánh giá chi tiết top 5 dòng máy khoan pin không chổi than lực khỏe, bền bỉ và tiết kiệm pin tốt nhất hiện nay từ King Blue.", "/top-5-may-khoan-pin-khong-choi-than", "Võ Thị Hoài Thương", "Đã xuất bản", "Đã index", "Gắn link trỏ về danh mục máy khoan"],
        [2, "SEO-02", "Công Nghệ Brushless Motor Là Gì? Vì Sao Nên Chọn Máy Pin Động Cơ Không Chổi Than?", "động cơ brushless", "brushless motor là gì, ưu điểm động cơ không chổi than", "Thông tin / Giáo dục", 2200, "Tìm hiểu toàn diện nguyên lý hoạt động và lý do vì sao động cơ Brushless Motor trở thành tiêu chuẩn vàng trên máy pin King Blue.", "/dong-co-brushless-motor-la-gi", "Võ Thị Hoài Thương", "Đã xuất bản", "Đã index", "Bài viết trụ cột (Pillar content)"],
        [3, "SEO-03", "Đá Cắt Sắt 107mm King Blue: Bền Gấp 3 Lần, Cắt Ngọt Không Cháy Phôi", "đá cắt sắt 107mm", "đá cắt king blue, đá cắt sắt bén", "Mua hàng", 1400, "Khám phá dòng đá cắt sắt 107mm King Blue với công nghệ hạt mài cao cấp, chống vỡ an toàn và tuổi thọ vượt trội.", "/da-cat-sat-107mm-kingblue", "Võ Thị Hoài Thương", "Đang viết", "Chưa index", "Chờ Thiện gửi ảnh chụp bao bì mới"]
    ]

    for row_idx, r_data in enumerate(sample_seo, start=4):
        ws5.row_dimensions[row_idx].height = 26
        for col_idx, val in enumerate(r_data, start=1):
            c = ws5.cell(row=row_idx, column=col_idx, value=val)
            c.font = font_body
            c.border = border_cell
            c.alignment = align_center if col_idx in [1, 2, 7, 10, 11, 12] else align_left
            if row_idx % 2 == 1:
                c.fill = fill_zebra

    col_widths_5 = {
        "A": 6, "B": 12, "C": 38, "D": 26, "E": 28, "F": 18, "G": 14,
        "H": 40, "I": 30, "J": 20, "K": 16, "L": 20, "M": 28
    }
    for col_letter, w in col_widths_5.items():
        ws5.column_dimensions[col_letter].width = w
    ws5.freeze_panes = "C4"

    # -------------------------------------------------------------
    # TAB 6: CAU HINH & DANH MUC
    # -------------------------------------------------------------
    ws6 = wb.create_sheet("CAU HINH")
    ws6.views.sheetView[0].showGridLines = True

    ws6.merge_cells("A1:F1")
    t6 = ws6.cell(row=1, column=1, value="⚙️ DANH MỤC THIẾT LẬP DROPDOWN & HỆ THỐNG - KING BLUE MARKETING")
    t6.font = font_title
    t6.fill = PatternFill("solid", fgColor=C_NAVY_DARK)
    t6.alignment = align_center
    ws6.row_dimensions[1].height = 36

    config_cols = [
        ("KÊNH ĐĂNG", [
            "Facebook Fanpage", "TikTok", "YouTube Shorts", "YouTube Video",
            "Website SEO", "Zalo OA", "KOC & Reviewer", "Sàn TMĐT Shopee/Lazada"
        ]),
        ("ĐỊNH DẠNG", [
            "Video ngắn (Reels/TikTok)", "Video dài (Youtube)", "Album ảnh",
            "Single Post / Ảnh đơn", "Infographic / POSM", "Bài viết chuẩn SEO", "Mini Game / Give away"
        ]),
        ("TRỤ CỘT NỘI DUNG", [
            "Giới thiệu sản phẩm", "Mẹo thợ & Trải nghiệm", "Giáo dục kỹ thuật",
            "Đại lý & Phân phối", "Minigame & Tương tác", "KOC & Reviewer", "Hậu trường & Đội ngũ"
        ]),
        ("DÒNG SẢN PHẨM", [
            "Máy pin Brushless", "Dụng cụ cầm tay", "Đá cắt & Đá mài",
            "Thiết bị đo Laser", "Vật tư tiêu hao kim khí", "Chính sách B2B", "Khác"
        ]),
        ("NHÂN SỰ PHỤ TRÁCH", [
            "Võ Thị Hoài Thương", "Kiều Thương", "Thương Thương",
            "Thiện", "Tứ", "Thức", "Ngân", "Hùng", "Marketing Manager"
        ]),
        ("TRẠNG THÁI CONTENT", [
            "Lên ý tưởng", "Đang viết kịch bản", "Đang viết bài", "Đang quay",
            "Đang dựng", "Chờ thiết kế", "Đang duyệt", "Sẵn sàng đăng", "Đã đăng", "Tạm hoãn"
        ])
    ]

    ws6.row_dimensions[3].height = 24
    for idx, (head, items) in enumerate(config_cols, start=1):
        c = ws6.cell(row=3, column=idx, value=head)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell
        ws6.column_dimensions[get_column_letter(idx)].width = 24

        for r_idx, item in enumerate(items, start=4):
            ci = ws6.cell(row=r_idx, column=idx, value=item)
            ci.font = font_body
            ci.border = border_cell
            ci.alignment = align_center if idx in [1, 2, 5, 6] else align_left

    # Thiết lập Data Validation dropdown cho Tab 1 (TONG HOP CONTENT)
    def apply_dv(ws, col_letter, source_range, prompt):
        dv = DataValidation(type="list", formula1=f"='CAU HINH'!{source_range}", allow_blank=True)
        dv.error = "Vui lòng chọn giá trị hợp lệ từ danh sách!"
        dv.promptTitle = prompt
        ws.add_data_validation(dv)
        dv.add(f"{col_letter}6:{col_letter}100")

    apply_dv(ws1, "D", "$A$4:$A$15", "Kênh đăng")
    apply_dv(ws1, "E", "$B$4:$B$15", "Định dạng")
    apply_dv(ws1, "F", "$C$4:$C$15", "Trụ cột nội dung")
    apply_dv(ws1, "G", "$D$4:$D$15", "Dòng sản phẩm")
    apply_dv(ws1, "H", "$E$4:$E$15", "Người phụ trách")
    apply_dv(ws1, "I", "$E$4:$E$15", "Người phối hợp")
    apply_dv(ws1, "L", "$F$4:$F$15", "Trạng thái")

    wb.save(XLSX_FILE)
    print(f"✅ Đã tạo thành công file Excel offline: {XLSX_FILE}")
    return XLSX_FILE

if __name__ == "__main__":
    create_excel_content()

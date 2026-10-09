# -*- coding: utf-8 -*-
"""
KẾ HOẠCH TEST ADS FACEBOOK B2B (ĐẠI LÝ & CỬA HÀNG PHÂN PHỐI) - KING BLUE
========================================================================
Định hướng chiến lược tinh gọn:
  - KHÔNG PHÂN CHIA THEO SẢN PHẨM CỤ THỂ: Vì chưa xác định được sản phẩm Win.
    Tránh chia nhỏ ngân sách 20 triệu làm phân mảnh dữ liệu máy học.
  - TIẾP CẬN TỔNG THỂ THƯƠNG HIỆU & HỆ SINH THÁI KING BLUE:
    Đánh vào: Chính sách chiết khấu, Quầy kệ điểm bán, Toàn bộ Catalogue 2026, Bảo vệ giá.
  - MỤC TIÊU KÉP CỦA ĐỢT TEST:
    1. Thu thập 100 - 105 Leads đại lý/cửa hàng phân phối tiềm năng (CPL 180k - 200k).
    2. Khảo sát thực tế nhu cầu thị trường xem cửa hàng quan tâm dòng hàng nào nhất
       để từ đó xác định chính xác "SẢN PHẨM WIN" cho giai đoạn mở rộng tiếp theo.
  - Kênh: 100% Facebook Ads (Instant Form, Messenger Ads).
  - Ngân sách: Test 20.000.000 VNĐ / tháng (~667.000 VNĐ/ngày).
  - Nhân sự: Kiều Thương (Phụ trách chính), Marketing Manager (Hỗ trợ & Duyệt).
"""

import os
import sys
import json
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_FILE = os.path.join(BASE_DIR, "Ke_Hoach_Chay_Quang_Cao_B2B_KingBlue.xlsx")
TOKEN_FILE = os.path.join(BASE_DIR, "API", "token.json")
LINKS_FILE = os.path.join(BASE_DIR, "google_sheets_links.json")

# Màu sắc nhận diện King Blue
C_NAVY_DARK = "0F172A"   # Slate 900
C_NAVY_HEAD = "1A365D"   # Royal Navy
C_BLUE_SUB  = "1E3A8A"   # Blue 900
C_BLUE_ACC  = "2563EB"   # Royal Blue
C_AMBER_BG  = "FEF3C7"   # Amber 100
C_GREEN_BG  = "DCFCE7"   # Green 100
C_ZEBRA     = "F8FAFC"   # Slate 50
C_BORDER    = "CBD5E1"   # Slate 300
C_CARD_BG   = "F1F5F9"   # Slate 100

def build_excel_b2b_brand_test():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    font_title = Font(name="Arial", size=13, bold=True, color="FFFFFF")
    font_sec_head = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    font_head = Font(name="Arial", size=9, bold=True, color="FFFFFF")
    font_body = Font(name="Arial", size=9, color="0F172A")
    font_bold = Font(name="Arial", size=9, bold=True, color="0F172A")
    font_stat_val = Font(name="Arial", size=12, bold=True, color="1E3A8A")
    font_stat_lbl = Font(name="Arial", size=8, bold=True, color="64748B")

    fill_title = PatternFill("solid", fgColor=C_NAVY_HEAD)
    fill_sec_head = PatternFill("solid", fgColor=C_NAVY_DARK)
    fill_head = PatternFill("solid", fgColor=C_BLUE_SUB)
    fill_card = PatternFill("solid", fgColor=C_CARD_BG)
    fill_amber_card = PatternFill("solid", fgColor=C_AMBER_BG)
    fill_green_card = PatternFill("solid", fgColor=C_GREEN_BG)

    thin_border_side = Side(style="thin", color=C_BORDER)
    border_cell = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")
    align_wrap_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # =========================================================================
    # TAB 1: TONG QUAN & KPI TEST B2B
    # =========================================================================
    ws1 = wb.create_sheet("TONG QUAN & KPI TEST B2B")
    ws1.views.sheetView[0].showGridLines = True

    # Title Banner
    ws1.merge_cells("A1:L1")
    t1 = ws1.cell(row=1, column=1, value="🎯 ĐỊNH HƯỚNG TEST ADS FACEBOOK B2B (NGÂN SÁCH 600k - 700k/NGÀY & TÌM SẢN PHẨM WIN) - KING BLUE")
    t1.font = font_title
    t1.fill = fill_title
    t1.alignment = align_center
    ws1.row_dimensions[1].height = 38

    # KPI Metric Cards (Dòng 2 & 3 - 6 thẻ từ A đến L)
    kpis = [
        ("A", "B", "NGÂN SÁCH THÁNG", "20,000,000 ₫", fill_card),
        ("C", "D", "NGÂN SÁCH NGÀY (DAILY)", "600k – 700k ₫/ngày (TB 670k)", fill_amber_card),
        ("E", "F", "MỤC TIÊU LEAD NGÀY", "~3 – 4 Leads / ngày", fill_green_card),
        ("G", "H", "MỤC TIÊU LEAD THÁNG", "100 – 105 Leads", fill_card),
        ("I", "J", "CPL MỤC TIÊU (COST/LEAD)", "180,000 ₫ – 200,000 ₫", fill_card),
        ("K", "L", "NHÂN SỰ PHỤ TRÁCH", "Kiều Thương (Manager hỗ trợ)", fill_card),
    ]

    for c_start, c_end, lbl, val, bg in kpis:
        ws1.merge_cells(f"{c_start}2:{c_end}2")
        ws1.merge_cells(f"{c_start}3:{c_end}3")
        c1 = ws1[f"{c_start}2"]
        c1.value = lbl
        c1.font = font_stat_lbl
        c1.alignment = align_center
        c1.fill = bg
        c2 = ws1[f"{c_start}3"]
        c2.value = val
        c2.font = font_stat_val
        c2.alignment = align_center
        c2.fill = bg

    ws1.row_dimensions[2].height = 18
    ws1.row_dimensions[3].height = 26

    # Section 1: Lộ Trình 3 Giai Đoạn Triển Khai Chiến Dịch Test Ads B2B
    ws1.merge_cells("A5:L5")
    s1 = ws1.cell(row=5, column=1, value="1. LỘ TRÌNH 3 GIAI ĐOẠN TRIỂN KHAI CHIẾN DỊCH TEST ADS B2B & TÌM SẢN PHẨM WIN")
    s1.font = font_sec_head
    s1.fill = fill_sec_head
    s1.alignment = align_left
    ws1.row_dimensions[5].height = 24

    ws1.merge_cells("C6:E6")
    ws1.merge_cells("F6:L6")
    ws1.row_dimensions[6].height = 24

    for ci, (col_letter, text) in enumerate([("A", "STT"), ("B", "Giai Đoạn Triển Khai"), ("C", "Nhiệm Vụ & Hoạt Động Trọng Tâm"), ("F", "Mục Tiêu & Tiêu Chuẩn Đầu Ra (KPI / Ngân Sách)")], start=1):
        c = ws1[f"{col_letter}6"]
        c.value = text
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    for c_empty in ["D6", "E6", "G6", "H6", "I6", "J6", "K6", "L6"]:
        ws1[c_empty].border = border_cell

    phase_data = [
        [
            1,
            "Giai đoạn 1: Sản xuất nội dung & Testing tìm kiếm nội dung win (Tuần 1)",
            "• Sản xuất ma trận creative (Ảnh Carousel hệ sinh thái, Video thực tế bàn giao kệ POSM, Infographic chiết khấu 35%).\n• Khởi chạy 4 Campaign thăm dò trên FB Ads với Daily Budget ~600k/ngày (130k - 200k/camp).\n• Đo lường chỉ số tương tác: CTR (>2.5%), CPC, tỷ lệ mở Lead Form và phản hồi ban đầu của chủ tiệm.",
            "• Thu về ~20 - 25 leads đầu tiên để kiểm tra chất lượng tệp đại lý.\n• Xác định rõ Mẫu Nội Dung Win (Winning Creative & Copy) có CPL < 180k - 200k.\n• Kiều Thương hoàn thiện kịch bản gọi điện tư vấn và gửi Catalogue/Báo giá sỉ."
        ],
        [
            2,
            "Giai đoạn 2: Tối ưu và chỉnh sửa (Tuần 2 đến Tuần 3)",
            "• Tắt ngay các mẫu quảng cáo/angle có CPL cao (> 220k - 250k) hoặc tỷ lệ chuyển đổi thấp.\n• Tối ưu sâu nội dung win: Thay hook 3s đầu video, thử nghiệm tiêu đề mới, thêm câu hỏi lọc tệp trong Lead Form để hạn chế lead rác.\n• Kiều Thương phân loại dòng hàng đại lý hỏi nhiều nhất vào Tab 5 (máy pin, đá cắt, catalogue...). Manager duyệt điều chỉnh ngân sách giữa các camp.",
            "• Kéo CPL toàn chiến dịch về chuẩn mục tiêu: 180.000 ₫ – 200.000 ₫ / Lead.\n• Tỷ lệ lead đúng chân dung chủ cửa hàng/đại lý đạt > 80%.\n• Thu thêm ~45 - 55 leads chất lượng cao, phục vụ sàng lọc nhu cầu thị trường."
        ],
        [
            3,
            "Giai đoạn 3: Ổn định ngân sách (Tuần 3 đến Tuần 4)",
            "• Khóa trần ngân sách ngày cố định ở mức 650.000 ₫ – 700.000 ₫ / ngày (dồn 75% ngân sách cho Camp Win, 25% duy trì khảo sát catalogue).\n• Duy trì phân phối ổn định của máy học Meta để dòng lead đổ về đều đặn ~3 – 4 leads/ngày.\n• Tổng kết dữ liệu Tab 5: Phân tích tỷ lệ đại lý quan tâm từng dòng hàng để chốt danh mục 'Sản Phẩm Win' cho King Blue.",
            "• Cán mốc tổng 100 – 105 Leads đại lý trong tháng với tổng ngân sách đúng 20.000.000 ₫.\n• Kiểm soát chặt chẽ chi phí hàng ngày, không bị hụt hoặc vượt ngân sách.\n• Báo cáo hoàn chỉnh danh mục Sản Phẩm Win làm tiền đề mở rộng quy mô lớn cho các tháng sau."
        ]
    ]

    for r_idx, r_val in enumerate(phase_data, start=7):
        ws1.row_dimensions[r_idx].height = 54
        ws1.cell(row=r_idx, column=1, value=r_val[0]).alignment = align_center
        ws1.cell(row=r_idx, column=1).font = font_body
        ws1.cell(row=r_idx, column=1).border = border_cell

        ws1.cell(row=r_idx, column=2, value=r_val[1]).alignment = align_wrap_left
        ws1.cell(row=r_idx, column=2).font = font_bold
        ws1.cell(row=r_idx, column=2).border = border_cell

        ws1.merge_cells(f"C{r_idx}:E{r_idx}")
        c_reg = ws1[f"C{r_idx}"]
        c_reg.value = r_val[2]
        c_reg.font = font_body
        c_reg.alignment = align_wrap_left
        for col_l in ["C", "D", "E"]:
            ws1[f"{col_l}{r_idx}"].border = border_cell

        ws1.merge_cells(f"F{r_idx}:L{r_idx}")
        c_det = ws1[f"F{r_idx}"]
        c_det.value = r_val[3]
        c_det.font = font_body
        c_det.alignment = align_wrap_left
        for col_l in ["F", "G", "H", "I", "J", "K", "L"]:
            ws1[f"{col_l}{r_idx}"].border = border_cell

    ws1.row_dimensions[10].height = 12

    # Section 2: 4 Trục Góc Tiếp Cận Thử Nghiệm & Cơ Cấu Ngân Sách Ngày
    ws1.merge_cells("A11:L11")
    s2 = ws1.cell(row=11, column=1, value="2. 4 TRỤC GÓC TIẾP CẬN THỬ NGHIỆM & PHÂN BỔ NGÂN SÁCH NGÀY (670.000 ₫ / NGÀY)")
    s2.font = font_sec_head
    s2.fill = fill_sec_head
    s2.alignment = align_left
    ws1.row_dimensions[11].height = 24

    seg_headers = [
        "STT", "Trục Góc Tiếp Cận (Angle)", "Ý Tưởng & Định Hướng Nội Dung", "Giá Trị Trọng Tâm Cho Đại Lý",
        "Hình Thức Triển Khai", "Mục Đích Khảo Sát", "Ngân Sách Ngày (VNĐ)",
        "Ngân Sách Tháng (VNĐ)", "Lead Ngày Dự Kiến", "KPI Lead Tháng", "CPL Kế Hoạch", "Tỷ Trọng (%)"
    ]
    ws1.row_dimensions[12].height = 24
    for idx, h in enumerate(seg_headers, start=1):
        c = ws1.cell(row=12, column=idx, value=h)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    angle_data = [
        [1, "Angle 1: Chính Sách Chiết Khấu & Biên Lợi Nhuận", "Đánh vào bài toán lãi gộp và nhập hàng trực tiếp từ nhà sản xuất", "Chiết khấu đại lý lên tới 35%, bảng giá sỉ trực tiếp không trung gian", "Lead Form (Nhận bảng giá sỉ)", "Đo lường mức độ nhạy cảm về giá & chiết khấu", 200000, 6000000, 1.0, 32, 187500, 0.30],
        [2, "Angle 2: Hỗ Trợ Điểm Bán & Kệ Trưng Bày POSM", "Đánh vào mong muốn nâng tầm hình ảnh cửa hàng đẹp mắt, chuyên nghiệp", "Tài trợ 100% Kệ sắt trưng bày chuẩn Royal Blue King Blue & Biển bảng", "Lead Form / Messenger", "Đo lường sự quan tâm về hình ảnh & hỗ trợ điểm bán", 170000, 5000000, 0.9, 27, 185185, 0.25],
        [3, "Angle 3: Toàn Bộ Hệ Sinh Thái & Catalogue 2026", "Giới thiệu toàn diện dải hàng: Máy pin, máy điện, đá mài, đồ cầm tay", "Tải trọn bộ Catalogue 2026 & Danh mục hơn 300 sản phẩm kim khí", "Lead Form (Tải Catalogue)", "Khảo sát xem đại lý hỏi dòng sản phẩm nào nhiều nhất", 170000, 5000000, 0.9, 27, 185185, 0.25],
        [4, "Angle 4: Cam Kết Bảo Vệ Vùng Bán & Chống Phá Giá", "Giải quyết nỗi lo bị cạnh tranh phá giá và đọng vốn tồn kho ban đầu", "Bảo vệ giá niêm yết toàn quốc, hỗ trợ đổi trả hàng chậm bán 60 ngày", "Messenger Ads (Tư vấn 1-1)", "Đo lường mức độ quan tâm về chính sách bảo hộ đại lý", 130000, 4000000, 0.6, 19, 210526, 0.20],
    ]

    for r_idx, row in enumerate(angle_data, start=13):
        ws1.row_dimensions[r_idx].height = 26
        for col_idx, val in enumerate(row, start=1):
            c = ws1.cell(row=r_idx, column=col_idx, value=val)
            c.font = font_body
            c.border = border_cell
            if col_idx == 1:
                c.alignment = align_center
            elif col_idx in [2, 3, 4, 5, 6]:
                c.alignment = align_wrap_left
            elif col_idx in [7, 8, 11]:
                c.alignment = align_right
                c.number_format = "#,##0 ₫"
            elif col_idx == 9:
                c.alignment = align_center
                c.number_format = "0.0"
            elif col_idx == 10:
                c.alignment = align_center
                c.number_format = "#,##0"
            elif col_idx == 12:
                c.alignment = align_center
                c.number_format = "0.0%"

    # Dòng Tổng Cộng Phân Khúc (Row 17)
    ws1.row_dimensions[17].height = 24
    ws1.cell(row=17, column=1, value="").border = border_cell
    c_tot_s = ws1.cell(row=17, column=2, value="TỔNG CỘNG")
    c_tot_s.font = font_bold
    c_tot_s.alignment = align_center
    c_tot_s.fill = fill_card
    c_tot_s.border = border_cell

    for ci in range(3, 7):
        c_dash = ws1.cell(row=17, column=ci, value="-")
        c_dash.font = font_bold
        c_dash.alignment = align_center
        c_dash.fill = fill_card
        c_dash.border = border_cell

    # Ngân sách ngày tổng cộng
    c_sum_daily = ws1.cell(row=17, column=7, value="=SUM(G13:G16)")
    c_sum_daily.font = font_bold
    c_sum_daily.alignment = align_right
    c_sum_daily.number_format = "#,##0 ₫"
    c_sum_daily.fill = fill_amber_card
    c_sum_daily.border = border_cell

    # Ngân sách tháng tổng cộng
    c_sum_bud = ws1.cell(row=17, column=8, value="=SUM(H13:H16)")
    c_sum_bud.font = font_bold
    c_sum_bud.alignment = align_right
    c_sum_bud.number_format = "#,##0 ₫"
    c_sum_bud.fill = fill_card
    c_sum_bud.border = border_cell

    # Lead ngày tổng cộng
    c_sum_lead_d = ws1.cell(row=17, column=9, value="=SUM(I13:I16)")
    c_sum_lead_d.font = font_bold
    c_sum_lead_d.alignment = align_center
    c_sum_lead_d.number_format = "0.0"
    c_sum_lead_d.fill = fill_green_card
    c_sum_lead_d.border = border_cell

    # Lead tháng tổng cộng
    c_sum_leads = ws1.cell(row=17, column=10, value="=SUM(J13:J16)")
    c_sum_leads.font = font_bold
    c_sum_leads.alignment = align_center
    c_sum_leads.number_format = "#,##0"
    c_sum_leads.fill = fill_card
    c_sum_leads.border = border_cell

    # CPL trung bình
    c_avg_cpl = ws1.cell(row=17, column=11, value="=H17/J17")
    c_avg_cpl.font = font_bold
    c_avg_cpl.alignment = align_right
    c_avg_cpl.number_format = "#,##0 ₫"
    c_avg_cpl.fill = fill_card
    c_avg_cpl.border = border_cell

    # Tỷ trọng tổng
    c_sum_pct = ws1.cell(row=17, column=12, value="=SUM(L13:L16)")
    c_sum_pct.font = font_bold
    c_sum_pct.alignment = align_center
    c_sum_pct.number_format = "0.0%"
    c_sum_pct.fill = fill_card
    c_sum_pct.border = border_cell

    col_w_1 = [6, 26, 32, 30, 20, 26, 18, 18, 14, 14, 16, 12]
    for idx, w in enumerate(col_w_1, start=1):
        ws1.column_dimensions[get_column_letter(idx)].width = w

    # =========================================================================
    # TAB 2: QUAN LY TASK DU AN (AI LÀM GÌ NHƯ THẾ NÀO)
    # =========================================================================
    ws_task = wb.create_sheet("QUAN LY TASK DU AN")
    ws_task.views.sheetView[0].showGridLines = True

    ws_task.merge_cells("A1:M1")
    t_task = ws_task.cell(row=1, column=1, value="📋 BẢNG PHÂN CÔNG & QUẢN LÝ TIẾN ĐỘ CÔNG VIỆC DỰ ÁN ADS B2B - KING BLUE")
    t_task.font = font_title
    t_task.fill = fill_title
    t_task.alignment = align_center
    ws_task.row_dimensions[1].height = 36

    # KPI summary bar (Row 2 & 3)
    task_kpis = [
        ("A", "B", "TỔNG SỐ ĐẦU VIỆC (TASKS)", "=COUNTA(B5:B25)", fill_card, "#,##0"),
        ("C", "D", "ĐÃ HOÀN THÀNH", '=COUNTIF(I5:I25, "Đã hoàn thành")', fill_green_card, "#,##0"),
        ("E", "F", "ĐANG THỰC HIỆN", '=COUNTIF(I5:I25, "Đang làm")', fill_amber_card, "#,##0"),
        ("G", "H", "CHỜ DUYỆT / REVIEW", '=COUNTIF(I5:I25, "Chờ duyệt")', fill_card, "#,##0"),
        ("I", "K", "TIẾN ĐỘ TOÀN DỰ ÁN", '=IF(COUNTA(B5:B25)>0, COUNTIF(I5:I25, "Đã hoàn thành")/COUNTA(B5:B25), 0)', fill_card, "0.0%"),
    ]

    for c_start, c_end, lbl, fml, bg, num_fmt in task_kpis:
        ws_task.merge_cells(f"{c_start}2:{c_end}2")
        ws_task.merge_cells(f"{c_start}3:{c_end}3")
        c1 = ws_task[f"{c_start}2"]
        c1.value = lbl
        c1.font = font_stat_lbl
        c1.alignment = align_center
        c1.fill = bg
        c2 = ws_task[f"{c_start}3"]
        c2.value = fml
        c2.font = font_stat_val
        c2.alignment = align_center
        c2.fill = bg
        c2.number_format = num_fmt

    ws_task.merge_cells("L2:M2")
    ws_task.merge_cells("L3:M3")
    ws_task["L2"].value = "ĐIỀU PHỐI DỰ ÁN"
    ws_task["L2"].font = font_stat_lbl
    ws_task["L2"].alignment = align_center
    ws_task["L2"].fill = fill_card
    ws_task["L3"].value = "Kiều Thương & Manager"
    ws_task["L3"].font = font_bold
    ws_task["L3"].alignment = align_center
    ws_task["L3"].fill = fill_card

    ws_task.row_dimensions[2].height = 18
    ws_task.row_dimensions[3].height = 26

    # Headers for Tasks
    task_headers = [
        "STT", "Mã Task", "Giai Đoạn", "Hạng Mục / Đầu Việc",
        "Mô Tả Chi Tiết & Hướng Dẫn (Làm Như Thế Nào)", "Tiêu Chuẩn Đầu Ra (Definition of Done)",
        "Người Phụ Trách (Ai Làm)", "Người Phối Hợp", "Trạng Thái", "Mức Độ Ưu Tiên",
        "Hạn Chót (Deadline)", "Kết Quả / Link File", "Ghi Chú Đánh Giá"
    ]
    ws_task.row_dimensions[4].height = 28
    for idx, h in enumerate(task_headers, start=1):
        c = ws_task.cell(row=4, column=idx, value=h)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    task_rows = [
        # Giai đoạn 1: SX Nội Dung & Test
        [
            1, "TASK-01", "Giai đoạn 1: SX Nội Dung & Test",
            "Xây dựng kịch bản Ad Copy cho 4 Campaign",
            "Soạn 4 bộ thông điệp theo 4 Angle: (1) Chiết khấu đại lý 35%, (2) Kệ POSM điểm bán, (3) Toàn bộ Catalogue 2026, (4) Cam kết bảo vệ giá & chống bán phá giá. Viết headline ngắn gọn, đánh trúng bài toán lợi nhuận của chủ tiệm.",
            "4 file kịch bản Ad Copy hoàn chỉnh (gồm Headline, Body copy, CTA) được Manager duyệt.",
            "Kiều Thương (Chạy ads chính)", "Marketing Manager (Hỗ trợ & Duyệt)",
            "Đã hoàn thành", "Khẩn cấp", "Tuần 1 - Ngày 1", "Tab CONTENT & CREATIVE FB", "Đã duyệt 4 bộ kịch bản"
        ],
        [
            2, "TASK-02", "Giai đoạn 1: SX Nội Dung & Test",
            "Thiết kế bộ Visual (Carousel 5 ảnh & Banner chính sách)",
            "Thiết kế bộ Carousel 5 ảnh tỷ lệ 1:1 chuẩn màu Royal Blue King Blue (ảnh dải máy pin, đá cắt, dụng cụ cầm tay); 2 banner tĩnh kèm dấu mộc cam kết chiết khấu 35% từ nhà sản xuất.",
            "Bộ 5 ảnh Carousel 1080x1080px + 2 banner Feed/Story sắc nét, đúng quy chuẩn nhận diện thương hiệu.",
            "Thiện (Thiết kế Visual)", "Kiều Thương (Chạy ads chính)",
            "Đã hoàn thành", "Khẩn cấp", "Tuần 1 - Ngày 2", "Drive / Creative Folder", "Đã bàn giao đầy đủ file ảnh"
        ],
        [
            3, "TASK-03", "Giai đoạn 1: SX Nội Dung & Test",
            "Quay & dựng video ngắn 30s thực tế quầy kệ POSM",
            "Đi thực tế tại điểm bán đối tác, quay cận cảnh độ chắc chắn của kệ sắt King Blue và dải hàng trưng bày; quay bàn giao biển hiệu hoặc clip giới thiệu 'Tài trợ 100% kệ sắt trưng bày'.",
            "1 video ngắn 30s tỷ lệ 9:16 (Reels/Stories) & 1:1 (Feed), âm thanh rõ, có text hook 3s đầu thu hút.",
            "Tứ (Quay dựng video)", "Thiện (Thiết kế Visual)",
            "Đã hoàn thành", "Cao", "Tuần 1 - Ngày 3", "Drive / Video POSM", "Video đạt chất lượng sắc nét"
        ],
        [
            4, "TASK-04", "Giai đoạn 1: SX Nội Dung & Test",
            "Thiết lập Instant Lead Form & Tích hợp nhận thông báo Lead",
            "Tạo Form đăng ký nhận báo giá/catalogue trên Meta: Thu thập Tên, SĐT, Tỉnh thành, Loại hình kinh doanh (Kim khí/Điện cơ/VLXD). Cài đặt thông báo chuông về Gmail/Zalo để phản hồi tức thì.",
            "Lead Form kích hoạt thành công, test điền form mẫu đổ về đầy đủ thông tin chuẩn xác.",
            "Kiều Thương (Chạy ads chính)", "Marketing Manager (Hỗ trợ & Duyệt)",
            "Đã hoàn thành", "Khẩn cấp", "Tuần 1 - Ngày 3", "Trình quản lý Meta Ads", "Form kết nối chuẩn xác"
        ],
        [
            5, "TASK-05", "Giai đoạn 1: SX Nội Dung & Test",
            "Khởi chạy 4 Campaign thăm dò với ngân sách ~600k-670k/ngày",
            "Setup 4 Campaign trên Trình quản lý quảng cáo theo đúng phân bổ: Camp 1 (200k/ngày), Camp 2 (170k/ngày), Camp 3 (170k/ngày), Camp 4 (130k/ngày). Target tệp chủ cửa hàng tỉnh, loại trừ thợ nhỏ.",
            "4 Campaign được Meta duyệt và cắn tiền đều đặn, không vi phạm chính sách quảng cáo.",
            "Kiều Thương (Chạy ads chính)", "Marketing Manager (Hỗ trợ & Duyệt)",
            "Đang làm", "Khẩn cấp", "Tuần 1 - Ngày 4", "Meta Ads Manager", "4 Camp đang phân phối ổn định"
        ],
        [
            6, "TASK-06", "Giai đoạn 1: SX Nội Dung & Test",
            "Tiếp nhận, gọi điện tư vấn 20-25 leads đầu tiên & Cập nhật Tab 5",
            "Gọi điện tư vấn trong vòng 15-30 phút sau khi có lead. Chào đại lý, kết bạn Zalo gửi Catalogue 2026 + Bảng giá sỉ. Hỏi dòng hàng khách quan tâm nhất và ghi nhận vào Tab 5 (THEO DOI LEAD).",
            "100% lead được gọi và phân loại trạng thái (Nóng/Ấm/Lạnh/Dòng hàng hỏi nhiều nhất) trong Tab 5.",
            "Kiều Thương (Chạy ads chính)", "Marketing Manager (Hỗ trợ & Duyệt)",
            "Đang làm", "Cao", "Tuần 1 - Ngày 7", "Tab THEO DOI LEAD", "Đã tiếp nhận 6 leads đầu tiên"
        ],

        # Giai đoạn 2: Tối Ưu & Chỉnh Sửa
        [
            7, "TASK-07", "Giai đoạn 2: Tối Ưu & Chỉnh Sửa",
            "Rà soát chỉ số 4 Campaign & Tắt góc tiếp cận CPL cao (>220k)",
            "Sau 3 - 5 ngày chạy, họp nhanh 15 phút đánh giá CTR, CPC, CPL và chất lượng phản hồi từ cuộc gọi. Tắt các angle đắt hoặc ra lead không nghe máy/sai số.",
            "Biên bản quyết định tắt 1-2 camp kém hiệu quả, giữ lại 1-2 camp win có CPL tốt nhất.",
            "Kiều Thương (Chạy ads chính)", "Marketing Manager (Hỗ trợ & Duyệt)",
            "Đang làm", "Cao", "Tuần 2 - Ngày 2", "Tab CHI TIET CHIEN DICH", "Đang theo dõi số liệu 3 ngày đầu"
        ],
        [
            8, "TASK-08", "Giai đoạn 2: Tối Ưu & Chỉnh Sửa",
            "Chỉnh sửa Creative Win & Thêm câu hỏi lọc tệp trong Lead Form",
            "Tối ưu lại mẫu quảng cáo win: Thay tiêu đề headline mạnh hơn, đổi ảnh bìa thumbnail, thêm câu hỏi bắt buộc: 'Anh/chị đang có mặt bằng cửa hàng kinh doanh không?' để chặn lead rác.",
            "Bộ 2-3 biến thể quảng cáo tối ưu được kích hoạt thay thế cho các mẫu cũ bị tắt.",
            "Thiện (Thiết kế Visual)", "Kiều Thương (Chạy ads chính)",
            "Chưa bắt đầu", "Trung bình", "Tuần 2 - Ngày 4", "Drive / Creative Win", "Chờ dữ liệu đo lường tuần 1"
        ],
        [
            9, "TASK-09", "Giai đoạn 2: Tối Ưu & Chỉnh Sửa",
            "Tăng ngân sách cho Campaign Win lên 400k-450k/ngày",
            "Dồn ngân sách cho Camp Win lên 400k - 450k/ngày, duy trì camp catalogue 150k - 200k/ngày. Tuyệt đối giữ tổng ngân sách ngày không vượt quá trần 700.000 ₫/ngày.",
            "Ngân sách tài khoản duy trì mức 650k - 700k/ngày, CPL bình quân toàn tài khoản giảm dưới 190.000 ₫.",
            "Kiều Thương (Chạy ads chính)", "Marketing Manager (Hỗ trợ & Duyệt)",
            "Chưa bắt đầu", "Cao", "Tuần 2 - Ngày 5", "Meta Ads Manager", "Sẽ nâng sau khi xác định camp win"
        ],
        [
            10, "TASK-10", "Giai đoạn 2: Tối Ưu & Chỉnh Sửa",
            "Chăm sóc chuyên sâu tệp lead 'Ấm' & 'Nóng' - Gửi mẫu dùng thử",
            "Lọc ra danh sách chủ tiệm có mặt bằng lớn, gọi điện tư vấn chính sách hỗ trợ mở điểm bán, gửi catalogue bản in + tặng mẫu đá cắt dùng thử hoặc mời ghé showroom.",
            "Tối thiểu 5 - 8 đại lý xác nhận quan tâm sâu hoặc hẹn lịch bàn giao quầy kệ điểm bán.",
            "Kiều Thương (Chạy ads chính)", "Marketing Manager (Hỗ trợ & Duyệt)",
            "Chưa bắt đầu", "Trung bình", "Tuần 2 - Ngày 7", "Zalo OA / Sổ tay CRM", "Thực hiện liên tục khi có lead tốt"
        ],

        # Giai đoạn 3: Ổn Định Ngân Sách
        [
            11, "TASK-11", "Giai đoạn 3: Ổn Định Ngân Sách",
            "Khóa trần ngân sách 650k-700k/ngày & Thu đều 3-4 leads/ngày",
            "Kiểm tra nhịp tiêu tiền của tài khoản Meta 2 lần/ngày (11h & 17h). Đảm bảo cắn tiền đều, duy trì dòng lead 3 - 4 số/ngày đổ về ổn định, tích lũy tiệm cận 20 triệu.",
            "Dòng lead đổ về đều đặn mỗi ngày, bảng Tab 2 và Tab 5 nhảy số tự động, không bị hụt ngân sách.",
            "Kiều Thương (Chạy ads chính)", "Marketing Manager (Hỗ trợ & Duyệt)",
            "Chưa bắt đầu", "Cao", "Tuần 3 - Tuần 4", "Meta Ads Manager", "Duy trì ổn định cả tuần"
        ],
        [
            12, "TASK-12", "Giai đoạn 3: Ổn Định Ngân Sách",
            "Thống kê dữ liệu Tab 5 & Phân tích tỷ lệ dòng hàng đại lý hỏi",
            "Trích xuất dữ liệu cột 'Dòng hàng khách hỏi nhiều nhất' tại Tab 5. Lập bảng thống kê tỷ lệ % đại lý quan tâm Máy pin 21V, Đá cắt/đá mài, Dụng cụ cầm tay, hay Catalogue mở tiệm mới.",
            "Biểu đồ phân tích thị hiếu thực tế của tệp 100+ đại lý kim khí toàn quốc đối với sản phẩm King Blue.",
            "Kiều Thương (Chạy ads chính)", "Marketing Manager (Hỗ trợ & Duyệt)",
            "Chưa bắt đầu", "Cao", "Tuần 4 - Ngày 5", "Tab THEO DOI LEAD", "Dữ liệu phục vụ chốt sản phẩm win"
        ],
        [
            13, "TASK-13", "Giai đoạn 3: Ổn Định Ngân Sách",
            "Họp nghiệm thu dự án Test Ads & Chốt danh mục 'Sản Phẩm Win'",
            "Họp tổng kết giữa Marketing Manager và Kiều Thương: Đánh giá tổng số lead thu về (100 - 105 lead), CPL thực tế (180k - 200k), chi đúng 20 triệu. Chốt danh mục dòng sản phẩm win để lập kế hoạch mở rộng.",
            "Báo cáo tổng kết dự án Test B2B hoàn chỉnh + Đề xuất ngân sách và chiến lược scale cho giai đoạn tiếp theo.",
            "Marketing Manager (Hỗ trợ & Duyệt)", "Kiều Thương (Chạy ads chính)",
            "Chưa bắt đầu", "Cao", "Tuần 4 - Ngày 7", "Báo cáo nghiệm thu dự án", "Chốt sản phẩm win làm trọng tâm"
        ]
    ]

    for r_idx, r_data in enumerate(task_rows, start=5):
        ws_task.row_dimensions[r_idx].height = 42
        for col_idx, val in enumerate(r_data, start=1):
            c = ws_task.cell(row=r_idx, column=col_idx, value=val)
            c.font = font_body
            c.border = border_cell
            if col_idx in [1, 2, 9, 10, 11]:
                c.alignment = align_center
            elif col_idx in [3, 7, 8]:
                c.alignment = align_left
            elif col_idx == 4:
                c.font = font_bold
                c.alignment = align_wrap_left
            else:
                c.alignment = align_wrap_left

    # Empty rows for new tasks (18 to 25)
    for r_idx in range(18, 26):
        ws_task.row_dimensions[r_idx].height = 24
        ws_task.cell(row=r_idx, column=1, value=r_idx - 4).alignment = align_center
        ws_task.cell(row=r_idx, column=1).border = border_cell
        for ci in range(2, 14):
            c = ws_task.cell(row=r_idx, column=ci, value="")
            c.border = border_cell

    col_w_task = [6, 12, 28, 30, 46, 36, 20, 20, 16, 14, 16, 24, 26]
    for idx, w in enumerate(col_w_task, start=1):
        ws_task.column_dimensions[get_column_letter(idx)].width = w

    # =========================================================================
    # TAB 3: CHI TIET CHIEN DICH FB ADS
    # =========================================================================
    ws2 = wb.create_sheet("CHI TIET CHIEN DICH FB ADS")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("A1:O1")
    t2 = ws2.cell(row=1, column=1, value="🎯 THEO DÕI CHI TIẾT CHIẾN DỊCH FB ADS (NGÂN SÁCH NGÀY 600k - 700k/NGÀY & ĐO LƯỜNG LEAD)")
    t2.font = font_title
    t2.fill = fill_title
    t2.alignment = align_center
    ws2.row_dimensions[1].height = 36

    # KPI summary bar (Row 2 & 3)
    ws2.merge_cells("A2:B2")
    ws2.merge_cells("A3:B3")
    ws2["A2"].value = "NGÂN SÁCH NGÀY (DAILY)"
    ws2["A2"].font = font_stat_lbl
    ws2["A2"].alignment = align_center
    ws2["A2"].fill = fill_amber_card
    ws2["A3"].value = "=SUM(F5:F15)"
    ws2["A3"].font = font_stat_val
    ws2["A3"].alignment = align_center
    ws2["A3"].fill = fill_amber_card
    ws2["A3"].number_format = "#,##0 ₫"

    ws2.merge_cells("C2:D2")
    ws2.merge_cells("C3:D3")
    ws2["C2"].value = "TỔNG NGÂN SÁCH THÁNG"
    ws2["C2"].font = font_stat_lbl
    ws2["C2"].alignment = align_center
    ws2["C2"].fill = fill_card
    ws2["C3"].value = "=SUM(G5:G15)"
    ws2["C3"].font = font_stat_val
    ws2["C3"].alignment = align_center
    ws2["C3"].fill = fill_card
    ws2["C3"].number_format = "#,##0 ₫"

    ws2.merge_cells("E2:F2")
    ws2.merge_cells("E3:F3")
    ws2["E2"].value = "TỔNG THỰC CHI"
    ws2["E2"].font = font_stat_lbl
    ws2["E2"].alignment = align_center
    ws2["E2"].fill = fill_card
    ws2["E3"].value = "=SUM(H5:H15)"
    ws2["E3"].font = font_stat_val
    ws2["E3"].alignment = align_center
    ws2["E3"].fill = fill_card
    ws2["E3"].number_format = "#,##0 ₫"

    ws2.merge_cells("G2:H2")
    ws2.merge_cells("G3:H3")
    ws2["G2"].value = "MỤC TIÊU LEAD THÁNG"
    ws2["G2"].font = font_stat_lbl
    ws2["G2"].alignment = align_center
    ws2["G2"].fill = fill_card
    ws2["G3"].value = "=SUM(I5:I15)"
    ws2["G3"].font = font_stat_val
    ws2["G3"].alignment = align_center
    ws2["G3"].fill = fill_card
    ws2["G3"].number_format = "#,##0"

    ws2.merge_cells("I2:J2")
    ws2.merge_cells("I3:J3")
    ws2["I2"].value = "LEAD THỰC TẾ THU VỀ"
    ws2["I2"].font = font_stat_lbl
    ws2["I2"].alignment = align_center
    ws2["I2"].fill = fill_green_card
    ws2["I3"].value = "=SUM(J5:J15)"
    ws2["I3"].font = font_stat_val
    ws2["I3"].alignment = align_center
    ws2["I3"].fill = fill_green_card
    ws2["I3"].number_format = "#,##0"

    ws2.merge_cells("K2:L2")
    ws2.merge_cells("K3:L3")
    ws2["K2"].value = "CPL THỰC TẾ TRUNG BÌNH"
    ws2["K2"].font = font_stat_lbl
    ws2["K2"].alignment = align_center
    ws2["K2"].fill = fill_card
    ws2["K3"].value = '=IF(SUM(J5:J15)>0, SUM(H5:H15)/SUM(J5:J15), 0)'
    ws2["K3"].font = font_stat_val
    ws2["K3"].alignment = align_center
    ws2["K3"].fill = fill_card
    ws2["K3"].number_format = "#,##0 ₫"

    ws2.merge_cells("M2:N2")
    ws2.merge_cells("M3:N3")
    ws2["M2"].value = "TIẾN ĐỘ ĐẠT LEAD"
    ws2["M2"].font = font_stat_lbl
    ws2["M2"].alignment = align_center
    ws2["M2"].fill = fill_card
    ws2["M3"].value = '=IF(SUM(I5:I15)>0, SUM(J5:J15)/SUM(I5:I15), 0)'
    ws2["M3"].font = font_stat_val
    ws2["M3"].alignment = align_center
    ws2["M3"].fill = fill_card
    ws2["M3"].number_format = "0.0%"

    ws2["O2"].value = "VẬN HÀNH"
    ws2["O2"].font = font_stat_lbl
    ws2["O2"].alignment = align_center
    ws2["O2"].fill = fill_card
    ws2["O3"].value = "Kiều Thương"
    ws2["O3"].font = font_bold
    ws2["O3"].alignment = align_center
    ws2["O3"].fill = fill_card

    ws2.row_dimensions[2].height = 18
    ws2.row_dimensions[3].height = 26

    # Headers for Campaigns (Đã có cột Ngân Sách Ngày và lược bỏ Sản Phẩm Trọng Tâm / Offer Hook)
    camp_headers = [
        "STT", "Mã Chiến Dịch", "Tên Chiến Dịch Facebook Ads", "Góc Tiếp Cận (Angle Thử Nghiệm)",
        "Định Dạng Ads", "Ngân Sách Ngày (VNĐ)", "Ngân Sách Tháng KH (VNĐ)", "Thực Chi (VNĐ)", "KPI Lead", "Lead Đạt",
        "Tỷ Lệ Đạt", "CPL KH (VNĐ)", "CPL Thực (VNĐ)", "Người Phụ Trách", "Trạng Thái"
    ]
    ws2.row_dimensions[4].height = 26
    for idx, h in enumerate(camp_headers, start=1):
        c = ws2.cell(row=4, column=idx, value=h)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    sample_campaigns = [
        [1, "FB-TEST-01", "Campaign 1", "Chiết khấu & Lợi nhuận", "Instant Lead Form", 200000, 6000000, 190000, "='THEO DOI LEAD & KHAO SAT WIN'!R5", "='THEO DOI LEAD & KHAO SAT WIN'!S5", "=IF(I5>0, J5/I5, 0)", "=IF(I5>0, G5/I5, 0)", "=IF(J5>0, H5/J5, 0)", "Kiều Thương (Chạy ads chính)", "Đang chạy"],
        [2, "FB-TEST-02", "Campaign 2", "Hỗ trợ điểm bán & Kệ POSM", "Instant Lead Form", 170000, 5000000, 370000, "='THEO DOI LEAD & KHAO SAT WIN'!R6", "='THEO DOI LEAD & KHAO SAT WIN'!S6", "=IF(I6>0, J6/I6, 0)", "=IF(I6>0, G6/I6, 0)", "=IF(J6>0, H6/J6, 0)", "Kiều Thương (Chạy ads chính)", "Đang chạy"],
        [3, "FB-TEST-03", "Campaign 3", "Catalogue & Hệ sinh thái", "Lead Form (Khảo sát dòng hàng)", 170000, 5000000, 360000, "='THEO DOI LEAD & KHAO SAT WIN'!R7", "='THEO DOI LEAD & KHAO SAT WIN'!S7", "=IF(I7>0, J7/I7, 0)", "=IF(I7>0, G7/I7, 0)", "=IF(J7>0, H7/J7, 0)", "Kiều Thương (Chạy ads chính)", "Đang chạy"],
        [4, "FB-TEST-04", "Campaign 4", "Bảo vệ giá & Hạn chế rủi ro", "Messenger Ads (Tin nhắn)", 130000, 4000000, 200000, "='THEO DOI LEAD & KHAO SAT WIN'!R8", "='THEO DOI LEAD & KHAO SAT WIN'!S8", "=IF(I8>0, J8/I8, 0)", "=IF(I8>0, G8/I8, 0)", "=IF(J8>0, H8/J8, 0)", "Kiều Thương (Chạy ads chính)", "Đang chạy"],
    ]

    for r_idx, r_data in enumerate(sample_campaigns, start=5):
        ws2.row_dimensions[r_idx].height = 22
        for col_idx, val in enumerate(r_data, start=1):
            c = ws2.cell(row=r_idx, column=col_idx, value=val)
            c.font = font_body
            c.border = border_cell
            if col_idx in [1, 2, 15]:
                c.alignment = align_center
            elif col_idx in [3, 4, 5, 14]:
                c.alignment = align_left
            elif col_idx in [6, 7, 8, 12, 13]:
                c.alignment = align_right
                c.number_format = "#,##0 ₫"
            elif col_idx in [9, 10]:
                c.alignment = align_center
                c.number_format = "#,##0"
            elif col_idx == 11:
                c.alignment = align_center
                c.number_format = "0.0%"

    # Empty rows for testing
    for r_idx in range(9, 16):
        ws2.row_dimensions[r_idx].height = 20
        ws2.cell(row=r_idx, column=1, value=r_idx - 4).alignment = align_center
        ws2.cell(row=r_idx, column=1).border = border_cell
        for ci in range(2, 16):
            c = ws2.cell(row=r_idx, column=ci, value="")
            c.border = border_cell
            if ci in [6, 7, 8, 12, 13]:
                c.number_format = "#,##0 ₫"
            elif ci in [9, 10]:
                c.number_format = "#,##0"
            elif ci == 11:
                c.value = f"=IF(I{r_idx}>0, J{r_idx}/I{r_idx}, 0)"
                c.number_format = "0.0%"
            elif ci == 13:
                c.value = f"=IF(J{r_idx}>0, H{r_idx}/J{r_idx}, 0)"

    col_w_2 = [6, 14, 20, 26, 22, 18, 18, 18, 10, 10, 12, 16, 16, 16, 14]
    for idx, w in enumerate(col_w_2, start=1):
        ws2.column_dimensions[get_column_letter(idx)].width = w

    # =========================================================================
    # TAB 3: NGAN SACH 4 TUAN (TEST 20 TRIEU)
    # =========================================================================
    ws3 = wb.create_sheet("NGAN SACH 4 TUAN")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("A1:K1")
    t3 = ws3.cell(row=1, column=1, value="💰 BẢNG PHÂN BỔ NGÂN SÁCH FACEBOOK ADS THEO 4 TUẦN & THEO NGÀY (TEST 20 TRIỆU)")
    t3.font = font_title
    t3.fill = fill_title
    t3.alignment = align_center
    ws3.row_dimensions[1].height = 36

    b_headers = [
        "STT", "Nhóm Góc Tiếp Cận Thử Nghiệm", "Ngân Sách Ngày (VNĐ)", "Ngân Sách Tháng KH (VNĐ)",
        "Tuần 1 (Thăm Dò)", "Tuần 2 (Sàng Lọc)", "Tuần 3 (Scale Góc Win)", "Tuần 4 (Tối Ưu & Thu Lead)",
        "Tổng Thực Chi (VNĐ)", "Chênh Lệch / Còn Lại", "Đánh Giá Pacing Ngân Sách"
    ]
    ws3.row_dimensions[3].height = 26
    for idx, h in enumerate(b_headers, start=1):
        c = ws3.cell(row=3, column=idx, value=h)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    b_rows = [
        [1, "Campaign 1 (Angle 1: Chiết Khấu Đại Lý)", 200000, 6000000, 1200000, 1500000, 1700000, 1600000, "Đang kiểm soát tốt"],
        [2, "Campaign 2 (Angle 2: Hỗ Trợ Kệ POSM)", 170000, 5000000, 1000000, 1300000, 1400000, 1300000, "Đang kiểm soát tốt"],
        [3, "Campaign 3 (Angle 3: Khám Phá Catalogue)", 170000, 5000000, 1200000, 1200000, 1300000, 1300000, "Đang kiểm soát tốt"],
        [4, "Campaign 4 (Angle 4: Bảo Vệ Vùng Bán)", 130000, 4000000, 800000, 1000000, 1100000, 1100000, "Đang kiểm soát tốt"],
    ]

    for r_idx, r_data in enumerate(b_rows, start=4):
        ws3.row_dimensions[r_idx].height = 22
        for col_idx, val in enumerate(r_data[:8], start=1):
            c = ws3.cell(row=r_idx, column=col_idx, value=val)
            c.font = font_body
            c.border = border_cell
            if col_idx == 1:
                c.alignment = align_center
            elif col_idx == 2:
                c.alignment = align_left
            else:
                c.alignment = align_right
                c.number_format = "#,##0 ₫"

        c_tot = ws3.cell(row=r_idx, column=9, value=f"=SUM(E{r_idx}:H{r_idx})")
        c_tot.font = font_bold
        c_tot.alignment = align_right
        c_tot.number_format = "#,##0 ₫"
        c_tot.border = border_cell

        c_diff = ws3.cell(row=r_idx, column=10, value=f"=D{r_idx}-I{r_idx}")
        c_diff.font = font_bold
        c_diff.alignment = align_right
        c_diff.number_format = "#,##0 ₫"
        c_diff.border = border_cell

        c_pacing = ws3.cell(row=r_idx, column=11, value=r_data[8])
        c_pacing.font = font_body
        c_pacing.alignment = align_center
        c_pacing.border = border_cell

    # Total row (Row 8)
    ws3.row_dimensions[8].height = 24
    c_tot_b = ws3.cell(row=8, column=2, value="TỔNG CỘNG THEO TUẦN")
    c_tot_b.font = font_bold
    c_tot_b.alignment = align_center
    c_tot_b.fill = fill_card
    c_tot_b.border = border_cell
    ws3.cell(row=8, column=1, value="").border = border_cell

    c_daily_tot = ws3.cell(row=8, column=3, value="=SUM(C4:C7)")
    c_daily_tot.font = font_bold
    c_daily_tot.alignment = align_right
    c_daily_tot.number_format = "#,##0 ₫"
    c_daily_tot.fill = fill_amber_card
    c_daily_tot.border = border_cell

    c_plan_tot = ws3.cell(row=8, column=4, value="=SUM(D4:D7)")
    c_plan_tot.font = font_bold
    c_plan_tot.alignment = align_right
    c_plan_tot.number_format = "#,##0 ₫"
    c_plan_tot.fill = fill_card
    c_plan_tot.border = border_cell

    for ci in range(5, 9):
        c_week = ws3.cell(row=8, column=ci, value=f"=SUM({get_column_letter(ci)}4:{get_column_letter(ci)}7)")
        c_week.font = font_bold
        c_week.alignment = align_right
        c_week.number_format = "#,##0 ₫"
        c_week.fill = fill_card
        c_week.border = border_cell

    c_tot_spent = ws3.cell(row=8, column=9, value="=SUM(I4:I7)")
    c_tot_spent.font = font_bold
    c_tot_spent.alignment = align_right
    c_tot_spent.number_format = "#,##0 ₫"
    c_tot_spent.fill = fill_amber_card
    c_tot_spent.border = border_cell

    c_tot_rem = ws3.cell(row=8, column=10, value="=SUM(J4:J7)")
    c_tot_rem.font = font_bold
    c_tot_rem.alignment = align_right
    c_tot_rem.number_format = "#,##0 ₫"
    c_tot_rem.fill = fill_green_card
    c_tot_rem.border = border_cell

    ws3.cell(row=8, column=11, value="").border = border_cell

    # Average Daily Budget Row per Week (Row 9)
    ws3.row_dimensions[9].height = 24
    ws3.cell(row=9, column=1, value="").border = border_cell
    c_avg_lbl = ws3.cell(row=9, column=2, value="TRUNG BÌNH CHI TIÊU / NGÀY")
    c_avg_lbl.font = font_bold
    c_avg_lbl.alignment = align_center
    c_avg_lbl.fill = fill_card
    c_avg_lbl.border = border_cell

    c_avg_d_all = ws3.cell(row=9, column=3, value="=C8")
    c_avg_d_all.font = font_bold
    c_avg_d_all.alignment = align_right
    c_avg_d_all.number_format = "#,##0 ₫"
    c_avg_d_all.fill = fill_amber_card
    c_avg_d_all.border = border_cell

    c_avg_m_lbl = ws3.cell(row=9, column=4, value="~667.000 ₫/ngày")
    c_avg_m_lbl.font = font_bold
    c_avg_m_lbl.alignment = align_center
    c_avg_m_lbl.fill = fill_card
    c_avg_m_lbl.border = border_cell

    for ci_w, col_l in [(5, "E"), (6, "F"), (7, "G"), (8, "H")]:
        c_w_avg = ws3.cell(row=9, column=ci_w, value=f"={col_l}8/7")
        c_w_avg.font = font_bold
        c_w_avg.alignment = align_right
        c_w_avg.number_format = "#,##0 ₫"
        c_w_avg.fill = fill_green_card
        c_w_avg.border = border_cell

    c_d9_dash1 = ws3.cell(row=9, column=9, value="-")
    c_d9_dash1.alignment = align_center
    c_d9_dash1.border = border_cell
    c_d9_dash2 = ws3.cell(row=9, column=10, value="-")
    c_d9_dash2.alignment = align_center
    c_d9_dash2.border = border_cell
    c_d9_dash3 = ws3.cell(row=9, column=11, value="-")
    c_d9_dash3.alignment = align_center
    c_d9_dash3.border = border_cell

    col_w_3 = [6, 38, 20, 22, 18, 18, 20, 20, 20, 20, 24]
    for idx, w in enumerate(col_w_3, start=1):
        ws3.column_dimensions[get_column_letter(idx)].width = w

    # =========================================================================
    # TAB 4: CONTENT & MA TRAN CREATIVE FB
    # =========================================================================
    ws4 = wb.create_sheet("CONTENT & CREATIVE FB")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells("A1:K1")
    t4 = ws4.cell(row=1, column=1, value="📝 MA TRẬN NỘI DUNG TỔNG THỂ THƯƠNG HIỆU & HỢP TÁC ĐẠI LÝ KING BLUE")
    t4.font = font_title
    t4.fill = fill_title
    t4.alignment = align_center
    ws4.row_dimensions[1].height = 36

    cnt_headers = [
        "STT", "Trục Thông Điệp (Angle)", "Tiêu Đề Quảng Cáo (Headline)",
        "Nội Dung Tiếp Cận (Ad Copy)", "Định Dạng Visual", "Yêu Cầu Media (Quay/Chụp)",
        "Kêu Gọi Hành Động (CTA)", "Đối Tượng Xem", "Người Phụ Trách", "Hỗ Trợ Visual", "Trạng Thái"
    ]
    ws4.row_dimensions[3].height = 26
    for idx, h in enumerate(cnt_headers, start=1):
        c = ws4.cell(row=3, column=idx, value=h)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    cnt_data = [
        [1, "Chiết khấu & Lợi nhuận", "TÌM NGUỒN HÀNG KIM KHÍ LÃI TỐT? CHIẾT KHẤU ĐẠI LÝ LÊN TỚI 35% CÙNG KING BLUE", "Kinh doanh kim khí muốn giữ khách phải có hàng bền, muốn biên lãi cao phải nhập tận gốc. King Blue mở rộng hệ thống đại lý toàn quốc: Chiết khấu tới 35%, bảng giá sỉ trực tiếp từ nhà sản xuất không qua trung gian.", "Ảnh Carousel 5 tấm trọn bộ", "Layout ảnh chụp tổng thể hệ sinh thái dụng cụ King Blue", "Đăng Ký Nhận Báo Giá Sỉ", "Chủ cửa hàng kim khí, điện cơ", "Kiều Thương (Chạy ads chính)", "Thiện (Thiết kế Visual)", "Đã sẵn sàng"],
        [2, "Hỗ trợ điểm bán & Kệ POSM", "MỞ ĐIỂM BÁN KING BLUE: TÀI TRỢ 100% KỆ TRƯNG BÀY & BIỂN HIỆU NHẬN DIỆN THƯƠNG HIỆU", "Nâng cấp không gian cửa hàng của bạn đẹp và chuyên nghiệp nhất khu vực. King Blue tài trợ kệ sắt sơn tĩnh điện chuyên dụng chuẩn thương hiệu Royal Blue, hỗ trợ thiết kế biển bảng mặt tiền.", "Video 30s thực tế lắp đặt kệ POSM", "Clip Tứ quay bàn giao kệ POSM tại cửa hàng đối tác", "Đăng Ký Tư Vấn Điểm Bán", "Chủ tiệm kim khí, VLXD", "Kiều Thương (Chạy ads chính)", "Tứ (Quay dựng video)", "Đã sẵn sàng"],
        [3, "Catalogue & Hệ sinh thái", "KHÁM PHÁ HỆ SINH THÁI THIẾT BỊ & KIM KHÍ KING BLUE 2026 - NHẬN TRỌN BỘ CATALOGUE", "Hơn 300 danh mục thiết bị từ máy pin, máy điện đến vật tư tiêu hao (đá cắt, mũi khoan, dụng cụ cầm tay). Đăng ký để tải trọn bộ catalogue chi tiết thông số và nhận tư vấn dòng hàng phù hợp nhất với khu vực của bạn.", "Banner Catalogue 2026 tổng thể", "Thiện thiết kế mockup cuốn catalogue King Blue dày dặn", "Tải Trọn Bộ Catalogue", "Chủ cửa hàng kim khí, điện cơ", "Kiều Thương (Chạy ads chính)", "Thiện (Thiết kế Visual)", "Đã sẵn sàng"],
        [4, "Bảo vệ giá & Hạn chế rủi ro", "CHÍNH SÁCH BẢO HỘ ĐẠI LÝ: KIỂM SOÁT 1 GIÁ TOÀN QUỐC - HỖ TRỢ ĐỔI TRẢ HÀNG CHẬM 60 NGÀY", "Không lo bị bán phá giá, không sợ tồn kho đọng vốn. King Blue áp dụng chính sách bảo vệ vùng bán và hỗ trợ đổi sang các sản phẩm phù hợp hơn trong 60 ngày đầu để đại lý yên tâm kinh doanh bền vững.", "Infographic cam kết bảo vệ đại lý", "Thiện làm visual cam kết không phá giá & đổi trả linh hoạt", "Xem Chính Sách Đại Lý", "Chủ cửa hàng máy công cụ, điện cơ", "Kiều Thương (Chạy ads chính)", "Thiện (Thiết kế Visual)", "Đã sẵn sàng"],
    ]

    for r_idx, row in enumerate(cnt_data, start=4):
        ws4.row_dimensions[r_idx].height = 36
        for col_idx, val in enumerate(row, start=1):
            c = ws4.cell(row=r_idx, column=col_idx, value=val)
            c.font = font_body
            c.border = border_cell
            if col_idx in [1, 7, 11]:
                c.alignment = align_center
            elif col_idx in [2, 8, 9, 10]:
                c.alignment = align_left
            else:
                c.alignment = align_wrap_left

    # Empty rows for new creative concepts (8 to 20)
    for r_idx in range(8, 21):
        ws4.row_dimensions[r_idx].height = 28
        ws4.cell(row=r_idx, column=1, value=r_idx - 3).alignment = align_center
        ws4.cell(row=r_idx, column=1).border = border_cell
        for ci in range(2, 12):
            c = ws4.cell(row=r_idx, column=ci, value="")
            c.border = border_cell

    col_w_4 = [6, 24, 32, 40, 24, 30, 22, 24, 16, 18, 16]
    for idx, w in enumerate(col_w_4, start=1):
        ws4.column_dimensions[get_column_letter(idx)].width = w

    # =========================================================================
    # TAB 5: THEO DOI LEAD & KHẢO SÁT SẢN PHẨM WIN
    # =========================================================================
    ws5 = wb.create_sheet("THEO DOI LEAD & KHAO SAT WIN")
    ws5.views.sheetView[0].showGridLines = True

    ws5.merge_cells("A1:T1")
    t5 = ws5.cell(row=1, column=1, value="🤝 DANH SÁCH TIẾP NHẬN LEAD ĐẠI LÝ & GHI NHẬN NHU CẦU ĐỂ TÌM 'SẢN PHẨM WIN'")
    t5.font = font_title
    t5.fill = fill_title
    t5.alignment = align_center
    ws5.row_dimensions[1].height = 36

    # Lead summary cards (Cột A đến N)
    lead_cards = [
        ("A", "C", "TỔNG LEAD THU VỀ", "=COUNTA(B5:B50)", fill_card),
        ("D", "F", "LEAD ĐÚNG CHÂN DUNG CỬA HÀNG", '=COUNTIF(M5:M50, "Nóng") + COUNTIF(M5:M50, "Ấm")', fill_amber_card),
        ("G", "I", "ĐÃ GỬI BÁO GIÁ / CATALOGUE", '=COUNTIF(K5:K50, "*Báo giá*") + COUNTIF(K5:K50, "*Catalogue*")', fill_card),
        ("J", "L", "HẸN HỢP TÁC / MỞ ĐIỂM BÁN", '=COUNTIF(K5:K50, "*ký thỏa thuận*") + COUNTIF(K5:K50, "*hẹn*")', fill_green_card),
        ("M", "N", "TỶ LỆ CHỐT LEAD", '=IF(COUNTA(B5:B50)>0, COUNTIF(K5:K50, "*ký thỏa thuận*")/COUNTA(B5:B50), 0)', fill_card)
    ]

    for c_start, c_end, lbl, fml, bg in lead_cards:
        ws5.merge_cells(f"{c_start}2:{c_end}2")
        ws5.merge_cells(f"{c_start}3:{c_end}3")
        c1 = ws5[f"{c_start}2"]
        c1.value = lbl
        c1.font = font_stat_lbl
        c1.alignment = align_center
        c1.fill = bg
        c2 = ws5[f"{c_start}3"]
        c2.value = fml
        c2.font = font_stat_val
        c2.alignment = align_center
        c2.fill = bg
        if "TỶ LỆ" in lbl:
            c2.number_format = "0.0%"
        else:
            c2.number_format = "#,##0"

    # Bảng Tiến Độ Thu Lead Theo Chiến Dịch (Cột P đến T)
    ws5.merge_cells("P2:T3")
    c_p_card = ws5["P2"]
    c_p_card.value = "🎯 BẢNG CHỈ TIÊU KPI & THỰC ĐẠT THEO CHIẾN DỊCH"
    c_p_card.font = font_sec_head
    c_p_card.fill = fill_sec_head
    c_p_card.alignment = align_center

    camp_summary_headers = ["STT", "Chiến Dịch FB", "KPI Lead", "Lead Đã Nhận", "Tỷ Lệ Đạt"]
    for idx_cs, h_cs in enumerate(camp_summary_headers, start=16):
        c_hcs = ws5.cell(row=4, column=idx_cs, value=h_cs)
        c_hcs.font = font_head
        c_hcs.fill = fill_head
        c_hcs.alignment = align_center
        c_hcs.border = border_cell

    camp_summary_data = [
        [1, "Campaign 1", "='TONG QUAN & KPI TEST B2B'!J13", "=COUNTIF(D$5:D$100, Q5)", "=IF(R5>0, S5/R5, 0)"],
        [2, "Campaign 2", "='TONG QUAN & KPI TEST B2B'!J14", "=COUNTIF(D$5:D$100, Q6)", "=IF(R6>0, S6/R6, 0)"],
        [3, "Campaign 3", "='TONG QUAN & KPI TEST B2B'!J15", "=COUNTIF(D$5:D$100, Q7)", "=IF(R7>0, S7/R7, 0)"],
        [4, "Campaign 4", "='TONG QUAN & KPI TEST B2B'!J16", "=COUNTIF(D$5:D$100, Q8)", "=IF(R8>0, S8/R8, 0)"],
    ]

    for r_idx, row_cs in enumerate(camp_summary_data, start=5):
        for c_idx, val_cs in enumerate(row_cs, start=16):
            c_cell = ws5.cell(row=r_idx, column=c_idx, value=val_cs)
            c_cell.font = font_body
            c_cell.border = border_cell
            if c_idx in [16, 17]:
                c_cell.alignment = align_center
            elif c_idx in [18, 19]:
                c_cell.alignment = align_center
                c_cell.number_format = "#,##0"
            elif c_idx == 20:
                c_cell.alignment = align_center
                c_cell.number_format = "0.0%"

    # Total row for Campaign Summary (Row 9)
    ws5.merge_cells("P9:Q9")
    c_tot_cs = ws5.cell(row=9, column=16, value="TỔNG CỘNG")
    c_tot_cs.font = font_bold
    c_tot_cs.alignment = align_center
    c_tot_cs.fill = fill_card
    c_tot_cs.border = border_cell
    ws5.cell(row=9, column=17).border = border_cell

    c_sum_kpi = ws5.cell(row=9, column=18, value="=SUM(R5:R8)")
    c_sum_kpi.font = font_bold
    c_sum_kpi.alignment = align_center
    c_sum_kpi.number_format = "#,##0"
    c_sum_kpi.fill = fill_card
    c_sum_kpi.border = border_cell

    c_sum_act = ws5.cell(row=9, column=19, value="=SUM(S5:S8)")
    c_sum_act.font = font_bold
    c_sum_act.alignment = align_center
    c_sum_act.number_format = "#,##0"
    c_sum_act.fill = fill_green_card
    c_sum_act.border = border_cell

    c_tot_rate = ws5.cell(row=9, column=20, value="=IF(R9>0, S9/R9, 0)")
    c_tot_rate.font = font_bold
    c_tot_rate.alignment = align_center
    c_tot_rate.number_format = "0.0%"
    c_tot_rate.fill = fill_card
    c_tot_rate.border = border_cell

    ws5.row_dimensions[2].height = 18
    ws5.row_dimensions[3].height = 26

    crm_headers = [
        "STT", "Mã Lead", "Ngày Nhận", "Chiến Dịch FB", "Tên Cửa Hàng / Đại Lý",
        "Người Liên Hệ", "Chức Vụ", "Số Điện Thoại / Zalo", "Tỉnh / Khu Vực",
        "Dòng Hàng Khách Hỏi Nhiều Nhất (Tìm SP Win)", "Trạng Thái Xử Lý", "Người Tiếp Nhận",
        "Đánh Giá Chất Lượng", "Ghi Chú Chi Tiết Phản Hồi Của Đại Lý"
    ]
    ws5.row_dimensions[4].height = 26
    for idx, h in enumerate(crm_headers, start=1):
        c = ws5.cell(row=4, column=idx, value=h)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell

    sample_leads = [
        [1, "FB-DL-001", "06/10/2026", "Campaign 1", "Cửa Hàng Kim Khí & Điện Nước Tuấn Phát", "Anh Nguyễn Văn Tuấn", "Chủ cửa hàng", "0912 345 678", "Đồng Nai", "Đá cắt & Đá mài (Vật tư tiêu hao)", "3-Đã gửi Báo giá & Chính sách", "Kiều Thương (Chạy ads chính)", "Nóng (Muốn hợp tác ngay)", "Khách hỏi kỹ giá đá cắt 107mm và 355mm, muốn so sánh giá với thương hiệu khác"],
        [2, "FB-DL-002", "06/10/2026", "Campaign 2", "Đại Lý Dụng Cụ Cơ Khí Hoàng Gia", "Anh Hoàng Văn Nam", "Chủ đại lý", "0988 123 456", "Bình Dương", "Combo mở điểm bán mới", "4-Đã ký thỏa thuận phân phối", "Kiều Thương (Chạy ads chính)", "Nóng (Muốn hợp tác ngay)", "Mặt bằng đẹp mặt tiền đường lớn, duyệt lắp kệ trưng bày King Blue và nhập dải máy pin"],
        [3, "FB-DL-003", "07/10/2026", "Campaign 3", "Cửa Hàng Thiết Bị Điện Cơ Tân Phát", "Anh Lê Quốc Tuấn", "Chủ tiệm", "0903 789 012", "Cần Thơ", "Máy pin Brushless 21V", "2-Đã tư vấn & Gửi Catalogue", "Kiều Thương (Chạy ads chính)", "Ấm (Đang xem chiết khấu)", "Tải catalogue xong nhắn hỏi máy pin có dùng chung chân pin Makita phổ thông không"],
        [4, "FB-DL-004", "07/10/2026", "Campaign 2", "Vật Liệu Xây Dựng & Kim Khí Việt Thắng", "Anh Phạm Văn Thắng", "Chủ đại lý", "0977 654 321", "Bắc Giang", "Combo mở điểm bán mới", "3-Đã gửi Báo giá & Chính sách", "Kiều Thương (Chạy ads chính)", "Nóng (Muốn hợp tác ngay)", "Chuẩn bị mở thêm chi nhánh, cần tư vấn danh mục 30 món hàng kim khí bán chạy nhất"],
        [5, "FB-DL-005", "08/10/2026", "Campaign 3", "Cửa Hàng Dụng Cụ Cầm Tay Tiến Phát", "Anh Trần Tiến Phát", "Chủ cửa hàng", "0934 567 890", "Hải Phòng", "Dụng cụ cầm tay & Thước cuộn", "2-Đã tư vấn & Gửi Catalogue", "Kiều Thương (Chạy ads chính)", "Ấm (Đang xem chiết khấu)", "Quan tâm kìm, cờ lê, thước cuộn tự hãm King Blue, đã gửi catalogue bản in"],
        [6, "FB-DL-006", "08/10/2026", "Campaign 4", "Đại Lý Phụ Kiện Kim Khí Quang Dũng", "Anh Vũ Quang Dũng", "Chủ tiệm", "0968 112 233", "Thanh Hóa", "Đá cắt & Đá mài (Vật tư tiêu hao)", "1-Mới tiếp nhận (Chờ gọi)", "Kiều Thương (Chạy ads chính)", "Nóng (Muốn hợp tác ngay)", "Lead mới đổ về, quan tâm chính sách bảo vệ giá và độc quyền khu vực huyện"]
    ]

    for r_idx, r_data in enumerate(sample_leads, start=5):
        ws5.row_dimensions[r_idx].height = 24
        for col_idx, val in enumerate(r_data, start=1):
            c = ws5.cell(row=r_idx, column=col_idx, value=val)
            c.font = font_body
            c.border = border_cell
            if col_idx in [1, 2, 3, 4, 7, 8, 9, 12, 13]:
                c.alignment = align_center
            else:
                c.alignment = align_wrap_left

    # Empty rows for new leads
    for r_idx in range(11, 46):
        ws5.row_dimensions[r_idx].height = 20
        ws5.cell(row=r_idx, column=1, value=r_idx - 4).alignment = align_center
        ws5.cell(row=r_idx, column=1).border = border_cell
        for ci in range(2, 15):
            c = ws5.cell(row=r_idx, column=ci, value="")
            c.border = border_cell

    col_w_5 = [6, 14, 12, 16, 28, 20, 16, 16, 16, 32, 26, 16, 16, 34, 4, 6, 16, 12, 14, 12]
    for idx, w in enumerate(col_w_5, start=1):
        ws5.column_dimensions[get_column_letter(idx)].width = w

    # =========================================================================
    # TAB 7: CAU HINH
    # =========================================================================
    ws6 = wb.create_sheet("CAU HINH")
    ws6.views.sheetView[0].showGridLines = True

    ws6.merge_cells("A1:V1")
    t6 = ws6.cell(row=1, column=1, value="⚙️ DANH MỤC CẤU HÌNH HỆ THỐNG DROPDOWN - FACEBOOK ADS ĐẠI LÝ B2B")
    t6.font = font_title
    t6.fill = fill_sec_head
    t6.alignment = align_center
    ws6.row_dimensions[1].height = 36

    config_cols = [
        # Col A (1)
        ("GÓC TIẾP CẬN (TEST ANGLE)", [
            "Chiết khấu & Lợi nhuận", "Hỗ trợ điểm bán & Kệ POSM",
            "Catalogue & Hệ sinh thái", "Bảo vệ giá & Hạn chế rủi ro",
            "Chính sách bảo hành uy tín", "Combo mở điểm bán mới"
        ]),
        # Col B (2)
        ("DÒNG HÀNG ĐẠI LÝ QUAN TÂM", [
            "Đá cắt & Đá mài (Vật tư tiêu hao)", "Máy pin Brushless 21V",
            "Máy điện & Máy hàn điện tử", "Dụng cụ cầm tay & Thước cuộn",
            "Thiết bị đo Laser", "Trọn bộ Catalogue / Tổng hợp",
            "Combo mở điểm bán mới"
        ]),
        # Col C (3)
        ("TÊN CHIẾN DỊCH FB", [
            "Campaign 1", "Campaign 2", "Campaign 3", "Campaign 4"
        ]),
        # Col D (4)
        ("ĐỊNH DẠNG QUẢNG CÁO FB", [
            "Instant Lead Form", "Messenger Ads (Tin nhắn)",
            "Lead Form (Khảo sát dòng hàng)", "Post Tương Tác Kéo Lead"
        ]),
        # Col E (5)
        ("TRẠNG THÁI CHIẾN DỊCH", [
            "Lên kế hoạch", "Chuẩn bị media", "Đang chạy", "Tạm dừng", "Đã hoàn thành"
        ]),
        # Col F (6)
        ("TRẠNG THÁI XỬ LÝ LEAD", [
            "1-Mới tiếp nhận (Chờ gọi)", "2-Đã tư vấn & Gửi Catalogue",
            "3-Đã gửi Báo giá & Chính sách", "4-Đã ký thỏa thuận phân phối",
            "5-Không liên lạc được / Sai số", "6-Không có nhu cầu"
        ]),
        # Col G (7)
        ("ĐÁNH GIÁ CHẤT LƯỢNG LEAD", [
            "Nóng (Muốn hợp tác ngay)", "Ấm (Đang xem chiết khấu)",
            "Lạnh (Tham khảo thêm)", "Sai số / Không nghe máy"
        ]),
        # Col H (8)
        ("NHÂN SỰ DỰ ÁN", [
            "Kiều Thương (Chạy ads chính)", "Marketing Manager (Hỗ trợ & Duyệt)",
            "Tứ (Quay dựng video)", "Thiện (Thiết kế Visual)"
        ]),
        # Col I (9)
        ("GIAI ĐOẠN DỰ ÁN", [
            "Giai đoạn 1: SX Nội Dung & Test",
            "Giai đoạn 2: Tối Ưu & Chỉnh Sửa",
            "Giai đoạn 3: Ổn Định Ngân Sách"
        ]),
        # Col J (10)
        ("TRẠNG THÁI TASK", [
            "Chưa bắt đầu", "Đang làm", "Chờ duyệt", "Đã hoàn thành", "Tạm hoãn"
        ]),
        # Col K (11)
        ("MỨC ĐỘ ƯU TIÊN", [
            "Khẩn cấp", "Cao", "Trung bình", "Thấp"
        ]),
        # Col L (12)
        ("CHỨC VỤ KHÁCH HÀNG", [
            "Chủ cửa hàng", "Chủ đại lý", "Chủ tiệm",
            "Quản lý kinh doanh", "Thợ nhận thầu / Cá nhân"
        ]),
        # Col M (13)
        ("ĐỊNH DẠNG VISUAL (CREATIVE)", [
            "Ảnh Carousel 5 tấm trọn bộ", "Video 30s thực tế lắp đặt kệ POSM",
            "Banner Catalogue 2026 tổng thể", "Infographic cam kết bảo vệ đại lý",
            "Bộ ảnh đơn chụp sản phẩm thực tế", "Video review máy pin / dụng cụ"
        ]),
        # Col N (14)
        ("KÊU GỌI HÀNH ĐỘNG (CTA)", [
            "Đăng Ký Nhận Báo Giá Sỉ", "Đăng Ký Tư Vấn Điểm Bán",
            "Tải Trọn Bộ Catalogue", "Xem Chính Sách Đại Lý",
            "Nhận Báo Giá & Chiết Khấu"
        ]),
        # Col O (15)
        ("TRẠNG THÁI CONTENT", [
            "Chưa bắt đầu", "Đang sản xuất", "Chờ duyệt", "Đã sẵn sàng", "Đang chạy ads"
        ]),
        # Col P (16)
        ("ĐỐI TƯỢNG XEM ADS", [
            "Chủ cửa hàng kim khí, điện cơ", "Chủ tiệm kim khí, VLXD",
            "Chủ cửa hàng máy công cụ, điện cơ", "Đại lý phân phối cấp 2 / cấp 3",
            "Thợ thi công công trình lớn"
        ]),
        # Col Q (17)
        ("TỈNH THÀNH / KHU VỰC TRỌNG TÂM", [
            "Đồng Nai", "Bình Dương", "Cần Thơ", "Bắc Giang", "Hải Phòng",
            "Thanh Hóa", "Nghệ An", "Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng",
            "Vĩnh Phúc", "Thái Bình", "Nam Định", "Hải Dương", "Quảng Ninh",
            "Bắc Ninh", "Thái Nguyên", "Phú Thọ", "Hưng Yên", "Hà Nam",
            "Ninh Bình", "Hà Tĩnh", "Quảng Bình", "Quảng Trị", "Thừa Thiên Huế",
            "Quảng Nam", "Quảng Ngãi", "Bình Định", "Phú Yên", "Khánh Hòa",
            "Gia Lai", "Đắk Lắk", "Lâm Đồng", "Bình Phước", "Tây Ninh",
            "Bà Rịa - Vũng Tàu", "Long An", "Tiền Giang", "Bến Tre", "Trà Vinh",
            "Vĩnh Long", "Đồng Tháp", "An Giang", "Kiên Giang", "Hậu Giang",
            "Sóc Trăng", "Bạc Liêu", "Cà Mau", "Toàn Miền Bắc", "Toàn Miền Trung",
            "Toàn Miền Nam"
        ]),
        # Col R (18)
        ("MỐC THỜI GIAN / DEADLINE", [
            "Tuần 1 - Ngày 1", "Tuần 1 - Ngày 2", "Tuần 1 - Ngày 3", "Tuần 1 - Ngày 4", "Tuần 1 - Ngày 7",
            "Tuần 2 - Ngày 2", "Tuần 2 - Ngày 4", "Tuần 2 - Ngày 5", "Tuần 2 - Ngày 7",
            "Tuần 3 - Tuần 4", "Tuần 4 - Ngày 5", "Tuần 4 - Ngày 7",
            "Hàng ngày", "Liên tục cả tháng"
        ]),
        # Col S (19)
        ("KÊNH LƯU TRỮ / BÁO CÁO", [
            "Tab CONTENT & CREATIVE FB", "Drive / Creative Folder", "Drive / Video POSM",
            "Trình quản lý Meta Ads", "Tab THEO DOI LEAD", "Báo cáo nghiệm thu dự án",
            "Zalo OA / Sổ tay CRM", "Google Drive Chung"
        ]),
        # Col T (20)
        ("YÊU CẦU MEDIA (QUAY/CHỤP)", [
            "Layout ảnh chụp tổng thể hệ sinh thái dụng cụ King Blue",
            "Clip Tứ quay bàn giao kệ POSM tại cửa hàng đối tác",
            "Thiện thiết kế mockup cuốn catalogue King Blue dày dặn",
            "Thiện làm visual cam kết không phá giá & đổi trả linh hoạt",
            "Chụp chi tiết dải máy pin Brushless 21V",
            "Video test độ bền đá cắt & đá mài King Blue",
            "Chụp quầy kệ & biển bảng nhận diện thương hiệu"
        ]),
        # Col U (21)
        ("PACING NGÂN SÁCH (ĐÁNH GIÁ)", [
            "Đang kiểm soát tốt", "Dồn ngân sách (Scale)",
            "Cắt giảm ngân sách", "Hoàn thành ngân sách"
        ]),
        # Col V (22)
        ("NHÓM GÓC TIẾP CẬN NGÂN SÁCH", [
            "Campaign 1 (Angle 1: Chiết Khấu Đại Lý)",
            "Campaign 2 (Angle 2: Hỗ Trợ Kệ POSM)",
            "Campaign 3 (Angle 3: Khám Phá Catalogue)",
            "Campaign 4 (Angle 4: Bảo Vệ Vùng Bán)",
            "Campaign Scale (Góc Tiếp Cận Win)",
            "Dự phòng phát sinh"
        ])
    ]

    ws6.row_dimensions[3].height = 24
    for idx, (head, items) in enumerate(config_cols, start=1):
        c = ws6.cell(row=3, column=idx, value=head)
        c.font = font_head
        c.fill = fill_head
        c.alignment = align_center
        c.border = border_cell
        ws6.column_dimensions[get_column_letter(idx)].width = 28

        for r_idx, item in enumerate(items, start=4):
            ci = ws6.cell(row=r_idx, column=idx, value=item)
            ci.font = font_body
            ci.border = border_cell
            ci.alignment = align_left

    # Data Validation Dropdowns Function
    def apply_dv(ws, col_letter, source_range, prompt, start_r=5, max_r=50):
        dv = DataValidation(type="list", formula1=f"='CAU HINH'!{source_range}", allow_blank=True)
        dv.error = "Vui lòng chọn giá trị hợp lệ từ danh sách!"
        dv.promptTitle = prompt
        ws.add_data_validation(dv)
        dv.add(f"{col_letter}{start_r}:{col_letter}{max_r}")

    # 1. Tab 1: TONG QUAN & KPI TEST B2B
    apply_dv(ws1, "K", "$H$4:$H$7", "Nhân sự phụ trách", 3, 3)
    apply_dv(ws1, "B", "$C$4:$C$7", "Tên chiến dịch", 13, 16)
    apply_dv(ws1, "C", "$A$4:$A$9", "Góc tiếp cận", 13, 16)

    # 2. Tab 2: QUAN LY TASK DU AN
    apply_dv(ws_task, "C", "$I$4:$I$6", "Giai đoạn dự án", 5, 25)
    apply_dv(ws_task, "G", "$H$4:$H$7", "Người phụ trách", 5, 25)
    apply_dv(ws_task, "H", "$H$4:$H$7", "Người phối hợp", 5, 25)
    apply_dv(ws_task, "I", "$J$4:$J$8", "Trạng thái task", 5, 25)
    apply_dv(ws_task, "J", "$K$4:$K$7", "Mức độ ưu tiên", 5, 25)
    apply_dv(ws_task, "K", "$R$4:$R$17", "Hạn chót / Mốc thời gian", 5, 25)
    apply_dv(ws_task, "L", "$S$4:$S$11", "Kênh lưu trữ / Báo cáo", 5, 25)

    # 3. Tab 3: CHI TIET CHIEN DICH FB ADS
    apply_dv(ws2, "O", "$H$4:$H$7", "Nhân sự vận hành", 3, 3)
    apply_dv(ws2, "C", "$C$4:$C$7", "Tên chiến dịch FB", 5, 15)
    apply_dv(ws2, "D", "$A$4:$A$9", "Góc tiếp cận", 5, 15)
    apply_dv(ws2, "E", "$D$4:$D$7", "Định dạng ads", 5, 15)
    apply_dv(ws2, "N", "$H$4:$H$7", "Người phụ trách", 5, 15)
    apply_dv(ws2, "O", "$E$4:$E$8", "Trạng thái chiến dịch", 5, 15)

    # 4. Tab 4: NGAN SACH 4 TUAN
    apply_dv(ws3, "B", "$V$4:$V$9", "Nhóm góc tiếp cận", 4, 7)
    apply_dv(ws3, "K", "$U$4:$U$7", "Đánh giá pacing ngân sách", 4, 7)

    # 5. Tab 5: CONTENT & CREATIVE FB
    apply_dv(ws4, "B", "$A$4:$A$9", "Trục thông điệp", 4, 20)
    apply_dv(ws4, "E", "$M$4:$M$9", "Định dạng visual", 4, 20)
    apply_dv(ws4, "F", "$T$4:$T$10", "Yêu cầu media quay chụp", 4, 20)
    apply_dv(ws4, "G", "$N$4:$N$8", "Kêu gọi hành động CTA", 4, 20)
    apply_dv(ws4, "H", "$P$4:$P$8", "Đối tượng xem", 4, 20)
    apply_dv(ws4, "I", "$H$4:$H$7", "Người phụ trách", 4, 20)
    apply_dv(ws4, "J", "$H$4:$H$7", "Hỗ trợ visual", 4, 20)
    apply_dv(ws4, "K", "$O$4:$O$8", "Trạng thái content", 4, 20)

    # 6. Tab 6: THEO DOI LEAD & KHAO SAT WIN
    apply_dv(ws5, "D", "$C$4:$C$7", "Chiến dịch Facebook", 5, 50)
    apply_dv(ws5, "G", "$L$4:$L$8", "Chức vụ khách hàng", 5, 50)
    apply_dv(ws5, "I", "$Q$4:$Q$54", "Tỉnh / Khu vực", 5, 50)
    apply_dv(ws5, "J", "$B$4:$B$10", "Dòng hàng tìm SP win", 5, 50)
    apply_dv(ws5, "K", "$F$4:$F$9", "Trạng thái xử lý lead", 5, 50)
    apply_dv(ws5, "L", "$H$4:$H$7", "Người tiếp nhận", 5, 50)
    apply_dv(ws5, "M", "$G$4:$G$7", "Đánh giá chất lượng lead", 5, 50)
    apply_dv(ws5, "Q", "$C$4:$C$7", "Chiến dịch FB", 5, 8)

    wb.save(XLSX_FILE)
    print(f"✅ Đã tạo file Excel Brand/Dealership Test offline: {XLSX_FILE}")
    return XLSX_FILE

def sync_to_google_drive(file_path):
    print("🔄 Đang đồng bộ cập nhật lên Google Drive...")
    if not os.path.exists(TOKEN_FILE):
        print(f"⚠️ Không tìm thấy file {TOKEN_FILE}")
        return None

    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive',
    ]

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    drive_service = build('drive', 'v3', credentials=creds)

    folder_id = "1e6BtoJ8BwmpIlJGhr_OMJND7rfuPqT_j"
    file_title = "Kế Hoạch Chạy Quảng Cáo B2B - King Blue Marketing"

    query = f"name = '{file_title}' and '{folder_id}' in parents and trashed = false"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name, webViewLink)').execute()
    items = results.get('files', [])

    media = MediaFileUpload(
        file_path,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        resumable=True
    )

    if items:
        file_id = items[0]['id']
        print(f"🔄 Đang cập nhật Google Sheet hiện có: {file_title} (ID: {file_id})...")
        updated_file = drive_service.files().update(
            fileId=file_id,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        sheet_link = updated_file.get('webViewLink')
    else:
        print(f"🚀 Tạo mới Google Sheet: {file_title}...")
        file_metadata = {
            'name': file_title,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': [folder_id]
        }
        created_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        sheet_link = created_file.get('webViewLink')

    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"sheets": {}}

    data["sheets"][file_title] = sheet_link

    with open(LINKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"🎉 Đã cập nhật xong Google Sheet: {sheet_link}")
    return sheet_link

if __name__ == "__main__":
    xlsx_path = build_excel_b2b_brand_test()
    link = sync_to_google_drive(xlsx_path)
    print(f"\n✨ HOÀN TẤT: Link Google Sheet = {link}")

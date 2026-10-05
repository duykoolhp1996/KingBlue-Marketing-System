import os
import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "Bao_Cao_Cong_Viec_KingBlue.xlsx")

# Danh sách 9 nhân sự phòng Marketing King Blue
PERSONNEL_LIST = [
    {
        "id": "1",
        "tab_name": "Hoai Thuong - Content",
        "name": "Võ Thị Hoài Thương",
        "role": "Content Marketing & SEO Fanpage/Website",
        "group": "Content",
        "manager": "Marketing Manager",
        "reports": [
            {
                "date": "05/10/2026",
                "time": "17:15",
                "res": "• Nhiệm vụ 1: Đề xuất hàng mẫu, liên hệ gặp KH (Lên danh sách 5 mã máy pin chủ lực, hẹn lịch 3 đại lý TP.HCM)\n• Nhiệm vụ 2: Tổng hợp thông tin chính sách, sản phẩm gửi KHM (Gửi catalogue & bảng chiết khấu)\n• Nhiệm vụ 3: Đi công tác: Đồng Nai, HCM (Khảo sát mặt bằng 2 đại lý Biên Hòa)",
                "diff": "• Đại lý Đồng Nai mặt bằng hẹp, phân vân giữa kệ 2 tầng và 3 tầng.",
                "lesson": "• Đề xuất Design (Thiện) hỗ trợ dựng thêm mockup kệ module đứng ngang 60cm.",
                "plan": "• Viết bài đăng Fanpage King Blue Tools giới thiệu máy mài góc pin 21V.\n• Follow chốt phương án trưng bày với 3 đại lý.",
                "link": "https://kingblue.vn/san-pham",
                "status": "Đúng hạn",
                "feedback": "Đã duyệt. Phương án kệ 60cm rất hợp lý."
            },
            {
                "date": "04/10/2026",
                "time": "17:20",
                "res": "• Nhiệm vụ 1: Viết 02 bài SEO website kingblue.vn về máy siết bulong không chổi than.\n• Nhiệm vụ 2: Lên lịch content Fanpage tuần 41.",
                "diff": "• Không có.",
                "lesson": "• Bài viết có bảng thông số kỹ thuật chi tiết giữ chân người đọc lâu hơn 35%.",
                "plan": "• Đi thị trường Đồng Nai khảo sát đại lý.",
                "link": "https://kingblue.vn/tin-tuc",
                "status": "Đúng hạn",
                "feedback": "Bài SEO chuẩn SEO tốt, duyệt đăng web."
            },
            {
                "date": "03/10/2026",
                "time": "17:10",
                "res": "• Nhiệm vụ 1: Đề xuất danh mục hàng mẫu gửi đối tác mới.\n• Nhiệm vụ 2: Rà soát từ khóa ngành dụng cụ điện cầm tay tháng 10.",
                "diff": "• Thiếu catalogue bản in gửi kèm hàng mẫu.",
                "lesson": "• Đã gửi file PDF tạm thời cho đại lý xem trước.",
                "plan": "• Chuẩn bị lịch đi công tác Đồng Nai.",
                "link": "-",
                "status": "Đúng hạn",
                "feedback": "Đã in bổ sung 50 cuốn catalogue gửi bạn."
            }
        ]
    },
    {
        "id": "2",
        "tab_name": "Kieu Thuong - Content",
        "name": "Kiều Thương",
        "role": "Content Video & Hợp Tác KOC/Reviewer",
        "group": "Content",
        "manager": "Marketing Manager",
        "reports": [
            {
                "date": "05/10/2026",
                "time": "17:25",
                "res": "• Nhiệm vụ 1: Hoàn thành kịch bản phân cảnh chi tiết video test máy khoan KM18QE.\n• Nhiệm vụ 2: Liên hệ và chốt lịch gửi máy test cho 2 KOC kênh cơ khí chế tạo.",
                "diff": "• Cần phôi sắt V dày 5mm và gạch mác cao để test lực đập thực tế.",
                "lesson": "• Cần mượn máy đo lực siết Nm để video có chỉ số kỹ thuật khách quan.",
                "plan": "• 08h30 sáng phối hợp Tứ Media bấm máy quay test máy khoan pin.\n• Lên outline kịch bản video 'Cách phân biệt pin King Blue chính hãng'.",
                "link": "https://youtube.com/@kingbluetools",
                "status": "Đúng hạn",
                "feedback": "Kịch bản chuẩn bị kỹ lưỡng, sáng mai quay đúng tiến độ."
            }
        ]
    },
    {
        "id": "3",
        "tab_name": "Thuy Thuong - Content",
        "name": "Thụy Thương",
        "role": "Trade Marketing & Chính Sách Điểm Bán",
        "group": "Content",
        "manager": "Marketing Manager",
        "reports": [
            {
                "date": "05/10/2026",
                "time": "17:18",
                "res": "• Nhiệm vụ 1: Hoàn thiện tài liệu One-sheet hướng dẫn kích hoạt bảo hành điện tử King Blue.\n• Nhiệm vụ 2: Rà soát danh sách 8 đại lý miền Trung đăng ký biển hiệu alu King Blue.",
                "diff": "• 02 đại lý gửi ảnh hiện trạng bị mờ, đo đạc thiếu chiều cao mặt tiền.",
                "lesson": "• Đã ban hành form chuẩn hóa quy cách đo biển hiệu cho Sales gửi đại lý.",
                "plan": "• Bàn giao kích thước 8 biển hiệu cho Thiện Design dựng bản vẽ thi công.\n• Viết bài hướng dẫn kích hoạt bảo hành điện tử trên web.",
                "link": "https://kingblue.vn/bao-hanh",
                "status": "Đúng hạn",
                "feedback": "Form đo đạc mới rất thực tế, Sales áp dụng ngay."
            }
        ]
    },
    {
        "id": "4",
        "tab_name": "Thien - Design",
        "name": "Thiện",
        "role": "Graphic Designer (2D/3D, POSM & Banner)",
        "group": "Design",
        "manager": "Marketing Manager",
        "reports": [
            {
                "date": "05/10/2026",
                "time": "17:30",
                "res": "• Nhiệm vụ 1: Thiết kế 3D quầy kệ đứng module 60cm tối ưu không gian đại lý Đồng Nai.\n• Nhiệm vụ 2: Thiết kế bộ 6 banner Flash Sale ngày đôi cho Shopee Mall và Lazada King Blue.",
                "diff": "• Chờ ảnh retouched nền trắng máy cưa kiếm từ Tứ Media để chốt banner còn lại.",
                "lesson": "• Tạo sẵn Master Library linh kiện & logo King Blue tăng tốc độ thiết kế lên 40%.",
                "plan": "• Lên maket 8 biển hiệu alu đại lý theo kích thước Thụy Thương bàn giao.\n• Thiết kế thumbnail chuẩn cho chuỗi video YouTube Review.",
                "link": "https://drive.google.com/drive/folders/1e6BtoJ8BwmpIlJGhr_OMJND7rfuPqT_j",
                "status": "Đúng hạn",
                "feedback": "Mẫu kệ 60cm thiết kế rất đẹp và sang trọng."
            }
        ]
    },
    {
        "id": "5",
        "tab_name": "Tu - Media",
        "name": "Tứ",
        "role": "Media / Photographer (Hình Ảnh, Video & User CRM)",
        "group": "Media",
        "manager": "Marketing Manager",
        "reports": [
            {
                "date": "05/10/2026",
                "time": "17:28",
                "res": "• Nhiệm vụ 1: Chụp 15 góc ảnh chi tiết bộ thùng đồ nghề KHD4233, retouched nền trắng 8 ảnh.\n• Nhiệm vụ 2: Setup thiết bị, ánh sáng phòng quay 4K cho buổi test máy khoan sáng mai.",
                "diff": "• Chờ Admin cấp tài khoản User Photographer trên CRM để up ảnh trực tiếp cho Sales.",
                "lesson": "• Cần chuẩn bị trước phôi bê tông và đá mài từ hôm nay để sáng mai quay đúng giờ.",
                "plan": "• 08h30 - 11h30: Quay test thực tế máy khoan KM18QE cùng Kiều Thương.\n• Buổi chiều: Dựng thô clip ngắn Reels/TikTok trình Marketing Manager duyệt.",
                "link": "https://tiktok.com/@kingbluetools",
                "status": "Đúng hạn",
                "feedback": "Admin sẽ cấp tài khoản CRM Photographer trong chiều nay."
            }
        ]
    },
    {
        "id": "6",
        "tab_name": "Thuc - San TMDT",
        "name": "Thức",
        "role": "Vận Hành Sàn TMĐT (Shopee & Lazada)",
        "group": "Sàn TMĐT",
        "manager": "Marketing Manager",
        "reports": [
            {
                "date": "05/10/2026",
                "time": "17:20",
                "res": "• Nhiệm vụ 1: Cài đặt chiến dịch Mega Sale trên Shopee Mall & Lazada (Voucher, Freeship).\n• Nhiệm vụ 2: Tối ưu SEO tiêu đề và bộ từ khóa cho 15 mã máy pin chủ lực.",
                "diff": "• Mã máy cưa xích mini pin đang tạm hết hàng trên sàn, phải tạm ẩn link.",
                "lesson": "• Khung giờ 12h và 20h có tỷ lệ click mua dụng cụ điện cao nhất, tập trung đẩy Flash Sale.",
                "plan": "• Rà soát giá niêm yết và tồn kho trước giờ chạy Sale.\n• Phối hợp kho MN (Hùng) chuẩn bị vật tư bọc hàng xốp bóng khí.",
                "link": "https://shopee.vn/kingblue",
                "status": "Đúng hạn",
                "feedback": "Đã ghi nhận, kho sẽ ưu tiên xuất máy mài pin thay thế."
            }
        ]
    },
    {
        "id": "7",
        "tab_name": "Ngan - San TMDT",
        "name": "Ngân",
        "role": "CSKH & Quản Trị Gian Hàng TikTok Shop",
        "group": "Sàn TMĐT",
        "manager": "Marketing Manager",
        "reports": [
            {
                "date": "05/10/2026",
                "time": "17:10",
                "res": "• Nhiệm vụ 1: Trực chat tư vấn 52 lượt khách hàng, chốt thành công 18 đơn máy khoan pin.\n• Nhiệm vụ 2: Xử lý 03 yêu cầu bảo hành, hướng dẫn khách kích hoạt bảo hành điện tử 100%.",
                "diff": "• Nhiều khách chưa phân biệt được dòng chân pin chung và chân pin riêng King Blue.",
                "lesson": "• Cần thêm ảnh infographic giải thích chân pin trên ảnh sản phẩm để khách tự tra cứu.",
                "plan": "• Trực chat ca sáng và chốt đơn đặt sớm cho đợt Sale ngày đôi.\n• Gửi voucher tri ân cho 50 khách hàng thân thiết mua máy pin tháng trước.",
                "link": "https://tiktok.com/@kingbluetools",
                "status": "Đúng hạn",
                "feedback": "Tỷ lệ chốt đơn qua chat rất tốt, tiếp tục phát huy."
            }
        ]
    },
    {
        "id": "8",
        "tab_name": "Hung - Kho MN",
        "name": "Hùng",
        "role": "Đóng Gói & Kho Vận Hàng Hóa Miền Nam",
        "group": "Đóng gói kho",
        "manager": "Marketing Manager",
        "reports": [
            {
                "date": "05/10/2026",
                "time": "17:35",
                "res": "• Nhiệm vụ 1: Đóng gói và bàn giao an toàn 145 đơn hàng TMĐT cho các đơn vị bưu tá.\n• Nhiệm vụ 2: Kiểm tra test pin và dán tem niêm phong 04 kiện hàng mẫu gửi đại lý Đồng Nai.",
                "diff": "• Shipper đến lấy hàng trễ 30 phút so với lịch hẹn buổi chiều.",
                "lesson": "• Cần dán thêm tem cảnh báo 'Hàng chính xác / Dễ vỡ' để bên vận chuyển nâng đỡ cẩn thận.",
                "plan": "• Chuẩn bị sẵn 200 vỏ thùng carton cỡ vừa phục vụ đóng hàng Mega Sale.\n• Sắp xếp lại kệ hàng phụ kiện mũi khoan theo đúng sơ đồ kho.",
                "link": "-",
                "status": "Đúng hạn",
                "feedback": "Kiện hàng mẫu gửi đi đóng gói rất chuẩn, đã bàn giao xe thành công."
            }
        ]
    },
    {
        "id": "9",
        "tab_name": "Hung - Kho MB",
        "name": "Hùng Miền Bắc",
        "role": "Đóng Gói & Kho Vận Chi Nhánh Hà Nội",
        "group": "Đóng gói kho",
        "manager": "Marketing Manager",
        "reports": [
            {
                "date": "05/10/2026",
                "time": "17:25",
                "res": "• Nhiệm vụ 1: Đóng gói 82 đơn hàng phía Bắc an toàn, giao đơn vị vận chuyển trước 16h30.\n• Nhiệm vụ 2: Kiểm kê thực tế hàng tồn kho máy pin và lưỡi cắt King Blue tại kho Hà Nội.",
                "diff": "• Khối pin 21V 4.0Ah tại kho Bắc chỉ còn 12 cục, nguy cơ thiếu hàng đợt Sale tới.",
                "lesson": "• Cần thông báo trước 5 ngày khi lượng tồn kho dưới ngưỡng an toàn.",
                "plan": "• Phối hợp nhận lô hàng 50 pin điều chuyển từ kho Tổng Miền Nam ra.\n• Đóng gói và xuất đơn trong ngày.",
                "link": "-",
                "status": "Đúng hạn",
                "feedback": "Marketing Manager đã ký lệnh điều chuyển 50 pin ra kho Hà Nội."
            }
        ]
    }
]

def build_workbook():
    wb = openpyxl.Workbook()
    
    # COLORS
    c_primary = "1A365D"       # Dark Royal Blue
    c_accent = "2B6CB0"        # Accent Blue
    c_light_blue = "EBF8FF"    # Light Blue
    c_header_gray = "EDF2F7"
    c_white = "FFFFFF"
    c_border = "CBD5E0"
    
    font_title = Font(name="Calibri", size=15, bold=True, color=c_white)
    font_section = Font(name="Calibri", size=12, bold=True, color=c_primary)
    font_header = Font(name="Calibri", size=10, bold=True, color=c_white)
    font_bold = Font(name="Calibri", size=10, bold=True)
    font_regular = Font(name="Calibri", size=10)
    font_small = Font(name="Calibri", size=9, italic=True, color="718096")
    font_kpi_num = Font(name="Calibri", size=16, bold=True, color=c_primary)
    font_kpi_label = Font(name="Calibri", size=9, bold=True, color="4A5568")

    fill_primary = PatternFill(start_color=c_primary, end_color=c_primary, fill_type="solid")
    fill_accent = PatternFill(start_color=c_accent, end_color=c_accent, fill_type="solid")
    fill_kpi = PatternFill(start_color=c_light_blue, end_color=c_light_blue, fill_type="solid")
    fill_sub = PatternFill(start_color=c_header_gray, end_color=c_header_gray, fill_type="solid")
    fill_done = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")
    fill_diff = PatternFill(start_color="FEEBC8", end_color="FEEBC8", fill_type="solid") # light orange

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
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
    align_top_center = Alignment(horizontal="center", vertical="top", wrap_text=True)

    # =========================================================
    # TAB 1: TỔNG HỢP HÀNG NGÀY (MASTER CONSOLIDATED SHEET)
    # =========================================================
    ws_master = wb.active
    ws_master.title = "TONG HOP HANG NGAY"
    ws_master.views.sheetView[0].showGridLines = True

    ws_master.merge_cells("A1:K2")
    ws_master["A1"] = "BẢNG TỔNG HỢP BÁO CÁO CÔNG VIỆC HÀNG NGÀY - PHÒNG MARKETING KING BLUE"
    ws_master["A1"].font = font_title
    ws_master["A1"].fill = fill_primary
    ws_master["A1"].alignment = align_center

    # KPI Banner
    kpi_cards = [
        ("B4:C4", "B5:C5", "TỔNG NHÂN SỰ", "9 Người"),
        ("D4:E4", "D5:E5", "ĐÃ NỘP HÔM NAY", "9 / 9 (100%)"),
        ("F4:G4", "F5:G5", "VƯỚNG MẮC PHÁT SINH", "3 Vấn đề"),
        ("H4:I4", "H5:I5", "TÌNH TRẠNG NỘP", "100% Đúng hạn"),
        ("J4:K4", "J5:K5", "TRƯỞNG PHÒNG", "Marketing Manager"),
    ]
    for top_range, bot_range, label, val in kpi_cards:
        ws_master.merge_cells(top_range)
        ws_master.merge_cells(bot_range)
        top_cell = ws_master[top_range.split(":")[0]]
        bot_cell = ws_master[bot_range.split(":")[0]]
        top_cell.value = label
        top_cell.font = font_kpi_label
        top_cell.fill = fill_sub
        top_cell.alignment = align_center
        bot_cell.value = val
        bot_cell.font = font_kpi_num
        bot_cell.fill = fill_kpi
        bot_cell.alignment = align_center
        for row in ws_master[f"{top_range.split(':')[0]}:{bot_range.split(':')[1]}"]:
            for cell in row:
                cell.border = kpi_border

    # Headers for Master Table
    headers_master = [
        "STT", "Nhân Sự", "Bộ Phận", "Vị Trí Chuyên Môn",
        "1️⃣ KẾT QUẢ ĐẠT ĐƯỢC HÔM NAY",
        "2️⃣ KHÓ KHĂN / VƯỚNG MẮC",
        "3️⃣ BÀI HỌC / ĐỀ XUẤT",
        "4️⃣ KẾ HOẠCH NGÀY MAI",
        "Giờ Nộp", "Tình Trạng", "Marketing Manager Phản Hồi"
    ]
    ws_master.row_dimensions[7].height = 28
    for col_idx, h_text in enumerate(headers_master, start=1):
        c = ws_master.cell(row=7, column=col_idx, value=h_text)
        c.font = font_header
        c.fill = fill_accent
        c.alignment = align_center
        c.border = thin_border

    # Fill Master Rows (Latest report of each of the 9 personnel)
    row_cur = 8
    for p in PERSONNEL_LIST:
        rep = p["reports"][0]
        ws_master.row_dimensions[row_cur].height = 70
        vals = [
            int(p["id"]),
            p["name"],
            p["group"],
            p["role"],
            rep["res"],
            rep["diff"],
            rep["lesson"],
            rep["plan"],
            rep["time"],
            rep["status"],
            rep["feedback"]
        ]
        for c_idx, v in enumerate(vals, start=1):
            cell = ws_master.cell(row=row_cur, column=c_idx, value=v)
            cell.font = font_regular
            cell.border = thin_border
            if c_idx in [1, 9, 10]:
                cell.alignment = align_top_center
            else:
                cell.alignment = align_top_left

            # Highlight difficulties
            if c_idx == 6 and v and "Không có" not in v:
                cell.fill = fill_diff
            if c_idx == 10:
                cell.fill = fill_done
                cell.font = font_bold
        row_cur += 1

    # Column widths for Master
    col_widths_master = {
        'A': 6, 'B': 20, 'C': 14, 'D': 25, 'E': 42,
        'F': 32, 'G': 32, 'H': 35, 'I': 10, 'J': 13, 'K': 30
    }
    for col_letter, width in col_widths_master.items():
        ws_master.column_dimensions[col_letter].width = width

    # =========================================================
    # 9 DEDICATED TABS: MỖI NHÂN SỰ 1 SHEET
    # =========================================================
    headers_individual = [
        "STT", "Ngày Báo Cáo", "Giờ Nộp",
        "1️⃣ KẾT QUẢ ĐẠT ĐƯỢC (Nhiệm vụ 1, 2, 3...)",
        "2️⃣ KHÓ KHĂN / VƯỚNG MẮC",
        "3️⃣ BÀI HỌC KINH NGHIỆM / ĐỀ XUẤT",
        "4️⃣ KẾ HOẠCH CÔNG VIỆC NGÀY MAI",
        "Link Minh Chứng", "Tình Trạng", "Marketing Manager Phê Duyệt & Phản Hồi"
    ]

    for p in PERSONNEL_LIST:
        ws_p = wb.create_sheet(title=p["tab_name"])
        ws_p.views.sheetView[0].showGridLines = True

        # Sheet Header Info
        ws_p.merge_cells("A1:J2")
        ws_p["A1"] = f"NHẬT KÝ BÁO CÁO CÔNG VIỆC HÀNG NGÀY - {p['name'].upper()}"
        ws_p["A1"].font = font_title
        ws_p["A1"].fill = fill_primary
        ws_p["A1"].alignment = align_center

        # Metadata banner
        ws_p.merge_cells("A3:B3")
        ws_p["A3"] = "Họ và Tên:"
        ws_p["A3"].font = font_bold
        ws_p.merge_cells("C3:D3")
        ws_p["C3"] = p["name"]
        ws_p["C3"].font = font_bold

        ws_p.merge_cells("E3:F3")
        ws_p["E3"] = "Vị trí chuyên môn:"
        ws_p["E3"].font = font_bold
        ws_p.merge_cells("G3:H3")
        ws_p["G3"] = p["role"]

        ws_p["I3"] = "Quản lý duyệt:"
        ws_p["I3"].font = font_bold
        ws_p["J3"] = p["manager"]
        ws_p["J3"].font = font_bold

        for row in ws_p["A3:J3"]:
            for c in row:
                c.fill = fill_sub
                c.border = thin_border

        # Table Headers
        ws_p.row_dimensions[5].height = 26
        for col_idx, h_text in enumerate(headers_individual, start=1):
            c = ws_p.cell(row=5, column=col_idx, value=h_text)
            c.font = font_header
            c.fill = fill_accent
            c.alignment = align_center
            c.border = thin_border

        # Populate user's reports history
        r_idx = 6
        for stt, rep in enumerate(p["reports"], start=1):
            ws_p.row_dimensions[r_idx].height = 75
            row_data = [
                stt,
                rep["date"],
                rep["time"],
                rep["res"],
                rep["diff"],
                rep["lesson"],
                rep["plan"],
                rep["link"],
                rep["status"],
                rep["feedback"]
            ]
            for c_idx, val in enumerate(row_data, start=1):
                cell = ws_p.cell(row=r_idx, column=c_idx, value=val)
                cell.font = font_regular
                cell.border = thin_border
                if c_idx in [1, 2, 3, 9]:
                    cell.alignment = align_top_center
                else:
                    cell.alignment = align_top_left

                if c_idx == 5 and val and "Không có" not in val:
                    cell.fill = fill_diff
                if c_idx == 9:
                    cell.fill = fill_done
                    cell.font = font_bold

            r_idx += 1

        # Add 10 blank template rows for future entries
        for blank_stt in range(len(p["reports"]) + 1, len(p["reports"]) + 11):
            ws_p.row_dimensions[r_idx].height = 30
            ws_p.cell(row=r_idx, column=1, value=blank_stt).alignment = align_center
            for c_idx in range(1, 11):
                cell = ws_p.cell(row=r_idx, column=c_idx)
                cell.border = thin_border
            r_idx += 1

        # Column widths for individual tab
        col_widths_ind = {
            'A': 6, 'B': 13, 'C': 10, 'D': 44, 'E': 34,
            'F': 34, 'G': 36, 'H': 20, 'I': 13, 'J': 32
        }
        for col_letter, width in col_widths_ind.items():
            ws_p.column_dimensions[col_letter].width = width

    # =========================================================
    # TAB 11: BÁO CÁO TUẦN (WEEKLY REPORT)
    # =========================================================
    ws_w = wb.create_sheet(title="BAO CAO TUAN")
    ws_w.views.sheetView[0].showGridLines = True
    ws_w.merge_cells("A1:H2")
    ws_w["A1"] = "BÁO CÁO TỔNG KẾT TUẦN - PHÒNG MARKETING KING BLUE"
    ws_w["A1"].font = font_title
    ws_w["A1"].fill = fill_primary
    ws_w["A1"].alignment = align_center

    headers_w = [
        "STT", "Họ và Tên", "Vị Trí", "Mục Tiêu Tuần",
        "Kết Quả Đạt Được (% Hoàn thành)", "Vấn Đề Tồn Đọng", "Kế Hoạch Tuần Tới", "Marketing Manager Đánh Giá"
    ]
    ws_w.row_dimensions[4].height = 25
    for col_idx, h_text in enumerate(headers_w, start=1):
        c = ws_w.cell(row=4, column=col_idx, value=h_text)
        c.font = font_header
        c.fill = fill_accent
        c.alignment = align_center
        c.border = thin_border

    sample_weekly = [
        (1, "Võ Thị Hoài Thương", "Content MKT & SEO", "Khảo sát đại lý Đồng Nai, lên plan SEO tháng 10", "100% Hoàn thành", "Cần mẫu kệ module hẹp", "Triển khai gửi hàng mẫu 3 đại lý", "Xuất sắc"),
        (2, "Kiều Thương", "Content Video & KOC", "Kịch bản test máy khoan, liên hệ 2 KOC", "100% Hoàn thành", "Cần phôi thép dày test tải", "Bấm máy quay video review", "Tốt"),
        (3, "Thụy Thương", "Trade Marketing", "Tài liệu bảo hành điện tử, duyệt biển hiệu", "95% Hoàn thành", "Đại lý chụp ảnh mờ", "Hoàn thiện maket 8 biển alu", "Tốt"),
        (4, "Thiện", "Graphic Designer", "Thiết kế quầy kệ 3D, banner Flash Sale", "100% Hoàn thành", "Chờ ảnh retouched", "Lên maket 8 biển đại lý", "Xuất sắc"),
        (5, "Tứ", "Media / Photographer", "Chụp bộ KHD4233, setup phòng test máy", "100% Hoàn thành", "Cần quyền User CRM", "Quay test máy KM18QE", "Tốt"),
        (6, "Thức", "Vận Hành Sàn TMĐT", "Setup Mega Sale Shopee & Lazada", "100% Hoàn thành", "Hết hàng cưa xích mini", "Theo dõi giờ vàng Flash Sale", "Tốt"),
        (7, "Ngân", "CSKH & TikTok Shop", "Trực chat, xử lý đổi trả bảo hành", "100% Hoàn thành", "Giải thích chân pin", "Chăm sóc khách hàng cũ", "Tốt"),
        (8, "Hùng", "Đóng Gói Kho MN", "Đóng gói đơn TMĐT, gửi hàng mẫu đại lý", "100% Hoàn thành", "Shipper trễ chuyến", "Chuẩn bị 200 thùng Mega Sale", "Tốt"),
        (9, "Hùng Miền Bắc", "Đóng Gói Kho MB", "Đóng gói đơn MB, kiểm kê kho Hà Nội", "95% Hoàn thành", "Tồn pin 4.0Ah thấp", "Nhận 50 pin chuyển từ kho Tổng", "Tốt"),
    ]
    for idx, r_data in enumerate(sample_weekly, start=5):
        ws_w.row_dimensions[idx].height = 40
        for c_idx, val in enumerate(r_data, start=1):
            cell = ws_w.cell(row=idx, column=c_idx, value=val)
            cell.font = font_regular
            cell.border = thin_border
            if c_idx in [1, 5, 8]:
                cell.alignment = align_top_center
                if c_idx == 5:
                    cell.font = font_bold
                    cell.fill = fill_done
            else:
                cell.alignment = align_top_left

    col_widths_w = {'A': 6, 'B': 22, 'C': 22, 'D': 35, 'E': 20, 'F': 25, 'G': 32, 'H': 25}
    for col_letter, width in col_widths_w.items():
        ws_w.column_dimensions[col_letter].width = width

    # Save local Excel file
    wb.save(FILE_PATH)
    print(f"✅ Đã lưu file Excel mới với {len(wb.sheetnames)} sheets tại: {FILE_PATH}")
    print(f"📋 Danh sách các Sheet: {wb.sheetnames}")

if __name__ == "__main__":
    build_workbook()

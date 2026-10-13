# 🏢 King Blue Marketing - Hệ Thống Báo Cáo Công Việc Hàng Ngày & Phân Quyền CRM

> **Hệ thống Quản lý Tiến độ, Tự động hóa Báo cáo Công việc & Đồng bộ Google Sheets hai chiều cho Phòng Marketing Công ty King Blue.**  
> Trợ lý ảo AI vận hành: 🐱 **Xu Xu**

---

## 📌 Giới Thiệu Tổng Quan

Hệ thống được xây dựng nhằm giải quyết bài toán quản trị tiến độ và báo cáo công việc hàng ngày của phòng Marketing King Blue:
1. **Dành cho Nhân sự (Users)**:
   - Đăng nhập bảo mật siêu đơn giản bằng **Mật khẩu / Mã PIN 4 số** (không cần nhập ID).
   - Tự động ghi nhận **thời gian bấm nút Gửi** chính xác đến từng giây (`HH:MM:SS`) và tự động kiểm tra hạn chót (**17:30** mỗi ngày).
   - Chỉ cần điền báo cáo trên Website — **không cần copy/paste gửi Zalo thủ công**.
   - Mỗi ngày nếu cập nhật nhiều lần, hệ thống luôn **tự động giữ bản gửi mới nhất**.
   - Modal Popup chúc mừng hoàn thành nhiệm vụ ngay khi gửi.

2. **Dành cho Marketing Manager (Admin)**:
   - Theo dõi toàn bộ 9 nhân sự tập trung trên một giao diện thống nhất.
   - **Bộ chọn ngày thông minh (Date Picker)**: Xem lại tiến độ của bất kỳ ngày nào trong quá khứ hoặc hiện tại.
   - **Chế độ xem kép (Dual Views)**:
     - 🗂️ **Thẻ Công Việc Hôm Nay**: Thiết kế trực quan các đầu việc hoàn thành, cảnh báo nổi bật các vướng mắc cần giải quyết lúc 17h00 chiều.
     - 📊 **Bảng Chi Tiết (Table View)**: Bảng dữ liệu chuẩn 10 cột rà soát nhanh.
   - **Xuất Báo Cáo 1-Click**: Tự động tổng hợp và định dạng văn bản chuẩn để sao chép gửi Ban Giám Đốc.
   - Gửi phản hồi & chỉ đạo công việc trực tiếp đến từng nhân sự.

---

## 👥 Danh Sách Phân Quyền & Tài Khoản Nội Bộ

Hệ thống phân quyền chuẩn CRM, toàn bộ nhân sự Marketing, Sàn TMĐT, Kho Vận và Photographer đều là các User độc lập do Admin quản lý:

| STT | Họ và Tên | Vai Trò Chuyên Môn | Bộ Phận / Brand | Mã PIN | Quyền CRM | Tab Google Sheets |
|:---:|:---|:---|:---:|:---:|:---:|:---|
| 👑 | **Marketing Manager** | Trưởng Phòng Marketing | Ban Quản Lý | `8888` | **Admin / Quản Trị** | `BAO CAO HOM NAY` |
| 1 | **Kiều Thương** | Quản lý Brand King Blue (Content, Video, KOC & Ads B2B) | **Brand King Blue** | `1002` | Brand Manager King Blue | `Kieu Thuong - King Blue` |
| 2 | **Võ Thị Hoài Thương** | Phụ trách Brand Ckô Store (SEO, Website & Chiến dịch Ecom) | **Brand CKO** | `1001` | Brand CKO Leader | `Hoai Thuong - CKO` |
| 3 | **Thương Thương** | Phụ trách Brand Ckô Store (Social, Trade MKT & Review) | **Brand CKO** | `1003` | Brand CKO Specialist | `Thuong Thuong - CKO` |
| 4 | **Thiện** | Graphic Designer (2D/3D, POSM & Banner) | Shared Service (Design) | `1004` | User | `Thien - Design` |
| 5 | **Tứ** | Media / Photographer (Hình Ảnh & User CRM) | Shared Service (Media) | `1005` | User | `Tu - Media` |
| 6 | **Thức** | Vận Hành Sàn TMĐT (Shopee & Lazada) | Shared Service (Sàn TMĐT) | `1006` | User | `Thuc - San TMDT` |
| 7 | **Ngân** | CSKH & Quản Trị Gian Hàng TikTok Shop | Shared Service (Sàn TMĐT) | `1007` | User | `Ngan - San TMDT` |
| 8 | **Hùng** | Đóng Gói & Kho Vận Hàng Hóa Miền Nam | Shared Service (Kho vận) | `1008` | User | `Hung - Kho MN` |
| 9 | **Hùng Miền Bắc** | Đóng Gói & Kho Vận Chi Nhánh Hà Nội | Shared Service (Kho vận) | `1009` | User | `Hung - Kho MB` |

---

## 🏗️ Cấu Trúc Hệ Thống & Google Sheets

- **Lark Sheet (Trang Tính Trực Tuyến)**:
  - 📗 **[Báo Cáo Tổng Quan & Phân Bổ Brand - King Blue (Lark Sheet)](https://ijphpnip01ra.jp.larksuite.com/sheets/BXOjs1mJ5hDXwltkM2kj2NuHpkb)**: Trang tính spreadsheet chuẩn gồm 3 tab (*1. Tổng Quan & Đánh Giá*, *2. Phân Công Brand & Nhân Sự*, *3. Kế Hoạch & Giao Việc Tuần*).
- **Lark Base (Cơ Sở Dữ Liệu Trực Tuyến)**:
  - 📊 **[Báo Cáo Bitable - King Blue (Lark Base)](https://ijphpnip01ra.jp.larksuite.com/base/NsOibhWx1aECklsG0r3jGYrTpuh)**: Gồm 3 bảng dữ liệu đa chiều.
- **File Google Sheets Trực Tuyến**:
  - `BAO CAO HOM NAY` (Sheet 1 - Master Dashboard): Tự động nhận diện `=TODAY()`, tích hợp lịch Date Picker nhấp đúp chọn ngày, công thức `XLOOKUP` kéo việc của 9 nhân sự.
  - 9 Sheet cá nhân riêng biệt cho 9 bạn nhân sự lưu lịch sử báo cáo.
  - `BAO CAO TUAN`: Sheet tổng hợp KPI và tiến độ hàng tuần.
- **Dashboard Báo Cáo Chuyên Sâu**:
  - 🎵 **[Dashboard Báo Cáo Hiệu Quả TikTok Cko Store (Q3/2026)](file:///Users/Admin/Documents/KIng%20BLue/dashboard_tiktok_cko.html)** (`dashboard_tiktok_cko.html`): Phân tích toàn diện 68 video, 173K+ views, tỷ lệ tương tác ER, biểu đồ tăng trưởng, top viral & kế hoạch nội dung Tháng 11.
- **File Excel Báo Cáo Offline**:
  - [Bao_Cao_Tong_Quan_Va_Phan_Bo_Brand_KingBlue.xlsx](file:///Users/Admin/Documents/KIng%20BLue/Bao_Cao_Tong_Quan_Va_Phan_Bo_Brand_KingBlue.xlsx)
  - `Bao_Cao_Cong_Viec_KingBlue.xlsx` (Cấu trúc 11 sheet đồng bộ chuẩn).
  - `cko_tiktok.xlsx` (Dữ liệu gốc 68 video TikTok Cko Store Quý 3).

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Local

### 1. Yêu cầu môi trường
- Python 3.9+
- Trình duyệt Chrome / Safari / Edge

### 2. Cài đặt thư viện cần thiết (nếu đồng bộ Google Sheets)
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib openpyxl
```

### 3. Khởi động Web Server nội bộ
```bash
python3 server.py
```
Server sẽ chạy tại: **`http://localhost:8080`**

### 4. Truy cập giao diện các ứng dụng
1. 📋 **App Quản Lý Công Việc & Tiến Độ (Database Google Sheets 2 Chiều)**:  
   👉 **[http://localhost:8080/quan_ly_cong_viec.html](http://localhost:8080/quan_ly_cong_viec.html)**  
   - 4 Chế độ xem: **Kanban Board**, **Danh Sách Chi Tiết (Table)**, **Dashboard & KPI Analytics**, **Hạn Chót Focus (Deadline)**.
   - Kết nối trực tiếp Google Sheet: `Quản Lý Công Việc - King Blue Marketing` (ID: `1CmcmBFP4jjdV1jrnNNWwXkc1foxa4j6asaOhI0qg7u8`).
   - Hỗ trợ đầy đủ: Tạo việc mới (+), Kéo/chuyển trạng thái, Cập nhật % tiến độ, Lọc "Việc của tôi".

2. 📊 **Hệ Thống Báo Cáo Công Việc Hàng Ngày (17:30)**:  
   👉 **[http://localhost:8080/website_tong_hop_bao_cao.html](http://localhost:8080/website_tong_hop_bao_cao.html)**  
   - Dành cho nộp báo cáo Standup hàng ngày và duyệt báo cáo chiều.

3. 🗂️ **Marketing Hub - Đầu Mối Thông Tin Toàn Bộ Phòng MKT**:  
   👉 **[http://localhost:8080/marketing_hub.html](http://localhost:8080/marketing_hub.html)**  
   - Tổng hợp nguyên bản 20 liên kết vận hành (Kế hoạch, Bảng chấm công, Order Media/Video, Drive KingBlue/CKO, Bảng sỉ lẻ, KOL, P&L sàn, Tồn kho Ecom, SOP Quy trình).
   - Tích hợp Live Search, bộ lọc loại file (Sheets / Drive / Console), chế độ xem Thẻ (Cards) & Bảng nguyên bản (Table).

---

---

## 🆕 Google Sheet Quản Lý Công Việc — Mỗi Người 1 Tab + 1 Tab Tổng Hợp

Script `tao_sheet_cong_viec_moi.py` tạo một Google Spreadsheet gồm **12 tab**:

| Nhóm | Tab |
|:---|:---|
| **10 tab cá nhân** | `Marketing Manager` · `Hoai Thuong` · `Kieu Thuong` · `Thuy Thuong` · `Thien` · `Tu` · `Thuc` · `Ngan` · `Hung MN` · `Hung MB` |
| **Tab tổng hợp** | `TONG HOP` — tự động gộp công việc của **tất cả** mọi người |
| **Tab cấu hình** | `CAU HINH` — danh mục nuôi dropdown (trạng thái, ưu tiên, nhóm việc, người phối hợp) |

### Cơ chế tự động

- **Trong mỗi tab cá nhân** (14 cột, tiêu đề dòng 4, dữ liệu từ dòng 5):
  - `STT` tự đánh số theo số dòng có dữ liệu.
  - `Người thực hiện` tự điền sẵn tên của người đó.
  - `Trạng thái hạn` tự tính: *Quá hạn / Sắp đến hạn / Đúng hạn / Đã xong*.
  - Dropdown cho *Nhóm công việc*, *Người phối hợp*, *Trạng thái*, *Độ ưu tiên*.
- **Tab `TONG HOP`** tự động kéo toàn bộ công việc của 10 tab cá nhân về một chỗ
  (công thức `QUERY` gộp mảng), kèm 6 thẻ thống kê: Tổng số việc · Hoàn thành ·
  Đang làm · Đang duyệt · Quá hạn · Sắp đến hạn.

> Nhập việc ở tab của mình → tab `TONG HOP` tự cập nhật, không cần copy tay.

### Cách tạo

```bash
# Cách 1 — Tạo trực tiếp trên Google Drive (cần mạng + API/token.json hợp lệ)
python3 tao_sheet_cong_viec_moi.py

# Cách 2 — Xuất file .xlsx rồi tự upload lên Drive (không cần mạng)
python3 tao_sheet_cong_viec_moi.py --xlsx
```

Với cách 1, script in ra link Google Sheet và lưu ID vào `cong_viec_config.json`.
Với cách 2, vào Drive → kéo thả file `.xlsx` → chuột phải → *Mở bằng* → *Google Trang tính* → *Tệp* → *Lưu thành Google Trang tính*.

---

## 📁 Cấu Trúc Thư Mục Dự Án

```
├── tao_sheet_cong_viec_moi.py        # Script tạo Google Sheet Quản lý công việc MỚI
├── marketing_hub.html                # Web App Đầu mối thông tin Marketing Hub (20 liên kết)
├── quan_ly_cong_viec.html            # Web App Quản lý công việc (Kanban, Table, Dashboard, CRUD)
├── website_tong_hop_bao_cao.html     # Web App Báo cáo hàng ngày 17:30
├── index.html                        # Trang chủ điều hướng hệ thống
├── server.py                         # Backend Server (Python REST API + Google Sheets API v4)
├── tai_khoan_nhan_su.json            # Cơ sở dữ liệu tài khoản & mã PIN 10 nhân sự
├── quan_ly_cong_viec_store.json      # Bộ nhớ đệm cache công việc cục bộ
├── bao_cao_store.json                # Bộ nhớ cache báo cáo hàng ngày
├── Quan_Ly_Cong_Viec_KingBlue.xlsx   # Bảng tính Excel quản lý công việc offline
├── Bao_Cao_Cong_Viec_KingBlue.xlsx   # Bảng tính Excel báo cáo offline
├── API/                              # Chứa cấu hình OAuth Google API (token.json)
├── org_chart_marketing_kingblue.md   # Sơ đồ tổ chức & quy định phân quyền CRM
├── mau_bao_cao_hang_ngay.md          # Quy chuẩn mẫu báo cáo hàng ngày
├── kpi_phong_marketing_cu.md         # Bảng tổng hợp KPI cũ Tháng 7/2026 (7 nhân sự)
├── thong_tin_dau_moi_marketing.md    # Dashboard đầu mối 20 liên kết thông tin & tài nguyên MKT
└── README.md                         # Tài liệu hướng dẫn sử dụng dự án
```

---
*Phát triển bởi đội ngũ Marketing King Blue & Trợ lý ảo AI 🐱 Xu Xu.*


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

| STT | Họ và Tên | Vai Trò Chuyên Môn | Bộ Phận | Mã PIN | Quyền CRM | Tab Google Sheets |
|:---:|:---|:---|:---:|:---:|:---:|:---|
| 👑 | **Marketing Manager** | Trưởng Phòng Marketing | Ban Quản Lý | `8888` | **Admin / Quản Trị** | `BAO CAO HOM NAY` |
| 1 | **Võ Thị Hoài Thương** | Content Marketing & SEO Fanpage/Website | Content | `1001` | User | `Hoai Thuong - Content` |
| 2 | **Kiều Thương** | Content Video & Hợp Tác KOC/Reviewer | Content | `1002` | User | `Kieu Thuong - Content` |
| 3 | **Thụy Thương** | Trade Marketing & Chính Sách Điểm Bán | Content | `1003` | User | `Thuy Thuong - Content` |
| 4 | **Thiện** | Graphic Designer (2D/3D, POSM & Banner) | Design | `1004` | User | `Thien - Design` |
| 5 | **Tứ** | Media / Photographer (Hình Ảnh & User CRM) | Media | `1005` | User | `Tu - Media` |
| 6 | **Thức** | Vận Hành Sàn TMĐT (Shopee & Lazada) | Sàn TMĐT | `1006` | User | `Thuc - San TMDT` |
| 7 | **Ngân** | CSKH & Quản Trị Gian Hàng TikTok Shop | Sàn TMĐT | `1007` | User | `Ngan - San TMDT` |
| 8 | **Hùng** | Đóng Gói & Kho Vận Hàng Hóa Miền Nam | Đóng gói kho | `1008` | User | `Hung - Kho MN` |
| 9 | **Hùng Miền Bắc** | Đóng Gói & Kho Vận Chi Nhánh Hà Nội | Đóng gói kho | `1009` | User | `Hung - Kho MB` |

---

## 🏗️ Cấu Trúc Hệ Thống & Google Sheets

- **File Google Sheets Trực Tuyến**:
  - `BAO CAO HOM NAY` (Sheet 1 - Master Dashboard): Tự động nhận diện `=TODAY()`, tích hợp lịch Date Picker nhấp đúp chọn ngày, công thức `XLOOKUP` kéo việc của 9 nhân sự.
  - 9 Sheet cá nhân riêng biệt cho 9 bạn nhân sự lưu lịch sử báo cáo.
  - `BAO CAO TUAN`: Sheet tổng hợp KPI và tiến độ hàng tuần.
- **File Excel Offline**: `Bao_Cao_Cong_Viec_KingBlue.xlsx` (Cấu trúc 11 sheet đồng bộ chuẩn).

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

---

## 📁 Cấu Trúc Thư Mục Dự Án

```
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
└── README.md                         # Tài liệu hướng dẫn sử dụng dự án
```

---
*Phát triển bởi đội ngũ Marketing King Blue & Trợ lý ảo AI 🐱 Xu Xu.*

# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG GOOGLE SHEETS QUẢN LÝ & BÁO CÁO CÔNG VIỆC KING BLUE

Chào mừng bạn đến với bộ tài liệu Google Sheets được thiết kế chuyên biệt cho công tác **Quản lý công việc** và **Báo cáo hiệu suất Marketing & Vận hành** của thương hiệu **King Blue**.

---

## 1. Danh Sách Liên Kết Trực Tuyến (Live Google Sheets)
Tài khoản kết nối: **Duykoolhp1996@gmail.com** (Đã đồng bộ và phân quyền truy cập)

* 📁 **Thư mục Google Drive tổng**: [King Blue - Quản Lý Marketing](https://drive.google.com/drive/folders/1e6BtoJ8BwmpIlJGhr_OMJND7rfuPqT_j)
* 📊 **Google Sheet Báo Cáo Công Việc Hàng Ngày**: [Báo Cáo Công Việc Hàng Ngày - King Blue Marketing](https://docs.google.com/spreadsheets/d/1_kID0uhutS6Ky_zpB2yW_AQXN2aUKKCKo_6tqZL1kbo/edit)
* 📈 **Google Sheet Quản Lý Giao Việc & Tiến Độ**: [Quản Lý Công Việc - King Blue Marketing](https://docs.google.com/spreadsheets/d/1CmcmBFP4jjdV1jrnNNWwXkc1foxa4j6asaOhI0qg7u8/edit)

---

## 2. File Bản Gốc Tại Máy Cục Bộ
1. **File Quản Lý Công Việc**: [Quan_Ly_Cong_Viec_KingBlue.xlsx](file:///Users/Admin/Documents/KIngblue/Quan_Ly_Cong_Viec_KingBlue.xlsx)
2. **File Báo Cáo Công Việc**: [Bao_Cao_Cong_Viec_KingBlue.xlsx](file:///Users/Admin/Documents/KIngblue/Bao_Cao_Cong_Viec_KingBlue.xlsx)
3. **Mã nguồn tự động đồng bộ API**: [connect_google_api.py](file:///Users/Admin/Documents/KIngblue/connect_google_api.py)
4. **Thư mục chứng chỉ API**: [API/](file:///Users/Admin/Documents/KIngblue/API/)

---

## 3. Cấu Trúc File 1: Quản Lý Công Việc (`Quan_Ly_Cong_Viec_KingBlue.xlsx`)

### Tab 1: `DASHBOARD` (Bảng điều khiển tự động)
* **Thẻ chỉ số nhanh (KPI Cards)**:
  - **Tổng số công việc**: Tự động đếm số lượng công việc đang có.
  - **Hoàn thành**: Số công việc đã xong.
  - **Đang thực hiện**: Số công việc đang trong quá trình chạy.
  - **Đang duyệt**: Số công việc chờ phê duyệt từ Leader/Admin.
  - **Quá hạn**: Tự động cảnh báo các task bị trễ hạn so với ngày hôm nay.
  - **Tỷ lệ hoàn thành (%)**: Tự động tính tỷ lệ % tiến độ tổng thể.
* **4 Bảng phân tích chi tiết**:
  1. Phân bổ theo Trạng thái (Số lượng & % Tỷ trọng).
  2. Phân bổ theo Mức độ ưu tiên (Khẩn cấp, Cao, Trung bình, Thấp).
  3. Phân bổ theo Hạng mục / Kênh Marketing (Website, Fanpage, YouTube, TikTok, POSM Đại lý, Sàn TMĐT, Media).
  4. Phân bổ theo Nhân sự phụ trách (Admin, MKT Leader, Content, Designer, Photographer/Media, Sales/E-com).

### Tab 2: `DS CONG VIEC` (Task Tracker chi tiết)
* Đã tích hợp sẵn **menu chọn thả xuống (Dropdown)** cho các cột:
  - **Hạng mục / Kênh**
  - **Người phụ trách & Phối hợp**
  - **Trạng thái** (Chưa bắt đầu, Đang làm, Đang duyệt, Hoàn thành, Tạm hoãn)
  - **Mức độ ưu tiên** (Khẩn cấp, Cao, Trung bình, Thấp)
* **Cột "Tình trạng hạn" tự động**: Dùng hàm logic `=IF(...)` so sánh ngày Deadline với ngày hiện tại (`TODAY()`) để tự động gắn nhãn:
  - `Đã xong` (nếu trạng thái là Hoàn thành)
  - `Đúng hạn` (còn nhiều hơn 2 ngày)
  - `Sắp đến hạn` (còn dưới 2 ngày)
  - `Quá hạn` (ngày deadline đã qua mà chưa xong)

### Tab 3: `CAU HINH` (Settings)
* Quản lý danh sách nhân sự, kênh truyền thông, trạng thái và độ ưu tiên. Bạn có thể thêm nhân sự hoặc thêm hạng mục mới tại đây để menu dropdown tự động cập nhật.

---

## 4. Cấu Trúc File 2: Báo Cáo Công Việc (`Bao_Cao_Cong_Viec_KingBlue.xlsx`)

### Tab 1: `BAO CAO HANG NGAY` (Báo cáo công việc mỗi ngày - Daily Standup / Log)
* **Quy chuẩn**: Toàn bộ **9 nhân sự** nộp báo cáo trước **17:30** mỗi ngày. **Marketing Manager** rà soát, phản hồi và duyệt công việc trước **18:00**.
* **4 Thẻ chỉ số tổng kết ngày**: Đếm tự động ngày hiện tại (`TODAY()`), số nhân sự đã nộp, số đầu việc hoàn thành 100%, số việc đang xử lý dở dang.
* **12 Cột nghiệp vụ chi tiết**:
  - `STT`, `Ngày`, `Nhân sự`, `Bộ phận / Vị trí`.
  - `Công việc thực hiện trong ngày`: Ghi rõ các đầu việc chính đã làm.
  - `Kết quả đầu ra (Deliverables)`: Minh chứng sản phẩm cụ thể (bài viết, video, ảnh sản phẩm, số đơn đóng...).
  - `Tình trạng`: Hoàn thành 100%, Đang làm (%), Chưa làm, Hoãn (tô màu tự động).
  - `Link sản phẩm / Minh chứng`: Link Google Drive, link bài viết, phiếu xuất kho.
  - `Khó khăn / Cần hỗ trợ (Blockers)`: Ghi nhận ngay vướng mắc trong ngày để giải quyết.
  - `Kế hoạch ngày mai`: Dự kiến đầu việc của ngày tiếp theo.
  - `Marketing Manager Phản Hồi`: Cột dành riêng cho Trưởng phòng nhận xét, duyệt hoặc nhắc nhở.
  - `Giờ nộp`: Kiểm soát tính đúng giờ và kỷ luật làm việc.

### Tab 2: `BAO CAO TUAN` (Báo cáo tiến độ tuần)
* **Thông tin tuần**: Điều phối tổng hợp bởi Marketing Manager, theo dõi 9 nhân sự (5 vị trí).
* **Phần I - Việc đã hoàn thành**: Bảng kê các việc đã bàn giao 100%, kết quả cụ thể, link tài liệu và đánh giá chất lượng.
* **Phần II - Việc đang xử lý & Trở ngại (Blockers)**: Nêu rõ nguyên nhân trễ hạn, giải pháp xử lý, người cần hỗ trợ và hạn chót mới.
* **Phần III - Kế hoạch tuần tới**: Danh sách nhiệm vụ trọng tâm, mục tiêu cần đạt, người phối hợp và mức độ ưu tiên.
* **Phần IV - Đề xuất & Kiến nghị**: Khu vực gửi đề xuất ngân sách quảng cáo, thiết bị hoặc hỗ trợ từ Ban Giám Đốc.

### Tab 3: `CHI SO MARKETING` (Metrics & KPI Kênh)
* Bảng theo dõi định lượng các chỉ số tăng trưởng:
  - **Facebook**: Lượt tiếp cận (Reach), Tương tác, Tin nhắn hỏi làm đại lý mới.
  - **YouTube**: Số video mới xuất bản, Lượt xem, Người đăng ký.
  - **TikTok & KOC**: Số lượt xem hashtag `#kingblue`, tương tác video review.
  - **Website (`kingblue.vn`)**: Lượt truy cập (Sessions), Số lượt tải catalogue.
  - **Sàn TMĐT & Bán buôn**: Doanh số nhóm phụ kiện/máy móc, số đơn hàng.
  - **Trade & POSM**: Số đại lý lắp đặt mới kệ trưng bày King Blue, biển hiệu bàn giao.
* Tự động tính toán tỷ lệ đạt `% Tỷ lệ hoàn thành` so với mục tiêu tháng.

### Tab 4: `DANH GIA THANG` (Monthly Review)
* Đánh giá hiệu suất nhân sự và phòng ban theo 5 trụ cột:
  1. Sản xuất nội dung & Social Media
  2. Thiết kế & Bộ nhận diện POSM
  3. Hình ảnh & Video sản phẩm (Media)
  4. Hỗ trợ Sales & Kênh Đại lý
  5. Kỷ luật & Tinh thần phối hợp
* Có cột tự đánh giá của nhân sự và cột nhận xét của Quản lý.

---
*Tài liệu được khởi tạo và cấu hình bởi trợ lý 🐱 Xu Xu dành riêng cho thương hiệu King Blue.*

import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "API", "token.json")
SPREADSHEET_ID = "1_kID0uhutS6Ky_zpB2yW_AQXN2aUKKCKo_6tqZL1kbo"

PERSONNEL_TABS = [
    {"row": 8, "tab": "Hoai Thuong - Content"},
    {"row": 9, "tab": "Kieu Thuong - Content"},
    {"row": 10, "tab": "Thuy Thuong - Content"},
    {"row": 11, "tab": "Thien - Design"},
    {"row": 12, "tab": "Tu - Media"},
    {"row": 13, "tab": "Thuc - San TMDT"},
    {"row": 14, "tab": "Ngan - San TMDT"},
    {"row": 15, "tab": "Hung - Kho MN"},
    {"row": 16, "tab": "Hung - Kho MB"},
]

def apply_formulas():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE)
    service = build("sheets", "v4", credentials=creds)

    print("🚀 Bắt đầu cài đặt công thức tự động liên kết 100% thời gian thực...")

    # 1. Cài đặt thanh chọn ngày ở Hàng 3
    date_cells = [
        ["📅 NGÀY XEM BÁO CÁO:", "05/10/2026", "(Gõ ngày cần xem theo định dạng DD/MM/YYYY hoặc gõ =TODAY())"]
    ]
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="'TONG HOP HANG NGAY'!B3:D3",
        valueInputOption="USER_ENTERED",
        body={"values": date_cells}
    ).execute()

    # 2. Cài đặt công thức KPI tự động ở Hàng 5
    kpi_formulas = [
        ['=COUNTIF(J8:J16; "Đúng hạn") & " / 9 (" & TEXT(COUNTIF(J8:J16; "Đúng hạn")/9; "0%") & ")"',
         '',
         '=COUNTIF(F8:F16; "*•*") & " Vấn đề"',
         '',
         '=IF(COUNTIF(J8:J16; "Chưa nộp")=0; "100% Đúng hạn"; "Còn " & COUNTIF(J8:J16; "Chưa nộp") & " chưa nộp")']
    ]
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="'TONG HOP HANG NGAY'!D5:H5",
        valueInputOption="USER_ENTERED",
        body={"values": kpi_formulas}
    ).execute()

    # 3. Cài đặt công thức liên kết động cho từng nhân sự (Row 8 -> 16)
    updates = []
    for item in PERSONNEL_TABS:
        r = item["row"]
        t = item["tab"]

        # Công thức lấy kết quả, khó khăn, đề xuất, kế hoạch, giờ, trạng thái, feedback
        f_res = f'=IFERROR(XLOOKUP(TEXT($C$3; "dd/mm/yyyy"); \'{t}\'!$B$6:$B$50; \'{t}\'!$D$6:$D$50; IFERROR(XLOOKUP($C$3; \'{t}\'!$B$6:$B$50; \'{t}\'!$D$6:$D$50; "⏳ Chưa nộp"); "⏳ Chưa nộp")); "⏳ Chưa nộp")'
        f_diff = f'=IFERROR(XLOOKUP(TEXT($C$3; "dd/mm/yyyy"); \'{t}\'!$B$6:$B$50; \'{t}\'!$E$6:$E$50; IFERROR(XLOOKUP($C$3; \'{t}\'!$B$6:$B$50; \'{t}\'!$E$6:$E$50; "-"); "-")); "-")'
        f_lesson = f'=IFERROR(XLOOKUP(TEXT($C$3; "dd/mm/yyyy"); \'{t}\'!$B$6:$B$50; \'{t}\'!$F$6:$F$50; IFERROR(XLOOKUP($C$3; \'{t}\'!$B$6:$B$50; \'{t}\'!$F$6:$F$50; "-"); "-")); "-")'
        f_plan = f'=IFERROR(XLOOKUP(TEXT($C$3; "dd/mm/yyyy"); \'{t}\'!$B$6:$B$50; \'{t}\'!$G$6:$G$50; IFERROR(XLOOKUP($C$3; \'{t}\'!$B$6:$B$50; \'{t}\'!$G$6:$G$50; "-"); "-")); "-")'
        f_time = f'=IFERROR(TEXT(XLOOKUP(TEXT($C$3; "dd/mm/yyyy"); \'{t}\'!$B$6:$B$50; \'{t}\'!$C$6:$C$50; IFERROR(XLOOKUP($C$3; \'{t}\'!$B$6:$B$50; \'{t}\'!$C$6:$C$50; "--:--"); "--:--")); "hh:mm:ss"); "--:--")'
        f_status = f'=IF(E{r}="⏳ Chưa nộp"; "Chưa nộp"; IFERROR(XLOOKUP(TEXT($C$3; "dd/mm/yyyy"); \'{t}\'!$B$6:$B$50; \'{t}\'!$I$6:$I$50; IFERROR(XLOOKUP($C$3; \'{t}\'!$B$6:$B$50; \'{t}\'!$I$6:$I$50; "Đúng hạn"); "Đúng hạn")); "Đúng hạn"))'
        f_feedback = f'=IFERROR(XLOOKUP(TEXT($C$3; "dd/mm/yyyy"); \'{t}\'!$B$6:$B$50; \'{t}\'!$J$6:$J$50; IFERROR(XLOOKUP($C$3; \'{t}\'!$B$6:$B$50; \'{t}\'!$J$6:$J$50; "-"); "-")); "-")'

        updates.append({
            "range": f"'TONG HOP HANG NGAY'!E{r}:K{r}",
            "values": [[f_res, f_diff, f_lesson, f_plan, f_time, f_status, f_feedback]]
        })

    service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": updates
        }
    ).execute()

    print("✅ ĐÃ CÀI ĐẶT THÀNH CÔNG 100% CÔNG THỨC ĐỘNG VÀO SHEET TỔNG!")

if __name__ == "__main__":
    apply_formulas()

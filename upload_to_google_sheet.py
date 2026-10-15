import os
import json
from connect_google_api import authenticate, get_or_create_folder, upload_and_convert_to_sheets
from googleapiclient.discovery import build

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "KingBlue_Du_Lieu_Chuan_SQL.xlsx")
TITLE = "THÔNG TIN KHÁCH HÀNG & GIÁ BÁN SÀN TMĐT (CHUẨN HOÁ SQL) - KINGBLUE"

def main():
    creds = authenticate()
    drive_service = build('drive', 'v3', credentials=creds)

    folder_id = get_or_create_folder(drive_service, "King Blue - Quản Lý Marketing")

    print(f"🚀 Đang tải lên và chuyển đổi '{FILE_PATH}' sang Google Sheet...")
    res = upload_and_convert_to_sheets(drive_service, FILE_PATH, TITLE, folder_id)

    if res:
        file_id = res.get('id')
        link = res.get('webViewLink')

        # Set permission anyone with link can edit/view
        try:
            drive_service.permissions().create(
                fileId=file_id,
                body={'type': 'anyone', 'role': 'writer'}
            ).execute()
            print("🔓 Đã cấp quyền chỉnh sửa cho bất kỳ ai có link!")
        except Exception as e:
            print(f"⚠️ Lỗi cấp quyền share: {e}")

        print("\n" + "="*70)
        print("🎉 TẠO GOOGLE SHEET THÀNH CÔNG!")
        print(f"🔗 File ID: {file_id}")
        print(f"🔗 Link Google Sheet: https://docs.google.com/spreadsheets/d/{file_id}/edit")
        print("="*70)

        # Cập nhật vào google_sheets_links.json
        links_file = os.path.join(BASE_DIR, "google_sheets_links.json")
        try:
            with open(links_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["sheets"][TITLE] = f"https://docs.google.com/spreadsheets/d/{file_id}/edit"
            with open(links_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"💾 Đã lưu vào {links_file}")
        except Exception as e:
            print(f"⚠️ Lỗi cập nhật json: {e}")

        return f"https://docs.google.com/spreadsheets/d/{file_id}/edit"
    else:
        print("❌ Lỗi khi upload!")
        return None

if __name__ == "__main__":
    main()

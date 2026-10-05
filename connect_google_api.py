import os
import sys
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_DIR = os.path.join(BASE_DIR, "API")

# Tìm file client secret trong thư mục API
CLIENT_SECRET_FILE = None
for f in os.listdir(API_DIR):
    if f.startswith("client_secret") and f.endswith(".json"):
        CLIENT_SECRET_FILE = os.path.join(API_DIR, f)
        break

if not CLIENT_SECRET_FILE:
    print("❌ Không tìm thấy file client_secret trong thư mục API!")
    sys.exit(1)

TOKEN_FILE = os.path.join(API_DIR, "token.json")

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            print("🔑 Đã tìm thấy file token.json hiện có.")
        except Exception as e:
            print(f"⚠️ Token hiện có không hợp lệ: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("🔄 Đang làm mới access token từ refresh token...")
                creds.refresh(Request())
            except Exception as e:
                print(f"⚠️ Làm mới token thất bại: {e}")
                creds = None

        if not creds:
            print("🌐 Đang khởi động luồng xác thực Google OAuth 2.0...")
            print(f"📁 Sử dụng Client Secret: {os.path.basename(CLIENT_SECRET_FILE)}")
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE,
                SCOPES
            )
            # Run local server flow, port=0 selects an available port
            creds = flow.run_local_server(port=0, open_browser=True)

        with open(TOKEN_FILE, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())
            print(f"✅ Đã lưu token xác thực thành công vào: {TOKEN_FILE}")

    return creds

def get_or_create_folder(drive_service, folder_name="King Blue - Quản Lý Marketing"):
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if items:
        folder_id = items[0]['id']
        print(f"📁 Đã tìm thấy thư mục Google Drive: '{folder_name}' (ID: {folder_id})")
        return folder_id
    else:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        print(f"✨ Đã tạo mới thư mục Google Drive: '{folder_name}' (ID: {folder_id})")
        return folder_id

def upload_and_convert_to_sheets(drive_service, file_path, file_title, folder_id):
    if not os.path.exists(file_path):
        print(f"⚠️ Không tìm thấy file nguồn: {file_path}")
        return None

    # Kiểm tra xem file đã tồn tại trên Drive trong folder chưa
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
        print(f"🔄 Đang cập nhật nội dung cho Google Sheet: '{file_title}' (ID: {file_id})...")
        updated_file = drive_service.files().update(
            fileId=file_id,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        return updated_file
    else:
        print(f"🚀 Đang tải lên và chuyển đổi sang Google Sheet: '{file_title}'...")
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
        return created_file

def main():
    print("=" * 60)
    print("🐱 XU XU - KẾT NỐI GOOGLE API CHO KING BLUE")
    print("=" * 60)
    creds = authenticate()

    drive_service = build('drive', 'v3', credentials=creds)

    # Lấy thông tin tài khoản người dùng
    try:
        about = drive_service.about().get(fields="user").execute()
        user_info = about.get('user', {})
        user_email = user_info.get('emailAddress', 'N/A')
        display_name = user_info.get('displayName', 'N/A')
        print(f"🎉 Kết nối thành công tới tài khoản: {display_name} ({user_email})")
    except Exception as e:
        print(f"⚠️ Không thể lấy thông tin user: {e}")

    # Lấy hoặc tạo thư mục trên Drive
    folder_id = get_or_create_folder(drive_service, "King Blue - Quản Lý Marketing")

    files_to_sync = [
        {
            "local": os.path.join(BASE_DIR, "Bao_Cao_Cong_Viec_KingBlue.xlsx"),
            "title": "Báo Cáo Công Việc Hàng Ngày - King Blue Marketing"
        },
        {
            "local": os.path.join(BASE_DIR, "Quan_Ly_Cong_Viec_KingBlue.xlsx"),
            "title": "Quản Lý Công Việc - King Blue Marketing"
        }
    ]

    synced_links = {}
    for item in files_to_sync:
        res = upload_and_convert_to_sheets(drive_service, item["local"], item["title"], folder_id)
        if res:
            synced_links[item["title"]] = res.get('webViewLink')
            print(f"✅ ĐÃ ĐỒNG BỘ: {item['title']}")
            print(f"   🔗 Link Google Sheet: {res.get('webViewLink')}")

    # Lưu lại file danh sách link
    links_file = os.path.join(BASE_DIR, "google_sheets_links.json")
    with open(links_file, 'w', encoding='utf-8') as f:
        json.dump({
            "account": user_email if 'user_email' in locals() else "Duykoolhp1996@gmail.com",
            "folder_id": folder_id,
            "folder_link": f"https://drive.google.com/drive/folders/{folder_id}",
            "sheets": synced_links
        }, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("🎉 HOÀN TẤT KẾT NỐI VÀ ĐỒNG BỘ GOOGLE SHEETS THÀNH CÔNG!")
    print(f"📁 Thư mục Google Drive: https://drive.google.com/drive/folders/{folder_id}")
    for title, link in synced_links.items():
        print(f"📊 {title}: {link}")
    print("=" * 60)

if __name__ == "__main__":
    main()

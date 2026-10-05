import os
import json
import datetime
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNTS_FILE = os.path.join(BASE_DIR, "tai_khoan_nhan_su.json")
REPORTS_STORE_FILE = os.path.join(BASE_DIR, "bao_cao_store.json")
TOKEN_FILE = os.path.join(BASE_DIR, "API", "token.json")
SPREADSHEET_ID = "1_kID0uhutS6Ky_zpB2yW_AQXN2aUKKCKo_6tqZL1kbo"

def get_sheets_service():
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE)
            return build("sheets", "v4", credentials=creds)
        except Exception as e:
            print(f"Lỗi khởi tạo Sheets API: {e}")
    return None

def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_reports_store():
    if os.path.exists(REPORTS_STORE_FILE):
        try:
            with open(REPORTS_STORE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_reports_store(store):
    try:
        with open(REPORTS_STORE_FILE, "w", encoding="utf-8") as f:
            json.dump(store, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi lưu store: {e}")

class KingBlueHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/reports":
            self.handle_get_reports(parsed)
        elif parsed.path == "/api/accounts":
            self.handle_get_accounts()
        else:
            super().do_GET()

    def handle_get_accounts(self):
        accounts = load_accounts()
        safe = [{k: v for k, v in u.items() if k not in ["password", "pin", "alt_pass"]} for u in accounts]
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(safe, ensure_ascii=False).encode("utf-8"))

    def handle_get_reports(self, parsed):
        query = urllib.parse.parse_qs(parsed.query)
        now = datetime.datetime.now()
        date_str = query.get("date", [now.strftime("%d/%m/%Y")])[0].strip()
        # Convert YYYY-MM-DD to DD/MM/YYYY if needed
        if "-" in date_str and len(date_str) == 10:
            parts = date_str.split("-")
            if len(parts[0]) == 4:
                date_str = f"{parts[2]}/{parts[1]}/{parts[0]}"
        
        store = load_reports_store()
        reports = {}
        users = [u for u in load_accounts() if u.get("type") == "USER"]
        for u in users:
            reports[u["username"]] = store.get(u["username"], {}).get(date_str, None)

        sheets_service = get_sheets_service()
        if sheets_service:
            try:
                ranges = [f"'{u['tabName']}'!A6:J50" for u in users]
                res = sheets_service.spreadsheets().values().batchGet(
                    spreadsheetId=SPREADSHEET_ID,
                    ranges=ranges
                ).execute()
                for u, vr in zip(users, res.get("valueRanges", [])):
                    rows = vr.get("values", [])
                    for r in rows:
                        if len(r) > 1 and r[1].strip() == date_str:
                            rep = {
                                "time": r[2] if len(r) > 2 else "--:--",
                                "res": r[3] if len(r) > 3 else "",
                                "diff": r[4] if len(r) > 4 else "• Không có",
                                "lesson": r[5] if len(r) > 5 else "• Không có",
                                "plan": r[6] if len(r) > 6 else "",
                                "link": r[7] if len(r) > 7 else "-",
                                "status": r[8] if len(r) > 8 else "Đúng hạn",
                                "feedback": r[9] if len(r) > 9 else ""
                            }
                            reports[u["username"]] = rep
                            if u["username"] not in store:
                                store[u["username"]] = {}
                            store[u["username"]][date_str] = rep
                            break
                save_reports_store(store)
            except Exception as e:
                print(f"Sheets live fetch error: {e}")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "date": date_str, "reports": reports}, ensure_ascii=False).encode("utf-8"))

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        
        try:
            body = json.loads(post_data) if post_data else {}
        except Exception:
            body = {}

        if parsed_path.path == "/api/login":
            self.handle_login(body)
        elif parsed_path.path == "/api/submit":
            self.handle_submit(body)
        elif parsed_path.path == "/api/feedback":
            self.handle_feedback(body)
        else:
            self.send_response(404)
            self.end_headers()

    def handle_login(self, body):
        username = body.get("username", "").strip().lower()
        password = str(body.get("password", "")).strip().lower()
        accounts = load_accounts()

        user = None
        if username:
            user = next((u for u in accounts if u["username"].lower() == username and (str(u["password"]).lower() == password or str(u.get("pin", "")).lower() == password or str(u.get("alt_pass", "")).lower() == password)), None)
        else:
            user = next((u for u in accounts if str(u["password"]).lower() == password or str(u.get("pin", "")).lower() == password or str(u.get("alt_pass", "")).lower() == password), None)

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

        if user:
            safe_user = {k: v for k, v in user.items() if k not in ["password", "pin", "alt_pass"]}
            resp = {"success": True, "user": safe_user}
        else:
            resp = {"success": False, "message": "Mật khẩu không đúng!"}
        self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))

    def handle_submit(self, body):
        now = datetime.datetime.now()
        submit_time = now.strftime("%H:%M:%S")
        date_str = body.get("date", now.strftime("%d/%m/%Y")).strip()
        
        is_on_time = (now.hour < 17) or (now.hour == 17 and now.minute <= 30)
        status = "Đúng hạn" if is_on_time else "Nộp muộn"

        username = body.get("username", "").strip().lower()
        accounts = load_accounts()
        user = next((u for u in accounts if u["username"].lower() == username), None)

        if not user:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "message": "Không tìm thấy nhân sự!"}).encode("utf-8"))
            return

        tab_name = user["tabName"]
        res = body.get("res", "").strip()
        diff = body.get("diff", "").strip() or "• Không có"
        lesson = body.get("lesson", "").strip() or "• Không có"
        plan = body.get("plan", "").strip()
        link = body.get("link", "").strip() or "-"

        # 1. Update local cache
        store = load_reports_store()
        if username not in store:
            store[username] = {}
        old_fb = store[username].get(date_str, {}).get("feedback", "Đã ghi nhận bản mới nhất, chờ duyệt")
        store[username][date_str] = {
            "time": submit_time,
            "status": status,
            "res": res,
            "diff": diff,
            "lesson": lesson,
            "plan": plan,
            "link": link,
            "feedback": old_fb
        }
        save_reports_store(store)

        # 2. Cập nhật trực tiếp lên Google Sheets tab cá nhân
        sheets_service = get_sheets_service()
        synced_online = False
        if sheets_service and tab_name not in ["BAO CAO HOM NAY", "TONG HOP HANG NGAY"]:
            try:
                res_dates = sheets_service.spreadsheets().values().get(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f"'{tab_name}'!B6:B50"
                ).execute()
                dates_list = [row[0] if row else "" for row in res_dates.get("values", [])]

                target_row = None
                for idx, d in enumerate(dates_list, start=6):
                    if d.strip() == date_str:
                        target_row = idx
                        break

                if target_row:
                    update_range = f"'{tab_name}'!C{target_row}:I{target_row}"
                    sheets_service.spreadsheets().values().update(
                        spreadsheetId=SPREADSHEET_ID,
                        range=update_range,
                        valueInputOption="USER_ENTERED",
                        body={"values": [[submit_time, res, diff, lesson, plan, link, status]]}
                    ).execute()
                else:
                    first_empty_row = 6 + len(dates_list)
                    new_stt = len(dates_list) + 1
                    update_range = f"'{tab_name}'!A{first_empty_row}:I{first_empty_row}"
                    sheets_service.spreadsheets().values().update(
                        spreadsheetId=SPREADSHEET_ID,
                        range=update_range,
                        valueInputOption="USER_ENTERED",
                        body={"values": [[new_stt, date_str, submit_time, res, diff, lesson, plan, link, status]]}
                    ).execute()
                synced_online = True
                print(f"✅ Đã đồng bộ Google Sheets cho {user['name']} lúc {submit_time}")
            except Exception as e:
                print(f"⚠️ Lỗi đồng bộ Sheets: {e}")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        resp = {
            "success": True,
            "message": f"Đã lưu báo cáo thành công lúc {submit_time} ({status})!",
            "submit_time": submit_time,
            "status": status,
            "synced_online": synced_online
        }
        self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))

    def handle_feedback(self, body):
        username = body.get("username", "").strip()
        date_str = body.get("date", "").strip()
        feedback = body.get("feedback", "").strip()

        accounts = load_accounts()
        user = next((u for u in accounts if u["username"] == username), None)
        if not user:
            self.send_response(400)
            self.end_headers()
            return

        # 1. Update local cache
        store = load_reports_store()
        if username in store and date_str in store[username]:
            store[username][date_str]["feedback"] = feedback
            save_reports_store(store)

        # 2. Update Sheets
        sheets_service = get_sheets_service()
        if sheets_service:
            try:
                tab_name = user["tabName"]
                res_dates = sheets_service.spreadsheets().values().get(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f"'{tab_name}'!B6:B50"
                ).execute()
                dates_list = [row[0] if row else "" for row in res_dates.get("values", [])]
                for idx, d in enumerate(dates_list, start=6):
                    if d.strip() == date_str:
                        sheets_service.spreadsheets().values().update(
                            spreadsheetId=SPREADSHEET_ID,
                            range=f"'{tab_name}'!J{idx}",
                            valueInputOption="USER_ENTERED",
                            body={"values": [[feedback]]}
                        ).execute()
                        break
            except Exception as e:
                print(f"Feedback error: {e}")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True}).encode("utf-8"))

def run_server():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, KingBlueHandler)
    print(f"🚀 King Blue Marketing Portal Server đang chạy tại http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Đang dừng server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

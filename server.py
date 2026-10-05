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

def normalize_date(d_str, default_year=None):
    if not d_str:
        return ""
    if not default_year:
        default_year = str(datetime.datetime.now().year)
    d_str = str(d_str).strip()
    if "/" in d_str:
        parts = d_str.split("/")
        if len(parts) == 2:
            try:
                return f"{int(parts[0]):02d}/{int(parts[1]):02d}/{default_year}"
            except Exception:
                return d_str
        elif len(parts) == 3:
            try:
                y = parts[2] if len(parts[2]) == 4 else f"20{parts[2]}"
                return f"{int(parts[0]):02d}/{int(parts[1]):02d}/{y}"
            except Exception:
                return d_str
    elif "-" in d_str and len(d_str) == 10:
        parts = d_str.split("-")
        if len(parts[0]) == 4:
            return f"{parts[2]}/{parts[1]}/{parts[0]}"
    return d_str

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
        raw_date = query.get("date", [now.strftime("%d/%m/%Y")])[0].strip()
        date_str = normalize_date(raw_date, default_year=str(now.year))
        
        store = load_reports_store()
        reports = {}
        users = [u for u in load_accounts() if u.get("type") == "USER"]
        for u in users:
            reports[u["username"]] = store.get(u["username"], {}).get(date_str, None)

        sheets_service = get_sheets_service()
        if sheets_service:
            try:
                # 1. Đọc trực tiếp từ master sheet BAO CAO HOM NAY
                res_master = sheets_service.spreadsheets().values().get(
                    spreadsheetId=SPREADSHEET_ID,
                    range="'BAO CAO HOM NAY'!C3:K16",
                    valueRenderOption="FORMATTED_VALUE"
                ).execute()
                master_vals = res_master.get("values", [])
                
                c3_date = master_vals[0][0].strip() if len(master_vals) > 0 and len(master_vals[0]) > 0 else ""
                c3_norm = normalize_date(c3_date, default_year=str(now.year))

                if c3_norm == date_str and len(master_vals) >= 14:
                    user_rows = master_vals[5:14]
                    for u, r in zip(users, user_rows):
                        res_work = r[2] if len(r) > 2 else "" # Col E
                        if res_work and res_work != "⏳ Chưa nộp" and res_work != "-":
                            t_val = r[6] if len(r) > 6 and r[6] not in ["--:--", "00:00:00", ""] else "17:00:00" # Col I
                            st_val = r[7] if len(r) > 7 and r[7].strip() and r[7] != "Chưa nộp" else "Đúng hạn" # Col J
                            rep = {
                                "time": t_val,
                                "res": res_work,
                                "diff": r[3] if len(r) > 3 and r[3].strip() else "• Không có", # Col F
                                "lesson": r[4] if len(r) > 4 and r[4].strip() else "• Không có", # Col G
                                "plan": r[5] if len(r) > 5 else "", # Col H
                                "link": "-",
                                "status": st_val,
                                "feedback": r[8] if len(r) > 8 else "" # Col K
                            }
                            reports[u["username"]] = rep
                            if u["username"] not in store:
                                store[u["username"]] = {}
                            store[u["username"]][date_str] = rep

                # 2. Đọc từng tab cá nhân nếu còn nhân sự nào chưa lấy được
                for u in users:
                    if reports.get(u["username"]) is None:
                        try:
                            tab_res = sheets_service.spreadsheets().values().get(
                                spreadsheetId=SPREADSHEET_ID,
                                range=f"'{u['tabName']}'!A6:J50",
                                valueRenderOption="FORMATTED_VALUE"
                            ).execute()
                            for r in tab_res.get("values", []):
                                if len(r) > 1:
                                    row_date = normalize_date(r[1], default_year=str(now.year))
                                    if row_date == date_str:
                                        res_text = r[3] if len(r) > 3 else ""
                                        if res_text and res_text != "⏳ Chưa nộp" and res_text != "-":
                                            t_val = r[2] if len(r) > 2 and r[2] not in ["--:--", "00:00:00", ""] else "17:00:00"
                                            st_val = r[8] if len(r) > 8 and r[8].strip() and r[8] != "Chưa nộp" else "Đúng hạn"
                                            rep = {
                                                "time": t_val,
                                                "res": res_text,
                                                "diff": r[4] if len(r) > 4 and r[4].strip() else "• Không có",
                                                "lesson": r[5] if len(r) > 5 and r[5].strip() else "• Không có",
                                                "plan": r[6] if len(r) > 6 else "",
                                                "link": r[7] if len(r) > 7 else "-",
                                                "status": st_val,
                                                "feedback": r[9] if len(r) > 9 else ""
                                            }
                                            reports[u["username"]] = rep
                                            if u["username"] not in store:
                                                store[u["username"]] = {}
                                            store[u["username"]][date_str] = rep
                                            break
                        except Exception as e_user:
                            pass

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
        raw_date = body.get("date", now.strftime("%d/%m/%Y")).strip()
        date_str = normalize_date(raw_date, default_year=str(now.year))
        
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
                dates_list = [normalize_date(row[0], default_year=str(now.year)) if row else "" for row in res_dates.get("values", [])]

                target_row = None
                for idx, d in enumerate(dates_list, start=6):
                    if d == date_str:
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
        now = datetime.datetime.now()
        raw_date = body.get("date", "").strip()
        date_str = normalize_date(raw_date, default_year=str(now.year))
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
                dates_list = [normalize_date(row[0], default_year=str(now.year)) if row else "" for row in res_dates.get("values", [])]
                for idx, d in enumerate(dates_list, start=6):
                    if d == date_str:
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

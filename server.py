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
TASK_SPREADSHEET_ID = "1CmcmBFP4jjdV1jrnNNWwXkc1foxa4j6asaOhI0qg7u8"
TASKS_STORE_FILE = os.path.join(BASE_DIR, "quan_ly_cong_viec_store.json")

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

def load_tasks_store():
    if os.path.exists(TASKS_STORE_FILE):
        try:
            with open(TASKS_STORE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_tasks_store(tasks):
    try:
        with open(TASKS_STORE_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi lưu tasks store: {e}")

def compute_deadline_status(status, deadline_str):
    if str(status).strip() == "Hoàn thành":
        return "Đã xong"
    if not deadline_str:
        return "Đang làm"
    try:
        deadline_str = str(deadline_str).strip()
        today = datetime.date.today()
        if "-" in deadline_str:
            p = deadline_str.split("-")
            dl = datetime.date(int(p[0]), int(p[1]), int(p[2]))
        elif "/" in deadline_str:
            p = deadline_str.split("/")
            dl = datetime.date(int(p[2]), int(p[1]), int(p[0]))
        else:
            return "Đúng hạn"
        diff = (dl - today).days
        if diff < 0:
            return "Quá hạn"
        elif diff <= 2:
            return "Sắp đến hạn"
        else:
            return "Đúng hạn"
    except Exception:
        return "Đúng hạn"

DEFAULT_TASK_CONFIG = {
    "statuses": ["Chưa bắt đầu", "Đang làm", "Đang duyệt", "Hoàn thành", "Tạm hoãn"],
    "priorities": ["Khẩn cấp", "Cao", "Trung bình", "Thấp"],
    "categories": [
        "Website & SEO",
        "Facebook Fanpage",
        "YouTube / Video",
        "TikTok & KOC",
        "Trade & POSM Đại lý",
        "Sàn TMĐT (Shopee/Lazada)",
        "Thiết kế & Media",
        "Đóng gói & Kho vận"
    ],
    "assignees": [
        {"name": "Marketing Manager", "role": "Trưởng Phòng Marketing", "group": "Ban Quản Lý"},
        {"name": "Hoài Thương", "role": "Content Marketing & SEO Fanpage/Website", "group": "Content"},
        {"name": "Kiều Thương", "role": "Content Video & Hợp Tác KOC/Reviewer", "group": "Content"},
        {"name": "Thụy Thương", "role": "Trade Marketing & Chính Sách Điểm Bán", "group": "Content"},
        {"name": "Thiện", "role": "Graphic Designer (2D/3D, POSM & Banner)", "group": "Design"},
        {"name": "Tứ", "role": "Media / Photographer (Hình Ảnh, Video & CRM User)", "group": "Media"},
        {"name": "Thức", "role": "Vận Hành Sàn TMĐT (Shopee & Lazada)", "group": "Sàn TMĐT"},
        {"name": "Ngân", "role": "CSKH & Quản Trị Gian Hàng TikTok Shop", "group": "Sàn TMĐT"},
        {"name": "Hùng", "role": "Đóng Gói & Kho Vận Hàng Hóa Miền Nam", "group": "Đóng gói kho"},
        {"name": "Hùng Miền Bắc", "role": "Đóng Gói & Kho Vận Chi Nhánh Hà Nội", "group": "Đóng gói kho"}
    ]
}

def fetch_tasks_from_sheets():
    sheets_service = get_sheets_service()
    if not sheets_service:
        return load_tasks_store()
    try:
        res = sheets_service.spreadsheets().values().get(
            spreadsheetId=TASK_SPREADSHEET_ID,
            range="'DS CONG VIEC'!A5:N150",
            valueRenderOption="FORMATTED_VALUE"
        ).execute()
        rows = res.get("values", [])
        tasks = []
        for idx, r in enumerate(rows, start=5):
            if len(r) >= 3 and (r[1] or r[2]):
                st = r[8] if len(r) > 8 and r[8] else "Chưa bắt đầu"
                dl = r[7] if len(r) > 7 and r[7] else ""
                dl_status = compute_deadline_status(st, dl)
                task = {
                    "row": idx,
                    "stt": r[0] if len(r) > 0 and r[0] else str(len(tasks) + 1),
                    "code": r[1] if len(r) > 1 and r[1] else f"KB-MKT-{len(tasks)+1:02d}",
                    "name": r[2] if len(r) > 2 else "",
                    "category": r[3] if len(r) > 3 and r[3] else "Website & SEO",
                    "assignee": r[4] if len(r) > 4 and r[4] else "Chưa phân công",
                    "supporter": r[5] if len(r) > 5 else "",
                    "startDate": r[6] if len(r) > 6 else "",
                    "deadline": dl,
                    "status": st,
                    "progress": r[9] if len(r) > 9 and r[9] else "0%",
                    "deadlineStatus": dl_status,
                    "priority": r[11] if len(r) > 11 and r[11] else "Trung bình",
                    "link": r[12] if len(r) > 12 else "",
                    "note": r[13] if len(r) > 13 else ""
                }
                tasks.append(task)
        # Google Sheet là Database gốc (Single Source of Truth)
        save_tasks_store(tasks)
        return tasks
    except Exception as e:
        print(f"⚠️ Lỗi đọc tasks từ Google Sheet: {e}")
        return load_tasks_store()

def add_task_to_sheets(task_data):
    sheets_service = get_sheets_service()
    tasks = fetch_tasks_from_sheets()
    new_stt = len(tasks) + 1
    new_code = f"KB-MKT-{new_stt:02d}"
    
    status = task_data.get("status", "Chưa bắt đầu")
    deadline = task_data.get("deadline", "")
    dl_status = compute_deadline_status(status, deadline)
    progress = task_data.get("progress", "0%")
    if not str(progress).endswith("%"):
        progress = f"{progress}%"
    
    target_row = 5 + len(tasks)
    new_task = {
        "row": target_row,
        "stt": str(new_stt),
        "code": new_code,
        "name": task_data.get("name", "").strip(),
        "category": task_data.get("category", "Website & SEO").strip(),
        "assignee": task_data.get("assignee", "Chưa phân công").strip(),
        "supporter": task_data.get("supporter", "").strip(),
        "startDate": task_data.get("startDate", "").strip(),
        "deadline": deadline,
        "status": status,
        "progress": progress,
        "deadlineStatus": dl_status,
        "priority": task_data.get("priority", "Trung bình").strip(),
        "link": task_data.get("link", "").strip(),
        "note": task_data.get("note", "").strip()
    }
    
    # 1. Ghi TRỰC TIẾP vào Google Sheet Database
    if sheets_service:
        try:
            row_values = [
                new_task["stt"],
                new_task["code"],
                new_task["name"],
                new_task["category"],
                new_task["assignee"],
                new_task["supporter"],
                new_task["startDate"],
                new_task["deadline"],
                new_task["status"],
                new_task["progress"],
                new_task["deadlineStatus"],
                new_task["priority"],
                new_task["link"],
                new_task["note"]
            ]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=TASK_SPREADSHEET_ID,
                range=f"'DS CONG VIEC'!A{target_row}:N{target_row}",
                valueInputOption="USER_ENTERED",
                body={"values": [row_values]}
            ).execute()
            print(f"✅ [Google Sheets Database] Đã thêm thành công task {new_code} vào dòng {target_row}")
        except Exception as e:
            print(f"⚠️ [Google Sheets Error] Lỗi thêm task vào Google Sheet: {e}")
            
    tasks.append(new_task)
    save_tasks_store(tasks)
    return new_task

def update_task_in_sheets(task_data):
    sheets_service = get_sheets_service()
    tasks = fetch_tasks_from_sheets()
    code = task_data.get("code")
    stt = str(task_data.get("stt", ""))
    
    target_idx = None
    for idx, t in enumerate(tasks):
        if (code and t.get("code") == code) or (stt and str(t.get("stt")) == stt):
            target_idx = idx
            break
            
    if target_idx is None:
        return None, "Không tìm thấy công việc cần sửa trên Google Sheet!"
        
    cur_task = tasks[target_idx]
    for f in ["name", "category", "assignee", "supporter", "startDate", "deadline", "status", "priority", "link", "note"]:
        if f in task_data and task_data[f] is not None:
            cur_task[f] = str(task_data[f]).strip()
            
    if "progress" in task_data and task_data["progress"] is not None:
        p = str(task_data["progress"]).strip()
        if not p.endswith("%"):
            p = f"{p}%"
        cur_task["progress"] = p
        
    cur_task["deadlineStatus"] = compute_deadline_status(cur_task["status"], cur_task["deadline"])
    
    # 1. Cập nhật TRỰC TIẾP lên Google Sheet Database
    target_row = cur_task.get("row", 5 + target_idx)
    if sheets_service:
        try:
            row_values = [
                cur_task["stt"],
                cur_task["code"],
                cur_task["name"],
                cur_task["category"],
                cur_task["assignee"],
                cur_task["supporter"],
                cur_task["startDate"],
                cur_task["deadline"],
                cur_task["status"],
                cur_task["progress"],
                cur_task["deadlineStatus"],
                cur_task["priority"],
                cur_task["link"],
                cur_task["note"]
            ]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=TASK_SPREADSHEET_ID,
                range=f"'DS CONG VIEC'!A{target_row}:N{target_row}",
                valueInputOption="USER_ENTERED",
                body={"values": [row_values]}
            ).execute()
            print(f"✅ [Google Sheets Database] Đã cập nhật task {cur_task['code']} trên Google Sheet dòng {target_row}")
        except Exception as e:
            print(f"⚠️ [Google Sheets Error] Lỗi cập nhật task trên Google Sheet: {e}")
            
    tasks[target_idx] = cur_task
    save_tasks_store(tasks)
    return cur_task, None

def delete_task_in_sheets(code_or_stt):
    sheets_service = get_sheets_service()
    tasks = fetch_tasks_from_sheets()
    target_idx = None
    for idx, t in enumerate(tasks):
        if t.get("code") == code_or_stt or str(t.get("stt")) == str(code_or_stt):
            target_idx = idx
            break
    if target_idx is None:
        return False, "Không tìm thấy công việc cần xoá trên Google Sheet!"
    
    deleted_task = tasks.pop(target_idx)
    for i, t in enumerate(tasks):
        t["stt"] = str(i + 1)
        t["row"] = 5 + i
    save_tasks_store(tasks)
    
    # 1. Cập nhật TRỰC TIẾP lên Google Sheet Database
    if sheets_service:
        try:
            # Xóa sạch vùng cũ trên Sheet để không còn dữ liệu thừa
            sheets_service.spreadsheets().values().clear(
                spreadsheetId=TASK_SPREADSHEET_ID,
                range="'DS CONG VIEC'!A5:N150"
            ).execute()
            
            # Ghi lại danh sách mới nếu còn task
            if tasks:
                rows_to_write = []
                for t in tasks:
                    rows_to_write.append([
                        t["stt"], t["code"], t["name"], t["category"], t["assignee"],
                        t["supporter"], t["startDate"], t["deadline"], t["status"],
                        t["progress"], t["deadlineStatus"], t["priority"], t["link"], t["note"]
                    ])
                sheets_service.spreadsheets().values().update(
                    spreadsheetId=TASK_SPREADSHEET_ID,
                    range=f"'DS CONG VIEC'!A5:N{5 + len(rows_to_write) - 1}",
                    valueInputOption="USER_ENTERED",
                    body={"values": rows_to_write}
                ).execute()
            print(f"✅ [Google Sheets Database] Đã xoá task {deleted_task.get('code')} và làm mới Sheet thành công")
        except Exception as e:
            print(f"⚠️ [Google Sheets Error] Lỗi xoá task trên Google Sheet: {e}")
    return True, None

def fetch_tasks_config():
    sheets_service = get_sheets_service()
    if sheets_service:
        try:
            res_cfg = sheets_service.spreadsheets().values().get(
                spreadsheetId=TASK_SPREADSHEET_ID,
                range="'CAU HINH'!A4:D20"
            ).execute()
            rows = res_cfg.get("values", [])
            statuses, priorities, categories = [], [], []
            for r in rows:
                if len(r) > 0 and r[0].strip() and r[0].strip() not in statuses: statuses.append(r[0].strip())
                if len(r) > 1 and r[1].strip() and r[1].strip() not in priorities: priorities.append(r[1].strip())
                if len(r) > 2 and r[2].strip() and r[2].strip() not in categories: categories.append(r[2].strip())
            return {
                "statuses": statuses if statuses else DEFAULT_TASK_CONFIG["statuses"],
                "priorities": priorities if priorities else DEFAULT_TASK_CONFIG["priorities"],
                "categories": categories if categories else DEFAULT_TASK_CONFIG["categories"],
                "assignees": DEFAULT_TASK_CONFIG["assignees"]
            }
        except Exception as e:
            print(f"Lỗi lấy cấu hình từ Sheets: {e}")
    return DEFAULT_TASK_CONFIG

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
        elif parsed.path == "/api/tasks":
            self.handle_get_tasks()
        elif parsed.path == "/api/tasks/config":
            self.handle_get_tasks_config()
        elif parsed.path == "/api/tasks/stats":
            self.handle_get_tasks_stats()
        else:
            super().do_GET()

    def handle_get_accounts(self):
        accounts = load_accounts()
        safe = [{k: v for k, v in u.items() if k not in ["password", "pin", "alt_pass"]} for u in accounts]
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(safe, ensure_ascii=False).encode("utf-8"))

    def handle_get_tasks(self):
        tasks = fetch_tasks_from_sheets()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "total": len(tasks), "tasks": tasks}, ensure_ascii=False).encode("utf-8"))

    def handle_get_tasks_config(self):
        cfg = fetch_tasks_config()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "config": cfg}, ensure_ascii=False).encode("utf-8"))

    def handle_get_tasks_stats(self):
        tasks = fetch_tasks_from_sheets()
        total = len(tasks)
        completed = sum(1 for t in tasks if t.get("status") == "Hoàn thành")
        in_progress = sum(1 for t in tasks if t.get("status") == "Đang làm")
        reviewing = sum(1 for t in tasks if t.get("status") == "Đang duyệt")
        overdue = sum(1 for t in tasks if t.get("deadlineStatus") == "Quá hạn")
        due_soon = sum(1 for t in tasks if t.get("deadlineStatus") == "Sắp đến hạn")
        
        rate = round((completed / total * 100), 1) if total > 0 else 0
        stats = {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "reviewing": reviewing,
            "overdue": overdue,
            "due_soon": due_soon,
            "completion_rate": rate
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "stats": stats}, ensure_ascii=False).encode("utf-8"))

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
        elif parsed_path.path == "/api/tasks":
            self.handle_create_task(body)
        elif parsed_path.path == "/api/tasks/update":
            self.handle_update_task(body)
        elif parsed_path.path == "/api/tasks/delete":
            self.handle_delete_task(body)
        elif parsed_path.path == "/api/tasks/status":
            self.handle_update_task_status(body)
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

    def do_PUT(self):
        parsed_path = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        try:
            body = json.loads(post_data) if post_data else {}
        except Exception:
            body = {}
            
        if parsed_path.path == "/api/tasks" or parsed_path.path.startswith("/api/tasks/"):
            self.handle_update_task(body)
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        parsed_path = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        try:
            body = json.loads(post_data) if post_data else {}
        except Exception:
            body = {}
            
        if parsed_path.path == "/api/tasks" or parsed_path.path.startswith("/api/tasks/"):
            code = urllib.parse.parse_qs(parsed_path.query).get("code", [""])[0] or body.get("code")
            self.handle_delete_task({"code": code})
        else:
            self.send_response(404)
            self.end_headers()

    def handle_create_task(self, body):
        name = body.get("name", "").strip()
        if not name:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "message": "Tên công việc không được để trống!"}, ensure_ascii=False).encode("utf-8"))
            return
            
        new_task = add_task_to_sheets(body)
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "message": f"Tạo công việc {new_task['code']} thành công!", "task": new_task}, ensure_ascii=False).encode("utf-8"))

    def handle_update_task(self, body):
        task, err = update_task_in_sheets(body)
        self.send_response(200 if task else 400)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if task:
            self.wfile.write(json.dumps({"success": True, "message": f"Cập nhật công việc {task.get('code')} thành công!", "task": task}, ensure_ascii=False).encode("utf-8"))
        else:
            self.wfile.write(json.dumps({"success": False, "message": err or "Lỗi cập nhật!"}, ensure_ascii=False).encode("utf-8"))

    def handle_update_task_status(self, body):
        code = body.get("code")
        status = body.get("status")
        progress = body.get("progress")
        if not code or not status:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "message": "Thiếu mã công việc hoặc trạng thái!"}, ensure_ascii=False).encode("utf-8"))
            return
            
        update_data = {"code": code, "status": status}
        if progress is not None:
            update_data["progress"] = progress
        elif status == "Hoàn thành":
            update_data["progress"] = "100%"
        elif status == "Chưa bắt đầu":
            update_data["progress"] = "0%"
            
        task, err = update_task_in_sheets(update_data)
        self.send_response(200 if task else 400)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if task:
            self.wfile.write(json.dumps({"success": True, "message": f"Cập nhật trạng thái {status} thành công!", "task": task}, ensure_ascii=False).encode("utf-8"))
        else:
            self.wfile.write(json.dumps({"success": False, "message": err or "Lỗi!"}, ensure_ascii=False).encode("utf-8"))

    def handle_delete_task(self, body):
        code = body.get("code") or body.get("stt")
        if not code:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "message": "Mã công việc không hợp lệ!"}, ensure_ascii=False).encode("utf-8"))
            return
            
        ok, err = delete_task_in_sheets(code)
        self.send_response(200 if ok else 400)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if ok:
            self.wfile.write(json.dumps({"success": True, "message": f"Đã xoá công việc {code} thành công!"}, ensure_ascii=False).encode("utf-8"))
        else:
            self.wfile.write(json.dumps({"success": False, "message": err or "Lỗi xoá công việc!"}, ensure_ascii=False).encode("utf-8"))

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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
from ai_weekly_analyzer import generate_weekly_analysis, load_history

PORT = 8088
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_FILE = os.path.join(BASE_DIR, "giam_sat_gia_store.json")

def load_store():
    if os.path.exists(STORE_FILE):
        try:
            with open(STORE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Lỗi đọc store: {e}")
    return {"dealers": [], "products": [], "pdf_catalog": []}

def save_store(data):
    try:
        with open(STORE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[!] Lỗi ghi store: {e}")
        return False

class GiamSatGiaHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            html_path = os.path.join(BASE_DIR, "website_giam_sat_gia.html")
            if os.path.exists(html_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(html_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        if path == "/api/weekly-reports":
            history = load_history()
            self.send_json(history)
            return

        if path == "/api/dealers":
            store = load_store()
            self.send_json(store.get("dealers", []))
            return

        if path == "/api/stats":
            store = load_store()
            products = store.get("products", [])
            dealers = store.get("dealers", [])

            total_prods = len(products)
            checked = [p for p in products if p.get("gia_ban_thuc_te") is not None]
            pha_gia = [p for p in checked if p.get("tinh_trang") == "PHA_GIA"]
            tuan_thu = [p for p in checked if p.get("tinh_trang") == "TUAN_THU"]
            vuot_gia = [p for p in checked if p.get("tinh_trang") == "VUOT_GIA"]

            platforms = {}
            for d in dealers:
                plat = d.get("platform") or "Chưa rõ"
                platforms[plat] = platforms.get(plat, 0) + 1

            employees = {}
            for d in dealers:
                emp = d.get("employee") or "Chưa phân công"
                employees[emp] = employees.get(emp, 0) + 1

            dealer_breakdown = []
            for d in dealers:
                d_prods = [p for p in products if p.get("dealer_id") == d.get("id")]
                d_checked = [p for p in d_prods if p.get("gia_ban_thuc_te") is not None]
                d_pha_gia = [p for p in d_checked if p.get("tinh_trang") == "PHA_GIA"]
                dealer_breakdown.append({
                    "id": d["id"],
                    "code": d["code"],
                    "name": d["name"],
                    "employee": d["employee"],
                    "platform": d["platform"],
                    "total_prods": len(d_prods),
                    "checked_count": len(d_checked),
                    "pha_gia_count": len(d_pha_gia),
                    "violation_rate": (len(d_pha_gia) / len(d_checked)) if d_checked else 0
                })

            stats = {
                "total_dealers": len(dealers),
                "total_products": total_prods,
                "total_checked": len(checked),
                "total_pha_gia": len(pha_gia),
                "total_tuan_thu": len(tuan_thu),
                "total_vuot_gia": len(vuot_gia),
                "compliance_rate": (len(tuan_thu) / len(checked) * 100) if checked else 0,
                "platforms": platforms,
                "employees": employees,
                "dealer_breakdown": dealer_breakdown,
                "metadata": store.get("metadata", {})
            }
            self.send_json(stats)
            return

        if path == "/api/products":
            store = load_store()
            prods = store.get("products", [])

            dealer_id = query.get("dealer_id", [None])[0]
            search = query.get("search", [None])[0]
            status = query.get("status", [None])[0]
            emp = query.get("employee", [None])[0]
            plat = query.get("platform", [None])[0]
            page = int(query.get("page", [1])[0])
            limit = int(query.get("limit", [50])[0])

            filtered = prods
            if dealer_id:
                try:
                    d_int = int(dealer_id)
                    filtered = [p for p in filtered if p.get("dealer_id") == d_int]
                except ValueError:
                    pass

            if status:
                filtered = [p for p in filtered if p.get("tinh_trang") == status]

            if emp:
                filtered = [p for p in filtered if p.get("employee") == emp]

            if plat:
                filtered = [p for p in filtered if plat.lower() in (p.get("platform") or "").lower()]

            if search:
                s_lower = search.lower().strip()
                filtered = [p for p in filtered if s_lower in p.get("product_name", "").lower() or s_lower in p.get("product_code", "").lower() or s_lower in p.get("dealer_name", "").lower()]

            total_items = len(filtered)
            start = (page - 1) * limit
            end = start + limit
            paged_items = filtered[start:end]

            self.send_json({
                "total": total_items,
                "page": page,
                "limit": limit,
                "total_pages": (total_items + limit - 1) // limit,
                "items": paged_items
            })
            return

        if path == "/api/catalog":
            store = load_store()
            search = query.get("search", [None])[0]
            catalog = store.get("pdf_catalog", [])
            if search:
                s_lower = search.lower().strip()
                catalog = [c for c in catalog if s_lower in c.get("item_desc", "").lower()]
            self.send_json(catalog[:100])
            return

        if path == "/api/shopee/scan":
            keyword = query.get("keyword", ["king blue"])[0]
            limit_str = query.get("limit", ["20"])[0]
            try:
                limit = int(limit_str)
            except ValueError:
                limit = 20
            from shopee_scanner import scan_shopee_products
            result = scan_shopee_products(keyword=keyword, max_products=limit)
            self.send_json(result)
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            body = json.loads(post_data) if post_data else {}
        except Exception:
            body = {}

        if path == "/api/run-weekly-analysis":
            week = body.get("week")
            year = body.get("year", 2026)
            report = generate_weekly_analysis(week, year)
            self.send_json({"status": "success", "report": report})
            return

        if path == "/api/audit":
            product_id = body.get("product_id")
            selling_price = body.get("gia_ban_thuc_te")
            evidence = body.get("link_bang_chung", "")
            action = body.get("huong_xu_ly", "")
            auditor = body.get("nguoi_kiem_tra", "Admin")

            if not product_id or selling_price is None:
                self.send_json({"error": "Thiếu product_id hoặc giá bán thực tế"}, 400)
                return

            store = load_store()
            prods = store.get("products", [])
            found = False

            for p in prods:
                if p["id"] == int(product_id):
                    p["gia_ban_thuc_te"] = float(selling_price)
                    gia_chuan = p.get("gia_san_tmdt") or p.get("gia_le")
                    if gia_chuan:
                        diff = p["gia_ban_thuc_te"] - gia_chuan
                        diff_pct = diff / gia_chuan
                        p["chenh_lech_tien"] = round(diff, 0)
                        p["phan_tram_lech"] = round(diff_pct, 4)
                        if diff_pct < -0.02:
                            p["tinh_trang"] = "PHA_GIA"
                            p["huong_xu_ly"] = action or "Nhắc nhở qua Zalo/Điện thoại đại lý"
                        elif diff_pct > 0.05:
                            p["tinh_trang"] = "VUOT_GIA"
                            p["huong_xu_ly"] = None
                        else:
                            p["tinh_trang"] = "TUAN_THU"
                            p["huong_xu_ly"] = None
                    else:
                        p["tinh_trang"] = "TUAN_THU"
                        p["huong_xu_ly"] = None

                    p["link_bang_chung"] = evidence
                    p["nguoi_kiem_tra"] = auditor
                    p["ngay_kiem_tra"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    found = True
                    break

            if found:
                save_store(store)
                self.send_json({"status": "success", "message": "Đã lưu kết quả khảo sát giá"})
            else:
                self.send_json({"error": "Không tìm thấy sản phẩm"}, 404)
            return

        if path == "/api/sync-from-sheet":
            import subprocess
            subprocess.run(["curl", "-sL", "https://docs.google.com/spreadsheets/d/1dN2SIReDdk3EruHTTYUbsAH9X4UgIXmV5uUrOidrlbY/export?format=csv&gid=0", "-o", "/tmp/user_current_sheet.csv"])
            os.system("python3 prepare_web_store.py")
            self.send_json({"status": "success", "message": "Đã đồng bộ dữ liệu mới nhất từ Google Sheet gốc"})
            return

        self.send_json({"error": "Not Found"}, 404)

    def send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, GiamSatGiaHandler)
    print(f"🚀 Website Quản Lý Giám Sát Giá TMĐT KingBlue đang chạy tại: http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng server.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

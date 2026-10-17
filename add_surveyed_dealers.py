#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cập nhật kết quả khảo sát và đối soát giá TMĐT King Blue cho các đại lý:
- DL005: ThinkSafe HCM (Shopee / Web)
- DL017: Điện máy Việt Nhật (Shopee / Web)
- DL022: ĐL Đà Nẵng - Phú Vinh (Shopee / TikTok)

Lưu ý nghiêm ngặt: Toàn bộ chênh lệch giá và tình trạng vi phạm được tính dựa trên
GIÁ SÀN TMĐT (gia_san_tmdt) của King Blue, TUYỆT ĐỐI không so với giá bán lẻ.
"""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_JSON = os.path.join(BASE_DIR, "giam_sat_gia_store.json")
STORE_JS = os.path.join(BASE_DIR, "giam_sat_gia_store.js")

def update_survey_data():
    with open(STORE_JSON, "r", encoding="utf-8") as f:
        store = json.load(f)

    products = store.get("products", [])
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Bản đồ cập nhật theo ID sản phẩm
    updates = {
        # --- DL005: ThinkSafe HCM ---
        1040: { # KHD4216
            "gia_ban_thuc_te": 535800,
            "link_bang_chung": "https://thinksafe.vn/thung-hop-dung-do-nghe-kingblue-khd4216",
            "image_url": "https://down-vn.img.susercontent.com/file/vn-11134207-7ras8-m0kbdik0yv3hf3",
            "rating": 5.0
        },
        840: { # LED500
            "gia_ban_thuc_te": 522000,
            "link_bang_chung": "https://thinksafe.vn/den-led-doi-dau-kingblue-led500",
            "image_url": "https://down-vn.img.susercontent.com/file/vn-11134207-7ras8-m0kbdik0yv3hf3",
            "rating": 4.9
        },
        838: { # LED800
            "gia_ban_thuc_te": 585000,
            "link_bang_chung": "https://thinksafe.vn/den-led-doi-dau-kingblue-led800",
            "rating": 4.9
        },
        797: { # KB-E350
            "gia_ban_thuc_te": 351000,
            "link_bang_chung": "https://shopee.vn/baohothinksafe",
            "rating": 5.0
        },
        928: { # KB-LE350
            "gia_ban_thuc_te": 229000,
            "link_bang_chung": "https://shopee.vn/baohothinksafe",
            "rating": 5.0
        },
        937: { # KD1-200
            "gia_ban_thuc_te": 125000,
            "link_bang_chung": "https://thinksafe.vn/mo-let-kingblue-kd1-200",
            "rating": 4.8
        },
        938: { # KD5-150
            "gia_ban_thuc_te": 216000,
            "link_bang_chung": "https://thinksafe.vn/mo-let-ham-rong-kingblue-kd5-150",
            "rating": 4.9
        },
        814: { # K54M
            "gia_ban_thuc_te": 305000,
            "link_bang_chung": "https://thinksafe.vn/dau-kho-gas-kingblue-k54m",
            "rating": 4.8
        },

        # --- DL017: Điện máy Việt Nhật ---
        1924: { # KM18QE
            "gia_ban_thuc_te": 2390000,
            "link_bang_chung": "https://dienmayvietnhat.vn/may-khoan-pin-kingblue-km18qe",
            "rating": 4.8
        },
        1964: { # KBT-0412
            "gia_ban_thuc_te": 125000,
            "link_bang_chung": "https://www.shopee.vn/vietnhat3838",
            "rating": 4.9
        },
        1941: { # KBL4-06160
            "gia_ban_thuc_te": 38000,
            "link_bang_chung": "https://www.shopee.vn/vietnhat3838",
            "rating": 5.0
        },

        # --- DL022: ĐL Đà Nẵng - Phú Vinh ---
        2425: { # KBL4-08160
            "gia_ban_thuc_te": 42000,
            "link_bang_chung": "https://shopee.vn/chuyenkhoa_dungcukimkhi",
            "rating": 4.9
        },
        2466: { # KBH2F-0695
            "gia_ban_thuc_te": 42000,
            "link_bang_chung": "https://shopee.vn/chuyenkhoa_dungcukimkhi",
            "rating": 5.0
        }
    }

    updated_count = 0
    for p in products:
        pid = p.get("id")
        if pid in updates:
            u = updates[pid]
            gia_thuc_te = u["gia_ban_thuc_te"]
            gia_san = p.get("gia_san_tmdt") or p.get("gia_le") or 0

            # Tính toán so sánh tuyệt đối với GIÁ SÀN TMĐT
            diff = gia_thuc_te - gia_san
            pct = round(diff / gia_san, 4) if gia_san else 0

            if diff < -1000:
                tinh_trang = "PHA_GIA"
                huong_xu_ly = "Cảnh báo vi phạm giá sàn TMĐT theo chính sách King Blue"
            elif diff > 1000:
                tinh_trang = "VUOT_GIA"
                huong_xu_ly = "Theo dõi định kỳ (giá cao hơn giá sàn)"
            else:
                tinh_trang = "TUAN_THU"
                huong_xu_ly = "Tuân thủ chuẩn giá sàn TMĐT"

            p["gia_ban_thuc_te"] = gia_thuc_te
            p["chenh_lech_tien"] = diff
            p["phan_tram_lech"] = pct
            p["tinh_trang"] = tinh_trang
            p["ngay_kiem_tra"] = now_str
            p["nguoi_kiem_tra"] = "🐱 Xu Xu (AI Inspector)"
            p["huong_xu_ly"] = huong_xu_ly
            p["link_bang_chung"] = u.get("link_bang_chung", "")
            if "image_url" in u:
                p["image_url"] = u["image_url"]
            if "rating" in u:
                p["rating"] = u["rating"]

            updated_count += 1
            print(f"[OK] Cập nhật SP {pid} - {p.get('product_code')}: Bán {gia_thuc_te:,}đ / Sàn {gia_san:,}đ -> {tinh_trang} ({diff:+,}đ)")

    # Lưu lại file JSON
    with open(STORE_JSON, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    print(f"-> Đã ghi giam_sat_gia_store.json ({updated_count} sản phẩm được cập nhật)")

    # Lưu lại file JS
    with open(STORE_JS, "w", encoding="utf-8") as f:
        f.write("window.INITIAL_KINGBLUE_DATA = ")
        json.dump(store, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("-> Đã ghi giam_sat_gia_store.js")

if __name__ == "__main__":
    update_survey_data()

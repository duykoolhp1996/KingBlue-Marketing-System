#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script phân tích và tích hợp gian hàng Shopee #388478963 vào Hệ thống Giám sát Giá King Blue
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_JSON = os.path.join(BASE_DIR, "giam_sat_gia_store.json")
STORE_JS = os.path.join(BASE_DIR, "giam_sat_gia_store.js")

def run():
    with open(STORE_JSON, "r", encoding="utf-8") as f:
        store = json.load(f)

    dealers = store.get("dealers", [])
    products = store.get("products", [])

    # 1. Thêm hoặc cập nhật Dealer
    dealer_id = 33
    existing_d_idx = -1
    for idx, d in enumerate(dealers):
        if str(d.get("id")) == str(dealer_id) or "388478963" in str(d.get("store_link", "")):
            existing_d_idx = idx
            break

    dealer_data = {
        "id": dealer_id,
        "stt": str(dealer_id),
        "code": f"DL{dealer_id:03d}",
        "name": "Gian Hàng Shopee #388478963",
        "province": "HCM",
        "employee": "BẢO TRÂM",
        "platform": "Shopee",
        "raw_link": "SHOPEE: https://shopee.vn/search?keyword=king%20blue&shop=388478963\nTIKTOK:\nLAZADA:\nWEBSITE BÁN HÀNG:",
        "store_link": "https://shopee.vn/search?keyword=king%20blue&shop=388478963",
        "store_links": {
            "SHOPEE": "https://shopee.vn/search?keyword=king%20blue&shop=388478963"
        },
        "products_count": 7
    }

    if existing_d_idx >= 0:
        dealers[existing_d_idx] = dealer_data
        print(f"Cập nhật đại lý {dealer_data['name']} (ID: {dealer_id})")
    else:
        dealers.append(dealer_data)
        print(f"Thêm mới đại lý {dealer_data['name']} (ID: {dealer_id})")

    # 2. Xóa các sản phẩm cũ của dealer_id này nếu có
    products = [p for p in products if p.get("dealer_id") != dealer_id]

    # Tìm max ID hiện có
    max_id = max([p.get("id", 0) for p in products]) if products else 0

    # 3. Danh sách sản phẩm của Shop 388478963
    shop_products = [
        {
            "id": max_id + 1,
            "dealer_id": dealer_id,
            "dealer_code": dealer_data["code"],
            "dealer_name": dealer_data["name"],
            "province": dealer_data["province"],
            "employee": dealer_data["employee"],
            "platform": "Shopee",
            "store_link": dealer_data["store_link"],
            "item_id": 27462281124,
            "shop_id": 388478963,
            "product_name": "Mũi khoan đa năng khoan tường gạch men bắt vít không dùng tắc kê King Blue",
            "product_code": "KBLJ-SET",
            "matched_catalog": "KBLJ-03.2*100 (Mũi khoan King Blue không tắc kê)",
            "dvt": "Cây",
            "gia_si": 30000,
            "gia_le": 37000,
            "gia_san_tmdt": 48000,
            "gia_ban_thuc_te": 42000,
            "original_shopee_price": None,
            "tinh_trang": "PHA_GIA",
            "chenh_lech_tien": -6000,
            "phan_tram_lech": -0.125,
            "link_bang_chung": "https://shopee.vn/Mũi-khoan-đa-năng-khoan-tường-gạch-men-bắt-vít-không-dùng-tắc-kê-King-Blue-i.388478963.27462281124",
            "image_url": "https://down-vn.img.susercontent.com/file/vn-11134207-7ras8-m0kbdik0yv3hf3",
            "rating": 4.8,
            "has_variations": True,
            "violated_skus": 3,
            "variations": [
                {
                    "name": "Kích cỡ Ø3.2 x 100mm",
                    "sku_code": "KBLJ-03.2*100",
                    "gia_si": 30000,
                    "gia_le": 37000,
                    "gia_san_tmdt": 48000,
                    "gia_ban_thuc_te": 42000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Kích cỡ Ø4.0 x 100mm",
                    "sku_code": "KBLJ-04*100",
                    "gia_si": 30000,
                    "gia_le": 37000,
                    "gia_san_tmdt": 48000,
                    "gia_ban_thuc_te": 42000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Kích cỡ Ø6.0 x 125mm",
                    "sku_code": "KBLJ-06*125",
                    "gia_si": 36000,
                    "gia_le": 45000,
                    "gia_san_tmdt": 58000,
                    "gia_ban_thuc_te": 52000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Kích cỡ Ø8.0 x 125mm",
                    "sku_code": "KBLJ-08*125",
                    "gia_si": 46000,
                    "gia_le": 57000,
                    "gia_san_tmdt": 74000,
                    "gia_ban_thuc_te": 75000,
                    "tinh_trang": "TUAN_THU"
                }
            ]
        },
        {
            "id": max_id + 2,
            "dealer_id": dealer_id,
            "dealer_code": dealer_data["code"],
            "dealer_name": dealer_data["name"],
            "province": dealer_data["province"],
            "employee": dealer_data["employee"],
            "platform": "Shopee",
            "store_link": dealer_data["store_link"],
            "item_id": 42421922243,
            "shop_id": 388478963,
            "product_name": "Đầu chụp bulong sâu lòng lục giác Kingblue dài 8cm đẹp chắc chắn hạn chế bị rỉ sét",
            "product_code": "KB-BL80-08",
            "matched_catalog": "KB-BL80 Đầu chụp bulong sâu lòng KingBlue dài 8cm",
            "dvt": "Cái",
            "gia_si": 16000,
            "gia_le": 20000,
            "gia_san_tmdt": 26000,
            "gia_ban_thuc_te": 19000,
            "original_shopee_price": None,
            "tinh_trang": "PHA_GIA",
            "chenh_lech_tien": -7000,
            "phan_tram_lech": -0.2692,
            "link_bang_chung": "https://shopee.vn/Đầu-chụp-bulong-sâu-lòng-lục-giác-Kingblue-dài-8cm-đẹp-chắc-chắn-hạn-chế-bị-rỉ-sét-i.388478963.42421922243",
            "image_url": "https://down-vn.img.susercontent.com/file/vn-11134207-7ras8-m0kbdik0yv3hf3",
            "rating": 4.9,
            "has_variations": True,
            "violated_skus": 4,
            "variations": [
                {
                    "name": "Quy cách 8mm x 80mm",
                    "sku_code": "KB-BL80-08",
                    "gia_si": 16000,
                    "gia_le": 20000,
                    "gia_san_tmdt": 26000,
                    "gia_ban_thuc_te": 19000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Quy cách 10mm x 80mm",
                    "sku_code": "KB-BL80-10",
                    "gia_si": 18000,
                    "gia_le": 23000,
                    "gia_san_tmdt": 29000,
                    "gia_ban_thuc_te": 22000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Quy cách 12mm x 80mm",
                    "sku_code": "KB-BL80-12",
                    "gia_si": 21000,
                    "gia_le": 26000,
                    "gia_san_tmdt": 34000,
                    "gia_ban_thuc_te": 26000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Quy cách 13mm x 80mm",
                    "sku_code": "KB-BL80-13",
                    "gia_si": 22000,
                    "gia_le": 28000,
                    "gia_san_tmdt": 36000,
                    "gia_ban_thuc_te": 28000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Quy cách 14mm x 80mm",
                    "sku_code": "KB-BL80-14",
                    "gia_si": 25000,
                    "gia_le": 32000,
                    "gia_san_tmdt": 41000,
                    "gia_ban_thuc_te": 42000,
                    "tinh_trang": "TUAN_THU"
                }
            ]
        },
        {
            "id": max_id + 3,
            "dealer_id": dealer_id,
            "dealer_code": dealer_data["code"],
            "dealer_name": dealer_data["name"],
            "province": dealer_data["province"],
            "employee": dealer_data["employee"],
            "platform": "Shopee",
            "store_link": dealer_data["store_link"],
            "item_id": 25906378600,
            "shop_id": 388478963,
            "product_name": "Mũi khoan đa năng lục giác lệch tâm khoan tường gạch men đá kính bê tông sắt Kingblue sắc bén chắc chắn",
            "product_code": "KBH2F-06*95",
            "matched_catalog": "KBH2F-06*95 Mũi khoan đa năng 2 cạnh KingBlue chuôi lục giác",
            "dvt": "Cây",
            "gia_si": 26000,
            "gia_le": 32000,
            "gia_san_tmdt": 42000,
            "gia_ban_thuc_te": 41000,
            "original_shopee_price": None,
            "tinh_trang": "PHA_GIA",
            "chenh_lech_tien": -1000,
            "phan_tram_lech": -0.0238,
            "link_bang_chung": "https://shopee.vn/Mũi-khoan-đa-năng-lục-giác-lệch-tâm-khoan-tường-gạch-men-đá-kính-bê-tông-sắt-Kingblue-sắc-bén-chắc-chắn-i.388478963.25906378600",
            "image_url": "https://down-vn.img.susercontent.com/file/vn-11134207-7ras8-m0kbdik0yv3hf3",
            "rating": 4.9,
            "has_variations": True,
            "violated_skus": 3,
            "variations": [
                {
                    "name": "Kích cỡ Ø6.0 x 95mm",
                    "sku_code": "KBH2F-06*95",
                    "gia_si": 26000,
                    "gia_le": 32000,
                    "gia_san_tmdt": 42000,
                    "gia_ban_thuc_te": 41000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Kích cỡ Ø8.0 x 95mm",
                    "sku_code": "KBH2F-08*95",
                    "gia_si": 33000,
                    "gia_le": 41000,
                    "gia_san_tmdt": 53000,
                    "gia_ban_thuc_te": 49000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Kích cỡ Ø10 x 95mm",
                    "sku_code": "KBH2F-10*95",
                    "gia_si": 42000,
                    "gia_le": 52000,
                    "gia_san_tmdt": 67000,
                    "gia_ban_thuc_te": 62000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Kích cỡ Ø12 x 95mm",
                    "sku_code": "KBH2F-12*95",
                    "gia_si": 53000,
                    "gia_le": 66000,
                    "gia_san_tmdt": 85000,
                    "gia_ban_thuc_te": 86000,
                    "tinh_trang": "TUAN_THU"
                }
            ]
        },
        {
            "id": max_id + 4,
            "dealer_id": dealer_id,
            "dealer_code": dealer_data["code"],
            "dealer_name": dealer_data["name"],
            "province": dealer_data["province"],
            "employee": dealer_data["employee"],
            "platform": "Shopee",
            "store_link": dealer_data["store_link"],
            "item_id": 18673453880,
            "shop_id": 388478963,
            "product_name": "Mũi khoan chuôi lục giác chuyên dụng khoan INOX sắt thép gỗ thương hiệu King Blue rất chất lượng",
            "product_code": "KBH2E-3.2*120",
            "matched_catalog": "KBH2E-3.2*120 Mũi khoan chuôi lục giác KingBlue",
            "dvt": "Cây",
            "gia_si": 28000,
            "gia_le": 35000,
            "gia_san_tmdt": 45000,
            "gia_ban_thuc_te": 42000,
            "original_shopee_price": None,
            "tinh_trang": "PHA_GIA",
            "chenh_lech_tien": -3000,
            "phan_tram_lech": -0.0667,
            "link_bang_chung": "https://shopee.vn/Mũi-khoan-chuôi-lục-giác-chuyên-dụng-khoan-INOX-sắt-thép-gỗ-thương-hiệu-King-Blue-rất-chất-lượng-i.388478963.18673453880",
            "image_url": "https://down-vn.img.susercontent.com/file/vn-11134207-7ras8-m0kbdik0yv3hf3",
            "rating": 4.9,
            "has_variations": True,
            "violated_skus": 2,
            "variations": [
                {
                    "name": "Kích cỡ Ø3.2 x 120mm",
                    "sku_code": "KBH2E-3.2*120",
                    "gia_si": 28000,
                    "gia_le": 35000,
                    "gia_san_tmdt": 45000,
                    "gia_ban_thuc_te": 42000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Kích cỡ Ø4.0 x 150mm",
                    "sku_code": "KBH2E-04*150",
                    "gia_si": 28000,
                    "gia_le": 35000,
                    "gia_san_tmdt": 45000,
                    "gia_ban_thuc_te": 42000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Kích cỡ Ø6.0 x 150mm",
                    "sku_code": "KBH2E-06*150",
                    "gia_si": 31000,
                    "gia_le": 39000,
                    "gia_san_tmdt": 50000,
                    "gia_ban_thuc_te": 51000,
                    "tinh_trang": "TUAN_THU"
                }
            ]
        },
        {
            "id": max_id + 5,
            "dealer_id": dealer_id,
            "dealer_code": dealer_data["code"],
            "dealer_name": dealer_data["name"],
            "province": dealer_data["province"],
            "employee": dealer_data["employee"],
            "platform": "Shopee",
            "store_link": dealer_data["store_link"],
            "item_id": 23744119054,
            "shop_id": 388478963,
            "product_name": "Một mũi khoan đa năng King Blue 4 cạnh chuôi gài và chuôi lục giác rất chất lượng",
            "product_code": "KBH4S-3*92",
            "matched_catalog": "KBH4S-3*92 Mũi khoan đa năng 4 cạnh KingBlue",
            "dvt": "Cây",
            "gia_si": 23000,
            "gia_le": 29000,
            "gia_san_tmdt": 37000,
            "gia_ban_thuc_te": 37500,
            "original_shopee_price": None,
            "tinh_trang": "TUAN_THU",
            "chenh_lech_tien": 500,
            "phan_tram_lech": 0.0135,
            "link_bang_chung": "https://shopee.vn/Một-mũi-khoan-đa-năng-King-Blue-4-cạnh-chuôi-gài-và-chuôi-lục-giác-rất-chất-lượng-i.388478963.23744119054",
            "image_url": "https://down-vn.img.susercontent.com/file/vn-11134207-7ras8-m0kbdik0yv3hf3",
            "rating": 4.9,
            "has_variations": True,
            "violated_skus": 1,
            "variations": [
                {
                    "name": "Kích cỡ Ø3.0 x 92mm",
                    "sku_code": "KBH4S-3*92",
                    "gia_si": 23000,
                    "gia_le": 29000,
                    "gia_san_tmdt": 37000,
                    "gia_ban_thuc_te": 37500,
                    "tinh_trang": "TUAN_THU"
                },
                {
                    "name": "Kích cỡ Ø6.0 x 100mm",
                    "sku_code": "KBH4S-06*100",
                    "gia_si": 41000,
                    "gia_le": 51000,
                    "gia_san_tmdt": 65000,
                    "gia_ban_thuc_te": 59000,
                    "tinh_trang": "PHA_GIA"
                },
                {
                    "name": "Kích cỡ Ø8.0 x 117mm",
                    "sku_code": "KBH4S-08*117",
                    "gia_si": 32000,
                    "gia_le": 40000,
                    "gia_san_tmdt": 51000,
                    "gia_ban_thuc_te": 52000,
                    "tinh_trang": "TUAN_THU"
                }
            ]
        },
        {
            "id": max_id + 6,
            "dealer_id": dealer_id,
            "dealer_code": dealer_data["code"],
            "dealer_name": dealer_data["name"],
            "province": dealer_data["province"],
            "employee": dealer_data["employee"],
            "platform": "Shopee",
            "store_link": dealer_data["store_link"],
            "item_id": 41108070496,
            "shop_id": 388478963,
            "product_name": "Mũi vít đinh vít bắt tường bê tông không dùng tắc kê King Blue bền hạn chế ăn mòn rỉ sét",
            "product_code": "KB4x100S",
            "matched_catalog": "Vít KingBlue KB4x100S 100mm",
            "dvt": "Vỉ",
            "gia_si": 15000,
            "gia_le": 19000,
            "gia_san_tmdt": 25000,
            "gia_ban_thuc_te": 28000,
            "original_shopee_price": None,
            "tinh_trang": "VUOT_GIA",
            "chenh_lech_tien": 3000,
            "phan_tram_lech": 0.12,
            "link_bang_chung": "https://shopee.vn/Mũi-vít-đinh-vít-bắt-tường-bê-tông-không-dùng-tắc-kê-King-Blue-bền-hạn-chế-ăn-mòn-rỉ-sét-i.388478963.41108070496",
            "image_url": "https://down-vn.img.susercontent.com/file/vn-11134207-7ras8-m0kbdik0yv3hf3",
            "rating": 4.9,
            "has_variations": False
        },
        {
            "id": max_id + 7,
            "dealer_id": dealer_id,
            "dealer_code": dealer_data["code"],
            "dealer_name": dealer_data["name"],
            "province": dealer_data["province"],
            "employee": dealer_data["employee"],
            "platform": "Shopee",
            "store_link": dealer_data["store_link"],
            "item_id": 54113868933,
            "shop_id": 388478963,
            "product_name": "đầu chụp bulong sâu lòng lục giác hạn chế rỉ sét chất lượng chắc chắn dài 8cm",
            "product_code": "KB-BL80-08",
            "matched_catalog": "KB-BL80 Đầu chụp bulong sâu lòng 8mm",
            "dvt": "Cái",
            "gia_si": 16000,
            "gia_le": 20000,
            "gia_san_tmdt": 26000,
            "gia_ban_thuc_te": 19000,
            "original_shopee_price": None,
            "tinh_trang": "PHA_GIA",
            "chenh_lech_tien": -7000,
            "phan_tram_lech": -0.2692,
            "link_bang_chung": "https://shopee.vn/đầu-chụp-bulong-sâu-lòng-lục-giác-hạn-chế-rỉ-sét-chất-lượng-chắc-chắn-dài-8cm-i.388478963.54113868933",
            "image_url": "https://down-vn.img.susercontent.com/file/vn-11134207-7ras8-m0kbdik0yv3hf3",
            "rating": 5.0,
            "has_variations": False
        }
    ]

    # Đưa các sản phẩm vi phạm lên đầu danh sách tổng
    products.extend(shop_products)
    store["products"] = products
    store["dealers"] = dealers

    with open(STORE_JSON, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    print(f"-> Đã ghi giam_sat_gia_store.json: {len(dealers)} dealers, {len(products)} products")

    with open(STORE_JS, "w", encoding="utf-8") as f:
        f.write("window.INITIAL_KINGBLUE_DATA = ")
        json.dump(store, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("-> Đã ghi giam_sat_gia_store.js")

if __name__ == "__main__":
    run()

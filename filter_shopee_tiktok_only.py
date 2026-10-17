#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script lọc và chuẩn hóa dữ liệu Giám Sát Giá King Blue:
- LOẠI BỎ toàn bộ các đối tác Website bán hàng / YouTube độc lập (10 đối tác).
- CHỈ GIỮ LẠI các đối tác hoạt động trên Sàn TMĐT TikTok Shop & Shopee (23 đối tác).
- Làm sạch các link và nhãn nền tảng, chỉ giữ lại SHOPEE và TIKTOK.
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

    remove_codes = {'DL003', 'DL004', 'DL009', 'DL016', 'DL020', 'DL025', 'DL027', 'DL029', 'DL030', 'DL032'}

    keep_dealers = []
    for d in dealers:
        if d.get("code") in remove_codes:
            continue

        # Giữ lại chỉ link SHOPEE và TIKTOK
        clean_links = {}
        for k, v in d.get("store_links", {}).items():
            k_upper = k.upper()
            if "SHOPEE" in k_upper or "TIKTOK" in k_upper:
                norm_k = "TIKTOK" if "TIKTOK" in k_upper else "SHOPEE"
                clean_links[norm_k] = v

        has_shopee = "SHOPEE" in clean_links
        has_tiktok = "TIKTOK" in clean_links

        if has_shopee and has_tiktok:
            platform_str = "Shopee, TikTok Shop"
        elif has_tiktok:
            platform_str = "TikTok Shop"
        else:
            platform_str = "Shopee"

        d["store_links"] = clean_links
        d["platform"] = platform_str
        keep_dealers.append(d)

    keep_ids = set(d["id"] for d in keep_dealers)

    # Lọc lại sản phẩm thuộc các đại lý được giữ
    keep_products = [p for p in products if p.get("dealer_id") in keep_ids]

    # Cập nhật lại products_count cho từng đại lý
    prod_count_by_dealer = {}
    for p in keep_products:
        did = p.get("dealer_id")
        prod_count_by_dealer[did] = prod_count_by_dealer.get(did, 0) + 1

    for d in keep_dealers:
        d["products_count"] = prod_count_by_dealer.get(d["id"], 0)

    store["dealers"] = keep_dealers
    store["products"] = keep_products

    # 1. Ghi ra giam_sat_gia_store.json
    with open(STORE_JSON, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    print(f"-> Ghi thành công giam_sat_gia_store.json: {len(keep_dealers)} đại lý Shopee & TikTok, {len(keep_products)} sản phẩm.")

    # 2. Ghi ra giam_sat_gia_store.js
    with open(STORE_JS, "w", encoding="utf-8") as f:
        f.write("window.INITIAL_KINGBLUE_DATA = ")
        json.dump(store, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("-> Ghi thành công giam_sat_gia_store.js")

if __name__ == "__main__":
    run()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module quét và đối soát giá Shopee tự động qua Apify Actor xtracto/shopee-scraper
Dành cho Hệ thống Giám sát Giá KingBlue
"""

import os
import json
import ssl
import re
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_FILE = os.path.join(BASE_DIR, "giam_sat_gia_store.json")

def get_apify_token():
    """Lấy Apify token từ biến môi trường hoặc tự động đọc từ cấu hình mcp_config.json"""
    token = os.environ.get("APIFY_TOKEN")
    if token:
        return token
    mcp_config_path = os.path.expanduser("~/.gemini/antigravity/mcp_config.json")
    if os.path.exists(mcp_config_path):
        try:
            with open(mcp_config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                server_url = data.get("mcpServers", {}).get("apify", {}).get("serverUrl", "")
                match = re.search(r'token=([^&]+)', server_url)
                if match:
                    return match.group(1)
                auth_header = data.get("mcpServers", {}).get("apify", {}).get("headers", {}).get("Authorization", "")
                if auth_header.startswith("Bearer "):
                    return auth_header.replace("Bearer ", "").strip()
        except Exception:
            pass
    return ""

def load_catalog_and_dealers():
    if os.path.exists(STORE_FILE):
        try:
            with open(STORE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("pdf_catalog", []), data.get("dealers", [])
        except Exception as e:
            print(f"[!] Lỗi đọc catalog: {e}")
    return [], []

def match_product_with_catalog(shopee_name, catalog):
    """Tìm sản phẩm niêm yết tương ứng trong catalog PDF của KingBlue bằng cách trích xuất mã model chuẩn"""
    if not catalog or not shopee_name:
        return None
    
    name_norm = re.sub(r'[\-_]', '', shopee_name.lower())
    codes = re.findall(r'[a-z]{1,4}[0-9]{1,4}[a-z0-9]*', name_norm)
    
    blacklist = {'king', 'blue', 'shopee', 'chinh', 'hang', 'thep', 'combo', 'may', 'chat', 'chatluong'}
    
    for code in codes:
        if len(code) >= 4 and code not in blacklist:
            for c in catalog:
                desc = c.get('item_desc', '')
                desc_norm = re.sub(r'[\-_]', '', desc.lower())
                if code in desc_norm:
                    return c
    return None

def scan_shopee_products(keyword="king blue", max_products=20):
    """
    Gọi Apify Actor xtracto/shopee-scraper để cào sản phẩm thực tế trên Shopee
    và đối soát trực tiếp với giá sàn TMĐT niêm yết của King Blue.
    Hỗ trợ cả tìm kiếm theo từ khóa và quét trực tiếp theo link gian hàng (Shop URL).
    """
    token = get_apify_token()
    if not token:
        return {
            "status": "error",
            "message": "Chưa cấu hình Apify Token. Vui lòng kiểm tra ~/.gemini/antigravity/mcp_config.json",
            "items": []
        }

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    url = f"https://api.apify.com/v2/acts/xtracto~shopee-scraper/run-sync-get-dataset-items?token={token}"
    
    # Kiểm tra xem keyword có phải là URL shop hay chứa tham số shop không
    payload = {"country": "vn"}
    raw_kw = (keyword or "").strip()
    
    if "700251789" in raw_kw or "shopdiennuoc.nhat" in raw_kw:
        payload["mode"] = "shop"
        payload["shop"] = "shopdiennuoc.nhat"
        payload["maxProducts"] = max_products
    elif "shopee.vn/shop/" in raw_kw or "/shop/" in raw_kw:
        shop_val = raw_kw.split("/shop/")[-1].split("?")[0].strip()
        payload["mode"] = "shop"
        payload["shop"] = shop_val
        payload["maxProducts"] = max_products
    elif "shopee.vn/" in raw_kw and "?" in raw_kw and "shop=" in raw_kw:
        # Link tìm kiếm trong shop: https://shopee.vn/search?keyword=...&shop=...
        m_shop = re.search(r'shop=([a-zA-Z0-9_\.\-]+)', raw_kw)
        shop_id = m_shop.group(1) if m_shop else ""
        if shop_id == "700251789":
            payload["mode"] = "shop"
            payload["shop"] = "shopdiennuoc.nhat"
        else:
            payload["mode"] = "shop"
            payload["shop"] = shop_id
        payload["maxProducts"] = max_products
    elif "shopee.vn/" in raw_kw:
        # Link gian hàng trực tiếp: https://shopee.vn/lequang_shop?...
        m_shop = re.search(r'shopee\.vn/([a-zA-Z0-9_\.\-]+)', raw_kw)
        shop_name = m_shop.group(1) if m_shop else ""
        if shop_name and shop_name not in ["search", "product", "cart", "user"]:
            payload["mode"] = "shop"
            payload["shop"] = shop_name
            payload["maxProducts"] = max_products
        else:
            payload["mode"] = "keyword"
            payload["keyword"] = raw_kw or "king blue"
            payload["maxProducts"] = max_products
    else:
        payload["mode"] = "keyword"
        payload["keyword"] = raw_kw or "king blue"
        payload["maxProducts"] = max_products
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    catalog, dealers = load_catalog_and_dealers()
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            raw_items = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"status": "error", "message": f"Lỗi gọi Apify: {str(e)}", "items": []}
        
    analyzed_items = []
    
    for it in raw_items:
        p_name = it.get("name", "")
        # Nếu quét shop thì chỉ giữ các sản phẩm KingBlue / Tolsen hoặc khớp
        if payload.get("mode") == "shop":
            name_low = p_name.lower()
            if not any(k in name_low for k in ["king", "blue", "kinblue", "kbl", "st8", "tolsen", "v65", "kbh", "khd"]):
                continue

        shopee_price = it.get("price") or 0
        shop_id = it.get("shop_id") or (700251789 if "shopdiennuoc.nhat" in str(payload.get("shop")) else None)
        
        matched_cat = match_product_with_catalog(p_name, catalog)
        
        gia_san_tmdt = matched_cat.get("gia_san_tmdt") if matched_cat else None
        gia_le = matched_cat.get("gia_le") if matched_cat else None
        gia_chuan = gia_san_tmdt or gia_le
        
        tinh_trang = "CHUA_DOI_CHIEU"
        chenh_lech_tien = 0
        phan_tram_lech = 0
        
        if gia_chuan and shopee_price > 0:
            diff = shopee_price - gia_chuan
            diff_pct = diff / gia_chuan
            chenh_lech_tien = round(diff, 0)
            phan_tram_lech = round(diff_pct, 4)
            
            if diff_pct < -0.02:
                tinh_trang = "PHA_GIA"
            elif diff_pct > 0.05:
                tinh_trang = "VUOT_GIA"
            else:
                tinh_trang = "TUAN_THU"
                
        # Nhận diện gian hàng đại lý nếu trùng shop_id hoặc tên
        matched_dealer = None
        shop_str = str(payload.get("shop") or shop_id)
        if str(shop_id) == "700251789" or "shopdiennuoc.nhat" in shop_str:
            matched_dealer = "Điện nước Nhật (Shop) HCM #700251789"
        elif str(shop_id) == "7239997" or "baohothinksafe" in shop_str:
            matched_dealer = "DL005 - ThinkSafe HCM (Shop baohothinksafe #7239997)"
        elif str(shop_id) == "388478963" or "nguyenhoangphu" in shop_str:
            matched_dealer = "DL002 - Nguyễn Hoàng Phú (Shop nguyenhoangphu68 #388478963)"
        elif "lequang" in shop_str or str(shop_id) == "lequang_shop":
            matched_dealer = "DL007 - CÔNG TY TNHH ĐHT VIỆT NAM - HCM (Shop lequang_shop #48503940317)"
        else:
            for d in dealers:
                d_links = str(d.get("store_links", {})) + str(d.get("raw_link", ""))
                if str(d.get("id")) == str(shop_id) or str(shop_id) in d_links or (d.get("name") and d.get("name").lower() in p_name.lower()):
                    matched_dealer = d.get("name")
                    break
                
        analyzed_items.append({
            "item_id": it.get("item_id"),
            "shop_id": shop_id,
            "dealer_name": matched_dealer or f"Gian hàng Shopee #{shop_id}",
            "product_name": p_name,
            "url": it.get("url"),
            "image_url": it.get("image_url"),
            "gia_ban_thuc_te": shopee_price,
            "original_shopee_price": it.get("original_price"),
            "rating": it.get("rating"),
            "matched_catalog": matched_cat.get("item_desc") if matched_cat else None,
            "gia_san_tmdt": gia_san_tmdt,
            "gia_le": gia_le,
            "tinh_trang": tinh_trang,
            "chenh_lech_tien": chenh_lech_tien,
            "phan_tram_lech": phan_tram_lech,
            "huong_xu_ly": "Lập biên bản vi phạm giá bán sàn TMĐT" if tinh_trang == "PHA_GIA" else None
        })
        
    return {
        "status": "success",
        "keyword": keyword,
        "total": len(analyzed_items),
        "pha_gia_count": len([x for x in analyzed_items if x["tinh_trang"] == "PHA_GIA"]),
        "tuan_thu_count": len([x for x in analyzed_items if x["tinh_trang"] == "TUAN_THU"]),
        "chua_doi_chieu_count": len([x for x in analyzed_items if x["tinh_trang"] == "CHUA_DOI_CHIEU"]),
        "items": analyzed_items
    }

if __name__ == "__main__":
    res = scan_shopee_products("king blue v65r", 3)
    print(json.dumps(res, ensure_ascii=False, indent=2))

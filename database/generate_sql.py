import csv
import re
import sqlite3
import os

# 1. Read sheet data
with open("sheet_data.csv", "r", encoding="utf-8") as f:
    rows = list(csv.reader(f))

# Header: STT, Tên khách hàng/NPP/Đại lý, tỉnh thành, Nhân viên phụ trách, Sàn TMĐT, Link gian hàng, Mã Sản phẩm..., Giá niêm yết..., Giá bán..., Chênh lệch (%), Tình trạng..., Ngày kiểm tra..., Bằng chứng..., Hướng xử lý...

customers_raw = []
for r in rows[2:7]:
    cid = int(r[0].strip())
    name = r[1].strip()
    province = r[2].strip()
    emp = r[3].strip()
    platform = r[4].strip()
    store_links = r[5].strip()
    products_text = r[6].strip()
    prods = [p.strip() for p in products_text.split("\n") if p.strip()]
    
    customers_raw.append({
        "id": cid,
        "name": name,
        "province": province,
        "employee": emp,
        "platform": platform,
        "store_links": store_links,
        "products": prods
    })

# 2. Extract unique entities
employees = sorted(list(set(c["employee"] for c in customers_raw)))
emp_map = {name: idx + 1 for idx, name in enumerate(employees)}

provinces = sorted(list(set(c["province"] for c in customers_raw)))
prov_map = {name: idx + 1 for idx, name in enumerate(provinces)}

platforms = ["Shopee", "TikTok Shop", "Lazada", "Website"]
plat_map = {p.lower(): idx + 1 for idx, p in enumerate(platforms)}

# Extract unique products
unique_products = sorted(list(set(p for c in customers_raw for p in c["products"])))
prod_map = {}

def extract_code(prod_name):
    # Regex to find product code usually uppercase with numbers like KB16VB2, CGS-2400, etc.
    tokens = prod_name.split()
    codes = []
    for t in reversed(tokens):
        cleaned = re.sub(r"[(),]", "", t)
        if re.search(r"[A-Z0-9]+-[A-Z0-9]+|\b[A-Z]{2,}\d+|\b[A-Z]\d+", cleaned):
            codes.append(cleaned)
    if codes:
        return codes[0]
    return None

for idx, p in enumerate(unique_products):
    code = extract_code(p)
    prod_map[p] = {
        "id": idx + 1,
        "name": p,
        "code": code if code else f"KB-{idx+1:04d}"
    }

print(f"Loaded: {len(employees)} employees, {len(provinces)} provinces, {len(customers_raw)} customers, {len(unique_products)} products.")

# 3. Create Schema SQL
schema_sql = """-- ====================================================================
-- HỆ THỐNG CƠ SỞ DỮ LIỆU QUẢN LÝ KHÁCH HÀNG & GIÁ BÁN SÀN TMĐT (KINGBLUE)
-- Chuẩn hóa từ Google Sheet:
-- https://docs.google.com/spreadsheets/d/1dN2SIReDdk3EruHTTYUbsAH9X4UgIXmV5uUrOidrlbY
-- Chuẩn thiết kế: 3NF (Third Normal Form) & BCNF
-- ====================================================================

-- 1. Bảng Tỉnh/Thành phố (Quản lý địa bàn hoạt động)
CREATE TABLE IF NOT EXISTS provinces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    province_code VARCHAR(20) UNIQUE NOT NULL,
    province_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) DEFAULT 'Miền Nam' -- Miền Bắc, Miền Trung, Miền Nam
);

-- 2. Bảng Nhân viên phụ trách (Sales / Account Manager / Marketing)
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_code VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    department VARCHAR(50) DEFAULT 'Kinh doanh',
    status VARCHAR(20) DEFAULT 'ACTIVE' -- ACTIVE, INACTIVE
);

-- 3. Bảng Sàn Thương Mại Điện Tử (Shopee, TikTok Shop, Lazada, Website, ...)
CREATE TABLE IF NOT EXISTS ecommerce_platforms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform_code VARCHAR(30) UNIQUE NOT NULL, -- SHOPEE, TIKTOK, LAZADA, WEBSITE, TIKI
    platform_name VARCHAR(100) NOT NULL,
    homepage_url VARCHAR(255),
    is_active BOOLEAN DEFAULT 1
);

-- 4. Bảng Khách hàng / Nhà phân phối (NPP) / Đại lý
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_code VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_type VARCHAR(50) DEFAULT 'Đại lý', -- NPP, Đại lý Cấp 1, Đại lý Cấp 2, Shop bán lẻ
    province_id INTEGER NOT NULL,
    assigned_employee_id INTEGER NOT NULL,
    phone VARCHAR(50),
    address TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (province_id) REFERENCES provinces(id),
    FOREIGN KEY (assigned_employee_id) REFERENCES employees(id)
);

-- 5. Bảng Gian hàng TMĐT của Khách hàng (1 Khách hàng có thể có nhiều gian hàng trên nhiều sàn)
CREATE TABLE IF NOT EXISTS customer_stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    platform_id INTEGER NOT NULL,
    store_name VARCHAR(255),
    store_url TEXT NOT NULL,
    store_identifier VARCHAR(100), -- username / shop_id trên sàn
    status VARCHAR(20) DEFAULT 'ACTIVE', -- ACTIVE, INACTIVE, SUSPENDED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (platform_id) REFERENCES ecommerce_platforms(id)
);

-- 6. Bảng Danh mục Sản phẩm KingBlue
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code VARCHAR(100) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100), -- Kìm, Mũi khoan, Cờ lê, Đèn led, Vít, v.v.
    listed_price DECIMAL(15, 2) DEFAULT 0.00, -- Giá niêm yết chính hãng KingBlue (VND)
    unit VARCHAR(30) DEFAULT 'Cái', -- Cái, Bộ, Hộp, Cây
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Bảng Sản phẩm Khách hàng đã nhập hàng (Từ đầu năm đến nay - Bảng quan hệ N-N)
CREATE TABLE IF NOT EXISTS customer_purchased_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    first_purchase_date DATE,
    last_purchase_date DATE,
    total_quantity_purchased INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE(customer_id, product_id)
);

-- 8. Bảng Lịch sử Kiểm tra & Giám sát Tuân thủ Giá bán trên Sàn (Price Audits)
CREATE TABLE IF NOT EXISTS price_audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_store_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    audited_by_employee_id INTEGER,
    audit_date DATE NOT NULL,
    
    -- Số liệu giá
    listed_price DECIMAL(15, 2) NOT NULL, -- Giá niêm yết KingBlue tại thời điểm kiểm tra
    selling_price DECIMAL(15, 2) NOT NULL, -- Giá bán thực tế trên gian hàng sàn TMĐT
    price_diff_percent DECIMAL(5, 2), -- Chênh lệch % = ((selling_price - listed_price) / listed_price) * 100
    
    -- Đánh giá tuân thủ
    compliance_status VARCHAR(50) NOT NULL, -- 'TUAN_THU' (Tuân thủ), 'PHA_GIA' (Bán phá giá), 'VUOT_GIA' (Bán cao hơn)
    
    -- Bằng chứng & Xử lý
    product_item_url TEXT, -- Link trực tiếp đến sản phẩm trên sàn
    evidence_url TEXT, -- Link ảnh chụp màn hình / video bằng chứng
    action_notes TEXT, -- Hướng xử lý: Nhắc nhở, Cắt chiết khấu, Dừng cấp hàng...
    status VARCHAR(30) DEFAULT 'PENDING', -- PENDING (Chờ xử lý), RESOLVED (Đã xử lý), CLOSED (Đóng)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_store_id) REFERENCES customer_stores(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (audited_by_employee_id) REFERENCES employees(id)
);

-- ====================================================================
-- CHỈ MỤC (INDEXES) TỐI ƯU HIỆU NĂNG TRUY VẤN
-- ====================================================================
CREATE INDEX IF NOT EXISTS idx_customers_assigned_employee ON customers(assigned_employee_id);
CREATE INDEX IF NOT EXISTS idx_customer_stores_customer ON customer_stores(customer_id);
CREATE INDEX IF NOT EXISTS idx_customer_stores_platform ON customer_stores(platform_id);
CREATE INDEX IF NOT EXISTS idx_purchased_products_cust ON customer_purchased_products(customer_id);
CREATE INDEX IF NOT EXISTS idx_purchased_products_prod ON customer_purchased_products(product_id);
CREATE INDEX IF NOT EXISTS idx_price_audits_store ON price_audits(customer_store_id);
CREATE INDEX IF NOT EXISTS idx_price_audits_prod ON price_audits(product_id);
CREATE INDEX IF NOT EXISTS idx_price_audits_date ON price_audits(audit_date);
CREATE INDEX IF NOT EXISTS idx_price_audits_compliance ON price_audits(compliance_status);

-- ====================================================================
-- VIEWS BÁO CÁO NGHIỆP VỤ (BUSINESS VIEWS)
-- ====================================================================

-- View 1: Danh sách tổng hợp khách hàng, gian hàng và số mã hàng đã nhập
CREATE VIEW IF NOT EXISTS v_customer_overview AS
SELECT 
    c.id AS customer_id,
    c.customer_code,
    c.customer_name,
    p.province_name,
    e.full_name AS sales_representative,
    COUNT(DISTINCT cs.id) AS total_stores,
    COUNT(DISTINCT cpp.product_id) AS total_products_imported
FROM customers c
LEFT JOIN provinces p ON c.province_id = p.id
LEFT JOIN employees e ON c.assigned_employee_id = e.id
LEFT JOIN customer_stores cs ON c.id = cs.customer_id
LEFT JOIN customer_purchased_products cpp ON c.id = cpp.customer_id
GROUP BY c.id;

-- View 2: Cảnh báo vi phạm giá bán trên các sàn TMĐT
CREATE VIEW IF NOT EXISTS v_price_compliance_alerts AS
SELECT 
    pa.id AS audit_id,
    pa.audit_date,
    c.customer_name,
    ep.platform_name,
    cs.store_name,
    cs.store_url,
    prd.product_code,
    prd.product_name,
    pa.listed_price,
    pa.selling_price,
    pa.price_diff_percent,
    pa.compliance_status,
    pa.evidence_url,
    pa.action_notes,
    e.full_name AS auditor_name
FROM price_audits pa
JOIN customer_stores cs ON pa.customer_store_id = cs.id
JOIN customers c ON cs.customer_id = c.id
JOIN ecommerce_platforms ep ON cs.platform_id = ep.id
JOIN products prd ON pa.product_id = prd.id
LEFT JOIN employees e ON pa.audited_by_employee_id = e.id
WHERE pa.compliance_status = 'PHA_GIA';
"""

with open("database/schema.sql", "w", encoding="utf-8") as f:
    f.write(schema_sql)

# 4. Generate Seed Data SQL
seed_sql = []
seed_sql.append("-- ====================================================================")
seed_sql.append("-- DỮ LIỆU KHỞI TẠO (SEED DATA) CHUYỂN ĐỔI TỪ GOOGLE SHEET THỰC TẾ")
seed_sql.append("-- ====================================================================\n")

# Provinces
seed_sql.append("-- 1. Dữ liệu Tỉnh/Thành")
for name, pid in prov_map.items():
    seed_sql.append(f"INSERT OR IGNORE INTO provinces (id, province_code, province_name, region) VALUES ({pid}, '{name.upper()}', '{name}', 'Miền Nam');")

# Employees
seed_sql.append("\n-- 2. Dữ liệu Nhân viên phụ trách")
for name, eid in emp_map.items():
    code = f"NV{eid:03d}"
    seed_sql.append(f"INSERT OR IGNORE INTO employees (id, employee_code, full_name, department) VALUES ({eid}, '{code}', '{name}', 'Kinh doanh');")

# Platforms
seed_sql.append("\n-- 3. Dữ liệu Sàn Thương Mại Điện Tử")
platforms_data = [
    (1, "SHOPEE", "Shopee", "https://shopee.vn"),
    (2, "TIKTOK", "TikTok Shop", "https://shop.tiktok.com"),
    (3, "LAZADA", "Lazada", "https://lazada.vn"),
    (4, "WEBSITE", "Website bán hàng", "")
]
for pid, code, name, url in platforms_data:
    seed_sql.append(f"INSERT OR IGNORE INTO ecommerce_platforms (id, platform_code, platform_name, homepage_url) VALUES ({pid}, '{code}', '{name}', '{url}');")

# Customers
seed_sql.append("\n-- 4. Dữ liệu Khách hàng / Đại lý")
for c in customers_raw:
    cid = c["id"]
    code = f"DL{cid:04d}"
    name_escaped = c["name"].replace("'", "''")
    prov_id = prov_map[c["province"]]
    emp_id = emp_map[c["employee"]]
    seed_sql.append(f"INSERT OR IGNORE INTO customers (id, customer_code, customer_name, customer_type, province_id, assigned_employee_id) VALUES ({cid}, '{code}', '{name_escaped}', 'Đại lý', {prov_id}, {emp_id});")

# Customer Stores
seed_sql.append("\n-- 5. Dữ liệu Gian hàng TMĐT của Khách hàng")
for c in customers_raw:
    cid = c["id"]
    # Determine platform
    p_name = c["platform"].strip()
    plat_id = 1 # default Shopee
    if "website" in p_name.lower():
        plat_id = 4
    elif "tiktok" in p_name.lower():
        plat_id = 2
    elif "lazada" in p_name.lower():
        plat_id = 3
    store_name_escaped = f"Gian hàng {c['name']}".replace("'", "''")
    seed_sql.append(f"INSERT OR IGNORE INTO customer_stores (id, customer_id, platform_id, store_name, store_url) VALUES ({cid}, {cid}, {plat_id}, '{store_name_escaped}', 'https://shopee.vn/shop_demo_{cid}');")

# Products
seed_sql.append("\n-- 6. Dữ liệu Danh mục Sản phẩm KingBlue (580 mã)")
for p_name, info in prod_map.items():
    pid = info["id"]
    code = info["code"]
    p_escaped = p_name.replace("'", "''")
    seed_sql.append(f"INSERT OR IGNORE INTO products (id, product_code, product_name, category, listed_price) VALUES ({pid}, '{code}', '{p_escaped}', 'Thiết bị & Dụng cụ KingBlue', 0.00);")

# Customer Purchased Products
seed_sql.append("\n-- 7. Dữ liệu Sản phẩm Đại lý đã nhập hàng từ đầu năm (1055 liên kết)")
c_prod_id = 1
for c in customers_raw:
    cid = c["id"]
    for p_name in c["products"]:
        pid = prod_map[p_name]["id"]
        seed_sql.append(f"INSERT OR IGNORE INTO customer_purchased_products (id, customer_id, product_id, status) VALUES ({c_prod_id}, {cid}, {pid}, 'ACTIVE');")
        c_prod_id += 1

# Demo Price Audit row to illustrate price monitoring
seed_sql.append("\n-- 8. Dữ liệu Mẫu Báo cáo Kiểm tra Giá (Price Audit Example)")
seed_sql.append("""INSERT OR IGNORE INTO price_audits (
    id, customer_store_id, product_id, audited_by_employee_id, audit_date, 
    listed_price, selling_price, price_diff_percent, compliance_status, 
    product_item_url, evidence_url, action_notes, status
) VALUES (
    1, 1, 1, 1, '2026-10-14',
    1250000.00, 1100000.00, -12.00, 'PHA_GIA',
    'https://shopee.vn/product/123/456', 'https://storage.kingblue.vn/evidence/audit_1.jpg',
    'Phát hiện bán thấp hơn giá niêm yết 12%. Đã gửi văn bản nhắc nhở yêu cầu điều chỉnh giá trong 24h.', 'PENDING'
);""")

with open("database/seed_data.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(seed_sql))

# 5. Generate Queries SQL
queries_sql = """-- ====================================================================
-- CÁC TRUY VẤN MẪU HỮU ÍCH CHO HỆ THỐNG GIÁM SÁT GIÁ TMĐT KINGBLUE
-- ====================================================================

-- 1. Báo cáo tổng quan số lượng sản phẩm nhập theo từng đại lý
SELECT 
    c.id AS customer_id,
    c.customer_name,
    p.province_name,
    e.full_name AS nhan_vien_phu_trach,
    COUNT(cpp.product_id) AS tong_san_pham_da_nhap
FROM customers c
JOIN provinces p ON c.province_id = p.id
JOIN employees e ON c.assigned_employee_id = e.id
LEFT JOIN customer_purchased_products cpp ON c.id = cpp.customer_id
GROUP BY c.id
ORDER BY tong_san_pham_da_nhap DESC;

-- 2. Top 15 sản phẩm được nhiều đại lý nhập bán nhất
SELECT 
    prd.product_code,
    prd.product_name,
    COUNT(cpp.customer_id) AS so_dai_ly_nhap_hang
FROM products prd
JOIN customer_purchased_products cpp ON prd.id = cpp.product_id
GROUP BY prd.id
ORDER BY so_dai_ly_nhap_hang DESC, prd.product_name ASC
LIMIT 15;

-- 3. Danh sách các gian hàng cần kiểm tra giá và tình trạng kiểm tra
SELECT 
    c.customer_name,
    ep.platform_name,
    cs.store_name,
    cs.store_url,
    MAX(pa.audit_date) AS ngay_kiem_tra_gan_nhat,
    COUNT(pa.id) AS so_lan_kiem_tra,
    SUM(CASE WHEN pa.compliance_status = 'PHA_GIA' THEN 1 ELSE 0 END) AS so_lan_vi_pham
FROM customers c
JOIN customer_stores cs ON c.id = cs.customer_id
JOIN ecommerce_platforms ep ON cs.platform_id = ep.id
LEFT JOIN price_audits pa ON cs.id = pa.customer_store_id
GROUP BY cs.id;

-- 4. Tìm kiếm các sản phẩm cụ thể mà đại lý 'Điện nước Nhật (Shop) HCM' đã nhập
SELECT 
    prd.product_code,
    prd.product_name,
    prd.listed_price
FROM customer_purchased_products cpp
JOIN customers c ON cpp.customer_id = c.id
JOIN products prd ON cpp.product_id = prd.id
WHERE c.customer_name LIKE '%Điện nước Nhật%'
ORDER BY prd.product_name;

-- 5. Báo cáo chi tiết các trường hợp bán phá giá cần xử lý
SELECT 
    pa.audit_date AS ngay_kiem_tra,
    c.customer_name,
    ep.platform_name AS san,
    prd.product_name,
    pa.listed_price AS gia_niem_yet,
    pa.selling_price AS gia_ban_san,
    pa.price_diff_percent AS phan_tram_lech,
    pa.action_notes AS huong_xu_ly,
    e.full_name AS nhan_vien_phu_trach
FROM price_audits pa
JOIN customer_stores cs ON pa.customer_store_id = cs.id
JOIN customers c ON cs.customer_id = c.id
JOIN ecommerce_platforms ep ON cs.platform_id = ep.id
JOIN products prd ON pa.product_id = prd.id
JOIN employees e ON c.assigned_employee_id = e.id
WHERE pa.compliance_status = 'PHA_GIA'
ORDER BY pa.audit_date DESC;
"""

with open("database/queries.sql", "w", encoding="utf-8") as f:
    f.write(queries_sql)

# 6. Execute in SQLite database to verify 100% correctness
db_path = "database/kingblue_ecommerce.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Run schema
with open("database/schema.sql", "r", encoding="utf-8") as f:
    cursor.executescript(f.read())

# Run seed data
with open("database/seed_data.sql", "r", encoding="utf-8") as f:
    cursor.executescript(f.read())

conn.commit()

# Test queries
print("\n--- TEST VIEW v_customer_overview ---")
cursor.execute("SELECT * FROM v_customer_overview")
for row in cursor.fetchall():
    print(row)

print("\n--- TEST QUERY: Top 5 most imported products ---")
cursor.execute("""
SELECT prd.product_name, COUNT(cpp.customer_id) as cnt
FROM products prd
JOIN customer_purchased_products cpp ON prd.id = cpp.product_id
GROUP BY prd.id
ORDER BY cnt DESC
LIMIT 5
""")
for row in cursor.fetchall():
    print(row)

conn.close()
print("\nDatabase SQLite created and verified successfully at database/kingblue_ecommerce.db!")

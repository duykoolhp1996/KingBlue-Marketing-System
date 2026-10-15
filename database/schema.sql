-- ====================================================================
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

-- ====================================================================
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

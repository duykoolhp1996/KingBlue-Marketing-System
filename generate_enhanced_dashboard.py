import json
import os

with open('/Users/Admin/Documents/KIng BLue/Report/customer_analytics_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>King Blue - Customer & Product Intelligence Dashboard 2026</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#eff6ff',
              100: '#dbeafe',
              500: '#3b82f6',
              600: '#2563eb',
              700: '#1d4ed8',
              800: '#1e40af',
              900: '#1e3a8a',
              navy: '#1A365D',
              dark: '#0f172a'
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    .custom-scrollbar::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    .custom-scrollbar::-webkit-scrollbar-track {{ background: #f1f5f9; }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 4px; }}
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {{ background: #94a3b8; }}
    .tab-btn.active {{
      background-color: #1A365D;
      color: #ffffff;
      border-color: #1A365D;
      box-shadow: 0 4px 12px rgba(26, 54, 93, 0.25);
    }}
    .badge-a {{ background-color: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }}
    .badge-b {{ background-color: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }}
    .badge-c {{ background-color: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }}
  </style>
</head>
<body class="bg-slate-100 text-slate-800 antialiased min-h-screen flex flex-col">

  <!-- ================= TOP APP HEADER ================= -->
  <header class="bg-[#1A365D] text-white border-b-4 border-amber-400 sticky top-0 z-40 shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-4">
      
      <!-- Brand & Title -->
      <div class="flex items-center gap-3.5">
        <div class="w-11 h-11 rounded-xl bg-amber-400 text-slate-950 flex items-center justify-center font-black text-xl shadow-inner shrink-0 tracking-wider">
          KB
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-lg sm:text-xl font-black tracking-tight">KING BLUE INTELLIGENCE DASHBOARD</h1>
            <span class="text-[10px] bg-amber-400 text-slate-950 font-black px-2 py-0.5 rounded-full uppercase tracking-wider">Khách Hàng & Sản Phẩm</span>
          </div>
          <p class="text-blue-200 text-xs font-medium">Hệ Thống Phân Tích Khách Hàng (RFM) & Quản Trị Danh Mục 1,226 SKU Sản Phẩm KingBlue 2026</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="flex items-center gap-2">
        <a href="index.html" class="bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold text-xs px-3 py-2 rounded-xl flex items-center gap-1.5 transition">
          <span>🏠</span> <span>Cổng Marketing</span>
        </a>
        <button onclick="exportCustomersCSV()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs px-3 py-2 rounded-xl flex items-center gap-1.5 transition shadow">
          <span>📥</span> <span>Xuất Excel KH</span>
        </button>
        <button onclick="exportProductsCSV()" class="bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs px-3 py-2 rounded-xl flex items-center gap-1.5 transition shadow">
          <span>📦</span> <span>Xuất Excel SP</span>
        </button>
        <button onclick="window.print()" class="bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs px-3 py-2 rounded-xl flex items-center gap-1.5 transition shadow">
          <span>🖨️</span> <span>In / PDF</span>
        </button>
      </div>

    </div>
  </header>

  <!-- ================= SUB HEADER BANNER ================= -->
  <div class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white py-3 border-b border-blue-950/40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-wrap items-center justify-between gap-3 text-xs">
      <div class="flex items-center gap-4 flex-wrap">
        <span class="inline-flex items-center gap-1.5 bg-blue-800/60 px-2.5 py-1 rounded-lg border border-blue-700/50">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Dữ liệu: <strong>70,855</strong> dòng chứng từ</span>
        </span>
        <span class="inline-flex items-center gap-1.5 bg-blue-800/60 px-2.5 py-1 rounded-lg border border-blue-700/50">
          <span>👥 Khách hàng: <strong>393 Đại lý</strong></span>
        </span>
        <span class="inline-flex items-center gap-1.5 bg-blue-800/60 px-2.5 py-1 rounded-lg border border-blue-700/50">
          <span>📦 Sản phẩm: <strong>1,226 SKU</strong></span>
        </span>
        <span class="inline-flex items-center gap-1.5 bg-blue-800/60 px-2.5 py-1 rounded-lg border border-blue-700/50">
          <span>📅 <strong>01/01/2026 - 29/09/2026 (9 Tháng)</strong></span>
        </span>
      </div>
      <div class="text-blue-300 font-medium">
        Tự động phân loại Pareto 80/20 kép: Khách Hàng (RFM) & Danh Mục Sản Phẩm (SKU ABC)
      </div>
    </div>
  </div>

  <!-- ================= MAIN CONTAINER ================= -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

    <!-- KPI SUMMARY CARDS -->
    <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3 sm:gap-4">
      
      <!-- Doanh thu thuần -->
      <div class="col-span-2 bg-white rounded-2xl p-4 border border-slate-200/80 shadow-sm relative overflow-hidden group hover:shadow-md transition">
        <div class="absolute -right-3 -top-3 w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center text-blue-200 text-2xl font-black pointer-events-none group-hover:scale-110 transition">₫</div>
        <div class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Doanh Thu Thuần</div>
        <div class="text-2xl sm:text-3xl font-black text-blue-900 font-mono tracking-tight" id="kpi-net">83.76 Tỷ</div>
        <div class="mt-2 text-xs text-slate-500 flex items-center gap-1.5">
          <span class="font-bold text-slate-700">Gross: 98.71 Tỷ</span>
          <span class="text-slate-300">|</span>
          <span class="text-emerald-600 font-semibold">Thuần: 84.8%</span>
        </div>
      </div>

      <!-- Chiết khấu -->
      <div class="col-span-2 bg-white rounded-2xl p-4 border border-slate-200/80 shadow-sm relative overflow-hidden group hover:shadow-md transition">
        <div class="absolute -right-3 -top-3 w-16 h-16 bg-amber-50 rounded-full flex items-center justify-center text-amber-200 text-2xl font-black pointer-events-none group-hover:scale-110 transition">%</div>
        <div class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Tổng Chiết Khấu</div>
        <div class="text-2xl sm:text-3xl font-black text-amber-600 font-mono tracking-tight" id="kpi-discount">13.97 Tỷ</div>
        <div class="mt-2 text-xs text-slate-500 flex items-center gap-1.5">
          <span class="bg-amber-100 text-amber-800 font-bold px-1.5 py-0.5 rounded text-[11px]">14.15% DT Gộp</span>
          <span class="text-slate-400">Ưu đãi thương mại</span>
        </div>
      </div>

      <!-- Khách hàng -->
      <div class="col-span-2 bg-white rounded-2xl p-4 border border-slate-200/80 shadow-sm relative overflow-hidden group hover:shadow-md transition">
        <div class="absolute -right-3 -top-3 w-16 h-16 bg-indigo-50 rounded-full flex items-center justify-center text-indigo-200 text-2xl font-black pointer-events-none group-hover:scale-110 transition">👥</div>
        <div class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Tổng Số Khách Hàng</div>
        <div class="text-2xl sm:text-3xl font-black text-indigo-900 font-mono tracking-tight" id="kpi-customers">393 KH</div>
        <div class="mt-2 text-xs text-slate-500 flex items-center gap-1.5">
          <span class="font-bold text-slate-700">10,992 Đơn hàng</span>
          <span class="text-slate-300">|</span>
          <span class="text-indigo-600 font-semibold">28 đơn/KH</span>
        </div>
      </div>

      <!-- Sản phẩm & Sản lượng -->
      <div class="col-span-2 bg-white rounded-2xl p-4 border border-slate-200/80 shadow-sm relative overflow-hidden group hover:shadow-md transition">
        <div class="absolute -right-3 -top-3 w-16 h-16 bg-teal-50 rounded-full flex items-center justify-center text-teal-200 text-2xl font-black pointer-events-none group-hover:scale-110 transition">📦</div>
        <div class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Quy Mô Sản Phẩm (SKU)</div>
        <div class="text-2xl sm:text-3xl font-black text-teal-800 font-mono tracking-tight" id="kpi-products">1,226 SKU</div>
        <div class="mt-2 text-xs text-slate-500 flex items-center gap-1.5">
          <span class="font-bold text-slate-700">3.39 Triệu sp</span>
          <span class="text-slate-300">|</span>
          <span class="text-rose-600 font-bold">Trả lại: 1.00%</span>
        </div>
      </div>

    </div>

    <!-- ================= TAB NAVIGATION ================= -->
    <div class="flex items-center gap-2 border-b border-slate-200 pb-2 overflow-x-auto custom-scrollbar">
      <button onclick="switchTab('overview')" id="tab-overview" class="tab-btn active px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-transparent transition">
        <span>📈</span> <span>Tổng Quan & Phân Khúc KH</span>
      </button>
      <button onclick="switchTab('territory')" id="tab-territory" class="tab-btn bg-white hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-slate-200 transition">
        <span>🗺️</span> <span>Địa Lý & Đội Ngũ Sales</span>
      </button>
      <button onclick="switchTab('products')" id="tab-products" class="tab-btn bg-white hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-slate-200 transition">
        <span>📦</span> <span>Phân Tích Sản Phẩm Chuyên Sâu</span>
        <span class="bg-teal-100 text-teal-800 text-[10px] font-black px-1.5 py-0.5 rounded-full">1,226 SKU</span>
      </button>
      <button onclick="switchTab('customers')" id="tab-customers" class="tab-btn bg-white hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-slate-200 transition">
        <span>📋</span> <span>Danh Bạ Khách Hàng 360°</span>
        <span class="bg-blue-100 text-blue-800 text-[10px] font-black px-1.5 py-0.5 rounded-full" id="tab-cust-count">393</span>
      </button>
      <button onclick="switchTab('strategy')" id="tab-strategy" class="tab-btn bg-white hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-slate-200 transition">
        <span>💡</span> <span>Chiến Lược & Cảnh Báo Hành Động</span>
        <span class="bg-rose-100 text-rose-700 text-[10px] font-black px-1.5 py-0.5 rounded-full">Cảnh báo</span>
      </button>
    </div>

    <!-- ================= TAB 1: OVERVIEW & SEGMENTATION ================= -->
    <div id="section-overview" class="tab-section space-y-6">
      
      <!-- Charts Row 1: Monthly Trend & ABC Pareto -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Monthly Trend (2 Cols) -->
        <div class="lg:col-span-2 bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
                <span>📊</span> Diễn Biến Doanh Thu Thuần & Chiết Khấu Theo Tháng
              </h3>
              <p class="text-xs text-slate-500">Tăng trưởng đột biến vào Tháng 3 (16.4 Tỷ) và duy trì ổn định ở mức 7.5 - 10.6 Tỷ/tháng</p>
            </div>
            <div class="text-right">
              <span class="text-xs font-mono font-bold text-blue-700 bg-blue-50 px-2 py-1 rounded-lg">Đỉnh T3: 16.4 Tỷ</span>
            </div>
          </div>
          <div class="relative h-72 w-full">
            <canvas id="monthlyChart"></canvas>
          </div>
        </div>

        <!-- ABC Pareto Chart (1 Col) -->
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>🎯</span> Cơ Cấu Khách Hàng ABC (Pareto 80/20)
            </h3>
            <p class="text-xs text-slate-500">42 khách hàng trụ cột quyết định 80% doanh thu toàn hệ thống</p>
          </div>
          <div class="relative h-56 w-full flex items-center justify-center">
            <canvas id="abcChart"></canvas>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-100 grid grid-cols-3 text-center text-xs">
            <div>
              <span class="font-black text-blue-700">Hạng A</span>
              <div class="font-bold text-slate-800">42 KH (11%)</div>
              <div class="text-[11px] text-slate-500 font-mono">66.9 Tỷ (80%)</div>
            </div>
            <div>
              <span class="font-black text-sky-600">Hạng B</span>
              <div class="font-bold text-slate-800">80 KH (20%)</div>
              <div class="text-[11px] text-slate-500 font-mono">12.6 Tỷ (15%)</div>
            </div>
            <div>
              <span class="font-black text-slate-500">Hạng C</span>
              <div class="font-bold text-slate-800">271 KH (69%)</div>
              <div class="text-[11px] text-slate-500 font-mono">4.2 Tỷ (5%)</div>
            </div>
          </div>
        </div>

      </div>

      <!-- Charts Row 2: RFM Matrix & Top Categories -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- RFM Segmentation Breakdown -->
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
                <span>👥</span> Phân Bổ Phân Khúc RFM (Doanh Thu & Số Khách)
              </h3>
              <p class="text-xs text-slate-500">Đánh giá theo Tần suất mua, Khoảng cách lần mua cuối và Giá trị tiền mặt</p>
            </div>
          </div>
          <div class="relative h-72 w-full">
            <canvas id="rfmChart"></canvas>
          </div>
        </div>

        <!-- Top Categories Breakdown -->
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
                <span>📦</span> Top 8 Ngành Hàng Đóng Góp Doanh Số Cao Nhất
              </h3>
              <p class="text-xs text-slate-500">Chén mài, Lưỡi cắt, Mũi khoan Inox và Đồ nghề chiếm hơn 65% tỷ trọng</p>
            </div>
          </div>
          <div class="relative h-72 w-full">
            <canvas id="categoryChart"></canvas>
          </div>
        </div>

      </div>

      <!-- Top 10 Customers Leaderboard Preview -->
      <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>🏆</span> Top 10 Khách Hàng / Đại Lý Lớn Nhất Toàn Quốc (KingBlue Champions)
            </h3>
            <p class="text-xs text-slate-500">10 đối tác chiến lược mang lại gần 40 tỷ doanh thu thuần trong 9 tháng</p>
          </div>
          <button onclick="switchTab('customers')" class="text-xs font-bold text-blue-600 hover:text-blue-800 transition">
            Xem tất cả 393 khách →
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-50 text-slate-600 font-bold border-y border-slate-200">
              <tr>
                <th class="py-2.5 px-3">Hạng</th>
                <th class="py-2.5 px-3">Mã KH</th>
                <th class="py-2.5 px-3">Tên Đại Lý / Khách Hàng</th>
                <th class="py-2.5 px-3">Tỉnh / Thành</th>
                <th class="py-2.5 px-3 text-right">Số Đơn</th>
                <th class="py-2.5 px-3 text-right">Doanh Thu Thuần</th>
                <th class="py-2.5 px-3 text-right">Tỷ Lệ CK</th>
                <th class="py-2.5 px-3 text-center">Lần Mua Cuối</th>
                <th class="py-2.5 px-3">Phân Khúc RFM</th>
                <th class="py-2.5 px-3 text-center">Thao Tác</th>
              </tr>
            </thead>
            <tbody id="top-customers-tbody" class="divide-y divide-slate-100">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ================= TAB 2: TERRITORY & SALES ================= -->
    <div id="section-territory" class="tab-section hidden space-y-6">
      
      <!-- Territory Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Top Provinces Chart -->
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>📍</span> Top 10 Tỉnh / Thành Phố Doanh Thu Cao Nhất
            </h3>
            <p class="text-xs text-slate-500">TP.HCM dẫn đầu áp đảo (30 Tỷ - 36%), tiếp theo là Đồng Nai (8.7 Tỷ) & Đắk Lắk (8.6 Tỷ)</p>
          </div>
          <div class="relative h-80 w-full">
            <canvas id="provinceChart"></canvas>
          </div>
        </div>

        <!-- Sales Leaderboard Chart -->
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>💼</span> Doanh Thu Thuần Theo Nhân Viên Kinh Doanh
            </h3>
            <p class="text-xs text-slate-500">Lê Thị Thuỳ Trang đạt 25.55 Tỷ, Nguyễn Đoàn Xuân Trang đạt 16.46 Tỷ</p>
          </div>
          <div class="relative h-80 w-full">
            <canvas id="salesChart"></canvas>
          </div>
        </div>

      </div>

      <!-- Sales Performance Detail Table -->
      <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <div class="mb-4">
          <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
            <span>🎖️</span> Bảng Xếp Hạng Chi Tiết Đội Ngũ Kinh Doanh
          </h3>
          <p class="text-xs text-slate-500">Đánh giá doanh số thuần, số lượng khách hàng phụ trách, số đơn hàng và ARPU trung bình/khách</p>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-50 text-slate-600 font-bold border-y border-slate-200">
              <tr>
                <th class="py-2.5 px-3">Xếp Hạng</th>
                <th class="py-2.5 px-3">Nhân Viên Bán Hàng</th>
                <th class="py-2.5 px-3 text-right">Doanh Thu Thuần</th>
                <th class="py-2.5 px-3 text-right">Doanh Số Gộp</th>
                <th class="py-2.5 px-3 text-right">Chiết Khấu Đã Cấp</th>
                <th class="py-2.5 px-3 text-right">Số KH Quản Lý</th>
                <th class="py-2.5 px-3 text-right">Tổng Số Đơn</th>
                <th class="py-2.5 px-3 text-right">ARPU (DT TB/KH)</th>
                <th class="py-2.5 px-3 text-right">Tỷ Trọng (%)</th>
              </tr>
            </thead>
            <tbody id="sales-detail-tbody" class="divide-y divide-slate-100">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- Province Distribution Table -->
      <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <div class="mb-4">
          <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
            <span>🗺️</span> Phân Bổ Thị Trường Theo 39 Tỉnh / Thành Phố
          </h3>
          <p class="text-xs text-slate-500">Chi tiết doanh thu thuần, số lượng đại lý và số đơn hàng theo từng địa phương</p>
        </div>
        <div class="overflow-x-auto max-h-96 custom-scrollbar">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-50 text-slate-600 font-bold border-y border-slate-200 sticky top-0">
              <tr>
                <th class="py-2 px-3">Tỉnh / Thành Phố</th>
                <th class="py-2 px-3 text-right">Doanh Thu Thuần</th>
                <th class="py-2 px-3 text-right">Doanh Số Gộp</th>
                <th class="py-2 px-3 text-right">Số Đại Lý</th>
                <th class="py-2 px-3 text-right">Số Đơn Hàng</th>
                <th class="py-2 px-3 text-right">Tỷ Trọng Thị Phần</th>
              </tr>
            </thead>
            <tbody id="province-detail-tbody" class="divide-y divide-slate-100">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ================= TAB 3: PRODUCT INTELLIGENCE (NEW!) ================= -->
    <div id="section-products" class="tab-section hidden space-y-6">
      
      <!-- Product KPIs Ribbon -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        <div class="bg-gradient-to-br from-blue-50 to-indigo-50/70 rounded-xl p-4 border border-blue-200 flex items-center justify-between">
          <div>
            <div class="text-[11px] font-bold text-blue-800 uppercase">Sản Phẩm Hạng A (Top 80%)</div>
            <div class="text-2xl font-black text-blue-900 font-mono mt-0.5">194 SKU (15.8%)</div>
            <div class="text-xs text-blue-700 font-medium">Doanh số: <strong>78.89 Tỷ (79.9%)</strong></div>
          </div>
          <div class="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center font-black text-lg shadow">
            ⭐
          </div>
        </div>

        <div class="bg-gradient-to-br from-sky-50 to-cyan-50/70 rounded-xl p-4 border border-sky-200 flex items-center justify-between">
          <div>
            <div class="text-[11px] font-bold text-sky-800 uppercase">Sản Phẩm Hạng B (15%)</div>
            <div class="text-2xl font-black text-sky-900 font-mono mt-0.5">319 SKU (26.0%)</div>
            <div class="text-xs text-sky-700 font-medium">Doanh số: <strong>14.86 Tỷ (15.1%)</strong></div>
          </div>
          <div class="w-10 h-10 rounded-xl bg-sky-500 text-white flex items-center justify-center font-black text-lg shadow">
            📈
          </div>
        </div>

        <div class="bg-gradient-to-br from-slate-50 to-gray-100 rounded-xl p-4 border border-slate-300 flex items-center justify-between">
          <div>
            <div class="text-[11px] font-bold text-slate-700 uppercase">Sản Phẩm Hạng C (5%)</div>
            <div class="text-2xl font-black text-slate-800 font-mono mt-0.5">713 SKU (58.2%)</div>
            <div class="text-xs text-slate-500 font-medium">Chậm luân chuyển: <strong>4.96 Tỷ (5.0%)</strong></div>
          </div>
          <div class="w-10 h-10 rounded-xl bg-slate-600 text-white flex items-center justify-center font-black text-lg shadow">
            ⏳
          </div>
        </div>

        <div class="bg-gradient-to-br from-teal-50 to-emerald-50/70 rounded-xl p-4 border border-teal-200 flex items-center justify-between">
          <div>
            <div class="text-[11px] font-bold text-teal-800 uppercase">Tổng Sản Lượng Tiêu Thụ</div>
            <div class="text-2xl font-black text-teal-900 font-mono mt-0.5">3.39 Triệu SP</div>
            <div class="text-xs text-teal-700 font-medium">Đơn giá TB: <strong>29,128 ₫ / sp</strong></div>
          </div>
          <div class="w-10 h-10 rounded-xl bg-teal-600 text-white flex items-center justify-center font-black text-lg shadow">
            📦
          </div>
        </div>
      </div>

      <!-- Product Charts Row 1: Top Revenue vs Top Volume -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Top 10 by Revenue -->
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>🏆</span> Top 10 Sản Phẩm Doanh Thu Cao Nhất KingBlue
            </h3>
            <p class="text-xs text-slate-500">Mũi khoan tường KBLJ 3.14 Tỷ, Đá cắt D1 hộp sắt 2.79 Tỷ, Thùng đồ nghề 2.54 Tỷ...</p>
          </div>
          <div class="relative h-80 w-full">
            <canvas id="prodTopRevChart"></canvas>
          </div>
        </div>

        <!-- Top 10 by Quantity -->
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>🚀</span> Top 10 Sản Phẩm Tiêu Thụ Số Lượng (Volume) Lớn Nhất
            </h3>
            <p class="text-xs text-slate-500">Đá cắt sắt D1 hộp sắt dẫn đầu với 781,801 cái, D3 hộp sắt đạt 398,900 cái</p>
          </div>
          <div class="relative h-80 w-full">
            <canvas id="prodTopQtyChart"></canvas>
          </div>
        </div>

      </div>

      <!-- Product Charts Row 2: Category Breakdown & ABC Donut -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Product ABC Pareto Donut -->
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>🎯</span> Phân Hạng ABC Sản Phẩm
            </h3>
            <p class="text-xs text-slate-500">194 mã hàng cốt lõi tạo ra 80% doanh thu toàn hệ thống</p>
          </div>
          <div class="relative h-56 w-full flex items-center justify-center">
            <canvas id="prodAbcChart"></canvas>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-100 grid grid-cols-3 text-center text-xs">
            <div>
              <span class="font-black text-blue-700">Hạng A</span>
              <div class="font-bold text-slate-800">194 SKU</div>
              <div class="text-[11px] text-slate-500 font-mono">78.9 Tỷ</div>
            </div>
            <div>
              <span class="font-black text-sky-600">Hạng B</span>
              <div class="font-bold text-slate-800">319 SKU</div>
              <div class="text-[11px] text-slate-500 font-mono">14.9 Tỷ</div>
            </div>
            <div>
              <span class="font-black text-slate-500">Hạng C</span>
              <div class="font-bold text-slate-800">713 SKU</div>
              <div class="text-[11px] text-slate-500 font-mono">5.0 Tỷ</div>
            </div>
          </div>
        </div>

        <!-- Category SKU & Revenue Bar -->
        <div class="lg:col-span-2 bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>🏷️</span> Doanh Số & Số Mã SKU Theo Ngành Hàng
            </h3>
            <p class="text-xs text-slate-500">Chén mài lưỡi cắt (21.2 Tỷ), Mũi khoan Inox (18.6 Tỷ), Dụng cụ đồ nghề (15.2 Tỷ)</p>
          </div>
          <div class="relative h-64 w-full">
            <canvas id="prodCategoryChart"></canvas>
          </div>
        </div>

      </div>

      <!-- PRODUCT MASTER TABLE -->
      <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-4">
        
        <!-- Product Filter Toolbar -->
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>🔍</span> Danh Mục & Bảng Tra Cứu 1,226 SKU Sản Phẩm KingBlue
            </h3>
            <p class="text-xs text-slate-500">Nhấp vào từng sản phẩm để xem xu hướng bán hàng qua 9 tháng và các đại lý mua nhiều nhất</p>
          </div>

          <div class="flex items-center gap-2">
            <span id="filtered-prod-badge" class="bg-teal-100 text-teal-800 font-extrabold text-xs px-2.5 py-0.5 rounded-full">1,226 / 1,226 SKU</span>
            <button onclick="exportProductsCSV()" class="bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs px-3 py-1.5 rounded-xl transition flex items-center gap-1 shadow-xs">
              <span>📥</span> Xuất Excel SP
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
          <!-- Search -->
          <div class="sm:col-span-2 relative">
            <input type="text" id="prod-search-input" oninput="applyProdFilters()" placeholder="Tìm mã hàng, tên sản phẩm..." class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 pl-8 focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-500 transition">
            <span class="absolute left-2.5 top-2.5 text-slate-400 text-xs">🔎</span>
          </div>

          <!-- Category Filter -->
          <div>
            <select id="prod-category-filter" onchange="applyProdFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-500 transition">
              <option value="ALL">Tất cả Ngành Hàng</option>
            </select>
          </div>

          <!-- ABC Filter -->
          <div>
            <select id="prod-abc-filter" onchange="applyProdFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-500 transition">
              <option value="ALL">Tất cả Hạng ABC</option>
              <option value="A">Hạng A - Trụ cột (194 SKU)</option>
              <option value="B">Hạng B - Tiềm năng (319 SKU)</option>
              <option value="C">Hạng C - Chậm luân chuyển (713 SKU)</option>
            </select>
          </div>
        </div>

        <!-- Product Table -->
        <div class="overflow-x-auto border border-slate-200 rounded-xl">
          <table class="w-full text-left text-xs whitespace-nowrap">
            <thead class="bg-slate-100 text-slate-700 font-extrabold border-b border-slate-200 select-none">
              <tr>
                <th class="py-3 px-3 cursor-pointer hover:bg-slate-200 transition" onclick="sortProdTable('code')">Mã SKU ⇕</th>
                <th class="py-3 px-3 cursor-pointer hover:bg-slate-200 transition" onclick="sortProdTable('name')">Tên Hàng Hóa ⇕</th>
                <th class="py-3 px-3 cursor-pointer hover:bg-slate-200 transition" onclick="sortProdTable('category')">Ngành Hàng ⇕</th>
                <th class="py-3 px-3 text-center">ĐVT</th>
                <th class="py-3 px-3 text-right cursor-pointer hover:bg-slate-200 transition" onclick="sortProdTable('qty')">Sản Lượng (SL) ⇕</th>
                <th class="py-3 px-3 text-right cursor-pointer hover:bg-slate-200 transition" onclick="sortProdTable('gross')">Doanh Số Gộp ⇕</th>
                <th class="py-3 px-3 text-right cursor-pointer hover:bg-slate-200 transition" onclick="sortProdTable('avg_price')">Đơn Giá TB ⇕</th>
                <th class="py-3 px-3 text-right cursor-pointer hover:bg-slate-200 transition" onclick="sortProdTable('discount_pct')">CK % ⇕</th>
                <th class="py-3 px-3 text-right cursor-pointer hover:bg-slate-200 transition" onclick="sortProdTable('return_pct')">Trả Lại % ⇕</th>
                <th class="py-3 px-3 text-right cursor-pointer hover:bg-slate-200 transition" onclick="sortProdTable('customers_count')">Đại Lý Mua ⇕</th>
                <th class="py-3 px-3 text-center cursor-pointer hover:bg-slate-200 transition" onclick="sortProdTable('abc')">Hạng ABC ⇕</th>
                <th class="py-3 px-3 text-center">Hồ Sơ SP</th>
              </tr>
            </thead>
            <tbody id="product-master-tbody" class="divide-y divide-slate-100">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>

        <!-- Product Pagination -->
        <div class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100 text-xs">
          <div class="text-slate-500" id="prod-pagination-info">
            Hiển thị 1 - 30 trong số 1,226 sản phẩm
          </div>
          <div class="flex items-center gap-1.5" id="prod-pagination-buttons">
            <!-- Buttons generated via JS -->
          </div>
        </div>

      </div>

    </div>

    <!-- ================= TAB 4: CUSTOMER MASTER 360 ================= -->
    <div id="section-customers" class="tab-section hidden space-y-4">
      
      <!-- Customer Search Toolbar -->
      <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div class="flex items-center gap-2">
            <span class="text-base">🔍</span>
            <span class="font-black text-slate-800 text-sm tracking-tight uppercase">Bộ Lọc Khách Hàng Thông Minh</span>
            <span id="filtered-count-badge" class="bg-blue-100 text-blue-800 font-extrabold text-xs px-2.5 py-0.5 rounded-full">393 / 393 Khách</span>
          </div>
          <button onclick="resetFilters()" class="text-xs font-bold text-slate-500 hover:text-rose-600 flex items-center gap-1 transition">
            <span>🔄</span> <span>Đặt lại bộ lọc</span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3">
          <!-- Search Input -->
          <div class="relative">
            <input type="text" id="search-input" oninput="applyFilters()" placeholder="Tìm tên KH, mã KH, SĐT..." class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 pl-8 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
            <span class="absolute left-2.5 top-2.5 text-slate-400 text-xs">🔎</span>
          </div>

          <!-- RFM Segment Dropdown -->
          <div>
            <select id="filter-segment" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
              <option value="ALL">Tất cả Phân Khúc RFM</option>
              <option value="CHAMPION">VIP / Khách hàng Vàng (103)</option>
              <option value="LOYAL">Khách hàng Trung thành (45)</option>
              <option value="POTENTIAL">Tiềm năng phát triển (61)</option>
              <option value="NEW_ACTIVE">Mới / Mua gần đây (9)</option>
              <option value="NEEDS_ATTENTION">Cần chăm sóc / Nguy cơ nguội (33)</option>
              <option value="AT_RISK">Nguy cơ rời bỏ cao (51)</option>
              <option value="LOST">Ngủ đông / Rời bỏ (91)</option>
            </select>
          </div>

          <!-- ABC Tier Dropdown -->
          <div>
            <select id="filter-abc" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
              <option value="ALL">Tất cả Hạng ABC (Pareto)</option>
              <option value="A">Hạng A - Top 80% Doanh thu (42)</option>
              <option value="B">Hạng B - 15% Tiếp theo (80)</option>
              <option value="C">Hạng C - 5% Cuối (271)</option>
            </select>
          </div>

          <!-- Province Dropdown -->
          <div>
            <select id="filter-province" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
              <option value="ALL">Tất cả Tỉnh / Thành phố</option>
            </select>
          </div>

          <!-- Sales Rep Dropdown -->
          <div>
            <select id="filter-sales-rep" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
              <option value="ALL">Tất cả Nhân Viên Sales</option>
            </select>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        
        <!-- Table Toolbar -->
        <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
          <div>
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>👥</span> Danh Bạ Quản Trị & Tra Cứu Khách Hàng 360°
            </h3>
            <p class="text-xs text-slate-500">Nhấp vào từng đại lý để xem chi tiết cơ cấu mua sắm, top sản phẩm và lịch sử mua hàng</p>
          </div>
          <div class="flex items-center gap-3">
            <span class="text-xs text-slate-500">Hiển thị mỗi trang:</span>
            <select id="page-size-select" onchange="changePageSize(this.value)" class="text-xs bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 focus:outline-none">
              <option value="15">15</option>
              <option value="30" selected>30</option>
              <option value="50">50</option>
              <option value="100">100</option>
              <option value="ALL">Tất cả (393)</option>
            </select>
          </div>
        </div>

        <!-- Master Table -->
        <div class="overflow-x-auto border border-slate-200 rounded-xl">
          <table class="w-full text-left text-xs whitespace-nowrap" id="customer-master-table">
            <thead class="bg-slate-100 text-slate-700 font-extrabold border-b border-slate-200 select-none">
              <tr>
                <th class="py-3 px-3 cursor-pointer hover:bg-slate-200 transition" onclick="sortTable('id')">Mã KH ⇕</th>
                <th class="py-3 px-3 cursor-pointer hover:bg-slate-200 transition" onclick="sortTable('name')">Tên Khách Hàng / Đại Lý ⇕</th>
                <th class="py-3 px-3 cursor-pointer hover:bg-slate-200 transition" onclick="sortTable('province')">Tỉnh / Thành ⇕</th>
                <th class="py-3 px-3 cursor-pointer hover:bg-slate-200 transition" onclick="sortTable('main_sales_rep')">Sales Phụ Trách ⇕</th>
                <th class="py-3 px-3 text-right cursor-pointer hover:bg-slate-200 transition" onclick="sortTable('f_orders')">Số Đơn ⇕</th>
                <th class="py-3 px-3 text-right cursor-pointer hover:bg-slate-200 transition" onclick="sortTable('net')">Doanh Thu Thuần ⇕</th>
                <th class="py-3 px-3 text-right cursor-pointer hover:bg-slate-200 transition" onclick="sortTable('discount_pct')">CK % ⇕</th>
                <th class="py-3 px-3 text-center cursor-pointer hover:bg-slate-200 transition" onclick="sortTable('last_date')">Lần Mua Cuối ⇕</th>
                <th class="py-3 px-3 text-center cursor-pointer hover:bg-slate-200 transition" onclick="sortTable('r_days')">Cách Đây ⇕</th>
                <th class="py-3 px-3 text-center cursor-pointer hover:bg-slate-200 transition" onclick="sortTable('abc')">Hạng ABC ⇕</th>
                <th class="py-3 px-3 cursor-pointer hover:bg-slate-200 transition" onclick="sortTable('segment')">Phân Khúc RFM ⇕</th>
                <th class="py-3 px-3 text-center">Hồ Sơ</th>
              </tr>
            </thead>
            <tbody id="master-table-tbody" class="divide-y divide-slate-100">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>

        <!-- Pagination Controls -->
        <div class="flex flex-wrap items-center justify-between gap-3 mt-4 pt-3 border-t border-slate-100 text-xs">
          <div class="text-slate-500" id="pagination-info">
            Hiển thị 1 - 30 trong số 393 khách hàng
          </div>
          <div class="flex items-center gap-1.5" id="pagination-buttons">
            <!-- Buttons generated via JS -->
          </div>
        </div>

      </div>

    </div>

    <!-- ================= TAB 5: STRATEGIC ACTION MATRIX ================= -->
    <div id="section-strategy" class="tab-section hidden space-y-6">
      
      <!-- Top Alert Banner -->
      <div class="bg-gradient-to-r from-amber-500 via-rose-500 to-indigo-600 rounded-2xl p-0.5 shadow-md">
        <div class="bg-white rounded-[14px] p-5">
          <div class="flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3.5">
              <div class="w-12 h-12 rounded-xl bg-rose-100 text-rose-600 flex items-center justify-center text-2xl font-black shrink-0">
                🚨
              </div>
              <div>
                <h3 class="text-base font-black text-slate-900">Ma Trận Cảnh Báo Sức Khỏe Khách Hàng & Chiến Lược Sản Phẩm KingBlue</h3>
                <p class="text-xs text-slate-600">Đề xuất hành động kinh doanh tức thì để bảo vệ doanh thu cốt lõi, tối ưu tồn kho và hồi sinh khách hàng nguội lạnh</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <span class="bg-rose-100 text-rose-800 text-xs font-black px-3 py-1 rounded-lg">51 KH Cần Kích Hoạt Lại (7.32 Tỷ)</span>
              <span class="bg-blue-100 text-blue-800 text-xs font-black px-3 py-1 rounded-lg">194 SKU Hạng A Trọng Yếu (78.9 Tỷ)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Matrices 4 Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <!-- Action 1: At-Risk Rescue -->
        <div class="bg-white rounded-2xl p-5 border-2 border-rose-200 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="bg-rose-500 text-white text-[11px] font-black px-2.5 py-1 rounded-lg uppercase tracking-wider">Khách Hàng Khẩn Cấp #1</span>
              <span class="text-xs font-bold text-rose-600 font-mono">51 Khách • 7.32 Tỷ</span>
            </div>
            <h4 class="font-black text-slate-900 text-sm mb-1.5 flex items-center gap-2">
              <span>⚠️</span> Kích Hoạt Lại Nhóm Khách Hàng Có Nguy Cơ Rời Bỏ (At-Risk)
            </h4>
            <p class="text-xs text-slate-600 leading-relaxed mb-4">
              Nhóm khách hàng này từng đóng góp doanh thu lớn nhưng đã từ <strong>90 đến 150 ngày</strong> không phát sinh đơn hàng mới.
              Đặc biệt cần rà soát lại kênh <strong>Sàn TMĐT Shopee CKO</strong> (đạt 4.87 tỷ trong 6 tháng đầu năm nhưng ngưng từ 30/06/2026).
            </p>
            
            <div class="bg-rose-50 rounded-xl p-3 text-xs text-rose-900 space-y-1.5 border border-rose-100 mb-4">
              <div class="font-bold flex items-center gap-1.5"><span>🎯</span> Hướng dẫn triển khai:</div>
              <ul class="list-disc list-inside space-y-1 text-slate-700">
                <li>Sales phụ trách (Xuân Trang, Thuỳ Trang, Ngọc Bích) liên hệ trực tiếp chủ đại lý trong tuần này.</li>
                <li>Khảo sát tồn kho thực tế các mặt hàng KingBlue và phản hồi của thợ về lưỡi cắt, mũi khoan.</li>
                <li>Áp dụng chính sách "Chào Hàng Mùa Cuối Năm": Tặng thêm 2% chiết khấu hoặc tặng kèm mũi khoét/kìm nếu lên đơn lại trong tháng 10.</li>
              </ul>
            </div>
          </div>

          <button onclick="filterBySegment('AT_RISK')" class="w-full bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs py-2.5 rounded-xl transition shadow">
            Xem Danh Sách 51 Khách Nguy Cơ Rời Bỏ →
          </button>
        </div>

        <!-- Action 2: Product Tier A Supply Chain -->
        <div class="bg-white rounded-2xl p-5 border-2 border-blue-200 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="bg-blue-600 text-white text-[11px] font-black px-2.5 py-1 rounded-lg uppercase tracking-wider">Sản Phẩm Trọng Tâm #2</span>
              <span class="text-xs font-bold text-blue-700 font-mono">194 SKU • 78.89 Tỷ</span>
            </div>
            <h4 class="font-black text-slate-900 text-sm mb-1.5 flex items-center gap-2">
              <span>⭐</span> Bảo Vệ Chuỗi Cung Ứng & Tồn Kho 194 Sản Phẩm Hạng A
            </h4>
            <p class="text-xs text-slate-600 leading-relaxed mb-4">
              194 mã sản phẩm này (Mũi khoan tường KBLJ, Đá cắt D1, Thùng đồ nghề KHD4233, Lưỡi cắt F1-125DN...) quyết định <strong>79.9%</strong> doanh thu KingBlue. Đứt gãy tồn kho bất kỳ mã nào trong nhóm này sẽ kéo tụt ngay doanh số.
            </p>

            <div class="bg-blue-50 rounded-xl p-3 text-xs text-blue-900 space-y-1.5 border border-blue-100 mb-4">
              <div class="font-bold flex items-center gap-1.5"><span>🎯</span> Hướng dẫn triển khai:</div>
              <ul class="list-disc list-inside space-y-1 text-slate-700">
                <li>Bộ phận Kho & Mua hàng thiết lập hạn mức "Tồn kho an toàn tối thiểu" ít nhất 45 ngày bán hàng cho top 194 SKU.</li>
                <li>Lên kế hoạch đặt hàng với nhà máy trước 2-3 tháng đón đầu mùa cao điểm xây dựng và sửa chữa cuối năm.</li>
                <li>Đảm bảo tỷ lệ giao đủ hàng (Order Fill Rate) trên 98% cho các đại lý Hạng A.</li>
              </ul>
            </div>
          </div>

          <button onclick="filterProdByABC('A')" class="w-full bg-blue-700 hover:bg-blue-600 text-white font-bold text-xs py-2.5 rounded-xl transition shadow">
            Xem 194 Mã Sản Phẩm Hạng A Chủ Lực →
          </button>
        </div>

        <!-- Action 3: Upgrade Tier B with Bundles -->
        <div class="bg-white rounded-2xl p-5 border-2 border-emerald-200 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="bg-emerald-600 text-white text-[11px] font-black px-2.5 py-1 rounded-lg uppercase tracking-wider">Kích Cầu Tăng Trưởng #3</span>
              <span class="text-xs font-bold text-emerald-700 font-mono">319 SKU B • 14.86 Tỷ</span>
            </div>
            <h4 class="font-black text-slate-900 text-sm mb-1.5 flex items-center gap-2">
              <span>🚀</span> Kích Hoạt 319 Sản Phẩm Hạng B Bằng Chiến Lược Bán Kèm Combo
            </h4>
            <p class="text-xs text-slate-600 leading-relaxed mb-4">
              Nhóm B đang có tiềm năng tăng trưởng rất tốt nhưng độ phủ thị trường chưa tối đa. Cần gắn kết các sản phẩm Hạng B với các sản phẩm Ngôi sao Hạng A.
            </p>

            <div class="bg-emerald-50 rounded-xl p-3 text-xs text-emerald-900 space-y-1.5 border border-emerald-100 mb-4">
              <div class="font-bold flex items-center gap-1.5"><span>🎯</span> Hướng dẫn triển khai:</div>
              <ul class="list-disc list-inside space-y-1 text-slate-700">
                <li>Thiết kế gói Combo: "Mua 5 hộp đá cắt D1 tặng kèm 10 mũi khoan inox" hoặc "Mua máy pin tặng kèm kìm tuốt dây".</li>
                <li>Tập huấn cho Sales giới thiệu thêm mã hàng chéo khi đại lý gọi đặt các mã quen thuộc.</li>
                <li>Thực hiện chương trình trưng bày sản phẩm mới tại kệ đại lý để thợ cơ khí trải nghiệm.</li>
              </ul>
            </div>
          </div>

          <button onclick="filterProdByABC('B')" class="w-full bg-emerald-700 hover:bg-emerald-600 text-white font-bold text-xs py-2.5 rounded-xl transition shadow">
            Xem 319 Mã Sản Phẩm Hạng B Tiềm Năng →
          </button>
        </div>

        <!-- Action 4: Clear Slow-moving Tier C -->
        <div class="bg-white rounded-2xl p-5 border-2 border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="bg-slate-700 text-white text-[11px] font-black px-2.5 py-1 rounded-lg uppercase tracking-wider">Tối Ưu Tồn Kho #4</span>
              <span class="text-xs font-bold text-slate-600 font-mono">713 SKU C • 4.96 Tỷ</span>
            </div>
            <h4 class="font-black text-slate-900 text-sm mb-1.5 flex items-center gap-2">
              <span>🧹</span> Tinh Gọn & Xả Hàng Tồn 713 Sản Phẩm Chậm Luân Chuyển
            </h4>
            <p class="text-xs text-slate-600 leading-relaxed mb-4">
              713 mã SKU chiếm tới <strong>58.2%</strong> danh mục sản phẩm nhưng chỉ đóng góp <strong>5.0%</strong> doanh thu. Việc ôm quá nhiều mã hàng bán chậm gây chôn vốn và tốn diện tích kho bãi.
            </p>

            <div class="bg-slate-50 rounded-xl p-3 text-xs text-slate-800 space-y-1.5 border border-slate-200 mb-4">
              <div class="font-bold flex items-center gap-1.5"><span>🎯</span> Hướng dẫn triển khai:</div>
              <ul class="list-disc list-inside space-y-1 text-slate-700">
                <li>Rà soát lọc ra các SKU có dưới 3 khách mua trong 9 tháng để đưa vào danh sách thanh lý xả kho.</li>
                <li>Chạy chương trình Flash Sale xả hàng tồn cuối năm cho đại lý với mức giảm giá từ 10% - 20%.</li>
                <li>Ngừng nhập khẩu/đặt hàng các biến thể kích thước ít người dùng.</li>
              </ul>
            </div>
          </div>

          <button onclick="filterProdByABC('C')" class="w-full bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs py-2.5 rounded-xl transition shadow">
            Xem 713 Mã Sản Phẩm Cần Tinh Gọn →
          </button>
        </div>

      </div>

    </div>

  </main>

  <!-- ================= CUSTOMER 360 MODAL ================= -->
  <div id="customer-modal" class="fixed inset-0 bg-slate-950/60 backdrop-blur-xs z-50 hidden flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
    <div class="bg-white rounded-3xl max-w-3xl w-full shadow-2xl border border-slate-200 overflow-hidden my-auto max-h-[90vh] flex flex-col">
      <div class="bg-[#1A365D] text-white p-5 border-b-4 border-amber-400 flex items-start justify-between">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-2xl bg-amber-400 text-slate-950 flex items-center justify-center font-black text-xl shadow">
            🏢
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span id="modal-cust-id" class="text-xs font-mono bg-blue-800/80 px-2 py-0.5 rounded text-blue-200 font-bold">Mã KH</span>
              <span id="modal-cust-abc" class="text-xs font-black px-2 py-0.5 rounded uppercase">Hạng A</span>
              <span id="modal-cust-segment" class="text-xs font-bold px-2 py-0.5 rounded">VIP</span>
            </div>
            <h3 id="modal-cust-name" class="text-lg font-black mt-1 text-white">Tên Khách Hàng</h3>
            <p id="modal-cust-address" class="text-xs text-blue-200 mt-0.5 truncate max-w-lg">Địa chỉ khách hàng</p>
          </div>
        </div>
        <button onclick="closeCustomerModal()" class="text-white/70 hover:text-white text-2xl font-black p-1 transition">
          ✕
        </button>
      </div>

      <div class="p-6 overflow-y-auto custom-scrollbar space-y-6 flex-1 text-xs">
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="bg-blue-50/70 p-3 rounded-xl border border-blue-100">
            <div class="text-[10px] text-blue-800 uppercase font-bold">Doanh Thu Thuần</div>
            <div id="modal-cust-net" class="text-base font-black text-blue-900 font-mono mt-0.5">0 ₫</div>
            <div class="text-[11px] text-slate-500 mt-0.5">Gross: <span id="modal-cust-gross" class="font-mono">0 ₫</span></div>
          </div>
          <div class="bg-amber-50/70 p-3 rounded-xl border border-amber-100">
            <div class="text-[10px] text-amber-800 uppercase font-bold">Chiết Khấu Đã Hưởng</div>
            <div id="modal-cust-discount" class="text-base font-black text-amber-700 font-mono mt-0.5">0 ₫</div>
            <div class="text-[11px] text-slate-500 mt-0.5">Tỷ lệ: <span id="modal-cust-discount-pct" class="font-bold">0%</span></div>
          </div>
          <div class="bg-emerald-50/70 p-3 rounded-xl border border-emerald-100">
            <div class="text-[10px] text-emerald-800 uppercase font-bold">Số Đơn Hàng</div>
            <div id="modal-cust-orders" class="text-base font-black text-emerald-900 font-mono mt-0.5">0 Đơn</div>
            <div class="text-[11px] text-slate-500 mt-0.5">Tổng SL: <span id="modal-cust-qty" class="font-bold">0</span> sp</div>
          </div>
          <div class="bg-indigo-50/70 p-3 rounded-xl border border-indigo-100">
            <div class="text-[10px] text-indigo-800 uppercase font-bold">Chu Kỳ Mua Hàng</div>
            <div id="modal-cust-recency" class="text-base font-black text-indigo-900 font-mono mt-0.5">0 Ngày</div>
            <div class="text-[11px] text-slate-500 mt-0.5">Gần nhất: <span id="modal-cust-last-date">--/--</span></div>
          </div>
        </div>

        <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200 grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <span class="text-slate-400 font-medium block">Số điện thoại:</span>
            <span id="modal-cust-phone" class="font-bold text-slate-800 font-mono text-xs">--</span>
          </div>
          <div>
            <span class="text-slate-400 font-medium block">Tỉnh / Thành phố:</span>
            <span id="modal-cust-province" class="font-bold text-slate-800 text-xs">--</span>
          </div>
          <div>
            <span class="text-slate-400 font-medium block">Sales phụ trách chính:</span>
            <span id="modal-cust-sales" class="font-black text-blue-700 text-xs">--</span>
          </div>
        </div>

        <div>
          <h4 class="font-black text-slate-900 text-xs uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
            <span>📦</span> Các Nhóm Ngành Hàng Đại Lý Tiêu Thụ Nhiều Nhất
          </h4>
          <div id="modal-cust-categories" class="space-y-2"></div>
        </div>

        <div>
          <h4 class="font-black text-slate-900 text-xs uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
            <span>🏷️</span> Top 5 Sản Phẩm Đại Lý Mua Nhiều Nhất
          </h4>
          <div class="border border-slate-200 rounded-xl overflow-hidden">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-100 font-bold text-slate-600">
                <tr>
                  <th class="py-2 px-3">Tên Sản Phẩm</th>
                  <th class="py-2 px-3 text-right">Số Lượng</th>
                  <th class="py-2 px-3 text-right">Doanh Số Gộp</th>
                </tr>
              </thead>
              <tbody id="modal-cust-products" class="divide-y divide-slate-100"></tbody>
            </table>
          </div>
        </div>

        <div class="bg-blue-50 border border-blue-200 rounded-2xl p-4">
          <div class="font-black text-blue-900 text-xs flex items-center gap-1.5 mb-1">
            <span>💡</span> Khuyến Nghị Hành Động Chăm Sóc Cho Đại Lý Này:
          </div>
          <p id="modal-cust-action" class="text-xs text-blue-800 leading-relaxed font-medium">--</p>
        </div>
      </div>

      <div class="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
        <span class="text-[11px] text-slate-400">KingBlue Customer Intelligence 360° View</span>
        <button onclick="closeCustomerModal()" class="bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs px-4 py-2 rounded-xl transition">
          Đóng cửa sổ
        </button>
      </div>
    </div>
  </div>

  <!-- ================= PRODUCT 360 MODAL (NEW!) ================= -->
  <div id="product-modal" class="fixed inset-0 bg-slate-950/60 backdrop-blur-xs z-50 hidden flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
    <div class="bg-white rounded-3xl max-w-3xl w-full shadow-2xl border border-slate-200 overflow-hidden my-auto max-h-[90vh] flex flex-col">
      
      <!-- Modal Header -->
      <div class="bg-gradient-to-r from-teal-900 to-slate-900 text-white p-5 border-b-4 border-amber-400 flex items-start justify-between">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-2xl bg-teal-500 text-white flex items-center justify-center font-black text-xl shadow">
            📦
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span id="modal-prod-code" class="text-xs font-mono bg-teal-800 px-2 py-0.5 rounded text-teal-200 font-bold">Mã SKU</span>
              <span id="modal-prod-category" class="text-xs bg-white/20 text-white px-2 py-0.5 rounded font-bold">Ngành Hàng</span>
              <span id="modal-prod-abc" class="text-xs font-black px-2 py-0.5 rounded uppercase">Hạng A</span>
            </div>
            <h3 id="modal-prod-name" class="text-lg font-black mt-1 text-white">Tên Sản Phẩm</h3>
            <p class="text-xs text-teal-200 mt-0.5">Đơn vị tính: <strong id="modal-prod-unit">Cái</strong> • <span id="modal-prod-penetration">0 đại lý mua</span></p>
          </div>
        </div>
        <button onclick="closeProductModal()" class="text-white/70 hover:text-white text-2xl font-black p-1 transition">
          ✕
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 overflow-y-auto custom-scrollbar space-y-6 flex-1 text-xs">
        
        <!-- Metrics Row -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="bg-teal-50/70 p-3 rounded-xl border border-teal-100">
            <div class="text-[10px] text-teal-800 uppercase font-bold">Doanh Số Gộp</div>
            <div id="modal-prod-gross" class="text-base font-black text-teal-900 font-mono mt-0.5">0 ₫</div>
            <div class="text-[11px] text-slate-500 mt-0.5">Thuần: <span id="modal-prod-net" class="font-mono">0 ₫</span></div>
          </div>
          <div class="bg-blue-50/70 p-3 rounded-xl border border-blue-100">
            <div class="text-[10px] text-blue-800 uppercase font-bold">Sản Lượng Bán (SL)</div>
            <div id="modal-prod-qty" class="text-base font-black text-blue-900 font-mono mt-0.5">0</div>
            <div class="text-[11px] text-slate-500 mt-0.5">Khuyến mãi: <span id="modal-prod-promo" class="font-mono">0</span></div>
          </div>
          <div class="bg-amber-50/70 p-3 rounded-xl border border-amber-100">
            <div class="text-[10px] text-amber-800 uppercase font-bold">Đơn Giá Trung Bình</div>
            <div id="modal-prod-price" class="text-base font-black text-amber-700 font-mono mt-0.5">0 ₫</div>
            <div class="text-[11px] text-slate-500 mt-0.5">Min: <span id="modal-prod-min-price">0</span> • Max: <span id="modal-prod-max-price">0</span></div>
          </div>
          <div class="bg-rose-50/70 p-3 rounded-xl border border-rose-100">
            <div class="text-[10px] text-rose-800 uppercase font-bold">Tỷ Lệ Hoàn Trả Lại</div>
            <div id="modal-prod-return-pct" class="text-base font-black text-rose-700 font-mono mt-0.5">0%</div>
            <div class="text-[11px] text-slate-500 mt-0.5">SL trả: <span id="modal-prod-return-qty">0</span> sp</div>
          </div>
        </div>

        <!-- Monthly Sales Trend Chart in Modal -->
        <div>
          <h4 class="font-black text-slate-900 text-xs uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
            <span>📈</span> Xu Hướng Doanh Số 9 Tháng (T1 - T9/2026)
          </h4>
          <div class="relative h-44 w-full bg-slate-50 p-3 rounded-2xl border border-slate-200">
            <canvas id="modalProdMonthlyChart"></canvas>
          </div>
        </div>

        <!-- Top 5 Customers Buying This Product -->
        <div>
          <h4 class="font-black text-slate-900 text-xs uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
            <span>🏢</span> Top 5 Đại Lý / Khách Hàng Tiêu Thụ Nhiều Nhất
          </h4>
          <div class="border border-slate-200 rounded-xl overflow-hidden">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-100 font-bold text-slate-600">
                <tr>
                  <th class="py-2 px-3">Tên Đại Lý / Khách Hàng</th>
                  <th class="py-2 px-3 text-right">Tổng Tiền Đã Mua</th>
                  <th class="py-2 px-3 text-center">Thao Tác</th>
                </tr>
              </thead>
              <tbody id="modal-prod-customers" class="divide-y divide-slate-100"></tbody>
            </table>
          </div>
        </div>

        <!-- Strategy Box -->
        <div class="bg-teal-50 border border-teal-200 rounded-2xl p-4">
          <div class="font-black text-teal-900 text-xs flex items-center gap-1.5 mb-1">
            <span>💡</span> Khuyến Nghị Chiến Lược Danh Mục Cho Mã Sản Phẩm Này:
          </div>
          <p id="modal-prod-action" class="text-xs text-teal-800 leading-relaxed font-medium">--</p>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
        <span class="text-[11px] text-slate-400">KingBlue Product Intelligence 360° View</span>
        <button onclick="closeProductModal()" class="bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs px-4 py-2 rounded-xl transition">
          Đóng cửa sổ
        </button>
      </div>

    </div>
  </div>

  <!-- ================= EMBEDDED DATA & JAVASCRIPT ================= -->
  <script>
    const RAW_DATA = {json_str};

    let allCustomers = RAW_DATA.customers || [];
    let filteredCustomers = [...allCustomers];
    let custCurrentPage = 1;
    let custPageSize = 30;
    let custSort = {{ col: 'net', asc: false }};

    let allProducts = RAW_DATA.products || [];
    let filteredProducts = [...allProducts];
    let prodCurrentPage = 1;
    let prodPageSize = 30;
    let prodSort = {{ col: 'gross', asc: false }};

    let modalProdChartInstance = null;

    function fmtVND(num) {{
      if (Math.abs(num) >= 1e9) return (num / 1e9).toFixed(2) + ' Tỷ';
      if (Math.abs(num) >= 1e6) return (num / 1e6).toFixed(1) + ' Tr';
      return new Intl.NumberFormat('vi-VN').format(Math.round(num)) + ' ₫';
    }}

    function fmtFullVND(num) {{
      return new Intl.NumberFormat('vi-VN').format(Math.round(num)) + ' ₫';
    }}

    function fmtNumber(num) {{
      return new Intl.NumberFormat('vi-VN').format(Math.round(num));
    }}

    // Init Page
    window.addEventListener('DOMContentLoaded', () => {{
      populateFilterDropdowns();
      initCharts();
      renderTopCustomers();
      renderSalesDetail();
      renderProvinceDetail();
      renderMasterTable();
      renderProductMasterTable();
    }});

    function populateFilterDropdowns() {{
      // Provinces
      const provSelect = document.getElementById('filter-province');
      RAW_DATA.provinces.forEach(p => {{
        const opt = document.createElement('option');
        opt.value = p.province;
        opt.textContent = `${{p.province}} (${{p.customers}} KH - ${{fmtVND(p.net)}})`;
        provSelect.appendChild(opt);
      }});

      // Sales reps
      const salesSelect = document.getElementById('filter-sales-rep');
      RAW_DATA.sales_reps.forEach(s => {{
        const opt = document.createElement('option');
        opt.value = s.name;
        opt.textContent = `${{s.name}} (${{s.customers}} KH - ${{fmtVND(s.net)}})`;
        salesSelect.appendChild(opt);
      }});

      // Product Categories
      const catSelect = document.getElementById('prod-category-filter');
      RAW_DATA.categories.forEach(c => {{
        const opt = document.createElement('option');
        opt.value = c.name;
        opt.textContent = `${{c.name}} (${{c.skus_count}} SKU - ${{fmtVND(c.gross)}})`;
        catSelect.appendChild(opt);
      }});
    }}

    // Switch Tabs
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.classList.remove('active');
        btn.classList.add('bg-white', 'text-slate-700', 'border-slate-200');
      }});
      document.querySelectorAll('.tab-section').forEach(sec => sec.classList.add('hidden'));

      const activeBtn = document.getElementById('tab-' + tabId);
      if (activeBtn) {{
        activeBtn.classList.add('active');
        activeBtn.classList.remove('bg-white', 'text-slate-700', 'border-slate-200');
      }}
      const activeSec = document.getElementById('section-' + tabId);
      if (activeSec) activeSec.classList.remove('hidden');
    }}

    // ================= CUSTOMER LOGIC =================
    function applyFilters() {{
      const search = document.getElementById('search-input').value.toLowerCase().trim();
      const seg = document.getElementById('filter-segment').value;
      const abc = document.getElementById('filter-abc').value;
      const prov = document.getElementById('filter-province').value;
      const sales = document.getElementById('filter-sales-rep').value;

      filteredCustomers = allCustomers.filter(c => {{
        if (search) {{
          const matchSearch = c.name.toLowerCase().includes(search) ||
                              c.id.toLowerCase().includes(search) ||
                              c.phone.includes(search) ||
                              c.province.toLowerCase().includes(search);
          if (!matchSearch) return false;
        }}
        if (seg !== 'ALL' && c.segment_code !== seg) return false;
        if (abc !== 'ALL' && c.abc !== abc) return false;
        if (prov !== 'ALL' && c.province !== prov) return false;
        if (sales !== 'ALL' && c.main_sales_rep !== sales) return false;
        return true;
      }});

      sortCustData();
      custCurrentPage = 1;
      renderMasterTable();
      updateFilteredStats();
    }}

    function resetFilters() {{
      document.getElementById('search-input').value = '';
      document.getElementById('filter-segment').value = 'ALL';
      document.getElementById('filter-abc').value = 'ALL';
      document.getElementById('filter-province').value = 'ALL';
      document.getElementById('filter-sales-rep').value = 'ALL';
      applyFilters();
    }}

    function updateFilteredStats() {{
      const totalFilteredNet = filteredCustomers.reduce((acc, c) => acc + c.net, 0);
      const badge = document.getElementById('filtered-count-badge');
      badge.textContent = `${{filteredCustomers.length}} / ${{allCustomers.length}} KH (${{fmtVND(totalFilteredNet)}})`;
      document.getElementById('tab-cust-count').textContent = filteredCustomers.length;
    }}

    function filterBySegment(segCode) {{
      switchTab('customers');
      document.getElementById('filter-segment').value = segCode;
      applyFilters();
    }}

    function filterByABC(tier) {{
      switchTab('customers');
      document.getElementById('filter-abc').value = tier;
      applyFilters();
    }}

    function sortTable(col) {{
      if (custSort.col === col) {{
        custSort.asc = !custSort.asc;
      }} else {{
        custSort.col = col;
        custSort.asc = (col === 'name' || col === 'id' || col === 'province') ? true : false;
      }}
      sortCustData();
      renderMasterTable();
    }}

    function sortCustData() {{
      filteredCustomers.sort((a, b) => {{
        let valA = a[custSort.col];
        let valB = b[custSort.col];
        if (typeof valA === 'string') valA = valA.toLowerCase();
        if (typeof valB === 'string') valB = valB.toLowerCase();
        if (valA < valB) return custSort.asc ? -1 : 1;
        if (valA > valB) return custSort.asc ? 1 : -1;
        return 0;
      }});
    }}

    function changePageSize(val) {{
      custPageSize = (val === 'ALL') ? filteredCustomers.length || 1 : parseInt(val);
      custCurrentPage = 1;
      renderMasterTable();
    }}

    function renderMasterTable() {{
      const tbody = document.getElementById('master-table-tbody');
      tbody.innerHTML = '';

      const start = (custCurrentPage - 1) * custPageSize;
      const end = Math.min(start + custPageSize, filteredCustomers.length);
      const pageData = filteredCustomers.slice(start, end);

      if (pageData.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="12" class="text-center py-8 text-slate-400">Không tìm thấy khách hàng nào phù hợp với bộ lọc</td></tr>`;
        document.getElementById('pagination-info').textContent = '0 khách hàng';
        document.getElementById('pagination-buttons').innerHTML = '';
        return;
      }}

      pageData.forEach(c => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-blue-50/50 transition cursor-pointer';
        tr.onclick = (e) => {{ if (e.target.tagName !== 'BUTTON') openCustomerModal(c.id); }};

        let abcBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-black badge-c">Hạng C</span>`;
        if (c.abc === 'A') abcBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-black badge-a">Hạng A</span>`;
        else if (c.abc === 'B') abcBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-black badge-b">Hạng B</span>`;

        let recencyBadge = `<span class="text-emerald-700 font-bold">${{c.r_days}} ngày</span>`;
        if (c.r_days > 90) recencyBadge = `<span class="text-rose-600 font-black bg-rose-50 px-1.5 py-0.5 rounded">${{c.r_days}} ngày ⚠️</span>`;
        else if (c.r_days > 45) recencyBadge = `<span class="text-amber-600 font-bold">${{c.r_days}} ngày</span>`;

        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono font-bold text-slate-600">${{c.id}}</td>
          <td class="py-2.5 px-3 font-black text-slate-900">
            <div class="truncate max-w-[220px]" title="${{c.name}}">${{c.name}}</div>
            <div class="text-[10px] text-slate-400 font-normal truncate max-w-[220px]">${{c.phone || c.address || ''}}</div>
          </td>
          <td class="py-2.5 px-3 text-slate-600">${{c.province}}</td>
          <td class="py-2.5 px-3 text-slate-700 font-medium">${{c.main_sales_rep}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-800">${{fmtNumber(c.f_orders)}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-black text-blue-900">${{fmtFullVND(c.net)}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-600">${{c.discount_pct}}%</td>
          <td class="py-2.5 px-3 text-center text-slate-500 font-mono text-[11px]">${{c.last_date}}</td>
          <td class="py-2.5 px-3 text-center">${{recencyBadge}}</td>
          <td class="py-2.5 px-3 text-center">${{abcBadge}}</td>
          <td class="py-2.5 px-3">
            <span class="inline-block px-2 py-0.5 rounded-full text-[10px] font-bold" style="background-color: ${{c.segment_color}}18; color: ${{c.segment_color}};">
              ${{c.segment}}
            </span>
          </td>
          <td class="py-2.5 px-3 text-center">
            <button onclick="event.stopPropagation(); openCustomerModal('${{c.id}}')" class="bg-blue-100 hover:bg-blue-200 text-blue-800 font-extrabold text-[11px] px-2.5 py-1 rounded-lg transition">
              360° 🔍
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      document.getElementById('pagination-info').textContent = `Hiển thị ${{start + 1}} - ${{end}} trong tổng số ${{filteredCustomers.length}} khách hàng`;
      renderCustPaginationButtons();
    }}

    function renderCustPaginationButtons() {{
      const container = document.getElementById('pagination-buttons');
      container.innerHTML = '';
      const totalPages = Math.ceil(filteredCustomers.length / custPageSize) || 1;
      if (totalPages <= 1) return;

      const prevBtn = document.createElement('button');
      prevBtn.className = `px-2 py-1 rounded border text-xs font-bold ${{custCurrentPage === 1 ? 'opacity-40 cursor-not-allowed border-slate-200' : 'hover:bg-slate-100 border-slate-300'}}`;
      prevBtn.textContent = '◀';
      prevBtn.disabled = custCurrentPage === 1;
      prevBtn.onclick = () => {{ if (custCurrentPage > 1) {{ custCurrentPage--; renderMasterTable(); }} }};
      container.appendChild(prevBtn);

      let startP = Math.max(1, custCurrentPage - 2);
      let endP = Math.min(totalPages, startP + 4);
      if (endP - startP < 4) startP = Math.max(1, endP - 4);

      for (let p = startP; p <= endP; p++) {{
        const btn = document.createElement('button');
        btn.className = `px-2.5 py-1 rounded text-xs font-bold ${{p === custCurrentPage ? 'bg-blue-600 text-white' : 'hover:bg-slate-100 border border-slate-200 text-slate-700'}}`;
        btn.textContent = p;
        btn.onclick = () => {{ custCurrentPage = p; renderMasterTable(); }};
        container.appendChild(btn);
      }}

      const nextBtn = document.createElement('button');
      nextBtn.className = `px-2 py-1 rounded border text-xs font-bold ${{custCurrentPage === totalPages ? 'opacity-40 cursor-not-allowed border-slate-200' : 'hover:bg-slate-100 border-slate-300'}}`;
      nextBtn.textContent = '▶';
      nextBtn.disabled = custCurrentPage === totalPages;
      nextBtn.onclick = () => {{ if (custCurrentPage < totalPages) {{ custCurrentPage++; renderMasterTable(); }} }};
      container.appendChild(nextBtn);
    }}

    // ================= PRODUCT LOGIC (NEW!) =================
    function applyProdFilters() {{
      const search = document.getElementById('prod-search-input').value.toLowerCase().trim();
      const cat = document.getElementById('prod-category-filter').value;
      const abc = document.getElementById('prod-abc-filter').value;

      filteredProducts = allProducts.filter(p => {{
        if (search) {{
          const match = p.code.toLowerCase().includes(search) || p.name.toLowerCase().includes(search);
          if (!match) return false;
        }}
        if (cat !== 'ALL' && p.category !== cat) return false;
        if (abc !== 'ALL' && p.abc !== abc) return false;
        return true;
      }});

      sortProdData();
      prodCurrentPage = 1;
      renderProductMasterTable();
      document.getElementById('filtered-prod-badge').textContent = `${{filteredProducts.length}} / ${{allProducts.length}} SKU`;
    }}

    function filterProdByABC(tier) {{
      switchTab('products');
      document.getElementById('prod-abc-filter').value = tier;
      applyProdFilters();
    }}

    function sortProdTable(col) {{
      if (prodSort.col === col) {{
        prodSort.asc = !prodSort.asc;
      }} else {{
        prodSort.col = col;
        prodSort.asc = (col === 'code' || col === 'name' || col === 'category') ? true : false;
      }}
      sortProdData();
      renderProductMasterTable();
    }}

    function sortProdData() {{
      filteredProducts.sort((a, b) => {{
        let valA = a[prodSort.col];
        let valB = b[prodSort.col];
        if (typeof valA === 'string') valA = valA.toLowerCase();
        if (typeof valB === 'string') valB = valB.toLowerCase();
        if (valA < valB) return prodSort.asc ? -1 : 1;
        if (valA > valB) return prodSort.asc ? 1 : -1;
        return 0;
      }});
    }}

    function renderProductMasterTable() {{
      const tbody = document.getElementById('product-master-tbody');
      tbody.innerHTML = '';

      const start = (prodCurrentPage - 1) * prodPageSize;
      const end = Math.min(start + prodPageSize, filteredProducts.length);
      const pageData = filteredProducts.slice(start, end);

      if (pageData.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="12" class="text-center py-8 text-slate-400">Không tìm thấy mã sản phẩm nào phù hợp</td></tr>`;
        document.getElementById('prod-pagination-info').textContent = '0 sản phẩm';
        document.getElementById('prod-pagination-buttons').innerHTML = '';
        return;
      }}

      pageData.forEach(p => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-teal-50/40 transition cursor-pointer';
        tr.onclick = (e) => {{ if (e.target.tagName !== 'BUTTON') openProductModal(p.code); }};

        let abcBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-black badge-c">Hạng C</span>`;
        if (p.abc === 'A') abcBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-black badge-a">Hạng A</span>`;
        else if (p.abc === 'B') abcBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-black badge-b">Hạng B</span>`;

        let returnBadge = `<span class="text-slate-500 font-mono">${{p.return_pct}}%</span>`;
        if (p.return_pct > 3) returnBadge = `<span class="text-rose-600 font-bold bg-rose-50 px-1 py-0.5 rounded font-mono">${{p.return_pct}}% ⚠️</span>`;

        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono font-bold text-slate-700">${{p.code}}</td>
          <td class="py-2.5 px-3 font-black text-slate-900">
            <div class="truncate max-w-[240px]" title="${{p.name}}">${{p.name}}</div>
          </td>
          <td class="py-2.5 px-3 text-slate-600 font-medium">${{p.category}}</td>
          <td class="py-2.5 px-3 text-center text-slate-500">${{p.unit}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-teal-900">${{fmtNumber(p.qty)}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-black text-blue-900">${{fmtFullVND(p.gross)}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-700">${{fmtFullVND(p.avg_price)}}</td>
          <td class="py-2.5 px-3 text-right font-mono text-slate-600">${{p.discount_pct}}%</td>
          <td class="py-2.5 px-3 text-right">${{returnBadge}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-800">${{p.customers_count}} KH</td>
          <td class="py-2.5 px-3 text-center">${{abcBadge}}</td>
          <td class="py-2.5 px-3 text-center">
            <button onclick="event.stopPropagation(); openProductModal('${{p.code}}')" class="bg-teal-100 hover:bg-teal-200 text-teal-900 font-extrabold text-[11px] px-2.5 py-1 rounded-lg transition">
              360° 🔍
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      document.getElementById('prod-pagination-info').textContent = `Hiển thị ${{start + 1}} - ${{end}} trong tổng số ${{filteredProducts.length}} sản phẩm`;
      renderProdPaginationButtons();
    }}

    function renderProdPaginationButtons() {{
      const container = document.getElementById('prod-pagination-buttons');
      container.innerHTML = '';
      const totalPages = Math.ceil(filteredProducts.length / prodPageSize) || 1;
      if (totalPages <= 1) return;

      const prevBtn = document.createElement('button');
      prevBtn.className = `px-2 py-1 rounded border text-xs font-bold ${{prodCurrentPage === 1 ? 'opacity-40 cursor-not-allowed border-slate-200' : 'hover:bg-slate-100 border-slate-300'}}`;
      prevBtn.textContent = '◀';
      prevBtn.disabled = prodCurrentPage === 1;
      prevBtn.onclick = () => {{ if (prodCurrentPage > 1) {{ prodCurrentPage--; renderProductMasterTable(); }} }};
      container.appendChild(prevBtn);

      let startP = Math.max(1, prodCurrentPage - 2);
      let endP = Math.min(totalPages, startP + 4);
      if (endP - startP < 4) startP = Math.max(1, endP - 4);

      for (let p = startP; p <= endP; p++) {{
        const btn = document.createElement('button');
        btn.className = `px-2.5 py-1 rounded text-xs font-bold ${{p === prodCurrentPage ? 'bg-teal-600 text-white' : 'hover:bg-slate-100 border border-slate-200 text-slate-700'}}`;
        btn.textContent = p;
        btn.onclick = () => {{ prodCurrentPage = p; renderProductMasterTable(); }};
        container.appendChild(btn);
      }}

      const nextBtn = document.createElement('button');
      nextBtn.className = `px-2 py-1 rounded border text-xs font-bold ${{prodCurrentPage === totalPages ? 'opacity-40 cursor-not-allowed border-slate-200' : 'hover:bg-slate-100 border-slate-300'}}`;
      nextBtn.textContent = '▶';
      nextBtn.disabled = prodCurrentPage === totalPages;
      nextBtn.onclick = () => {{ if (prodCurrentPage < totalPages) {{ prodCurrentPage++; renderProductMasterTable(); }} }};
      container.appendChild(nextBtn);
    }}

    // Product 360 Modal
    function openProductModal(prodCode) {{
      const prod = allProducts.find(p => p.code === prodCode);
      if (!prod) return;

      document.getElementById('modal-prod-code').textContent = prod.code;
      document.getElementById('modal-prod-name').textContent = prod.name;
      document.getElementById('modal-prod-category').textContent = prod.category;
      document.getElementById('modal-prod-unit').textContent = prod.unit;
      document.getElementById('modal-prod-penetration').textContent = `${{prod.customers_count}} đại lý đã mua (${{prod.customer_penetration_pct}}% độ phủ)`;

      const abcEl = document.getElementById('modal-prod-abc');
      abcEl.textContent = 'Hạng ' + prod.abc;
      abcEl.className = 'text-xs font-black px-2 py-0.5 rounded uppercase ' + (prod.abc === 'A' ? 'badge-a' : prod.abc === 'B' ? 'badge-b' : 'badge-c');

      document.getElementById('modal-prod-gross').textContent = fmtFullVND(prod.gross);
      document.getElementById('modal-prod-net').textContent = fmtFullVND(prod.net);
      document.getElementById('modal-prod-qty').textContent = fmtNumber(prod.qty) + ' ' + prod.unit;
      document.getElementById('modal-prod-promo').textContent = fmtNumber(prod.promo_qty);
      document.getElementById('modal-prod-price').textContent = fmtFullVND(prod.avg_price);
      document.getElementById('modal-prod-min-price').textContent = fmtFullVND(prod.min_price);
      document.getElementById('modal-prod-max-price').textContent = fmtFullVND(prod.max_price);
      document.getElementById('modal-prod-return-pct').textContent = prod.return_pct + '%';
      document.getElementById('modal-prod-return-qty').textContent = fmtNumber(prod.return_qty);
      document.getElementById('modal-prod-action').textContent = prod.action;

      // Top customers for this product
      const custTable = document.getElementById('modal-prod-customers');
      custTable.innerHTML = '';
      if (prod.top_customers && prod.top_customers.length > 0) {{
        prod.top_customers.forEach(c => {{
          const tr = document.createElement('tr');
          tr.className = 'hover:bg-slate-50';
          tr.innerHTML = `
            <td class="py-2 px-3 font-bold text-slate-800">${{c.name}}</td>
            <td class="py-2 px-3 text-right font-mono font-black text-blue-900">${{fmtFullVND(c.gross)}}</td>
            <td class="py-2 px-3 text-center">
              <button onclick="closeProductModal(); openCustomerByName('${{c.name.replace(/'/g, "\\\\'")}}')" class="bg-blue-100 hover:bg-blue-200 text-blue-800 font-bold text-[10px] px-2 py-0.5 rounded transition">
                Xem KH
              </button>
            </td>
          `;
          custTable.appendChild(tr);
        }});
      }} else {{
        custTable.innerHTML = '<tr><td colspan="3" class="text-center py-3 text-slate-400">Chưa có dữ liệu khách hàng</td></tr>';
      }}

      // Monthly Chart in modal
      const ctx = document.getElementById('modalProdMonthlyChart').getContext('2d');
      if (modalProdChartInstance) modalProdChartInstance.destroy();

      const labels = prod.monthly.map(m => `Tháng ${{parseInt(m.month.split('-')[1])}}`);
      const dataGross = prod.monthly.map(m => m.gross / 1e6);

      modalProdChartInstance = new Chart(ctx, {{
        type: 'line',
        data: {{
          labels: labels,
          datasets: [{{
            label: 'Doanh số (Triệu VNĐ)',
            data: dataGross,
            borderColor: '#0d9488',
            backgroundColor: 'rgba(13, 148, 136, 0.1)',
            fill: true,
            tension: 0.3,
            borderWidth: 2,
            pointRadius: 3
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: function(ctx) {{ return `${{ctx.raw.toFixed(1)}} Triệu VNĐ`; }}
              }}
            }}
          }},
          scales: {{
            y: {{ grid: {{ color: '#f1f5f9' }} }}
          }}
        }}
      }});

      document.getElementById('product-modal').classList.remove('hidden');
    }}

    function closeProductModal() {{
      document.getElementById('product-modal').classList.add('hidden');
    }}

    function openCustomerByName(name) {{
      const cust = allCustomers.find(c => c.name === name);
      if (cust) openCustomerModal(cust.id);
    }}

    // Top Customers preview
    function renderTopCustomers() {{
      const tbody = document.getElementById('top-customers-tbody');
      tbody.innerHTML = '';
      allCustomers.slice(0, 10).forEach((c, idx) => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-blue-50/50 transition cursor-pointer';
        tr.onclick = () => openCustomerModal(c.id);

        let rankBadge = `<span class="w-5 h-5 rounded-full bg-slate-200 text-slate-800 font-black inline-flex items-center justify-center text-[10px]">${{idx + 1}}</span>`;
        if (idx === 0) rankBadge = `<span class="w-5 h-5 rounded-full bg-amber-400 text-slate-950 font-black inline-flex items-center justify-center text-[10px]">🥇</span>`;
        if (idx === 1) rankBadge = `<span class="w-5 h-5 rounded-full bg-slate-300 text-slate-950 font-black inline-flex items-center justify-center text-[10px]">🥈</span>`;
        if (idx === 2) rankBadge = `<span class="w-5 h-5 rounded-full bg-amber-700 text-white font-black inline-flex items-center justify-center text-[10px]">🥉</span>`;

        tr.innerHTML = `
          <td class="py-2.5 px-3">${{rankBadge}}</td>
          <td class="py-2.5 px-3 font-mono font-bold text-slate-600">${{c.id}}</td>
          <td class="py-2.5 px-3 font-black text-slate-900">${{c.name}}</td>
          <td class="py-2.5 px-3 text-slate-600">${{c.province}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-800">${{fmtNumber(c.f_orders)}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-black text-blue-900">${{fmtFullVND(c.net)}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-600">${{c.discount_pct}}%</td>
          <td class="py-2.5 px-3 text-center text-slate-500 font-mono text-[11px]">${{c.last_date}}</td>
          <td class="py-2.5 px-3">
            <span class="inline-block px-2 py-0.5 rounded-full text-[10px] font-bold" style="background-color: ${{c.segment_color}}18; color: ${{c.segment_color}};">
              ${{c.segment}}
            </span>
          </td>
          <td class="py-2.5 px-3 text-center">
            <button onclick="event.stopPropagation(); openCustomerModal('${{c.id}}')" class="bg-blue-100 hover:bg-blue-200 text-blue-800 font-bold text-[10px] px-2 py-0.5 rounded transition">
              Chi tiết
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderSalesDetail() {{
      const tbody = document.getElementById('sales-detail-tbody');
      tbody.innerHTML = '';
      RAW_DATA.sales_reps.forEach((s, idx) => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-bold text-slate-600">#${{idx + 1}}</td>
          <td class="py-2.5 px-3 font-black text-slate-900 text-xs">${{s.name}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-black text-blue-900">${{fmtFullVND(s.net)}}</td>
          <td class="py-2.5 px-3 text-right font-mono text-slate-600">${{fmtFullVND(s.gross)}}</td>
          <td class="py-2.5 px-3 text-right font-mono text-amber-700 font-bold">${{fmtFullVND(s.discount)}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-800">${{s.customers}} KH</td>
          <td class="py-2.5 px-3 text-right font-mono text-slate-700">${{fmtNumber(s.orders)}} đơn</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-emerald-700">${{fmtVND(s.arpu)}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-extrabold text-blue-700">${{s.pct_of_total}}%</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderProvinceDetail() {{
      const tbody = document.getElementById('province-detail-tbody');
      tbody.innerHTML = '';
      RAW_DATA.provinces.forEach(p => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 transition';
        tr.innerHTML = `
          <td class="py-2 px-3 font-bold text-slate-900">${{p.province}}</td>
          <td class="py-2 px-3 text-right font-mono font-black text-blue-900">${{fmtFullVND(p.net)}}</td>
          <td class="py-2 px-3 text-right font-mono text-slate-600">${{fmtFullVND(p.gross)}}</td>
          <td class="py-2 px-3 text-right font-mono font-bold text-slate-700">${{p.customers}} KH</td>
          <td class="py-2 px-3 text-right font-mono text-slate-600">${{fmtNumber(p.orders)}} đơn</td>
          <td class="py-2 px-3 text-right font-mono font-bold text-blue-700">${{p.pct_of_total}}%</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function openCustomerModal(custId) {{
      const cust = allCustomers.find(c => c.id === custId);
      if (!cust) return;

      document.getElementById('modal-cust-id').textContent = cust.id;
      document.getElementById('modal-cust-name').textContent = cust.name;
      document.getElementById('modal-cust-address').textContent = cust.address || 'Chưa cập nhật địa chỉ';
      document.getElementById('modal-cust-phone').textContent = cust.phone || 'Chưa có SĐT';
      document.getElementById('modal-cust-province').textContent = cust.province;
      document.getElementById('modal-cust-sales').textContent = cust.main_sales_rep;

      const abcEl = document.getElementById('modal-cust-abc');
      abcEl.textContent = 'Hạng ' + cust.abc;
      abcEl.className = 'text-xs font-black px-2 py-0.5 rounded uppercase ' + (cust.abc === 'A' ? 'badge-a' : cust.abc === 'B' ? 'badge-b' : 'badge-c');

      const segEl = document.getElementById('modal-cust-segment');
      segEl.textContent = cust.segment;
      segEl.style.backgroundColor = cust.segment_color + '25';
      segEl.style.color = cust.segment_color;

      document.getElementById('modal-cust-net').textContent = fmtFullVND(cust.net);
      document.getElementById('modal-cust-gross').textContent = fmtFullVND(cust.gross);
      document.getElementById('modal-cust-discount').textContent = fmtFullVND(cust.discount);
      document.getElementById('modal-cust-discount-pct').textContent = cust.discount_pct + '%';
      document.getElementById('modal-cust-orders').textContent = fmtNumber(cust.f_orders) + ' Đơn';
      document.getElementById('modal-cust-qty').textContent = fmtNumber(cust.total_qty);
      document.getElementById('modal-cust-recency').textContent = cust.r_days + ' Ngày';
      document.getElementById('modal-cust-last-date').textContent = cust.last_date;
      document.getElementById('modal-cust-action').textContent = cust.action;

      const catContainer = document.getElementById('modal-cust-categories');
      catContainer.innerHTML = '';
      if (cust.top_categories && cust.top_categories.length > 0) {{
        const maxCatVal = cust.top_categories[0].gross || 1;
        cust.top_categories.forEach(cat => {{
          const pct = Math.min(100, Math.round((cat.gross / maxCatVal) * 100));
          const row = document.createElement('div');
          row.className = 'space-y-1';
          row.innerHTML = `
            <div class="flex justify-between font-medium">
              <span class="text-slate-800 font-bold">${{cat.name}}</span>
              <span class="font-mono text-blue-900 font-bold">${{fmtFullVND(cat.gross)}}</span>
            </div>
            <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
              <div class="bg-blue-600 h-full rounded-full" style="width: ${{pct}}%;"></div>
            </div>
          `;
          catContainer.appendChild(row);
        }});
      }}

      const prodTable = document.getElementById('modal-cust-products');
      prodTable.innerHTML = '';
      if (cust.top_products && cust.top_products.length > 0) {{
        cust.top_products.forEach(p => {{
          const tr = document.createElement('tr');
          tr.className = 'hover:bg-slate-50';
          tr.innerHTML = `
            <td class="py-2 px-3 font-medium text-slate-800">${{p.name}}</td>
            <td class="py-2 px-3 text-right font-mono font-bold text-slate-700">${{fmtNumber(p.qty)}}</td>
            <td class="py-2 px-3 text-right font-mono font-black text-blue-900">${{fmtFullVND(p.gross)}}</td>
          `;
          prodTable.appendChild(tr);
        }});
      }}

      document.getElementById('customer-modal').classList.remove('hidden');
    }}

    function closeCustomerModal() {{
      document.getElementById('customer-modal').classList.add('hidden');
    }}

    // Export CSVs
    function exportCustomersCSV() {{
      let csvContent = "\\uFEFFMã KH,Tên Khách Hàng,Tỉnh Thành,Sales Phụ Trách,Số Đơn,Doanh Thu Thuần,Doanh Số Gộp,Chiết Khấu,Tỷ Lệ CK,Lần Mua Cuối,Recency Ngày,Hạng ABC,Phân Khúc RFM\\n";
      filteredCustomers.forEach(c => {{
        const row = [`"${{c.id}}"`, `"${{c.name.replace(/"/g, '""')}}"`, `"${{c.province}}"`, `"${{c.main_sales_rep}}"`, c.f_orders, c.net, c.gross, c.discount, c.discount_pct, `"${{c.last_date}}"`, c.r_days, `"${{c.abc}}"`, `"${{c.segment}}"`];
        csvContent += row.join(",") + "\\n";
      }});
      downloadFile(csvContent, `KingBlue_Danh_Sach_Khach_Hang_${{new Date().toISOString().slice(0, 10)}}.csv`);
    }}

    function exportProductsCSV() {{
      let csvContent = "\\uFEFFMã SKU,Tên Sản Phẩm,Ngành Hàng,ĐVT,Sản Lượng,Doanh Số Gộp,Doanh Thu Thuần,Đơn Giá TB,Chiết Khấu,Tỷ Lệ Trả Lại %,Số Khách Mua,Hạng ABC\\n";
      filteredProducts.forEach(p => {{
        const row = [`"${{p.code}}"`, `"${{p.name.replace(/"/g, '""')}}"`, `"${{p.category}}"`, `"${{p.unit}}"`, p.qty, p.gross, p.net, p.avg_price, p.discount_pct, p.return_pct, p.customers_count, `"${{p.abc}}"`];
        csvContent += row.join(",") + "\\n";
      }});
      downloadFile(csvContent, `KingBlue_Danh_Sach_San_Pham_SKU_${{new Date().toISOString().slice(0, 10)}}.csv`);
    }}

    function downloadFile(content, fileName) {{
      const blob = new Blob([content], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', fileName);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    // Charts
    function initCharts() {{
      // 1. Monthly Chart
      const ctxMonthly = document.getElementById('monthlyChart').getContext('2d');
      new Chart(ctxMonthly, {{
        type: 'bar',
        data: {{
          labels: RAW_DATA.monthly.map(m => m.month_label),
          datasets: [
            {{ type: 'line', label: 'Số đơn hàng', data: RAW_DATA.monthly.map(m => m.orders), borderColor: '#f59e0b', backgroundColor: '#f59e0b', yAxisID: 'yOrders', borderWidth: 2, tension: 0.3, pointRadius: 4 }},
            {{ type: 'bar', label: 'Doanh thu thuần (Tỷ VNĐ)', data: RAW_DATA.monthly.map(m => m.net / 1e9), backgroundColor: '#2563eb', borderRadius: 6, yAxisID: 'yRev' }},
            {{ type: 'bar', label: 'Chiết khấu (Tỷ VNĐ)', data: RAW_DATA.monthly.map(m => m.discount / 1e9), backgroundColor: '#93c5fd', borderRadius: 6, yAxisID: 'yRev' }}
          ]
        }},
        options: {{
          responsive: true, maintainAspectRatio: false, interaction: {{ mode: 'index', intersect: false }},
          scales: {{
            yRev: {{ type: 'linear', position: 'left', grid: {{ color: '#f1f5f9' }} }},
            yOrders: {{ type: 'linear', position: 'right', grid: {{ drawOnChartArea: false }} }}
          }}
        }}
      }});

      // 2. ABC Donut
      const ctxAbc = document.getElementById('abcChart').getContext('2d');
      new Chart(ctxAbc, {{
        type: 'doughnut',
        data: {{
          labels: ['Hạng A (80% DT)', 'Hạng B (15% DT)', 'Hạng C (5% DT)'],
          datasets: [{{ data: [RAW_DATA.abc.find(a => a.tier === 'A').net / 1e9, RAW_DATA.abc.find(a => a.tier === 'B').net / 1e9, RAW_DATA.abc.find(a => a.tier === 'C').net / 1e9], backgroundColor: ['#2563eb', '#0ea5e9', '#cbd5e1'], borderWidth: 3, borderColor: '#ffffff' }}]
        }},
        options: {{ responsive: true, maintainAspectRatio: false, cutout: '68%' }}
      }});

      // 3. RFM Chart
      const ctxRfm = document.getElementById('rfmChart').getContext('2d');
      new Chart(ctxRfm, {{
        type: 'bar',
        data: {{
          labels: RAW_DATA.segments.map(s => s.name.split('/')[0].trim()),
          datasets: [{{ label: 'Doanh thu thuần (Tỷ VNĐ)', data: RAW_DATA.segments.map(s => s.net / 1e9), backgroundColor: RAW_DATA.segments.map(s => s.color), borderRadius: 6 }}]
        }},
        options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
      }});

      // 4. Categories Chart
      const ctxCat = document.getElementById('categoryChart').getContext('2d');
      const topCats = RAW_DATA.categories.slice(0, 8);
      new Chart(ctxCat, {{
        type: 'bar',
        data: {{
          labels: topCats.map(c => c.name),
          datasets: [{{ label: 'Doanh số gộp (Tỷ VNĐ)', data: topCats.map(c => c.gross / 1e9), backgroundColor: ['#1e40af', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#cbd5e1', '#e2e8f0'], borderRadius: 6 }}]
        }},
        options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
      }});

      // 5. Province Chart
      const ctxProv = document.getElementById('provinceChart').getContext('2d');
      const topProvs = RAW_DATA.provinces.slice(0, 10);
      new Chart(ctxProv, {{
        type: 'bar',
        data: {{
          labels: topProvs.map(p => p.province),
          datasets: [{{ label: 'Doanh thu thuần (Tỷ VNĐ)', data: topProvs.map(p => p.net / 1e9), backgroundColor: '#1d4ed8', borderRadius: 6 }}]
        }},
        options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
      }});

      // 6. Sales Chart
      const ctxSales = document.getElementById('salesChart').getContext('2d');
      new Chart(ctxSales, {{
        type: 'bar',
        data: {{
          labels: RAW_DATA.sales_reps.map(s => s.name),
          datasets: [{{ label: 'Doanh thu thuần (Tỷ VNĐ)', data: RAW_DATA.sales_reps.map(s => s.net / 1e9), backgroundColor: '#059669', borderRadius: 6 }}]
        }},
        options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
      }});

      // 7. Product Top Revenue Chart (NEW!)
      const ctxProdRev = document.getElementById('prodTopRevChart').getContext('2d');
      const top10ProdRev = allProducts.slice(0, 10);
      new Chart(ctxProdRev, {{
        type: 'bar',
        data: {{
          labels: top10ProdRev.map(p => p.name.length > 25 ? p.name.slice(0, 25) + '...' : p.name),
          datasets: [{{
            label: 'Doanh số gộp (Tỷ VNĐ)',
            data: top10ProdRev.map(p => p.gross / 1e9),
            backgroundColor: '#0d9488',
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                title: function(ctx) {{ return top10ProdRev[ctx[0].dataIndex].name; }},
                label: function(ctx) {{
                  const p = top10ProdRev[ctx.dataIndex];
                  return `${{ctx.raw.toFixed(2)}} Tỷ VNĐ | SL: ${{fmtNumber(p.qty)}} ${{p.unit}} | ${{p.customers_count}} KH`;
                }}
              }}
            }}
          }}
        }}
      }});

      // 8. Product Top Quantity Chart (NEW!)
      const ctxProdQty = document.getElementById('prodTopQtyChart').getContext('2d');
      const top10ProdQty = [...allProducts].sort((a, b) => b.qty - a.qty).slice(0, 10);
      new Chart(ctxProdQty, {{
        type: 'bar',
        data: {{
          labels: top10ProdQty.map(p => p.name.length > 25 ? p.name.slice(0, 25) + '...' : p.name),
          datasets: [{{
            label: 'Sản lượng (Nghìn cái)',
            data: top10ProdQty.map(p => p.qty / 1e3),
            backgroundColor: '#0284c7',
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                title: function(ctx) {{ return top10ProdQty[ctx[0].dataIndex].name; }},
                label: function(ctx) {{
                  const p = top10ProdQty[ctx.dataIndex];
                  return `Sản lượng: ${{fmtNumber(p.qty)}} ${{p.unit}} | DS: ${{fmtVND(p.gross)}}`;
                }}
              }}
            }}
          }}
        }}
      }});

      // 9. Product ABC Donut (NEW!)
      const ctxProdAbc = document.getElementById('prodAbcChart').getContext('2d');
      new Chart(ctxProdAbc, {{
        type: 'doughnut',
        data: {{
          labels: ['Hạng A (194 SKU - 80%)', 'Hạng B (319 SKU - 15%)', 'Hạng C (713 SKU - 5%)'],
          datasets: [{{
            data: RAW_DATA.product_abc.map(a => a.gross / 1e9),
            backgroundColor: ['#2563eb', '#0ea5e9', '#cbd5e1'],
            borderWidth: 3,
            borderColor: '#ffffff'
          }}]
        }},
        options: {{ responsive: true, maintainAspectRatio: false, cutout: '68%' }}
      }});

      // 10. Product Categories SKU & Revenue (NEW!)
      const ctxProdCat = document.getElementById('prodCategoryChart').getContext('2d');
      const catLabels = RAW_DATA.categories.slice(0, 8).map(c => c.name);
      new Chart(ctxProdCat, {{
        type: 'bar',
        data: {{
          labels: catLabels,
          datasets: [
            {{
              type: 'bar',
              label: 'Doanh số gộp (Tỷ VNĐ)',
              data: RAW_DATA.categories.slice(0, 8).map(c => c.gross / 1e9),
              backgroundColor: '#3b82f6',
              borderRadius: 6,
              yAxisID: 'yGross'
            }},
            {{
              type: 'line',
              label: 'Số lượng SKU',
              data: RAW_DATA.categories.slice(0, 8).map(c => c.skus_count),
              borderColor: '#f59e0b',
              backgroundColor: '#f59e0b',
              borderWidth: 2,
              tension: 0.3,
              pointRadius: 4,
              yAxisID: 'ySkus'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          interaction: {{ mode: 'index', intersect: false }},
          scales: {{
            yGross: {{ type: 'linear', position: 'left', grid: {{ color: '#f1f5f9' }} }},
            ySkus: {{ type: 'linear', position: 'right', grid: {{ drawOnChartArea: false }} }}
          }}
        }}
      }});

    }}
  </script>
</body>
</html>
"""

report_html_path = '/Users/Admin/Documents/KIng BLue/Report/customer_dashboard.html'
root_html_path = '/Users/Admin/Documents/KIng BLue/customer_dashboard.html'

with open(report_html_path, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Generated {report_html_path} ({os.path.getsize(report_html_path)/1024:.1f} KB)")

with open(root_html_path, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Generated {root_html_path} ({os.path.getsize(root_html_path)/1024:.1f} KB)")

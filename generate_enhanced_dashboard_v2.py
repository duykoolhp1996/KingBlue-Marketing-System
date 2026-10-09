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
  <title>King Blue - Customer, Product & Reorder Forecasting Dashboard 2026</title>
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
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.5; }}
    }}
    .pulse-dot {{ animation: pulseGlow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }}
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
            <span class="text-[10px] bg-amber-400 text-slate-950 font-black px-2 py-0.5 rounded-full uppercase tracking-wider">AI Forecast Pro</span>
          </div>
          <p class="text-blue-200 text-xs font-medium">Hệ Thống Phân Tích Khách Hàng, Sản Phẩm & Dự Báo Chu Kỳ Hết Hàng Đại Lý 2026</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="flex items-center gap-2">
        <a href="index.html" class="bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold text-xs px-3 py-2 rounded-xl flex items-center gap-1.5 transition">
          <span>🏠</span> <span>Cổng Marketing</span>
        </a>
        <button onclick="exportForecastCSV()" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs px-3 py-2 rounded-xl flex items-center gap-1.5 transition shadow">
          <span>📞</span> <span>Xuất Call List Hôm Nay</span>
        </button>
        <button onclick="exportCustomersCSV()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs px-3 py-2 rounded-xl flex items-center gap-1.5 transition shadow">
          <span>👥</span> <span>Xuất Excel KH</span>
        </button>
        <button onclick="exportProductsCSV()" class="bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs px-3 py-2 rounded-xl flex items-center gap-1.5 transition shadow">
          <span>📦</span> <span>Xuất Excel SP</span>
        </button>
      </div>

    </div>
  </header>

  <!-- ================= SUB HEADER BANNER ================= -->
  <div class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white py-3 border-b border-blue-950/40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-wrap items-center justify-between gap-3 text-xs">
      <div class="flex items-center gap-4 flex-wrap">
        <span class="inline-flex items-center gap-1.5 bg-blue-800/60 px-2.5 py-1 rounded-lg border border-blue-700/50">
          <span class="w-2 h-2 rounded-full bg-emerald-400 pulse-dot"></span>
          <span>Dữ liệu: <strong>70,855</strong> dòng chứng từ</span>
        </span>
        <span class="inline-flex items-center gap-1.5 bg-blue-800/60 px-2.5 py-1 rounded-lg border border-blue-700/50">
          <span>👥 <strong>393 Đại lý</strong></span>
        </span>
        <span class="inline-flex items-center gap-1.5 bg-blue-800/60 px-2.5 py-1 rounded-lg border border-blue-700/50">
          <span>📦 <strong>1,226 SKU</strong></span>
        </span>
        <span class="inline-flex items-center gap-1.5 bg-amber-500/20 text-amber-300 px-2.5 py-1 rounded-lg border border-amber-500/30">
          <span>⚡ <strong>53 Đại Lý Sắp Cạn Tồn Kho</strong></span>
        </span>
      </div>
      <div class="text-blue-300 font-medium">
        Hệ thống Tự Động Tính Chu Kỳ Mua Hàng & Dự Báo Thời Điểm Chốt Đơn Gối Đầu
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
          <span class="font-bold text-slate-700">10,992 Đơn</span>
          <span class="text-slate-300">|</span>
          <span class="text-indigo-600 font-semibold">28 đơn/KH</span>
        </div>
      </div>

      <!-- Dự báo sắp hết hàng (NEW!) -->
      <div class="col-span-2 bg-gradient-to-br from-amber-50 to-orange-50/70 rounded-2xl p-4 border-2 border-amber-300 shadow-sm relative overflow-hidden group hover:shadow-md transition cursor-pointer" onclick="switchTab('forecast')">
        <div class="absolute -right-3 -top-3 w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center text-amber-300 text-2xl font-black pointer-events-none group-hover:scale-110 transition">⚡</div>
        <div class="text-xs font-bold uppercase tracking-wider text-amber-800 mb-1 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-amber-500 pulse-dot"></span>
          <span>Sắp Hết Hàng Cần Gọi</span>
        </div>
        <div class="text-2xl sm:text-3xl font-black text-amber-900 font-mono tracking-tight">53 Đại Lý</div>
        <div class="mt-2 text-xs text-amber-700 font-medium flex items-center gap-1.5">
          <span>Doanh thu: <strong>15.2+ Tỷ</strong></span>
          <span class="text-slate-300">|</span>
          <span class="underline font-bold">Xem ngay →</span>
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
        <span>📦</span> <span>Phân Tích Sản Phẩm (1,226 SKU)</span>
      </button>
      <button onclick="switchTab('forecast')" id="tab-forecast" class="tab-btn bg-white hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-slate-200 transition">
        <span>🔮</span> <span>Dự Đoán Sắp Hết Hàng</span>
        <span class="bg-amber-400 text-slate-950 text-[10px] font-black px-1.5 py-0.5 rounded-full">53 Cần Gọi</span>
      </button>
      <button onclick="switchTab('customers')" id="tab-customers" class="tab-btn bg-white hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-slate-200 transition">
        <span>📋</span> <span>Danh Bạ Khách Hàng 360°</span>
        <span class="bg-blue-100 text-blue-800 text-[10px] font-black px-1.5 py-0.5 rounded-full" id="tab-cust-count">393</span>
      </button>
      <button onclick="switchTab('strategy')" id="tab-strategy" class="tab-btn bg-white hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-slate-200 transition">
        <span>💡</span> <span>Chiến Lược & Cảnh Báo Hành Động</span>
      </button>
    </div>

    <!-- ================= TAB 1: OVERVIEW & SEGMENTATION ================= -->
    <div id="section-overview" class="tab-section space-y-6">
      
      <!-- Charts Row 1: Monthly Trend & ABC Pareto -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
                <span>📊</span> Diễn Biến Doanh Thu Thuần & Chiết Khấu Theo Tháng
              </h3>
              <p class="text-xs text-slate-500">Đỉnh Tháng 3 đạt 16.4 Tỷ và ổn định ở mức 7.5 - 10.6 Tỷ/tháng</p>
            </div>
            <span class="text-xs font-mono font-bold text-blue-700 bg-blue-50 px-2 py-1 rounded-lg">Đỉnh T3: 16.4 Tỷ</span>
          </div>
          <div class="relative h-72 w-full">
            <canvas id="monthlyChart"></canvas>
          </div>
        </div>

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
              <div class="text-[11px] text-slate-500 font-mono">66.9 Tỷ</div>
            </div>
            <div>
              <span class="font-black text-sky-600">Hạng B</span>
              <div class="font-bold text-slate-800">80 KH (20%)</div>
              <div class="text-[11px] text-slate-500 font-mono">12.6 Tỷ</div>
            </div>
            <div>
              <span class="font-black text-slate-500">Hạng C</span>
              <div class="font-bold text-slate-800">271 KH (69%)</div>
              <div class="text-[11px] text-slate-500 font-mono">4.2 Tỷ</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Row 2: RFM Matrix & Top Categories -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>👥</span> Phân Bổ Phân Khúc RFM (Doanh Thu & Số Khách)
            </h3>
            <p class="text-xs text-slate-500">Tần suất mua, Khoảng cách lần mua cuối và Giá trị thanh toán</p>
          </div>
          <div class="relative h-72 w-full">
            <canvas id="rfmChart"></canvas>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>📦</span> Top 8 Ngành Hàng Đóng Góp Doanh Số Cao Nhất
            </h3>
            <p class="text-xs text-slate-500">Chén mài, Lưỡi cắt, Mũi khoan Inox và Đồ nghề chiếm hơn 65% tỷ trọng</p>
          </div>
          <div class="relative h-72 w-full">
            <canvas id="categoryChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Top 10 Preview -->
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
            <tbody id="top-customers-tbody" class="divide-y divide-slate-100"></tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ================= TAB 2: TERRITORY & SALES ================= -->
    <div id="section-territory" class="tab-section hidden space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
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

      <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <div class="mb-4">
          <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
            <span>🎖️</span> Bảng Xếp Hạng Chi Tiết Đội Ngũ Kinh Doanh
          </h3>
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
            <tbody id="sales-detail-tbody" class="divide-y divide-slate-100"></tbody>
          </table>
        </div>
      </div>

      <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <div class="mb-4">
          <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
            <span>🗺️</span> Phân Bổ Thị Trường Theo 39 Tỉnh / Thành Phố
          </h3>
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
            <tbody id="province-detail-tbody" class="divide-y divide-slate-100"></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ================= TAB 3: PRODUCT INTELLIGENCE ================= -->
    <div id="section-products" class="tab-section hidden space-y-6">
      
      <!-- Product KPIs Ribbon -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        <div class="bg-gradient-to-br from-blue-50 to-indigo-50/70 rounded-xl p-4 border border-blue-200 flex items-center justify-between">
          <div>
            <div class="text-[11px] font-bold text-blue-800 uppercase">Sản Phẩm Hạng A (Top 80%)</div>
            <div class="text-2xl font-black text-blue-900 font-mono mt-0.5">194 SKU (15.8%)</div>
            <div class="text-xs text-blue-700 font-medium">Doanh số: <strong>78.89 Tỷ (79.9%)</strong></div>
          </div>
          <div class="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center font-black text-lg shadow">⭐</div>
        </div>

        <div class="bg-gradient-to-br from-sky-50 to-cyan-50/70 rounded-xl p-4 border border-sky-200 flex items-center justify-between">
          <div>
            <div class="text-[11px] font-bold text-sky-800 uppercase">Sản Phẩm Hạng B (15%)</div>
            <div class="text-2xl font-black text-sky-900 font-mono mt-0.5">319 SKU (26.0%)</div>
            <div class="text-xs text-sky-700 font-medium">Doanh số: <strong>14.86 Tỷ (15.1%)</strong></div>
          </div>
          <div class="w-10 h-10 rounded-xl bg-sky-500 text-white flex items-center justify-center font-black text-lg shadow">📈</div>
        </div>

        <div class="bg-gradient-to-br from-slate-50 to-gray-100 rounded-xl p-4 border border-slate-300 flex items-center justify-between">
          <div>
            <div class="text-[11px] font-bold text-slate-700 uppercase">Sản Phẩm Hạng C (5%)</div>
            <div class="text-2xl font-black text-slate-800 font-mono mt-0.5">713 SKU (58.2%)</div>
            <div class="text-xs text-slate-500 font-medium">Chậm luân chuyển: <strong>4.96 Tỷ</strong></div>
          </div>
          <div class="w-10 h-10 rounded-xl bg-slate-600 text-white flex items-center justify-center font-black text-lg shadow">⏳</div>
        </div>

        <div class="bg-gradient-to-br from-teal-50 to-emerald-50/70 rounded-xl p-4 border border-teal-200 flex items-center justify-between">
          <div>
            <div class="text-[11px] font-bold text-teal-800 uppercase">Tổng Sản Lượng Tiêu Thụ</div>
            <div class="text-2xl font-black text-teal-900 font-mono mt-0.5">3.39 Triệu SP</div>
            <div class="text-xs text-teal-700 font-medium">Đơn giá TB: <strong>29,128 ₫ / sp</strong></div>
          </div>
          <div class="w-10 h-10 rounded-xl bg-teal-600 text-white flex items-center justify-center font-black text-lg shadow">📦</div>
        </div>
      </div>

      <!-- Product Charts Row 1 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
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

        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>🚀</span> Top 10 Sản Phẩm Tiêu Thụ Số Lượng (Volume) Lớn Nhất
            </h3>
            <p class="text-xs text-slate-500">Đá cắt sắt D1 hộp sắt đạt 781,801 cái, D3 hộp sắt đạt 398,900 cái</p>
          </div>
          <div class="relative h-80 w-full">
            <canvas id="prodTopQtyChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Product Charts Row 2 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
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
          <div class="sm:col-span-2 relative">
            <input type="text" id="prod-search-input" oninput="applyProdFilters()" placeholder="Tìm mã hàng, tên sản phẩm..." class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 pl-8 focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-500 transition">
            <span class="absolute left-2.5 top-2.5 text-slate-400 text-xs">🔎</span>
          </div>
          <div>
            <select id="prod-category-filter" onchange="applyProdFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-500 transition">
              <option value="ALL">Tất cả Ngành Hàng</option>
            </select>
          </div>
          <div>
            <select id="prod-abc-filter" onchange="applyProdFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-500 transition">
              <option value="ALL">Tất cả Hạng ABC</option>
              <option value="A">Hạng A - Trụ cột (194 SKU)</option>
              <option value="B">Hạng B - Tiềm năng (319 SKU)</option>
              <option value="C">Hạng C - Chậm luân chuyển (713 SKU)</option>
            </select>
          </div>
        </div>

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
            <tbody id="product-master-tbody" class="divide-y divide-slate-100"></tbody>
          </table>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100 text-xs">
          <div class="text-slate-500" id="prod-pagination-info">Hiển thị 1 - 30 trong số 1,226 sản phẩm</div>
          <div class="flex items-center gap-1.5" id="prod-pagination-buttons"></div>
        </div>
      </div>
    </div>

    <!-- ================= TAB 4: REORDER FORECASTING (NEW & EXPANDED!) ================= -->
    <div id="section-forecast" class="tab-section hidden space-y-6">
      
      <!-- Prediction Alert Banner -->
      <div class="bg-gradient-to-r from-amber-500 via-orange-500 to-red-600 rounded-2xl p-0.5 shadow-md">
        <div class="bg-white rounded-[14px] p-5">
          <div class="flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3.5">
              <div class="w-12 h-12 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center text-2xl font-black shrink-0">
                ⚡
              </div>
              <div>
                <h3 class="text-base font-black text-slate-900">Mô Hình AI Dự Báo Khách Hàng Sắp Hết Hàng & Chu Kỳ Lên Đơn Gối Đầu</h3>
                <p class="text-xs text-slate-600">Tính toán dựa trên tần suất và khoảng cách ngày giữa các lần nhập hàng lịch sử. Giúp Sales chủ động chốt đơn trước khi đại lý cạn kho!</p>
              </div>
            </div>
            <div class="flex items-center gap-2 flex-wrap">
              <span class="bg-amber-100 text-amber-900 text-xs font-black px-3 py-1.5 rounded-lg border border-amber-300 flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-amber-500 pulse-dot"></span>
                <span>53 Đại Lý Sắp Hết Hàng Trong Tuần (15.2 Tỷ)</span>
              </span>
              <span class="bg-red-100 text-red-900 text-xs font-black px-3 py-1.5 rounded-lg border border-red-300">
                195 Đại Lý Đã Quá Hạn Chu Kỳ
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Forecast KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <!-- RUNNING_LOW -->
        <div class="bg-gradient-to-br from-amber-50 to-orange-50 rounded-2xl p-4 border-2 border-amber-300 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <span class="text-[11px] font-black uppercase text-amber-800 tracking-wider">Cần Gọi Chốt Đơn Ngay</span>
              <span class="w-2.5 h-2.5 rounded-full bg-amber-500 pulse-dot"></span>
            </div>
            <div class="text-2xl font-black text-amber-950 font-mono">53 Đại Lý</div>
            <div class="text-xs text-amber-800 font-medium mt-1">Dự kiến cạn hàng trong <strong>1 - 5 ngày</strong> tới</div>
          </div>
          <div class="mt-3 pt-2.5 border-t border-amber-200/80 text-[11px] text-amber-900 font-bold flex justify-between items-center">
            <span>Doanh thu nhóm:</span>
            <span class="font-mono text-xs">15.2+ Tỷ VNĐ</span>
          </div>
        </div>

        <!-- OVERDUE -->
        <div class="bg-gradient-to-br from-red-50 to-rose-50 rounded-2xl p-4 border-2 border-red-300 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <span class="text-[11px] font-black uppercase text-red-800 tracking-wider">Đã Quá Hạn Chu Kỳ</span>
              <span class="text-xs">⚠️</span>
            </div>
            <div class="text-2xl font-black text-red-950 font-mono">195 Đại Lý</div>
            <div class="text-xs text-red-800 font-medium mt-1">Đã quá chu kỳ quen thuộc, nguy cơ mất khách</div>
          </div>
          <div class="mt-3 pt-2.5 border-t border-red-200/80 text-[11px] text-red-900 font-bold flex justify-between items-center">
            <span>Doanh thu nhóm:</span>
            <span class="font-mono text-xs">14.8 Tỷ VNĐ</span>
          </div>
        </div>

        <!-- UPCOMING -->
        <div class="bg-gradient-to-br from-yellow-50 to-amber-50 rounded-2xl p-4 border border-yellow-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <span class="text-[11px] font-bold uppercase text-yellow-800 tracking-wider">Sắp Đến Chu Kỳ</span>
              <span class="text-xs">🟡</span>
            </div>
            <div class="text-2xl font-black text-yellow-950 font-mono">53 Đại Lý</div>
            <div class="text-xs text-yellow-800 font-medium mt-1">Dự kiến lên đơn trong <strong>7 - 15 ngày</strong> tới</div>
          </div>
          <div class="mt-3 pt-2.5 border-t border-yellow-200/80 text-[11px] text-yellow-900 font-bold flex justify-between items-center">
            <span>Chuẩn bị chương trình:</span>
            <span>Gửi báo giá mới</span>
          </div>
        </div>

        <!-- SAFE -->
        <div class="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl p-4 border border-emerald-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <span class="text-[11px] font-bold uppercase text-emerald-800 tracking-wider">Tồn Kho Đang An Toàn</span>
              <span class="text-xs">🟢</span>
            </div>
            <div class="text-2xl font-black text-emerald-950 font-mono">92 Đại Lý</div>
            <div class="text-xs text-emerald-800 font-medium mt-1">Mới nhập hàng gần đây, kho đại lý còn nhiều</div>
          </div>
          <div class="mt-3 pt-2.5 border-t border-emerald-200/80 text-[11px] text-emerald-900 font-bold flex justify-between items-center">
            <span>Trạng thái:</span>
            <span>Chăm sóc sau bán</span>
          </div>
        </div>

      </div>

      <!-- Forecast Charts Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Top Running Low Customers Bar Chart -->
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>🚨</span> Top 10 Khách Hàng VIP Sắp Hết Hàng Cần Lên Đơn Gấp
            </h3>
            <p class="text-xs text-slate-500">NPP Châu Loan (chu kỳ 1.7 ngày), Nguyễn Hoàng Phú (chu kỳ 3.2 ngày), NPP Trường Giang (2.3 ngày)...</p>
          </div>
          <div class="relative h-80 w-full">
            <canvas id="forecastTopBarChart"></canvas>
          </div>
        </div>

        <!-- Sales Rep Task Breakdown -->
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div class="mb-4">
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>📞</span> Phân Bổ Cuộc Gọi Hôm Nay Theo Nhân Viên Kinh Doanh
            </h3>
            <p class="text-xs text-slate-500">Số lượng đại lý đang chạm ngưỡng cạn hàng được phân công cho từng nhân sự phụ trách</p>
          </div>
          <div class="relative h-80 w-full">
            <canvas id="forecastSalesChart"></canvas>
          </div>
        </div>

      </div>

      <!-- REORDER CALL SHEET TABLE (SMART DISPATCH) -->
      <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-4">
        
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h3 class="font-black text-slate-900 text-base flex items-center gap-2">
              <span>📋</span> Bảng Phân Bổ Cuộc Gọi Bán Hàng & Chốt Đơn Gối Đầu Hôm Nay
            </h3>
            <p class="text-xs text-slate-500">Được sắp xếp tự động theo mức độ khẩn cấp (Urgency) và quy mô doanh thu đại lý</p>
          </div>
          <div class="flex items-center gap-2">
            <span id="forecast-count-badge" class="bg-amber-100 text-amber-900 font-extrabold text-xs px-2.5 py-1 rounded-full border border-amber-300">Đang hiển thị: 393 Đại lý</span>
            <button onclick="exportForecastCSV()" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs px-3 py-1.5 rounded-xl transition flex items-center gap-1 shadow-xs">
              <span>📥</span> Xuất Call Sheet CSV
            </button>
          </div>
        </div>

        <!-- Filter Bar for Forecast -->
        <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
          <!-- Search -->
          <div class="relative sm:col-span-2">
            <input type="text" id="forecast-search-input" oninput="applyForecastFilters()" placeholder="Tìm tên đại lý, số điện thoại, mã KH..." class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 pl-8 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500 transition">
            <span class="absolute left-2.5 top-2.5 text-slate-400 text-xs">🔎</span>
          </div>

          <!-- Status Filter -->
          <div>
            <select id="forecast-status-filter" onchange="applyForecastFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500 transition">
              <option value="ALL">Tất cả Trạng Thái Chu Kỳ</option>
              <option value="RUNNING_LOW" selected>⚡ Sắp Hết Hàng (Cần Gọi Ngay - 53 KH)</option>
              <option value="OVERDUE">🔴 Đã Quá Hạn Chu Kỳ (195 KH)</option>
              <option value="UPCOMING">🟡 Sắp Đến Chu Kỳ (53 KH)</option>
              <option value="SAFE">🟢 Tồn Kho An Toàn (92 KH)</option>
            </select>
          </div>

          <!-- Sales Rep Filter -->
          <div>
            <select id="forecast-sales-filter" onchange="applyForecastFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500 transition">
              <option value="ALL">Tất cả Nhân Viên Sales</option>
            </select>
          </div>
        </div>

        <!-- Forecast Table -->
        <div class="overflow-x-auto border border-slate-200 rounded-xl">
          <table class="w-full text-left text-xs whitespace-nowrap">
            <thead class="bg-slate-100 text-slate-700 font-extrabold border-b border-slate-200 select-none">
              <tr>
                <th class="py-3 px-3">Mức Độ Khẩn Cấp</th>
                <th class="py-3 px-3 cursor-pointer hover:bg-slate-200 transition" onclick="sortForecastTable('name')">Đại Lý / Khách Hàng ⇕</th>
                <th class="py-3 px-3">Số Điện Thoại</th>
                <th class="py-3 px-3 cursor-pointer hover:bg-slate-200 transition" onclick="sortForecastTable('main_sales_rep')">Sales Phụ Trách ⇕</th>
                <th class="py-3 px-3 text-right cursor-pointer hover:bg-slate-200 transition" onclick="sortForecastTable('net')">Doanh Thu Thuần ⇕</th>
                <th class="py-3 px-3 text-center cursor-pointer hover:bg-slate-200 transition" onclick="sortForecastTable('avg_cycle')">Chu Kỳ Đặt TB ⇕</th>
                <th class="py-3 px-3 text-center cursor-pointer hover:bg-slate-200 transition" onclick="sortForecastTable('r_days')">Đã Qua ⇕</th>
                <th class="py-3 px-3 text-center">Tiêu Hao Tồn Kho</th>
                <th class="py-3 px-3 text-center cursor-pointer hover:bg-slate-200 transition" onclick="sortForecastTable('predicted_date')">Dự Kiến Hết Hàng ⇕</th>
                <th class="py-3 px-3">Gợi Ý Mặt Hàng Cần Chào</th>
                <th class="py-3 px-3 text-center">Hành Động</th>
              </tr>
            </thead>
            <tbody id="forecast-table-tbody" class="divide-y divide-slate-100"></tbody>
          </table>
        </div>

        <!-- Pagination for Forecast -->
        <div class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100 text-xs">
          <div class="text-slate-500" id="forecast-pagination-info">Hiển thị 1 - 30 trong số các đại lý</div>
          <div class="flex items-center gap-1.5" id="forecast-pagination-buttons"></div>
        </div>

      </div>

    </div>

    <!-- ================= TAB 5: CUSTOMER MASTER 360 ================= -->
    <div id="section-customers" class="tab-section hidden space-y-4">
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
          <div class="relative">
            <input type="text" id="search-input" oninput="applyFilters()" placeholder="Tìm tên KH, mã KH, SĐT..." class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 pl-8 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
            <span class="absolute left-2.5 top-2.5 text-slate-400 text-xs">🔎</span>
          </div>
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
          <div>
            <select id="filter-abc" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
              <option value="ALL">Tất cả Hạng ABC (Pareto)</option>
              <option value="A">Hạng A - Top 80% Doanh thu (42)</option>
              <option value="B">Hạng B - 15% Tiếp theo (80)</option>
              <option value="C">Hạng C - 5% Cuối (271)</option>
            </select>
          </div>
          <div>
            <select id="filter-province" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
              <option value="ALL">Tất cả Tỉnh / Thành phố</option>
            </select>
          </div>
          <div>
            <select id="filter-sales-rep" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
              <option value="ALL">Tất cả Nhân Viên Sales</option>
            </select>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
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
            <tbody id="master-table-tbody" class="divide-y divide-slate-100"></tbody>
          </table>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-3 mt-4 pt-3 border-t border-slate-100 text-xs">
          <div class="text-slate-500" id="pagination-info">Hiển thị 1 - 30 trong số 393 khách hàng</div>
          <div class="flex items-center gap-1.5" id="pagination-buttons"></div>
        </div>
      </div>
    </div>

    <!-- ================= TAB 6: STRATEGIC ACTION MATRIX ================= -->
    <div id="section-strategy" class="tab-section hidden space-y-6">
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
              <span class="bg-amber-100 text-amber-900 text-xs font-black px-3 py-1 rounded-lg">53 KH Sắp Hết Hàng (15.2 Tỷ)</span>
              <span class="bg-blue-100 text-blue-800 text-xs font-black px-3 py-1 rounded-lg">194 SKU Hạng A Trọng Yếu (78.9 Tỷ)</span>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white rounded-2xl p-5 border-2 border-amber-200 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="bg-amber-500 text-slate-950 text-[11px] font-black px-2.5 py-1 rounded-lg uppercase tracking-wider">Hành Động Chốt Đơn #1</span>
              <span class="text-xs font-bold text-amber-700 font-mono">53 Khách • 15.2 Tỷ</span>
            </div>
            <h4 class="font-black text-slate-900 text-sm mb-1.5 flex items-center gap-2">
              <span>⚡</span> Gọi Chăm Sóc Ngay Cho 53 Đại Lý Sắp Cạn Tồn Kho
            </h4>
            <p class="text-xs text-slate-600 leading-relaxed mb-4">
              Đây là các đại lý đang chạm hoặc vượt nhẹ chu kỳ đặt hàng trung bình. Họ đang có nhu cầu bổ sung hàng thật sự, tỷ lệ chốt đơn thành công khi gọi lúc này là trên 85%.
            </p>
          </div>
          <button onclick="switchTab('forecast')" class="w-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs py-2.5 rounded-xl transition shadow">
            Mở Danh Sách 53 Đại Lý Cần Gọi Hôm Nay →
          </button>
        </div>

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
          </div>
          <button onclick="switchTab('products')" class="w-full bg-blue-700 hover:bg-blue-600 text-white font-bold text-xs py-2.5 rounded-xl transition shadow">
            Xem 194 Mã Sản Phẩm Hạng A Chủ Lực →
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
          <div class="w-12 h-12 rounded-2xl bg-amber-400 text-slate-950 flex items-center justify-center font-black text-xl shadow">🏢</div>
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
        <button onclick="closeCustomerModal()" class="text-white/70 hover:text-white text-2xl font-black p-1 transition">✕</button>
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
          <div><span class="text-slate-400 font-medium block">Số điện thoại:</span><span id="modal-cust-phone" class="font-bold text-slate-800 font-mono text-xs">--</span></div>
          <div><span class="text-slate-400 font-medium block">Tỉnh / Thành phố:</span><span id="modal-cust-province" class="font-bold text-slate-800 text-xs">--</span></div>
          <div><span class="text-slate-400 font-medium block">Sales phụ trách:</span><span id="modal-cust-sales" class="font-black text-blue-700 text-xs">--</span></div>
        </div>

        <div>
          <h4 class="font-black text-slate-900 text-xs uppercase tracking-wider mb-2.5 flex items-center gap-1.5"><span>📦</span> Các Nhóm Ngành Hàng Đại Lý Tiêu Thụ Nhiều Nhất</h4>
          <div id="modal-cust-categories" class="space-y-2"></div>
        </div>

        <div>
          <h4 class="font-black text-slate-900 text-xs uppercase tracking-wider mb-2.5 flex items-center gap-1.5"><span>🏷️</span> Top 5 Sản Phẩm Đại Lý Mua Nhiều Nhất</h4>
          <div class="border border-slate-200 rounded-xl overflow-hidden">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-100 font-bold text-slate-600"><tr><th class="py-2 px-3">Tên Sản Phẩm</th><th class="py-2 px-3 text-right">Số Lượng</th><th class="py-2 px-3 text-right">Doanh Số Gộp</th></tr></thead>
              <tbody id="modal-cust-products" class="divide-y divide-slate-100"></tbody>
            </table>
          </div>
        </div>

        <div class="bg-blue-50 border border-blue-200 rounded-2xl p-4">
          <div class="font-black text-blue-900 text-xs flex items-center gap-1.5 mb-1"><span>💡</span> Khuyến Nghị Hành Động Chăm Sóc Cho Đại Lý Này:</div>
          <p id="modal-cust-action" class="text-xs text-blue-800 leading-relaxed font-medium">--</p>
        </div>
      </div>

      <div class="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
        <span class="text-[11px] text-slate-400">KingBlue Customer Intelligence 360°</span>
        <button onclick="closeCustomerModal()" class="bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs px-4 py-2 rounded-xl transition">Đóng</button>
      </div>
    </div>
  </div>

  <!-- ================= PRODUCT 360 MODAL ================= -->
  <div id="product-modal" class="fixed inset-0 bg-slate-950/60 backdrop-blur-xs z-50 hidden flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
    <div class="bg-white rounded-3xl max-w-3xl w-full shadow-2xl border border-slate-200 overflow-hidden my-auto max-h-[90vh] flex flex-col">
      <div class="bg-gradient-to-r from-teal-900 to-slate-900 text-white p-5 border-b-4 border-amber-400 flex items-start justify-between">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-2xl bg-teal-500 text-white flex items-center justify-center font-black text-xl shadow">📦</div>
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
        <button onclick="closeProductModal()" class="text-white/70 hover:text-white text-2xl font-black p-1 transition">✕</button>
      </div>

      <div class="p-6 overflow-y-auto custom-scrollbar space-y-6 flex-1 text-xs">
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

        <div>
          <h4 class="font-black text-slate-900 text-xs uppercase tracking-wider mb-2.5 flex items-center gap-1.5"><span>📈</span> Xu Hướng Doanh Số 9 Tháng (T1 - T9/2026)</h4>
          <div class="relative h-44 w-full bg-slate-50 p-3 rounded-2xl border border-slate-200">
            <canvas id="modalProdMonthlyChart"></canvas>
          </div>
        </div>

        <div>
          <h4 class="font-black text-slate-900 text-xs uppercase tracking-wider mb-2.5 flex items-center gap-1.5"><span>🏢</span> Top 5 Đại Lý Tiêu Thụ Nhiều Nhất</h4>
          <div class="border border-slate-200 rounded-xl overflow-hidden">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-100 font-bold text-slate-600"><tr><th class="py-2 px-3">Tên Đại Lý</th><th class="py-2 px-3 text-right">Tổng Tiền Mua</th><th class="py-2 px-3 text-center">Thao Tác</th></tr></thead>
              <tbody id="modal-prod-customers" class="divide-y divide-slate-100"></tbody>
            </table>
          </div>
        </div>

        <div class="bg-teal-50 border border-teal-200 rounded-2xl p-4">
          <div class="font-black text-teal-900 text-xs flex items-center gap-1.5 mb-1"><span>💡</span> Khuyến Nghị Chiến Lược Cho Mã Sản Phẩm Này:</div>
          <p id="modal-prod-action" class="text-xs text-teal-800 leading-relaxed font-medium">--</p>
        </div>
      </div>

      <div class="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
        <span class="text-[11px] text-slate-400">KingBlue Product Intelligence 360°</span>
        <button onclick="closeProductModal()" class="bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs px-4 py-2 rounded-xl transition">Đóng</button>
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

    let allPredictions = RAW_DATA.predictions || [];
    let filteredPredictions = [...allPredictions];
    let forecastCurrentPage = 1;
    let forecastPageSize = 30;
    let forecastSort = {{ col: 'score', asc: false }};

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

    window.addEventListener('DOMContentLoaded', () => {{
      populateFilterDropdowns();
      initCharts();
      renderTopCustomers();
      renderSalesDetail();
      renderProvinceDetail();
      renderMasterTable();
      renderProductMasterTable();
      renderForecastTable();
      applyForecastFilters(); // default to RUNNING_LOW
    }});

    function populateFilterDropdowns() {{
      const provSelect = document.getElementById('filter-province');
      RAW_DATA.provinces.forEach(p => {{
        const opt = document.createElement('option');
        opt.value = p.province;
        opt.textContent = `${{p.province}} (${{p.customers}} KH - ${{fmtVND(p.net)}})`;
        provSelect.appendChild(opt);
      }});

      const salesSelect = document.getElementById('filter-sales-rep');
      const forecastSalesSelect = document.getElementById('forecast-sales-filter');
      RAW_DATA.sales_reps.forEach(s => {{
        const opt = document.createElement('option');
        opt.value = s.name;
        opt.textContent = `${{s.name}} (${{s.customers}} KH - ${{fmtVND(s.net)}})`;
        salesSelect.appendChild(opt);

        const opt2 = document.createElement('option');
        opt2.value = s.name;
        opt2.textContent = s.name;
        forecastSalesSelect.appendChild(opt2);
      }});

      const catSelect = document.getElementById('prod-category-filter');
      RAW_DATA.categories.forEach(c => {{
        const opt = document.createElement('option');
        opt.value = c.name;
        opt.textContent = `${{c.name}} (${{c.skus_count}} SKU - ${{fmtVND(c.gross)}})`;
        catSelect.appendChild(opt);
      }});
    }}

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

    // ================= REORDER FORECASTING LOGIC (NEW!) =================
    function applyForecastFilters() {{
      const search = document.getElementById('forecast-search-input').value.toLowerCase().trim();
      const status = document.getElementById('forecast-status-filter').value;
      const sales = document.getElementById('forecast-sales-filter').value;

      filteredPredictions = allPredictions.filter(p => {{
        if (search) {{
          const match = p.name.toLowerCase().includes(search) || p.id.toLowerCase().includes(search) || (p.phone && p.phone.includes(search));
          if (!match) return false;
        }}
        if (status !== 'ALL' && p.status !== status) return false;
        if (sales !== 'ALL' && p.main_sales_rep !== sales) return false;
        return true;
      }});

      sortForecastData();
      forecastCurrentPage = 1;
      renderForecastTable();
      document.getElementById('forecast-count-badge').textContent = `Đang hiển thị: ${{filteredPredictions.length}} / ${{allPredictions.length}} Đại lý`;
    }}

    function sortForecastTable(col) {{
      if (forecastSort.col === col) {{
        forecastSort.asc = !forecastSort.asc;
      }} else {{
        forecastSort.col = col;
        forecastSort.asc = (col === 'name' || col === 'main_sales_rep') ? true : false;
      }}
      sortForecastData();
      renderForecastTable();
    }}

    function sortForecastData() {{
      filteredPredictions.sort((a, b) => {{
        let valA = a[forecastSort.col];
        let valB = b[forecastSort.col];
        if (typeof valA === 'string') valA = valA.toLowerCase();
        if (typeof valB === 'string') valB = valB.toLowerCase();
        if (valA < valB) return forecastSort.asc ? -1 : 1;
        if (valA > valB) return forecastSort.asc ? 1 : -1;
        return 0;
      }});
    }}

    function renderForecastTable() {{
      const tbody = document.getElementById('forecast-table-tbody');
      tbody.innerHTML = '';

      const start = (forecastCurrentPage - 1) * forecastPageSize;
      const end = Math.min(start + forecastPageSize, filteredPredictions.length);
      const pageData = filteredPredictions.slice(start, end);

      if (pageData.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="11" class="text-center py-8 text-slate-400">Không tìm thấy đại lý nào phù hợp với bộ lọc chu kỳ</td></tr>`;
        document.getElementById('forecast-pagination-info').textContent = '0 đại lý';
        document.getElementById('forecast-pagination-buttons').innerHTML = '';
        return;
      }}

      pageData.forEach(p => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-amber-50/40 transition cursor-pointer';
        tr.onclick = (e) => {{ if (e.target.tagName !== 'BUTTON' && e.target.tagName !== 'A') openCustomerModal(p.id); }};

        // Status badge
        let statusBadge = '';
        if (p.status === 'RUNNING_LOW') {{
          statusBadge = `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-black bg-amber-100 text-amber-900 border border-amber-300"><span class="w-2 h-2 rounded-full bg-amber-500 pulse-dot"></span>Sắp Hết Hàng (Gọi Ngay)</span>`;
        }} else if (p.status === 'OVERDUE') {{
          statusBadge = `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-black bg-red-100 text-red-900 border border-red-300">🔴 Quá Hạn Chu Kỳ</span>`;
        }} else if (p.status === 'UPCOMING') {{
          statusBadge = `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-bold bg-yellow-100 text-yellow-900 border border-yellow-200">🟡 Sắp Đến Đợt</span>`;
        }} else {{
          statusBadge = `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-900 border border-emerald-200">🟢 Tồn Kho An Toàn</span>`;
        }}

        // Progress bar for depletion
        const depPct = Math.min(100, p.depletion_pct);
        let barColor = '#10b981';
        if (p.depletion_pct >= 120) barColor = '#ef4444';
        else if (p.depletion_pct >= 80) barColor = '#f97316';
        else if (p.depletion_pct >= 50) barColor = '#eab308';

        // Products pills
        const prodPills = p.top_products.slice(0, 2).map(name => `<span class="inline-block bg-slate-100 text-slate-700 text-[10px] px-1.5 py-0.5 rounded mr-1 truncate max-w-[140px]" title="${{name}}">${{name}}</span>`).join('') || '<span class="text-slate-400 text-[10px]">--</span>';

        tr.innerHTML = `
          <td class="py-2.5 px-3">${{statusBadge}}</td>
          <td class="py-2.5 px-3 font-black text-slate-900">
            <div class="truncate max-w-[210px]" title="${{p.name}}">${{p.name}}</div>
            <div class="text-[10px] text-slate-400 font-mono">${{p.id}} • ${{p.province}}</div>
          </td>
          <td class="py-2.5 px-3 font-mono text-slate-700">
            ${{p.phone ? `<a href="tel:${{p.phone}}" onclick="event.stopPropagation()" class="text-blue-600 hover:underline font-bold">📞 ${{p.phone}}</a>` : '<span class="text-slate-300">Chưa có SĐT</span>'}}
          </td>
          <td class="py-2.5 px-3 text-slate-700 font-medium">${{p.main_sales_rep}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-black text-blue-900">${{fmtFullVND(p.net)}}</td>
          <td class="py-2.5 px-3 text-center font-mono font-bold text-slate-700">${{p.avg_cycle}} ngày</td>
          <td class="py-2.5 px-3 text-center font-mono font-bold text-slate-600">${{p.r_days}} ngày</td>
          <td class="py-2.5 px-3 text-center w-28">
            <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
              <div class="h-full rounded-full" style="width: ${{depPct}}%; background-color: ${{barColor}};"></div>
            </div>
            <span class="text-[10px] font-mono font-bold text-slate-500">${{p.depletion_pct}}%</span>
          </td>
          <td class="py-2.5 px-3 text-center font-mono">
            <div class="font-bold text-slate-800">${{p.predicted_date}}</div>
            <div class="text-[10px] ${{p.days_left <= 0 ? 'text-red-600 font-black' : 'text-amber-700 font-bold'}}">
              ${{p.days_left <= 0 ? `Quá ${{Math.abs(p.days_left)}} ngày` : `Còn ${{p.days_left}} ngày`}}
            </div>
          </td>
          <td class="py-2.5 px-3">${{prodPills}}</td>
          <td class="py-2.5 px-3 text-center">
            <button onclick="event.stopPropagation(); openCustomerModal('${{p.id}}')" class="bg-amber-100 hover:bg-amber-200 text-amber-900 font-extrabold text-[11px] px-2.5 py-1 rounded-lg transition shadow-xs">
              Chi Tiết 🔍
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      document.getElementById('forecast-pagination-info').textContent = `Hiển thị ${{start + 1}} - ${{end}} trong số ${{filteredPredictions.length}} đại lý`;
      renderForecastPaginationButtons();
    }}

    function renderForecastPaginationButtons() {{
      const container = document.getElementById('forecast-pagination-buttons');
      container.innerHTML = '';
      const totalPages = Math.ceil(filteredPredictions.length / forecastPageSize) || 1;
      if (totalPages <= 1) return;

      const prevBtn = document.createElement('button');
      prevBtn.className = `px-2 py-1 rounded border text-xs font-bold ${{forecastCurrentPage === 1 ? 'opacity-40 cursor-not-allowed border-slate-200' : 'hover:bg-slate-100 border-slate-300'}}`;
      prevBtn.textContent = '◀';
      prevBtn.disabled = forecastCurrentPage === 1;
      prevBtn.onclick = () => {{ if (forecastCurrentPage > 1) {{ forecastCurrentPage--; renderForecastTable(); }} }};
      container.appendChild(prevBtn);

      let startP = Math.max(1, forecastCurrentPage - 2);
      let endP = Math.min(totalPages, startP + 4);
      if (endP - startP < 4) startP = Math.max(1, endP - 4);

      for (let p = startP; p <= endP; p++) {{
        const btn = document.createElement('button');
        btn.className = `px-2.5 py-1 rounded text-xs font-bold ${{p === forecastCurrentPage ? 'bg-amber-500 text-slate-950 font-black' : 'hover:bg-slate-100 border border-slate-200 text-slate-700'}}`;
        btn.textContent = p;
        btn.onclick = () => {{ forecastCurrentPage = p; renderForecastTable(); }};
        container.appendChild(btn);
      }}

      const nextBtn = document.createElement('button');
      nextBtn.className = `px-2 py-1 rounded border text-xs font-bold ${{forecastCurrentPage === totalPages ? 'opacity-40 cursor-not-allowed border-slate-200' : 'hover:bg-slate-100 border-slate-300'}}`;
      nextBtn.textContent = '▶';
      nextBtn.disabled = forecastCurrentPage === totalPages;
      nextBtn.onclick = () => {{ if (forecastCurrentPage < totalPages) {{ forecastCurrentPage++; renderForecastTable(); }} }};
      container.appendChild(nextBtn);
    }}

    function exportForecastCSV() {{
      let csvContent = "\\uFEFFMã KH,Tên Đại Lý,SĐT,Tỉnh Thành,Sales Phụ Trách,Doanh Thu Thuần,Chu Kỳ Đặt TB (Ngày),Đã Qua (Ngày),Dự Kiến Hết Hàng,Trạng Thái,Mức Độ Khẩn Cấp,Sản Phẩm Hay Mua\\n";
      filteredPredictions.forEach(p => {{
        const prods = (p.top_products || []).join(" | ").replace(/"/g, '""');
        const row = [
          `"${{p.id}}"`,
          `"${{p.name.replace(/"/g, '""')}}"`,
          `"${{p.phone || ''}}"`,
          `"${{p.province}}"`,
          `"${{p.main_sales_rep}}"`,
          p.net,
          p.avg_cycle,
          p.r_days,
          `"${{p.predicted_date}}"`,
          `"${{p.status_label}}"`,
          `"${{p.urgency}}"`,
          `"${{prods}}"`
        ];
        csvContent += row.join(",") + "\\n";
      }});
      downloadFile(csvContent, `KingBlue_Danh_Sach_Dai_Ly_Sap_Het_Hang_${{new Date().toISOString().slice(0, 10)}}.csv`);
    }}

    // ================= CUSTOMER MASTER & PRODUCT MASTER LOGIC =================
    function applyFilters() {{
      const search = document.getElementById('search-input').value.toLowerCase().trim();
      const seg = document.getElementById('filter-segment').value;
      const abc = document.getElementById('filter-abc').value;
      const prov = document.getElementById('filter-province').value;
      const sales = document.getElementById('filter-sales-rep').value;

      filteredCustomers = allCustomers.filter(c => {{
        if (search) {{
          const matchSearch = c.name.toLowerCase().includes(search) || c.id.toLowerCase().includes(search) || (c.phone && c.phone.includes(search)) || c.province.toLowerCase().includes(search);
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
      if (custSort.col === col) {{ custSort.asc = !custSort.asc; }}
      else {{ custSort.col = col; custSort.asc = (col === 'name' || col === 'id' || col === 'province') ? true : false; }}
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

    // Product Functions
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
      if (prodSort.col === col) {{ prodSort.asc = !prodSort.asc; }}
      else {{ prodSort.col = col; prodSort.asc = (col === 'code' || col === 'name' || col === 'category') ? true : false; }}
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
          responsive: true, maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ y: {{ grid: {{ color: '#f1f5f9' }} }} }}
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

    // Customer Preview & Details
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

    // Charts Init
    function initCharts() {{
      // Monthly Chart
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

      // ABC Donut
      const ctxAbc = document.getElementById('abcChart').getContext('2d');
      new Chart(ctxAbc, {{
        type: 'doughnut',
        data: {{
          labels: ['Hạng A (80% DT)', 'Hạng B (15% DT)', 'Hạng C (5% DT)'],
          datasets: [{{ data: [RAW_DATA.abc.find(a => a.tier === 'A').net / 1e9, RAW_DATA.abc.find(a => a.tier === 'B').net / 1e9, RAW_DATA.abc.find(a => a.tier === 'C').net / 1e9], backgroundColor: ['#2563eb', '#0ea5e9', '#cbd5e1'], borderWidth: 3, borderColor: '#ffffff' }}]
        }},
        options: {{ responsive: true, maintainAspectRatio: false, cutout: '68%' }}
      }});

      // RFM Chart
      const ctxRfm = document.getElementById('rfmChart').getContext('2d');
      new Chart(ctxRfm, {{
        type: 'bar',
        data: {{
          labels: RAW_DATA.segments.map(s => s.name.split('/')[0].trim()),
          datasets: [{{ label: 'Doanh thu thuần (Tỷ VNĐ)', data: RAW_DATA.segments.map(s => s.net / 1e9), backgroundColor: RAW_DATA.segments.map(s => s.color), borderRadius: 6 }}]
        }},
        options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
      }});

      // Categories Chart
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

      // Province Chart
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

      // Sales Chart
      const ctxSales = document.getElementById('salesChart').getContext('2d');
      new Chart(ctxSales, {{
        type: 'bar',
        data: {{
          labels: RAW_DATA.sales_reps.map(s => s.name),
          datasets: [{{ label: 'Doanh thu thuần (Tỷ VNĐ)', data: RAW_DATA.sales_reps.map(s => s.net / 1e9), backgroundColor: '#059669', borderRadius: 6 }}]
        }},
        options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
      }});

      // Product Top Revenue Chart
      const ctxProdRev = document.getElementById('prodTopRevChart').getContext('2d');
      const top10ProdRev = allProducts.slice(0, 10);
      new Chart(ctxProdRev, {{
        type: 'bar',
        data: {{
          labels: top10ProdRev.map(p => p.name.length > 25 ? p.name.slice(0, 25) + '...' : p.name),
          datasets: [{{ label: 'Doanh số gộp (Tỷ VNĐ)', data: top10ProdRev.map(p => p.gross / 1e9), backgroundColor: '#0d9488', borderRadius: 6 }}]
        }},
        options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
      }});

      // Product Top Quantity Chart
      const ctxProdQty = document.getElementById('prodTopQtyChart').getContext('2d');
      const top10ProdQty = [...allProducts].sort((a, b) => b.qty - a.qty).slice(0, 10);
      new Chart(ctxProdQty, {{
        type: 'bar',
        data: {{
          labels: top10ProdQty.map(p => p.name.length > 25 ? p.name.slice(0, 25) + '...' : p.name),
          datasets: [{{ label: 'Sản lượng (Nghìn cái)', data: top10ProdQty.map(p => p.qty / 1e3), backgroundColor: '#0284c7', borderRadius: 6 }}]
        }},
        options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
      }});

      // Product ABC Donut
      const ctxProdAbc = document.getElementById('prodAbcChart').getContext('2d');
      new Chart(ctxProdAbc, {{
        type: 'doughnut',
        data: {{
          labels: ['Hạng A (194 SKU - 80%)', 'Hạng B (319 SKU - 15%)', 'Hạng C (713 SKU - 5%)'],
          datasets: [{{ data: RAW_DATA.product_abc.map(a => a.gross / 1e9), backgroundColor: ['#2563eb', '#0ea5e9', '#cbd5e1'], borderWidth: 3, borderColor: '#ffffff' }}]
        }},
        options: {{ responsive: true, maintainAspectRatio: false, cutout: '68%' }}
      }});

      // Product Categories SKU & Revenue
      const ctxProdCat = document.getElementById('prodCategoryChart').getContext('2d');
      new Chart(ctxProdCat, {{
        type: 'bar',
        data: {{
          labels: RAW_DATA.categories.slice(0, 8).map(c => c.name),
          datasets: [
            {{ type: 'bar', label: 'Doanh số gộp (Tỷ VNĐ)', data: RAW_DATA.categories.slice(0, 8).map(c => c.gross / 1e9), backgroundColor: '#3b82f6', borderRadius: 6, yAxisID: 'yGross' }},
            {{ type: 'line', label: 'Số lượng SKU', data: RAW_DATA.categories.slice(0, 8).map(c => c.skus_count), borderColor: '#f59e0b', backgroundColor: '#f59e0b', borderWidth: 2, tension: 0.3, pointRadius: 4, yAxisID: 'ySkus' }}
          ]
        }},
        options: {{
          responsive: true, maintainAspectRatio: false,
          scales: {{
            yGross: {{ type: 'linear', position: 'left', grid: {{ color: '#f1f5f9' }} }},
            ySkus: {{ type: 'linear', position: 'right', grid: {{ drawOnChartArea: false }} }}
          }}
        }}
      }});

      // FORECAST CHARTS (NEW!)
      // Top 10 Running Low Customers Bar Chart
      const ctxForecastBar = document.getElementById('forecastTopBarChart').getContext('2d');
      const runningLowTop10 = allPredictions.filter(p => p.status === 'RUNNING_LOW').slice(0, 10);
      new Chart(ctxForecastBar, {{
        type: 'bar',
        data: {{
          labels: runningLowTop10.map(p => p.name.length > 22 ? p.name.slice(0, 22) + '...' : p.name),
          datasets: [{{
            label: 'Doanh thu thuần (Tỷ VNĐ)',
            data: runningLowTop10.map(p => p.net / 1e9),
            backgroundColor: '#f97316',
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
                title: function(ctx) {{ return runningLowTop10[ctx[0].dataIndex].name; }},
                label: function(ctx) {{
                  const p = runningLowTop10[ctx.dataIndex];
                  return `${{ctx.raw.toFixed(2)}} Tỷ | Chu kỳ: ${{p.avg_cycle}} ngày | Đã qua: ${{p.r_days}} ngày (${{p.days_left <= 0 ? 'Quá hạn ' + Math.abs(p.days_left) + ' ngày' : 'Còn ' + p.days_left + ' ngày'}})`;
                }}
              }}
            }}
          }}
        }}
      }});

      // Forecast Tasks per Sales Rep
      const ctxForecastSales = document.getElementById('forecastSalesChart').getContext('2d');
      const salesTaskCounts = {{}};
      allPredictions.filter(p => p.status === 'RUNNING_LOW').forEach(p => {{
        salesTaskCounts[p.main_sales_rep] = (salesTaskCounts[p.main_sales_rep] || 0) + 1;
      }});
      const salesLabels = Object.keys(salesTaskCounts).sort((a,b) => salesTaskCounts[b] - salesTaskCounts[a]);

      new Chart(ctxForecastSales, {{
        type: 'bar',
        data: {{
          labels: salesLabels,
          datasets: [{{
            label: 'Số đại lý sắp cạn hàng cần gọi',
            data: salesLabels.map(s => salesTaskCounts[s]),
            backgroundColor: '#ea580c',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ y: {{ grid: {{ color: '#f1f5f9' }} }} }}
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

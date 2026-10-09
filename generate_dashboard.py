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
  <title>King Blue - Customer Intelligence & RFM Dashboard 2026</title>
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
            <h1 class="text-lg sm:text-xl font-black tracking-tight">KING BLUE CUSTOMER INTELLIGENCE</h1>
            <span class="text-[10px] bg-amber-400 text-slate-950 font-black px-2 py-0.5 rounded-full uppercase tracking-wider">RFM Pro</span>
          </div>
          <p class="text-blue-200 text-xs font-medium">Báo cáo Phân tích Khách hàng Toàn diện & Quản trị Doanh số 2026 (01/01 - 29/09/2026)</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="flex items-center gap-2">
        <a href="../index.html" class="bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold text-xs px-3 py-2 rounded-xl flex items-center gap-1.5 transition">
          <span>🏠</span> <span>Cổng Marketing</span>
        </a>
        <button onclick="exportToCSV()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs px-3 py-2 rounded-xl flex items-center gap-1.5 transition shadow">
          <span>📥</span> <span>Xuất Excel/CSV</span>
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
          <span>🏢 Chi nhánh: <strong>Hồ Chí Minh & Đà Nẵng</strong></span>
        </span>
        <span class="inline-flex items-center gap-1.5 bg-blue-800/60 px-2.5 py-1 rounded-lg border border-blue-700/50">
          <span>📅 Chu kỳ: <strong>01/01/2026 - 29/09/2026 (9 Tháng)</strong></span>
        </span>
      </div>
      <div class="text-blue-300 font-medium">
        Hệ thống Tự động Nhận diện Pareto 80/20 & Chu kỳ Khách hàng
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

      <!-- Trả lại -->
      <div class="col-span-2 bg-white rounded-2xl p-4 border border-slate-200/80 shadow-sm relative overflow-hidden group hover:shadow-md transition">
        <div class="absolute -right-3 -top-3 w-16 h-16 bg-rose-50 rounded-full flex items-center justify-center text-rose-200 text-2xl font-black pointer-events-none group-hover:scale-110 transition">↺</div>
        <div class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Hàng Bán Trả Lại</div>
        <div class="text-2xl sm:text-3xl font-black text-rose-600 font-mono tracking-tight" id="kpi-return">984.4 Tr</div>
        <div class="mt-2 text-xs text-slate-500 flex items-center gap-1.5">
          <span class="bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded text-[11px]">Tỷ lệ: 1.00%</span>
          <span class="text-emerald-600 font-medium text-[11px]">Rất an toàn</span>
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

    </div>

    <!-- SECOND ROW KPI RIBBON -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
      
      <!-- Hạng A (Top 80%) -->
      <div class="bg-gradient-to-br from-blue-50 to-indigo-50/60 rounded-xl p-3.5 border border-blue-200/80 flex items-center justify-between">
        <div>
          <div class="text-[11px] font-bold text-blue-800 uppercase">Khách Hàng Hạng A (80%)</div>
          <div class="text-xl font-black text-blue-900 font-mono mt-0.5">42 Khách (10.7%)</div>
          <div class="text-xs text-blue-700 font-medium">Đóng góp: <strong>66.90 Tỷ (79.9%)</strong></div>
        </div>
        <div class="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center font-black text-base shadow">
          A
        </div>
      </div>

      <!-- Khách VIP / Vàng -->
      <div class="bg-gradient-to-br from-amber-50 to-orange-50/60 rounded-xl p-3.5 border border-amber-200/80 flex items-center justify-between">
        <div>
          <div class="text-[11px] font-bold text-amber-800 uppercase">VIP / Khách Hàng Vàng</div>
          <div class="text-xl font-black text-amber-900 font-mono mt-0.5">103 Khách (26.2%)</div>
          <div class="text-xs text-amber-700 font-medium">Đóng góp: <strong>69.04 Tỷ (82.4%)</strong></div>
        </div>
        <div class="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center font-black text-base shadow">
          👑
        </div>
      </div>

      <!-- Cảnh báo At Risk -->
      <div class="bg-gradient-to-br from-rose-50 to-pink-50/60 rounded-xl p-3.5 border border-rose-200/80 flex items-center justify-between">
        <div>
          <div class="text-[11px] font-bold text-rose-800 uppercase">Nguy Cơ Rời Bỏ (At-Risk)</div>
          <div class="text-xl font-black text-rose-900 font-mono mt-0.5">51 Khách (13.0%)</div>
          <div class="text-xs text-rose-700 font-medium">Doanh số cũ: <strong>7.32 Tỷ (8.7%)</strong></div>
        </div>
        <div class="w-10 h-10 rounded-xl bg-rose-500 text-white flex items-center justify-center font-black text-base shadow">
          ⚠️
        </div>
      </div>

      <!-- Giá trị TB Đơn (AOV) & ARPU -->
      <div class="bg-gradient-to-br from-emerald-50 to-teal-50/60 rounded-xl p-3.5 border border-emerald-200/80 flex items-center justify-between">
        <div>
          <div class="text-[11px] font-bold text-emerald-800 uppercase">AOV & ARPU Bình Quân</div>
          <div class="text-xl font-black text-emerald-900 font-mono mt-0.5">7.62 Tr / Đơn</div>
          <div class="text-xs text-emerald-700 font-medium">ARPU: <strong>213.1 Tr / Khách</strong></div>
        </div>
        <div class="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-black text-base shadow">
          📊
        </div>
      </div>

    </div>

    <!-- ================= MULTI-FILTER CONTROL BAR ================= -->
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
          <input type="text" id="search-input" oninput="applyFilters()" placeholder="Tìm tên KH, mã KH, SĐT..." class="w-full text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 pl-8 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition">
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

    <!-- ================= TAB NAVIGATION ================= -->
    <div class="flex items-center gap-2 border-b border-slate-200 pb-2 overflow-x-auto custom-scrollbar">
      <button onclick="switchTab('overview')" id="tab-overview" class="tab-btn active px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-transparent transition">
        <span>📈</span> <span>Tổng Quan & Phân Khúc</span>
      </button>
      <button onclick="switchTab('territory')" id="tab-territory" class="tab-btn bg-white hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-slate-200 transition">
        <span>🗺️</span> <span>Địa Lý & Đội Ngũ Sales</span>
      </button>
      <button onclick="switchTab('customers')" id="tab-customers" class="tab-btn bg-white hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-slate-200 transition">
        <span>📋</span> <span>Danh Bạ Khách Hàng 360°</span>
        <span class="bg-blue-100 text-blue-800 text-[10px] font-black px-1.5 py-0.5 rounded-full" id="tab-cust-count">393</span>
      </button>
      <button onclick="switchTab('strategy')" id="tab-strategy" class="tab-btn bg-white hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center gap-2 border border-slate-200 transition">
        <span>💡</span> <span>Chiến Lược & Cảnh Báo Hành Động</span>
        <span class="bg-rose-100 text-rose-700 text-[10px] font-black px-1.5 py-0.5 rounded-full">Hot</span>
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
              <p class="text-xs text-slate-500">Tăng trưởng đột biến vào Tháng 3 (16.4 Tỷ) và ổn định ở mức 7.5 - 10.6 Tỷ/tháng</p>
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
              <span>🎯</span> Cơ Cấu Hạng ABC (Pareto 80/20)
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

    <!-- ================= TAB 3: CUSTOMER MASTER 360 ================= -->
    <div id="section-customers" class="tab-section hidden space-y-4">
      
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

    <!-- ================= TAB 4: STRATEGIC ACTION MATRIX ================= -->
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
                <h3 class="text-base font-black text-slate-900">Ma Trận Cảnh Báo Sức Khỏe Khách Hàng & Chiến Lược Doanh Số Q4</h3>
                <p class="text-xs text-slate-600">Đề xuất hành động kinh doanh tức thì để bảo vệ doanh thu cốt lõi và hồi sinh khách hàng nguội lạnh</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <span class="bg-rose-100 text-rose-800 text-xs font-black px-3 py-1 rounded-lg">51 KH Cần Kích Hoạt Lại (7.32 Tỷ)</span>
              <span class="bg-blue-100 text-blue-800 text-xs font-black px-3 py-1 rounded-lg">42 KH Trụ Cột Hạng A (66.9 Tỷ)</span>
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
              <span class="bg-rose-500 text-white text-[11px] font-black px-2.5 py-1 rounded-lg uppercase tracking-wider">Hành Động Khẩn Cấp #1</span>
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

        <!-- Action 2: VIP / Tier A Protection -->
        <div class="bg-white rounded-2xl p-5 border-2 border-blue-200 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="bg-blue-600 text-white text-[11px] font-black px-2.5 py-1 rounded-lg uppercase tracking-wider">Chiến Lược Trọng Tâm #2</span>
              <span class="text-xs font-bold text-blue-700 font-mono">42 Khách • 66.9 Tỷ</span>
            </div>
            <h4 class="font-black text-slate-900 text-sm mb-1.5 flex items-center gap-2">
              <span>👑</span> Giữ Chân & Ký Hợp Đồng Năm Với 42 Đại Lý Hạng A (Top 80%)
            </h4>
            <p class="text-xs text-slate-600 leading-relaxed mb-4">
              Chỉ 42 khách hàng này chiếm tới <strong>79.9%</strong> tổng doanh số. Bất kỳ một đại lý nào trong nhóm này chuyển sang dùng hàng đối thủ sẽ gây ảnh hưởng nghiêm trọng đến doanh thu của KingBlue.
            </p>

            <div class="bg-blue-50 rounded-xl p-3 text-xs text-blue-900 space-y-1.5 border border-blue-100 mb-4">
              <div class="font-bold flex items-center gap-1.5"><span>🎯</span> Hướng dẫn triển khai:</div>
              <ul class="list-disc list-inside space-y-1 text-slate-700">
                <li>Gửi thư cảm ơn & quà tri ân đặc biệt từ Ban Giám Đốc KingBlue (NPP Châu Loan Đắk Lắk, Nông Sản Lâm Hồng, NPP Minh Phương, ThinkSafe...).</li>
                <li>Cam kết độc quyền vùng và ưu tiên 100% lượng hàng các mã bán chạy (Chén mài, Lưỡi cắt Kingblue).</li>
                <li>Ký kết chỉ tiêu doanh số năm 2027 kèm thưởng du lịch / hoàn tiền cuối năm.</li>
              </ul>
            </div>
          </div>

          <button onclick="filterByABC('A')" class="w-full bg-blue-700 hover:bg-blue-600 text-white font-bold text-xs py-2.5 rounded-xl transition shadow">
            Xem Danh Sách 42 Khách Hạng A Trụ Cột →
          </button>
        </div>

        <!-- Action 3: Upgrade Tier B to Tier A -->
        <div class="bg-white rounded-2xl p-5 border-2 border-emerald-200 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="bg-emerald-600 text-white text-[11px] font-black px-2.5 py-1 rounded-lg uppercase tracking-wider">Kích Cầu Tăng Trưởng #3</span>
              <span class="text-xs font-bold text-emerald-700 font-mono">80 Khách • 12.64 Tỷ</span>
            </div>
            <h4 class="font-black text-slate-900 text-sm mb-1.5 flex items-center gap-2">
              <span>🚀</span> Nâng Hạng Nhóm B Lên Nhóm A Bằng Chính Sách Bậc Thang
            </h4>
            <p class="text-xs text-slate-600 leading-relaxed mb-4">
              80 khách hàng Hạng B đang có sức mua đều đặn từ 50 - 200 triệu/tháng. Đây là nguồn lực tăng trưởng khả thi nhất để KingBlue bứt phá doanh số quý 4.
            </p>

            <div class="bg-emerald-50 rounded-xl p-3 text-xs text-emerald-900 space-y-1.5 border border-emerald-100 mb-4">
              <div class="font-bold flex items-center gap-1.5"><span>🎯</span> Hướng dẫn triển khai:</div>
              <ul class="list-disc list-inside space-y-1 text-slate-700">
                <li>Thiết lập chương trình chiết khấu bậc thang theo combo ngành hàng (VD: Lấy đá mài + máy pin được chiết khấu thêm 3%).</li>
                <li>Hỗ trợ đại lý làm biển bảng quảng cáo KingBlue, kệ trưng bày hàng chuẩn POSM.</li>
                <li>Tổ chức demo sản phẩm trực tiếp tại cửa hàng cho thợ cơ khí và xây dựng quanh khu vực.</li>
              </ul>
            </div>
          </div>

          <button onclick="filterByABC('B')" class="w-full bg-emerald-700 hover:bg-emerald-600 text-white font-bold text-xs py-2.5 rounded-xl transition shadow">
            Xem Danh Sách 80 Khách Hàng Hạng B →
          </button>
        </div>

        <!-- Action 4: Long Tail & Hibernating Optimization -->
        <div class="bg-white rounded-2xl p-5 border-2 border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="bg-slate-700 text-white text-[11px] font-black px-2.5 py-1 rounded-lg uppercase tracking-wider">Tối Ưu Chi Phí #4</span>
              <span class="text-xs font-bold text-slate-600 font-mono">271 Khách C • 91 Khách Ngủ Đông</span>
            </div>
            <h4 class="font-black text-slate-900 text-sm mb-1.5 flex items-center gap-2">
              <span>🧹</span> Tinh Gọn Quản Lý Nhóm C & Tối Ưu Chi Phí Bán Hàng
            </h4>
            <p class="text-xs text-slate-600 leading-relaxed mb-4">
              Nhóm C chiếm 69% số lượng khách (271 đại lý) nhưng chỉ tạo ra 5% doanh số. Nếu nhân viên kinh doanh tốn quá nhiều thời gian gọi điện chăm sóc nhóm này sẽ lãng phí nguồn lực.
            </p>

            <div class="bg-slate-50 rounded-xl p-3 text-xs text-slate-800 space-y-1.5 border border-slate-200 mb-4">
              <div class="font-bold flex items-center gap-1.5"><span>🎯</span> Hướng dẫn triển khai:</div>
              <ul class="list-disc list-inside space-y-1 text-slate-700">
                <li>Chuyển dịch nhóm C sang đặt hàng tự động qua Zalo OA / Website B2B hoặc gộp đơn tối thiểu từ 3 triệu/lần để giảm chi phí logistics.</li>
                <li>Kiểm soát chặt mức chiết khấu: Không áp dụng mức chiết khấu của đại lý lớn cho nhóm mua lẻ tẻ.</li>
                <li>Dọn dẹp và phân loại lại mã khách hàng ảo hoặc đại lý đã chuyển đổi mô hình kinh doanh.</li>
              </ul>
            </div>
          </div>

          <button onclick="filterByABC('C')" class="w-full bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs py-2.5 rounded-xl transition shadow">
            Xem Danh Sách Nhóm C Cần Tinh Gọn →
          </button>
        </div>

      </div>

    </div>

  </main>

  <!-- ================= CUSTOMER 360 MODAL ================= -->
  <div id="customer-modal" class="fixed inset-0 bg-slate-950/60 backdrop-blur-xs z-50 hidden flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
    <div class="bg-white rounded-3xl max-w-3xl w-full shadow-2xl border border-slate-200 overflow-hidden my-auto max-h-[90vh] flex flex-col">
      
      <!-- Modal Header -->
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

      <!-- Modal Body -->
      <div class="p-6 overflow-y-auto custom-scrollbar space-y-6 flex-1 text-xs">
        
        <!-- Metrics Row -->
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

        <!-- Contact & Sales Rep Info -->
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

        <!-- Top Categories Breakdown -->
        <div>
          <h4 class="font-black text-slate-900 text-xs uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
            <span>📦</span> Các Nhóm Ngành Hàng Đại Lý Tiêu Thụ Nhiều Nhất
          </h4>
          <div id="modal-cust-categories" class="space-y-2">
            <!-- Rendered via JS -->
          </div>
        </div>

        <!-- Top Products Breakdown -->
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
              <tbody id="modal-cust-products" class="divide-y divide-slate-100">
                <!-- Rendered via JS -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Recommended Action Box -->
        <div class="bg-blue-50 border border-blue-200 rounded-2xl p-4">
          <div class="font-black text-blue-900 text-xs flex items-center gap-1.5 mb-1">
            <span>💡</span> Khuyến Nghị Hành Động Chăm Sóc Cho Đại Lý Này:
          </div>
          <p id="modal-cust-action" class="text-xs text-blue-800 leading-relaxed font-medium">
            --
          </p>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
        <span class="text-[11px] text-slate-400">KingBlue Customer Intelligence 360° View</span>
        <button onclick="closeCustomerModal()" class="bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs px-4 py-2 rounded-xl transition">
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
    let currentPage = 1;
    let pageSize = 30;
    let currentSort = {{ col: 'net', asc: false }};

    // Number formatter
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
    }});

    // Populate dropdown options
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
    }}

    // Filter Logic
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

      // Sort
      sortFilteredData();

      currentPage = 1;
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

    // Table Sorting
    function sortTable(col) {{
      if (currentSort.col === col) {{
        currentSort.asc = !currentSort.asc;
      }} else {{
        currentSort.col = col;
        currentSort.asc = (col === 'name' || col === 'id' || col === 'province') ? true : false;
      }}
      sortFilteredData();
      renderMasterTable();
    }}

    function sortFilteredData() {{
      filteredCustomers.sort((a, b) => {{
        let valA = a[currentSort.col];
        let valB = b[currentSort.col];
        if (typeof valA === 'string') valA = valA.toLowerCase();
        if (typeof valB === 'string') valB = valB.toLowerCase();

        if (valA < valB) return currentSort.asc ? -1 : 1;
        if (valA > valB) return currentSort.asc ? 1 : -1;
        return 0;
      }});
    }}

    // Pagination
    function changePageSize(val) {{
      if (val === 'ALL') {{
        pageSize = filteredCustomers.length || 1;
      }} else {{
        pageSize = parseInt(val);
      }}
      currentPage = 1;
      renderMasterTable();
    }}

    // Render Master Table
    function renderMasterTable() {{
      const tbody = document.getElementById('master-table-tbody');
      tbody.innerHTML = '';

      const start = (currentPage - 1) * pageSize;
      const end = Math.min(start + pageSize, filteredCustomers.length);
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
        tr.onclick = (e) => {{
          if (e.target.tagName !== 'BUTTON') openCustomerModal(c.id);
        }};

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

      // Update Pagination UI
      document.getElementById('pagination-info').textContent = `Hiển thị ${{start + 1}} - ${{end}} trong tổng số ${{filteredCustomers.length}} khách hàng`;
      renderPaginationButtons();
    }}

    function renderPaginationButtons() {{
      const container = document.getElementById('pagination-buttons');
      container.innerHTML = '';
      const totalPages = Math.ceil(filteredCustomers.length / pageSize) || 1;

      if (totalPages <= 1) return;

      const prevBtn = document.createElement('button');
      prevBtn.className = `px-2 py-1 rounded border text-xs font-bold ${{currentPage === 1 ? 'opacity-40 cursor-not-allowed border-slate-200' : 'hover:bg-slate-100 border-slate-300'}}`;
      prevBtn.textContent = '◀';
      prevBtn.disabled = currentPage === 1;
      prevBtn.onclick = () => {{ if (currentPage > 1) {{ currentPage--; renderMasterTable(); }} }};
      container.appendChild(prevBtn);

      let startP = Math.max(1, currentPage - 2);
      let endP = Math.min(totalPages, startP + 4);
      if (endP - startP < 4) startP = Math.max(1, endP - 4);

      for (let p = startP; p <= endP; p++) {{
        const btn = document.createElement('button');
        btn.className = `px-2.5 py-1 rounded text-xs font-bold ${{p === currentPage ? 'bg-blue-600 text-white' : 'hover:bg-slate-100 border border-slate-200 text-slate-700'}}`;
        btn.textContent = p;
        btn.onclick = () => {{ currentPage = p; renderMasterTable(); }};
        container.appendChild(btn);
      }}

      const nextBtn = document.createElement('button');
      nextBtn.className = `px-2 py-1 rounded border text-xs font-bold ${{currentPage === totalPages ? 'opacity-40 cursor-not-allowed border-slate-200' : 'hover:bg-slate-100 border-slate-300'}}`;
      nextBtn.textContent = '▶';
      nextBtn.disabled = currentPage === totalPages;
      nextBtn.onclick = () => {{ if (currentPage < totalPages) {{ currentPage++; renderMasterTable(); }} }};
      container.appendChild(nextBtn);
    }}

    // Render Top 10 Preview
    function renderTopCustomers() {{
      const tbody = document.getElementById('top-customers-tbody');
      tbody.innerHTML = '';
      const top10 = allCustomers.slice(0, 10);

      top10.forEach((c, idx) => {{
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

    // Render Sales Detail Table
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

    // Render Province Detail Table
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

    // Customer 360 Modal
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

      // Top categories
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
      }} else {{
        catContainer.innerHTML = '<div class="text-slate-400">Không có dữ liệu ngành hàng</div>';
      }}

      // Top products table
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
      }} else {{
        prodTable.innerHTML = '<tr><td colspan="3" class="text-center py-3 text-slate-400">Chưa có dữ liệu sản phẩm</td></tr>';
      }}

      document.getElementById('customer-modal').classList.remove('hidden');
    }}

    function closeCustomerModal() {{
      document.getElementById('customer-modal').classList.add('hidden');
    }}

    // Export to CSV
    function exportToCSV() {{
      let csvContent = "\\uFEFF"; // UTF-8 BOM
      csvContent += "Mã KH,Tên Khách Hàng,Tỉnh Thành,Sales Phụ Trách,Số Đơn,Doanh Thu Thuần,Doanh Số Gộp,Chiết Khấu,Tỷ Lệ CK,Lần Mua Cuối,Recency Ngày,Hạng ABC,Phân Khúc RFM\\n";

      filteredCustomers.forEach(c => {{
        const row = [
          `"${{c.id}}"`,
          `"${{c.name.replace(/"/g, '""')}}"`,
          `"${{c.province}}"`,
          `"${{c.main_sales_rep}}"`,
          c.f_orders,
          c.net,
          c.gross,
          c.discount,
          c.discount_pct,
          `"${{c.last_date}}"`,
          c.r_days,
          `"${{c.abc}}"`,
          `"${{c.segment}}"`
        ];
        csvContent += row.join(",") + "\\n";
      }});

      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `KingBlue_Bao_Cao_Khach_Hang_${{new Date().toISOString().slice(0, 10)}}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    // Chart.js Visualizations
    function initCharts() {{
      
      // 1. Monthly Chart
      const ctxMonthly = document.getElementById('monthlyChart').getContext('2d');
      const monthLabels = RAW_DATA.monthly.map(m => m.month_label);
      const monthNet = RAW_DATA.monthly.map(m => m.net / 1e9);
      const monthDiscount = RAW_DATA.monthly.map(m => m.discount / 1e9);
      const monthOrders = RAW_DATA.monthly.map(m => m.orders);

      new Chart(ctxMonthly, {{
        type: 'bar',
        data: {{
          labels: monthLabels,
          datasets: [
            {{
              type: 'line',
              label: 'Số đơn hàng',
              data: monthOrders,
              borderColor: '#f59e0b',
              backgroundColor: '#f59e0b',
              yAxisID: 'yOrders',
              borderWidth: 2,
              tension: 0.3,
              pointRadius: 4
            }},
            {{
              type: 'bar',
              label: 'Doanh thu thuần (Tỷ VNĐ)',
              data: monthNet,
              backgroundColor: '#2563eb',
              borderRadius: 6,
              yAxisID: 'yRev'
            }},
            {{
              type: 'bar',
              label: 'Chiết khấu (Tỷ VNĐ)',
              data: monthDiscount,
              backgroundColor: '#93c5fd',
              borderRadius: 6,
              yAxisID: 'yRev'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          interaction: {{ mode: 'index', intersect: false }},
          plugins: {{
            legend: {{ position: 'top', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }},
            tooltip: {{
              callbacks: {{
                label: function(ctx) {{
                  if (ctx.dataset.yAxisID === 'yOrders') return `Số đơn: ${{fmtNumber(ctx.raw)}} đơn`;
                  return `${{ctx.dataset.label}}: ${{ctx.raw.toFixed(2)}} Tỷ VNĐ`;
                }}
              }}
            }}
          }},
          scales: {{
            yRev: {{
              type: 'linear',
              position: 'left',
              title: {{ display: true, text: 'Doanh thu (Tỷ VNĐ)', font: {{ size: 10 }} }},
              grid: {{ color: '#f1f5f9' }}
            }},
            yOrders: {{
              type: 'linear',
              position: 'right',
              title: {{ display: true, text: 'Số lượng đơn hàng', font: {{ size: 10 }} }},
              grid: {{ drawOnChartArea: false }}
            }}
          }}
        }}
      }});

      // 2. ABC Pareto Donut Chart
      const ctxAbc = document.getElementById('abcChart').getContext('2d');
      new Chart(ctxAbc, {{
        type: 'doughnut',
        data: {{
          labels: ['Hạng A (80% DT)', 'Hạng B (15% DT)', 'Hạng C (5% DT)'],
          datasets: [{{
            data: [
              RAW_DATA.abc.find(a => a.tier === 'A').net / 1e9,
              RAW_DATA.abc.find(a => a.tier === 'B').net / 1e9,
              RAW_DATA.abc.find(a => a.tier === 'C').net / 1e9
            ],
            backgroundColor: ['#2563eb', '#0ea5e9', '#cbd5e1'],
            borderWidth: 3,
            borderColor: '#ffffff'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }},
            tooltip: {{
              callbacks: {{
                label: function(ctx) {{
                  return `${{ctx.label}}: ${{ctx.raw.toFixed(2)}} Tỷ VNĐ`;
                }}
              }}
            }}
          }},
          cutout: '68%'
        }}
      }});

      // 3. RFM Chart
      const ctxRfm = document.getElementById('rfmChart').getContext('2d');
      const rfmLabels = RAW_DATA.segments.map(s => s.name.split('/')[0].trim());
      const rfmNet = RAW_DATA.segments.map(s => s.net / 1e9);
      const rfmColors = RAW_DATA.segments.map(s => s.color);

      new Chart(ctxRfm, {{
        type: 'bar',
        data: {{
          labels: rfmLabels,
          datasets: [{{
            label: 'Doanh thu thuần (Tỷ VNĐ)',
            data: rfmNet,
            backgroundColor: rfmColors,
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
                label: function(ctx) {{
                  const seg = RAW_DATA.segments[ctx.dataIndex];
                  return `${{seg.count}} KH (${{seg.cust_pct}}%) | ${{ctx.raw.toFixed(2)}} Tỷ VNĐ (${{seg.rev_pct}}%)`;
                }}
              }}
            }}
          }},
          scales: {{
            x: {{ grid: {{ color: '#f1f5f9' }}, title: {{ display: true, text: 'Doanh thu thuần (Tỷ VNĐ)', font: {{ size: 10 }} }} }}
          }}
        }}
      }});

      // 4. Categories Chart
      const ctxCat = document.getElementById('categoryChart').getContext('2d');
      const topCats = RAW_DATA.categories.slice(0, 8);
      new Chart(ctxCat, {{
        type: 'bar',
        data: {{
          labels: topCats.map(c => c.name),
          datasets: [{{
            label: 'Doanh số gộp (Tỷ VNĐ)',
            data: topCats.map(c => c.gross / 1e9),
            backgroundColor: ['#1e40af', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#cbd5e1', '#e2e8f0'],
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
                label: function(ctx) {{
                  const c = topCats[ctx.dataIndex];
                  return `${{ctx.raw.toFixed(2)}} Tỷ VNĐ (${{c.pct_of_total}}%) | ${{fmtNumber(c.qty)}} sp | ${{c.customers}} KH`;
                }}
              }}
            }}
          }},
          scales: {{
            x: {{ grid: {{ color: '#f1f5f9' }}, title: {{ display: true, text: 'Doanh số gộp (Tỷ VNĐ)', font: {{ size: 10 }} }} }}
          }}
        }}
      }});

      // 5. Province Chart
      const ctxProv = document.getElementById('provinceChart').getContext('2d');
      const topProvs = RAW_DATA.provinces.slice(0, 10);
      new Chart(ctxProv, {{
        type: 'bar',
        data: {{
          labels: topProvs.map(p => p.province),
          datasets: [{{
            label: 'Doanh thu thuần (Tỷ VNĐ)',
            data: topProvs.map(p => p.net / 1e9),
            backgroundColor: '#1d4ed8',
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
                label: function(ctx) {{
                  const p = topProvs[ctx.dataIndex];
                  return `${{ctx.raw.toFixed(2)}} Tỷ VNĐ (${{p.pct_of_total}}%) | ${{p.customers}} KH | ${{fmtNumber(p.orders)}} đơn`;
                }}
              }}
            }}
          }},
          scales: {{
            x: {{ grid: {{ color: '#f1f5f9' }} }}
          }}
        }}
      }});

      // 6. Sales Chart
      const ctxSales = document.getElementById('salesChart').getContext('2d');
      new Chart(ctxSales, {{
        type: 'bar',
        data: {{
          labels: RAW_DATA.sales_reps.map(s => s.name),
          datasets: [{{
            label: 'Doanh thu thuần (Tỷ VNĐ)',
            data: RAW_DATA.sales_reps.map(s => s.net / 1e9),
            backgroundColor: '#059669',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: function(ctx) {{
                  const s = RAW_DATA.sales_reps[ctx.dataIndex];
                  return `${{ctx.raw.toFixed(2)}} Tỷ VNĐ (${{s.pct_of_total}}%) | ${{s.customers}} KH | ${{fmtNumber(s.orders)}} đơn`;
                }}
              }}
            }}
          }},
          scales: {{
            y: {{ grid: {{ color: '#f1f5f9' }}, title: {{ display: true, text: 'Doanh thu (Tỷ VNĐ)', font: {{ size: 10 }} }} }}
          }}
        }}
      }});

    }}
  </script>
</body>
</html>
"""

# Write to both Report/customer_dashboard.html and customer_dashboard.html in root
report_html_path = '/Users/Admin/Documents/KIng BLue/Report/customer_dashboard.html'
root_html_path = '/Users/Admin/Documents/KIng BLue/customer_dashboard.html'

with open(report_html_path, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Generated {report_html_path} ({os.path.getsize(report_html_path)/1024:.1f} KB)")

with open(root_html_path, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Generated {root_html_path} ({os.path.getsize(root_html_path)/1024:.1f} KB)")


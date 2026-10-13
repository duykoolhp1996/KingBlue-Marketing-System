import json

with open('tiktok_cko_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

json_data_str = json.dumps(data, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Báo Cáo Hiệu Quả Nội Dung TikTok Cko Store (Q3/2026)</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Google Fonts: Inter & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #0B0F17;
      color: #E2E8F0;
    }}
    .font-mono {{ font-family: 'JetBrains+Mono', monospace; }}
    .hide-scrollbar::-webkit-scrollbar {{ display: none; }}
    .hide-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
    
    /* Custom Neon & Glow Accents */
    .glow-cyan {{
      box-shadow: 0 0 25px -5px rgba(0, 242, 254, 0.25);
    }}
    .glow-rose {{
      box-shadow: 0 0 25px -5px rgba(254, 44, 85, 0.25);
    }}
    .gradient-tiktok {{
      background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 50%, #FE2C55 100%);
    }}
    .gradient-text-tiktok {{
      background: linear-gradient(135deg, #00F2FE 0%, #FE2C55 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .glass-card {{
      background: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .glass-card-hover:hover {{
      background: rgba(24, 33, 53, 0.95);
      border-color: rgba(0, 242, 254, 0.3);
      transform: translateY(-2px);
    }}

    @media print {{
      body {{ background: white; color: black; }}
      .no-print {{ display: none !important; }}
      .glass-card {{ background: white; border: 1px solid #cbd5e1; color: black; box-shadow: none; }}
    }}
  </style>
</head>
<body class="min-h-screen antialiased selection:bg-[#FE2C55]/30 selection:text-white">

  <!-- ================= TOP NOTIFICATION / BRAND BAR ================= -->
  <header class="sticky top-0 z-50 bg-[#0B0F17]/90 backdrop-blur-md border-b border-slate-800/80 px-4 sm:px-8 py-3.5 transition-all">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
      
      <!-- Brand & Channel Info -->
      <div class="flex items-center gap-3.5 w-full md:w-auto">
        <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-[#00F2FE] to-[#FE2C55] p-0.5 flex items-center justify-center shrink-0 shadow-lg glow-rose">
          <div class="w-full h-full bg-[#0B0F17] rounded-[14px] flex items-center justify-center font-black text-xl text-white">
            <svg class="w-6 h-6 fill-current text-white" viewBox="0 0 24 24">
              <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64c.298-.002.595.042.88.13V9.4a6.33 6.33 0 0 0-1-.08A6.34 6.34 0 0 0 3 15.66a6.34 6.34 0 0 0 10.82 4.5 6.3 6.3 0 0 0 1.88-4.5V8.84a8.28 8.28 0 0 0 4.89 1.58V7a4.83 4.83 0 0 1-1-.31z"/>
            </svg>
          </div>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-base sm:text-lg font-black text-white tracking-tight flex items-center gap-1.5">
              CKO STORE <span class="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono font-normal border border-slate-700">@cko_store</span>
            </h1>
            <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> TikTok Analytics
            </span>
          </div>
          <p class="text-xs text-slate-400">Báo Cáo Hiệu Quả Nội Dung Video Q3 (Tháng 7 - Tháng 9 / 2026) & Kế Hoạch T11</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2 w-full md:w-auto justify-end overflow-x-auto no-print">
        <a href="https://www.tiktok.com/@cko_store" target="_blank" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-1.5 shrink-0">
          <span>🎵</span> <span>Kênh TikTok</span>
        </a>
        <a href="https://docs.google.com/spreadsheets/d/1Nkq-OrCnu5yC_1FKyp0JBJxfOnQ1YG4d5VcAtwqFxoY/edit?gid=0#gid=0" target="_blank" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-700/50 transition flex items-center gap-1.5 shrink-0">
          <span>📊</span> <span>Google Sheet Gốc</span>
        </a>
        <button onclick="copyExecutiveSummary()" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-blue-950 hover:bg-blue-900 text-blue-300 border border-blue-700/50 transition flex items-center gap-1.5 shrink-0">
          <span>📋</span> <span>Copy Tóm Tắt BOD</span>
        </button>
        <button onclick="window.print()" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition flex items-center gap-1.5 shrink-0">
          <span>🖨️</span> <span>In PDF</span>
        </button>
      </div>

    </div>
  </header>

  <!-- ================= MAIN CONTAINER ================= -->
  <main class="max-w-7xl mx-auto px-4 sm:px-8 py-6 space-y-7">

    <!-- HERO HIGHLIGHT BANNER -->
    <div class="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-r from-[#0F172A] via-[#1E1B4B] to-[#0F172A] p-6 sm:p-8 shadow-2xl">
      <div class="absolute -right-16 -top-16 w-64 h-64 bg-[#FE2C55]/15 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -left-16 -bottom-16 w-64 h-64 bg-[#00F2FE]/15 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative z-10 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
        <div class="space-y-2 max-w-2xl">
          <div class="flex items-center gap-2">
            <span class="text-xs font-black tracking-wider uppercase px-2.5 py-0.5 rounded-md bg-[#FE2C55]/20 text-[#FE2C55] border border-[#FE2C55]/30">
              Q3/2026 Executive Review
            </span>
            <span class="text-xs text-slate-400 font-mono">Dữ liệu thực tế: 68 Video</span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-black text-white tracking-tight leading-snug">
            Tăng trưởng đột phá Tháng 9: <span class="gradient-text-tiktok">+26.3% Lượt xem & +365% Lượt thích</span>
          </h2>
          <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Nhóm <strong class="text-white">Collab KOL/KOC</strong> bùng nổ hiệu ứng viral với trung bình <strong>7,152 lượt xem/video</strong> (cao gấp 3.3 lần trung bình kênh). Video giới thiệu sản phẩm tiếp tục giữ vai trò xương sống gắn giỏ hàng TikTok Shop với 75% sản lượng.
          </p>
        </div>

        <!-- Quick Filter Switcher -->
        <div class="bg-slate-900/90 border border-slate-800 p-2 rounded-2xl flex flex-wrap sm:flex-nowrap items-center gap-1.5 w-full lg:w-auto justify-center shrink-0">
          <button onclick="setFilterMonth('ALL')" id="filter-btn-ALL" class="filter-month-btn px-3.5 py-2 rounded-xl text-xs font-extrabold transition bg-gradient-to-r from-[#00F2FE] to-[#FE2C55] text-slate-950 shadow-md">
            🌟 Tất cả Q3 (68 Video)
          </button>
          <button onclick="setFilterMonth('Tháng 7')" id="filter-btn-Tháng 7" class="filter-month-btn px-3 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition">
            Tháng 7 (25)
          </button>
          <button onclick="setFilterMonth('Tháng 8')" id="filter-btn-Tháng 8" class="filter-month-btn px-3 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition">
            Tháng 8 (22)
          </button>
          <button onclick="setFilterMonth('Tháng 9')" id="filter-btn-Tháng 9" class="filter-month-btn px-3 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition">
            🔥 Tháng 9 (21)
          </button>
        </div>
      </div>
    </div>

    <!-- ================= 1. HERO KPI CARDS GRID ================= -->
    <section class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5 sm:gap-4">
      
      <!-- KPI 1: Tổng số Video -->
      <div class="glass-card glass-card-hover p-4 sm:p-5 rounded-2xl flex flex-col justify-between transition-all duration-200">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-400">Tổng Video</span>
          <span class="text-lg">🎬</span>
        </div>
        <div class="mt-3">
          <div class="text-2xl sm:text-3xl font-black text-white font-mono" id="kpi-videos">68</div>
          <div class="flex items-center gap-1 text-[11px] font-bold text-sky-400 mt-1" id="kpi-videos-sub">
            <span>22.7</span> <span>video / tháng</span>
          </div>
        </div>
      </div>

      <!-- KPI 2: Tổng Lượt Xem -->
      <div class="glass-card glass-card-hover p-4 sm:p-5 rounded-2xl flex flex-col justify-between transition-all duration-200 border-l-2 border-l-[#00F2FE]">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-400">Tổng Lượt Xem</span>
          <span class="text-lg">👁️</span>
        </div>
        <div class="mt-3">
          <div class="text-2xl sm:text-3xl font-black text-white font-mono" id="kpi-views">173,762</div>
          <div class="flex items-center gap-1 text-[11px] font-bold text-emerald-400 mt-1" id="kpi-views-sub">
            <span>▲ +26.3%</span> <span class="text-slate-500 font-normal">T9 vs T8</span>
          </div>
        </div>
      </div>

      <!-- KPI 3: Tổng Lượt Thích -->
      <div class="glass-card glass-card-hover p-4 sm:p-5 rounded-2xl flex flex-col justify-between transition-all duration-200 border-l-2 border-l-[#FE2C55]">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-400">Tổng Lượt Thích</span>
          <span class="text-lg">❤️</span>
        </div>
        <div class="mt-3">
          <div class="text-2xl sm:text-3xl font-black text-white font-mono" id="kpi-likes">2,019</div>
          <div class="flex items-center gap-1 text-[11px] font-bold text-[#FE2C55] mt-1" id="kpi-likes-sub">
            <span>▲ +365.4%</span> <span class="text-slate-500 font-normal">bùng nổ T9</span>
          </div>
        </div>
      </div>

      <!-- KPI 4: Tổng Bình Luận -->
      <div class="glass-card glass-card-hover p-4 sm:p-5 rounded-2xl flex flex-col justify-between transition-all duration-200">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-400">Bình Luận</span>
          <span class="text-lg">💬</span>
        </div>
        <div class="mt-3">
          <div class="text-2xl sm:text-3xl font-black text-white font-mono" id="kpi-comments">62</div>
          <div class="flex items-center gap-1 text-[11px] font-bold text-amber-400 mt-1" id="kpi-comments-sub">
            <span>▲ +583%</span> <span class="text-slate-500 font-normal">tương tác T9</span>
          </div>
        </div>
      </div>

      <!-- KPI 5: TB Lượt Xem / Video -->
      <div class="glass-card glass-card-hover p-4 sm:p-5 rounded-2xl flex flex-col justify-between transition-all duration-200">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-400">TB View / Video</span>
          <span class="text-lg">📊</span>
        </div>
        <div class="mt-3">
          <div class="text-2xl sm:text-3xl font-black text-white font-mono" id="kpi-avg-views">2,555</div>
          <div class="flex items-center gap-1 text-[11px] font-bold text-slate-400 mt-1" id="kpi-avg-views-sub">
            <span>KOL: 7,152</span>
          </div>
        </div>
      </div>

      <!-- KPI 6: Tỷ Lệ Tương Tác -->
      <div class="glass-card glass-card-hover p-4 sm:p-5 rounded-2xl flex flex-col justify-between transition-all duration-200">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-400">Engagement Rate</span>
          <span class="text-lg">🎯</span>
        </div>
        <div class="mt-3">
          <div class="text-2xl sm:text-3xl font-black text-white font-mono" id="kpi-eng-rate">1.20%</div>
          <div class="flex items-center gap-1 text-[11px] font-bold text-emerald-400 mt-1" id="kpi-eng-rate-sub">
            <span>2,081</span> <span class="text-slate-500 font-normal">tổng TT</span>
          </div>
        </div>
      </div>

    </section>

    <!-- ================= 2. CHARTS SECTION ================= -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
      
      <!-- Chart A: Xu Hướng Tăng Trưởng Lượt Xem & Lượt Thích Theo Tháng (7 Cols) -->
      <div class="lg:col-span-7 glass-card p-5 sm:p-6 rounded-3xl space-y-4">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
          <div>
            <h3 class="text-sm sm:text-base font-extrabold text-white flex items-center gap-2">
              <span>📈</span> Xu Hướng Lượt Xem & Tương Tác Qua 3 Tháng (MoM)
            </h3>
            <p class="text-xs text-slate-400">Tăng trưởng liên tục qua các tháng: Tháng 7 (49.7k) ➔ Tháng 8 (54.8k) ➔ Tháng 9 (69.2k)</p>
          </div>
          <span class="text-[11px] font-mono font-bold px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            T9 Đạt Đỉnh Views
          </span>
        </div>
        <div class="h-64 sm:h-72 w-full">
          <canvas id="monthlyTrendChart"></canvas>
        </div>
      </div>

      <!-- Chart B: Cơ Cấu Tỷ Trọng Lượt Xem Theo Nhóm Nội Dung (5 Cols) -->
      <div class="lg:col-span-5 glass-card p-5 sm:p-6 rounded-3xl space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800/80 pb-3">
          <div>
            <h3 class="text-sm sm:text-base font-extrabold text-white flex items-center gap-2">
              <span>🍩</span> Tỷ Trọng Lượt Xem Theo Nhóm
            </h3>
            <p class="text-xs text-slate-400">Cơ cấu đóng góp view giữa sản phẩm và collab</p>
          </div>
        </div>
        <div class="h-64 sm:h-72 w-full flex items-center justify-center">
          <canvas id="categoryShareChart"></canvas>
        </div>
      </div>

    </div>

    <!-- ================= 3. PERFORMANCE MATRIX BY CATEGORY ================= -->
    <section class="glass-card rounded-3xl p-5 sm:p-6 space-y-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
        <div>
          <h3 class="text-base sm:text-lg font-black text-white flex items-center gap-2">
            <span>📊</span> Bảng So Sánh Hiệu Quả Chi Tiết Theo Nhóm Nội Dung
          </h3>
          <p class="text-xs text-slate-400">Đánh giá tương quan giữa Sản lượng video, Lượt xem và Hiệu quả tương tác thực tế</p>
        </div>
        <div class="flex items-center gap-2 text-xs font-mono text-slate-400">
          <span class="w-2.5 h-2.5 rounded-full bg-[#00F2FE]"></span> Views
          <span class="w-2.5 h-2.5 rounded-full bg-[#FE2C55] ml-2"></span> Likes
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs sm:text-sm text-slate-300">
          <thead class="bg-slate-900/90 text-slate-400 uppercase font-mono text-[11px] border-b border-slate-800">
            <tr>
              <th class="p-3.5">Nhóm Nội Dung</th>
              <th class="p-3.5 text-center">Số Video</th>
              <th class="p-3.5 text-center">% Số Video</th>
              <th class="p-3.5 text-right">Tổng Views</th>
              <th class="p-3.5 text-right">TB Views / Video</th>
              <th class="p-3.5 text-right">% Views</th>
              <th class="p-3.5 text-right">Tổng Likes</th>
              <th class="p-3.5 text-right">TB Likes</th>
              <th class="p-3.5 text-right">% Likes</th>
              <th class="p-3.5 text-center">Đánh Giá</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60 font-medium">
            
            <!-- Category 1: Giới thiệu sản phẩm -->
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                <span>Giới thiệu sản phẩm</span>
              </td>
              <td class="p-3.5 text-center font-mono font-bold text-white">51</td>
              <td class="p-3.5 text-center font-mono text-slate-400">75.0%</td>
              <td class="p-3.5 text-right font-mono font-bold text-white">109,269</td>
              <td class="p-3.5 text-right font-mono text-slate-300">2,143</td>
              <td class="p-3.5 text-right font-mono text-emerald-400 font-bold">62.88%</td>
              <td class="p-3.5 text-right font-mono text-white">684</td>
              <td class="p-3.5 text-right font-mono text-slate-400">13.4</td>
              <td class="p-3.5 text-right font-mono text-slate-400">33.88%</td>
              <td class="p-3.5 text-center">
                <span class="px-2 py-0.5 rounded-md bg-blue-500/10 text-blue-400 text-[11px] font-bold border border-blue-500/20">
                  Xương sống bán hàng
                </span>
              </td>
            </tr>

            <!-- Category 2: Collab KOL/KOC -->
            <tr class="hover:bg-slate-800/40 transition bg-[#FE2C55]/5 border-l-2 border-l-[#FE2C55]">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-[#FE2C55]"></span>
                <span class="text-[#FE2C55] font-black">Collab KOL / KOC</span>
                <span class="text-[10px] px-1.5 py-0.2 rounded bg-[#FE2C55] text-white font-bold">HOT</span>
              </td>
              <td class="p-3.5 text-center font-mono font-bold text-white">7</td>
              <td class="p-3.5 text-center font-mono text-slate-400">10.3%</td>
              <td class="p-3.5 text-right font-mono font-black text-white">50,061</td>
              <td class="p-3.5 text-right font-mono text-[#00F2FE] font-black">7,152</td>
              <td class="p-3.5 text-right font-mono text-[#00F2FE] font-bold">28.81%</td>
              <td class="p-3.5 text-right font-mono font-black text-[#FE2C55]">1,192</td>
              <td class="p-3.5 text-right font-mono text-[#FE2C55] font-black">170.3</td>
              <td class="p-3.5 text-right font-mono text-[#FE2C55] font-bold">59.04%</td>
              <td class="p-3.5 text-center">
                <span class="px-2 py-0.5 rounded-md bg-[#FE2C55]/20 text-[#FE2C55] text-[11px] font-bold border border-[#FE2C55]/30">
                  Hiệu quả Viral vượt trội
                </span>
              </td>
            </tr>

            <!-- Category 3: Review / Trải nghiệm -->
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                <span>Review / trải nghiệm thực tế</span>
              </td>
              <td class="p-3.5 text-center font-mono font-bold text-white">3</td>
              <td class="p-3.5 text-center font-mono text-slate-400">4.4%</td>
              <td class="p-3.5 text-right font-mono font-bold text-white">5,215</td>
              <td class="p-3.5 text-right font-mono text-slate-300">1,738</td>
              <td class="p-3.5 text-right font-mono text-slate-400">3.00%</td>
              <td class="p-3.5 text-right font-mono text-white">74</td>
              <td class="p-3.5 text-right font-mono text-slate-400">24.7</td>
              <td class="p-3.5 text-right font-mono text-slate-400">3.67%</td>
              <td class="p-3.5 text-center">
                <span class="px-2 py-0.5 rounded-md bg-amber-500/10 text-amber-400 text-[11px] font-bold border border-amber-500/20">
                  Tương tác tốt (24.7 lk)
                </span>
              </td>
            </tr>

            <!-- Category 4: Hướng dẫn sử dụng -->
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                <span>Hướng dẫn sử dụng</span>
              </td>
              <td class="p-3.5 text-center font-mono font-bold text-white">4</td>
              <td class="p-3.5 text-center font-mono text-slate-400">5.9%</td>
              <td class="p-3.5 text-right font-mono font-bold text-white">6,188</td>
              <td class="p-3.5 text-right font-mono text-slate-300">1,547</td>
              <td class="p-3.5 text-right font-mono text-slate-400">3.56%</td>
              <td class="p-3.5 text-right font-mono text-white">52</td>
              <td class="p-3.5 text-right font-mono text-slate-400">13.0</td>
              <td class="p-3.5 text-right font-mono text-slate-400">2.58%</td>
              <td class="p-3.5 text-center">
                <span class="px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 text-[11px] font-bold border border-emerald-500/20">
                  Tăng uy tín & CSKH
                </span>
              </td>
            </tr>

            <!-- Category 5: Banner sản phẩm -->
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
                <span>Banner sản phẩm</span>
              </td>
              <td class="p-3.5 text-center font-mono font-bold text-white">3</td>
              <td class="p-3.5 text-center font-mono text-slate-400">4.4%</td>
              <td class="p-3.5 text-right font-mono font-bold text-white">3,029</td>
              <td class="p-3.5 text-right font-mono text-slate-300">1,010</td>
              <td class="p-3.5 text-right font-mono text-slate-400">1.74%</td>
              <td class="p-3.5 text-right font-mono text-white">17</td>
              <td class="p-3.5 text-right font-mono text-slate-400">5.7</td>
              <td class="p-3.5 text-right font-mono text-slate-400">0.84%</td>
              <td class="p-3.5 text-center">
                <span class="px-2 py-0.5 rounded-md bg-purple-500/10 text-purple-400 text-[11px] font-bold border border-purple-500/20">
                  Hiệu quả thấp nhất
                </span>
              </td>
            </tr>

          </tbody>
        </table>
      </div>
    </section>

    <!-- ================= 4. TOP PERFORMING VIDEOS SPOTLIGHT ================= -->
    <section class="space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-base sm:text-lg font-black text-white flex items-center gap-2">
            <span>🏆</span> Top Video Xuất Sắc Nhất Quý 3 (Viral Leaderboard)
          </h3>
          <p class="text-xs text-slate-400">Các video đạt lượt xem và tương tác cao nhất dẫn dắt lưu lượng toàn kênh</p>
        </div>
        <span class="text-xs text-slate-400 font-mono hidden sm:inline">Nhấp vào thẻ để mở xem video TikTok</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="top-videos-grid">
        <!-- Populated by JS -->
      </div>
    </section>

    <!-- ================= 5. STRATEGIC EVALUATION & PLAN THÁNG 11 ================= -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
      
      <!-- Box 1: Đánh Giá & Bài Học Thực Chiến (7 Cols) -->
      <div class="lg:col-span-7 glass-card p-6 rounded-3xl space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800/80 pb-3">
          <h3 class="text-base font-extrabold text-white flex items-center gap-2">
            <span>💡</span> Đánh Giá Chiến Lược & Bài Học Marketing
          </h3>
          <span class="text-xs px-2.5 py-0.5 rounded-md bg-amber-500/10 text-amber-400 border border-amber-500/20 font-bold">
            Insight Chuyên Sâu
          </span>
        </div>

        <div class="space-y-3.5 text-xs sm:text-sm text-slate-300 leading-relaxed">
          <div class="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-start gap-3">
            <span class="text-xl shrink-0">🎯</span>
            <div>
              <strong class="text-white block font-bold mb-0.5">1. Động lực Viral từ Collab KOL/KOC</strong>
              Video <em>"Combo điện lạnh"</em> đạt đỉnh <strong>42,000 views</strong> và <strong>1,103 tương tác</strong> (chiếm 24% tổng view toàn quý). Điều này khẳng định người dùng TikTok phản hồi cực kỳ tích cực với định dạng chuyên gia / thợ nghề review thực chiến.
            </div>
          </div>

          <div class="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-start gap-3">
            <span class="text-xl shrink-0">🛒</span>
            <div>
              <strong class="text-white block font-bold mb-0.5">2. Vai trò của Giới Thiệu Sản Phẩm (75% sản lượng)</strong>
              Mặc dù view trung bình (2,143) không bằng KOL, nhưng đây là nhóm trực tiếp gắn link giỏ hàng TikTok Shop, cung cấp thông số kỹ thuật đầy đủ để khách hàng chốt đơn.
            </div>
          </div>

          <div class="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-start gap-3">
            <span class="text-xl shrink-0">⚠️</span>
            <div>
              <strong class="text-white block font-bold mb-0.5">3. Cần thu hẹp định dạng Banner Sản Phẩm</strong>
              Video dạng tĩnh / banner chỉ đạt trung bình 1,010 views và 5.7 likes (kém hấp dẫn trên nền tảng video ngắn). Đề xuất giảm tỷ trọng xuống còn tối đa 5% trong Tháng 11.
            </div>
          </div>
        </div>
      </div>

      <!-- Box 2: Kế Hoạch Phân Bổ Nội Dung Tháng 11 (5 Cols) -->
      <div class="lg:col-span-5 glass-card p-6 rounded-3xl space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800/80 pb-3">
          <h3 class="text-base font-extrabold text-white flex items-center gap-2">
            <span>📅</span> Phân Bổ Nội Dung Tháng 11
          </h3>
          <span class="text-xs px-2.5 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold font-mono">
            Mục tiêu: 24 Video
          </span>
        </div>

        <div class="space-y-3">
          <div class="p-3 rounded-2xl bg-slate-900/90 border border-slate-800/80 flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <span class="w-3 h-3 rounded-full bg-blue-500 shrink-0"></span>
              <div>
                <span class="text-xs sm:text-sm font-bold text-white block">Giới thiệu sản phẩm</span>
                <span class="text-[11px] text-slate-400">Gắn giỏ hàng TikTok Shop</span>
              </div>
            </div>
            <div class="text-right">
              <span class="text-sm font-black text-white font-mono">70%</span>
              <span class="text-xs text-slate-400 block font-mono">17 Video</span>
            </div>
          </div>

          <div class="p-3 rounded-2xl bg-slate-900/90 border border-slate-800/80 flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <span class="w-3 h-3 rounded-full bg-amber-500 shrink-0"></span>
              <div>
                <span class="text-xs sm:text-sm font-bold text-white block">Review / So sánh máy</span>
                <span class="text-[11px] text-slate-400">Test tải nặng, thực chiến</span>
              </div>
            </div>
            <div class="text-right">
              <span class="text-sm font-black text-white font-mono">15%</span>
              <span class="text-xs text-slate-400 block font-mono">4 Video</span>
            </div>
          </div>

          <div class="p-3 rounded-2xl bg-slate-900/90 border border-slate-800/80 flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <span class="w-3 h-3 rounded-full bg-emerald-500 shrink-0"></span>
              <div>
                <span class="text-xs sm:text-sm font-bold text-white block">Hướng dẫn sử dụng</span>
                <span class="text-[11px] text-slate-400">Mẹo bảo dưỡng & CSKH</span>
              </div>
            </div>
            <div class="text-right">
              <span class="text-sm font-black text-white font-mono">10%</span>
              <span class="text-xs text-slate-400 block font-mono">2 Video</span>
            </div>
          </div>

          <div class="p-3 rounded-2xl bg-slate-900/90 border border-slate-800/80 flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <span class="w-3 h-3 rounded-full bg-purple-500 shrink-0"></span>
              <div>
                <span class="text-xs sm:text-sm font-bold text-white block">Banner sản phẩm</span>
                <span class="text-[11px] text-slate-400">Flash Sale & Mini-game</span>
              </div>
            </div>
            <div class="text-right">
              <span class="text-sm font-black text-white font-mono">5%</span>
              <span class="text-xs text-slate-400 block font-mono">1 Video</span>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- ================= 6. MASTER VIDEO EXPLORER (SEARCH & FILTER) ================= -->
    <section class="glass-card rounded-3xl p-5 sm:p-6 space-y-4">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
        <div>
          <h3 class="text-base sm:text-lg font-black text-white flex items-center gap-2">
            <span>📑</span> Danh Sách Chi Tiết 68 Video TikTok Q3
          </h3>
          <p class="text-xs text-slate-400">Tìm kiếm, lọc theo nhóm nội dung, sắp xếp lượt xem và mở xem video TikTok trực tiếp</p>
        </div>

        <!-- Search Box & Filter Controls -->
        <div class="flex flex-wrap items-center gap-2.5 w-full md:w-auto">
          <!-- Search input -->
          <div class="relative flex-1 sm:w-64">
            <input type="text" id="video-search-input" oninput="renderVideosTable()" placeholder="Tìm tên video / sản phẩm..." class="w-full bg-slate-900 border border-slate-700/80 text-white rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:border-[#00F2FE] placeholder-slate-500 font-medium">
            <span class="absolute right-2.5 top-2 text-xs text-slate-500 pointer-events-none">🔍</span>
          </div>

          <!-- Category Select -->
          <select id="video-category-select" onchange="renderVideosTable()" class="bg-slate-900 border border-slate-700/80 text-white rounded-xl px-2.5 py-1.5 text-xs focus:outline-none focus:border-[#00F2FE] font-medium">
            <option value="ALL">Tất cả nhóm</option>
            <option value="Giới thiệu sản phẩm">Giới thiệu sản phẩm (51)</option>
            <option value="Collab KOL/KOC">Collab KOL/KOC (7)</option>
            <option value="Review / trải nghiệm thực tế">Review / trải nghiệm (3)</option>
            <option value="Hướng dẫn sử dụng">Hướng dẫn sử dụng (4)</option>
            <option value="Banner sản phẩm">Banner sản phẩm (3)</option>
          </select>

          <!-- Export CSV button -->
          <button onclick="exportVideosToCSV()" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-1">
            <span>📥</span> <span>Tải CSV</span>
          </button>
        </div>
      </div>

      <!-- Videos Table -->
      <div class="overflow-x-auto max-h-[550px] overflow-y-auto border border-slate-800/80 rounded-2xl">
        <table class="w-full text-left text-xs sm:text-sm text-slate-300 border-collapse">
          <thead class="bg-slate-900/95 sticky top-0 z-20 text-slate-400 uppercase font-mono text-[11px] border-b border-slate-800 backdrop-blur-md">
            <tr>
              <th class="p-3 w-12 text-center">STT</th>
              <th class="p-3 w-24">Ngày Đăng</th>
              <th class="p-3 w-24 text-center">Tháng</th>
              <th class="p-3 min-w-[240px]">Tên / Chủ Đề Video</th>
              <th class="p-3 w-40">Nhóm Nội Dung</th>
              <th class="p-3 w-28 text-center">Thời Lượng</th>
              <th class="p-3 w-28 text-right cursor-pointer hover:text-white" onclick="changeSort('views')">
                Lượt Xem <span id="sort-icon-views">▼</span>
              </th>
              <th class="p-3 w-24 text-right cursor-pointer hover:text-white" onclick="changeSort('likes')">
                Lượt Thích <span id="sort-icon-likes"></span>
              </th>
              <th class="p-3 w-20 text-right cursor-pointer hover:text-white" onclick="changeSort('comments')">
                Cmt <span id="sort-icon-comments"></span>
              </th>
              <th class="p-3 w-24 text-right cursor-pointer hover:text-white" onclick="changeSort('rate')">
                Tỷ Lệ TT <span id="sort-icon-rate"></span>
              </th>
              <th class="p-3 w-24 text-center">TikTok</th>
            </tr>
          </thead>
          <tbody id="videos-table-body" class="divide-y divide-slate-800/60 font-medium">
            <!-- Populated by JS -->
          </tbody>
        </table>
      </div>

      <div class="flex items-center justify-between text-xs text-slate-400 pt-2 px-1">
        <span id="table-count-label">Hiển thị 68 / 68 video</span>
        <span class="font-mono text-[11px]">Dữ liệu chuẩn hóa từ TikTok Analytics Cko Store</span>
      </div>
    </section>

  </main>

  <!-- ================= FOOTER ================= -->
  <footer class="mt-12 border-t border-slate-800/80 bg-[#0B0F17] py-6 px-4 text-center text-xs text-slate-500 space-y-1">
    <p>🐱 <strong>Xu Xu</strong> - Trợ Lý Ảo Marketing • Hệ Thống Báo Cáo Hiệu Quả Nội Dung TikTok Cko Store</p>
    <p class="text-[11px] text-slate-600">Được đồng bộ tự động từ Google Sheet gốc • Phát triển cho King Blue / Cko Store Media Team</p>
  </footer>

  <!-- ================= TOAST NOTIFICATION ================= -->
  <div id="toast" class="fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 pointer-events-none">
    <div class="bg-slate-900 border border-emerald-500/40 text-emerald-300 px-4 py-3 rounded-2xl shadow-2xl flex items-center gap-2.5 text-xs font-bold">
      <span class="text-base">✅</span>
      <span id="toast-msg">Đã sao chép báo cáo tóm tắt!</span>
    </div>
  </div>

  <!-- SCRIPT DATA & APP ENGINE -->
  <script>
    const DATASET = {json_data_str};

    let currentFilterMonth = 'ALL';
    let currentSortField = 'views';
    let currentSortAsc = false;
    let monthlyChart = null;
    let shareChart = null;

    window.addEventListener("DOMContentLoaded", () => {{
      renderKpis();
      initCharts();
      renderTopVideosGrid();
      renderVideosTable();
    }});

    // Filter by Month
    function setFilterMonth(month) {{
      currentFilterMonth = month;
      
      // Update buttons style
      document.querySelectorAll('.filter-month-btn').forEach(btn => {{
        btn.className = "filter-month-btn px-3 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition";
      }});
      
      const activeBtn = document.getElementById('filter-btn-' + month);
      if (activeBtn) {{
        activeBtn.className = "filter-month-btn px-3.5 py-2 rounded-xl text-xs font-extrabold transition bg-gradient-to-r from-[#00F2FE] to-[#FE2C55] text-slate-950 shadow-md";
      }}

      renderKpis();
      renderTopVideosGrid();
      renderVideosTable();
    }}

    // Calculate & Render KPI Cards
    function renderKpis() {{
      const vids = getFilteredVideos();
      const totalVids = vids.length;
      const totalViews = vids.reduce((s, v) => s + v.views, 0);
      const totalLikes = vids.reduce((s, v) => s + v.likes, 0);
      const totalComments = vids.reduce((s, v) => s + v.comments, 0);
      const avgViews = totalVids > 0 ? Math.round(totalViews / totalVids) : 0;
      const totalEng = totalLikes + totalComments;
      const engRate = totalViews > 0 ? (totalEng / totalViews * 100).toFixed(2) : "0.00";

      document.getElementById('kpi-videos').textContent = totalVids;
      document.getElementById('kpi-views').textContent = totalViews.toLocaleString('vi-VN');
      document.getElementById('kpi-likes').textContent = totalLikes.toLocaleString('vi-VN');
      document.getElementById('kpi-comments').textContent = totalComments.toLocaleString('vi-VN');
      document.getElementById('kpi-avg-views').textContent = avgViews.toLocaleString('vi-VN');
      document.getElementById('kpi-eng-rate').textContent = engRate + '%';

      const subVideos = document.getElementById('kpi-videos-sub');
      const subViews = document.getElementById('kpi-views-sub');
      const subLikes = document.getElementById('kpi-likes-sub');

      if (currentFilterMonth === 'ALL') {{
        subVideos.innerHTML = `<span>22.7</span> <span>video / tháng</span>`;
        subViews.innerHTML = `<span>▲ +26.3%</span> <span class="text-slate-500 font-normal">T9 vs T8</span>`;
        subLikes.innerHTML = `<span>▲ +365.4%</span> <span class="text-slate-500 font-normal">bùng nổ T9</span>`;
      }} else if (currentFilterMonth === 'Tháng 7') {{
        subVideos.innerHTML = `<span>36.8%</span> <span>tổng video Q3</span>`;
        subViews.innerHTML = `<span>28.6%</span> <span class="text-slate-500 font-normal">views Q3</span>`;
        subLikes.innerHTML = `<span>368 likes</span> <span class="text-slate-500 font-normal">khởi động</span>`;
      }} else if (currentFilterMonth === 'Tháng 8') {{
        subVideos.innerHTML = `<span>32.4%</span> <span>tổng video Q3</span>`;
        subViews.innerHTML = `<span>▲ +10.3%</span> <span class="text-slate-500 font-normal">vs Tháng 7</span>`;
        subLikes.innerHTML = `<span>▼ -20.6%</span> <span class="text-slate-500 font-normal">vs Tháng 7</span>`;
      }} else if (currentFilterMonth === 'Tháng 9') {{
        subVideos.innerHTML = `<span>30.8%</span> <span>tổng video Q3</span>`;
        subViews.innerHTML = `<span>▲ +26.3%</span> <span class="text-slate-500 font-normal">vs Tháng 8</span>`;
        subLikes.innerHTML = `<span>▲ +365%</span> <span class="text-slate-500 font-normal">KOL đỉnh cao</span>`;
      }}
    }}

    function getFilteredVideos() {{
      if (currentFilterMonth === 'ALL') return DATASET.videos;
      return DATASET.videos.filter(v => v.month === currentFilterMonth);
    }}

    // Render Top Videos Grid
    function renderTopVideosGrid() {{
      const container = document.getElementById('top-videos-grid');
      container.innerHTML = "";
      
      const vids = getFilteredVideos();
      const topList = [...vids].sort((a, b) => b.views - a.views).slice(0, 6);

      topList.forEach((v, idx) => {{
        const card = document.createElement('a');
        card.href = v.url || "https://www.tiktok.com/@cko_store";
        card.target = "_blank";
        card.className = "glass-card glass-card-hover p-4 rounded-2xl block space-y-3 transition duration-200 group relative border border-slate-800";
        
        let medal = "";
        let medalBadge = "";
        if (idx === 0) {{
          medal = "🥇 TOP 1 VIRAL";
          medalBadge = "bg-amber-500/20 text-amber-300 border-amber-500/30";
        }} else if (idx === 1) {{
          medal = "🥈 TOP 2";
          medalBadge = "bg-slate-400/20 text-slate-300 border-slate-400/30";
        }} else if (idx === 2) {{
          medal = "🥉 TOP 3";
          medalBadge = "bg-orange-500/20 text-orange-300 border-orange-500/30";
        }} else {{
          medal = `#${{idx + 1}} Trending`;
          medalBadge = "bg-slate-800 text-slate-400 border-slate-700";
        }}

        card.innerHTML = `
          <div class="flex items-center justify-between gap-2">
            <span class="text-[10px] font-mono font-black px-2 py-0.5 rounded-full border ${{medalBadge}}">
              ${{medal}}
            </span>
            <span class="text-[11px] text-slate-400 font-mono">${{v.month}} • ${{v.date}}</span>
          </div>

          <div>
            <h4 class="font-extrabold text-white text-sm line-clamp-2 group-hover:text-[#00F2FE] transition leading-snug">
              ${{v.title}}
            </h4>
            <div class="mt-1 flex items-center gap-1.5 text-xs text-slate-400">
              <span class="px-2 py-0.5 rounded bg-slate-800/80 text-[10px] text-slate-300 border border-slate-700/60 font-medium">${{v.category}}</span>
              <span class="text-slate-500">•</span>
              <span class="text-slate-400 text-[11px]">${{v.duration}}</span>
            </div>
          </div>

          <div class="pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <div class="flex items-center gap-3">
              <span class="font-mono font-black text-white text-sm flex items-center gap-1">
                <span class="text-[#00F2FE]">👁️</span> ${{v.views.toLocaleString('vi-VN')}}
              </span>
              <span class="font-mono font-bold text-slate-300 flex items-center gap-1">
                <span class="text-[#FE2C55]">❤️</span> ${{v.likes.toLocaleString('vi-VN')}}
              </span>
            </div>
            <span class="text-[11px] text-emerald-400 font-mono font-bold">
              ${{v.engagement_rate}}% TT
            </span>
          </div>
        `;

        container.appendChild(card);
      }});
    }}

    // Render Main Videos Table
    function renderVideosTable() {{
      const tbody = document.getElementById('videos-table-body');
      tbody.innerHTML = "";

      const query = (document.getElementById('video-search-input')?.value || "").toLowerCase().trim();
      const catFilter = document.getElementById('video-category-select')?.value || "ALL";

      let list = getFilteredVideos();

      if (catFilter !== 'ALL') {{
        list = list.filter(v => v.category === catFilter);
      }}

      if (query) {{
        list = list.filter(v => v.title.toLowerCase().includes(query) || v.category.toLowerCase().includes(query));
      }}

      // Sorting
      list.sort((a, b) => {{
        let valA, valB;
        if (currentSortField === 'views') {{ valA = a.views; valB = b.views; }}
        else if (currentSortField === 'likes') {{ valA = a.likes; valB = b.likes; }}
        else if (currentSortField === 'comments') {{ valA = a.comments; valB = b.comments; }}
        else if (currentSortField === 'rate') {{ valA = a.engagement_rate; valB = b.engagement_rate; }}
        else {{ valA = a.id; valB = b.id; }}

        return currentSortAsc ? valA - valB : valB - valA;
      }});

      document.getElementById('table-count-label').textContent = `Hiển thị ${{list.length}} / 68 video`;

      list.forEach((v, idx) => {{
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-800/40 transition group";

        let catBadge = "bg-slate-800 text-slate-300 border-slate-700";
        if (v.category === 'Collab KOL/KOC') catBadge = "bg-[#FE2C55]/15 text-[#FE2C55] border-[#FE2C55]/30 font-bold";
        else if (v.category === 'Giới thiệu sản phẩm') catBadge = "bg-blue-500/10 text-blue-400 border-blue-500/20";
        else if (v.category === 'Review / trải nghiệm thực tế') catBadge = "bg-amber-500/10 text-amber-400 border-amber-500/20";
        else if (v.category === 'Hướng dẫn sử dụng') catBadge = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
        else if (v.category === 'Banner sản phẩm') catBadge = "bg-purple-500/10 text-purple-400 border-purple-500/20";

        tr.innerHTML = `
          <td class="p-3 text-center font-mono text-slate-500 text-xs">${{idx + 1}}</td>
          <td class="p-3 font-mono text-xs text-slate-300">${{v.date}}</td>
          <td class="p-3 text-center">
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
              ${{v.month}}
            </span>
          </td>
          <td class="p-3 font-medium text-white group-hover:text-[#00F2FE] transition">
            <a href="${{v.url || '#'}}" target="_blank" class="hover:underline flex items-center gap-1.5">
              <span>${{v.title}}</span>
              ${{v.views >= 10000 ? '<span class="text-[10px] px-1.5 py-0.2 rounded bg-amber-500/20 text-amber-300 font-bold border border-amber-500/30">🔥 Viral</span>' : ''}}
            </a>
          </td>
          <td class="p-3">
            <span class="px-2.5 py-1 rounded-md text-[11px] border ${{catBadge}} inline-block">
              ${{v.category}}
            </span>
          </td>
          <td class="p-3 text-center font-mono text-xs text-slate-400">${{v.duration}}</td>
          <td class="p-3 text-right font-mono font-bold text-white">${{v.views.toLocaleString('vi-VN')}}</td>
          <td class="p-3 text-right font-mono text-slate-300">${{v.likes.toLocaleString('vi-VN')}}</td>
          <td class="p-3 text-right font-mono text-slate-400">${{v.comments}}</td>
          <td class="p-3 text-right font-mono font-bold ${{v.engagement_rate >= 2 ? 'text-emerald-400' : 'text-slate-400'}}">
            ${{v.engagement_rate}}%
          </td>
          <td class="p-3 text-center">
            <a href="${{v.url || '#'}}" target="_blank" class="text-xs px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-[#FE2C55] text-slate-300 hover:text-white transition font-bold inline-flex items-center gap-1">
              <span>▶</span> Xem
            </a>
          </td>
        `;

        tbody.appendChild(tr);
      }});
    }}

    function changeSort(field) {{
      if (currentSortField === field) {{
        currentSortAsc = !currentSortAsc;
      }} else {{
        currentSortField = field;
        currentSortAsc = false;
      }}
      ['views', 'likes', 'comments', 'rate'].forEach(f => {{
        const el = document.getElementById('sort-icon-' + f);
        if (el) el.textContent = f === currentSortField ? (currentSortAsc ? '▲' : '▼') : '';
      }});
      renderVideosTable();
    }}

    // Export Table to CSV
    function exportVideosToCSV() {{
      const vids = getFilteredVideos();
      const headers = ["STT", "Tháng", "Ngày đăng", "Tên video", "Nhóm nội dung", "Thời lượng", "Lượt xem", "Lượt thích", "Bình luận", "Tỷ lệ tương tác (%)", "Link TikTok"];
      
      const rows = vids.map((v, i) => [
        i + 1,
        v.month,
        v.date,
        `"${{v.title.replace(/"/g, '""')}}"`,
        `"${{v.category}}"`,
        `"${{v.duration}}"`,
        v.views,
        v.likes,
        v.comments,
        v.engagement_rate,
        v.url
      ]);

      const csvContent = "\uFEFF" + [headers.join(","), ...rows.map(r => r.join(","))].join("\\n");
      const blob = new Blob([csvContent], {{ type: "text/csv;charset=utf-8;" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `Bao_Cao_TikTok_Cko_Store_${{currentFilterMonth.replace(/\\s/g, '_')}}.csv`;
      a.click();
      URL.revokeObjectURL(url);
      showToast("Đã tải xuống file CSV!");
    }}

    // Copy Executive Summary for BOD
    function copyExecutiveSummary() {{
      const text = `📊 BÁO CÁO TỔNG HỢP HIỆU QUẢ NỘI DUNG TIKTOK CKO STORE (Q3/2026)
Kính gửi Ban Giám Đốc,

1️⃣ CHỈ SỐ TỔNG QUAN QUÝ 3 (THÁNG 7 - THÁNG 9):
• Tổng số video đã đăng: 68 video (TB: 22.7 video/tháng)
• Tổng lượt xem (Views): 173,762 lượt xem
• Tổng lượt thích (Likes): 2,019 lượt thích
• Tổng bình luận: 62 bình luận
• Tỷ lệ tương tác chung: 1.20%

2️⃣ TĂNG TRƯỞNG THEO THÁNG (MOM):
• Tháng 7: 25 video | 49,699 views | 368 likes
• Tháng 8: 22 video | 54,824 views (+10.3%) | 292 likes
• Tháng 9: 21 video | 69,239 views (+26.3%) | 1,359 likes (+365.4% bùng nổ!)

3️⃣ HIỆU QUẢ THEO NHÓM NỘI DUNG:
• Collab KOL/KOC: Đạt hiệu quả cao nhất với 7,152 views/video (gấp 3.3 lần trung bình kênh), mang lại 59% tổng lượng like toàn quý. Video đỉnh: "Combo điện lạnh" (42k views).
• Giới thiệu sản phẩm: Chiếm 75% sản lượng (51 video), 109,269 views (62.9%), giữ vai trò xương sống gắn giỏ hàng TikTok Shop chốt đơn.
• Review thực tế: Đạt tỷ lệ tương tác cao (24.7 like/video).
• Banner sản phẩm: Hiệu quả thấp nhất (1,010 views/video), đề xuất thu hẹp.

4️⃣ ĐỀ XUẤT PHÂN BỔ THÁNG 11 (24 VIDEO):
• Giới thiệu sản phẩm: 70% (17 video) - Duy trì gắn giỏ hàng TikTok Shop
• Review / so sánh: 15% (4 video) - Test tải thực chiến kích thích chuyển đổi
• Hướng dẫn sử dụng: 10% (2 video) - Tăng trải nghiệm sau mua & uy tín
• Banner sản phẩm: 5% (1 video) - Flash Sale`;

      navigator.clipboard.writeText(text).then(() => {{
        showToast("Đã sao chép tóm tắt gửi BOD thành công!");
      }});
    }}

    function showToast(msg) {{
      const t = document.getElementById('toast');
      const m = document.getElementById('toast-msg');
      if (m) m.textContent = msg;
      t.classList.remove('translate-y-20', 'opacity-0');
      t.classList.add('translate-y-0', 'opacity-100');
      setTimeout(() => {{
        t.classList.remove('translate-y-0', 'opacity-100');
        t.classList.add('translate-y-20', 'opacity-0');
      }}, 3000);
    }}

    // Init Chart.js Visualizations
    function initCharts() {{
      // Chart 1: Monthly Trend (Dual-axis)
      const ctx1 = document.getElementById('monthlyTrendChart').getContext('2d');
      monthlyChart = new Chart(ctx1, {{
        type: 'bar',
        data: {{
          labels: ['Tháng 7', 'Tháng 8', 'Tháng 9'],
          datasets: [
            {{
              label: 'Lượt Xem (Views)',
              data: [49699, 54824, 69239],
              backgroundColor: 'rgba(0, 242, 254, 0.7)',
              borderColor: '#00F2FE',
              borderWidth: 1.5,
              borderRadius: 8,
              yAxisID: 'y'
            }},
            {{
              label: 'Lượt Thích (Likes)',
              data: [368, 292, 1359],
              type: 'line',
              borderColor: '#FE2C55',
              backgroundColor: 'rgba(254, 44, 85, 0.2)',
              borderWidth: 3,
              pointBackgroundColor: '#FE2C55',
              pointRadius: 6,
              tension: 0.35,
              yAxisID: 'y1'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              labels: {{ color: '#94A3B8', font: {{ family: 'Inter', weight: '600', size: 11 }} }}
            }},
            tooltip: {{
              backgroundColor: '#0F172A',
              titleColor: '#fff',
              bodyColor: '#E2E8F0',
              borderColor: '#334155',
              borderWidth: 1,
              padding: 10,
              boxPadding: 4
            }}
          }},
          scales: {{
            x: {{
              grid: {{ display: false }},
              ticks: {{ color: '#94A3B8', font: {{ family: 'Inter', weight: '600' }} }}
            }},
            y: {{
              type: 'linear',
              position: 'left',
              grid: {{ color: 'rgba(255,255,255,0.06)' }},
              ticks: {{
                color: '#00F2FE',
                callback: v => (v / 1000) + 'k views'
              }}
            }},
            y1: {{
              type: 'linear',
              position: 'right',
              grid: {{ display: false }},
              ticks: {{
                color: '#FE2C55',
                callback: v => v + ' likes'
              }}
            }}
          }}
        }}
      }});

      // Chart 2: Category Views Share (Donut)
      const ctx2 = document.getElementById('categoryShareChart').getContext('2d');
      shareChart = new Chart(ctx2, {{
        type: 'doughnut',
        data: {{
          labels: [
            'Giới thiệu sản phẩm (62.9%)',
            'Collab KOL/KOC (28.8%)',
            'Hướng dẫn sử dụng (3.6%)',
            'Review / Trải nghiệm (3.0%)',
            'Banner sản phẩm (1.7%)'
          ],
          datasets: [{{
            data: [109269, 50061, 6188, 5215, 3029],
            backgroundColor: [
              '#3B82F6',
              '#FE2C55',
              '#10B981',
              '#F59E0B',
              '#A855F7'
            ],
            borderColor: '#0B0F17',
            borderWidth: 3
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: 'bottom',
              labels: {{
                color: '#94A3B8',
                font: {{ family: 'Inter', size: 11, weight: '500' }},
                boxWidth: 12,
                padding: 12
              }}
            }},
            tooltip: {{
              backgroundColor: '#0F172A',
              borderColor: '#334155',
              borderWidth: 1,
              callbacks: {{
                label: function(ctx) {{
                  const v = ctx.raw || 0;
                  return ' ' + ctx.label + ': ' + v.toLocaleString('vi-VN') + ' views';
                }}
              }}
            }}
          }},
          cutout: '65%'
        }}
      }});
    }}
  </script>
</body>
</html>
'''

with open('dashboard_tiktok_cko.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Generated dashboard_tiktok_cko.html successfully!")

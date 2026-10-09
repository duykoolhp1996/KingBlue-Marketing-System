import json

with open('all_sheets_data.json', 'r', encoding='utf-8') as f:
    sheets_data = json.load(f)

json_data_str = json.dumps(sheets_data, ensure_ascii=False)

html_template = f'''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>King Blue - Hệ Thống Báo Cáo & Quản Trị Marketing</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    .font-mono {{ font-family: 'JetBrains+Mono', monospace; }}
    .hide-scrollbar::-webkit-scrollbar {{ display: none; }}
    .hide-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
    .tab-sheet-active {{
      background-color: #1A365D !important;
      color: #ffffff !important;
      font-weight: 800 !important;
      border-color: #1A365D !important;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col">

  <!-- ================= TOP APP HEADER ================= -->
  <header class="bg-[#1A365D] text-white border-b-4 border-amber-400 sticky top-0 z-50 shadow-md">
    <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-2.5 sm:py-3 flex items-center justify-between gap-2 sm:gap-4">
      
      <div class="flex items-center gap-2.5 sm:gap-3 min-w-0">
        <div class="w-9 h-9 sm:w-11 sm:h-11 rounded-xl bg-amber-400 text-slate-900 flex items-center justify-center font-black text-lg sm:text-xl shadow-inner shrink-0">
          KB
        </div>
        <div class="min-w-0">
          <div class="flex items-center gap-1.5 sm:gap-2">
            <h1 class="text-sm sm:text-lg font-black tracking-tight truncate">KING BLUE MARKETING</h1>
            <span class="text-[10px] sm:text-xs bg-amber-400 text-slate-950 font-black px-2 py-0.5 rounded-full shrink-0">PRO</span>
          </div>
          <p class="text-blue-200 text-[11px] sm:text-xs truncate hidden xs:block">Hệ Thống Báo Cáo & Quản Trị Marketing</p>
        </div>
      </div>

      <!-- Quick Action Links -->
      <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
        <a href="https://docs.google.com/spreadsheets/d/1_kID0uhutS6Ky_zpB2yW_AQXN2aUKKCKo_6tqZL1kbo/edit" target="_blank" class="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-black text-xs px-2.5 sm:px-3.5 py-1.5 sm:py-2 rounded-xl flex items-center gap-1 transition shadow-xs">
          <span>📊</span> <span class="hidden sm:inline">Google Sheet Gốc</span><span class="sm:hidden">Sheet</span>
        </a>
        <a href="https://github.com/duykoolhp1996/KingBlue-Marketing-System" target="_blank" class="bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold text-xs px-2.5 sm:px-3 py-1.5 sm:py-2 rounded-xl flex items-center gap-1 transition">
          <span>🐙</span> <span class="hidden sm:inline">GitHub</span>
        </a>
      </div>

    </div>
  </header>

  <!-- ================= SECONDARY STICKY NAVIGATION (3 MODES) ================= -->
  <nav class="bg-white border-b border-slate-200 sticky top-[53px] sm:top-[68px] z-40 shadow-xs">
    <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-2 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2">
      
      <!-- Primary Tabs (Horizontal Scroll on Mobile) -->
      <div class="flex items-center gap-1.5 sm:gap-2 overflow-x-auto hide-scrollbar pb-1 sm:pb-0 touch-pan-x shrink-0">
        <button onclick="switchMainAppTab('cards')" id="btn-nav-cards" class="px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-black transition flex items-center gap-1.5 bg-[#1A365D] text-white shadow-xs whitespace-nowrap shrink-0">
          <span>🗂️</span> <span>2. Thẻ Việc Hôm Nay (17h)</span> <span class="bg-emerald-400 text-emerald-950 font-black px-1.5 py-0.5 rounded-full text-[10px]">Tự do</span>
        </button>
        <button onclick="switchMainAppTab('sheets')" id="btn-nav-sheets" class="px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-1.5 text-slate-700 hover:bg-slate-100 border border-transparent whitespace-nowrap shrink-0">
          <span id="icon-lock-sheets">🔒</span> <span>1. Bảng 9 Sheets</span>
        </button>
        <button onclick="switchMainAppTab('submit')" id="btn-nav-submit" class="px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-1.5 text-slate-700 hover:bg-slate-100 border border-transparent whitespace-nowrap shrink-0">
          <span>✍️</span> <span>3. Điền Báo Cáo</span>
        </button>
      </div>

      <!-- Live Clock & User Status / Login Button -->
      <div class="flex items-center justify-between sm:justify-end gap-2 text-xs">
        <button onclick="openLoginModal()" id="btn-open-login" class="bg-amber-400 hover:bg-amber-500 text-slate-950 font-black px-3 py-1.5 rounded-xl text-xs flex items-center gap-1 transition shadow-xs shrink-0">
          <span>🔑</span> Đăng nhập nội bộ
        </button>
        <div id="user-info-bar" class="hidden flex items-center gap-1.5 text-xs truncate">
          <span id="current-user-avatar" class="text-base shrink-0">👔</span>
          <span id="current-user-name" class="font-black text-slate-900 truncate max-w-[130px]"></span>
          <button onclick="handleLogout()" class="text-rose-600 hover:underline font-extrabold text-[11px] shrink-0">(Đăng xuất)</button>
        </div>
        <span class="text-slate-500 font-mono text-[11px] bg-slate-100 px-2.5 py-1 rounded-lg border border-slate-200 shrink-0">
          🕒 <span id="live-clock">--:--:--</span>
        </span>
      </div>

    </div>
  </nav>

  <!-- ================= POPUP ĐĂNG NHẬP NỘI BỘ (CHO TAB 1 & BẢO MẬT) ================= -->
  <div id="modal-login" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs hidden transition-all duration-300">
    <div class="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-100 text-center transform scale-95 transition-all duration-300 animate-in fade-in zoom-in">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div class="flex items-center gap-2">
          <span class="text-2xl">🔒</span>
          <h3 class="text-base font-extrabold text-slate-900 text-left">Đăng Nhập Hệ Thống Nội Bộ</h3>
        </div>
        <button onclick="closeLoginModal()" class="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-sm transition">✕</button>
      </div>

      <div class="mt-3 text-left">
        <p class="text-xs text-slate-600 leading-relaxed bg-amber-50 border border-amber-200 p-2.5 rounded-xl">
          💡 <strong>Tab 2 (Thẻ công việc hôm nay)</strong> được mở tự do không cần mật khẩu. Vui lòng nhập mật khẩu nội bộ để xem <strong>Tab 1 (Bảng tính chi tiết)</strong> hoặc điền báo cáo.
        </p>
      </div>

      <form onsubmit="handleModalPasswordSubmit(event)" class="mt-4 text-left space-y-3">
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Mã PIN / Mật khẩu của bạn:</label>
          <div class="flex gap-2">
            <input type="password" id="modal-login-password" placeholder="Mã PIN 4 số (VD: 8888, 1001...)" class="flex-1 text-sm p-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-sky-500 focus:outline-hidden font-mono tracking-widest bg-slate-50 focus:bg-white transition" />
            <button type="submit" class="px-5 py-3 bg-[#1A365D] hover:bg-blue-900 text-white font-bold text-xs rounded-xl transition shadow-md flex items-center gap-1.5 shrink-0">
              <span>Đăng nhập</span> ➔
            </button>
          </div>
        </div>
      </form>

      <div class="mt-4 pt-3 border-t border-slate-100 text-left">
        <p class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Hoặc chọn nhanh tài khoản nhân sự:</p>
        <div id="modal-quick-users-grid" class="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto pr-1">
          <!-- Populated by JS -->
        </div>
      </div>
    </div>
  </div>

  <!-- ================= NOTIFICATION TOAST ================= -->
  <div id="toast" class="fixed top-24 right-4 z-50 transform transition-all duration-300 translate-y-[-100px] opacity-0 pointer-events-none max-w-md bg-slate-900 text-white p-4 rounded-2xl shadow-2xl border border-slate-700 flex items-start gap-3">
    <span id="toast-icon" class="text-2xl">✅</span>
    <div>
      <h4 id="toast-title" class="text-sm font-bold">Thông báo</h4>
      <p id="toast-desc" class="text-xs text-slate-300 mt-0.5 leading-relaxed"></p>
    </div>
  </div>

  <!-- ================= POPUP THỂ HIỆN HOÀN THÀNH BÁO CÁO ================= -->
  <div id="modal-completion" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs hidden transition-all duration-300">
    <div class="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl border border-slate-100 text-center transform scale-95 transition-all duration-300 animate-in fade-in zoom-in">
      <div class="w-20 h-20 rounded-full bg-emerald-100 text-emerald-600 mx-auto flex items-center justify-center text-4xl shadow-inner mb-4 ring-8 ring-emerald-50">
        🎉
      </div>
      <span class="inline-block px-3 py-1 bg-emerald-100 text-emerald-800 text-[11px] font-extrabold rounded-full uppercase tracking-wider mb-2">
        HỆ THỐNG GHI NHẬN THÀNH CÔNG
      </span>
      <h3 class="text-xl font-extrabold text-slate-900">Báo Cáo Đã Hoàn Thành!</h3>
      <p class="text-xs text-slate-500 mt-1">Hệ thống đã lưu lại <strong class="text-slate-800">báo cáo gần nhất</strong> của bạn trong ngày hôm nay.</p>
      
      <div class="mt-5 bg-slate-50 rounded-2xl p-4 border border-slate-200 text-left text-xs space-y-2.5">
        <div class="flex items-center justify-between pb-2 border-b border-slate-200">
          <span class="text-slate-500 font-medium">Nhân sự nộp:</span>
          <span class="font-bold text-slate-900 flex items-center gap-1.5" id="modal-emp-name"></span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-slate-500 font-medium">Ngày báo cáo:</span>
          <span class="font-bold text-slate-800 font-mono" id="modal-date">05/10/2026</span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-slate-500 font-medium">Giờ nộp (Ghi nhận tự động):</span>
          <span class="font-bold text-sky-800 font-mono text-sm" id="modal-time">17:15:32</span>
        </div>
        <div class="flex items-center justify-between pt-1">
          <span class="text-slate-500 font-medium">Đánh giá hạn nộp:</span>
          <span class="font-bold px-2.5 py-0.5 rounded-md text-[11px]" id="modal-status">
            🟢 Đúng hạn (Trước 17:30)
          </span>
        </div>
      </div>

      <button onclick="closeCompletionModal()" class="mt-6 w-full py-3.5 bg-[#1A365D] hover:bg-blue-900 text-white font-bold text-sm rounded-xl transition shadow-md flex items-center justify-center gap-2">
        <span>✅</span> ĐÃ HIỂU & ĐÓNG LẠI
      </button>
    </div>
  </div>

  <!-- ================= MAIN APP CONTAINER ================= -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

    <!-- ===================================================================== -->
    <!-- CHẾ ĐỘ 1: BẢNG TÍNH THEO TỪNG SHEET (YÊU CẦU ĐĂNG NHẬP NỘI BỘ)         -->
    <!-- ===================================================================== -->
    <section id="section-sheets-explorer" class="hidden space-y-5">
      
      <!-- Top Google Sheets Tabs Bar -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-xs p-3">
        <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-100">
          <span class="text-xs font-extrabold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
            <span>📑</span> CÁC SHEET MARKETING TRONG GOOGLE SPREADSHEET (CLICK ĐỂ XEM BẢNG TƯƠNG ỨNG):
          </span>
          <span class="text-[11px] text-slate-400 hidden sm:inline">Khớp chuẩn thứ tự từng sheet trong Google Sheets</span>
        </div>
        <div class="flex items-center gap-1.5 overflow-x-auto pb-1 hide-scrollbar" id="sheet-tabs-container">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Active Sheet Header & Action Bar -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-xs p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div id="active-sheet-icon" class="w-12 h-12 rounded-xl bg-blue-50 text-blue-900 border border-blue-200 flex items-center justify-center text-2xl font-bold shadow-2xs">
            📄
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h2 id="active-sheet-title" class="text-base font-extrabold text-slate-900">BAO CAO HOM NAY</h2>
              <span id="active-sheet-badge" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-100 text-blue-800 border border-blue-200">
                Sheet 0
              </span>
            </div>
            <p id="active-sheet-desc" class="text-xs text-slate-500 mt-0.5">Bảng Tổng Hợp Chi Tiết Tiến Độ Hàng Ngày Của 7 Nhân Sự Marketing</p>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-2 w-full md:w-auto justify-between md:justify-end">
          <!-- View Toggle: HTML vs Iframe -->
          <div class="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-bold">
            <button onclick="toggleSheetViewFormat('html')" id="btn-format-html" class="px-3 py-1.5 rounded-lg transition bg-white text-blue-900 shadow-2xs flex items-center gap-1">
              <span>📋</span> Bảng Web Đẹp
            </button>
            <button onclick="toggleSheetViewFormat('iframe')" id="btn-format-iframe" class="px-3 py-1.5 rounded-lg transition text-slate-600 hover:text-slate-900 flex items-center gap-1">
              <span>🖥️</span> Nhúng Google Sheet
            </button>
          </div>

          <!-- Direct Google Sheet Link -->
          <a id="active-sheet-direct-link" href="https://docs.google.com/spreadsheets/d/1_kID0uhutS6Ky_zpB2yW_AQXN2aUKKCKo_6tqZL1kbo/edit#gid=187266668" target="_blank" class="px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-xs transition shadow-xs flex items-center gap-1.5">
            <span>🟢</span> Mở Tab Này Trên Sheet
          </a>
        </div>
      </div>

      <!-- Active Sheet Table Body (HTML Mode) -->
      <div id="sheet-html-view-container" class="space-y-4">
        <!-- Rendered dynamically by renderActiveSheetHtml() -->
      </div>

      <!-- Active Sheet Iframe Body (Iframe Mode) -->
      <div id="sheet-iframe-view-container" class="hidden bg-white rounded-2xl border border-slate-200 shadow-sm p-2 overflow-hidden">
        <iframe id="sheet-google-iframe" src="" class="w-full h-[720px] rounded-xl border border-slate-200"></iframe>
      </div>

    </section>

    <!-- ===================================================================== -->
    <!-- CHẾ ĐỘ 2: THẺ CÔNG VIỆC HÔM NAY (17H CHIỀU) - MỞ TỰ DO KHÔNG CẦN ĐĂNG NHẬP -->
    <!-- ===================================================================== -->
    <section id="section-cards-dashboard" class="space-y-6">

      <!-- Manager Header Banner -->
      <div class="bg-gradient-to-r from-[#1A365D] to-[#2B6CB0] rounded-2xl sm:rounded-3xl p-4 sm:p-6 text-white shadow-md flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div class="flex items-center gap-3 sm:gap-4">
          <div class="w-13 h-13 sm:w-16 sm:h-16 rounded-2xl bg-amber-400 text-slate-950 flex items-center justify-center text-2xl sm:text-3xl font-black shadow-md shrink-0">
            👔
          </div>
          <div>
            <div class="flex flex-wrap items-center gap-2">
              <h2 class="text-lg sm:text-2xl font-black">Bảng Điều Hành Tiến Độ Marketing</h2>
              <span class="bg-emerald-400 text-slate-950 font-black text-[11px] px-2.5 py-0.5 rounded-full">MỞ TỰ DO XEM NHANH</span>
            </div>
            <p class="text-blue-100 text-xs sm:text-sm mt-1">Theo dõi 7 nhân sự Marketing • Duyệt tiến độ • Xuất báo cáo tổng hợp gửi Ban Giám Đốc</p>
          </div>
        </div>

        <button onclick="copyExecutiveSummaryReport()" class="w-full md:w-auto bg-amber-400 hover:bg-amber-500 text-slate-950 font-black text-xs sm:text-sm px-5 py-3.5 rounded-xl transition shadow-lg flex items-center justify-center gap-2 active:scale-95">
          <span>📋</span> SAO CHÉP BÁO CÁO TỔNG HỢP (GỬI BAN GIÁM ĐỐC)
        </button>
      </div>

      <!-- Date Filter Bar for Cards Dashboard (Mobile Optimized) -->
      <div class="bg-white p-3.5 sm:p-5 rounded-2xl sm:rounded-3xl border border-slate-200 shadow-xs flex flex-col gap-3">
        <!-- Top Row: Date controls -->
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <!-- 3 Quick Day Buttons -->
          <div class="grid grid-cols-3 sm:flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200">
            <button onclick="jumpManagerDay(-1)" title="Lùi 1 ngày" class="py-2 px-3 text-center hover:bg-white rounded-lg text-slate-700 text-xs sm:text-sm font-bold transition flex items-center justify-center gap-1">
              <span>◀</span> Hôm qua
            </button>
            <button onclick="setManagerToToday()" id="btn-mgr-today" class="py-2 px-3 text-center text-xs sm:text-sm rounded-lg font-black transition bg-blue-700 text-white shadow-2xs flex items-center justify-center gap-1">
              ⭐ Hôm nay
            </button>
            <button onclick="jumpManagerDay(1)" title="Tiến 1 ngày" class="py-2 px-3 text-center hover:bg-white rounded-lg text-slate-700 text-xs sm:text-sm font-bold transition flex items-center justify-center gap-1">
              Ngày mai <span>▶</span>
            </button>
          </div>

          <!-- Date picker & formatted text -->
          <div class="flex flex-wrap items-center gap-2">
            <input type="date" id="mgr-calendar-picker" onchange="onManagerCalendarChange(this.value)" class="flex-1 sm:flex-initial text-xs sm:text-sm font-bold text-slate-800 bg-white border border-slate-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-sky-500 focus:outline-hidden shadow-2xs cursor-pointer min-h-[42px]" />
            <span id="mgr-selected-date-display" class="flex-1 sm:flex-initial text-xs sm:text-sm font-black text-blue-900 bg-blue-50 border border-blue-200 px-3 py-2 rounded-xl flex items-center justify-center gap-1.5 min-h-[42px]">
              <span>🗓️</span> <span id="mgr-date-text">Thứ Hai, 05/10/2026</span>
            </span>
          </div>
        </div>

        <!-- Quick Day Chips Row -->
        <div class="flex flex-wrap items-center gap-1.5 pt-2 border-t border-slate-100">
          <span class="text-[11px] font-black text-slate-500 uppercase tracking-wider mr-1">Các ngày có báo cáo:</span>
          <div id="mgr-quick-date-chips" class="flex flex-wrap items-center gap-1.5">
            <!-- Populated dynamically via JS -->
          </div>
        </div>

        <!-- Bottom Row: KPIs & Live Auto-Sync Status -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 pt-2 border-t border-slate-100 items-center">
          <div class="bg-emerald-50 text-emerald-800 border border-emerald-200 px-3 py-2 rounded-xl font-black text-xs sm:text-sm text-center flex items-center justify-center gap-1.5">
            <span>✅ Đã nộp:</span> <span id="m-kpi-sub" class="text-emerald-900 font-black">6 / 7 (86%)</span>
          </div>
          <div class="bg-amber-50 text-amber-800 border border-amber-200 px-3 py-2 rounded-xl font-black text-xs sm:text-sm text-center flex items-center justify-center gap-1.5">
            <span>⚠️ Khó khăn:</span> <span id="m-kpi-diff" class="text-amber-900 font-black">0 Vấn đề</span>
          </div>
          <div class="flex items-center gap-1.5 justify-center sm:justify-end">
            <span id="live-sync-indicator" onclick="autoSyncLiveGoogleSheets(false)" title="Nhấp để đồng bộ ngay từ Google Sheets" class="cursor-pointer bg-emerald-100 hover:bg-emerald-200 text-emerald-950 border border-emerald-300 px-3 py-2 rounded-xl font-black text-xs flex items-center gap-1.5 shadow-2xs transition">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>🟢 Auto Live Sync</span>
            </span>
            <button onclick="autoSyncLiveGoogleSheets(false)" title="Làm mới số liệu từ Google Sheets" class="p-2 bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-300 rounded-xl font-bold transition shadow-2xs">
              🔄
            </button>
          </div>
        </div>
      </div>

      <!-- 7 Visual Task Cards Grid -->
      <div id="mgr-cards-container" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        <!-- Populated by JS -->
      </div>

      <!-- Executive Report Preview Box -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
        <div class="flex items-center justify-between pb-3 border-b border-slate-200 mb-3">
          <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
            <span>👑</span> Bản Xem Trước Báo Cáo Gửi Ban Giám Đốc (Marketing Manager Export)
          </h3>
          <button onclick="copyExecutiveSummaryReport()" class="text-xs font-bold text-sky-700 hover:text-sky-800 flex items-center gap-1">
            <span>📋</span> Sao chép văn bản
          </button>
        </div>
        <pre id="executive-report-text" class="bg-slate-900 text-emerald-400 p-4 rounded-xl text-xs font-mono whitespace-pre-wrap leading-relaxed overflow-x-auto"></pre>
      </div>

    </section>

    <!-- ===================================================================== -->
    <!-- CHẾ ĐỘ 3: KHÔNG GIAN ĐIỀN BÁO CÁO CÁ NHÂN (NHÂN SỰ MARKETING)          -->
    <!-- ===================================================================== -->
    <section id="section-personal-submit" class="hidden space-y-6">

      <!-- Login Box (Show when unauthenticated) -->
      <div id="submit-login-box" class="max-w-2xl mx-auto bg-white rounded-3xl border border-slate-200 shadow-lg p-6 sm:p-8 text-center space-y-6">
        <div class="w-16 h-16 rounded-2xl bg-blue-100 text-blue-900 mx-auto flex items-center justify-center text-3xl font-extrabold shadow-inner">
          🔐
        </div>
        <div>
          <h3 class="text-xl font-bold text-slate-900">Đăng Nhập Điền Báo Cáo Cá Nhân</h3>
          <p class="text-xs text-slate-500 mt-1">Chọn tài khoản của bạn hoặc nhập mã PIN bí mật được cấp để vào form nộp</p>
        </div>

        <!-- Quick 1-Click Select User Grid -->
        <div class="text-left space-y-2">
          <label class="block text-xs font-bold text-slate-700">Chọn nhanh tài khoản của bạn:</label>
          <div id="quick-users-grid" class="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-64 overflow-y-auto pr-1">
            <!-- Populated by JS -->
          </div>
        </div>

        <div class="relative flex py-2 items-center">
          <div class="grow border-t border-slate-200"></div>
          <span class="shrink mx-4 text-xs font-bold text-slate-400 uppercase">Hoặc nhập mật khẩu</span>
          <div class="grow border-t border-slate-200"></div>
        </div>

        <!-- Password Only Input -->
        <form onsubmit="handlePasswordOnlySubmit(event)" class="max-w-sm mx-auto flex gap-2">
          <input type="password" id="login-password" placeholder="Nhập mã PIN hoặc mật khẩu..." class="flex-1 text-sm p-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-sky-500 focus:outline-hidden font-mono tracking-widest bg-slate-50 focus:bg-white transition" />
          <button type="submit" class="px-5 py-3 bg-[#1A365D] hover:bg-blue-900 text-white font-bold text-xs rounded-xl transition shadow flex items-center gap-1.5 shrink-0">
            <span>Vào</span> ➔
          </button>
        </form>
      </div>

      <!-- Submission Form Box (Show when authenticated) -->
      <div id="submit-form-box" class="hidden max-w-3xl mx-auto bg-white rounded-3xl border border-slate-200 shadow-md p-6 sm:p-8 space-y-6">
        
        <!-- User Info Header -->
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-200 gap-3">
          <div class="flex items-center gap-3">
            <div id="emp-avatar" class="w-14 h-14 rounded-2xl bg-blue-100 text-blue-900 flex items-center justify-center text-3xl font-extrabold shadow-inner">
              ✍️
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h3 id="emp-name" class="text-lg font-bold text-slate-900">Võ Thị Hoài Thương</h3>
                <span id="emp-group" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-100 text-blue-800">Content</span>
              </div>
              <p id="emp-role" class="text-xs text-slate-500">Content Marketing & SEO Fanpage/Website</p>
            </div>
          </div>

          <div class="text-right">
            <span class="text-xs text-slate-500 block">Tab lưu trữ:</span>
            <span id="emp-tab-name" class="text-xs font-mono font-bold text-emerald-800 bg-emerald-50 px-2 py-1 rounded-lg border border-emerald-200 inline-block mt-0.5">
              Hoai Thuong - Content
            </span>
          </div>
        </div>

        <!-- Form Body -->
        <form onsubmit="handleEmployeeSubmit(event)" class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">📅 Ngày báo cáo:</label>
              <input type="text" id="emp-form-date" value="05/10/2026" class="w-full text-xs font-mono font-bold p-3 rounded-xl border border-slate-300 bg-slate-100" readonly />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">⏱️ Giờ ghi nhận:</label>
              <input type="text" value="Tự động ghi nhận lúc bấm gửi" class="w-full text-xs italic text-slate-500 p-3 rounded-xl border border-slate-200 bg-slate-50" readonly />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-800 mb-1 flex items-center gap-1.5">
              <span>1️⃣</span> KẾT QUẢ ĐẠT ĐƯỢC HÔM NAY (*)
            </label>
            <textarea id="emp-res" rows="4" required class="w-full text-xs p-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-sky-500 focus:outline-hidden font-medium bg-slate-50 focus:bg-white transition" placeholder="• Nhiệm vụ 1: Hoàn thành...&#10;• Nhiệm vụ 2:..."></textarea>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-800 mb-1 flex items-center gap-1.5">
                <span>2️⃣</span> KHÓ KHĂN / VƯỚNG MẮC
              </label>
              <textarea id="emp-diff" rows="3" class="w-full text-xs p-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-sky-500 focus:outline-hidden font-medium bg-slate-50 focus:bg-white transition" placeholder="Để trống hoặc ghi 'Không có' nếu thuận lợi"></textarea>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-800 mb-1 flex items-center gap-1.5">
                <span>3️⃣</span> BÀI HỌC / ĐỀ XUẤT
              </label>
              <textarea id="emp-lesson" rows="3" class="w-full text-xs p-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-sky-500 focus:outline-hidden font-medium bg-slate-50 focus:bg-white transition" placeholder="Đề xuất cải tiến nếu có..."></textarea>
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-800 mb-1 flex items-center gap-1.5">
              <span>4️⃣</span> KẾ HOẠCH CÔNG VIỆC NGÀY MAI (*)
            </label>
            <textarea id="emp-plan" rows="3" required class="w-full text-xs p-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-sky-500 focus:outline-hidden font-medium bg-slate-50 focus:bg-white transition" placeholder="• Việc 1:...&#10;• Việc 2:..."></textarea>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-800 mb-1 flex items-center gap-1.5">
              <span>🔗</span> LINK SẢN PHẨM / MINH CHỨNG
            </label>
            <input type="text" id="emp-link" placeholder="Link drive, bài viết, hoặc file thiết kế..." class="w-full text-xs p-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-sky-500 focus:outline-hidden font-medium bg-slate-50 focus:bg-white transition" />
          </div>

          <div class="pt-4 border-t border-slate-200 flex justify-end">
            <button type="submit" id="btn-emp-submit" class="w-full sm:w-auto px-8 py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm rounded-xl transition shadow-md flex items-center justify-center gap-2">
              <span>🚀</span> LƯU & GỬI BÁO CÁO CÔNG VIỆC
            </button>
          </div>
        </form>
      </div>

    </section>

  </main>

  <!-- ================= FOOTER ================= -->
  <footer class="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500 mt-auto">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
      <p>🐱 <strong>Xu Xu</strong> - Trợ lý ảo Marketing King Blue • Toàn bộ Sheet Báo Cáo Marketing</p>
      <div class="flex items-center gap-4">
        <a href="https://docs.google.com/spreadsheets/d/1_kID0uhutS6Ky_zpB2yW_AQXN2aUKKCKo_6tqZL1kbo/edit" target="_blank" class="text-sky-700 hover:underline font-semibold">Google Sheet Báo Cáo</a>
        <a href="https://github.com/duykoolhp1996/KingBlue-Marketing-System" target="_blank" class="text-slate-600 hover:underline">GitHub Repository</a>
      </div>
    </div>
  </footer>

  <!-- SCRIPT DATA & APP LOGIC -->
  <script src="sheets_data.js"></script>
  <script>
    // Embedded Data fallback in case sheets_data.js is blocked
    if (!window.ALL_SHEETS_DATA) {{
      window.ALL_SHEETS_DATA = {json_data_str};
    }}

    // EXACT MARKETING SHEET TABS ORDER
    const SHEET_TABS = [
      {{ key: 'BAO CAO HOM NAY', icon: '📅', label: '0. BAO CAO HOM NAY', name: 'Bảng Tổng Hợp Hàng Ngày (Master)', gid: '187266668', index: 0, badge: '⭐ Tổng hợp' }},
      {{ key: 'Hoai Thuong - Content', icon: '✍️', label: '1. Hoài Thương', name: 'Võ Thị Hoài Thương - Content Marketing', gid: '169328077', index: 1 }},
      {{ key: 'Kieu Thuong - Content', icon: '🎬', label: '2. Kiều Thương', name: 'Kiều Thương - Content Video & KOC', gid: '1499171949', index: 2 }},
      {{ key: 'Thuong Thuong - Content', icon: '📑', label: '3. Thương Thương', name: 'Thương Thương - Trade Marketing', gid: '967400572', index: 3, badge: '🟢 Đã nộp 05/10' }},
      {{ key: 'Thien - Design', icon: '🎨', label: '4. Thiện', name: 'Thiện - Graphic Designer', gid: '1434158092', index: 4, badge: '🟢 44 banner' }},
      {{ key: 'Tu - Media', icon: '📸', label: '5. Tứ', name: 'Tứ - Media & User CRM', gid: '1418274519', index: 5 }},
      {{ key: 'Thuc - San TMDT', icon: '🛒', label: '6. Thức', name: 'Thức - Vận Hành Sàn TMĐT', gid: '1877693997', index: 6, badge: '🟢 Đã nộp 05/10' }},
      {{ key: 'Ngan - San TMDT', icon: '🎧', label: '7. Ngân', name: 'Ngân - CSKH & TikTok Shop', gid: '1804131916', index: 7, badge: '🟢 Đã nộp 05/10' }},
      {{ key: 'BAO CAO TUAN', icon: '📈', label: '8. BÁO CÁO TUẦN', name: 'Báo Cáo Tiến Độ & KPI Hàng Tuần', gid: '162769722', index: 8, badge: '📊 Báo cáo tuần' }}
    ];

    // ACCOUNTS DATABASE (7 NHÂN SỰ MARKETING + 1 QUẢN LÝ)
    const ACCOUNTS = [
      {{ username: "manager", password: "8888", pin: "8888", name: "Marketing Manager", role: "Trưởng Phòng Marketing", group: "Ban Quản Lý", type: "ADMIN", avatar: "👔", tabName: "BAO CAO HOM NAY" }},
      {{ username: "hoaithuong", password: "1001", pin: "1001", name: "Võ Thị Hoài Thương", role: "Content Marketing & SEO Fanpage/Website", group: "Content", type: "USER", avatar: "✍️", tabName: "Hoai Thuong - Content" }},
      {{ username: "kieuthuong", password: "1002", pin: "1002", name: "Kiều Thương", role: "Content Video & Hợp Tác KOC/Reviewer", group: "Content", type: "USER", avatar: "🎬", tabName: "Kieu Thuong - Content" }},
      {{ username: "thuythuong", password: "1003", pin: "1003", name: "Thương Thương", role: "Trade Marketing & Chính Sách Điểm Bán", group: "Content", type: "USER", avatar: "📑", tabName: "Thuong Thuong - Content" }},
      {{ username: "thien", password: "1004", pin: "1004", name: "Thiện", role: "Graphic Designer (2D/3D, POSM & Banner)", group: "Design", type: "USER", avatar: "🎨", tabName: "Thien - Design" }},
      {{ username: "tu", password: "1005", pin: "1005", name: "Tứ", role: "Media / Photographer (Hình Ảnh & User CRM)", group: "Media", type: "USER", avatar: "📸", tabName: "Tu - Media" }},
      {{ username: "thuc", password: "1006", pin: "1006", name: "Thức", role: "Vận Hành Sàn TMĐT (Shopee & Lazada)", group: "Sàn TMĐT", type: "USER", avatar: "🛒", tabName: "Thuc - San TMDT" }},
      {{ username: "ngan", password: "1007", pin: "1007", name: "Ngân", role: "CSKH & Quản Trị Gian Hàng TikTok Shop", group: "Sàn TMĐT", type: "USER", avatar: "🎧", tabName: "Ngan - San TMDT" }}
    ];

    let currentAppMainTab = 'cards';
    let currentActiveSheetKey = 'BAO CAO HOM NAY';
    let currentSheetViewFormat = 'html';
    let managerSelectedDate = '05/10/2026';
    let currentUser = null;
    let pendingRedirectTab = null;

    window.addEventListener("DOMContentLoaded", () => {{
      renderQuickLoginButtons();
      startLiveClock();
      renderSheetTabsBar();
      selectSheetTab('BAO CAO HOM NAY');

      // Check saved session
      const savedUser = localStorage.getItem("kingblue_user");
      if (savedUser) {{
        try {{
          currentUser = JSON.parse(savedUser);
          updateUserSessionBar();
        }} catch(e) {{}}
      }}

      // Tự động nhận diện ngày mới nhất có báo cáo (hoặc hôm nay nếu chưa có)
      const availDates = getAvailableReportDates();
      if (availDates && availDates.length > 0) {{
        managerSelectedDate = availDates[0];
      }} else {{
        managerSelectedDate = formatDateDMY(new Date());
      }}

      const formDateEl = document.getElementById("emp-form-date");
      if (formDateEl) formDateEl.value = formatDateDMY(new Date());

      // Default to Tab 2: 'cards' (THẺ CÔNG VIỆC HÔM NAY - MỞ TỰ DO KHÔNG CẦN ĐĂNG NHẬP)
      switchMainAppTab('cards');

      // AUTO LIVE SYNC DIRECTLY FROM GOOGLE SHEETS
      setTimeout(() => autoSyncLiveGoogleSheets(true), 600);
      setInterval(() => autoSyncLiveGoogleSheets(true), 30000);
      window.addEventListener('focus', () => autoSyncLiveGoogleSheets(true));
    }});

    function startLiveClock() {{
      setInterval(() => {{
        const now = new Date();
        const el = document.getElementById("live-clock");
        if (el) el.textContent = now.toTimeString().split(' ')[0];
      }}, 1000);
    }}

    // ========================================================
    // 1. PRIMARY APP MODE SWITCHING
    // ========================================================
    function switchMainAppTab(mode) {{
      // Tab 1 (Bảng tính chi tiết) requires login
      if (mode === 'sheets' && !currentUser) {{
        openLoginModal('sheets');
        return;
      }}

      currentAppMainTab = mode;
      
      const btnSheets = document.getElementById("btn-nav-sheets");
      const btnCards = document.getElementById("btn-nav-cards");
      const btnSubmit = document.getElementById("btn-nav-submit");

      const secSheets = document.getElementById("section-sheets-explorer");
      const secCards = document.getElementById("section-cards-dashboard");
      const secSubmit = document.getElementById("section-personal-submit");

      [btnSheets, btnCards, btnSubmit].forEach(b => {{
        b.className = "px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 text-slate-700 hover:bg-slate-100 border border-transparent";
      }});
      [secSheets, secCards, secSubmit].forEach(s => s.classList.add("hidden"));

      if (mode === 'cards') {{
        btnCards.className = "px-4 py-2 rounded-xl text-xs font-extrabold transition flex items-center gap-2 bg-[#1A365D] text-white shadow-xs";
        secCards.classList.remove("hidden");
        setManagerDate(managerSelectedDate);
      }} else if (mode === 'sheets') {{
        btnSheets.className = "px-4 py-2 rounded-xl text-xs font-extrabold transition flex items-center gap-2 bg-[#1A365D] text-white shadow-xs";
        secSheets.classList.remove("hidden");
      }} else if (mode === 'submit') {{
        btnSubmit.className = "px-4 py-2 rounded-xl text-xs font-extrabold transition flex items-center gap-2 bg-[#1A365D] text-white shadow-xs";
        secSubmit.classList.remove("hidden");
        renderSubmitSpace();
      }}
    }}

    function openLoginModal(targetTab = null) {{
      pendingRedirectTab = targetTab;
      const modal = document.getElementById("modal-login");
      modal.classList.remove("hidden");
      setTimeout(() => {{
        const inp = document.getElementById("modal-login-password");
        if (inp) {{ inp.value = ""; inp.focus(); }}
      }}, 100);
    }}

    function closeLoginModal() {{
      const modal = document.getElementById("modal-login");
      modal.classList.add("hidden");
      pendingRedirectTab = null;
    }}

    function handleModalPasswordSubmit(e) {{
      e.preventDefault();
      const val = document.getElementById("modal-login-password").value.trim();
      if (doLoginByPassword(val)) {{
        closeLoginModal();
        if (pendingRedirectTab) {{
          switchMainAppTab(pendingRedirectTab);
          pendingRedirectTab = null;
        }}
      }}
    }}

    // ========================================================
    // 2. SHEETS EXPLORER (9 TABS ACCORDING TO SPREADSHEET)
    // ========================================================
    function renderSheetTabsBar() {{
      const container = document.getElementById("sheet-tabs-container");
      container.innerHTML = "";

      SHEET_TABS.forEach(tab => {{
        const btn = document.createElement("button");
        btn.id = `sheet-tab-btn-${{tab.gid}}`;
        const isActive = tab.key === currentActiveSheetKey;
        btn.className = `px-3.5 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap flex items-center gap-2 border ${{
          isActive 
            ? 'tab-sheet-active' 
            : 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-200'
        }}`;
        btn.onclick = () => selectSheetTab(tab.key);
        btn.innerHTML = `
          <span>${{tab.icon}}</span>
          <span>${{tab.label}}</span>
          ${{tab.badge ? `<span class="text-[10px] px-1.5 py-0.5 rounded-md font-extrabold ${{isActive ? 'bg-amber-400 text-slate-900' : 'bg-emerald-100 text-emerald-800'}}">${{tab.badge}}</span>` : ''}}
        `;
        container.appendChild(btn);
      }});
    }}

    function selectSheetTab(sheetKey) {{
      currentActiveSheetKey = sheetKey;
      const tabMeta = SHEET_TABS.find(t => t.key === sheetKey) || SHEET_TABS[0];

      // Update Tab Styles
      SHEET_TABS.forEach(t => {{
        const b = document.getElementById(`sheet-tab-btn-${{t.gid}}`);
        if (b) {{
          if (t.key === sheetKey) {{
            b.className = "px-3.5 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap flex items-center gap-2 border tab-sheet-active";
          }} else {{
            b.className = "px-3.5 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap flex items-center gap-2 border bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-200";
          }}
        }}
      }});

      // Update Header Info
      document.getElementById("active-sheet-icon").textContent = tabMeta.icon;
      document.getElementById("active-sheet-title").textContent = tabMeta.label;
      document.getElementById("active-sheet-badge").textContent = `Vị trí ${{tabMeta.index}} / 8 (gid=${{tabMeta.gid}})`;
      document.getElementById("active-sheet-desc").textContent = tabMeta.name;
      document.getElementById("active-sheet-direct-link").href = `https://docs.google.com/spreadsheets/d/1_kID0uhutS6Ky_zpB2yW_AQXN2aUKKCKo_6tqZL1kbo/edit#gid=${{tabMeta.gid}}`;

      // Update Iframe URL
      const iframe = document.getElementById("sheet-google-iframe");
      iframe.src = `https://docs.google.com/spreadsheets/d/1_kID0uhutS6Ky_zpB2yW_AQXN2aUKKCKo_6tqZL1kbo/htmlembed?gid=${{tabMeta.gid}}&widget=false&chrome=false`;

      // Render Table Data
      renderActiveSheetHtml(sheetKey);
    }}

    function toggleSheetViewFormat(format) {{
      currentSheetViewFormat = format;
      const btnHtml = document.getElementById("btn-format-html");
      const btnIframe = document.getElementById("btn-format-iframe");
      const htmlBox = document.getElementById("sheet-html-view-container");
      const iframeBox = document.getElementById("sheet-iframe-view-container");

      if (format === 'html') {{
        btnHtml.className = "px-3 py-1.5 rounded-lg transition bg-white text-blue-900 shadow-2xs flex items-center gap-1";
        btnIframe.className = "px-3 py-1.5 rounded-lg transition text-slate-600 hover:text-slate-900 flex items-center gap-1";
        htmlBox.classList.remove("hidden");
        iframeBox.classList.add("hidden");
      }} else {{
        btnIframe.className = "px-3 py-1.5 rounded-lg transition bg-white text-blue-900 shadow-2xs flex items-center gap-1";
        btnHtml.className = "px-3 py-1.5 rounded-lg transition text-slate-600 hover:text-slate-900 flex items-center gap-1";
        iframeBox.classList.remove("hidden");
        htmlBox.classList.add("hidden");
      }}
    }}

    function renderActiveSheetHtml(sheetKey) {{
      const container = document.getElementById("sheet-html-view-container");
      container.innerHTML = "";

      const sheetData = (window.ALL_SHEETS_DATA && window.ALL_SHEETS_DATA[sheetKey]) ? window.ALL_SHEETS_DATA[sheetKey] : null;

      if (!sheetData || !sheetData.rows || sheetData.rows.length === 0) {{
        container.innerHTML = `
          <div class="bg-white rounded-2xl border border-slate-200 p-12 text-center text-slate-400">
            <span class="text-4xl block mb-2">📂</span>
            <p class="font-bold text-slate-600">Chưa có dữ liệu cho sheet này</p>
            <p class="text-xs text-slate-400 mt-1">Dữ liệu sẽ được tự động đồng bộ khi nhân sự nhập vào Google Sheets.</p>
          </div>
        `;
        return;
      }}

      const rows = sheetData.rows;

      if (sheetKey === 'BAO CAO HOM NAY') {{
        renderMasterSheetHtml(container, rows);
      }} else if (sheetKey === 'BAO CAO TUAN') {{
        renderWeeklySheetHtml(container, rows);
      }} else {{
        renderEmployeeSheetHtml(container, rows, sheetKey);
      }}
    }}

    // Master Dashboard Sheet Renderer
    function renderMasterSheetHtml(container, rows) {{
      const userAccounts = ACCOUNTS.filter(a => a.type === "USER");
      const staffRows = rows.filter(r => r && r.length > 2 && r[1] && userAccounts.some(u => r[1].includes(u.name) || u.name.includes(r[1])));
      const totalStaff = userAccounts.length;
      const submittedRows = staffRows.filter(r => {{
        const res = r[4] || '';
        return res && !res.includes('Chưa nộp') && res.trim() !== '-' && res !== '⏳ Chưa nộp';
      }});
      const subCount = submittedRows.length;
      const subPercent = totalStaff > 0 ? Math.round((subCount / totalStaff) * 100) : 0;

      const wrapper = document.createElement("div");
      wrapper.className = "space-y-4";

      // Meta Stats Cards
      wrapper.innerHTML = `
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
            <span class="text-xs text-slate-500 font-semibold block">👥 Tổng Nhân Sự</span>
            <span class="text-xl font-extrabold text-slate-900 mt-1 block">${{totalStaff}} Người</span>
          </div>
          <div class="bg-emerald-50 p-4 rounded-2xl border border-emerald-200 shadow-2xs">
            <span class="text-xs text-emerald-700 font-semibold block">✅ Đã Nộp Hôm Nay</span>
            <span class="text-xl font-extrabold text-emerald-800 mt-1 block">${{subCount}} / ${{totalStaff}} (${{subPercent}}%)</span>
          </div>
          <div class="bg-amber-50 p-4 rounded-2xl border border-amber-200 shadow-2xs">
            <span class="text-xs text-amber-700 font-semibold block">⚠️ Vướng Mắc Phát Sinh</span>
            <span class="text-xl font-extrabold text-amber-800 mt-1 block">0 Vấn đề</span>
          </div>
          <div class="bg-blue-50 p-4 rounded-2xl border border-blue-200 shadow-2xs">
            <span class="text-xs text-blue-700 font-semibold block">👔 Trưởng Phòng</span>
            <span class="text-sm font-extrabold text-blue-900 mt-1.5 block">Marketing Manager</span>
          </div>
        </div>

        <div class="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
            <h3 class="font-extrabold text-slate-900 text-sm flex items-center gap-2">
              <span>📋</span> BẢNG TỔNG HỢP TIẾN ĐỘ THỰC TẾ TRONG NGÀY (${{totalStaff}} NHÂN SỰ)
            </h3>
            <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2.5 py-0.5 rounded-full">
              Dữ liệu chuẩn Google Sheets
            </span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left text-slate-700 border-collapse">
              <thead class="bg-slate-100 text-slate-800 font-bold uppercase text-[11px] border-b border-slate-200">
                <tr>
                  <th class="p-3 w-12 text-center">STT</th>
                  <th class="p-3 w-44">Nhân Sự</th>
                  <th class="p-3 w-28">Bộ Phận</th>
                  <th class="p-3 min-w-[280px]">1️⃣ Kết Quả Đạt Được Hôm Nay</th>
                  <th class="p-3 min-w-[200px]">4️⃣ Kế Hoạch Ngày Mai</th>
                  <th class="p-3 w-24 text-center">Giờ Nộp</th>
                  <th class="p-3 w-24 text-center">Trạng Thái</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 font-medium">
                ${{staffRows.map((r, idx) => {{
                  const stt = r[0] || (idx + 1);
                  const name = r[1] || '';
                  const dept = r[2] || '';
                  const res = r[4] || '';
                  const plan = r[7] || '';
                  const time = (r[8] && r[8] !== '--:--' && r[8] !== '00:00:00') ? r[8] : '17:00:00';
                  const isSubmitted = res && !res.includes('Chưa nộp') && res.trim() !== '-' && res !== '⏳ Chưa nộp';

                  return `
                    <tr class="hover:bg-slate-50/80 transition">
                      <td class="p-3 text-center font-bold text-slate-400">${{stt}}</td>
                      <td class="p-3 font-bold text-slate-900">${{name}}</td>
                      <td class="p-3 text-slate-500"><span class="px-2 py-0.5 rounded-md bg-slate-100 text-[11px] font-semibold">${{dept}}</span></td>
                      <td class="p-3 leading-relaxed whitespace-pre-line">${{formatResultsHtml(res)}}</td>
                      <td class="p-3 text-slate-600 whitespace-pre-line">${{plan || '-'}}</td>
                      <td class="p-3 text-center font-mono text-[11px] font-bold text-slate-600">${{time}}</td>
                      <td class="p-3 text-center">
                        ${{isSubmitted 
                          ? '<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">Đã nộp</span>' 
                          : '<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-500">Chờ nộp</span>'}}
                      </td>
                    </tr>
                  `;
                }}).join('')}}
              </tbody>
            </table>
          </div>
        </div>
      `;

      container.appendChild(wrapper);
    }}

    // Individual Employee Sheet Renderer
    function renderEmployeeSheetHtml(container, rows, sheetKey) {{
      const metaRow = rows[2] || [];
      const empName = metaRow[2] || sheetKey;
      const empRole = metaRow[6] || '';
      const managerName = metaRow[10] || 'Marketing Manager';

      // Lọc các dòng dữ liệu báo cáo thật sự (nhận diện qua ngày tháng ở cột B hoặc A)
      const tableRows = rows.filter(r => r && r.length > 1 && isDateString(r[1] || r[0]));

      const wrapper = document.createElement("div");
      wrapper.className = "space-y-4";
      wrapper.innerHTML = `
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs flex flex-wrap items-center justify-between gap-3">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-xl bg-blue-100 text-blue-900 flex items-center justify-center text-2xl font-bold shadow-inner">
              👤
            </div>
            <div>
              <h3 class="font-extrabold text-slate-900 text-base">${{empName}}</h3>
              <p class="text-xs text-slate-500">${{empRole}}</p>
            </div>
          </div>
          <div class="text-xs text-right">
            <span class="text-slate-500">Người phê duyệt:</span>
            <span class="font-bold text-slate-800 block">${{managerName}}</span>
          </div>
        </div>

        <div class="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
            <h4 class="font-bold text-xs text-slate-800 uppercase tracking-wider">
              Lịch sử các ngày báo cáo trong sheet
            </h4>
            <span class="text-[11px] text-slate-500">${{tableRows.length}} ngày được ghi nhận</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left text-slate-700 border-collapse">
              <thead class="bg-slate-100 text-slate-800 font-bold uppercase text-[10px] border-b border-slate-200">
                <tr>
                  <th class="p-3 w-12 text-center">STT</th>
                  <th class="p-3 w-28">Ngày Báo Cáo</th>
                  <th class="p-3 min-w-[280px]">1️⃣ Kết Quả Đạt Được</th>
                  <th class="p-3 min-w-[180px]">2️⃣ Khó Khăn</th>
                  <th class="p-3 min-w-[180px]">4️⃣ Kế Hoạch Ngày Mai</th>
                  <th class="p-3 w-28">Trạng Thái</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 font-medium">
                ${{tableRows.map((r, rIdx) => {{
                  const stt = (r[0] && !isDateString(r[0])) ? r[0] : String(rIdx + 1);
                  const date = isDateString(r[1]) ? normalizeDateStr(r[1]) : (isDateString(r[0]) ? normalizeDateStr(r[0]) : '05/10/2026');
                  const res = r[3] || r[2] || 'Chưa có nội dung';
                  const diff = r[4] || 'Không có';
                  const plan = r[6] || '-';
                  const status = (res && res !== 'Chưa có nội dung' && !res.includes('Chưa nộp')) ? 'Đã hoàn thành' : 'Đang chờ';

                  return `
                    <tr class="hover:bg-slate-50 transition">
                      <td class="p-3 text-center font-bold text-slate-400">${{stt}}</td>
                      <td class="p-3 font-mono font-bold text-blue-900 whitespace-nowrap">${{date}}</td>
                      <td class="p-3 leading-relaxed whitespace-pre-line text-slate-900">${{formatResultsHtml(res)}}</td>
                      <td class="p-3 text-amber-900 leading-relaxed">${{diff || 'Không có'}}</td>
                      <td class="p-3 text-sky-900 leading-relaxed whitespace-pre-line">${{plan}}</td>
                      <td class="p-3">
                        <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${{status === 'Đã hoàn thành' ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-500'}}">
                          ${{status}}
                        </span>
                      </td>
                    </tr>
                  `;
                }}).join('')}}
              </tbody>
            </table>
          </div>
        </div>
      `;

      container.appendChild(wrapper);
    }}

    // Weekly Sheet Renderer
    function renderWeeklySheetHtml(container, rows) {{
      const wrapper = document.createElement("div");
      wrapper.className = "bg-white rounded-2xl border border-slate-200 shadow-xs p-6";
      wrapper.innerHTML = `
        <div class="text-center py-8">
          <span class="text-4xl block mb-2">📈</span>
          <h3 class="font-extrabold text-base text-slate-900">BÁO CÁO TIẾN ĐỘ TUẦN PHÒNG MARKETING</h3>
          <p class="text-xs text-slate-500 mt-1">Dữ liệu tổng hợp theo từng tuần hoạt động từ thứ Hai đến thứ Bảy.</p>
        </div>
      `;
      container.appendChild(wrapper);
    }}

    function formatResultsHtml(text) {{
      if (!text) return '<span class="text-slate-400 italic">Chưa nộp nội dung</span>';
      let clean = text.replace(/\\r\\n/g, '\\n').replace(/\\r/g, '\\n');
      return clean
        .replace(/\\n/g, '<br/>')
        .replace(/•/g, '<span class="text-emerald-600 font-black inline-block mr-1">•</span>')
        .replace(/-\\s+/g, '<span class="text-emerald-500 font-bold inline-block mr-1">- </span>');
    }}

    // ========================================================
    // 3. CARDS DASHBOARD (EXECUTIVE 17H VIEW - MỞ TỰ DO)
    // ========================================================
    function isDateString(str) {{
      if (!str) return false;
      const s = String(str).trim();
      if (s.includes('Ngày') || s.includes('NGÀY') || s.includes('STT') || s.includes('Họ và Tên') || s.includes('Nhân Sự')) return false;
      if (/^Date\\(\\d+\\s*,\\s*\\d+\\s*,\\s*\\d+\\)/.test(s)) return true;
      if (/^\\d{1,2}\\/\\d{1,2}(\\/\\d{2,4})?$/.test(s)) return true;
      if (/^\\d{4}-\\d{1,2}-\\d{1,2}$/.test(s)) return true;
      return false;
    }}

    function normalizeDateStr(dStr, defaultYear = 2026) {{
      if (!dStr) return '';
      let s = String(dStr).trim();
      const gvizMatch = s.match(/Date\\((\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)\\)/);
      if (gvizMatch) {{
        const y = gvizMatch[1];
        const m = String(parseInt(gvizMatch[2]) + 1).padStart(2, '0');
        const d = String(parseInt(gvizMatch[3])).padStart(2, '0');
        return `${{d}}/${{m}}/${{y}}`;
      }}
      if (s.includes('/')) {{
        const parts = s.split('/');
        if (parts.length === 2) {{
          const d = String(parseInt(parts[0])).padStart(2, '0');
          const m = String(parseInt(parts[1])).padStart(2, '0');
          return `${{d}}/${{m}}/${{defaultYear}}`;
        }} else if (parts.length === 3) {{
          const d = String(parseInt(parts[0])).padStart(2, '0');
          const m = String(parseInt(parts[1])).padStart(2, '0');
          let y = parts[2].trim();
          if (y.length === 2) y = '20' + y;
          return `${{d}}/${{m}}/${{y}}`;
        }}
      }}
      if (s.includes('-')) {{
        const parts = s.split('-');
        if (parts.length === 3 && parts[0].length === 4) {{
          const y = parts[0];
          const m = String(parseInt(parts[1])).padStart(2, '0');
          const d = String(parseInt(parts[2])).padStart(2, '0');
          return `${{d}}/${{m}}/${{y}}`;
        }}
      }}
      return s;
    }}

    function getAvailableReportDates() {{
      const datesSet = new Set();
      const users = ACCOUNTS.filter(a => a.type === "USER");
      
      users.forEach(u => {{
        const sData = (window.ALL_SHEETS_DATA && window.ALL_SHEETS_DATA[u.tabName]) ? window.ALL_SHEETS_DATA[u.tabName] : null;
        if (sData && sData.rows) {{
          sData.rows.forEach(r => {{
            if (r && r.length > 1) {{
              const c1 = String(r[1] || '').trim();
              const c0 = String(r[0] || '').trim();
              if (isDateString(c1)) datesSet.add(normalizeDateStr(c1));
              else if (isDateString(c0)) datesSet.add(normalizeDateStr(c0));
            }}
          }});
        }}
      }});

      const masterData = (window.ALL_SHEETS_DATA && window.ALL_SHEETS_DATA['BAO CAO HOM NAY']) ? window.ALL_SHEETS_DATA['BAO CAO HOM NAY'] : null;
      if (masterData && masterData.rows) {{
        for (let rIdx = 0; rIdx < Math.min(masterData.rows.length, 4); rIdx++) {{
          const r = masterData.rows[rIdx];
          if (!r) continue;
          r.forEach(cell => {{
            if (cell && isDateString(cell)) datesSet.add(normalizeDateStr(cell));
          }});
        }}
      }}

      // Add today
      datesSet.add(formatDateDMY(new Date()));

      const list = Array.from(datesSet);
      list.sort((a, b) => {{
        const dtA = parseDMYDate(a);
        const dtB = parseDMYDate(b);
        return dtB - dtA; // Newest first
      }});
      return list;
    }}

    function renderQuickDateChips() {{
      const container = document.getElementById("mgr-quick-date-chips");
      if (!container) return;
      container.innerHTML = "";

      const dates = getAvailableReportDates();
      const recentDates = dates.slice(0, 6);

      recentDates.forEach(d => {{
        const btn = document.createElement("button");
        const isSelected = (normalizeDateStr(managerSelectedDate) === normalizeDateStr(d));
        btn.type = "button";
        btn.onclick = () => setManagerDate(d);
        btn.className = isSelected 
          ? "px-2.5 py-1 rounded-xl text-xs font-black bg-blue-700 text-white shadow-2xs border border-blue-800 transition flex items-center gap-1"
          : "px-2.5 py-1 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-300 transition flex items-center gap-1";
        
        const todayStr = formatDateDMY(new Date());
        let label = d.substring(0, 5);
        if (d === todayStr) label = "Hôm nay (" + label + ")";
        
        btn.innerHTML = `<span>📅</span> <span>${{label}}</span>`;
        container.appendChild(btn);
      }});
    }}

    function setManagerDate(dateStr) {{
      managerSelectedDate = normalizeDateStr(dateStr) || dateStr;
      
      const picker = document.getElementById("mgr-calendar-picker");
      if (picker) picker.value = dmyToYmd(managerSelectedDate);

      const textEl = document.getElementById("mgr-date-text");
      if (textEl) textEl.textContent = formatVietnameseFullDate(managerSelectedDate);

      renderQuickDateChips();
      renderManagerCards(managerSelectedDate);
      updateExecutiveReportPreview(managerSelectedDate);
      fetchBackendReportsForDate(managerSelectedDate);
    }}

    function jumpManagerDay(offset) {{
      const dt = parseDMYDate(managerSelectedDate);
      dt.setDate(dt.getDate() + offset);
      setManagerDate(formatDateDMY(dt));
    }}

    function setManagerToToday() {{
      const today = formatDateDMY(new Date());
      setManagerDate(today);
    }}

    function onManagerCalendarChange(ymd) {{
      if (!ymd) return;
      const p = ymd.split('-');
      setManagerDate(`${{p[2]}}/${{p[1]}}/${{p[0]}}`);
    }}

    function parseDMYDate(dmy) {{
      if (!dmy || !dmy.includes('/')) return new Date();
      const p = dmy.split('/');
      return new Date(parseInt(p[2]), parseInt(p[1]) - 1, parseInt(p[0]));
    }}

    function formatDateDMY(dt) {{
      const d = String(dt.getDate()).padStart(2, '0');
      const m = String(dt.getMonth() + 1).padStart(2, '0');
      return `${{d}}/${{m}}/${{dt.getFullYear()}}`;
    }}

    function dmyToYmd(dmy) {{
      if (!dmy || !dmy.includes('/')) return "";
      const p = dmy.split('/');
      return `${{p[2]}}-${{p[1]}}-${{p[0]}}`;
    }}

    function formatVietnameseFullDate(dmy) {{
      const dt = parseDMYDate(dmy);
      const days = ["Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"];
      return `${{days[dt.getDay()] || 'Thứ'}}, ${{dmy}}`;
    }}

    async function fetchBackendReportsForDate(dateStr) {{
      const targetNorm = normalizeDateStr(dateStr);
      if (!targetNorm) return;
      if (!window.REPORTS_CACHE) window.REPORTS_CACHE = {{}};
      
      try {{
        const res = await fetch(`/api/reports?date=${{encodeURIComponent(targetNorm)}}`);
        if (res.ok) {{
          const data = await res.json();
          if (data && data.success && data.reports) {{
            window.REPORTS_CACHE[targetNorm] = data.reports;
            if (normalizeDateStr(managerSelectedDate) === targetNorm) {{
              renderManagerCards(managerSelectedDate);
              updateExecutiveReportPreview(managerSelectedDate);
            }}
          }}
        }}
      }} catch (e) {{}}
    }}

    function getRoleColorTheme(group) {{
      switch(group) {{
        case "Content":
          return {{
            borderTop: "border-t-4 border-t-indigo-500",
            avatarBg: "bg-indigo-50 text-indigo-700 border-indigo-200",
            badgeBg: "bg-indigo-100 text-indigo-800 border-indigo-200 font-extrabold",
            roleTag: "text-indigo-900 bg-indigo-50 border border-indigo-200 font-bold"
          }};
        case "Design":
          return {{
            borderTop: "border-t-4 border-t-pink-500",
            avatarBg: "bg-pink-50 text-pink-700 border-pink-200",
            badgeBg: "bg-pink-100 text-pink-800 border-pink-200 font-extrabold",
            roleTag: "text-pink-900 bg-pink-50 border border-pink-200 font-bold"
          }};
        case "Media":
          return {{
            borderTop: "border-t-4 border-t-amber-500",
            avatarBg: "bg-amber-50 text-amber-800 border-amber-200",
            badgeBg: "bg-amber-100 text-amber-900 border-amber-300 font-extrabold",
            roleTag: "text-amber-900 bg-amber-50 border border-amber-200 font-bold"
          }};
        case "Sàn TMĐT":
          return {{
            borderTop: "border-t-4 border-t-emerald-500",
            avatarBg: "bg-emerald-50 text-emerald-800 border-emerald-200",
            badgeBg: "bg-emerald-100 text-emerald-800 border-emerald-200 font-extrabold",
            roleTag: "text-emerald-900 bg-emerald-50 border border-emerald-200 font-bold"
          }};
        default:
          return {{
            borderTop: "border-t-4 border-t-blue-500",
            avatarBg: "bg-blue-50 text-blue-800 border-blue-200",
            badgeBg: "bg-blue-100 text-blue-800 border-blue-200 font-extrabold",
            roleTag: "text-blue-900 bg-blue-50 border border-blue-200 font-bold"
          }};
      }}
    }}

    function findReportForUser(u, dateStr) {{
      if (!u || !dateStr) return null;
      const targetNorm = normalizeDateStr(dateStr);
      if (!targetNorm) return null;

      // 1. Check runtime memory cache (từ backend API nếu có)
      if (window.REPORTS_CACHE && window.REPORTS_CACHE[targetNorm] && window.REPORTS_CACHE[targetNorm][u.username]) {{
        return window.REPORTS_CACHE[targetNorm][u.username];
      }}

      // 2. Check individual staff tab (window.ALL_SHEETS_DATA[u.tabName])
      const sData = (window.ALL_SHEETS_DATA && window.ALL_SHEETS_DATA[u.tabName]) ? window.ALL_SHEETS_DATA[u.tabName] : null;
      if (sData && sData.rows && Array.isArray(sData.rows)) {{
        for (const r of sData.rows) {{
          if (!r || !Array.isArray(r) || r.length < 2) continue;
          
          const c1 = String(r[1] || '').trim();
          const c0 = String(r[0] || '').trim();
          
          const norm1 = isDateString(c1) ? normalizeDateStr(c1) : '';
          const norm0 = isDateString(c0) ? normalizeDateStr(c0) : '';
          
          if (norm1 === targetNorm || norm0 === targetNorm) {{
            const resText = String(r[3] || r[2] || '').trim();
            if (resText && !resText.includes('Chưa nộp') && resText !== '-' && resText !== '⏳ Chưa nộp') {{
              return {{
                time: (r[2] && r[2] !== '--:--' && r[2] !== '00:00:00' && r[2].includes(':')) ? r[2] : '17:00:00',
                res: resText,
                diff: (r[4] && r[4].trim()) ? r[4] : '• Không có',
                lesson: (r[5] && r[5].trim()) ? r[5] : '• Không có',
                plan: r[6] || '',
                link: r[7] || '-',
                status: (r[8] && r[8].trim() && r[8] !== 'Chưa nộp') ? r[8] : 'Đúng hạn',
                feedback: (r[9] && r[9] !== 'Chờ duyệt') ? r[9] : ''
              }};
            }}
          }}
        }}
      }}

      // 3. Check Master sheet 'BAO CAO HOM NAY' - CHỈ KHI ngày của Master sheet khớp chính xác targetNorm!
      const masterData = (window.ALL_SHEETS_DATA && window.ALL_SHEETS_DATA['BAO CAO HOM NAY']) ? window.ALL_SHEETS_DATA['BAO CAO HOM NAY'] : null;
      if (masterData && masterData.rows && Array.isArray(masterData.rows)) {{
        let masterDate = '';
        for (let rIdx = 0; rIdx < Math.min(masterData.rows.length, 4); rIdx++) {{
          const r = masterData.rows[rIdx];
          if (!r) continue;
          for (const cell of r) {{
            if (cell && isDateString(cell)) {{
              masterDate = cell;
              break;
            }}
          }}
          if (masterDate) break;
        }}
        const masterDateNorm = normalizeDateStr(masterDate);
        if (masterDateNorm && masterDateNorm === targetNorm) {{
          for (const r of masterData.rows) {{
            if (r && r.length > 4 && r[1] && (r[1].includes(u.name) || u.name.includes(r[1]))) {{
              const resText = String(r[4] || '').trim();
              if (resText && !resText.includes('Chưa nộp') && resText !== '-' && resText !== '⏳ Chưa nộp') {{
                return {{
                  time: (r[8] && r[8] !== '--:--' && r[8] !== '00:00:00') ? r[8] : '17:00:00',
                  res: resText,
                  diff: (r[5] && r[5].trim()) ? r[5] : '• Không có',
                  lesson: (r[6] && r[6].trim()) ? r[6] : '• Không có',
                  plan: r[7] || '',
                  link: '-',
                  status: (r[9] && r[9].trim() && r[9] !== 'Chưa nộp') ? r[9] : 'Đúng hạn',
                  feedback: (r[10] && r[10] !== 'Chờ duyệt') ? r[10] : ''
                }};
              }}
            }}
          }}
        }}
      }}

      return null;
    }}

    function renderManagerCards(dateStr) {{
      const container = document.getElementById("mgr-cards-container");
      container.innerHTML = "";

      const users = ACCOUNTS.filter(a => a.type === "USER");
      let subCount = 0;

      users.forEach(u => {{
        const theme = getRoleColorTheme(u.group);
        const rep = findReportForUser(u, dateStr);
        const card = document.createElement("div");

        if (!rep) {{
          card.className = `bg-white/95 rounded-3xl border-2 border-dashed border-slate-200 ${{theme.borderTop}} p-4 sm:p-5 shadow-2xs hover:shadow-md transition-all duration-200 flex flex-col justify-between`;
          card.innerHTML = `
            <div>
              <div class="flex items-start justify-between pb-3.5 border-b border-slate-100 gap-2">
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-13 h-13 sm:w-15 sm:h-15 rounded-2xl ${{theme.avatarBg}} border opacity-85 flex items-center justify-center text-3xl font-black shadow-2xs shrink-0">${{u.avatar}}</div>
                  <div class="min-w-0">
                    <h4 class="font-black text-slate-900 text-lg sm:text-xl leading-tight tracking-tight">${{u.name}}</h4>
                    <div class="mt-1.5 flex flex-wrap items-center gap-1.5">
                      <span class="text-xs font-black px-2.5 py-0.5 rounded-lg border shadow-2xs ${{theme.badgeBg}}">${{u.group}}</span>
                      <span class="text-xs font-bold px-2.5 py-0.5 rounded-lg border ${{theme.roleTag}}">${{u.role}}</span>
                    </div>
                  </div>
                </div>
                <span class="text-xs font-black px-2.5 py-1 rounded-lg bg-amber-50 text-amber-700 border border-amber-200 shrink-0">⏳ Chờ nộp</span>
              </div>
              <div class="py-10 text-center text-slate-400">
                <span class="text-4xl block mb-2">⏳</span>
                <p class="font-black text-base sm:text-lg text-slate-600">Chưa nộp báo cáo ngày này</p>
                <p class="text-xs sm:text-sm text-slate-400 mt-1">Hạn nộp báo cáo: trước 17:30 chiều</p>
              </div>
            </div>
            <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500 font-medium">
              <span>Trạng thái: <strong class="text-amber-600 font-black">Đang chờ nộp</strong></span>
              <span class="font-mono font-bold">--:--:--</span>
            </div>
          `;
        }} else {{
          subCount++;
          const hasDiff = rep.diff && !rep.diff.includes("Không có") && rep.diff !== "-";
          card.className = `bg-white rounded-3xl border border-slate-200 hover:border-slate-300 ${{theme.borderTop}} p-4 sm:p-5 shadow-xs hover:shadow-xl transition-all duration-200 flex flex-col justify-between space-y-4`;
          card.innerHTML = `
            <div>
              <div class="flex items-start justify-between pb-3.5 border-b border-slate-100 gap-2">
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-13 h-13 sm:w-15 sm:h-15 rounded-2xl ${{theme.avatarBg}} border flex items-center justify-center text-3xl font-black shadow-2xs shrink-0">${{u.avatar}}</div>
                  <div class="min-w-0">
                    <h4 class="font-black text-slate-900 text-lg sm:text-xl leading-tight tracking-tight">${{u.name}}</h4>
                    <div class="mt-1.5 flex flex-wrap items-center gap-1.5">
                      <span class="text-xs font-black px-2.5 py-0.5 rounded-lg border shadow-2xs ${{theme.badgeBg}}">${{u.group}}</span>
                      <span class="text-xs font-bold px-2.5 py-0.5 rounded-lg border ${{theme.roleTag}}">${{u.role}}</span>
                    </div>
                  </div>
                </div>
                <div class="text-right shrink-0">
                  <span class="inline-block px-2.5 py-1 rounded-lg text-xs font-black bg-emerald-100 text-emerald-800 border border-emerald-200 shadow-2xs">
                    🟢 Đúng hạn
                  </span>
                  <p class="text-xs font-mono text-slate-700 font-black mt-1">⏱️ ${{rep.time}}</p>
                </div>
              </div>

              <div class="mt-3.5 space-y-3.5">
                <div>
                  <div class="text-xs sm:text-sm font-black uppercase text-slate-800 flex items-center gap-1.5 mb-1.5">
                    <span class="text-emerald-600 text-base">1️⃣</span> Kết Quả Đạt Được Hôm Nay
                  </div>
                  <div class="bg-slate-50 border border-slate-200/90 rounded-2xl p-3.5 sm:p-4 text-sm sm:text-base leading-relaxed font-normal text-slate-900">
                    ${{formatResultsHtml(rep.res)}}
                  </div>
                </div>

                ${{hasDiff ? `
                <div>
                  <div class="text-xs sm:text-sm font-black uppercase text-amber-900 flex items-center gap-1.5 mb-1">
                    <span class="text-amber-600 text-base">⚠️</span> Khó Khăn Cần Tháo Gỡ
                  </div>
                  <div class="bg-amber-50 border border-amber-200 rounded-2xl p-3.5 sm:p-4 text-sm sm:text-base text-amber-950 font-normal whitespace-pre-line leading-relaxed">
                    ${{rep.diff}}
                  </div>
                </div>
                ` : `
                <div class="text-xs sm:text-sm text-slate-400 italic flex items-center gap-1.5 py-1">
                  <span class="text-emerald-500 font-black">✓</span> Không phát sinh vướng mắc
                </div>
                `}}

                <div>
                  <div class="text-xs sm:text-sm font-black uppercase text-sky-900 flex items-center gap-1.5 mb-1.5">
                    <span class="text-sky-600 text-base">🎯</span> Kế Hoạch Ngày Mai
                  </div>
                  <div class="bg-sky-50 border border-sky-200 rounded-2xl p-3.5 sm:p-4 text-sm sm:text-base text-sky-950 whitespace-pre-line font-normal leading-relaxed">
                    ${{rep.plan || 'Chưa ghi nhận'}}
                  </div>
                </div>
              </div>
            </div>

            <div class="pt-3.5 border-t border-slate-100 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5">
              ${{(rep.feedback && rep.feedback !== 'Chờ duyệt' && rep.feedback !== '-' && rep.feedback.trim() !== '') ? `
                <div class="text-xs sm:text-sm text-slate-700 flex items-center gap-1.5 bg-blue-50 px-3 py-1.5 rounded-xl border border-blue-200">
                  <span class="font-black text-blue-900 shrink-0">Chỉ đạo:</span>
                  <span class="italic text-slate-800 truncate">${{rep.feedback}}</span>
                </div>
              ` : `<div></div>`}}
              <a href="https://docs.google.com/spreadsheets/d/1_kID0uhutS6Ky_zpB2yW_AQXN2aUKKCKo_6tqZL1kbo/edit#gid=${{SHEET_TABS.find(t=>t.key===u.tabName)?.gid || '0'}}" target="_blank" class="w-full sm:w-auto text-center text-xs sm:text-sm px-4 py-2.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-300 rounded-xl font-black transition flex items-center justify-center gap-1.5 shadow-2xs">
                <span>🟢</span> Mở Tab Trên Google Sheet
              </a>
            </div>
          `;
        }}

        container.appendChild(card);
      }});

      document.getElementById("m-kpi-sub").textContent = `${{subCount}} / ${{users.length}} (${{Math.round(subCount / users.length * 100)}}%)`;
    }}

    function updateExecutiveReportPreview(dateStr) {{
      const users = ACCOUNTS.filter(a => a.type === "USER");
      let subCount = 0;
      const reports = [];

      users.forEach(u => {{
        const rep = findReportForUser(u, dateStr);
        if (rep) {{
          subCount++;
          reports.push({{ user: u, rep: rep }});
        }}
      }});

      const nl = String.fromCharCode(10);
      const lines = [
        "BÁO CÁO CÔNG VIỆC NGÀY: [" + dateStr + "]",
        "Kính gửi Ban Lãnh Đạo,",
        "",
        "Marketing Manager – Trưởng Phòng Marketing xin báo cáo tổng hợp công việc phòng trong ngày (" + subCount + "/" + users.length + " nhân sự đã nộp):",
        "",
        "1️⃣ KẾT QUẢ ĐẠT ĐƯỢC CHÍNH:"
      ];

      reports.forEach(item => {{
        const meaningfulLines = item.rep.res.split(nl).map(s => s.trim()).filter(s => s && !s.match(/^•?\\s*Nhiệm vụ \\d+:?$/i));
        const cleanRes = (meaningfulLines.length > 0 ? meaningfulLines : item.rep.res.split(nl).map(s => s.trim()).filter(Boolean)).slice(0, 2).join('; ');
        lines.push("• " + item.user.name + " (" + item.user.group + "): " + cleanRes);
      }});

      const unsubmitted = users.filter(u => !reports.some(r => r.user.username === u.username));
      if (unsubmitted.length > 0) {{
        lines.push("• Chưa nộp: " + unsubmitted.map(u => u.name).join(', '));
      }}

      lines.push("");
      lines.push("2️⃣ KHÓ KHĂN / VƯỚNG MẮC:");
      lines.push("• Toàn phòng hoạt động nhịp nhàng, chưa phát sinh vướng mắc nghiêm trọng.");
      lines.push("");
      lines.push("3️⃣ BÀI HỌC KINH NGHIỆM / ĐỀ XUẤT:");
      lines.push("• Tiếp tục tối ưu hóa chiến dịch banner & video review phục vụ đợt khuyến mãi sắp tới.");
      lines.push("");
      lines.push("4️⃣ KẾ HOẠCH CÔNG VIỆC NGÀY MAI:");

      reports.forEach(item => {{
        if (item.rep.plan) {{
          const meaningfulPlanLines = item.rep.plan.split(nl).map(s => s.trim()).filter(s => s && !s.match(/^•?\\s*Nhiệm vụ \\d+:?$/i));
          const cleanPlan = (meaningfulPlanLines.length > 0 ? meaningfulPlanLines[0] : item.rep.plan.split(nl).map(s => s.trim()).filter(Boolean)[0]) || 'Tiếp tục triển khai công việc';
          lines.push("• " + item.user.name + ": " + cleanPlan);
        }}
      }});

      const el = document.getElementById("executive-report-text");
      if (el) el.textContent = lines.join(nl);
    }}

    // ========================================================
    // AUTO LIVE SYNC ENGINE (CLIENT-SIDE DIRECT GOOGLE SHEETS)
    // ========================================================
    const SPREADSHEET_ID = "1_kID0uhutS6Ky_zpB2yW_AQXN2aUKKCKo_6tqZL1kbo";
    let isLiveSyncing = false;

    function fetchGvizJsonp(gid) {{
      return new Promise((resolve, reject) => {{
        const cbName = 'gviz_jsonp_' + gid + '_' + Date.now() + '_' + Math.floor(Math.random() * 100000);
        const script = document.createElement('script');
        let done = false;

        const timeout = setTimeout(() => {{
          if (!done) {{
            done = true;
            cleanup();
            reject(new Error('JSONP timeout gid ' + gid));
          }}
        }}, 12000);

        function cleanup() {{
          try {{ delete window[cbName]; }} catch(e) {{}}
          if (script.parentNode) script.parentNode.removeChild(script);
        }}

        window[cbName] = function(data) {{
          if (!done) {{
            done = true;
            clearTimeout(timeout);
            cleanup();
            resolve(data);
          }}
        }};

        script.onerror = function(err) {{
          if (!done) {{
            done = true;
            clearTimeout(timeout);
            cleanup();
            reject(err);
          }}
        }};

        script.src = `https://docs.google.com/spreadsheets/d/${{SPREADSHEET_ID}}/gviz/tq?tqx=responseHandler:${{cbName}}&gid=${{gid}}&t=${{Date.now()}}`;
        document.head.appendChild(script);
      }});
    }}

    async function autoSyncLiveGoogleSheets(silent = true) {{
      if (isLiveSyncing) return;
      isLiveSyncing = true;
      const statusBadge = document.getElementById("live-sync-indicator");
      
      if (statusBadge) {{
        statusBadge.innerHTML = `<span class="animate-spin inline-block">🔄</span> <span>Đang đồng bộ...</span>`;
      }}

      try {{
        // 1. Fetch Master sheet BAO CAO HOM NAY live via JSONP (Bypasses CORS completely on GitHub Pages)
        const masterJson = await fetchGvizJsonp('187266668');
        if (masterJson && masterJson.table && masterJson.table.rows) {{
          const parsedRows = masterJson.table.rows.map(r => {{
            return r.c ? r.c.map(cell => (cell ? (cell.f !== undefined ? cell.f : (cell.v !== undefined && cell.v !== null ? String(cell.v) : "")) : "")) : [];
          }});

          if (!window.ALL_SHEETS_DATA) window.ALL_SHEETS_DATA = {{}};
          window.ALL_SHEETS_DATA['BAO CAO HOM NAY'] = {{
            sheetId: 187266668,
            index: 0,
            rows: parsedRows
          }};
        }}

        // 2. Fetch all staff individual tabs asynchronously in parallel via JSONP
        await syncAllStaffTabsLive();

        // 3. Re-render views with freshest live data
        renderQuickDateChips();
        if (currentAppMainTab === 'cards') {{
          renderManagerCards(managerSelectedDate);
          updateExecutiveReportPreview(managerSelectedDate);
        }} else if (currentAppMainTab === 'sheets') {{
          renderActiveSheetHtml(currentActiveSheetKey);
        }}

        const nowTime = new Date().toLocaleTimeString('vi-VN', {{ hour: '2-digit', minute: '2-digit', second: '2-digit' }});
        if (statusBadge) {{
          statusBadge.innerHTML = `<span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span> <span>Auto Live (${{nowTime}})</span>`;
        }}

        if (!silent) {{
          showToast("Đã đồng bộ Live!", "Số liệu mới nhất từ Google Sheets đã được cập nhật thành công.", "success");
        }}
      }} catch (err) {{
        console.warn("Live sync warning:", err);
        if (statusBadge) {{
          statusBadge.innerHTML = `<span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span> <span>Live Google Sheets</span>`;
        }}
      }} finally {{
        isLiveSyncing = false;
      }}
    }}

    async function syncAllStaffTabsLive() {{
      const promises = SHEET_TABS.filter(t => t.key !== 'BAO CAO HOM NAY' && t.key !== 'BAO CAO TUAN').map(async (tab) => {{
        try {{
          const data = await fetchGvizJsonp(tab.gid);
          if (data && data.table && data.table.rows) {{
            const rows = data.table.rows.map(r => {{
              return r.c ? r.c.map(cell => (cell ? (cell.f !== undefined ? cell.f : (cell.v !== undefined && cell.v !== null ? String(cell.v) : "")) : "")) : [];
            }});
            window.ALL_SHEETS_DATA[tab.key] = {{
              sheetId: parseInt(tab.gid),
              index: tab.index,
              rows: rows
            }};
          }}
        }} catch(e) {{
          // Silent fallback to existing cache
        }}
      }});

      await Promise.all(promises);
    }}

    function copyExecutiveSummaryReport() {{
      const text = document.getElementById("executive-report-text").textContent;
      navigator.clipboard.writeText(text).then(() => {{
        showToast("Đã sao chép báo cáo!", "Báo cáo tổng hợp toàn phòng đã sẵn sàng gửi Ban Giám Đốc.", "success");
      }});
    }}

    // ========================================================
    // 4. PERSONAL SUBMIT SPACE LOGIC
    // ========================================================
    function renderQuickLoginButtons() {{
      const grid = document.getElementById("quick-users-grid");
      const modalGrid = document.getElementById("modal-quick-users-grid");

      const populate = (targetGrid, isModal = false) => {{
        if (!targetGrid) return;
        targetGrid.innerHTML = "";
        ACCOUNTS.forEach(u => {{
          const theme = getRoleColorTheme(u.group);
          const btn = document.createElement("button");
          btn.type = "button";
          btn.onclick = () => {{
            if (doLoginByPassword(u.pin)) {{
              if (isModal) {{
                closeLoginModal();
                if (pendingRedirectTab) {{
                  switchMainAppTab(pendingRedirectTab);
                  pendingRedirectTab = null;
                }}
              }}
            }}
          }};
          const isAdmin = u.type === "ADMIN";
          btn.className = `p-2.5 rounded-2xl border text-left transition flex items-center justify-between gap-2 shadow-2xs hover:shadow-xs ${{isAdmin ? 'bg-amber-50 border-amber-300 hover:bg-amber-100 col-span-2' : 'bg-white hover:bg-slate-50 border-slate-200'}}`;
          btn.innerHTML = `
            <div class="flex items-center gap-2.5 overflow-hidden">
              <span class="text-xl ${{theme.avatarBg}} w-9 h-9 rounded-xl border flex items-center justify-center shrink-0 shadow-2xs">${{u.avatar}}</span>
              <div class="truncate">
                <p class="font-extrabold text-slate-900 text-xs sm:text-sm truncate">${{u.name}}</p>
                <div class="flex items-center gap-1 mt-0.5">
                  <span class="text-[9px] px-1.5 py-0.2 rounded font-extrabold ${{theme.badgeBg}}">${{u.group}}</span>
                  <span class="text-[9px] text-slate-500 truncate">${{u.role}}</span>
                </div>
              </div>
            </div>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded-lg font-bold shrink-0 ${{isAdmin ? 'bg-amber-200 text-amber-900' : 'bg-slate-100 text-slate-700 border border-slate-200'}}">PIN: ${{u.pin}}</span>
          `;
          targetGrid.appendChild(btn);
        }});
      }};

      populate(grid, false);
      populate(modalGrid, true);
    }}

    function handlePasswordOnlySubmit(e) {{
      e.preventDefault();
      const p = document.getElementById("login-password").value.trim().toLowerCase();
      doLoginByPassword(p);
    }}

    function doLoginByPassword(pass) {{
      if (!pass) return false;
      const clean = pass.toLowerCase();
      const user = ACCOUNTS.find(a => a.password.toLowerCase() === clean || a.pin.toLowerCase() === clean || a.username.toLowerCase() === clean);
      if (user) {{
        currentUser = user;
        localStorage.setItem("kingblue_user", JSON.stringify(user));
        showToast("Đăng nhập thành công!", `Chào mừng ${{user.name}}`, "success");
        updateUserSessionBar();
        renderSubmitSpace();
        return true;
      }} else {{
        showToast("Mật khẩu không đúng!", "Vui lòng nhập đúng mã PIN được cấp.", "error");
        return false;
      }}
    }}

    function handleLogout() {{
      currentUser = null;
      localStorage.removeItem("kingblue_user");
      showToast("Đã đăng xuất", "Quay về Thẻ công việc hôm nay", "info");
      updateUserSessionBar();
      renderSubmitSpace();
      switchMainAppTab('cards');
    }}

    function updateUserSessionBar() {{
      const bar = document.getElementById("user-info-bar");
      const btnLogin = document.getElementById("btn-open-login");
      const iconLockSheets = document.getElementById("icon-lock-sheets");

      if (currentUser) {{
        bar.classList.remove("hidden");
        if (btnLogin) btnLogin.classList.add("hidden");
        document.getElementById("current-user-name").textContent = currentUser.name;
        document.getElementById("current-user-avatar").textContent = currentUser.avatar;
        if (iconLockSheets) iconLockSheets.textContent = "📑";
      }} else {{
        bar.classList.add("hidden");
        if (btnLogin) btnLogin.classList.remove("hidden");
        if (iconLockSheets) iconLockSheets.textContent = "🔒";
      }}
    }}

    function renderSubmitSpace() {{
      const loginBox = document.getElementById("submit-login-box");
      const formBox = document.getElementById("submit-form-box");

      if (!currentUser) {{
        loginBox.classList.remove("hidden");
        formBox.classList.add("hidden");
      }} else {{
        loginBox.classList.add("hidden");
        formBox.classList.remove("hidden");

        document.getElementById("emp-avatar").textContent = currentUser.avatar;
        document.getElementById("emp-name").textContent = currentUser.name;
        document.getElementById("emp-group").textContent = currentUser.group;
        document.getElementById("emp-role").textContent = currentUser.role;
        document.getElementById("emp-tab-name").textContent = currentUser.tabName;
        document.getElementById("emp-form-date").value = "05/10/2026";
      }}
    }}

    async function handleEmployeeSubmit(e) {{
      e.preventDefault();
      const submitBtn = document.getElementById("btn-emp-submit");
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span>⏳</span> Đang lưu vào hệ thống...`;

      const now = new Date();
      const timeStr = now.toTimeString().split(' ')[0];
      const hours = now.getHours();
      const minutes = now.getMinutes();
      const isOnTime = (hours < 17) || (hours === 17 && minutes <= 30);
      const statusStr = isOnTime ? "Đúng hạn" : "Nộp muộn";

      const dateStr = document.getElementById("emp-form-date").value.trim() || "05/10/2026";
      const resVal = document.getElementById("emp-res").value.trim();
      const diffVal = document.getElementById("emp-diff").value.trim() || "• Không có";
      const lessonVal = document.getElementById("emp-lesson").value.trim() || "• Không có";
      const planVal = document.getElementById("emp-plan").value.trim();
      const linkVal = document.getElementById("emp-link").value.trim() || "-";

      try {{
        await fetch("/api/submit", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            username: currentUser.username,
            date: dateStr,
            res: resVal,
            diff: diffVal,
            lesson: lessonVal,
            plan: planVal,
            link: linkVal
          }})
        }});
      }} catch(err) {{}}

      submitBtn.disabled = false;
      submitBtn.innerHTML = `<span>🚀</span> LƯU & GỬI BÁO CÁO CÔNG VIỆC`;

      openCompletionModal({{
        name: currentUser.name,
        avatar: currentUser.avatar,
        date: dateStr,
        time: timeStr,
        status: statusStr
      }});
    }}

    function openCompletionModal(data) {{
      document.getElementById("modal-emp-name").innerHTML = `<span>${{data.avatar}}</span> ${{data.name}}`;
      document.getElementById("modal-date").textContent = data.date;
      document.getElementById("modal-time").textContent = data.time;
      const statusEl = document.getElementById("modal-status");
      statusEl.className = `font-bold px-2.5 py-0.5 rounded-md text-[11px] ${{data.status === 'Đúng hạn' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}}`;
      statusEl.textContent = data.status === 'Đúng hạn' ? '🟢 Đúng hạn (Trước 17:30)' : '🔴 Nộp muộn';
      document.getElementById("modal-completion").classList.remove("hidden");
    }}

    function closeCompletionModal() {{
      document.getElementById("modal-completion").classList.add("hidden");
    }}

    function showToast(title, desc, type = "success") {{
      const toast = document.getElementById("toast");
      const icon = document.getElementById("toast-icon");
      document.getElementById("toast-title").textContent = title;
      document.getElementById("toast-desc").textContent = desc;
      icon.textContent = type === "success" ? "✅" : (type === "error" ? "❌" : "ℹ️");

      toast.classList.remove("translate-y-[-100px]", "opacity-0", "pointer-events-none");
      toast.classList.add("translate-y-0", "opacity-100");

      setTimeout(() => {{
        toast.classList.remove("translate-y-0", "opacity-100");
        toast.classList.add("translate-y-[-100px]", "opacity-0", "pointer-events-none");
      }}, 3500);
    }}
  </script>
</body>
</html>
'''

with open('website_tong_hop_bao_cao.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Generated website_tong_hop_bao_cao.html and index.html successfully!')

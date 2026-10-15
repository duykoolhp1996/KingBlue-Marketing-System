import csv
import os
import openpyxl

wb = openpyxl.load_workbook("KingBlue_Du_Lieu_Chuan_SQL.xlsx", data_only=False)

os.makedirs("database/csv_tables", exist_ok=True)

name_map = {
    "1_Data_Phang_Chuan_1NF": "database/csv_tables/1_data_phang_chuan_1nf.csv",
    "2_Khach_Hang": "database/csv_tables/2_khach_hang.csv",
    "3_Gian_Hang_TMDT": "database/csv_tables/3_gian_hang_tmdt.csv",
    "4_Danh_Muc_San_Pham": "database/csv_tables/4_danh_muc_san_pham.csv",
    "5_Kiem_Tra_Gia_San": "database/csv_tables/5_kiem_tra_gia_san.csv"
}

for sheetname, filepath in name_map.items():
    ws = wb[sheetname]
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        for row in ws.iter_rows(values_only=True):
            writer.writerow(row)
    print(f"Exported: {filepath}")


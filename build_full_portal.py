import json
import os

with open('all_sheets_data.json', 'r', encoding='utf-8') as f:
    sheets_data = json.load(f)

# Also ensure sheets_data.js is updated
with open('sheets_data.js', 'w', encoding='utf-8') as f:
    f.write('window.ALL_SHEETS_DATA = ' + json.dumps(sheets_data, ensure_ascii=False, indent=2) + ';\n')

print('sheets_data.js generated successfully!')

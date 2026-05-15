# -*- coding: utf-8 -*-
import csv
import re
import os

DETAIL_FILE = r'C:\Users\paink\Desktop\51job_detail.csv'
LIST_FILE = r'C:\Users\paink\Desktop\51job_列表采集结果.csv'
OUTPUT_FILE = r'C:\Users\paink\Desktop\51job_merged.csv'

# ---- 1. 读取 detail CSV，只保留标题链接 + 职位信息_全文 ----
detail_map = {}  # url -> 职位信息_全文（清洗后）

# 需要从职位信息全文中去除的尾部垃圾模式
STRIP_PATTERNS = [
    r'职能类别：.*',
    r'工作地址.*',
    r'上班地址：.*',
    r'查看地图.*',
    r'51Job安全提醒.*',
    r'求职过程中.*',
    r'公司信息.*',
    r'登录享受更多.*',
    r'\+86\s*.*',
    r'发送验证码.*',
    r'APP下载.*',
]

def clean_full_text(text):
    """去掉职位信息_全文中的冗余部分，只保留核心职位描述。"""
    if not text:
        return ''
    # 去掉开头的"职位信息"标题行
    text = re.sub(r'^职位信息\s*\n?', '', text, flags=re.MULTILINE)
    # 找到第一个噪音段落的位置，截断
    cut_pos = len(text)
    for pattern in STRIP_PATTERNS:
        m = re.search(pattern, text, flags=re.DOTALL | re.MULTILINE)
        if m and m.start() < cut_pos:
            cut_pos = m.start()
    text = text[:cut_pos].strip()
    return text

with open(DETAIL_FILE, encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row.get('标题链接', '').strip()
        full_text = (row.get('职位信息_全文') or '').strip()
        cleaned = clean_full_text(full_text)
        if url:
            detail_map[url] = cleaned

print(f'[detail] 共读取 {len(detail_map)} 条记录')

# ---- 2. 读取列表 CSV ----
list_rows = []
list_fieldnames = []

with open(LIST_FILE, encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    list_fieldnames = reader.fieldnames[:]
    for row in reader:
        list_rows.append(row)

print(f'[列表] 共读取 {len(list_rows)} 条记录')

# ---- 3. 合并：在列表末尾插入"职位信息_全文"列 ----
NEW_COL = '职位信息_全文'
if NEW_COL not in list_fieldnames:
    list_fieldnames.append(NEW_COL)

matched = 0
for row in list_rows:
    url = row.get('标题链接', '').strip()
    job_text = detail_map.get(url, '')
    row[NEW_COL] = job_text
    if job_text:
        matched += 1

print(f'[合并] 匹配到职位描述的记录数：{matched} / {len(list_rows)}')

# ---- 4. 写出结果 ----
with open(OUTPUT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list_fieldnames)
    writer.writeheader()
    writer.writerows(list_rows)

print(f'[完成] 已保存到: {OUTPUT_FILE}')

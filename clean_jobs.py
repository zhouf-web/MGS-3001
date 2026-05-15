# -*- coding: utf-8 -*-
"""
51job_merged.csv 清洗脚本
- 去重: 所有栏位完全相同的行
- 删除整列全空的废列 (er2, 采集时间)
- 删除栏位错位的脏行 (抓取时间格式异常, 字段1 含日期串等)
- 删除职位信息_全文 为空的行
"""
import csv
import re
import sys

INPUT_FILE = r'C:\Users\paink\Downloads\data\mgs3001\项目\51job_merged.csv'
OUTPUT_FILE = r'C:\Users\paink\Downloads\data\mgs3001\项目\51job_cleaned.csv'

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$')
DATE_FRAG_RE = re.compile(r'\d{2}-\d{2}-\d{2}')  # 形如 26-05-12 的错位片段

with open(INPUT_FILE, encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fields = reader.fieldnames[:]

total = len(rows)
print(f'[原始] {total} 行, {len(fields)} 列')

# ---- 1. 删除整列全空的废列 ----
empty_cols = [c for c in fields if all(not (r.get(c) or '').strip() for r in rows)]
print(f'[废列] 全空列 = {empty_cols} -> 删除')
fields = [c for c in fields if c not in empty_cols]

# ---- 2. 删除栏位错位的行 ----
def is_misaligned(r):
    # 抓取时间不符合 YYYY-MM-DD HH:MM:SS 格式
    t = (r.get('抓取时间') or '').strip()
    if t and not DATE_RE.match(t):
        return True
    # 字段1 (公司规模) 里出现日期串, 说明错位
    f1 = (r.get('字段1') or '').strip()
    if DATE_FRAG_RE.search(f1):
        return True
    return False

misaligned = [r for r in rows if is_misaligned(r)]
rows = [r for r in rows if not is_misaligned(r)]
print(f'[错位] 删除 {len(misaligned)} 行')

# ---- 3. 删除职位信息_全文 为空的行 ----
before = len(rows)
rows = [r for r in rows if (r.get('职位信息_全文') or '').strip()]
print(f'[空描述] 删除 {before - len(rows)} 行')

# ---- 4. 完全相同行去重 (按保留后的列计算签名) ----
seen = set()
deduped = []
for r in rows:
    sig = tuple((r.get(c) or '').strip() for c in fields)
    if sig in seen:
        continue
    seen.add(sig)
    deduped.append(r)
print(f'[去重] 删除 {len(rows) - len(deduped)} 行 (完全相同)')
rows = deduped

# ---- 5. 写出 ----
with open(OUTPUT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

print(f'[完成] {total} -> {len(rows)} 行, 已保存到: {OUTPUT_FILE}')

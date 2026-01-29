import csv
import json
import os

def read_json(file_path):
    """Read JSON"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def export_json(data, file_path):
    """Read JSON"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Success output JSON to: {file_path}")

def read_csv(file_path):
    """Read CSV file"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return list(reader)

def export_csv(data, file_path):
    """output CSV file"""
    if not data:
        return
    
    headers = data[0].keys()
    
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"Success output CSV to: {file_path}")
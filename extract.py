import json
import os

# 确保文件名与你仓库中的完全一致
JSON_FILE = "humaneval-decompile.json"
OUTPUT_DIR = "src_code"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def main():
    if not os.path.exists(JSON_FILE):
        print(f"❌ Error: {JSON_FILE} not found!")
        return

    print(f"Opening {JSON_FILE}...")
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
            
        if not isinstance(data_list, list):
            print("❌ Error: JSON content is not a list/array!")
            return

        print(f"Found {len(data_list)} items. Starting extraction...")

        count = 0
        for item in data_list:
            # 匹配你提供的键名
            idx = item.get('index', count)
            header = item.get('func_dep', '')
            body = item.get('func', '')
            lang = str(item.get('language', 'cpp')).lower()
            
            if not body:
                continue

            # 决定扩展名
            ext = ".cpp" if lang in ["cpp", "c++"] else ".c"
            
            # 拼接完整代码
            full_code = f"{header}\n{body}"
            
            # 保存文件
            file_name = f"problem{idx}{ext}"
            file_path = os.path.join(OUTPUT_DIR, file_name)
            
            with open(file_path, 'w', encoding='utf-8') as cf:
                cf.write(full_code)
            count += 1

        print(f"✅ Success: Generated {count} files in '{OUTPUT_DIR}'")

    except Exception as e:
        print(f"❌ Failed to process JSON: {e}")

if __name__ == "__main__":
    main()
import requests
import xml.etree.ElementTree as ET
from typing import List
from core.html_base import HtmlBaseParser

class PexipConferencingNodesParser(HtmlBaseParser):
    """
    Парсер для Pexip Infinity Generic Conferencing Node (.ova).
    """
    # Базовий URL для скачування (S3 bucket)
    S3_BASE_URL = "https://pexip-download.s3-eu-west-1.amazonaws.com/"
    
    # URL для отримання списку папок версій
    S3_LIST_URL = "https://pexip-download.s3-eu-west-1.amazonaws.com/?list-type=2&delimiter=/&prefix=infinity/"

    def get_versions(self) -> List[str]:
        results = []

        try:
            # 1. Отримуємо список версій (папок)
            response = requests.get(self.S3_LIST_URL, timeout=10)
            if response.status_code != 200:
                print(f"[ERROR] Pexip Generic S3 error: {response.status_code}")
                return []

            root = ET.fromstring(response.content)

            # Допоміжна функція пошуку без namespace
            def find_tags(node, suffix):
                return [child for child in node.iter() if child.tag.endswith(suffix)]

            # 2. Збираємо папки версій (infinity/vXX.X/)
            valid_folders = []
            for cp in find_tags(root, 'CommonPrefixes'):
                for p in find_tags(cp, 'Prefix'):
                    raw_prefix = p.text # infinity/v38.1/
                    if not raw_prefix: continue

                    folder_name = raw_prefix.rstrip('/').split('/')[-1]
                    
                    # Перевіряємо формат vXX або vXX.X
                    if folder_name.startswith('v') and folder_name[1:].replace('.', '').isdigit():
                        valid_folders.append({
                            'ver_str': folder_name.lstrip('v'),
                            's3_prefix': raw_prefix
                        })

            # Сортуємо версії
            valid_folders.sort(
                key=lambda x: [int(u) for u in x['ver_str'].split('.') if u.isdigit()],
                reverse=True
            )

            # 3. Шукаємо файл generic_ConfNode у кожній версії
            for item in valid_folders:
                ver_number = item['ver_str']
                prefix = item['s3_prefix']
                
                # Запит вмісту конкретної папки
                folder_url = f"https://pexip-download.s3-eu-west-1.amazonaws.com/?list-type=2&prefix={prefix}"

                try:
                    res_folder = requests.get(folder_url, timeout=5)
                    if res_folder.status_code != 200: continue
                    
                    f_root = ET.fromstring(res_folder.content)
                    
                    found = False
                    for content in find_tags(f_root, 'Contents'):
                        for key_node in find_tags(content, 'Key'):
                            file_path = key_node.text
                            # Приклад: infinity/v38.1/Pexip_Infinity_v38.1_generic_ConfNode_81931.ova
                            
                            # === ФІЛЬТР ТУТ ===
                            if file_path and file_path.endswith('.ova') and 'generic_ConfNode' in file_path:
                                full_link = f"{self.S3_BASE_URL}{file_path}"
                                results.append(f"{ver_number} {full_link}")
                                found = True
                                break
                        if found: break
                
                except Exception as e:
                    print(f"[WARN] Error scanning folder {prefix}: {e}")
                    continue

        except Exception as e:
            print(f"[CRITICAL] Pexip Generic Parser Error: {e}")

        return results

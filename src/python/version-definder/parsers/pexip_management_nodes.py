import requests
import xml.etree.ElementTree as ET
from typing import List
from core.html_base import HtmlBaseParser

class PexipManagementNodesParser(HtmlBaseParser):
    # Базовий URL для побудови посилань на скачування
    S3_BASE_URL = "https://pexip-download.s3-eu-west-1.amazonaws.com/"
    
    # URL для отримання списку папок (версій)
    S3_LIST_URL = "https://pexip-download.s3-eu-west-1.amazonaws.com/?list-type=2&delimiter=/&prefix=infinity/"

    def get_versions(self) -> List[str]:
        results = []

        try:
            # 1. Запит до S3 для отримання кореневого списку папок
            # Використовуємо stream=True, щоб не тягнути зайві дані, якщо відповідь величезна
            response = requests.get(self.S3_LIST_URL, timeout=10)
            if response.status_code != 200:
                print(f"[ERROR] Pexip S3 повернув помилку: {response.status_code}")
                return []

            # Парсимо XML
            root = ET.fromstring(response.content)

            # Допоміжна функція для пошуку тегів, ігноруючи Namespace (xmlns)
            # S3 часто повертає XML з namespace, тому find('Prefix') може не спрацювати без нього.
            def find_tags(node, suffix):
                return [child for child in node.iter() if child.tag.endswith(suffix)]

            # 2. Витягуємо версії з <CommonPrefixes><Prefix>infinity/vXX.X/</Prefix>
            valid_folders = []
            
            for cp in find_tags(root, 'CommonPrefixes'):
                for p in find_tags(cp, 'Prefix'):
                    raw_prefix = p.text  # Наприклад: "infinity/v38.1/"
                    
                    if not raw_prefix:
                        continue

                    # Чистимо назву: "infinity/v38.1/" -> "v38.1"
                    folder_name = raw_prefix.rstrip('/').split('/')[-1]
                    
                    # Перевіряємо формат: має починатися на 'v' і містити цифри (наприклад v38 або v38.1)
                    # Видаляємо крапки, щоб перевірити isdigit (для 38.1)
                    if folder_name.startswith('v') and folder_name[1:].replace('.', '').isdigit():
                        valid_folders.append({
                            'ver_str': folder_name.lstrip('v'), # "38.1"
                            's3_prefix': raw_prefix             # "infinity/v38.1/"
                        })

            # Сортуємо версії (від нових до старих)
            # Використовуємо list comprehension для розбивки "38.1" -> [38, 1] для коректного порівняння
            valid_folders.sort(
                key=lambda x: [int(u) for u in x['ver_str'].split('.') if u.isdigit()],
                reverse=True
            )

            # 3. Проходимо по кожній версії, щоб знайти конкретний файл .ova
            for item in valid_folders:
                ver_number = item['ver_str']
                prefix = item['s3_prefix'] 

                # URL для отримання вмісту конкретної папки
                # Прибираємо delimiter, щоб побачити файли (Key)
                folder_content_url = f"https://pexip-download.s3-eu-west-1.amazonaws.com/?list-type=2&prefix={prefix}"

                try:
                    res_folder = requests.get(folder_content_url, timeout=5)
                    if res_folder.status_code != 200:
                        continue
                    
                    folder_root = ET.fromstring(res_folder.content)
                    
                    # Шукаємо <Contents><Key>...ova</Key>
                    found_file = False
                    for content_block in find_tags(folder_root, 'Contents'):
                        for key_node in find_tags(content_block, 'Key'):
                            file_path = key_node.text 
                            # file_path приклад: infinity/v38.1/Pexip_Infinity_v38.1_pxMgr_VMware.ova
                            
                            # Нам потрібен файл Management Node (pxMgr), формат OVA (для VMware)
                            if file_path and file_path.endswith('.ova') and 'pxMgr' in file_path:
                                full_link = f"{self.S3_BASE_URL}{file_path}"
                                
                                # Додаємо в результати: "ВЕРСІЯ ПОСИЛАННЯ"
                                results.append(f"{ver_number} {full_link}")
                                
                                found_file = True
                                break 
                        
                        if found_file:
                            break

                except Exception as e:
                    # Ігноруємо помилки окремих папок, йдемо далі
                    print(f"[WARN] Помилка обробки версії {ver_number}: {e}")
                    continue

        except Exception as e:
            print(f"[CRITICAL] Глобальна помилка парсингу Pexip: {e}")

        return results

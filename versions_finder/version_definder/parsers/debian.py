import re
from typing import List
from .html_base import HtmlBaseParser

class DebianCloudParser(HtmlBaseParser):
    BASE_URL = "https://cloud.debian.org/images/cloud/"

    def get_versions(self) -> List[str]:
        results = []
        seen_versions = set()

        # 1. Отримуємо список папок (тут помилки нам потрібні, тому quiet=False за замовчуванням)
        all_links = self.fetch_and_parse_links(
            self.BASE_URL,
            lambda x: True 
        )

        for link in all_links:
            raw_folder = link.strip('/')

            # Шукаємо тільки папки з '-backports'
            if '-backports' not in raw_folder:
                continue

            # Відрізаємо хвіст: "bullseye-backports" -> "bullseye"
            target_folder = raw_folder.replace('-backports', '')
            target_url = f"{self.BASE_URL}{target_folder}/latest/"
            
            # === ЗМІНА ТУТ: додали quiet=True ===
            # Ми передаємо quiet=True, щоб при помилці 403 (як у stretch) 
            # програма просто промовчала і пішла далі.
            files = self.fetch_and_parse_links(
                target_url,
                lambda x: x.endswith('.qcow2') and 'generic' in x and 'amd64' in x,
                quiet=True  # <--- Тихий режим
            )
            
            if files:
                filename = files[0]
                match = re.search(r'debian-(\d+)-', filename)
                
                if match:
                    version_num = match.group(1)
                    full_link = f"{target_url}{filename}"
                    
                    if version_num not in seen_versions:
                        results.append(f"{version_num} {full_link}")
                        seen_versions.add(version_num)

        return sorted(results, key=lambda x: int(x.split()[0]), reverse=True)

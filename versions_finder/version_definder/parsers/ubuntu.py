from typing import List
from .html_base import HtmlBaseParser

class UbuntuParser(HtmlBaseParser):
    BASE_URL = "https://cloud-images.ubuntu.com/releases/"

    def get_versions(self) -> List[str]:
        results = []

        # Логіка фільтрації LTS (з вашого оригінального файлу)
        def is_lts(version_str):
            parts = version_str.split('.')
            if len(parts) == 2 and parts[0].isdigit() and parts[1] == '04':
                return int(parts[0]) % 2 == 0
            return False

        # 1. Отримуємо список папок версій
        versions = self.fetch_and_parse_links(self.BASE_URL, is_lts)
        versions = self.sort_versions(versions)

        # 2. Проходимо по кожній версії
        for ver in versions:
            release_url = f"{self.BASE_URL}{ver}/release/"
            
            # Шукаємо файл .ova
            files = self.fetch_and_parse_links(
                release_url, 
                lambda x: x.endswith('.ova') and 'amd64' in x
            )
            
            if files:
                file_name = files[0]
                full_link = f"{release_url}{file_name}"
                
                # Повертаємо рядок для bash-скрипта: "VER LINK"
                results.append(f"{ver} {full_link}")
        
        return results

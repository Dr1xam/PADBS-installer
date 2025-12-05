from typing import List
from .html_base import HtmlBaseParser

class ZabbixParser(HtmlBaseParser):
    BASE_URL = "https://cdn.zabbix.com/zabbix/appliances/stable/"

    def get_versions(self) -> List[str]:
        results = []

        # 1. Шукаємо мажорні версії (наприклад, 7.0), що закінчуються на .0
        majors = self.fetch_and_parse_links(
            self.BASE_URL, 
            lambda x: x.endswith('.0')
        )
        majors = self.sort_versions(majors)

        # 2. Проходимо по кожній версії
        for major in majors:
            major_url = f"{self.BASE_URL}{major}/"
            
            # Шукаємо патчі всередині (наприклад 7.0.21)
            patches = self.fetch_and_parse_links(
                major_url, 
                lambda x: x.startswith(major) and x.replace('.', '').isdigit()
            )
            
            if patches:
                latest_patch = self.sort_versions(patches)[0]
                
                # Формуємо посилання (OVF)
                file_name = f"zabbix_appliance-{latest_patch}-ovf.tar.gz"
                full_link = f"{major_url}{latest_patch}/{file_name}"
                
                # Повертаємо рядок: "VER LINK"
                results.append(f"{major} {full_link}")
        
        return results

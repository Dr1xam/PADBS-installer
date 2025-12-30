from core.snap_base import SnapBaseParser

class CoreSnapsParser(SnapBaseParser):
    def __init__(self):
        # Ініціалізуємо батьківський клас з заглушкою,
        # оскільки ми будемо змінювати self.package_name динамічно.
        super().__init__(package_name="core")
        
        # Список пакетів Ubuntu Core, які нас цікавлять
        self.target_cores = ["core18", "core20", "core22", "core24"]

    def get_versions(self) -> list:
        results = []

        for core_name in self.target_cores:
            # 1. Підміняємо назву пакету для поточного запиту
            self.package_name = core_name
            
            # 2. Виконуємо запит до API (використовуємо логіку батьківського класу)
            data = self._fetch_snap_info()
            
            # Якщо даних немає або помилка — пропускаємо
            if not data:
                continue

            # 3. Шукаємо стабільну версію
            channels = data.get("channel-map", [])
            candidates = []

            for item in channels:
                channel_info = item.get("channel", {})
                risk = channel_info.get("risk")
                arch = channel_info.get("architecture")
                
                version = item.get("version")
                download_url = item.get("download", {}).get("url")

                # Фільтруємо: ТІЛЬКИ stable, ТІЛЬКИ amd64
                if risk == "stable" and arch == "amd64" and version and download_url:
                    candidates.append({
                        "version": version,
                        "url": download_url
                    })

            if candidates:
                # 4. Сортуємо версії (від нових до старих)
                # Версії core часто виглядають як дати (напр. 20230530) або numbers (16-2.61.4)
                # Використовуємо універсальне сортування по числах у версії
                candidates.sort(
                    key=lambda x: [int(u) for u in x['version'].replace('-', '.').split('.') if u.isdigit()], 
                    reverse=True
                )

                # Беремо найновішу
                latest = candidates[0]
                
                # Формуємо рядок: "НАЗВА ВЕРСІЯ ЛІНК"
                # Наприклад: core22 20240115 https://...
                results.append(f"{core_name} {latest['version']} {latest['url']}")

        return results

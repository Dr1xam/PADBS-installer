from core.snap_base import SnapBaseParser

class RocketChatParser(SnapBaseParser):
    def __init__(self):
        super().__init__(package_name="rocketchat-server")

    def get_versions(self) -> list:
        data = self._fetch_snap_info()
        results = []
        seen = set()

        # Отримуємо карту каналів з API
        channels = data.get("channel-map", [])

        for item in channels:
            channel_info = item.get("channel", {})
            risk = channel_info.get("risk")    
            # --- ДОДАНО ПЕРЕВІРКУ АРХІТЕКТУРИ ---
            arch = channel_info.get("architecture") 
            
            version = item.get("version")
            download_url = item.get("download", {}).get("url")

            # Фільтруємо: ТІЛЬКИ стабільні та ТІЛЬКИ для стандартних ПК/серверів (amd64)
            if risk == "stable" and arch == "amd64" and version and download_url:
                ver_string = f"{version} {download_url}"

                if ver_string not in seen:
                    results.append(ver_string)
                    seen.add(ver_string)

        # Сортуємо результати (найновіші версії будуть зверху)
        return sorted(results, key=lambda x: x.split()[0], reverse=True)

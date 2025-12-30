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
            risk = channel_info.get("risk")    # напр. "stable"
            
            # Витягуємо реальну версію та посилання
            version = item.get("version")
            download_url = item.get("download", {}).get("url")

            # Фільтруємо лише стабільні релізи
            if risk == "stable" and version and download_url:
                # Формуємо рядок: "ВЕРСІЯ ПОСИЛАННЯ"
                ver_string = f"{version} {download_url}"

                if ver_string not in seen:
                    results.append(ver_string)
                    seen.add(ver_string)

        # Сортуємо за версією у зворотному порядку
        return sorted(results, reverse=True)

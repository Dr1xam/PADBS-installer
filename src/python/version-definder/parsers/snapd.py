from core.snap_base import SnapBaseParser

class SnapdParser(SnapBaseParser):
    def __init__(self):
        # Вказуємо назву пакету в Snap Store
        super().__init__(package_name="snapd")

    def get_versions(self) -> list:
        data = self._fetch_snap_info()
        stable_releases = []

        # Отримуємо карту каналів з API
        channels = data.get("channel-map", [])

        for item in channels:
            channel_info = item.get("channel", {})
            risk = channel_info.get("risk")
            # --- НОВА ПЕРЕВІРКА ТУТ ---
            arch = channel_info.get("architecture") 
            
            version = item.get("version")
            download_url = item.get("download", {}).get("url")

            # Фільтруємо: ТІЛЬКИ стабільні, ТІЛЬКИ amd64 та з посиланням
            if risk == "stable" and arch == "amd64" and version and download_url:
                stable_releases.append({
                    "version": version,
                    "url": download_url
                })

        if not stable_releases:
            return []

        # Сортуємо знайдені версії (від нових до старих)
        stable_releases.sort(
            key=lambda x: [int(u) for u in x['version'].split('.') if u.isdigit()], 
            reverse=True
        )

        # Беремо лише одну останню версію
        latest = stable_releases[0]
        return [f"{latest['version']} {latest['url']}"]

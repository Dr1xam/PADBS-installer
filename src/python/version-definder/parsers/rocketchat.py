from core.snap_base import SnapBaseParser

class RocketChatParser(SnapBaseParser):
    def __init__(self):
        super().__init__(package_name="rocketchat-server")

    def get_versions(self) -> list:
        data = self._fetch_snap_info()
        results = []
        seen = set()

        channels = data.get("channel-map", [])

        for item in channels:
            channel_info = item.get("channel", {})
            track = channel_info.get("track")  # напр. "6.x"
            risk = channel_info.get("risk")    # напр. "stable"

            if risk == "stable":
                #  f"{track} /{risk}" -> "6.x /stable" (два слова через пробіл)
                
                ver_string = f"{track} {track}/{risk}"

                if ver_string not in seen:
                    results.append(ver_string)
                    seen.add(ver_string)

        return sorted(results, reverse=True)

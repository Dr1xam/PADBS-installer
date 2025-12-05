import urllib.request
import json
from typing import List  # <--- ДОДАНО ЦЕЙ ІМПОРТ
from .base import BaseParser

class SnapBaseParser(BaseParser):
    """
    Батьківський клас для роботи з Snapcraft API.
    """
    API_URL = "https://api.snapcraft.io/v2/snaps/info/{package}"
    HEADERS = {
        "Snap-Device-Series": "16",
        "User-Agent": "VersionFinder/1.0"
    }

    def __init__(self, package_name: str):
        self.package_name = package_name

    def _fetch_snap_info(self) -> dict:
        """Виконує HTTP-запит до Snapcraft API"""
        url = self.API_URL.format(package=self.package_name)
        req = urllib.request.Request(url, headers=self.HEADERS)
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            # У реальному проекті тут варто додати логування
            print(f"[ERROR] Snap API error for {self.package_name}: {e}")
            return {}

    def get_versions(self) -> List[str]:
        # Цей метод має бути перевизначений у конкретних класах,
        # бо логіка фільтрації версій у кожного різна.
        raise NotImplementedError

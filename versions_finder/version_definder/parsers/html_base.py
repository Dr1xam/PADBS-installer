import urllib.request
from html.parser import HTMLParser
from typing import List, Callable
from .base import BaseParser

class SimpleLinkParser(HTMLParser):
    def __init__(self, filter_func):
        super().__init__()
        self.links = []
        self.filter_func = filter_func

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, val in attrs:
                if name == 'href':
                    clean_val = val.rstrip('/')
                    if self.filter_func(clean_val):
                        self.links.append(clean_val)

class HtmlBaseParser(BaseParser):
    """
    Базовий клас для HTML-парсерів.
    """

    # === ЗМІНА ТУТ: додали аргумент quiet=False ===
    def fetch_and_parse_links(self, url: str, filter_func: Callable[[str], bool], quiet: bool = False) -> List[str]:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as f:
                html = f.read().decode('utf-8')
            
            parser = SimpleLinkParser(filter_func)
            parser.feed(html)
            return parser.links
        except Exception as e:
            # Якщо режим НЕ тихий — друкуємо помилку.
            # Якщо тихий (quiet=True) — просто мовчимо і повертаємо пустий список.
            if not quiet:
                print(f"[ERROR] Failed to parse {url}: {e}")
            return []

    def sort_versions(self, version_list: List[str]) -> List[str]:
        try:
            return sorted(version_list, key=lambda s: [int(u) for u in s.split('.') if u.isdigit()], reverse=True)
        except ValueError:
            return sorted(version_list, reverse=True)

    def get_versions(self) -> List[str]:
        raise NotImplementedError

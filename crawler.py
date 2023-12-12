import requests

from cache import Cache


class Crawler:
    def __init__(self):
        self.cache = Cache()
        self.cache.cache_dir = "cache_html"

    def crawl(self, url):
        content = self.cache.read(url)
        if  content is None:
            # https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0
            # https://www.kleinanzeigen.de/s-preis:20:/seite:2/l%C3%B6tstation/k0
            print("web_read: " + url)
            response = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
            })
            print("web_read: " + str(response.status_code) + " " + url)
            # Sicherstellen, dass die Anfrage erfolgreich war
            return self.cache.write(url, response.text) if response.status_code == 200 else None

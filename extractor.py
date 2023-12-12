from bs4 import BeautifulSoup

from cache import Cache
from crawler import Crawler
from image_handler import ImageHandler


class Extractor:

    def __init__(self):
        self.cache = Cache()
        self.cache.cache_dir = "cache_data"

    def extract(self, url):
        content = self.cache.read(url)
        if  content is None:
            # https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0
            # https://www.kleinanzeigen.de/s-preis:20:/seite:2/l%C3%B6tstation/k0
            html = Crawler.crawl(url)
            print("extract: " + url)
            #
            #    load image
            #    resize Image
            img_url= ""
            finger_print = ImageHandler.image_fingerprint( img_url);
            #    fingerprint Image
            #
            print("extract: " + " --> " + url)
            # Sicherstellen, dass die Anfrage erfolgreich war
            return self.cache.write(url, content)


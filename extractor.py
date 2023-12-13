from bs4 import BeautifulSoup

from cache import Cache
from crawler import Crawler
from image_handler import ImageHandler


class Extractor:

    def __init__(self):
        self.cache = Cache()
        self.cache.cache_dir = "cache_data/"
        self.crawler = Crawler()
        self.img_handler = ImageHandler()

    # get data from source
    # extract atom-data
    # enrich with fingerprints of image
    #   read/cache image
    #   create/cache downsize version
    #   fingerprint downsize version
    def extract(self, url):
        print("extract: try " + url + " ")
        content = self.cache.read(url)
        if content is None:
            # https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0
            # https://www.kleinanzeigen.de/s-preis:20:/seite:2/l%C3%B6tstation/k0
            html = self.crawler.crawl(url)
            print("extract: got " + url)
            #
            #    load image
            #    resize Image
            img_url = "https://img.kleinanzeigen.de/api/v1/prod-ads/images/15/15aca795-1586-4b10-b1a6-5ba4c88d4c13?rule=$_59.JPG"
            finger_print = self.img_handler.finger_print(img_url);
            #    fingerprint Image
            #
            print("extract: --> " + url)
            # Sicherstellen, dass die Anfrage erfolgreich war
            return self.cache.write(url, content)
        return content


import json
import re

from cache import Cache
from extractor import Extractor


class Coordinator:
    def __init__(self):
        print()
        self.cache = Cache()
        self.cache.cache_dir = "cache_query/"
        self.extractor = Extractor()
        # self.web_interface = WebInterface()
        self.result_idx = 0

    # receive query and
    # show result ...
    def query(self, url, filters):
        # app.start()
        self.extractor.reset()
        html = ""

        data = self.cache.read(url + ".query")
        data = None
        if data is None:
            url_page = url
            if 0 == url_page.count(":/seite:"):
                url_page = re.sub(r"(preis:[0-9]*:[0-9]*/)", "\\1seite:1/", url_page)
            i = 1
            data = dict()
            while 1 == i or (html.count(":/seite:" + str(i)) > 0 and len(html) > 1 and i < 10):
                url_page = re.sub(r":/seite:[0-9]+", ":/seite:" + str(i), url_page)
                data_, html = self.extractor.extract(url_page, "refresh" in filters)
                data.update( data_) # merge
                print("coord: " + str(len(data.keys())) + " ("+ str(len(data.keys())) + " rows from " + url_page + ")")
                i = i + 1
            # self.cache.write(url + ".query", repr(data))
            # self.cache.write(url + ".query", data.encode('utf-8'))
            print("coord::query " + url)
            self.cache.write(url + ".json", json.dumps(data))
            self.cache.write(url + ".query", json.dumps(data))
        return data

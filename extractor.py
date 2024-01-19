import ast
import json
import re
from urllib.parse import urljoin

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
        print("xtrct: try " + url + " ")
        content = self.cache.read(url)
        data_str = self.cache.read(url + ".data") # load dictonary
        data_ = ast.literal_eval(data_str) if data_str is not None else None # load dictonary
        if content is None or data_ is None:
            # https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0
            # https://www.kleinanzeigen.de/s-preis:20:/seite:2/l%C3%B6tstation/k0
            content = self.crawler.crawl(url)
            print("xtrct: got " + url)
            #
            word_count_, words_, data_ = self.extract_internal(url, content) # fills data etc ...
            #
            print("xtrct: sav " + url)
            # Sicherstellen, dass die Anfrage erfolgreich war
            self.cache.write(url, content)
            self.cache.write(url + ".data", data_)
            # clone as csv ...
            data_csv = ""
            for key in data_:
                data_csv += str(data[ key ]).lstrip('[').rstrip(']') + "\n" # fake csv from list-to-string
            self.cache.write( url + ".csv", data_csv)
        return data_, content

    def reset(self):
        # allow aggregating across pages ...
        word_count.clear()
        words.clear()
        data.clear()

    def extract_internal(self, url, html):
        soup = BeautifulSoup(html, "html.parser")
        for img in soup.find_all("img"):
            # start from image
            img_src = urljoin(url, img.get("src"))  # Absoluter Pfad zur Bild-URL generieren
            img_txt = img.get("alt")  # Weller EC2002 Temtronic Lötstation Bayern - Langerringen Vorschau
            img_lnk = urljoin(url, img.parent.parent.get("href"))
            img_lnk_elms = (str(img_lnk) + "/////").split("/")
            key = img_lnk_elms[5]
            print("xtrct: " + key + "          " + img_txt)
            # add further
            img_fingerprint = self.img_handler.finger_print(img_src)
            # get item
            item = img.parent.parent.parent.parent
            descr = item.find_all("p", class_="aditem-main--middle--description")
            price = item.find_all("p", class_="aditem-main--middle--price-shipping--price")
            if len(descr) > 0 and len(img_src) > 0 and not img_lnk is None:
                descr_text = re.sub(r"[\s\r\n]+", " ", str(descr[0].text), 0, re.MULTILINE)
                price_text = re.sub(r"[\s\r\n]+", " ", str(price[0].text), 0, re.MULTILINE)
                #
                print("xtrct:    >>key      " + str(key))
                print("xtrct:    >>img      " + str(img_fingerprint))
                print("xtrct:    >>img_src  " + str(img_src))
                print("xtrct:    >>img_lnk  " + str(img_lnk))
                print("xtrct:    >>descr    " + str(descr_text))
                print("xtrct:    >>price    " + str(price_text))
                #
                data[key] = [key, img_src, img_lnk, descr_text, price_text.replace(" €",""), img_fingerprint]
                #
                dupl = []
                for word in (img_txt + " " + descr[0].text).split(" "):
                    word = re.sub(r'[^a-zA-Z0-9]$', '', word)
                    if len(word) > 1 and word not in dupl:
                        if word not in word_count.keys():
                            word_count[word] = 0
                            words[word] = []
                        word_count[word] = word_count[word] + 1
                        words[word].append(key)
                        dupl.append(word)
            else:
                None
                # print ("SKIPP: " + img.text)
        return word_count, words, data


# wordCount [ a-word ]
# words [ <a-word> ] = [ key1, key2 ... ]
# data [ key ] = [ <key>, <val1> , <val2> ,... ]
# dupl - do not add same key multiple times to word


word_count = {}
words = {}
data = {}

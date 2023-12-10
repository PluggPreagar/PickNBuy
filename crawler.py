import hashlib

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def read_web(url, fileName):
        print ("read web")
        # reset ...
        with open(fileName, 'w', encoding='utf8') as file:
            print()
        # https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0
        # https://www.kleinanzeigen.de/s-preis:20:/seite:2/l%C3%B6tstation/k0
        i=1
        response = None
        while 1 == i or ( url.count(":/seite:") > 0 and 200 == response.status_code and i < 1):
            print("read web: " + url)
            url = re.sub(r":/seite:[0-9]+",":/seite:" + str(i), url)
            response = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
            })
            print(response.status_code)
            #
            if response.status_code == 200:
                data = response.text
                with open(fileName, 'a', encoding='utf8') as file:
                    file.write(data)
            i = i +1
        #
        # Sicherstellen, dass die Anfrage erfolgreich war
        if response.status_code == 200:
            return data

        return None

def read(url):
    print("check: " + url)
    url_digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    fileName = 'ebay' + url_digest + '.html'
    try:
        with open( fileName, 'r', encoding='utf8') as file:
            data = file.read().replace('\n', '')
        print ("read file (" + fileName + ")")
        return data
    except FileNotFoundError:
        return read_web( url, fileName)

def web_crawler(url):
    data = read( url)
    soup = BeautifulSoup(data, "html.parser")
    tags = soup.find_all()
    image_tags = soup.find_all("img")
    image_urls = []
    print("---------")
    for img in image_tags:
        src = img.get("src")
        abs_url = urljoin(url, src)  # Absoluter Pfad zur Bild-URL generieren
        image_urls.append(abs_url)
        txt = img.get("alt") #   Weller EC2002 Temtronic Lötstation Bayern - Langerringen Vorschau
        # print( txt )
        lnk = img.parent.parent.get("href")
        #print (lnk)
        linkElems = (str(lnk)+"///").split("/")
        print ( linkElems[3] + "          " + txt )
        item = img.parent.parent.parent.parent
        descr = item.find_all("p", class_="aditem-main--middle--description")
        price = item.find_all("p", class_="aditem-main--middle--price-shipping--price")
        if len(descr) > 0 and len(abs_url) > 0 and not lnk is None :
            # print("   >>img    " + abs_url)
            # print("   >>lnk    " + lnk)
            # print("   >>descr  " + descr[0].text)
            # print("   >>item   " + item.text )
            for word in (txt + " " + descr[0].text).split(" "):
                word = re.sub( r'[^a-zA-Z0-9]$', '', word)
                if len(word)>1:
                    if not word in words.keys() :
                        words[word] = 0
                        items[word] = []
                        # items[word] += 'X'
                    words[ word ] = words[ word ] + 1
                    prices[ linkElems[3] ] = price[0].text.replace(" ", "")
                    links[ linkElems[3] ] = urljoin(url, lnk)
                    images[ linkElems[3] ] = abs_url
                    if  not word + "----" + linkElems[3] in dupl:
                        items[ word ].append( linkElems[3] )   # may append same multiple times
                        dupl[ word + "----" + linkElems[3] ] = 1
        else:
            print ("SKIPP: " + img.text)
    return tags, image_urls


def scanAndSave(url):
    tags, image_tags = web_crawler(url)

    sortedEntries = sorted(words.items(), key=lambda x: str(x[1] + 100000) + " " + x[0])  # sort by count and name
    print("")
    with open('data.csv', 'w', encoding='utf8') as file:
        for entry in sortedEntries:
            # print(entry[0] + "<<")
            if "Vorschau" == entry[0]:
                print("-")
            elif typePattern.match(entry[0].lower()) or entry[1] > 10:
                # print(entry[0] + " " + str(entry[1]) + "x    ")
                file.write(entry[0] + " " + str(entry[1]) + "x    " + "\n")
                sortedItems = sorted(items[entry[0]],
                                     key=lambda x: str(int(prices[x].replace(".","").replace("€","").replace("VB", "")) + 100000) + " " + x[
                                         0])  # sort by price
                for item in sortedItems:
                    # item = sortedItem[0];
                    # print(item + " ", end="")
                    # print("  " + prices[item] ) # + " " + images[item] + " " + links[item] )
                    # print("  " + prices[item] + " " + images[item] ) # + " " + links[item])
                    # print("  " + prices[item] + " " + images[item] + " " + links[item])
                    file.write("  " + prices[item] + " " + images[item] + " " + links[item] + "\n")
                print("")


# Beispielaufruf des Crawlers
#url = "https://example.com"
words = {}
items = {}
prices = {}
images = {}
dupl = {}
links = {}
typePattern = re.compile("[a-z]+(-_)?[0-9]+|[0-9]+(-_)?[a-z]+")

# url = "https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0"
# scanAndSave(url)


#############################################################################

item="""
       <li class="ad-listitem    ">
                    <article class="aditem" data-adid="2623175592" 
                             data-href="/s-anzeige/jbc-hd-2b-loetstation/2623175592-282-4610">
                        <div class="aditem-image">
                            <a href="/s-anzeige/jbc-hd-2b-loetstation/2623175592-282-4610">
                                        <div class="imagebox srpimagebox">
                                            <img
                                                   src="https://img.kleinanzeigen.de/api/v1/prod-ads/images/86/86ab9c01-2647-4cfa-9592-63ff063890ad?rule=$_2.JPG"
                                                srcset="https://img.kleinanzeigen.de/api/v1/prod-ads/images/86/86ab9c01-2647-4cfa-9592-63ff063890ad?rule=$_35.JPG"
                                                alt="JBC HD 2B lötstation Hessen - Hofbieber Vorschau"
                                                fetchpriority="low"
                                                loading="lazy"
                                                
                                            />
                                            <div class="galleryimage--counter">
                                                    4</div>
                                            </div>
                                    </a>
                                </div>
                        <div class="aditem-main">
                            <div class="aditem-main--top">
                                <div class="aditem-main--top--left">
                                    <i class="icon icon-small icon-pin-gray"></i> 36145 Hofbieber</div>
                                <div class="aditem-main--top--right">
                                    <i class="icon icon-small icon-calendar-open"></i>
                                        Heute, 15:19</div>
                            </div>
                            <div class="aditem-main--middle">
                                <h2 class="text-module-begin">
                                    <a class="ellipsis" name="2623175592"
                                       href="/s-anzeige/jbc-hd-2b-loetstation/2623175592-282-4610">JBC HD 2B lötstation</a>
                                </h2>
                                <p class="aditem-main--middle--description">Hallo,
Biete eine funktionale lötstation ohne zubehör. Nur die station keinerlei Kabel oder...</p>
                                <div class="aditem-main--middle--price-shipping">
                                    <p class="aditem-main--middle--price-shipping--price">
                                        200  VB</p>
                                    <p class="aditem-main--middle--price-shipping--shipping">
                                            Versand möglich</p>
                                        </div>
                                    </div>
                            <div class="aditem-main--bottom">
                                <p class="text-module-end">
                                    </p>
                                </div>
                        </div>
                    </article>
                </li>
"""
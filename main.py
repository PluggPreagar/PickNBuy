import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def web_crawler(url):
    # Anfrage an die URL senden
    response = requests.get(url)

    # Sicherstellen, dass die Anfrage erfolgreich war
    if response.status_code == 200:
        # HTML-Inhalt der Webseite abrufen
        html_content = response.text

        # BeautifulSoup-Objekt für das Parsen des HTML erstellen
        soup = BeautifulSoup(html_content, "html.parser")

        # Alle Tags auf der Webseite finden
        tags = soup.find_all()

        # Alle Bilder auf der Webseite finden
        images = soup.find_all("img")

        # Zugriff auf die URLs der Bilder erlangen
        image_urls = []
        for img in images:
            src = img.get("src")
            abs_url = urljoin(url, src)  # Absoluter Pfad zur Bild-URL generieren
            image_urls.append(abs_url)
            print( img.get("alt"))


        return tags, image_urls

    # Rückgabe von None, falls die Anfrage fehlschlägt
    return None

# Beispielaufruf des Crawlers
url = "https://example.com"
tags, images = web_crawler(url)

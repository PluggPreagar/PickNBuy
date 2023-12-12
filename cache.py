import hashlib
import os
import re


# https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0
# https://www.kleinanzeigen.de/s-preis:20:/seite:2/l%C3%B6tstation/k0
class Cache:
    def __init__(self):
        self.cache_dir = "cache/"

    def file_name(self, url):
        if re.match("\\.JPG", url) or self.cache_dir.startswith("cache_img"):
            return self.cache_dir + re.sub(r"[^a-zA-Z.0-9]", "_", re.sub(r".*/", "", url), 100)
        return self.cache_dir + re.sub("[a-zA-Z0-9]", "_", re.sub(r"https*://w*.*?/.*", "", url)) \
            + hashlib.sha256(url.encode("utf-8")).hexdigest() + ".html"

    def get(self, url):
        return self.read(url) if self.exists(url) else None

    def exists(self, url):
        # Check if cache file exists for the given URL
        return os.path.exists(self.file_name(url))

    def read(self, url):
        # Read and return the content from cache file
        with open(self.file_name(url), 'r') as file:
            return file.read()

    def write(self, url, content):
        # Write the content to cache file
        with open(self.file_name(url), 'w') as file:
            file.write(content)
        return content

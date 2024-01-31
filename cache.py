import hashlib
import os
import re


# https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0
# https://www.kleinanzeigen.de/s-preis:20:/seite:2/l%C3%B6tstation/k0
class Cache:
    def __init__(self):
        self.cache_dir = "cache/"
        self.force = 0

    def file_name(self, url):
        if re.match("\\.JPG", url) or self.cache_dir.startswith("cache_img"):
            return self.cache_dir + re.sub(r"[^a-zA-Z.0-9]", "_", re.sub(r".*/", "", url), 100)
        return self.cache_dir + re.sub("[^a-zA-Z0-9]+", "_", re.sub(r"https*://w*(.*?)/.*", "\\1", url)) \
            + hashlib.sha256(url.encode("utf-8")).hexdigest() + re.sub(r".*(\.[^.]{1,6})$|.*", "\\1", url)

    def get(self, url, mode=''):
        return self.read(url, mode) if self.exists(url) else None

    def exists(self, url):
        # Check if cache file exists for the given URL
        return os.path.exists(self.file_name(url))

    def read(self, url, mode=''):
        # Read and return the content from cache file
        if self.force:
            print("cache: skipp " + self.file_name(url))
            return None
        try:
            with open(self.file_name(url), 'r' + mode, encoding='utf8' if '' == mode else None) as file:
                print("cache: read " + self.file_name(url))
                return file.read()
        except FileNotFoundError:
            print("cache: miss " + self.file_name(url))
            return None

    def write(self, url, content, mode=''):
        if 2 == self.force:
            print("cache: SKIPP " + self.file_name(url))
            return content
        if content is None:
            print("cache: NONE " + self.file_name(url))
            return content
        if 'b' != mode:
            content = str(content)
        # Write the content to cache file
        print("cache: write " + self.file_name(url))
        with open(self.file_name(url), 'w' + mode, encoding='utf8' if '' == mode else None) as file:
            file.write(content)
        return content

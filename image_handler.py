import hashlib

import cv2
import numpy as np
import requests
from PIL import Image, UnidentifiedImageError

from cache import Cache


class ImageHandler():


    def __init__(self):
        self.cache = Cache()
        self.cache.cache_dir = "cache_img/"
        self.cacheResize = Cache()
        self.cacheResize.cache_dir = "cache_img_resize/"

    def finger_print(self, url):
        img_fingerprint = self.cacheResize.get(url + ".hash")
        if img_fingerprint is None:
            img = self.cache.get(url, 'b' )
            if img is None  and not str(url).endswith('svg'):
                self.cache.write( url, requests.get(url, headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
                    }).content, 'b')
            img_resize_name = self.resize_image(self.cache.file_name(url), self.cacheResize.file_name(url))
            img_fingerprint = self.cacheResize.write( url + ".hash", self.image_fingerprint(img_resize_name) if img_resize_name is not None else None )
        print("imgFP: " + str(img_fingerprint) + " for " + str(url))
        return img_fingerprint

    def resize_image(self, filename, fileNameResized):
        try:
            img = Image.open(filename)
            img_resized = img.resize((3, 3))
            img_resized.save(fileNameResized)
            return fileNameResized
        except UnidentifiedImageError:
            return None
        except FileNotFoundError:
            return None

    def image_fingerprint(self, image_path):
        # Load the image using OpenCV
        reduced_image = cv2.imread(image_path)
        # Downscale the image for faster processing (optional)
        # downscale_ratio = 0.5
        # reduced_image = cv2.resize(image, (0, 0), fx=downscale_ratio, fy=downscale_ratio)
        #reduced_image = cv2.resize(image, (4, 4))
        # Convert the image to grayscale
        #gray_image = cv2.cvtColor(reduced_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(reduced_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite( image_path + ".bmp", rgb_image)
        rgb_bytes = bytes(rgb_image.data)
        #
        #
        #
        # Calculate the average pixel value of the grayscale image
        # average_pixel_value = np.mean(rgb_image)
        # Generate hash of the average pixel value using hashlib
        fingerprint = hashlib.md5(rgb_bytes).hexdigest()
        fingerprint = fingerprint[-10:]  # right most chars only
        return fingerprint

    def image_fingerprint2(self, image_path):
        image = Image.open(image_path)
        # Resize the image to 4x4 pixels
        new_image = image.resize((4, 4), resample=Image.NEAREST)
        # Convert the image to bitmap
        bitmap_image = new_image.convert("1")
        # Reduce color space to 256-bit
        color_reduced_image = bitmap_image.convert("P", palette=Image.ADAPTIVE, colors=256)
        img_as_bytes = bytes(list(color_reduced_image.getdata()))
        #
        color_reduced_image.save(image_path+".bmp", format="BMP")
        #
        fingerprint = hashlib.md5(str(color_reduced_image).encode('utf-8')).hexdigest()
        fingerprint = fingerprint[-10:]  # right most chars only
        return fingerprint



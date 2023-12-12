import re

import requests
from PIL import Image
import cv2
import numpy as np
import hashlib
from os.path import exists as file_exists

def img2hash(imgUrl):
    print ("img2hash: " + imgUrl)
    filename = "img\\" + re.sub(r"[^a-zA-Z.0-9]","_", re.sub(r".*/","", imgUrl), 100)
    filename_resized = f"resized_{filename}"
    print ("img2hash: " + imgUrl + " " + filename_resized )
    if (not file_exists(filename_resized)) :
        download_image( imgUrl , filename)
        filename_resized = resize_image( filename, filename_resized)
    fingerprint = image_fingerprint( filename_resized )
    print ("img2hash: " + imgUrl + " " + filename_resized + " " + fingerprint)
    return fingerprint


def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def resize_image(filename, fileNameResized):
    img = Image.open(filename)
    img_resized = img.resize((5, 5))
    img_resized.save(fileNameResized)
    return fileNameResized

def image_fingerprint(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    # Downscale the image for faster processing (optional)
    downscale_ratio = 0.5
    reduced_image = cv2.resize(image, (0, 0), fx=downscale_ratio, fy=downscale_ratio)
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(reduced_image, cv2.COLOR_BGR2GRAY)
    # Calculate the average pixel value of the grayscale image
    average_pixel_value = np.mean(gray_image)
    # Generate hash of the average pixel value using hashlib
    fingerprint = hashlib.md5(str(average_pixel_value).encode('utf-8')).hexdigest()
    return fingerprint


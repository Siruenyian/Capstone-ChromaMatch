from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import numpy as np
import csv
import time
import random
import cv2


def rgb2hsv(r, g, b):
    # Normalize R, G, B values
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    # h, s, v = hue, saturation, value
    max_rgb = max(r, g, b)
    min_rgb = min(r, g, b)
    difference = max_rgb-min_rgb

    # if max_rgb and max_rgb are equal then h = 0
    if max_rgb == min_rgb:
        h = 0

    # if max_rgb==r then h is computed as follows
    elif max_rgb == r:
        h = (60 * ((g - b) / difference) + 360) % 360

    # if max_rgb==g then compute h as follows
    elif max_rgb == g:
        h = (60 * ((b - r) / difference) + 120) % 360

    # if max_rgb=b then compute h
    elif max_rgb == b:
        h = (60 * ((r - g) / difference) + 240) % 360

    # if max_rgb==zero then s=0
    if max_rgb == 0:
        s = 0
    else:
        s = (difference / max_rgb) * 100

    # compute v
    v = max_rgb * 100
    # return rounded values of H, S and V
    return tuple(map(round, (h, s, v)))


def links(url):
    driver = webdriver.Firefox()

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.findAll('section')[1].findChildren(
        "span", recursive=True, style=True)
    colorlist = []
    for tag in links:
        color = tag.get('style').split("#")[1]
        # convert to rgb
        color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        color = rgb2hsv(color[0], color[1], color[2])
        colorlist.append(color)
    driver.close()
    return colorlist


def webscrape(link, csvlink):
    a = links(link)

    # a = np.array(a).reshape(-1, 4)
    # if you want a hex, just split it by 4
    a = np.array(a).reshape(-1, 12)

    # writing the data into the file
    with open(csvlink, 'a+', newline='') as csvfile:
        write = csv.writer(csvfile)
        write.writerows(a)


csvlink = './dataset/sample_hsv.csv'
baselink = 'https://www.canva.com/colors/color-palettes/'

# /page/{n}/ to navigate to next pages
webscrape(baselink, csvlink)
for i in range(1, 2):
    navlink = baselink+'page/'+str(i)
    print(navlink)
    webscrape(navlink, csvlink)
    time.sleep(random.randint(1, 5))
print('done scraping :)')

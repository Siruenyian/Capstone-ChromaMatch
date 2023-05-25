from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import numpy as np
import csv
import time
import random


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


csvlink = './dataset/sample.csv'
baselink = 'https://www.canva.com/colors/color-palettes/'

# /page/{n}/ to navigate to next pages
webscrape(baselink, csvlink)
for i in range(1, 50):
    navlink = baselink+'page/'+str(i)
    print(navlink)
    webscrape(navlink, csvlink)
    time.sleep(random.randint(1, 5))
print('done scraping :)')

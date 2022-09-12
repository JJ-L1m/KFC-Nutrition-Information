import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import html5lib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import sys
import time
import warnings
warnings.filterwarnings('ignore')

# url = "https://kfcsg.cognizantorderserv.com/nutrition-allergen"
kfc_data = pd.DataFrame(columns=["Food", "Energy (kcal)", "Protein (g)", "Total Fat (g)", "Saturated fat (g)", "Carbohydrate (g)", "Sodium (mg)"])

driver = webdriver.Chrome(executable_path=r'C:\Users\music\Downloads\chromedriver_win32\chromedriver.exe')
driver.get('https://kfcsg.cognizantorderserv.com/nutrition-allergen')
html = driver.page_source
soup = BeautifulSoup(html, 'html5lib')
# print(soup.prettify()) to see parsed form

# scrape the nutrition data of food items
tr = soup.find_all('tr')
for row in tr:
    cols = row.find_all('td', attrs={'class': 'align-middle ng-binding'})
    # print(cols) to see
    try:
        food = cols[0].text
        energy = cols[2].text
        protein = cols[3].text
        fat = cols[4].text
        satfat = cols[5].text
        carb = cols[6].text
        sodium = cols[7].text
    except:
        continue
    time.sleep(2)

    # Finally we append the data of each row to the table
    kfc_data = kfc_data.append({"Food": food, "Energy (kcal)": energy, "Protein (g)": protein, "Total Fat (g)": fat, "Saturated fat (g)": satfat, "Carbohydrate (g)": carb, "Sodium (mg)": sodium}, ignore_index=True)

# create a copy to work on
df = kfc_data.copy()

# strip whitespaces after selecting columns that are type:objects
swhite = df.select_dtypes(object).columns
df[swhite] = df[swhite].apply(lambda x: x.str.strip())

# change columns (index 1 onwards) to float and replace any symbols in cells to ''
for col in df.columns[1:]:
    df[col] = df[col].replace(',', '', regex=True).astype(float)

# remove duplicates
df.drop_duplicates(keep='first', inplace=True)

print(df.info())

# export df to csv
df.to_csv(r'C:\Users\music\Desktop\kfcdata.csv', index=False)

# scrape the images of the food items
image_info = []
for image in soup.find_all('img'):
    kfcext = image.get('src').replace('..', '')
    if kfcext.startswith('https'):
        image_info.append(kfcext)
    else:
        kfcurl = 'https://kfcsg.cognizantorderserv.com'
        fullurl = kfcurl + kfcext
        image_info.append(fullurl)
    time.sleep(2)

# print(image_info) to see all the image extensions added to list
# noted duplicates in list; remove duplicates in list while maintaining order in list
# print(image_info_2) to see new list w/o duplicates
image_info_2 = list(dict.fromkeys(image_info))

# saving images into own desktop
image_count = 1
for img in image_info_2:
    with open(r'C:\Users\music\Desktop\kfc_images\image_'+str(image_count)+'.jpg', 'wb') as f:
        res = requests.get(img)
        f.write(res.content)
    image_count = image_count+1






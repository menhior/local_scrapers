from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

name_list = []
address_list = []
description_list = []
phone_list = []
link_list = []

for i in range(1, 12):
    print("Page Number:", str(i))
    url = 'https://oneclick.az/business/clothing-accessories/Jewellery/Yuvelirnie+izdeliya?city=784&page=' + str(i)

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # Load the website
    driver.get(url)
    time.sleep(11)
    # Click any buttons or fill out forms if required
    # In this case, we don't need to perform any actions

    # Get the page source after the page has loaded completely
    html = driver.page_source

    # Close the driver
    driver.quit()

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    #print(soup)
    links = []
    descriptions = []
    divs = soup.find_all('div', class_='wrap')
    for div in divs:
        ul = div.find('ul')
        li = ul.find('li', class_='site')
        if li != None:
            a_to_website = li.find('a')
            href_value = a_to_website['href']
            links.append(href_value)
        else:
            links.append(li)
    for div in divs:
        description = div.find('p', class_='f14')
        if description != None:
            descriptions.append(description.text)
        else:
            descriptions.append(description)

    phones = soup.find_all('li', class_='phone')
    addresses = soup.find_all('p', class_='f16')
    #urls = soup.find_all(attrs={'itemprop': 'url'})
    urls = soup.find_all('h3')
    names = []
    for url in urls:
        name = url.find(attrs={'itemprop': 'name'})
        if name != None:
            names.append(name.text)


    for address in addresses:
        clean_address = address.text.replace("\n", "").replace('                                ', "")
        address_list.append(clean_address)
    for phone in phones:
        phone_list.append(phone.text)
    for link in links:
        link_list.append(link)
    for description in descriptions:
        description_list.append(description)
    for name in names:
        name_list.append(name)

    print(len(link_list))
    print(len(name_list))
    print(len(address_list))
    print(len(phone_list))
    print(len(link_list))

    time.sleep(3)

big_dict = {}
big_dict = {"Names": name_list, "Adresses": address_list, 'Descriptions': description_list, 'Phones':phone_list, "links": link_list}

df = pd.DataFrame(big_dict)
print(df)
print(df.isnull().values.any())
df.to_excel(r'Scraped_2.xlsx', index=False)

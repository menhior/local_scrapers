from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

names_list = []
addresses_list = []
phones_list = []

for i in range(1, 45):
    url = 'https://2gis.az/ru/baku/search/s%C4%B1r%C4%9Falar/page/' + str(i) + '?m=50.329836%2C40.415891%2F10.36'
    print('URL page: \n' + url )

    driver = webdriver.Firefox()

    # Load the website
    driver.get(url)
    time.sleep(2)
    # Click any buttons or fill out forms if required
    # In this case, we don't need to perform any actions

    # Get the page source after the page has loaded completely
    html = driver.page_source

    # Close the driver
    driver.quit()

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', class_='_zjunba')
    links_to_parse = []
    for div in divs:
        a_to_web = div.find('a', class_='_1rehek')
        href_value = a_to_web['href']
        links_to_parse.append(href_value)

    for link_to_parse in links_to_parse:
        url_to_parse = 'https://2gis.az/' + link_to_parse
        print(url_to_parse)
        driver = webdriver.Firefox()

        # Load the website
        driver.get(url_to_parse)
        time.sleep(3)
        # Click any buttons or fill out forms if required
        # In this case, we don't need to perform any actions

        # Get the page source after the page has loaded completely
        html_to_parse = driver.page_source

        # Close the driver
        driver.quit()
        soup_to_scrap = BeautifulSoup(html_to_parse, 'html.parser')

        h1 = soup_to_scrap.find('h1', class_='_tvxwjf')
        name = h1.find('span').text

        address = soup_to_scrap.find_all('a', class_='_2lcm958')[3].text
        
        div = soup_to_scrap.find('div', class_='_b0ke8')
        if div != None:
            a_data = div.find('a', class_='_2lcm958')
            phone = a_data['href']
        else:
            phone = None

        names_list.append(name)
        addresses_list.append(address)
        phones_list.append(phone)

    print(len(names_list))
    print(len(addresses_list))
    print(len(phones_list))


big_dict = {}
big_dict = {"Names": names_list, "Adresses": addresses_list, 'Phones':phones_list}

df = pd.DataFrame(big_dict)
print(df)
print(df.isnull().values.any())
df.to_excel(r'Scraped.xlsx', index=False)
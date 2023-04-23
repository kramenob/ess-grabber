import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # Для использования клавиш
from selenium.webdriver.common.by import By # Для обращения к объектам страницы
from selenium.webdriver.common.action_chains import ActionChains
import time

######################################################################################################


def get_source_html(url):

    # путь к драйверу взаимодействия с браузером (Google Chrome v.112.0.5615.49 в Моём случае)
    driver = webdriver.Chrome(
        executable_path="./chromedriver/chromedriver.exe" # for notice debug :: https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
    )

    # разворот окна во весь экран
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(1)
        
        # минуем уведомление кук
        accept_button = driver.find_element(By.ID, "es-consent-accept-btn")
        accept_button.send_keys(Keys.RETURN)

        # блок текста
        while True:
            text_block = driver.find_elements(By.CLASS_NAME, "css-im25bh")

            if driver.find_elements(By.CLASS_NAME, "css-1a3u26t"):
                with open("./info.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)
                break
            else:
                actions = ActionChains(driver)
                actions.move_to_element(text_block).perform()
                time.sleep(1)

    # вывод ошибки, в случае неудачи
    except Exception as _ex:
        print(_ex)

    # в завершение функции - закрывается окно, завершается скрипт
    finally:
        time.sleep(1) # просто смотрим :: для теста
        driver.close()
        driver.quit()

#######################################################################################################

def get_items_urls(file_path):
    with open(file_path, encoding="utf_8_sig") as file:
        src = file.read()
        
    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("a", class_="css-1eulu15")
    
    urls = []
    for item in items_divs:
        item_url = item.find("span", class_="css-1a3u26t").text
        urls.append(item_url)
        
    with open("./hashtags.txt", "w", encoding="utf_8_sig") as file:
        for url in urls:
            file.write(f"{url}\n")

#######################################################################################################

def get_title(file_path):
    with open(file_path, encoding="utf_8_sig") as file:
        src = file.read()
        
    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("h1", class_="css-1x68g13")
    
    urls = []
    for item in items_divs:
        item_url = item.text
        urls.append(item_url)
        
    with open("./title.txt", "w", encoding="utf_8_sig") as file:
        for url in urls:
            file.writelines(f"{url}\n")

#######################################################################################################

def get_description(file_path):
    with open(file_path, encoding="utf_8_sig") as file:
        src = file.read()
        
    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("p", class_="css-26f274")
    
    urls = []
    for item in items_divs:
        item_url = item.text
        urls.append(item_url)
        
    with open("./description.txt", "w", encoding="utf_8_sig") as file:
        for url in urls:
            file.writelines(f"{url}\n")

#######################################################################################################

def get_cover(file_path):
    with open(file_path, encoding="utf_8_sig") as file:
        src = file.read()
        
    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("div", class_="css-ovr3rn")
    
    urls = []
    for item in items_divs:
        item_url = item.find("img", class_="css-25xkn8").get("src")
        urls.append(item_url)
        
    with open("./cover.txt", "w", encoding="utf_8_sig") as file:
        for url in urls:
            file.writelines(f"{url}\n")

#######################################################################################################

def main():
    # get_source_html(url="https://www.epidemicsound.com/music/themes/nature/sound-of-the-seas/")
    # get_items_urls(file_path="./info.html")
    # get_title(file_path="./info.html")
    # get_description(file_path="./info.html")
    get_cover(file_path="./info.html")

if __name__ == "__main__":
    main()
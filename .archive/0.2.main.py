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

        # находим блок текста
        while True:
            text_block = driver.find_elements(By.CLASS_NAME, "css-im25bh")

            if driver.find_elements(By.CLASS_NAME, "css-1a3u26t"):
                with open("./bin/source/source_page.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)
                break
            else:
                actions = ActionChains(driver)
                actions.move_to_element(text_block).perform()
                # time.sleep(1)

    # вывод ошибки, в случае неудачи
    except Exception as _ex:
        print(_ex)

    # в завершение функции - закрывается окно, завершается скрипт
    finally:
        # time.sleep(1) # просто смотрим :: для теста
        driver.close()
        driver.quit()

#######################################################################################################

def get_album_info(file_path):
    with open(file_path, encoding="utf_8_sig") as file:
        src = file.read()
        
    soup = BeautifulSoup(src, "lxml")

    element_hashtags = soup.find_all("a", class_="css-1eulu15")
    element_title = soup.find("h1", class_="css-1x68g13").text
    element_description = soup.find("p", class_="css-26f274").text
    element_cover = soup.find("img", class_="css-25xkn8").get("src")
    

    # извлекаем все хэштеги
    hashtags = []
    for item in element_hashtags:
        item_hashtag = item.find("span", class_="css-1a3u26t").text
        hashtags.append(item_hashtag)

    # сохраняем все хэштеги
    with open("./bin/info/hashtags.txt", "w", encoding="utf_8_sig") as file:
        for hashtag in hashtags:
            hashtag = hashtag.replace(" ", "_")
            file.write("#_" + hashtag + " ")

    # сохраняем заголовок
    with open("./bin/info/title.txt", "w", encoding="utf_8_sig") as file:
        file.write(element_title)

    # сохраняем заголовок
    with open("./bin/info/description.txt", "w", encoding="utf_8_sig") as file:
        file.write(element_description)

    # сохраняем заголовок
    with open("./bin/info/cover.txt", "w", encoding="utf_8_sig") as file:
        file.write(element_cover)

#######################################################################################################

def main():
    get_source_html(url="https://www.epidemicsound.com/music/themes/nature/sound-of-the-seas/")
    get_album_info(file_path="./bin/source/source_page.html")

if __name__ == "__main__":
    main()
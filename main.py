
# main.py
# Main Sound Grabber code
# It can download album page and get album info

###########################################################################################################################
                                                                                                                          #
from bs4 import BeautifulSoup                                       # HTML reader                                         #
from selenium import webdriver                                      # Web Browser interaction                             #
from selenium.webdriver.common.keys import Keys                     # Keyboard emulation                                  #
from selenium.webdriver.common.by import By                         # HTML elements request                               #
from selenium.webdriver.common.action_chains import ActionChains    # Move page emulation (mouse scroll)                  #
from PIL import Image                                               # Work with images (for album cover)                  #
import time                                                         # Timer                                               #
import urllib.request                                               # Download files by link (for album cover download)   #
import bot                                                          # Telegram bot code                                   #
                                                                                                                          #
########################################################################################################################### 



def main():
    bot.start()



def get_source_html(url):

    # путь к драйверу взаимодействия с браузером (Google Chrome v.112.0.5615.49 в Моём случае)
    driver = webdriver.Chrome(
        executable_path="./chromedriver/chromedriver.exe" # for notice debug :: https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
    )
 
    # разворот окна во весь экран
    driver.maximize_window()

    try:
        driver.get(url=url)
        # time.sleep(1) # Just wait loading
        
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
                # time.sleep(1) # Just wait loading

    # вывод ошибки, в случае неудачи
    except Exception as _ex:
        print(_ex)

    # в завершение функции - закрывается окно, завершается скрипт
    finally:
        driver.close()
        driver.quit()



def get_album_info(file_path):
    with open(file_path, encoding="utf_8_sig") as file:
        src = file.read()
        
    soup = BeautifulSoup(src, "lxml")

    element_title = soup.find("h1", class_="css-1x68g13").text.replace("’", "'")       # Заголовок
    element_description = soup.find("p", class_="css-26f274").text.replace("’", "'")   # Описание
    element_hashtags = soup.find_all("a", class_="css-1eulu15")      # Хэштеги
    element_cover = soup.find("img", class_="css-25xkn8").get("src") # Обложка
    
    # извлекаем все хэштеги
    hashtags = []
    for item in element_hashtags:
        item_hashtag = item.find("span", class_="css-1a3u26t").text.replace(" ", "_").replace("&", " #").replace(",", " #").replace("_ ", " ")
        if item_hashtag != element_title.replace(" ", "_").replace("&", " #").replace(",", " #").replace("_ ", " "): # убирает дублирующий заголовок хэштег
            hashtags.append("#_" + item_hashtag + " ")
        else:
            continue

    # Обложка альбома
    urllib.request.urlretrieve(element_cover, "./bin/info/cover.png") # загружает
    cover = Image.open('./bin/info/cover.png')                        # открывает
    cover = cover.resize((500, 500))                                  # подгоняет
    cover.save('./bin/info/cover.png')                                # заменяет

    # Информация альбома
    album_info = (
        "<b>" + element_title + "</b>" + "\n\n" +
        "<i>" + element_description + "</i>" + "\n\n" +
        "".join(hashtags)
    )
    with open("./bin/info/info.md", "w", encoding="utf_8_sig") as file:
        file.write(album_info)



if __name__ == "__main__":
    main()



# p.s. Tutorial - https://youtu.be/w7YEorllJZI
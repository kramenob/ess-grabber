


###########################################################################################################################
                                                                                                                          #
from bs4 import BeautifulSoup                                       # HTML reader                                         #
from selenium import webdriver                                      # Web Browser interaction                             #
from selenium.webdriver.common.keys import Keys                     # Keyboard emulation                                  #
from selenium.webdriver.common.by import By                         # HTML elements request                               #
from selenium.webdriver.common.action_chains import ActionChains    # Move page emulation (mouse scroll)                  #
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from PIL import Image                                               # Work with images (for album cover)                  #
import time                                                         # Timer                                               #
import urllib.request                                               # Download files by link (for album cover download)   #
import bot                                                          # Telegram bot code                                   #
import sys
import config
import webbrowser
                                                                                                                          #
###########################################################################################################################

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def vpn(url):

    # driver = webdriver.Chrome(
    #     executable_path="./chromedriver/chromedriver.exe" # for notice debug :: https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
    # )

    chop = webdriver.ChromeOptions()

    chop.add_extension(config.vpn_file)

    driver = webdriver.Chrome(chrome_options=chop)

    try:
        driver.get(url=url)
        driver.refresh()
        time.sleep(1) # Just wait loading

        continue_btn = driver.find_element(By.CLASS_NAME, 'next')
        continue_btn.send_keys(Keys.RETURN)

        continue_btn = driver.find_element(By.CLASS_NAME, 'next')
        continue_btn.send_keys(Keys.RETURN)
        
        time.sleep(5) # Just wait loading
        driver.switch_to.window(driver.window_handles[0])

        action = webdriver.common.action_chains.ActionChains(driver)
        continue_btn = driver.find_element(By.CLASS_NAME, 'button-clicker')
        action.move_to_element_with_offset(continue_btn, 5, 5)
        action.click()
        action.perform()
        time.sleep(5) # Just wait loading
        
        driver.close()
        driver.get('https://soundcloud.com/')
        driver.refresh()
        # driver.switch_to.window(driver.window_handles[1])

    except Exception as _ex:
        print(_ex)

    finally:
        time.sleep(120) # Just wait loading
        driver.close()
        driver.quit()

def soundcloud_link(url):

    driver = webdriver.Chrome(
        executable_path="./chromedriver/chromedriver.exe" # for notice debug :: https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
    )

    try:

        vpn(url=config.vpn)

        driver.get(url=url)
        time.sleep(1) # Just wait loading

        track_link = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/div/div/ul/li/div/div/div/div[2]/div[4]/div[1]/div/div/button[4]')
        track_link.send_keys(Keys.RETURN)

    except Exception as _ex:
        print(_ex)

    finally:
        driver.close()
        driver.quit()

def get_source_html(url):

    # путь к драйверу взаимодействия с браузером (Google Chrome v.112.0.5615.49 в Моём случае)
    driver = webdriver.Chrome(
        executable_path="./chromedriver/chromedriver.exe" # for notice debug :: https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
    )

    # разворот окна во весь экран
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(1) # Just wait loading

        # минуем уведомление кук
        accept_button = driver.find_element(By.ID, "es-consent-accept-btn")
        accept_button.send_keys(Keys.RETURN)

        to_delete_footer = driver.find_element(By.CLASS_NAME, 'src-mainapp-SignedOutNav-___SignedOutNav__container___OU7YK')
        to_delete_info = driver.find_element(By.CLASS_NAME, 'css-im25bh')
        to_delete_cover = driver.find_element(By.CLASS_NAME, 'css-ovr3rn')

        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, to_delete_footer)

        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, to_delete_info)

        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, to_delete_cover)

        n = 1
        
        # Get track block
        track_block = driver.\
            find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/main/div/div[1]/div/div/div/div[3]/div/div/div').\
            get_attribute('innerHTML')
        
        soup = BeautifulSoup (
            track_block,
            'html.parser'
            )
        
        track_rows = soup.\
            find_all (
                "div",
                {"class": "css-1w66edn"}
                )

        track_rows_count = len ( track_rows )

        # Found N tracks
        print (
            "\n    Found " + \
            str(track_rows_count) + \
            " tracks"
            )

        # Stop number
        track_rows_count = track_rows_count + 1
        
        # Листать пока style не поимеет padding-bottom: 0px; ()
        while True:

            if n == track_rows_count:

                print("\n    That's all")

                break

            else:
                track_name =   driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[1]/main/div/div[1]/div/div/div/div[3]/div/div/div/div[{n}]/div/div/div[1]/div[1]/div/span/span[1]/a').text
                track_author = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[1]/main/div/div[1]/div/div/div/div[3]/div/div/div/div[{n}]/div/div/div[1]/div[2]/div/div/span/span[1]/span/a[1]').text
                track_long = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[1]/main/div/div[1]/div/div/div/div[3]/div/div/div/div[{n}]/div/div/div[4]/div[1]/span').text
                # Write if there is no
                track_bpm = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[1]/main/div/div[1]/div/div/div/div[3]/div/div/div/div[{n}]/div/div/div[4]/div[2]').text
                track_genres = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[1]/main/div/div[1]/div/div/div/div[3]/div/div/div/div[{n}]/div/div/div[5]/div[1]').text
                track_moods = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[1]/main/div/div[1]/div/div/div/div[3]/div/div/div/div[{n}]/div/div/div[5]/div[2]').text

                # print('\n    ID: ' + str(n))

                # print( 
                #     '\n' + track_author + " - " + track_name +
                #     '\n' + "Genres: " + "#_" + track_genres.replace(" ", "_").replace("&", " #").replace(",", " #").replace("_ ", " ") +
                #     '\n' + "Moods: " + "#_" + track_moods.replace(" ", "_").replace("&", " #").replace(",", " #").replace("_ ", " ") +
                #     '\n' + "#_Duration_" + track_long.replace(":", "m") +"s" +
                #     ' ' + "#_BPM_" + track_bpm.replace(" BPM", "")
                # )

                track_link = "https://soundcloud.com/search?q=" + (track_author + track_name).replace(" ", "%20").replace("'", "%27")
                
                print(
                    '\n' + str(n) + ". " + track_link +
                    '\n' + "Genres: " + "#_" + track_genres.replace(" ", "_").replace("&", " #").replace(",", " #").replace("_ ", " ") +
                    '\n' + "Moods: " + "#_" + track_moods.replace(" ", "_").replace("&", " #").replace(",", " #").replace("_ ", " ") +
                    '\n' + "#_Duration_" + track_long.replace(":", "m") +"s" +
                    ' ' + "#_BPM_" + track_bpm.replace(" BPM", "")
                )

                # Need VPN connection
                # get_source_html(url=track_link)
                # print(
                #     '\n' + 
                #     str(n) + ". "
                #     "SoundCloud link: " + 
                #     pyperclip.paste()
                # )

            n = n + 1

    # вывод ошибки, в случае неудачи
    except Exception as _ex:
        print(_ex)

    finally:
        driver.close()
        driver.quit()

get_source_html(url="https://www.epidemicsound.com/music/themes/ads-promos-trailers/feelgood-trailers/")

# vpn(url=config.vpn)
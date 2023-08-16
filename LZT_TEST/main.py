import time

import selenium.webdriver.chrome.options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from user_input import User_Input  # Функция ввода данных


class YouTubeBot:
    def __init__(self, driver_path="chromedriver.exe"):
        self.driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(driver_path),
            options=selenium.webdriver.chrome.options.Options().add_argument(
                '--ignore-certificate-errors-spki-list'
                )
            )  # Запускаем браузер
        self.wait = WebDriverWait(self.driver, 30)

    def Page_has_loaded(self):  # Проверка загрузки страницы
        while True:
            page_state = self.driver.execute_script('return document.readyState;')  # Получаем состояние страницы
            if page_state == 'complete':
                break
            time.sleep(0.5)  # Спим 0.5 секунд между проверками состояния

    def Open_Youtube(self):
        self.driver.get("https://www.youtube.com")  # Открываем страницу ютуба перед загрузкой куки
        self.Page_has_loaded()  # Ждем пока страница загрузится

    def Load_Cookies(self, cookies_file):  # Загружаем куки

        cookies = []  # Пустой список куков
        with open(cookies_file, "r") as file:  # Открываем файл с куками
            for line in file:
                parts = line.strip().split("\t")  # Разделяем строку на части по табуляции
                if len(parts) == 7:
                    cookie = {
                        "name": parts[5],
                        "value": parts[6],
                        "domain": parts[0],
                        "path": parts[2],
                        "expires": int(parts[4]),
                        "httpOnly": False if parts[1] == "FALSE" else True,  # Проверка на httpOnly
                        "secure": False if parts[3] == "FALSE" else True  # Проверка на secure
                    }
                    cookies.append(cookie)  # Добавляем кук в список

        # Добавление куков в браузер
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def Search_And_Watch_Video(self, search_query, video_index):
        self.driver.refresh()  # Перезагружаем страницу после загрузки куков
        self.Page_has_loaded()  # Ждем пока страница загрузится

        search_box = self.driver.find_element('css selector', '#search-input > input')  # Находим строку поиска
        search_box.click()  # Кликаем по строке поиска
        search_box.send_keys(search_query)  # Вводим запрос
        search_box.send_keys(Keys.RETURN)  # Нажимаем Enter
        self.Page_has_loaded()  # Ждем пока страница загрузится

        video_xpath = '//*[@id="contents"]/ytd-video-renderer[6]'  # Xpath видео
        video = self.wait.until(EC.element_to_be_clickable((By.XPATH, video_xpath)))  # Ждем пока видео загрузится
        video.click()  # Кликаем по видео

        like_xpath = r'//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button'  # Xpath лайка
        self.wait.until(EC.element_to_be_clickable((By.XPATH, like_xpath)))  # Ждем пока кнопка лайка загрузится
        self.driver.find_element('xpath', like_xpath).click()  # Кликаем по лайку

        sub_xpath = r'//*[@id="subscribe-button-shape"]/button'  # Xpath подписки
        self.wait.until(EC.element_to_be_clickable((By.XPATH, sub_xpath)))  # Ждем пока кнопка подписки загрузится
        self.driver.find_element('xpath', sub_xpath).click()  # Кликаем по подписке

        time.sleep(60)

    def Close(self):
        self.driver.quit()  # Закрываем браузер


if __name__ == "__main__":
    search_query, video_index, cookee_path = User_Input()  # Получаем данные от пользователя
    bot = YouTubeBot()  # Создаем объект класса YouTubeBot
    bot.Open_Youtube()  # Открываем ютуб
    bot.Load_Cookies(cookee_path)  # Загружаем куки
    bot.Search_And_Watch_Video(search_query, video_index)  # Ищем видео и открываем его
    bot.Close()  # Закрываем браузер

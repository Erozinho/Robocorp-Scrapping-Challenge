from setup import payload
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tasklib import (check_date,
                     check_dollar,
                     count_phrase,
                     write_xls_data,
                     save_img)
from time import sleep
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class Challenge:
    def __init__(self):
        # use this librarie to instance the webdrvier
        # browsers (Chrome, Chromium, Brave, Edge, FireFox and Opera)
        service = ChromeService(ChromeDriverManager().install())
        """Option i normally use"""
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-in-process-stack-traces")
        options.add_argument("--disable-logging")
        options.add_argument('--no-sandbox')
        # options.add_argument("--headless=new")
        options.add_argument("--incognito")
        options.add_argument("--silent")
        options.add_argument("start-maximized")
        options.add_argument('--log-level=3')
        options.add_argument("disable-dev-shm-usage")
        options.add_argument("disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(20)

    def close_browser(self) -> None:
        self.driver.quit()

    def open_target(self, url: str) -> None:
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 45, poll_frequency=0.2)

    def search_word(self, word: str) -> None:
        try:
            sh = '//button[@data-element="search-button"]'
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, sh))).click()

            s_bar = '//input[@data-element="search-form-input"]'
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, s_bar))).send_keys(word+Keys.RETURN)

        except ValueError as e:
            raise f'Error on search: {e}'

    def select_topic(self, topic: str) -> None:
        if len(topic) == 0:
            return 'No topic for been selected!'
        for value in topic:
            try:
                select = f'//span[contains(text(), "{value}")]'
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, select))).click()
                sleep(2.75)

            except ValueError:
                print("Topic not found/Wrongly digited")

    def set_newest(self) -> None:
        try:
            element = self.wait.until(
                EC.presence_of_element_located((
                    By.CLASS_NAME, 'select-input')))

            element = Select(element)
            element.select_by_visible_text('Newest')
            sleep(3.5)

        except ValueError as e:
            raise f'Error on set to newest: {e}'

    def get_news(self, phrase) -> None:
        data = []
        page = '//ul[@class="search-results-module-results-menu"]/li'
        content = self.driver.find_elements(By.XPATH, f'{page}')
        for value in content:
            img_file = value.find_element(By.TAG_NAME, 'img')
            txt = value.text.split('\n')
            title = txt[1]
            desc = txt[2]
            date = check_date(txt[3])
            img = save_img(img_file.get_attribute('src'))
            phrase_c = count_phrase(phrase, title) + count_phrase(phrase, desc)
            dol_bol = check_dollar(title) or check_dollar(desc)
            result = [title,
                      date,
                      desc,
                      img,
                      phrase_c,
                      dol_bol]
            data.append(result)
        write_xls_data(data)

    def main(self) -> None:
        try:
            # run everything
            url = payload['url']
            phrase = payload['phrase']
            topic = payload['topic']
            self.open_target(url)
            self.search_word(phrase)
            self.select_topic(topic)
            self.set_newest()
            self.get_news(phrase)

        finally:
            self.close_browser()


if __name__ == "__main__":
    scrap = Challenge()
    scrap.main()

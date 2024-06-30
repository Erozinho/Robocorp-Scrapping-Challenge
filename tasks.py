import json
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
from time import sleep
from tasklib import check_date, check_dollar, count_phrase, save_img


class Challenge:
    def __init__(self):
        self.browser = Selenium()
        self.files = Files()
        self.http = HTTP()
        self.payload = self.load_payload()

    def load_payload(self):
        with open('resources/payload.json', 'r') as f:
            return json.load(f)

    def close_browser(self) -> None:
        self.browser.close_all_browsers()

    def open_target(self, url: str) -> None:
        self.browser.open_available_browser(url)

    def search_word(self, word: str) -> None:
        try:
            search_btn = '//button[@data-element="search-button"]'
            self.browser.wait_until_element_is_visible(search_btn, timeout=45)
            self.browser.click_element(search_btn)

            search_bar = '//input[@data-element="search-form-input"]'
            self.browser.wait_until_element_is_visible(search_bar)
            self.browser.input_text(search_bar, word)
            self.browser.press_keys(search_bar, 'ENTER')

        except ValueError as e:
            raise Exception(f'Error on search: {e}')

    def select_topic(self, topic: list) -> None:
        if not topic:
            return 'No topic for selection!'
        for value in topic:
            try:
                select = f'//span[contains(text(), "{value}")]'
                self.browser.wait_until_element_is_visible(select)
                self.browser.click_element(select)
                sleep(2.75)
            except ValueError:
                print("Topic not found/Wrongly digited")

    def set_newest(self) -> None:
        try:
            element = '//select[@class="select-input"]'
            self.browser.wait_until_element_is_visible(element)
            self.browser.select_from_list_by_label(element, 'Newest')
            sleep(3.5)

        except ValueError as e:
            raise Exception(f'Error on set to newest: {e}')

    def get_news(self, phrase) -> None:
        data = []
        page = '//ul[@class="search-results-module-results-menu"]/li'
        content = self.browser.find_elements(page)
        for value in content:
            img_element = self.browser.find_element(value, 'tag:img')
            txt = value.text.split('\n')
            title = txt[1]
            desc = txt[2]
            date = check_date(txt[3])
            img = save_img(img_element.get_attribute('src'))
            phrase_c = count_phrase(phrase, title) + count_phrase(phrase, desc)
            dollar_bool = check_dollar(title) or check_dollar(desc)
            result = [title, date, desc, img, phrase_c, dollar_bool]
            data.append(result)
        self.write_xls_data(data)

    def write_xls_data(self, data: list) -> None:
        self.files.create_workbook('output/News_data.xlsx')
        for line in data:
            self.files.append_worksheet(line, "Sheet1")
        self.files.save_workbook()

    def main(self) -> None:
        try:
            # Run everything
            url = self.payload['url']
            phrase = self.payload['phrase']
            topic = self.payload['topic']
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

from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems
from robocorp.tasks import task
from dotenv import load_dotenv
from setup import payload

load_dotenv()

class Challenge:
    def __init__(self):
        self.browser = Selenium()
        # self.browser.set_browser_implicit_wait(15)

    def close_browser(self) -> None:
        self.browser.close_browser()

    def open_target(self, url: str) -> None:
        self.browser.open_available_browser(url)
        self.browser.maximize_browser_window()

    def main(self) -> None:
        try:
            # run everything
            inv = WorkItems()
            inv.get_input_work_item()
            url = inv.get_work_item_variable['url']
            self.open_target(url=url)

        finally:
            # close webpage on the end of execution
            pass


if __name__ == "__main__":
    @task
    scrap = Challenge()
    scrap.main()

from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems
from setup import payload


class Challenge:
    def __init__(self):
        self.browser = Selenium()
        self.browser.set_browser_implicit_wait(15)

    def close_browser(self) -> None:
        self.browser.close_browser()

    def main(self) -> None:
        # run everything
        inv = WorkItems()
        inv.get_input_work_item()


if __name__ == "__main__":
    scrap = Challenge()
    scrap.main()

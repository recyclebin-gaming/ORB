from os import listdir
from difflib import get_close_matches
from os.path import exists
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from ror2_wiki_scrapper.constants import ITEM_NAMES, ITEM_LINKS
from ror2_wiki_scrapper.utils import close_tabs


class WebDriver:
    # FIXME functions possibly fucking dies if timed out handle them somehow
    def __init__(self, url: str = None):
        self.driver = webdriver.Firefox()
        self.addons = listdir("addons")
        self.url = url

        for addon in self.addons:
            self.driver.install_addon(f"addons/{addon}")
        self.driver.implicitly_wait(5)
        for handle in self.driver.window_handles[1:]:
            self.driver.switch_to.window(handle)
            self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        if url:
            self.driver.get(url)

    @close_tabs
    def fetch_item(self, item_name: str):
        """saves an image of the item's infobox to pics folder"""
        request = get_close_matches(item_name, ITEM_NAMES)[0]
        index = ITEM_NAMES.index(request)
        self.driver.get(ITEM_LINKS[index])
        WebDriverWait(self.driver, 120).until(ec.visibility_of_element_located((By.XPATH, "//td[1]/img[1]")))
        element = self.driver.find_element(By.CLASS_NAME, "infoboxtable")
        element.screenshot(f"pics/{request}.png")

    @close_tabs
    def regenerate_db(self):
        """checks the pics folder for every item in the game if anything is missing fetches them again"""
        with self.driver as table_fetcher:
            for i in ITEM_NAMES:
                index = ITEM_NAMES.index(i)
                url = ITEM_LINKS[index]
                if not exists(f"ror2_wiki_scrapper/pics/{i}.png"):
                    table_fetcher.get(url)
                    table_fetcher.implicitly_wait(5)
                    WebDriverWait(table_fetcher, 120).until(
                        ec.visibility_of_element_located((By.XPATH, "//td[1]/img[1]")))
                    element = table_fetcher.find_element(By.CLASS_NAME, "infoboxtable")
                    element.screenshot(f"ror2_wiki_scrapper/pics/{i}.png")

from difflib import get_close_matches
from os.path import exists
from re import sub
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from ror2_wiki_scrapper.constants import ITEM_NAMES, ITEM_LINKS


def poll_webdriver(url=None):
    driver = webdriver.Firefox()
    driver.install_addon("addons/adblockultimate@adblockultimate.net.xpi")
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    if url:
        driver.get(url)
    return driver


def fetch_item(item_name, item_fetcher):
    request = get_close_matches(item_name, ITEM_NAMES)[0]
    index = ITEM_NAMES.index(request)
    item_fetcher.switch_to.window(item_fetcher.window_handles[0])
    item_fetcher.get(ITEM_LINKS[index])
    sleep(3)
    WebDriverWait(item_fetcher, 120).until(ec.visibility_of_element_located((By.XPATH, "//td[1]/img[1]")))
    element = item_fetcher.find_element(By.CLASS_NAME, "infoboxtable")
    element.screenshot(f"pics/{request}.png")
    return


def regenerate_db(full):
    with webdriver.Firefox() as table_fetcher:
        for i in ITEM_NAMES:
            index = ITEM_NAMES.index(i)
            url = ITEM_LINKS[index]
            if not exists(f"ror2_wiki_scrapper/pics/{i}.png") and full:
                table_fetcher.get(url)
                table_fetcher.implicitly_wait(5)
                WebDriverWait(table_fetcher, 120).until(ec.visibility_of_element_located((By.XPATH, "//td[1]/img[1]")))
                element = table_fetcher.find_element(By.CLASS_NAME, "infoboxtable")
                element.screenshot(f"ror2_wiki_scrapper/pics/{i}.png")


def process_input(command):
    processed_message = sub(r'/getitem', '', command)
    return processed_message

from selenium import webdriver
from selenium.webdriver.common.by import By

item_fetcher = webdriver.Firefox()
item_fetcher.get("file:///H:/help/Soldier's%20Syringe%20-%20Risk%20of%20Rain%202%20Wiki.htm")
element = item_fetcher.find_element(By.CLASS_NAME, "infoboxtable")
element.screenshot('E://visual studio code,python projects//ror2_wiki_scrapper//pics//Soldier.png')




link_fetcher = webdriver.Firefox()
link_fetcher.get("file:///H:/help/Items%20-%20Risk%20of%20Rain%202%20Wiki.htm")

item_links = []
item_names = []
element = link_fetcher.find_elements(By.XPATH, "//tbody/tr/td/span/a")
for i in element:
    item_links.append(i.get_property("href"))
    item_names.append(i.get_property("title"))

index = item_names.index('Tougher Times')
print(item_links[index])

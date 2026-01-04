from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("detach", True)  # Chrome stays open after quit

driver = webdriver.Chrome(options=options)
driver.get("https://gbf.wiki/api.php?action=cargoquery&tables=characters&fields=id,name,jpname,release_date,obtain_text,base_evo,max_evo,rarity,element,type,race,weapon&format=json&order_by=id%20DESC&limit=500&offset=0")

input("Press Enter when finished debugging…")  # keeps script alive
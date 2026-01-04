import json
import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

__Session = requests.Session()

def requestsGet(url, params = {}):
  # Getting 403 with default user agent as of 2024-03-15
  headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0"
  }
  request = requests.Request(method='GET', url = url, params = params, headers = headers)
  r = request.prepare()
  print("Requests: " + r.url)

  s = __Session.send(request=r)
  if s.status_code != 200:
    print('Got status code', s.status_code, 'for', r.url)
  
  return s

def _getDriver():
  # Use undetected_chromedriver to bypass Cloudflare
  options = uc.ChromeOptions()
  options.add_argument("--window-size=1920,1080")
  options.add_argument("--start-maximized")
  
  driver = uc.Chrome(options=options, version_main=None)
  return driver

__Driver = _getDriver()

# Warm up the driver by making the ACTUAL first query that will be used (category query with limit 500)
print("Making initial category query to establish Cloudflare session...")
print("This is the same query type that parse.py will use, to trigger any Cloudflare checks now.")
__Driver.get("https://gbf.wiki/api.php?action=query&prop=info&generator=categorymembers&gcmtitle=Category:characters&format=json&gcmlimit=500&gcmcontinue=")
print("Waiting for user confirmation that Cloudflare challenge is passed and JSON is visible...")
input("Press Enter once the page has loaded and you can see the JSON data (not a Cloudflare challenge page)...")
print("Session established. Continuing with data download...")

def seleniumGet(url, params = {}):
  global __Driver
  
  full_url = url + '?'
  for key in params:
    full_url += str(key) + '=' + str(params[key]) + '&'

  # Reconnect if driver is dead
  try:
    __Driver.current_url  # Test if driver is still alive
  except:
    print("[RECONNECT] Browser connection lost, reconnecting...")
    __Driver = _getDriver()
  
  __Driver.get(full_url)
  
  # Wait a bit for the page to load and render JSON
  time.sleep(1)
  
  # Try to find and extract the pre element (contains JSON)
  try:
    element = WebDriverWait(__Driver, 10).until(
      EC.presence_of_element_located((By.TAG_NAME, "pre"))
    )
    json_text = element.text
    return json.loads(json_text)
  except Exception as e:
    # If pre element not found, try to get body text directly
    try:
      body_text = __Driver.find_element(By.TAG_NAME, "body").text
      if body_text:
        return json.loads(body_text)
    except:
      pass
    
    print(f"[ERROR] Failed to extract JSON from {full_url}")
    print(f"[ERROR] Page title: {__Driver.title}")
    print(f"[ERROR] URL: {__Driver.current_url}")
    raise Exception(f"Could not extract JSON from response")

# https://gbf.wiki/api.php?action=query&prop=imageinfo&iiprop=url&format=json&titles=File:
def getImageURL(image) -> str:
  time.sleep(.1) # Don't hammer the server - ORIGINAL SPEED
  request = seleniumGet(
    url = 'https://gbf.wiki/api.php',
    params = {
      'action': 'query',
      'prop': 'imageinfo',
      'iiprop': 'url',
      'format': 'json',
      'titles': 'File:' + image
    })
  request_json = request['query']['pages']
  try:
    return next(iter(request_json.values()))['imageinfo'][0]['url']
  except:
    print(request_json)
    raise

import time
import requests

__Session = requests.Session()

def sessionGet(url, params = {}):
  # Getting 403 with default user agent as of 2024-03-15
  headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0"
  }
  request = requests.Request(method='GET', url = url, params = params, headers = headers)
  r = request.prepare()
  print("Query: " + r.url)

  s = __Session.send(request=r)
  if s.status_code != 200:
    print('Got status code', s.status_code, 'for', r.url)
  
  return s

# https://gbf.wiki/api.php?action=query&prop=imageinfo&iiprop=url&format=json&titles=File:
def getImageURL(image) -> str:
  time.sleep(.1) # Don't hammer the server
  request = sessionGet(
    url = 'https://gbf.wiki/api.php',
    params = {
      'action': 'query',
      'prop': 'imageinfo',
      'iiprop': 'url',
      'format': 'json',
      'titles': 'File:' + image
    })
  request_json = request.json()['query']['pages']
  try:
    return next(iter(request_json.values()))['imageinfo'][0]['url']
  except:
    print(request_json)
    raise

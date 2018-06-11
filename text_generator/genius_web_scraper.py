# Credit to some dude online
# https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/

import requests
from bs4 import BeautifulSoup

base_url = "http://api.genius.com"
headers = {'Authorization': 'Mxd-p03AZq5SymCqOlL1l2V6kTYRqjlGttH6YibByR14hI-6cPpJ5vQp7gdqa8t2'}

song_title = "Lake Song"
artist_name = "The Decemberists"

def lyrics_from_song_api_path(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]
  #gotta go regular html scraping... come on Genius
  page_url = "http://genius.com" + path
  page = requests.get(page_url)
  html = BeautifulSoup(page.text, "html.parser")
  #remove script tags that they put in the middle of the lyrics
  [h.extract() for h in html('script')]
  #at least Genius is nice and has a tag called 'lyrics'!
  lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
  return lyrics

if __name__ == "__main__":
  search_url = base_url + "/search"
  data = {'q': song_title}
  response = requests.get(search_url, data=data, headers=headers)
  json = response.json()
  song_info = None
  print(json)
  for hit in json["response"]["hits"]:
    if hit["result"]["primary_artist"]["name"] == artist_name:
      song_info = hit
      break
  if song_info:
    song_api_path = song_info["result"]["api_path"]
    print lyrics_from_song_api_path(song_api_path)
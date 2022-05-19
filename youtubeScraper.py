from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import requests
import json

output = {}
query = 'ukraine'

##### API Key
YOUR_API_KEY = ''

def main():
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  driver.get(f"https://www.youtube.com/results?search_query={query}")

  content = driver.page_source.encode('utf-8').strip()
  soup = BeautifulSoup(content, 'html.parser')
  titles = soup.find_all('a', id='video-title')

  for i in range(0, 10):
    videoURL = 'https://www.youtube.com' + titles[i]['href']
    href = titles[i]['href'] 
    video_id = href.split("=", 1)[1] # get video id
    print(video_id)
    print(videoURL)
    output[videoURL] = [] # assign key with empty list to output
    getComments(videoURL, video_id)

# Utilise the Youtube data API
def getComments(url, video_id):
  endpoint = f'https://www.googleapis.com/youtube/v3/commentThreads?key={YOUR_API_KEY}&textFormat=plainText&part=snippet&videoId={video_id}&maxResults=3'

  response = requests.get(endpoint)
  data = response.json()

  comments = []

  if 'error' not in data:
    items = data['items']
    for item in items:
      comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
      comments.append(comment)

  output[url] = comments
  
main()
# getComments('https://www.youtube.com/watch?v=umNjlp2LObM&t=1149s&ab_channel=NikoOmilana', 'umNjlp2LObM')

with open('output.json', 'w') as f:
  json.dump(output, f)

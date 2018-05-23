from bs4 import BeautifulSoup
import requests
import random

url = "http://www.airlinequality.com/airline-reviews/air-india/page/2/"

agent = "Mozilla/5.0 (Windows NT 6.2) Firefox/40.1"

headers = {'user-agent': agent}
r = requests.get(url, headers=headers)

data = r.content
print(data)
exit()
soup = BeautifulSoup(data)
for div in soup.findAll("div", { "class" : "text_content" }):
	print(str(div))
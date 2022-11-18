import requests
from bs4 import BeautifulSoup

'''
Web-scrapping from Wikipedia.
Bids from 2008 to 2022yy
'''

url2008 = "https://en.wikipedia.org/wiki/List_of_2008_Indian_Premier_League_auctions_and_personnel_signings"
url09_22 = "https://en.wikipedia.org/wiki/List_of_2009_Indian_Premier_League_personnel_changes"
page2008 = requests.get(url2008)
soup = BeautifulSoup(page2008.content, 'html.parser')

# for i in range(9, 23):
#     page = requests.get(
#         f"https://en.wikipedia.org/wiki/List_of_20{i:02d}_Indian_Premier_League_personnel_changes")
#     print(page.status_code)

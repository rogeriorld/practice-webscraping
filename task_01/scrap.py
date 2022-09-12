from urllib import request as req, error
from bs4 import BeautifulSoup
from time import sleep
import csv

# Source: https://www.scrapethissite.com/pages/frames/
# Challenge #1: Get all info from each iframe (turtle) and store and a csv file

def request(page='pages/frames/'):
    domain = 'https://www.scrapethissite.com/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    request = req.Request(domain+page, headers=header)
    try:
        result = req.urlopen(request).read()
        return result
    except error:
        print('Error')
        print(error)
    return None

def getTheTurtles():
    page = 'pages/frames/'
    turtlesList = []

    soup = BeautifulSoup(request(page), 'html.parser')
    # get the iframe source 
    iframe_source = soup.find('iframe').get('src')

    # access the html content from iframe
    soup = BeautifulSoup(request(iframe_source), 'html.parser')
    # get the link to access the info from each turtle
    # two seconds each request
    turtles = soup(attrs={'class': 'turtle-family-card'})
    for turtle in turtles:
        link = turtle.findChildren('a')
        # create the request from each link
        
        soup = BeautifulSoup(request(link[0].get('href')), 'html.parser')
        # get the name and description
        name = soup.find('h3').text
        desc = soup.find('p', class_='lead').text
        turtlesList.append({'name': name, 'description': desc})
        sleep(1)
    return turtlesList

def export_csv(turtles):
    with open('./output.csv', 'w', encoding="utf-8", newline='') as f:
        wr = csv.writer(f, delimiter=';')
        wr.writerow(("Name", "Description"))
        for turtle in turtles:
            wr.writerow((turtle['name'], turtle['description'].strip()))

export_csv(getTheTurtles())
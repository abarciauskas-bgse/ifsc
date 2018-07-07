from bs4 import BeautifulSoup
from selenium import webdriver
import psycopg2
from psycopg2.extensions import AsIs
import json
import re

conn = psycopg2.connect("dbname=ifsc")

# NOTE: Just world cups
comp_base_url = 'http://www.ifsc-climbing.org/index.php/world-competition#!year=2016&filter[cat_id]=69&filter[cup]=!'

options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
url = comp_base_url
driver.get(url)
html_doc = driver.page_source
driver.close()

soup = BeautifulSoup(html_doc, 'html.parser')

# (comp table)
# id
# city
# country
# year
# start_date

competitions = soup.find(id='ifsc_calendar').findAll('div', {'class': 'competition'})

for idx, competition in enumerate(competitions):
  title = competition.find('div', {'class': 'title'}).get_text()
  location_and_year = title.split(' - ')[1]
  year = int(re.match(r'.*(20\d{2})', location_and_year).groups(1)[0])
  country = re.match(r'.*\((\w{3})\)', location_and_year).groups(0)[0]
  town = re.match(r'(.*)\(', location_and_year).groups(0)[0].strip()
  competition_rel_link = competition.find('a')['href']
  comp_id = int(re.match(r'.*WetId=(\d+)', competition_rel_link).groups(1)[0])
  date_text = competition.find('div', {'class': 'date'}).get_text()
  month = re.match(r'.*(January|February|March|April|May|June|July|August|September|October|November|December).*', date_text).groups(1)[0].strip()
  start_date = int(re.match(r'(\d{1,2}).*', date_text).groups(1)[0])

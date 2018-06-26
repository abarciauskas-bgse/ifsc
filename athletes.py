from bs4 import BeautifulSoup
from selenium import webdriver
import psycopg2
from psycopg2.extensions import AsIs

conn = psycopg2.connect("dbname=ifsc")

# for chrome driver: export PATH=$PATH:~/Projects/ifsc/
base_url = 'http://www.ifsc-climbing.org/index.php?option=com_ifsc&view=athlete&id='
athleteid = 9238

options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
url = '{0}{1}'.format(base_url, athleteid)
driver.get(url)
html_doc = driver.page_source
driver.close()

soup = BeautifulSoup(html_doc, 'html.parser')
athlete_data = {}
athlete_data['id'] = athleteid
name = soup.findAll('h1', {'class': 'name'})[0].get_text().strip()
names = name.split(' ')
athlete_data['first_name'] = names[0]
athlete_data['last_name'] = (' ').join(names[1:])

personal_data = soup.find(id="panel_information")
attributes = ['birthdate', 'nation', 'height', 'weight', 'city', 'federation']
for attr in attributes:
  value = personal_data.findAll('dt', {'class': attr})[0].get_text().strip()
  athlete_data[attr] = value

print(athlete_data)

cursor = conn.cursor()
columns = athlete_data.keys()
values = athlete_data.values()
insert_statement_template = 'insert into athletes (%s) values %s'
insert_statement = cursor.mogrify(insert_statement_template, (AsIs(','.join(columns)), tuple(values)))
print(insert_statement)
cursor.execute(insert_statement)
conn.commit()


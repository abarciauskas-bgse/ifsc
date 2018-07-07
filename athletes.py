from bs4 import BeautifulSoup
from selenium import webdriver
import helpers

# for chrome driver: export PATH=$PATH:~/Projects/ifsc/
base_url = 'http://www.ifsc-climbing.org/index.php?option=com_ifsc&view=athlete&id='
athlete_id_start = 9237
athlete_id_end = 9240

def generate_athlete_data(athlete_id):
  url = '{0}{1}'.format(base_url, athlete_id)
  soup = helpers.fetch_page(url)
  name = soup.findAll('h1', {'class': 'name'})[0].get_text().strip()
  names = name.split(' ')
  personal_data = soup.find(id="panel_information")
  attributes = ['birthdate', 'nation', 'height', 'weight', 'city', 'federation']

  athlete_data = {
    'id': athlete_id,
    'first_name': names[0],
    'last_name': (' ').join(names[1:])
  }
  for attr in attributes:
    value = personal_data.find('dt', {'class': attr}).get_text().strip()
    value = value if value else None
    athlete_data.update({attr: value})
  return athlete_data

for athlete_id in range(athlete_id_start, athlete_id_end):
  data = generate_athlete_data(athlete_id)
  helpers.insert_row('athletes', data)

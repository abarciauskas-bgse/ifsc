import re
import helpers

first_year = 2000
last_year = 2018

# NOTE: Just world cups
comp_base_url = 'http://www.ifsc-climbing.org/index.php/world-competition#!year=2016&filter[cat_id]=69&filter[cup]=!'

soup = helpers.fetch_page(comp_base_url)
competitions = soup.find(id='ifsc_calendar').findAll('div', {'class': 'competition'})

def generate_comp_data(competition_html):
  competition_rel_link = competition_html.find('a')['href']
  comp_id = int(re.match(r'.*WetId=(\d+)', competition_rel_link).groups(1)[0])
  title = competition_html.find('div', {'class': 'title'}).get_text()
  location_and_year = title.split(' - ')[1]
  country = re.match(r'.*\((\w{3})\)', location_and_year).groups(0)[0]
  town = re.match(r'(.*)\(', location_and_year).groups(0)[0].strip()
  year = int(re.match(r'.*(20\d{2})', location_and_year).groups(1)[0])
  date_text = competition_html.find('div', {'class': 'date'}).get_text()
  month = re.match(r'.*(January|February|March|April|May|June|July|August|September|October|November|December).*', date_text).groups(1)[0].strip()
  month_day = int(re.match(r'(\d{1,2}).*', date_text).groups(1)[0])
  return {
    'id': comp_id,
    'town': town,
    'country': country,
    'year': year,
    'month': helpers.month_indices[month],
    'month_day': month_day
  }  

for idx, competition_html in enumerate(competitions[1:2]):
  data = generate_comp_data(competition_html)
  helpers.insert_row('comps', data)

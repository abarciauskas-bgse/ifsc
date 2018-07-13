import helpers
import re
import sys

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

def comps_for_year(year):
  # NOTE: Just world cups
  comp_base_url = """
    http://www.ifsc-climbing.org/index.php/world-competition#!year=
    {0}&filter[cat_id]=69&filter[cup]=!
    """.format(year)
  soup = helpers.fetch_page(comp_base_url)
  competitions = soup.find(id='ifsc_calendar').findAll('div', {'class': 'competition'})

  for competition_html in competitions:
    data = generate_comp_data(competition_html)
    print('inserting competition {0} for year {1}'.format(data['id'], data['year']))
    helpers.insert_row('comps', data)

# Loop through each year of interest. Fetch world cups competition list page and
# store each comp.
def get_all_comps(start_year, end_year):
  helpers.parallelize(comps_for_year, range(start_year, end_year))

get_all_comps(2006, 2018)

from bs4 import BeautifulSoup
from selenium import webdriver
import psycopg2
from psycopg2.extensions import AsIs
import json

conn = psycopg2.connect("dbname=ifsc")

comp_id = 6158
category = 5 # women's bouldering
stage_to_route = {
  'final': 3 # final, 2 - semifinal
}
comp_stage = 'final'

comp_base_url = 'http://www.ifsc-climbing.org/index.php/world-competition/calendar#!'
comp_stage_url = 'comp={0}&cat={1}&route={2}'.format(comp_id, category, stage_to_route[comp_stage])

options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
url = '{0}{1}'.format(comp_base_url, comp_stage_url)
driver.get(url)
html_doc = driver.page_source
driver.close()

soup = BeautifulSoup(html_doc, 'html.parser')
results_table = soup.find(id='ifsc_calendar').find('table', {'class': 'DrTable'})
results = results_table.findAll('tr')

# table_col_names = results[0]

for idx, result in enumerate(results[1:]):
  comp_result_data = {'comp_id': comp_id, 'comp_stage': comp_stage}  
  comp_result_data['comp_stage_rank'] = idx + 1
  comp_result_data['athelete_id'] = int(result['id'])
  comp_result_data['previous_heat'] = int(result.find('td', {'class': 'rank_prev_heat'}).get_text())
  if category == 5:
    all_bonus_tries = result.findAll('div', {'class': 'bonusTries'})
    for bidx, btry in enumerate(all_bonus_tries):
      comp_result_data['boulder_{0}_bonus_tries'.format(bidx+1)] = int(btry.get_text())
    all_top_tries = result.findAll('div', {'class': 'topTries'})
    for tidx, ttry in enumerate(all_top_tries):
      comp_result_data['boulder_{0}_top_tries'.format(tidx+1)] = int(ttry.get_text())
    # FIXME: Not sure this will always work, should do a validation here
    final_result = result.find('td', {'class': None}).findAll('div')
    tops = final_result[0].get_text().split('t')
    bonuses = final_result[1].get_text().split('b')
    comp_result_data['tops'] = int(tops[0]) if tops[0] else 0
    comp_result_data['top_tries'] = int(tops[1]) if tops[1] else 0
    comp_result_data['bonuses'] = int(bonuses[0]) if bonuses[0] else 0
    comp_result_data['bonus_tries'] = int(bonuses[1]) if bonuses[1] else 0    
  print(json.dumps(comp_result_data, indent=2))

# (per comp stage)
# comp_id 
# comp_stage
#
# (per athlete)
# comp_stage_rank
# athelete_id
# previous heat
#
# (bouldering-specific)
# tops
# top_tries
# bonuses
# bonus_tries
# boulder_1_top_tries
# boulder_1_bonus_tries
# boulder_2_top_tries
# boulder_2_bonus_tries
# boulder_3_top_tries
# boulder_3_bonus_tries
# boulder_4_top_tries
# boulder_4_bonus_tries


import helpers

# TODO: Look up all comp ids in the DB and iterate through combinations of
# categories and stages.
comp_id = 6158
categories = {
  'womens_bouldering': 5,
  'mens_bouldering': 6
}
stage_to_route = {
  'final': 3,
  'semifinal': 2
}
comp_stage = 'final'
category = 'womens_bouldering'

comp_base_url = 'http://www.ifsc-climbing.org/index.php/world-competition/calendar#!'
comp_stage_url = 'comp={0}&cat={1}&route={2}'.format(
  comp_id,
  categories[category],
  stage_to_route[comp_stage]
)

url = '{0}{1}'.format(comp_base_url, comp_stage_url)
soup = helpers.fetch_page(url)

results_table = soup.find(id='ifsc_calendar').find('table', {'class': 'DrTable'})
results = results_table.findAll('tr')
# table_col_names = results[0]

def generate_results_data(idx, result):
  comp_result_data = {
    'comp_id': comp_id,
    'comp_stage': comp_stage,
    'comp_stage_rank': idx + 1,
    'athelete_id': int(result['id']),
    'previous_heat': int(result.find('td', {'class': 'rank_prev_heat'}).get_text())
  }
  if categories[category] in [5, 6]:
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
    comp_result_data.update({
      'tops': int(tops[0]) if tops[0] else 0,
      'top_tries': int(tops[1]) if tops[1] else 0,
      'bonuses': int(bonuses[0]) if bonuses[0] else 0,
      'bonus_tries': int(bonuses[1]) if bonuses[1] else 0
    })
    return comp_result_data

for idx, result in enumerate(results[1:]):
  data = generate_results_data(idx, result)
  helpers.insert_row('comp_result', data)

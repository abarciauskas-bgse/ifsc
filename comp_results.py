import helpers
import json
import re
import traceback

def generate_results_data(idx, result, comp_id, comp_stage, category):
  athlete_id = int(result['id'])
  previous_heat = result.find('td', {'class': 'rank_prev_heat'})
  comp_result_data = {
    'id': int('{0}{1}{2}'.format(comp_id, stage_to_route[comp_stage], athlete_id)),
    'category': category,
    'comp_id': comp_id,
    'comp_stage': comp_stage,
    'comp_stage_rank': int(result.find('td', {'class': 'result_rank'}).get_text()),
    'athlete_id': athlete_id
  }
  if 'bouldering' in category:
    all_bonus_tries = result.findAll('div', {'class': 'bonusTries'})
    for bidx, btry in enumerate(all_bonus_tries):
      tries = int(btry.get_text())
      comp_result_data['boulder_{0}_bonus_tries'.format(bidx+1)] = tries
    all_top_tries = result.findAll('div', {'class': 'topTries'})
    for tidx, ttry in enumerate(all_top_tries):
      tries = int(ttry.get_text())     
      comp_result_data['boulder_{0}_top_tries'.format(tidx+1)] = tries
    # FIXME: Not sure this will always work, should do a validation here
    final_result = result.find('td', {'class': None}).findAll('div')
    tops = final_result[0].get_text().split('t')
    bonuses = final_result[1].get_text().split('b')
    comp_result_data.update({
      'tops': int(tops[0]) if tops[0] else 0,
      'top_tries': int(tops[1]) if tops[1] else 0,
      'bonuses': int(bonuses[0]) if bonuses[0] else 0,
      'bonus_tries': int(bonuses[1]) if bonuses[1] else 0,
      'previous_heat': int(previous_heat.get_text()) if previous_heat else None
    })
  elif 'lead' in category:
    lead_result = result.find('td', {'class': 'result'}).get_text()
    if re.search('\\+', lead_result):
      lead_result = float(lead_result.replace('+', ''))
      lead_result = lead_result + 0.5 # arbitrary quantification of upward progress
    if re.search('\\-', lead_result):
      lead_result = float(lead_result.replace('-', ''))
      lead_result = lead_result - 0.5 # arbitrary quantification of upward progress      
    elif lead_result == 'Top':
      lead_result = 100 # arbitrary quantification of a top
    else:
      lead_result = float(lead_result)
    comp_result_data.update({
      'result': lead_result,
      'previous_heat': float(previous_heat.get_text())
    })
  return comp_result_data

categories = {
  'mens_lead': 1,
  'womens_lead': 2,
  'womens_bouldering': 5,
  'mens_bouldering': 6
}

stage_to_route = {
  'final': 3,
  'semifinal': 2
}

def fetch_comp_results(comp_id):
  try:
    # TODO: Iterate through combinations of
    # categories and stages.
    for category in categories.keys():
      for comp_stage in stage_to_route.keys():
        comp_base_url = 'http://www.ifsc-climbing.org/index.php/world-competition/calendar#!'
        comp_stage_url = 'comp={0}&cat={1}&route={2}'.format(
          comp_id,
          categories[category],
          stage_to_route[comp_stage]
        )
        url = '{0}{1}'.format(comp_base_url, comp_stage_url)
        soup = helpers.fetch_page(url)
        results_table = soup.find(id='ifsc_calendar').find('table', {'class': 'DrTable'})
        if results_table:
          results = results_table.findAll('tr')
          # table_col_names = results[0]
          for idx, result in enumerate(results[1:]):
            data = generate_results_data(idx, result, comp_id, comp_stage, category)
            table = re.sub(r'womens_|mens_', '', category)
            print(
              'Inserting result for competition {0}, stage {1}, athelete {2} into table {3}'
                  .format(data['comp_id'], data['comp_stage'], data['athlete_id'], table)
            )
            helpers.insert_row('{0}_comp_results'.format(table), data)
  except Exception as e:
    print(e)

def fetch_all_comp_results():
  # scoring changed between 2006 and 2007
  # 2007 had bonuses 
  # it changed again in 2018 to zones
  comp_ids = helpers.fetch_all('id', 'comps', 'year >= 2007')
  print('ids: {0}'.format(comp_ids))
  helpers.parallelize(fetch_comp_results, comp_ids)

fetch_all_comp_results()

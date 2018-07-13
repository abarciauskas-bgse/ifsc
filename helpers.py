from bs4 import BeautifulSoup
import multiprocessing
import sys
sys.path.append('/Users/aimeebarciauskas/Library/Python/3.6/lib/python/site-packages')
from selenium import webdriver
import psycopg2
from psycopg2.extensions import AsIs

def fetch_all(columns, table, where):
  conn = psycopg2.connect('dbname=ifsc')
  cursor = conn.cursor()
  query = 'select {0} from {1}'.format(columns, table)
  if where:
    query = '{0} where {1}'.format(query, where)
  cursor.execute(query)
  rows = cursor.fetchall()
  return list(map(lambda row: row[0], rows))

def fetch_page(url):
  options = webdriver.ChromeOptions()
  driver = webdriver.Chrome()
  driver.get(url)
  html_doc = driver.page_source
  driver.close()
  return BeautifulSoup(html_doc, 'html.parser')

def insert_row(table, data):
  try:
    # TODO: should re-use connection
    conn = psycopg2.connect('dbname=ifsc')
    cursor = conn.cursor()
    columns = data.keys()
    values = data.values()
    insert_statement_template = 'insert into {0} (%s) values %s'.format(table)
    insert_statement = cursor.mogrify(insert_statement_template, (AsIs(','.join(columns)), tuple(values)))
    print(insert_statement)
    cursor.execute(insert_statement)
    conn.commit()
  except Exception as e:
    print('Exception raised: {0}'.format(e))
    conn.close()

def parallelize(fn, maplist):
  pool = multiprocessing.Pool(multiprocessing.cpu_count())
  mr = pool.map_async(fn, maplist)
  while not mr.ready():
    sys.stdout.flush()
    sys.stderr.flush()
    mr.wait(0.1)
  pool.close()
  pool.join()  

month_indices = {
  'January': 1,
  'February': 2,
  'March': 3,
  'April': 4,
  'May': 5,
  'June': 6,
  'July': 7,
  'August': 8,
  'September': 9,
  'October': 10,
  'November': 11,
  'December': 12
}

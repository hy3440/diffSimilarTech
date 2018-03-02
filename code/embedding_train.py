import gensim
import logging
import mysql.connector
from prepros import get_words


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

cnx = mysql.connector.connect(host='localhost',
                              user='root',
                              password='yfwrshgrm',
                              db='stackoverflow')
cursor = cnx.cursor()
query = "SELECT Id, Body FROM Posts WHERE Score >= 0 AND Id >= {} AND Id < {}".format(start, start+200000)
cursor.execute(query)
for current_id, row in cursor.fetchall():

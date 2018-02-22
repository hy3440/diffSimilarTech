from prepros import get_words
# import mysql.connector
from tech_sentences import check_tech_pairs_v2
import os
import pickle

# cnx = mysql.connector
#
# cnx = mysql.connector.connect(host='localhost',
#                               user='root',
#                               password='yfwrshgrm',
#                               db='stackoverflow')
# cursor = cnx.cursor()
# query = "SELECT Body FROM Posts WHERE Id=120140"
# cursor.execute(query)

words = get_words("Basically he was saying that ASP.NET MVC is not for large-scale enterprise applications")
print(words[0])
(line, techs) = check_tech_pairs_v2(words[0])
print(line)

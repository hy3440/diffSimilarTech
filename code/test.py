import nltk
import os
import pickle
from prepros import add_patterns, get_cv_and_cin, get_words
import pymysql.cursors
import spacy
from spacy.matcher import Matcher
import sys
import webbrowser

# nlp = spacy.load('en')
# matcher = Matcher(nlp.vocab)
# adds_patterns(matcher)
# pos_tag = "CV VBG APP CV APP"
# pattern = matcher(nlp(u'{}'.format(pos_tag)))
# print pattern


# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='yfwrshgrm',
#                              db='stackoverflow')
# try:
#     with connection.cursor() as cursor:
#         # word = "java"
#         num = sys.argv[1]
#         cursor.execute("SELECT Body FROM Posts WHERE Id={}".format(num))
#         # for i in range(cursor.rowcount):
#         row = cursor.fetchall()
#         with open("{}.html".format(num), "a") as f:
#             f.write(str(row))
#         f.close()
#         webbrowser.get('mozilla').open_new_tab(os.path.join(os.getcwd(), "{}.html".format(num)))
#         # print body
#         # pos_tag = nltk.pos_tag(row)
# finally:
#     connection.close()

# # Insert pairs.txt into mysql
# cursor = connection.cursor()
# count = 1
# with open(os.path.join(os.pardir, "Data", "cateInGroups_freq100_v2.txt")) as data_file:
#     for line in data_file:
#         tech_list = line.split("\t")
#         first = tech_list[0]
#         second = tech_list[1]
#         sql = "INSERT INTO pairs(Id, First, Second) VALUES ('%d', '%s', '%s')" % (count, first, second)
#         cursor.execute(sql)
#         connection.commit()
#         count += 1
# connection.close()

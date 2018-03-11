"""
Open Post.
python3 open_post.py $POSTID
"""

import mysql.connector
import os
# import pymysql.cursors
import sys
import webbrowser

cnx = mysql.connector.connect(host='localhost',
                             user='root',
                             password='yfwrshgrm',
                             db='stackoverflow')

cursor = cnx.cursor()
# word = "java"
num = sys.argv[1]
cursor.execute("SELECT Body FROM Posts WHERE Id={}".format(num))
# for i in range(cursor.rowcount):
row = cursor.fetchall()
with open("{}.html".format(num), "a") as f:
    f.write(str(row))
webbrowser.get('mozilla').open_new_tab(os.path.join(os.getcwd(), "{}.html".format(num)))
# print body
# pos_tag = nltk.pos_tag(row)

cursor.close()
cnx.close()

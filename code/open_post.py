import os
import pymysql.cursors
import sys
import webbrowser

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='yfwrshgrm',
                             db='stackoverflow')
try:
    with connection.cursor() as cursor:
        # word = "java"
        num = sys.argv[1]
        cursor.execute("SELECT Body FROM Posts WHERE Id={}".format(num))
        # for i in range(cursor.rowcount):
        row = cursor.fetchall()
        with open("{}.html".format(num), "a") as f:
            f.write(str(row))
        f.close()
        webbrowser.get('mozilla').open_new_tab(os.path.join(os.getcwd(), "{}.html".format(num)))
        # print body
        # pos_tag = nltk.pos_tag(row)
finally:
    connection.close()

# Save all tags in ../data/tags.pkl

import mysql.connector
import os
import pickle

cnx = mysql.connector.connect(host='localhost',
                              user='root',
                              password='yfwrshgrm',
                              db='stackoverflow')
cursor = cnx.cursor()
query = "SELECT Id, TagName FROM tags"
cursor.execute(query)

tags = set()
for _, row in cursor.fetchall():
    tags.add(row)

with open(os.path.join(os.pardir, "data", "tags.pkl"), 'wb') as tags_file:
    pickle.dump(tags, tags_file)

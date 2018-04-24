import datetime
from multiprocessing import Process
import mysql.connector
import operator
import os.path
import pickle
from prepros import get_words

batch = 5951929
# batch = 100
s = batch * 8 * 0
table_name = "Posts"
pw = "yfwrshgrm"
techa = "heapsort"
techb = "quicksort"
# techa = 'branch'
# techb = 'merge'


def main(start):
    compa_sent_count = 0
    total_sent_count = 0
    post_count = 0
    current_id = 0
    try:
        cnx = mysql.connector.connect(host='localhost',
                                      user='root',
                                      password=pw,
                                      db='stackoverflow')
        cursor = cnx.cursor()
        query = "SELECT Id, Body FROM {} WHERE PostTypeId=1 AND Score > 0 AND Id >= {} AND Id < {} AND (Title Like \'%{}%{}%\' OR Title Like \'%{}%{}%\')".format(table_name, start, start+batch, techa, techb, techb, techa)
        cursor.execute(query)
        for current_id, row in cursor.fetchall():
            with open(os.path.join(os.pardir, "usefulness", "{}.txt".format(os.getpid())), "a") as out_file:
                out_file.write(str(current_id)+"\n")
            # post_count += 1
            # word_list = get_words(row)
            # total_sent_count += len(word_list)
            #
            # for words in word_list:
            #     if words == []:
            #         continue
            #     if techa in words and techb in words:
            #         compa_sent_count += 1
            #         data_file = open(os.path.join(os.pardir, "usefulness", table_name, "{}.txt".format(os.getpid())), "a")
            #         data_file.write("{}\n".format(current_id))
            #         data_file.write("{}\n".format(rtn[1]))
            #         data_file.write("{}\n".format(rtn[0]))
            #         data_file.write("\n")
            #         data_file.close()
    finally:
        print("Proc {}: {}/{} from {} to {} ({} posts)".format(os.getpid(), compa_sent_count, total_sent_count, start, current_id, post_count))

datalist = [j*batch + s for j in range(8)]

procs = []
for i in range(8):
    proc = Process(target=main, args=(datalist[i],))
    procs.append(proc)
    proc.start()

for proc in procs:
    proc.join()

print(datetime.datetime.now())

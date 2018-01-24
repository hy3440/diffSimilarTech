import os.path
import pickle
from prepros import get_words
import pymysql.cursors
import sys
import time

start_time = time.time()
compa_sent_count = 0
total_sent_count = 0
post_count = 0

pkl_file = open(os.path.join(os.pardir, "Data", "pairs.pkl"), 'rb')
pairs = pickle.load(pkl_file)
pkl_file.close()

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='{}'.format(sys.argv[1]),
                             db='stackoverflow')


start = 100000
end = 200000


def contains_key_tech(words):
    for key in pairs.keys():
        if key in words:
            for value in pairs[key]:
                if value in words:
                    return True
    return False

try:
    with connection.cursor() as cursor:
        sql = "SELECT Id, Body FROM Posts WHERE Score >= 0 AND Id >= {} AND Id < {}".format(start, end)
        cursor.execute(sql)
        for i in range(cursor.rowcount):
            post_count += 1
            current_id, row = cursor.fetchone()
            word_list = get_words(row)
            total_sent_count += len(word_list)

            for words in word_list:
                if contains_key_tech(words):
                    compa_sent_count += 1
                    data_file = open(os.path.join(os.pardir, "Data", "key_tech", "key_tech_sentences_2.txt"), "a")
                    data_file.write("{}\n".format(current_id))
                    data_file.write(" ".join(words))
                    data_file.write("\n")
                    data_file.close()

finally:
    end_time = time.time()
    summary_file = open(os.path.join(os.pardir, "Data", "key_tech", "key_tech_summary.txt"), "a")
    summary_file.write("Id from {} to {} in {}\n".format(start, current_id, end_time-start_time))
    summary_file.write("Comparative sentences: {}\n".format(compa_sent_count))
    summary_file.write("Sentence number: {}\n".format(total_sent_count))
    summary_file.write("Post number: {}\n".format(post_count))
    summary_file.write("\n")
    summary_file.close()
    connection.close()

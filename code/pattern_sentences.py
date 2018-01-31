import nltk
import os.path
from prepros import get_cv_and_cin, add_patterns, get_words
import pymysql.cursors
import spacy
from spacy.matcher import Matcher
import sys
import time


start_time = time.time()
count = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0}
compa_sent_count = 0
total_sent_count = 0
post_count = 0

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='{}'.format(sys.argv[1]),
                             db='stackoverflow')

(cv, cin) = get_cv_and_cin()

nlp = spacy.load('en')
matcher = Matcher(nlp.vocab)
add_patterns(matcher)

start_id = start = 20000
end = 50000
try:
    with connection.cursor() as cursor:
        while(start < end):
            sql = "SELECT Id, Body FROM Posts WHERE Score >= 0 AND Id >= {} AND Id < {}".format(start, start+100)
            cursor.execute(sql)
            for current_id, row in cursor.fetchall():
                post_count += 1
                # row = cursor.fetchone()
                word_list = get_words(row)
                total_sent_count += len(word_list)

                for sent in word_list:
                    tagged_words = nltk.pos_tag(sent)
                    # print tagged_words
                    tag_list = []
                    for (word, tag) in tagged_words:
                        if tag == "IN" and word in cin:
                            tag_list.append("CIN")
                        elif tag[:2] == "VB" and word in cv:
                            tag_list.append("CV")
                        else:
                            cursor.execute("SELECT * FROM Tags WHERE TagName = \'{}\'".format(word))
                            if cursor.rowcount == 0:
                                tag_list.append(tag)
                            else:
                                tag_list.append("APP")

                    pos_tag = " ".join(tag_list)
                    # print pos_tag
                    patterns = matcher(nlp(u'{}'.format(pos_tag)))
                    if patterns != []:
                        compa_sent_count += 1
                        for pattern in patterns:
                            count[str(pattern[0])] += 1
                            data_file = open(os.path.join(os.pardir, "out", "pattern", "{}.txt".format(pattern[0])), "a")
                            data_file.write("{}\n".format(current_id))
                            data_file.write(" ".join(sent))
                            data_file.write("\n")
                            data_file.close()
            start += 100
finally:
    end_time = time.time()
    summary_file = open(os.path.join(os.pardir, "out", "pattern", "pattern_summary.txt"), "a")
    summary_file.write("Id from {} to {} in {}\n".format(start_id, current_id, end_time-start_time))
    summary_file.write("Comparative sentences: {}\n".format(compa_sent_count))
    summary_file.write("Sentence number: {}\n".format(total_sent_count))
    summary_file.write("Post number: {}\n".format(post_count))
    for key, value in count.iteritems():
        summary_file.write("Pattern {}: {} sentences\n".format(key, value))
    summary_file.write("\n")
    summary_file.close()
    connection.close()

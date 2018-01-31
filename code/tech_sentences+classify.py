import datetime
import os.path
from pattern_matcher import PatternMatcher
import pickle
from prepros import get_words
import pymysql.cursors
import sys
import time

print datetime.datetime.now()
pattern_matcher = PatternMatcher()

start_time = time.time()
compa_sent_count = 0
total_sent_count = 0
post_count = 0

pairs_file = open(os.path.join(os.pardir, "data", "pairs.pkl"), 'rb')
pairs = pickle.load(pairs_file)
pairs_file.close()

synonyms_file = open(os.path.join(os.pardir, "data", "synonyms.pkl"), 'rb')
synonyms = pickle.load(synonyms_file)
synonyms_file.close()

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='{}'.format(sys.argv[1]),
                             db='stackoverflow')


start = 1000000
# start = 0
end = 2000000


def contains_tech(tech, words):
    if " " in tech:
        tech_list = tech.split(" ")
        n = len(tech_list)
        for i in range(len(words) - n + 1):
            if tech_list == words[i:i+n]:
                return True
        return False
    else:
        return tech in words

def check_tech_pairs(words):
    for first in pairs.keys():
        for first_tech in synonyms[first]:
            if contains_tech(first_tech, words):
                for second in pairs[first]:
                    for second_tech in synonyms[second]:
                        if contains_tech(second_tech, words):
                            line = " ".join(words)
                            line = line.replace(first_tech, first)
                            line = line.replace(second_tech, second)
                            return (line, first+"\t"+second)
    return None


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
                rtn = check_tech_pairs(words)
                if rtn is not None:
                    words = rtn[0].split(" ")
                    pattern_matcher.match_pattern(words, current_id, rtn[1], "keytechs")

finally:
    end_time = time.time()
    summary_file = open(os.path.join(os.pardir, "out", "tech_v3", "summary.txt"), "a")
    summary_file.write("Id from {} to {}\n".format(start, current_id))
    summary_file.write("Comparative sentences: {}\n".format(pattern_matcher.compa_sent_count))
    summary_file.write("Sentence number: {}\n".format(total_sent_count))
    # summary_file.write("Post number: {}\n".format(num))
    for key, value in pattern_matcher.count.iteritems():
        summary_file.write("Pattern {}: {} sentences\n".format(key, value))
    summary_file.write("\n")
    summary_file.close()
    pattern_matcher.connection.close()
    print datetime.datetime.now()

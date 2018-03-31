"""
Extract sentences containing similar tech pairs.
"""

import datetime
from multiprocessing import Process
import mysql.connector
import operator
import os.path
import pickle
from prepros import get_words

batch = 10000
table_name = "posts"
pw = "ccywch"
# pw = "yfwrshgrm"

similar_techs_file = open(os.path.join(os.pardir, "data", "similar_techs.pkl"), 'rb')
similar_techs = pickle.load(similar_techs_file)
similar_techs_file.close()

synonyms_file = open(os.path.join(os.pardir, "data", "synonyms.pkl"), 'rb')
synonyms = pickle.load(synonyms_file)
synonyms_file.close()

print(datetime.datetime.now())


def contains_tech(synonym, words):
    """ Test if words contains synonym.

        (str, [str]) -> bool
    """
    if "_" in synonym:
        synonym_list = synonym.split("_")
        n = len(synonym_list)
        for i in range(len(words) - n + 1):
            if synonym_list == words[i:i+n]:
                return True
        return False
    else:
        return synonym in words


def replace_synonym(synonym, tech, words):
    """ Replace the synonym in words with tech.

        (str, str, [str]) -> [str]
    """
    rtn = []
    if "_" in synonym:
        synonym_list = synonym.split("_")
        n = len(synonym_list)
        flag = True
        for i in range(len(words)):
            if i <= len(words) - n and synonym_list == words[i:i+n]:
                rtn.append(tech)
                end = i + n - 1
                flag = False
            elif flag:
                rtn.append(words[i])
            elif i == end:
                flag = True
    else:
        for word in words:
            if word == synonym:
                rtn.append(tech)
            else:
                rtn.append(word)
    return rtn


def check_tech_pairs(words):
    """ Test if words contain similar tech pairs and replace synonym with tech.

        ([str]) -> (str, str)
    """
    techs_list = []
    count = 0
    tech_pairs = []
    for first, values in similar_techs.items():
        first_temp = []
        for first_synonym in synonyms[first]:
            if contains_tech(first_synonym, words):
                first_temp.append((first_synonym, first, len(first_synonym)))
        if len(first_temp) != 0:
            for second in values:
                second_temp = []
                for second_synonym in synonyms[second]:
                    if contains_tech(second_synonym, words):
                        second_temp.append((second_synonym, second, len(second_synonym)))
                if len(second_temp) != 0:
                    count += 1
                    tech_pairs.append((first, second))
                    techs_list += first_temp
                    techs_list += second_temp

    # Replace synonyms with techs in descending order of length.
    for (synonym, tech, l) in sorted(techs_list, key=operator.itemgetter(2), reverse=True):
        if synonym != tech:
            words = replace_synonym(synonym, tech, words)

    rtn = []
    for (first, second) in tech_pairs:
        if first in words and second in words:
            rtn.append(first)
            rtn.append(second)

    if len(rtn) > 0:
        return (" ".join(words), "\t".join(rtn)) # (sentence, tech pairs)
    else:
        return None


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
        query = "SELECT Id, Body FROM {} WHERE Score >= 0 AND Id >= {} AND Id < {}".format(table_name, start, start+batch)
        cursor.execute(query)
        for current_id, row in cursor.fetchall():
            post_count += 1
            word_list = get_words(row)
            total_sent_count += len(word_list)

            for words in word_list:
                if words == []:
                    continue
                print(words)
                rtn = check_tech_pairs(words)
                if rtn is not None:
                    compa_sent_count += 1
                    data_file = open(os.path.join(os.pardir, "out", "{}", "{}.txt".format(table_name, os.getpid())), "a")
                    data_file.write("{}\n".format(current_id))
                    data_file.write("{}\n".format(rtn[1]))
                    data_file.write("{}\n".format(rtn[0]))
                    data_file.write("\n")
                    data_file.close()
    finally:
        print("Proc {}: {}/{} from {} to {} ({} posts)".format(os.getpid(), compa_sent_count, total_sent_count, start, current_id, post_count))

datalist = [j*batch for j in range(8)]

procs = []
for i in range(8):
    proc = Process(target=main, args=(datalist[i],))
    procs.append(proc)
    proc.start()

for proc in procs:
    proc.join()

print(datetime.datetime.now())

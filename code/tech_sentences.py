import datetime
from multiprocessing import Process
import mysql.connector
import operator
import os.path
import pickle
from prepros import get_words

similar_techs_file = open(os.path.join(os.pardir, "data", "similar_techs.pkl"), 'rb')
similar_techs = pickle.load(similar_techs_file)
similar_techs_file.close()

synonyms_file = open(os.path.join(os.pardir, "data", "synonyms.pkl"), 'rb')
synonyms = pickle.load(synonyms_file)
synonyms_file.close()

print(datetime.datetime.now())


def contains_key_techs(words):
    techs = []
    for key in similar_techs.keys():
        if key in words:
            for value in similar_techs[key]:
                if value in words:
                    techs.append(key)
                    techs.append(value)
    if len(techs) == 0:
        return None
    else:
        return (" ".join(words), "\t".join(techs))


def contains_tech(tech, words):
    if "_" in tech:
        tech_list = tech.split("_")
        n = len(tech_list)
        for i in range(len(words) - n + 1):
            if tech_list == words[i:i+n]:
                return True
        return False
    else:
        return tech in words


def check_tech_pairs(words):
    for first in similar_techs.keys():
        for first_tech in synonyms[first]:
            if contains_tech(first_tech, words):
                line = " ".join(words)
                line = line.replace(first_tech, first)
                words = line.split(" ")
                for second in similar_techs[first]:
                    for second_tech in synonyms[second]:
                        if contains_tech(second_tech, words):
                            line = " ".join(words)
                            line = line.replace(second_tech, second)
                            return (line, first+"\t"+second)
    return None


def check_tech_pairs_v2(words):
    techs_list = []
    for key, values in synonyms.items():
        for value in values:
            if contains_tech(value, words):
                techs_list.append((value, key, len(value)))
    for(synonym, tech, l) in sorted(techs_list, key=operator.itemgetter(2), reverse=True):
        if contains_tech(synonym, words):
            line = " ".join(words).replace(synonym, tech)
            words = line.split()
    return contains_key_techs(words)


def replace_synonym(synonym, tech, words):
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


def check_tech_pairs_v3(words):
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

    for (synonym, tech, l) in sorted(techs_list, key=operator.itemgetter(2), reverse=True):
        if synonym != tech:
            words = replace_synonym(synonym, tech, words)

    rtn = []
    for (first, second) in tech_pairs:
        if first in words and second in words:
            rtn.append(first)
            rtn.append(second)

    if len(rtn) > 0:
        return (" ".join(words), "\t".join(rtn))
    else:
        return None


def some_function(start):
    compa_sent_count = 0
    total_sent_count = 0
    post_count = 0
    current_id = 0
    try:
        cnx = mysql.connector.connect(host='localhost',
                                      user='root',
                                      password='ccywch',
                                      db='stackoverflow')
        cursor = cnx.cursor()
        query = "SELECT Id, Body FROM Posts WHERE Score >= 0 AND Id >= {} AND Id < {}".format(start, start+800000)
        cursor.execute(query)
        for current_id, row in cursor.fetchall():
            post_count += 1
            word_list = get_words(row)
            total_sent_count += len(word_list)

            for words in word_list:
                rtn = check_tech_pairs_v3(words)
                if rtn is not None:
                    compa_sent_count += 1
                    data_file = open(os.path.join(os.pardir, "out", "tech_v6", "{}.txt".format(os.getpid())), "a")
                    data_file.write("{}\n".format(current_id))
                    data_file.write("{}\n".format(rtn[1]))
                    data_file.write("{}\n".format(rtn[0]))
                    data_file.write("\n")
                    data_file.close()
    finally:
        print("Proc {}: {}/{} from {} to {} ({} posts)".format(os.getpid(), compa_sent_count, total_sent_count, start, current_id, post_count))

# datalist = [120000, 130000, 140000, 150000, 160000, 170000, 180000, 190000]
# datalist = [1100000, 1900000, 2000000, 2100000, 2200000, 2300000, 2400000, 2500000]
datalist = [38500000, 39300000, 40100000, 40900000, 41700000, 42500000, 43300000, 44100000]

procs = []
for i in range(8):
    proc = Process(target=some_function, args=(datalist[i],))
    procs.append(proc)
    proc.start()

for proc in procs:
    proc.join()

print(datetime.datetime.now())

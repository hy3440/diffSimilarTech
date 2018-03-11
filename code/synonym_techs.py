"""
Process synonyms.
"""

import os
import pickle
import mysql.connector


cnx = mysql.connector.connect(host='localhost',
                              user='root',
                              password='yfwrshgrm',
                              db='stackoverflow')
cursor = cnx.cursor()
synonym_techs = {}
with open(os.path.join(os.pardir, "data", "cateInGroups_freqabove10_600_10_1_sg_v1.txt")) as data1_file:
    for line in data1_file:
        flag = True
        tech_list = line.split("\t")
        first = tech_list[0]
        second = tech_list[1]
        check_file = open(os.path.join(os.pardir, "data", "synonymAbbreviation_manualCheck.txt"))
        for synonym_tech_line in check_file:
            synonym_tech = synonym_tech_line.split(",")
            if first in synonym_tech and second in synonym_tech:
                flag = False
                break
        check_file.close()
        if flag:
            synonym_techs[first] = set()
            synonym_techs[first].add(first)
            synonym_techs[second] = set()
            synonym_techs[second].add(second)


def extract_synonyms_v2():
    with open(os.path.join(os.pardir, "data", "synonymAbbreviation_manualCheck.txt")) as data_file:
        count = 0
        for line in data_file:
            tech_list = line.split(",")
            tech_list[-1] = tech_list[-1].strip()
            for tech in tech_list:
                if tech in synonym_techs:
                    synonym_techs[tech] = set(tech_list)
                    count += 1
                    break
    print(count)
    print(len(synonym_techs))
    with open(os.path.join(os.pardir, "data", "synonyms.pkl"), 'wb') as output_file:
        pickle.dump(synonym_techs, output_file)
extract_synonyms_v2()


def extract_synonyms_v1():
    with open(os.path.join(os.pardir, "data", "synonymAbbreviation_manualCheck.txt")) as data_file:
        count = 0
        for line in data_file:
            tech_list = line.split(",")
            tech_list[-1] = tech_list[-1].strip()

            for tech in tech_list:
                if tech in synonym_techs:
                    for name in tech_list:
                        if "_" in name:
                            name_list = name.split("_")
                            synonym_techs[tech].add("".join(name_list))
                            synonym_techs[tech].add(" ".join(name_list))
                            synonym_techs[tech].add("-".join(name_list))
                            synonym_techs[tech].add(".".join(name_list))
                        else:
                            name_list = name.split("-")
                            synonym_techs[tech].add("".join(name_list))
                            synonym_techs[tech].add(" ".join(name_list))
                            synonym_techs[tech].add(".".join(name_list))
                            name_list = name.split(".")
                            synonym_techs[tech].add("".join(name_list))
                            synonym_techs[tech].add(" ".join(name_list))
                            synonym_techs[tech].add("-".join(name_list))
                    break

    for key, value in synonym_techs.items():
        if value == set():
            synonym_techs[key].add(key)
            name_list = key.split("-")
            synonym_techs[key].add("".join(name_list))
            synonym_techs[key].add(" ".join(name_list))
            synonym_techs[key].add(".".join(name_list))
            name_list = key.split(".")
            synonym_techs[key].add("".join(name_list))
            synonym_techs[key].add(" ".join(name_list))
            synonym_techs[key].add("-".join(name_list))

    if "sqlyog" in synonym_techs:
        synonym_techs["sqlyog"].add("sqlyog s")
    synonym_techs["python"].add("python s")
    synonym_techs["ormlite"].add("ormlite s")
    synonym_techs["valgrind"].add("valgrind s")
    synonym_techs["grafika"].add("grafika s")
    synonym_techs["tomahawk"].add("tomahawk s")
    synonym_techs["jquery"].add("jquery s")
    synonym_techs["firebug"].add("firebug s")

    with open(os.path.join(os.pardir, "data", "synonyms_for_all_similar_techs.pkl"), 'wb') as output_file:
        pickle.dump(synonym_techs, output_file)


def delete_all_same_techs():
    synonyms_file = open(os.path.join(os.pardir, "data", "synonyms_for_all_similar_techs.pkl"), 'rb')
    synonyms = pickle.load(synonyms_file)
    synonyms_file.close()

    print(len(synonyms))

    deleted_synonyms = {}
    for key, values in synonyms.items():
        flag = True
        if len(values) == 1:
            for value in values:
                if value == key:
                    flag = False
        if flag:
            deleted_synonyms[key] = values

    print(len(deleted_synonyms))

    with open(os.path.join(os.pardir, "data", "synonyms.pkl"), 'wb') as output_file:
        pickle.dump(deleted_synonyms, output_file)

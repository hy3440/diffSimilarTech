import os
import pickle
import pymysql.cursors


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='yfwrshgrm',
                             db='stackoverflow')
cursor = connection.cursor()
synonym_techs = {}
with open(os.path.join(os.pardir, "data", "cateInGroups_freq100_v2.txt")) as data1_file:
    for line in data1_file:
        tech_list = line.split("\t")
        first = tech_list[0]
        second = tech_list[1]
        synonym_techs[first] = set()
        synonym_techs[second] = set()

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

with open(os.path.join(os.pardir, "data", "synonyms.pkl"), 'wb') as output_file:
    pickle.dump(synonym_techs, output_file)

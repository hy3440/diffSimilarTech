import os
import pickle
import mysql.connector


# with open(os.path.join(os.pardir, "data", "cateInGroups_freq100_v2.txt")) as data_file:
#     for line in data_file:
#         flag = True
#         techs = line.split("\t")
#         first = techs[0]
#         second = techs[1]
#         check_file = open(os.path.join(os.pardir, "data", "synonymAbbreviation_manualCheck.txt"))
#         for synonym_tech in check_file:
#             if first in synonym_tech and second in synonym_tech:
#                 flag = False
#                 break
#         check_file.close()
#         if flag:
#             if first in second or second in first:
#                 print("{}\t{}".format(first, second))

def get_similar_techs():
    """This method is used to read similar technique pairs from text, to delete
       synonyms and to store in a dictionary ../data/similar_techs.pkl.

    """
    similar_techs = {}
    count = 0
    with open(os.path.join(os.pardir, "data", "cateInGroups_freqabove10_600_10_1_sg_v1.txt")) as data_file:
        for line in data_file:
            flag = True
            techs = line.split("\t")
            first = techs[0]
            second = techs[1]
            check_file = open(os.path.join(os.pardir, "data", "synonymAbbreviation_manualCheck.txt"))
            for synonym_tech_line in check_file:
                synonym_tech = synonym_tech_line.split(",")
                if first in synonym_tech and second in synonym_tech:
                    flag = False
                    break
            check_file.close()
            if flag:
                count += 1
                if first in similar_techs:
                    similar_techs[first].add(second)
                elif second in similar_techs:
                    similar_techs[second].add(first)
                else:
                    temp = set()
                    temp.add(second)
                    similar_techs[first] = temp
                # if len(first) >= len(second):
                #     if first in similar_techs:
                #         similar_techs[first].add(second)
                #     else:
                #         temp = set()
                #         temp.add(second)
                #         similar_techs[first] = temp
                # else:
                #     if second in similar_techs:
                #         similar_techs[second].add(first)
                #     else:
                #         temp = set()
                #         temp.add(first)
                #         similar_techs[second] = temp

    with open(os.path.join(os.pardir, "data", "similar_techs.pkl"), 'wb') as output_file:
        pickle.dump(similar_techs, output_file)
    print(count)
get_similar_techs()

def get_key_tech_dictionary():
    """This method is used to read similar technique pairs from text and to
       store in a dictionary ../data/pairs.pkl.

       original version.
    """
    count = 0
    pairs = {}
    with open(os.path.join(os.pardir, "data", "cateInGroups_freq100_v2.txt")) as data_file:
        for line in data_file:
            tech_list = line.split("\t")
            first = tech_list[0]
            second = tech_list[1]
            # if first == "java" or second == "java":
            #     print "first: {}, second: {}\n".format(first, second)
            #     print line
            if first in pairs:
                pairs[first].add(second)
            elif second in pairs:
                pairs[second].add(first)
            else:
                temp = set()
                temp.add(second)
                pairs[first] = temp
            count += 1

    with open(os.path.join(os.pardir, "data", "pairs.pkl"), 'wb') as output_file:
        pickle.dump(pairs, output_file)


def import_key_tech():
    """Read tech pairs from text and import to mysql.
    """
    key_tech = set()
    with open(os.path.join(os.pardir, "data", "cateInGroups_freq100_v2.txt")) as data_file:
        for line in data_file:
            tech_list = line.split("\t")
            first = tech_list[0]
            second = tech_list[1]
            key_tech.add(first)
            key_tech.add(second)
    connection = mysql.connector.connect(host='localhost',
                                 user='root',
                                 password='yfwrshgrm',
                                 db='stackoverflow')
    cursor = connection.cursor()
    count = 1
    for tech in key_tech:
        sql = "INSERT INTO keytechs(Id, TagName) VALUES ('%d', '%s')" % (count, tech)
        cursor.execute(sql)
        connection.commit()
        count += 1
    connection.close()

def import_similar_techs():
    connection = mysql.connector.connect(host='localhost',
                                 user='root',
                                 password='yfwrshgrm',
                                 db='stackoverflow')
    cursor = connection.cursor()
    count = 1
    with open(os.path.join(os.pardir, "data", "cateInGroups_freqabove10_600_10_1_sg_v1.txt")) as data_file:
        for line in data_file:
            tech_list = line.split("\t")
            first = tech_list[0]
            second = tech_list[1]
            query = "INSERT INTO similartechs(Id, TechA, TechB) VALUES ('%d', '%s', '%s')" % (count, first, second)
            cursor.execute(query)
            connection.commit()
            count += 1
    connection.close()
    print(count)
import_similar_techs()

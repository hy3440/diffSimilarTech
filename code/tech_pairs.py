import os
import pickle
import pymysql.cursors


def get_key_tech_dictionary():
    """This method is used to read similar technique pairs from text and to
       store in a dictionary ../Data/pairs.pkl.
    """
    count = 0
    pairs = {}
    with open(os.path.join(os.pardir, "Data", "cateInGroups_freq100_v2.txt")) as data_file:
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
    print count
    print len(pairs.keys())
    print len(pairs.values())
    data_file.close()

    with open(os.path.join(os.pardir, "Data", "pairs.pkl"), 'wb') as output_file:
        pickle.dump(pairs, output_file)
    output_file.close()


def get_key_tech():
    """Read tech pairs from text and import to mysql.
    """
    key_tech = set()
    with open(os.path.join(os.pardir, "Data", "cateInGroups_freq100_v2.txt")) as data_file:
        for line in data_file:
            tech_list = line.split("\t")
            first = tech_list[0]
            second = tech_list[1]
            key_tech.add(first)
            key_tech.add(second)
    data_file.close()
    connection = pymysql.connect(host='localhost',
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

import datetime
from multiprocessing import Process
import mysql.connector
import operator
import os.path
import pickle
from prepros import get_words
import spacy
from spacy.matcher import Matcher
from nltk import pos_tag
from nltk.tag.stanford import CoreNLPPOSTagger
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np


table_name = "Posts"
pw = "yfwrshgrm"
# techs = {"heapsort", "quicksort"}  # 2467751
# ({"compiled-language", "interpreted-language"}, 3265357)

candidates = [({"post", "get"}, 46585),
              ({"udp", "tcp"}, 5970383),
              ({"quicksort", "mergesort"}, 70402),
              ({"vmware", "virtualbox"}, 630179),
              ({"awt", "swing"}, 408820),
             ]
# techs = {"mysql", "postgresql"} # 724867
# Comparative verbs
cv = {"beat", "beats", "prefer", "prefers", "recommend", "recommends",
      "defeat", "defeats", "kill", "kills", "lead", "leads", "obliterate",
      "obliterates", "outclass", "outclasses", "outdo", "outdoes",
      "outperform", "outperforms", "outplay", "outplays", "overtake",
      "overtakes", "smack", "smacks", "subdue", "subdues", "surpass",
      "surpasses", "trump", "trumps", "win", "wins", "blow", "blows",
      "decimate", "decimates", "destroy", "destroys", "buy", "buys",
      "choose", "chooses", "favor", "favors", "grab", "grabs", "pick",
      "picks", "purchase", "purchases", "select", "selects", "race",
      "races", "compete", "competes", "match", "matches", "compare",
      "compares", "lose", "loses", "suck", "sucks"}

# Comparative prepositions
cin = {"than", "over", "beyond", "upon", "as", "against", "out", "behind",
       "under", "between", "after", "unlike", "with", "by", "opposite", "to"}


def add_patterns(matcher):
    """ Add custom patterns to mathcer.

        (Matcher) -> None
    """
    matcher.add(3,
                None,
                [{'ORTH': 'JJR'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                [{'ORTH': 'JJR'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                [{'ORTH': 'JJR'}, {'ORTH': 'CIN'}, {}, {'ORTH': 'TECH'}],
                [{'ORTH': 'JJR'}, {}, {'ORTH': 'CIN'}, {}, {'ORTH': 'TECH'}])
    # matcher.add(1,
    #             None,
    #             [{'ORTH': 'RB'}, {'ORTH': 'JJ'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
    #             [{'ORTH': 'RB'}, {'ORTH': 'JJ'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}])
    matcher.add(4,
                None,
                [{'ORTH': 'RBR'}, {'ORTH': 'JJ'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                [{'ORTH': 'RBR'}, {'ORTH': 'JJ'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}])
    matcher.add(5,
                None,
                [{'ORTH': 'CV'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                [{'ORTH': 'CV'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}])
    matcher.add(6,
                None,
                [{'ORTH': 'CV'}, {'ORTH': 'VB'}, {'ORTH': 'TECH'}])
    # matcher.add(7,
    #             None,
    #             [{'ORTH': 'CV'}, {'ORTH': 'TECH'}])
    # matcher.add(5,
    #             None,
    #             [{'ORTH': 'VB'}, {'ORTH': 'VBN'}, {'ORTH': 'TECH'}],
    #             [{'ORTH': 'VB'}, {'ORTH': 'VBN'}, {}, {'ORTH': 'TECH'}])
    # matcher.add(6,
    #             None,
    #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'JJS'}],
    #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'JJS'}],
    #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJS'}],
    #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJS'}])
    matcher.add(2,
                None,
                [{'ORTH': 'TECH'}, {'ORTH': 'VB'}, {'ORTH': 'RBR'}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VB'}, {'ORTH': 'RBR'}],
                [{'ORTH': 'TECH'}, {'ORTH': 'VB'}, {}, {'ORTH': 'RBR'}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VB'}, {}, {'ORTH': 'RBR'}],
                [{'ORTH': 'TECH'}, {'ORTH': 'VB'}, {'ORTH': 'RBR'}, {}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VB'}, {'ORTH': 'RBR'}, {}],
                [{'ORTH': 'TECH'}, {'ORTH': 'VB'}, {}, {'ORTH': 'RBR'}, {}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VB'}, {}, {'ORTH': 'RBR'}, {}])
    matcher.add(1,
                None,
                [{'ORTH': 'TECH'}, {'ORTH': 'VB'}, {'ORTH': 'JJR'}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VB'}, {'ORTH': 'JJR'}],
                [{'ORTH': 'TECH'}, {'ORTH': 'VB'}, {}, {'ORTH': 'JJR'}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VB'}, {}, {'ORTH': 'JJR'}],
                [{'ORTH': 'TECH'}, {'ORTH': 'VB'}, {'ORTH': 'JJR'}, {}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VB'}, {'ORTH': 'JJR'}, {}],
                [{'ORTH': 'TECH'}, {'ORTH': 'VB'}, {}, {'ORTH': 'JJR'}, {}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VB'}, {}, {'ORTH': 'JJR'}, {}])

def get_pos_tag(techs, words):
    """ Get POS tag of words.

        ([str], [str]) -> ([str], [str])
    """
    tags = []
    flag = False
    tagged_words = CoreNLPPOSTagger(url='http://localhost:9000').tag(words)
    if len(words) != len(tagged_words):
        tagged_words = pos_tag(words)
    words = []
    for (word, tag) in tagged_words:
        if flag:
            word = "." + word
            flag = False
        if tag == "IN" and word in cin:
            tags.append("CIN")
        elif word in cv:
            tags.append("CV")
        elif word in techs:
            tags.append("TECH")
        elif word == ".":
            flag = True
            continue
        elif tag[:2] == "VB":
            tags.append("VB")
        else:
            tags.append(tag)
        words.append(word)
    return (words, tags)


def main(techs, id):
    ids.append(" ".join(techs))
    s.append("")
    current_id = 0
    try:
        nlp = spacy.load('en')
        matcher = Matcher(nlp.vocab)
        add_patterns(matcher)
        cnx = mysql.connector.connect(host='localhost',
                                      user='root',
                                      password=pw,
                                      db='stackoverflow')
        cursor = cnx.cursor()
        query = "SELECT Id, Body FROM {} WHERE ParentId={} AND Score >= 0".format(table_name, id)
        cursor.execute(query)
        for current_id, row in cursor.fetchall():
            # with open(os.path.join(os.pardir, "usefulness", "{}.txt".format(os.getpid())), "a") as out_file:
            #     out_file.write(str(current_id)+"\n")
            word_list = get_words(row)

            for words in word_list:
                if words == []:
                    continue
                (words, tags) = get_pos_tag(techs, words)
                patterns = matcher(nlp(" ".join(tags)))
                if patterns != []:
                    ids.append(current_id)
                    s.append(" ".join(words))
    finally:
        print(current_id)
        ids.append("")
        s.append("")

ids = []
s = []
for techs, id in candidates:
    main(techs, id)
df = pd.DataFrame({'Post ID': ids,
                   'Sentence': s})
out_path = os.path.join(os.pardir, "usefulness.xlsx")
writer = ExcelWriter(out_path)
df.to_excel(writer, "sheet1", index=False)
writer.save()

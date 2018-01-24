import nltk
import os.path
from prepros import add_patterns, get_words
import pymysql.cursors
import spacy
from spacy.matcher import Matcher
import sys


class PatternMatcher:

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
    cin = {"than", "over", "beyond", "upon", "as", "against", "out", "behind",
           "under", "between", "after", "unlike", "with", "by", "opposite"}

    def __init__(self):
        self.count = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
                      "6": 0, "7": 0, "8": 0, "9": 0, "10": 0}
        self.compa_sent_count = 0

        self.nlp = spacy.load('en')
        self.matcher = Matcher(self.nlp.vocab)
        self.matcher.add(0,
                    None,
                    [{'ORTH': 'JJR'}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}],
                    [{'ORTH': 'JJR'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}],
                    [{'ORTH': 'JJR'}, {'ORTH': 'CIN'}, {}, {'ORTH': 'APP'}],
                    [{'ORTH': 'JJR'}, {}, {'ORTH': 'CIN'}, {}, {'ORTH': 'APP'}])
        self.matcher.add(1,
                    None,
                    [{'ORTH': 'RB'}, {'ORTH': 'JJ'}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}],
                    [{'ORTH': 'RB'}, {'ORTH': 'JJ'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}])
        self.matcher.add(8,
                    None,
                    [{'ORTH': 'RBR'}, {'ORTH': 'JJ'}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}],
                    [{'ORTH': 'RBR'}, {'ORTH': 'JJ'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}])
        self.matcher.add(2,
                    None,
                    [{'ORTH': 'CV'}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}],
                    [{'ORTH': 'CV'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}])
        self.matcher.add(3,
                    None,
                    [{'ORTH': 'CV'}, {'ORTH': 'VBG'}, {'ORTH': 'APP'}])
        self.matcher.add(4,
                    None,
                    [{'ORTH': 'CV'}, {'ORTH': 'APP'}])
        self.matcher.add(5,
                    None,
                    [{'ORTH': 'VB'}, {'ORTH': 'VBN'}, {'ORTH': 'APP'}],
                    [{'ORTH': 'VB'}, {'ORTH': 'VBN'}, {}, {'ORTH': 'APP'}])
        self.matcher.add(6,
                    None,
                    [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {'ORTH': 'JJS'}],
                    [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'JJS'}],
                    [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJS'}],
                    [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJS'}])
        self.matcher.add(10,
                    None,
                    [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {'ORTH': 'RBR'}],
                    [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'RBR'}],
                    [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBR'}],
                    [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBR'}])
        self.matcher.add(7,
                    None,
                    [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {'ORTH': 'JJR'}],
                    [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'JJR'}],
                    [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJR'}],
                    [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJR'}])
        self.matcher.add(9,
                    None,
                    [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
                    [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
                    [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}],
                    [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}])

        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='yfwrshgrm',
                                     db='stackoverflow')
        self.cursor = self.connection.cursor()

    def add_pos_tag(self, words, table='Tags'):
        tagged_words = nltk.pos_tag(words)
        # print tagged_words
        tag_list = []
        for (word, tag) in tagged_words:
            if tag == "IN" and word in self.cin:
                tag_list.append("CIN")
            elif tag[:2] == "VB" and word in self.cv:
                tag_list.append("CV")
            else:
                self.cursor.execute("SELECT * FROM {} WHERE TagName = \'{}\'".format(table, word))
                if self.cursor.rowcount == 0:
                    tag_list.append(tag)
                else:
                    tag_list.append("APP")
        return tag_list

    def match_pattern(self, words, current_id, table):
        tag_list = self.add_pos_tag(words, table)
        patterns = self.matcher(self.nlp(u'{}'.format(" ".join(tag_list))))
        if patterns != []:
            self.compa_sent_count += 1
            for pattern in patterns:
                self.count[str(pattern[0])] += 1
                data_file = open(os.path.join(os.pardir, "Data", "tech", "classified_by_tech", "{}.txt".format(pattern[0])), "a")
                data_file.write("{}\n".format(current_id))
                data_file.write(" ".join(words))
                data_file.write("\n")
                data_file.close()

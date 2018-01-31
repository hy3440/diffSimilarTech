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
                    [{'ORTH': 'JJR'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                    [{'ORTH': 'JJR'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                    [{'ORTH': 'JJR'}, {'ORTH': 'CIN'}, {}, {'ORTH': 'TECH'}],
                    [{'ORTH': 'JJR'}, {}, {'ORTH': 'CIN'}, {}, {'ORTH': 'TECH'}])
        self.matcher.add(1,
                    None,
                    [{'ORTH': 'RB'}, {'ORTH': 'JJ'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                    [{'ORTH': 'RB'}, {'ORTH': 'JJ'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}])
        self.matcher.add(8,
                    None,
                    [{'ORTH': 'RBR'}, {'ORTH': 'JJ'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                    [{'ORTH': 'RBR'}, {'ORTH': 'JJ'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}])
        self.matcher.add(2,
                    None,
                    [{'ORTH': 'CV'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                    [{'ORTH': 'CV'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}])
        self.matcher.add(3,
                    None,
                    [{'ORTH': 'CV'}, {'ORTH': 'VBG'}, {'ORTH': 'TECH'}])
        self.matcher.add(4,
                    None,
                    [{'ORTH': 'CV'}, {'ORTH': 'TECH'}])
        self.matcher.add(5,
                    None,
                    [{'ORTH': 'VB'}, {'ORTH': 'VBN'}, {'ORTH': 'TECH'}],
                    [{'ORTH': 'VB'}, {'ORTH': 'VBN'}, {}, {'ORTH': 'TECH'}])
        # self.matcher.add(6,
        #             None,
        #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'JJS'}],
        #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'JJS'}],
        #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJS'}],
        #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJS'}])
        self.matcher.add(10,
                    None,
                    [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'RBR'}],
                    [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'RBR'}],
                    [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBR'}],
                    [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBR'}])
        self.matcher.add(7,
                    None,
                    [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'JJR'}],
                    [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'JJR'}],
                    [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJR'}],
                    [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJR'}])
        # self.matcher.add(9,
        #             None,
        #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
        #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
        #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}],
        #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}])

        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='yfwrshgrm',
                                     db='stackoverflow')
        self.cursor = self.connection.cursor()

    def add_pos_tag(self, words, table, tech_pair):
        tagged_words = nltk.pos_tag(words)
        # print tagged_words
        tag_list = []
        for (word, tag) in tagged_words:
            if tag == "IN" and word in self.cin:
                tag_list.append("CIN")
            elif tag[:2] == "VB" and word in self.cv:
                tag_list.append("CV")
            # else:
            #     self.cursor.execute("SELECT * FROM {} WHERE TagName = \'{}\'".format(table, word))
            #     if self.cursor.rowcount == 0:
            #         tag_list.append(tag)
            #     else:
            #         tag_list.append("TECH")
            elif word in tech_pair.split("\t"):
                tag_list.append("TECH")
            else:
                tag_list.append(tag)
        return tag_list

    def match_pattern(self, words, current_id, tech_pair, table):
        tag_list = self.add_pos_tag(words, table, tech_pair)
        patterns = self.matcher(self.nlp(u'{}'.format(" ".join(tag_list))))
        if patterns != []:
            self.compa_sent_count += 1
            out_file = open(os.path.join(os.pardir, "out", "tech_v3", "sentences.txt"), "a")
            out_file.write(" ".join(words))
            out_file.write("\n")
            out_file.close()
            data_file = open(os.path.join(os.pardir, "out", "tech_v3", "output.txt"), "a")
            data_file.write("{}\n".format(current_id))
            data_file.write("{}\nPattern(s): ".format(tech_pair))
            for pattern in patterns:
                self.count[str(pattern[0])] += 1
                data_file.write(str(pattern[0])+"\t")
                # data_file = open(os.path.join(os.pardir, "out", "tech_v2", "{}.txt".format(pattern[0])), "a")
            data_file.write("\n")
            data_file.write(" ".join(words))
            data_file.write("\n\n\n")
            data_file.close()

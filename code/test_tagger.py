"""
This stript is used to test POS Tagger and Dependency Parser of CoreNLP.
"""

from nltk import pos_tag
from nltk.tag.stanford import CoreNLPPOSTagger
from nltk.parse.corenlp import CoreNLPDependencyParser
import spacy
from spacy.matcher import Matcher


# dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
#
# while True:
#     parse, = dep_parser.raw_parse(input(">>>"))
#
#     for governor, dep, dependent in parse.triples():
#         print(governor, dep, dependent)

# line = input(">>>")
# print(line.split(" "))
# for (word, tag) in CoreNLPPOSTagger(url='http://localhost:9000').tag(line.split(" ")):
#     print(word)
#     print(tag)

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
       "under", "between", "after", "unlike", "with", "by", "opposite", "to"}
pos_tag_set = {"JJR", "RBR", "JJ"}

def add_patterns(matcher):
    matcher.add(0,
                None,
                [{'ORTH': 'JJR'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                [{'ORTH': 'JJR'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                [{'ORTH': 'JJR'}, {'ORTH': 'CIN'}, {}, {'ORTH': 'TECH'}],
                [{'ORTH': 'JJR'}, {}, {'ORTH': 'CIN'}, {}, {'ORTH': 'TECH'}])
    # matcher.add(1,
    #             None,
    #             [{'ORTH': 'RB'}, {'ORTH': 'JJ'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
    #             [{'ORTH': 'RB'}, {'ORTH': 'JJ'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}])
    matcher.add(8,
                None,
                [{'ORTH': 'RBR'}, {'ORTH': 'JJ'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                [{'ORTH': 'RBR'}, {'ORTH': 'JJ'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}])
    matcher.add(2,
                None,
                [{'ORTH': 'CV'}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}],
                [{'ORTH': 'CV'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'TECH'}])
    matcher.add(3,
                None,
                [{'ORTH': 'CV'}, {'ORTH': 'VBG'}, {'ORTH': 'TECH'}])
    matcher.add(4,
                None,
                [{'ORTH': 'CV'}, {'ORTH': 'TECH'}])
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
    matcher.add(10,
                None,
                [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'RBR'}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'RBR'}],
                [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBR'}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBR'}])
    matcher.add(7,
                None,
                [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'JJR'}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'JJR'}],
                [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJR'}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJR'}])

nlp = spacy.load('en')
matcher = Matcher(nlp.vocab)
add_patterns(matcher)

tech_pair = ["sortedlist", "sorteddictionary"]
tags = []
line = input(">>>")
while(line != "/"):
    flag = False
    tag_list = []
    words = line.split()
    tagged_words = CoreNLPPOSTagger(url='http://localhost:9000').tag(words)
    if len(words) != len(tagged_words):
        tagged_words = pos_tag(words)
    for (word, tag) in tagged_words:
    # for (word, tag) in CoreNLPPOSTagger(url='http://localhost:9000').tag(line.split()):
        if flag:
            word = "." + word
            flag = False
        if tag == "IN" and word in cin:
            tag_list.append("CIN")
        elif word in cv:
            tag_list.append("CV")
        elif word in tech_pair:
            tag_list.append("TECH")
        elif word == ".":
            flag = True
            continue
        else:
            tag_list.append(tag)
        words.append(word)

    for i in range(len(tag_list)):
        print(words[i]+": "+tag_list[i])
    line = input(">>>")
# for i in range(len(words)):
#     print(words[i]+": "+tag_list[i]+"\t"+tags[i])
# print(len(tag_list))
# print(len(line.split()))

# for i in range(len(line.split())):
#     print(line.split()[i]+": "+tag_list[i])
# if patterns != []:
#     for (pattern, start, end) in patterns:
#         words = line.split()
#         print("start: "+str(words[start])+" end: "+str(words[end-1]))
#         out_list = []
#         for i in range(len(words)):
#             if tag_list[i] == "TECH":
#                 out_list.append(words[i])
#             if i in range(start, end):
#                 if tag_list[i] in pos_tag_set:
#                     out_list.append(words[i])
# print(out_list)

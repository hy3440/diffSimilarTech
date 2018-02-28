import datetime
import io
from multiprocessing import Process
from nltk import pos_tag
from nltk.tag.stanford import CoreNLPPOSTagger
import os.path
import spacy
from spacy.matcher import Matcher


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

pattern_set = {0, 8, 7, 10}
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
    # matcher.add(9,
    #             None,
    #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
    #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
    #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}],
    #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}])


def classify(no):
    num = 0
    compa_sent_count = 0
    current_id = 0
    try:
        nlp = spacy.load('en')
        matcher = Matcher(nlp.vocab)
        add_patterns(matcher)
        with open(os.path.join(os.pardir, "out", "tech_v6", "{}.txt".format(no))) as data_file:
            compa_sent_count = 0
            for line in data_file:
                if num % 4 == 0:
                    current_id = line
                elif num % 4 == 1:
                    tech_pair = line.split("\t")
                    tech_pair[-1] = tech_pair[-1].strip()
                elif num % 4 == 2:
                    tag_list = []
                    words = []
                    flag = False
                    for (word, tag) in CoreNLPPOSTagger(url='http://localhost:9000').tag(line.split(" ")):
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
                    pos_tag = " ".join(tag_list)
                    patterns = matcher(nlp(pos_tag))
                    if patterns != []:
                        compa_sent_count += 1
                        data_file = open(os.path.join(os.pardir, "out", "tech_v6", "sentences_.txt"), "a")
                        data_file.write("{}".format(current_id))
                        data_file.write("{}\n".format("\t".join(tech_pair)))
                        for (pattern, start, end) in patterns:
                            data_file.write("pattern"+str(pattern)+"\t")
                            out_list = []
                            if pattern in pattern_set:
                                for i in range(len(words)):
                                    if tag_list[i] == "TECH":
                                        out_list.append(words[i])
                                    if i in range(start, end):
                                        if tag_list[i] in pos_tag_set:
                                            out_list.append(words[i])
                            data_file.write(" ".join(out_list))
                            data_file.write("\n")
                        data_file.write(str("{}\n".format(line)))
                        data_file.close()
                num += 1
    finally:
        print("Proc {}: {}/{} from - to {}".format(os.getpid(), compa_sent_count, num/4, current_id))

print(datetime.datetime.now())

for i in range(1, 9):
    classify(i)
# datalist = [0, 1, 2, 3, 4, 5, 6, 7]
# procs = []
# for i in range(8):
#     proc = Process(target=classify, args=(datalist[i],))
#     procs.append(proc)
#     proc.start()
#
# for proc in procs:
#     proc.join()

print(datetime.datetime.now())

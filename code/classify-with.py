import datetime
import io
from multiprocessing import Process
from nltk import pos_tag
from nltk.tag.stanford import CoreNLPPOSTagger
import os.path
import pickle
import spacy
from spacy.matcher import Matcher

total_compa = 0
total_sent = 0
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
pos_tag_set = {"JJR", "RBR", "JJ", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS", "JJS"}
tag_set = {"CIN", "CV", "VB", "VBZ", "VBD", "VBG", "VBN", "VBP"}
recordings = {}

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
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBR'}],
                [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'RBR'}, {}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'RBR'}, {}],
                [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBR'}, {}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBR'}, {}])
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
                    current_id = line.strip()
                elif num % 4 == 1:
                    techs = line.split("\t")
                    techs[-1] = techs[-1].strip()
                elif num % 4 == 2:
                    tag_list = []
                    flag = False
                    words = line.split()
                    tagged_words = CoreNLPPOSTagger(url='http://localhost:9000').tag(words)
                    if len(words) != len(tagged_words):
                        tagged_words = pos_tag(words)
                    words = []
                    for (word, tag) in tagged_words:
                        if flag:
                            word = "." + word
                            flag = False
                        if tag == "IN" and word in cin:
                            tag_list.append("CIN")
                        elif word in cv:
                            tag_list.append("CV")
                        elif word in techs:
                            tag_list.append("TECH")
                        elif word == ".":
                            flag = True
                            continue
                        else:
                            tag_list.append(tag)
                        words.append(word)
                    pos = " ".join(tag_list)
                    patterns = matcher(nlp(pos))
                    if patterns != []:
                        compa_sent_count += 1
                        data_file = open(os.path.join(os.pardir, "out", "tech_v6", "sentences.txt"), "a")
                        data_file.write("{}\n".format(current_id))
                        data_file.write("{}\n".format("\t".join(techs)))
                        tech_pair = []
                        for i in range(int(len(techs) / 2)):
                            tech_pair.append((techs[i], techs[i+1]))
                        for (pattern, start, end) in patterns:
                            data_file.write("pattern"+str(pattern)+"\t")
                            out_list = []
                            if pattern in pattern_set:
                                techa = ""
                                techb = ""
                                for i in range(len(words)):
                                    if tag_list[i] == "TECH":
                                        if techa == "":
                                            techa = words[i]
                                        elif out_list == []:
                                            techa = words[i]
                                        else:
                                            techb = words[i]
                                            if (techa, techb) in tech_pair or (techb, techa) in tech_pair:
                                                data_file.write(" ".join(out_list))
                                                data_file.write("\t")
                                                if (techa, techb) in recordings:
                                                    recordings[(techa, techb)].add("{} {} {} {}".format(current_id, techa, " ".join(out_list), techb))
                                                elif (techb, techa) in recordings:
                                                    recordings[(techb, techa)].add("{} {} {} {}".format(current_id, techa, " ".join(out_list), techb))
                                                else:
                                                    recordings[(techa, techb)] = set()
                                                    recordings[(techa, techb)].add("{} {} {} {}".format(current_id, techa, " ".join(out_list), techb))
                                            techa = ""
                                            techb = ""
                                            out_list = []
                                    if i in range(start, end):
                                        if tag_list[i] in pos_tag_set and techa != "":
                                            out_list.append(words[i])
                        data_file.write(str("\n{}\n".format(line)))
                        data_file.close()
                num += 1
    finally:
        print("Proc {}: {}/{} from - to {}".format(os.getpid(), compa_sent_count, num/4, current_id))
        return(compa_sent_count, num/4)

print(datetime.datetime.now())

try:
    for i in range(1, 83):
        (c, t) = classify(i)
        total_compa += c
        total_sent += t
    for i in range(100, 106):
        (c, t) = classify(i)
        total_compa += c
        total_sent += t
# datalist = [1, 2, 3, 4, 5, 6, 7, 8]
# procs = []
# for i in range(8):
#     proc = Process(target=classify, args=(datalist[i],))
#     procs.append(proc)
#     proc.start()
# for proc in procs:
#     proc.join()
finally:
    with open(os.path.join(os.pardir, "out", "tech_v6", "recordings.txt"), "a") as recordings_file:
        recordings_file.write(str(len(recordings))+"\n\n")
        for key, values in recordings.items():
            recordings_file.write(key[0]+"\t"+key[1]+"\t"+str(len(values))+"\n")
            for value in values:
                recordings_file.write(value+"\n")
            recordings_file.write("\n")
    print("{} / {}".format(total_compa, total_sent))
    with open(os.path.join(os.pardir, "data", "recordings.pkl"), 'wb') as output_file:
        pickle.dump(recordings, output_file)
    print(datetime.datetime.now())

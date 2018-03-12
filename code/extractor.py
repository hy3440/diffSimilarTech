"""
This script extracts comparative sentences based on different patterns and
extracts topic.
"""

import datetime
import io
from multiprocessing import Process
from nltk import pos_tag
from nltk.tag.stanford import CoreNLPPOSTagger
import operator
import os.path
import pickle
import spacy
from spacy.matcher import Matcher

total_compa = 0
total_sent = 0
total_pattern234 = 0

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

pattern_set = {0, 8, 7, 10}
pos_tag_set = {"JJR", "JJS", "JJ", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS"}
tag_set = {"CIN", "CV", "VB", "VBZ", "VBD", "VBG", "VBN", "VBP"}
recordings = {}
# ignore_set = {"more", "less"}

jjr = {}
jj = {}
nn = {}
rbr = {}
other = {}


def add_patterns(matcher):
    """ Add custom patterns to mathcer.

        (Matcher) -> None
    """
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
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJR'}]
                [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'JJR'}, {}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'JJR'}, {}],
                [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJR'}, {}],
                [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJR'}, {}])
    # matcher.add(9,
    #             None,
    #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
    #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
    #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}],
    #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}])


# Topic keywords
memory = {'memory', 'space', 'size', 'disk', 'lighter', 'lightweight',
          'light-weight', 'heavy', 'heavyweight', 'heavy-weight', 'smaller',
          'larger', 'bigger', 'huger'}
usability = {'experience', 'option', 'options', 'function', 'functionality',
             'support', 'access', 'development', 'framework', 'approach',
             'range', 'control', 'feature', 'features', 'application',
             'applications', 'structure', 'constraints', 'usage', 'flexibility',
             'capabilities', 'usability', 'implementation', 'control', 'mode',
             'complexity', 'easier', 'useful', 'functional', 'compact',
             'complicated', 'complex', 'simplicity', 'simpler', 'powerful',
             'flexible', 'concise', 'elegant', 'comfortable', 'readable',
             'compatible', 'incompatible', 'user-friendly', 'extensible',
             'capable', 'available', 'popular', 'convenient', 'portable'}
performance = {'overhead', 'quality', 'runtime', 'speed', 'time', 'performance',
               'efficient', ' quicker', 'slower', 'faster', 'consistent'
               'effective', 'inefficient', 'accurate'}
security = {'security', 'safer', 'securer', 'private'}
reliability = {'error', 'errors', 'lifetime', 'reliable', 'robust', 'stable'}


def add_dict(dictionary, word):
    """ Record word.

        (dict, str) -> None
    """
    if word in dictionary:
        dictionary[word] += 1
    else:
        dictionary[word] = 0


def extract_topic(out_list):
    """ Extract topic from the sentence.

        ([str]) -> str
    """
    # if len(out_list) == 1 and out_list[0] in ignore_set:
    #     return None
    # else:
    if True:
        for (w, t) in out_list:
            if t[:2] == "NN":
                add_dict(nn, w)
            elif t == "jjr":
                add_dict(jjr, w)
            elif t == "jj":
                add_dict(jj, w)
            elif t == "rbr":
                add_dict(rbr, w)
            else:
                add_dict(other, w)

            if w in memory:
                return "memory"
            elif w in usability:
                return "usability"
            elif w in performance:
                return "performance"
            elif w in security:
                return "security"
            elif w in reliability:
                return "reliability"
        return ""


def get_pos_tag(techs, words):
    """ Get POS tag of words.

        ([str], [str]) -> ([str], [str])
    """
    tag_list = []
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
    return (words, tag_list)


def extract_pattern08710(current_id, techs, pattern, words, line, start, end, tag_list):
    """ Extract topics for pattern 08710.

        (int, [str], int, [str], str, int, int, [str]) -> None
    """
    data_file = open(os.path.join(os.pardir, "relation", "sentences.txt"), "a")
    data_file.write("{}\n".format(current_id))
    data_file.write("{}\n".format("\t".join(techs)))
    tech_pair = []
    for i in range(0, len(techs), 2):
        tech_pair.append((techs[i], techs[i+1]))
    data_file.write("pattern"+str(pattern)+"\t")
    out_list = []
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
                    topic = extract_topic(out_list)
                    if topic is not None:
                        data_file.write(" ".join(out_list))
                        data_file.write("\t")
                        if (techa, techb) in recordings:
                            recordings[(techa, techb)].add((techa, " ".join(out_list), techb, topic, current_id, line))
                        elif (techb, techa) in recordings:
                            recordings[(techb, techa)].add((techa, " ".join(out_list), techb, topic, current_id, line))
                        else:
                            recordings[(techa, techb)] = set()
                            recordings[(techa, techb)].add((techa, " ".join(out_list), techb, topic, current_id, line))
                techa = ""
                techb = ""
                out_list = []
        if i in range(start, end):
            if tag_list[i] in pos_tag_set and techa != "":
                out_list.append((words[i], tag_list[i]))
    data_file.write(str("\n{}\n".format(line)))
    data_file.close()


def extract(no):
    """ Extract comparative sentences and topics.

        (int) -> (int, int)
    """
    num = 0
    compa_sent_count = 0
    current_id = 0
    pattern234 = 0
    try:
        nlp = spacy.load('en')
        matcher = Matcher(nlp.vocab)
        add_patterns(matcher)
        with open(os.path.join(os.pardir, "out", "tech", "{}.txt".format(no))) as data_file:
            compa_sent_count = 0
            for line in data_file:
                if num % 4 == 0:
                    current_id = line.strip()
                elif num % 4 == 1:
                    techs = line.split("\t")
                    techs[-1] = techs[-1].strip()
                elif num % 4 == 2:
                    (words, tag_list) = get_pos_tag(techs, line.split())
                    patterns = matcher(nlp(" ".join(tag_list)))
                    if patterns != []:
                        compa_sent_count += 1
                        for (pattern, start, end) in patterns:
                            if pattern in pattern_set:
                                extract_pattern08710(current_id, techs, pattern, words, line, start, end, tag_list)
                            else:
                                pattern234 += 1
                                data_file = open(os.path.join(os.pardir, "relation", "pattern234.txt"), "a")
                                data_file.write("{}\n".format(current_id))
                                data_file.write("{}\n".format("\t".join(techs)))
                                data_file.write("pattern"+str(pattern)+"\t")
                                data_file.write(str("\n{}\n".format(line)))
                                data_file.close()
                num += 1
    finally:
        print("{}/{} from - to {}\n".format(compa_sent_count, num/4, current_id))
        return(compa_sent_count, num/4, pattern234)

print(datetime.datetime.now())

try:
    for i in range(1, 30):
        (c, t, p) = extract(i)
        total_compa += c
        total_sent += t
        total_pattern234 += p
    # for i in range(100, 106):
    #     (c, t) = classify(i)
    #     total_compa += c
    #     total_sent += t
# datalist = [1, 2, 3, 4, 5, 6, 7, 8]
# procs = []
# for i in range(8):
#     proc = Process(target=classify, args=(datalist[i],))
#     procs.append(proc)
#     proc.start()
# for proc in procs:
#     proc.join()
finally:
    with open(os.path.join(os.pardir, "relation", "relations.txt"), "a") as recordings_file:
        recordings_file.write(str(len(recordings))+"\n\n")
        for key, values in recordings.items():
            recordings_file.write(key[0]+"\t"+key[1]+"\t"+str(len(values))+"\n")
            for value in values:
                # recordings_file.write(" ".join(value)+"\n")
                recordings_file.write(str(value)+'\n')
            recordings_file.write("\n")
    print("{} / {}".format(total_compa, total_sent))
    print("{} pattern234\n")

    with open(os.path.join(os.pardir, "relation", "relations.pkl"), 'wb') as output_file:
        pickle.dump(recordings, output_file)

    sorted_jjr = sorted(jjr.items(), key=operator.itemgetter(1), reverse=True)
    sorted_jj = sorted(jj.items(), key=operator.itemgetter(1), reverse=True)
    sorted_nn = sorted(nn.items(), key=operator.itemgetter(1), reverse=True)
    sorted_rbr = sorted(rbr.items(), key=operator.itemgetter(1), reverse=True)
    sorted_other = sorted(other.items(), key=operator.itemgetter(1), reverse=True)

    with open(os.path.join(os.path.pardir, "relation", "jjr.txt"), "a") as out_file:
        for word, frequency in sorted_jjr:
            out_file.write("{:<20}{}\n".format(word, frequency))

    with open(os.path.join(os.path.pardir, "relation", "jj.txt"), "a") as out_file1:
        for word, frequency in sorted_jj:
            out_file1.write("{:<20}{}\n".format(word, frequency))

    with open(os.path.join(os.path.pardir, "relation", "nn.txt"), "a") as out_file2:
        for word, frequency in sorted_nn:
            out_file2.write("{:<20}{}\n".format(word, frequency))

    with open(os.path.join(os.path.pardir, "relation", "rbr.txt"), "a") as out_file3:
        for word, frequency in sorted_rbr:
            out_file3.write("{:<20}{}\n".format(word, frequency))

    with open(os.path.join(os.path.pardir, "relation", "other.txt"), "a") as out_file4:
        for word, frequency in sorted_other:
            out_file4.write("{:<20}{}\n".format(word, frequency))

    print(datetime.datetime.now())

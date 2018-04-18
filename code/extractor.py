"""
This script extracts comparative sentences based on different patterns and
extracts topic.
"""

import datetime
# import io
# from multiprocessing import Process
from nltk import pos_tag
from nltk.tag.stanford import CoreNLPPOSTagger
# import operator
import os
import pickle
import spacy
from spacy.matcher import Matcher


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

pattern_set = {1, 2, 3, 4}
# pos_tag_set = {"JJR", "JJS", "JJ", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS"}
# tag_set = {"CIN", "CV", "VB", "VBZ", "VBD", "VBG", "VBN", "VBP"}
pairs = {}
pattern1234_pairs = {}
pattern567_pairs = {}
sent_recordings = {}  # record all sentences and corresponding database and post id
pattern1234_recordings = {}  # record pattern1234 sentences and corresponding database and post id
pattern567_recordings = {}  # record pattern567 sentences and corresponding database and post id
count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, "compa": 0, "total": 0}
current_id = 0
i = 0
# ignore_set = {"more", "less"}

# jjr = {}
# jj = {}
# nn = {}
# rbr = {}
# other = {}


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
                [{'ORTH': 'CV'}, {'ORTH': 'VBG'}, {'ORTH': 'TECH'}])
    matcher.add(7,
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
    # matcher.add(9,
    #             None,
    #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
    #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
    #             [{'ORTH': 'TECH'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}],
    #             [{'ORTH': 'TECH'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}])


# # Topic keywords
# memory = {'memory', 'space', 'size', 'disk', 'lighter', 'lightweight',
#           'light-weight', 'heavy', 'heavyweight', 'heavy-weight', 'smaller',
#           'larger', 'bigger', 'huger'}
# usability = {'experience', 'option', 'options', 'function', 'functionality',
#              'support', 'access', 'development', 'framework', 'approach',
#              'range', 'control', 'feature', 'features', 'application',
#              'applications', 'structure', 'constraints', 'usage', 'flexibility',
#              'capabilities', 'usability', 'implementation', 'control', 'mode',
#              'complexity', 'easier', 'useful', 'functional', 'compact',
#              'complicated', 'complex', 'simplicity', 'simpler', 'powerful',
#              'flexible', 'concise', 'elegant', 'comfortable', 'readable',
#              'compatible', 'incompatible', 'user-friendly', 'extensible',
#              'capable', 'available', 'popular', 'convenient', 'portable'}
# performance = {'overhead', 'quality', 'runtime', 'speed', 'time', 'performance',
#                'efficient', ' quicker', 'slower', 'faster', 'consistent'
#                'effective', 'inefficient', 'accurate'}
# security = {'security', 'safer', 'securer', 'private'}
# reliability = {'error', 'errors', 'lifetime', 'reliable', 'robust', 'stable'}


# def add_dict(dictionary, word):
#     """ Record word.
#
#         (dict, str) -> None
#     """
#     if word in dictionary:
#         dictionary[word] += 1
#     else:
#         dictionary[word] = 1


# def extract_topic(out_list, tag_list):
#     """ Extract topic from the sentence.
#
#         ([str]) -> str
#     """
#     # if len(out_list) == 1 and out_list[0] in ignore_set:
#     #     return None
#     # else:
#     if True:
#         for i in range(len(out_list)):
#             w = out_list[i]
#             t = tag_list[i]
#             if t[:2] == "NN":
#                 add_dict(nn, w)
#             elif t == "JJR":
#                 add_dict(jjr, w)
#             elif t == "JJ":
#                 add_dict(jj, w)
#             elif t == "RBR":
#                 add_dict(rbr, w)
#             else:
#                 add_dict(other, w)
#
#             if w in memory:
#                 return "memory"
#             elif w in usability:
#                 return "usability"
#             elif w in performance:
#                 return "performance"
#             elif w in security:
#                 return "security"
#             elif w in reliability:
#                 return "reliability"
#         return ""


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
            tag = "VB"
        else:
            tags.append(tag)
        words.append(word)
    return (words, tags)


# def extract_pattern08710(current_id, techs, pattern, words, line, start, end, tags):
#     """ Extract topics for pattern 08710.
#
#         (int, [str], int, [str], str, int, int, [str]) -> None
#     """
#     pattern08710_file = open(os.path.join(os.pardir, "out", "sentences.txt"), "a")
#     pattern08710_file.write("{}\n".format(current_id))
#     pattern08710_file.write("{}\n".format("\t".join(techs)))
#     tech_pair = []
#     for i in range(0, len(techs), 2):
#         tech_pair.append((techs[i], techs[i+1]))
#     pattern08710_file.write("pattern"+str(pattern)+"\t")
#     out_list = []
#     tag_list = []
#     techa = ""
#     techb = ""
#     for i in range(len(words)):
#         if tags[i] == "TECH":
#             if techa == "":
#                 techa = words[i]
#             elif out_list == []:
#                 techa = words[i]
#             else:
#                 techb = words[i]
#                 if (techa, techb) in tech_pair or (techb, techa) in tech_pair:
#                     # topic = extract_topic(out_list, tag_list)
#                     if topic is not None:
#                         pattern08710_file.write(" ".join(out_list))
#                         pattern08710_file.write("\t")
#                         if (techa, techb) in recordings:
#                             recordings[(techa, techb)].add(line)
#                         elif (techb, techa) in recordings:
#                             recordings[(techb, techa)].add(line)
#                         else:
#                             recordings[(techa, techb)] = set()
#                             recordings[(techa, techb)].add((techa, " ".join(out_list), techb, topic, current_id, line))
#                         if line not in sent_recordings:
#                             sent_recordings[line] = (techa, " ".join(out_list), techb, topic, current_id, "stackoverflow")
#                 techa = ""
#                 techb = ""
#                 out_list = []
#                 tag_list = []
#         if i in range(start, end):
#             if tags[i] in pos_tag_set and techa != "":
#                 out_list.append(words[i])
#                 tag_list.append(tags[i])
#     pattern08710_file.write("\n{}\n".format(line))
#     pattern08710_file.close()


def write_sentences_file(fname, current_id, techs, pattern, line):
    with open(os.path.join(os.pardir, "out", fname), "a") as f:
        f.write("{}\n".format(current_id))
        f.write("{}\n".format("\t".join(techs)))
        f.write("pattern"+str(pattern)+"\t")
        f.write(str("\n{}\n".format(line)))


def add_to_dict(dictionary, techs, line):
    for i in range(0, len(techs), 2):
        if (techs[i], techs[i+1]) not in dictionary:
            dictionary[(techs[i], techs[i+1])] = set()
        dictionary[(techs[i], techs[i+1])].add(line)


def save_to_pkl(fname, data):
    with open(os.path.join(os.pardir, "out", fname), 'wb') as out_file:
        pickle.dump(data, out_file)


def extract(no, dbname):
    """ Extract comparative sentences and topics.

        (int, str) -> None
    """
    try:
        nlp = spacy.load('en')
        matcher = Matcher(nlp.vocab)
        add_patterns(matcher)
        num = 0
        with open(os.path.join(os.pardir, "out", dbname, "{}.txt".format(no))) as data_file:
            for line in data_file:
                if num % 4 == 0:
                    current_id = line.strip()
                elif num % 4 == 1:
                    techs = line.split("\t")
                    techs[-1] = techs[-1].strip()
                elif num % 4 == 2:
                    count["total"] += 1
                    (words, tags) = get_pos_tag(techs, line.split())
                    patterns = matcher(nlp(" ".join(tags)))
                    if patterns != []:
                        count["compa"] += 1
                        add_to_dict(pairs, techs, line)
                        for (pattern, start, end) in patterns:
                            count[pattern] += 1
                            if pattern in pattern_set:
                                add_to_dict(pattern1234_pairs, techs, line)
                                # extract_pattern08710(current_id, techs, pattern, words, line, start, end, tags)
                                write_sentences_file("pattern1234.txt", current_id, techs, pattern, line)
                                if line not in pattern1234_recordings:
                                    pattern1234_recordings[line] = (current_id, "stackoverflow")
                            else:
                                add_to_dict(pattern567_pairs, techs, line)
                                write_sentences_file("pattern567.txt", current_id, techs, pattern, line)
                                if line not in pattern567_recordings:
                                    pattern567_recordings[line] = (current_id, "stackoverflow")
                num += 1
    finally:
        print("{}/{} from - to {}".format(count["compa"], count["total"], current_id))

print(datetime.datetime.now())

try:
    dbname = "tech"
    for i in range(1, 83):
        extract(i, dbname)
    for i in range(100, 147):
        extract(i, dbname)
finally:
    print("current file: {}, current id: {}".format(i, current_id))
    for key, value in count.items():
        print("{}: {}".format(key, value))
    save_to_pkl("all_pairs.pkl", pairs)
    save_to_pkl("pattern1234_pairs.pkl", pattern1234_pairs)
    save_to_pkl("pattern567_pairs.pkl", pattern567_pairs)
    save_to_pkl("all_sentences.pkl", sent_recordings)
    save_to_pkl("pattern567_sents.pkl", pattern567_recordings)
    save_to_pkl("pattern1234_sents.pkl", pattern1234_recordings)
    save_to_pkl("count.pkl", count)
    with open(os.path.join(os.pardir, "out", "all_pairs.txt"), "a") as recordings_file:
        recordings_file.write(str(len(pairs))+"\n\n")
        for key, values in pairs.items():
            recordings_file.write(key[0]+"\t"+key[1]+"\t"+str(len(values))+"\n")
            for value in values:
                # recordings_file.write(" ".join(value)+"\n")
                recordings_file.write(str(value)+'\n')
            recordings_file.write("\n")


    # sorted_jjr = sorted(jjr.items(), key=operator.itemgetter(1), reverse=True)
    # sorted_jj = sorted(jj.items(), key=operator.itemgetter(1), reverse=True)
    # sorted_nn = sorted(nn.items(), key=operator.itemgetter(1), reverse=True)
    # sorted_rbr = sorted(rbr.items(), key=operator.itemgetter(1), reverse=True)
    # sorted_other = sorted(other.items(), key=operator.itemgetter(1), reverse=True)

    # with open(os.path.join(os.path.pardir, "out", "softwareen", "jjr.txt"), "a") as out_file:
    #     for word, frequency in sorted_jjr:
    #         out_file.write("{:<20}{}\n".format(word, frequency))
    #
    # with open(os.path.join(os.path.pardir, "out", "softwareen", "jj.txt"), "a") as out_file1:
    #     for word, frequency in sorted_jj:
    #         out_file1.write("{:<20}{}\n".format(word, frequency))
    #
    # with open(os.path.join(os.path.pardir, "out", "softwareen", "nn.txt"), "a") as out_file2:
    #     for word, frequency in sorted_nn:
    #         out_file2.write("{:<20}{}\n".format(word, frequency))
    #
    # with open(os.path.join(os.path.pardir, "out", "softwareen", "rbr.txt"), "a") as out_file3:
    #     for word, frequency in sorted_rbr:
    #         out_file3.write("{:<20}{}\n".format(word, frequency))
    #
    # with open(os.path.join(os.path.pardir, "out", "softwarerecs", "other.txt"), "a") as out_file4:
    #     for word, frequency in sorted_other:
    #         out_file4.write("{:<20}{}\n".format(word, frequency))

    print(datetime.datetime.now())

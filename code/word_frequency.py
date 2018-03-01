from nltk.corpus import stopwords
from nltk.tag.stanford import CoreNLPPOSTagger
import operator
import os
import pickle

synonyms_file = open(os.path.join(os.pardir, "data", "synonyms.pkl"), 'rb')
synonyms = pickle.load(synonyms_file)
synonyms_file.close()

wf = {}
jj = {}
nn = {}
rb = {}
stopwords_en = set(stopwords.words('english'))
modal_verbs = {"can", "could", "will", "would", "may", "might", "shall", "should", "must"}


def count(file_name):
    with open(os.path.join(os.path.pardir, "out", "tech_v6", file_name)) as data3_file:
        num = 0
        for line in data3_file:
            if num % 4 == 2:
                words = line.split(" ")
                words[-1] = words[-1].strip()
                for (word, tag) in CoreNLPPOSTagger(url='http://localhost:9000').tag(words):
                    if word not in stopwords_en and word not in modal_verbs and word not in synonyms:
                        if word in wf:
                            wf[word] += 1
                        else:
                            wf[word] = 1
                        if tag[:2] == "JJ":
                            if word in jj:
                                jj[word] += 1
                            else:
                                jj[word] = 1
                        elif tag[:2] == "NN":
                            if word in nn:
                                nn[word] += 1
                            else:
                                nn[word] = 1
                        elif tag[:2] == "RB":
                            if word in rb:
                                rb[word] += 1
                            else:
                                rb[word] = 1
            num += 1

count("sentences_.txt")

sorted_wf = sorted(wf.items(), key=operator.itemgetter(1), reverse=True)
sorted_jj = sorted(jj.items(), key=operator.itemgetter(1), reverse=True)
sorted_nn = sorted(nn.items(), key=operator.itemgetter(1), reverse=True)
sorted_rb = sorted(rb.items(), key=operator.itemgetter(1), reverse=True)

with open(os.path.join(os.path.pardir, "out", "tech_v6", "word_frequency_v5.txt"), "a") as out_file:
    for word, frequency in sorted_wf:
        out_file.write("{:<20}{}\n".format(word, frequency))

with open(os.path.join(os.path.pardir, "out", "tech_v6", "adjective.txt"), "a") as out_file1:
    for word, frequency in sorted_jj:
        out_file1.write("{:<20}{}\n".format(word, frequency))

with open(os.path.join(os.path.pardir, "out", "tech_v6", "noun.txt"), "a") as out_file2:
    for word, frequency in sorted_nn:
        out_file2.write("{:<20}{}\n".format(word, frequency))

with open(os.path.join(os.path.pardir, "out", "tech_v6", "adverb.txt"), "a") as out_file3:
    for word, frequency in sorted_rb:
        out_file3.write("{:<20}{}\n".format(word, frequency))

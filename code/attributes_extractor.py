from nltk.corpus import stopwords
from nltk.tag.stanford import CoreNLPPOSTagger
import operator
import os
import pickle

synonyms_file = open(os.path.join(os.pardir, "data", "synonyms_for_all_similar_techs.pkl"), 'rb')
synonyms = pickle.load(synonyms_file)
synonyms_file.close()

wf = {}
jj = {}
nn = {}
rb = {}
stopwords_en = set(stopwords.words('english'))
modal_verbs = {"can", "could", "will", "would", "may", "might", "shall", "should", "must"}
patterns = {"pattern0", "pattern8", "pattern7", "pattern10"}


def count(file_name):
    jj_file = open(os.path.join(os.path.pardir, "out", "pattern07810", "jj.txt"), "a")
    nn_file = open(os.path.join(os.path.pardir, "out", "pattern07810", "nn.txt"), "a")
    rb_file = open(os.path.join(os.path.pardir, "out", "pattern07810", "rb.txt"), "a")


    with open(os.path.join(os.path.pardir, "out", "tech_v5", file_name)) as data3_file:
        num = 0
        flag = False
        for line in data3_file:
            if num % 5 == 2:
                pattern_list = line.split("\t")
                for pattern in pattern_list:
                    if pattern.strip() in patterns:
                        flag = True
            elif num % 5 == 3 and flag:
                flag = False
                words = line.split(" ")
                words[-1] = words[-1].strip()
                for (word, tag) in CoreNLPPOSTagger(url='http://localhost:9000').tag(words):
                    if word not in stopwords_en and word not in modal_verbs and word not in synonyms:
                        if word in wf:
                            wf[word] += 1
                        else:
                            wf[word] = 1
                        if tag[:2] == "JJ":
                            jj_file.write(word+"\t")
                            if word in jj:
                                jj[word] += 1
                            else:
                                jj[word] = 1
                        elif tag[:2] == "NN":
                            nn_file.write(word+"\t")
                            if word in nn:
                                nn[word] += 1
                            else:
                                nn[word] = 1
                        elif tag[:2] == "RB":
                            rb_file.write(word+"\t")
                            if word in rb:
                                rb[word] += 1
                            else:
                                rb[word] = 1
                jj_file.write("\n")
                nn_file.write("\n")
                rb_file.write("\n")
            num += 1
    jj_file.close()
    nn_file.close()
    rb_file.close()
    

count("sentences_4.txt")
count("sentences_3.txt")

sorted_wf = sorted(wf.items(), key=operator.itemgetter(1), reverse=True)
sorted_jj = sorted(jj.items(), key=operator.itemgetter(1), reverse=True)
sorted_nn = sorted(nn.items(), key=operator.itemgetter(1), reverse=True)
sorted_rb = sorted(rb.items(), key=operator.itemgetter(1), reverse=True)

with open(os.path.join(os.path.pardir, "out", "pattern07810", "word_frequency_v5.txt"), "a") as out_file:
    for word, frequency in sorted_wf:
        out_file.write("{:<20}{}\n".format(word, frequency))

with open(os.path.join(os.path.pardir, "out", "pattern07810", "adjective.txt"), "a") as out_file1:
    for word, frequency in sorted_jj:
        out_file1.write("{:<20}{}\n".format(word, frequency))

with open(os.path.join(os.path.pardir, "out", "pattern07810", "noun.txt"), "a") as out_file2:
    for word, frequency in sorted_nn:
        out_file2.write("{:<20}{}\n".format(word, frequency))

with open(os.path.join(os.path.pardir, "out", "pattern07810", "adverb.txt"), "a") as out_file3:
    for word, frequency in sorted_rb:
        out_file3.write("{:<20}{}\n".format(word, frequency))

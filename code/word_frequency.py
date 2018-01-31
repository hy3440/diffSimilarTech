from nltk.corpus import stopwords
import operator
import os
import pickle

synonyms_file = open(os.path.join(os.pardir, "data", "synonyms.pkl"), 'rb')
synonyms = pickle.load(synonyms_file)
synonyms_file.close()

wf = {}
stopwords_en = set(stopwords.words('english'))
modal_verbs = {"can", "could", "will", "would", "may", "might", "shall", "should", "must"}

with open(os.path.join(os.path.pardir, "out", "tech_v2", "sentences.txt")) as data_file:
    for line in data_file:
        words = line.split(" ")
        words[-1] = words[-1].strip()
        for word in words:
            if word not in stopwords_en and word not in modal_verbs and word not in synonyms:
                if word in wf:
                    wf[word] += 1
                else:
                    wf[word] = 1

sorted_wf = sorted(wf.iteritems(), key=operator.itemgetter(1), reverse=True)

with open(os.path.join(os.path.pardir, "out", "tech_v2", "word_frequency.txt"), "a") as out_file:
    for word, frequency in sorted_wf:
        out_file.write("{:<20}{}\n".format(word, frequency))

"""
gensim LDA model.
"""

import gensim
from nltk.corpus import stopwords
import os
import pickle

synonyms_file = open(os.path.join(os.pardir, "data", "synonyms.pkl"), 'rb')
synonyms = pickle.load(synonyms_file)
synonyms_file.close()

stopwords_en = set(stopwords.words('english'))

modal_verbs = {"can", "could", "will", "would", "may", "might", "shall", "should", "must"}

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

for verb in modal_verbs:
    stopwords_en.add(verb)

for tech in synonyms.keys():
    stopwords_en.add(tech)

for c in cv:
    stopwords_en.add(c)

for c in cin:
    stopwords_en.add(c)

with open(os.path.join(os.path.pardir, "out", "tech_v2", "sentences.txt")) as data2_file:
    texts = [[word for word in line.split() if word not in stopwords_en] for line in data2_file]

with open(os.path.join(os.path.pardir, "out", "tech_v3", "sentences.txt")) as data3_file:
    for line in data3_file:
        line_list = []
        for word in line.split():
            if word not in stopwords_en:
                line_list.append(word)
        texts.append(line_list)

dictionary = gensim.corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, update_every=1, chunksize=10000, passes=1)

for no, out in lda.print_topics(10):
    print "Topic {}: {}\n".format(no, out)

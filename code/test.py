# import nltk
import os
import pickle
from prepros import *
# from prepros import add_patterns, get_cv_and_cin, get_words
# import pymysql.cursors
# import spacy
# from spacy.matcher import Matcher
# import webbrowser

# nlp = spacy.load('en')
# matcher = Matcher(nlp.vocab)
# adds_patterns(matcher)
# pos_tag = "CV VBG APP CV APP"
# pattern = matcher(nlp(u'{}'.format(pos_tag)))
# print pattern




# # Insert pairs.txt into mysql
# cursor = connection.cursor()
# count = 1
# with open(os.path.join(os.pardir, "Data", "cateInGroups_freq100_v2.txt")) as data_file:
#     for line in data_file:
#         tech_list = line.split("\t")
#         first = tech_list[0]
#         second = tech_list[1]
#         sql = "INSERT INTO pairs(Id, First, Second) VALUES ('%d', '%s', '%s')" % (count, first, second)
#         cursor.execute(sql)
#         connection.commit()
#         count += 1
# connection.close()

# from gensim.test.utils import common_texts
# from gensim.corpora import Dictionary
# from gensim.models import Word2Vec
# from gensim.similarities import WmdSimilarity
#
#
# model = Word2Vec(common_texts, size=20, min_count=1)  # train word-vectors
# dictionary = Dictionary(common_texts)
# bow_corpus = [dictionary.doc2bow(document) for document in common_texts]
#
# print((common_texts))
# index = WmdSimilarity(bow_corpus, model)
# # Make query.
# query = 'trees'
# sims = index[query]


# in_path = os.path.join(os.pardir, "data", "relations.pkl")
# relations_file = open(in_path, 'rb')
# relations = pickle.load(relations_file)
# out_path = os.path.join(os.pardir, "keywords.txt")
# with open(out_path, "a") as out_file:
#     for key, values in relations.items():
#         for value in values:
#             #if value[3] != "":
#             if True:
#                 out_file.write(value[1]+"\n")
#                 out_file.write(value[5])
#                 out_file.write("\n")
a = 1
with open(os.path.join(os.pardir, "a.pkl"), "wb") as f:
    pickle.dump(a, f)

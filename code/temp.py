# from multiprocessing import Pool
# from multiprocessing.dummy import Pool as ThreadPool
from nltk.tag.stanford import CoreNLPPOSTagger
# import os
# import pickle
# from prepros import add_patterns, get_cv_and_cin, get_words
# import pymysql.cursors
# import spacy
# from spacy import displacy

# tech = {"python", "java"}
# nlp = spacy.load('en')
# doc = nlp("python is slower than java")
# displacy.serve(doc, style='dep')
tech_pair = [".net"]
lines = ["i want to test .net", "asp.net-mvc is more useful than .net", "i will use node.js"]
for line in lines:
    flag = False
    tag_list = []
    for (word, tag) in CoreNLPPOSTagger(url='http://localhost:9000').tag(line.split(" ")):
        if flag:
            word = "." + word
            flag = False
        if word in tech_pair:
            tag_list.append("TECH")
        elif word == ".":
            flag = True
        else:
            tag_list.append(tag)
    pos_tag = " ".join(tag_list)
    print(pos_tag)

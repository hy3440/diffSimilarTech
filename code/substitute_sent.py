import os
import pandas as pd
from pandas import ExcelFile
from pandas import ExcelWriter
import pickle
import random


def substitute():
    in_path = os.path.join(os.pardir, "aspects", "aspects.pkl")
    aspects = pickle.load(open(in_path, 'rb'))

    techas = []
    relations = []
    techbs = []
    topics = []
    ids = []
    sents = []
    sentences = []
    for values in aspects.values():
        for techa, relation, techb, topic, id, sent in values:
            techas.append(techa)
            relations.append(relation)
            techbs.append(techb)
            topics.append(topic)
            ids.append(id)
            sents.append(sent)
            sentence = sent.replace(techa, "a")
            sentence = sentence.replace(techb, "b")
            sentences.append(sentence)

    df = pd.DataFrame({'TECHA': techas,
                       'RELATION': relations,
                       'TECHB': techbs,
                       'TOPIC': topics,
                       'ID': ids,
                       'ORIGINAL': sents,
                       'SENTENCE': sentences})
    out_path = os.path.join(os.pardir, "aspects", "samples.xlsx")
    writer = ExcelWriter(out_path)
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()


def random_choice():
    indices = random.sample(range(7162), 1000)
    i = 0
    in_path = os.path.join(os.pardir, "aspects", "aspects.pkl")
    aspects = pickle.load(open(in_path, 'rb'))

    techas = []
    relations = []
    techbs = []
    topics = []
    ids = []
    sents = []
    sentences = []
    for values in aspects.values():
        for techa, relation, techb, topic, id, sent in values:
            if i in indices:
                techas.append(techa)
                relations.append(relation)
                techbs.append(techb)
                topics.append(topic)
                ids.append(id)
                sents.append(sent)
                sentence = sent.replace(techa, "a")
                sentence = sentence.replace(techb, "b")
                sentences.append(sentence)
            i += 1
            print(i)
            print(i in indices)

    df = pd.DataFrame({'TECHA': techas,
                       'RELATION': relations,
                       'TECHB': techbs,
                       'TOPIC': topics,
                       'ID': ids,
                       'ORIGINAL': sents,
                       'SENTENCE': sentences})
    out_path = os.path.join(os.pardir, "aspects", "samples.xlsx")
    writer = ExcelWriter(out_path)
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()

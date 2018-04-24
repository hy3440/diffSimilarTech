import os, pickle
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

pattern = 6
def import_to_excel(pattern):
    pair = []
    flag = []
    sentence = []
    temp = False
    with open(os.path.join(os.pardir, "sentence_sample", "pattern{}_samples.txt".format(pattern))) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            elif line == "yes" or line == "no":
                flag.append(line)
                temp = True
            elif temp:
                temp = False
                pair.append(line)
            else:
                print(line)
                sentence.append(line)
    print(len(pair))
    print(len(flag))
    print(len(sentence))
    df = pd.DataFrame({'Pair': pair,
                       'Y/N': flag,
                       'Sentence': sentence})
    out_path = os.path.join(os.pardir, "{}.xlsx".format(pattern))
    writer = ExcelWriter(out_path)
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()

def import_to_excel2(pattern):
    pair = []
    flag = []
    sentence = []
    with open(os.path.join(os.pardir, "sentence_sample", "pattern{}_samples.txt".format(pattern))) as f:
        n = 0
        for line in f:
            line = line.strip()
            if n % 4 == 0:
                flag.append(line)
            elif n % 4 == 1:
                pair.append(line)
            elif n % 4 == 2:
                sentence.append(line)
                print(line)
            n += 1

    print(len(pair))
    print(len(flag))
    print(len(sentence))
    df = pd.DataFrame({'Pair': pair,
                       'Y/N': flag,
                       'Sentence': sentence})
    out_path = os.path.join(os.pardir, "{}.xlsx".format(pattern))
    writer = ExcelWriter(out_path)
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()

import_to_excel(pattern)

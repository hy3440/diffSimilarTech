import os, pickle, random
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np


def save_to_pkl(fname, data):
    with open(os.path.join(os.pardir, "sentence_sample", fname), 'wb') as out_file:
        pickle.dump(data, out_file)


def contains_techs(techa, techb, sent):
    a = techa+" "+techb in sent
    b = techa+" and "+techb in sent
    c = techa+" or "+techb in sent
    d = techb+" "+techa in sent
    e = techb+" and "+techa in sent
    f = techb+" or "+techa in sent
    # print("b: ", b)
    # print("e: ", e)
    return a or b or c or d or e or f


def pros_file(f):
    num = 0
    with open(os.path.join(os.pardir, "out", f)) as data_file:
        for line in data_file:
            if num % 5 == 2:
                p = line.strip()
            elif num % 5 == 1:
                techs = line.strip().split()
            elif num % 5 == 3:
                if p != "pattern7":
                    sent = line.strip()
                    flag = True
                    for i in range(0, len(techs), 2):
                        if contains_techs(techs[i], techs[i+1], sent):
                            flag = False
                            break
                    if flag:
                        techs_of_sent[sent] = " ".join(techs)
                        patterns[p].add(sent)
                        all.add(sent)
            num += 1

# f = open(os.path.join(os.pardir, "out", "patterns.pkl"), 'rb')
# patterns = pickle.load(f)
# f.close()

def random_samples(p):
    print(p+": "+str(len(patterns[p])))

    sents = []
    for sentence in patterns[p]:
        check = techs_of_sent[sentence]
        if 'width' in check or 'height' in check or 'int' in check or 'char' in check:
            continue
        else:
            sents.append(sentence)
    r = random.sample(range(len(sents)), 70)
    print(len(set(r)))

    t = []
    s = []

    for i in range(70):
        # f.write(str(i)+"\n")
        t.append(techs_of_sent[sents[r[i]]])
        s.append(sents[r[i]])
    tt[p] = t
    ss[p] = s


techs_of_sent = {}
all = set()
patterns = {"pattern1": set(),
            "pattern2": set(),
            "pattern3": set(),
            "pattern4": set(),
            "pattern5": set(),
            "pattern6": set()
            }
tt = {}
ss = {}
pros_file("pattern1234.txt")
pros_file("pattern567.txt")
save_to_pkl("patterns.pkl", patterns)

out_path = os.path.join(os.pardir, "samples.xlsx")
writer = ExcelWriter(out_path)
for k in patterns.keys():
    random_samples(k)
    df = pd.DataFrame({'TECH': tt[k],
                       'Sentence': ss[k]})
    df.to_excel(writer, k, index=False)
writer.save()
print(len(all))
# techs = ["post", "get"]
# sent = "post and get"
# flag = True
# for i in range(0, len(techs), 2):
#     if contains_techs(techs[i], techs[i+1], sent):
#         print(sent)
#         flag = False
#         break
# print(flag)

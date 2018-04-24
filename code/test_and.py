import os, pickle
# import pandas as pd
# from pandas import ExcelWriter
# from pandas import ExcelFile
# import numpy as np


# f = open(os.path.join(os.pardir, "out", "pattern1234_sents.pkl"), "rb")
# sents = pickle.load(f)
# f.close()

all = set()

f = open(os.path.join(os.pardir, "out", "pattern1234_pairs.pkl"), "rb")
pairs = pickle.load(f)
f.close()

# new_pairs = {}
# for pair, sentences in pairs.items():
#     (techa, techb) = pair
#     for sent in sentences:
#         if techa+" "+techb in sent or techa+" and "+techb in sent or techa+" or "+techb in sent or techb+" "+techa in sent or techb+" and "+techa in sent or techb+" or "+techa in sent:
#             continue
#         else:
#             all.add(sent)
#             if pair not in new_pairs:
#                 new_pairs[pair] = set()
#             new_pairs[pair].add(sent)
#
# with open(os.path.join(os.pardir, "new_pattern1234_pairs.pkl"), "wb") as f:
#     pickle.dump(new_pairs, f)

print("pairs: ", len(pairs.keys()))
# print("sentences: ", len(all))

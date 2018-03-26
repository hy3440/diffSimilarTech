import gensim
import logging
import os


fname = os.path.join(os.pardir, "data", "mymodel30000000")
model = gensim.models.Word2Vec.load(fname)
print(model.wv.most_similar(positive=['performance']))

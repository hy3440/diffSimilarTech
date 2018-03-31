import gensim
import logging
import os


fname = os.path.join(os.pardir, "data", "mymodel")
model = gensim.models.Word2Vec.load(fname)
print(model.wv.vocab['a'])

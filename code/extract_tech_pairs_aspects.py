import community
import gensim, os, pickle
import matplotlib.pyplot as plt
import networkx as nx
# from networkx.algorithms import community
from nltk.corpus import stopwords
from nltk import download
import ssl


# Prepare stop words list
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
download('stopwords')
stop_words = stopwords.words('english')

# Prepare sentences
in_path = os.path.join(os.pardir, "data", "relations.pkl")
relations_file = open(in_path, 'rb')
relations = pickle.load(relations_file)
relations_file.close()
sentences = set()
for items in relations[("udp", "tcp")]:
    sentences.add(items[5])
sentences = list(sentences)
words = []
for sentence in sentences:
    words.append([w for w in sentence.split() if w not in stop_words])

# Prepare word2vector model
fname = os.path.join(os.pardir, "data", "mymodel")
model = gensim.models.Word2Vec.load(fname)
model.init_sims(replace=True)

# Build weighted graph
G = nx.Graph()
l = len(sentences)
for i in range(l - 1):
    for j in range(i + 1, l):
        distance = abs(model.wmdistance(words[i], words[j]))
        if distance > 0.5:
            if sentences[i] not in G: G.add_node(sentences[i])
            if sentences[j] not in G: G.add_node(sentences[j])
            G.add_edge(sentences[i], sentences[j], weight=distance)

# Draw graph
# pos = nx.spring_layout(G)
# plt.figure(figsize=(19,12))
# plt.axis('off')
# nx.draw_networkx_nodes(G, pos, node_size=50)
# nx.draw_networkx_edges(G, pos, width=0.75)
# plt.savefig("weighted_graph.png")
# plt.show()

# Detect communities
partition = community.best_partition(G)
print(partition)

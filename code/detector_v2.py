# import community
import gensim, os, pickle
from gensim.corpora import Dictionary
from gensim.similarities import WmdSimilarity
import math
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import community
from nltk import pos_tag
from nltk.tag.stanford import CoreNLPPOSTagger
from textblob import TextBlob as tb


# Setting
# f = open(os.path.join(os.pardir, "aspects.pkl"), 'rb')
# aspects = pickle.load(f)
# f.close()
# f = open(os.path.join(os.pardir, "new_aspects.pkl"), 'rb')
# new_aspects = pickle.load(f)
# f.close()
new_aspects = {}
query_flag = False
ver_flag = True
if ver_flag:
    com_dir = "communities"
else:
    com_dir = "communities_"
flag = False  # all sentences
pos_flag = True
if pos_flag:
    pos = ""
else:
    pos = "_without_pos_"

# pairs = [("3des", "aes"), ("png", "bmp"), ("g++", "gcc"), # < 10
#          ("postgresql", "mysql"), ("udp", "tcp"), # >100
#          ("quicksort", "mergesort"), # 50 ~ 100
#          ("vmware", "virtualbox"), ("datamapper", "activerecord"), ("sortedlist", "sorteddictionary"), # 10 ~ 15
#          ("testng", "junit"), ("jruby", "mri"), # 15 ~ 20
#          ("rsa", "aes"), ("compiled-language", "interpreted-language"), ("google-chrome", "safari"), ("heapsort", "quicksort")] #20 ~ 50

# pair = ("postgresql", "mysql")
# pair = ("udp", "tcp")
# pair = ("datamapper", "activerecord")
# pair = ("sortedlist", "sorteddictionary")
# pair = ("png", "bmp")
# pair = ("3des", "aes")
# pair = ("nfa", "dfa")
# pair = ("awt", "swing")
# pair = ("testng", "junit")
# pair = ("quicksort", "mergesort")
# pair = ("rsa", "aes")
# pair = ("vmware", "virtualbox")
# pair = pairs[-1]
large_pairs = {("chars", "int"), ("double", "int"), ("for-loop", "loops"),
               ("google-chrome", "firefox"), ("height", "width"), ("innodb", "myisam"),
               ("max", "min"), ("multiplication", "addition"), ("multiplication", "addition"),
               ("parent", "children"), ("post", "get")}

# Prepare POS tagger
pos_tag_set = {"JJR", "JJ", "NN", "NNS", "NNP", "NNPS", "RBR", "RBS", "JJS"}
# keywords_path = os.path.join(os.pardir, "communities", "{}.txt".format("&".join(pair)))
# stopwords_path = os.path.join(os.pardir, "communities", "stopwords.txt")

# Prepare stop words set
stop_words = pickle.load(open(os.path.join(os.pardir, "data", "stop_words.pkl"), 'rb'))


# Prepare stop phrases
stop_phrases = [["for", "example"], ["in", "terms", "of"], ["keep", "in", "mind"],
                ["in", "this", "case"],
                ["a", "bit"], ["of", "course"], ["due", "to"], ["generally", "speaking"],
                ["in", "general"], ["at", "the", "moment"], ["from", "my", "point", "of", "view"],
                ["in", "my", "experience"], ["at", "least"], ["at", "most"],
                ["from", "my", "experience"], ["in", "so", "many", "ways"],
                ["hard", "data"], ["sorted", "data"], ["unsorted", "data"],
                ["by", "index"], ["new", "element"], ["are", "familiar", "of"],
                ["ios", "google-chrome"], ["several", "tests"]]

# Prepare tags set
# tags = pickle.load(open(os.path.join(os.pardir, "data", "tags.pkl"), 'rb'))

# Prepare sentences
in_path = os.path.join(os.pardir, "out", "pattern1234_pairs.pkl")
relations_file = open(in_path, 'rb')
relations = pickle.load(relations_file)
relations_file.close()


# Prepare tf-idf
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


def set_shreshold(a, b):
    if ver_flag:
        if a == b:
            return 0.52
        return 0.55 - 0.05 ** abs(a - b)
    else:
        if a == b:
            return 0.55
        elif a > 3 or b > 3:
            return 0.55 - 0.1 ** abs(a - b)
        return 0.55 - 0.05 ** abs(a - b)


def main():
    sentences = list(relations[pair])
    l = len(sentences)
    corpus = []
    topics = []
    for sentence in sentences:
        if pos_flag:
            words = sentence.split()
            words[-1] = words[-1].strip()
            tagged_words = CoreNLPPOSTagger(url='http://localhost:9000').tag(words)
            if len(words) != len(tagged_words):
                tagged_words = pos_tag(words)
            # print(tagged_words)
            # print(sentence.strip())
            for phrase in stop_phrases:
                n = len(phrase)
                for i in range(len(tagged_words) - n + 1):
                    if phrase == words[i:i+n]:
                        for j in range(i, i+n):
                            tagged_words[j] = (None, tagged_words[j][1])
            i = 0
            indices = []
            keywords = []
            for (word, tag) in tagged_words:
                if word in pair:
                    indices.append(i)
                    keywords.append(word)
                    i += 1
                elif word not in stop_words and tag in pos_tag_set and word is not None:
                    keywords.append(word)
                    i += 1
            # topics.append(" ".join(keywords))
            # topics.append(sentence.strip())
            if len(keywords) <= 10 and flag:
                ws = [w for w in keywords if w not in pair]
            else:
                ws = []
                # if len(indices) == 2:
                #     for j in range(len(keywords)):
                #
                #         if j > indices[0] and j <= indices[0] + 4 and keywords[j] not in pair and j < indices[1]:
                #             ws.append(keywords[j])
                #         elif j >= indices[1] - 2 and j <= indices[1] + 2 and keywords[j] not in pair:
                #             ws.append(keywords[j])
                # else:
                if True:
                    for j in range(len(keywords)):
                        for i in indices:
                            if j >= i - 2 and j <= i + 2 and keywords[j] not in pair and keywords[j] not in ws:
                                ws.append(keywords[j])
                                break
            # with open(keywords_path, "a") as keywords_file:
            #     keywords_file.write(",".join(ws)+"\n")
            #     keywords_file.write(sentence+"\n")
            corpus.append(ws)
            topics.append(" ".join(ws))
        else:
            corpus.append([w for w in sentence.split() if w not in stop_words])

    if query_flag:
        with open(os.path.join(os.pardir, "keywords", "corpus.pkl"), 'wb') as corpus_file:
            pickle.dump(corpus, corpus_file)
        with open(os.path.join(os.pardir, "keywords", "sentences.pkl"), 'wb') as sentences_file:
            pickle.dump(sentences, sentences_file)

    else:
        # Prepare word2vector model
        fname = os.path.join(os.pardir, "data", "mymodel")
        model = gensim.models.Word2Vec.load(fname)
        model.init_sims(replace=True)

        # Build weighted graph
        # dictionary = Dictionary(corpus)
        # bow_corpus = [dictionary.doc2bow(document) for document in corpus]

        index = WmdSimilarity(corpus, model)


        G = nx.Graph()
        for i in range(l - 1):
            sims = index[corpus[i]]
            # print("query:")
            # print(corpus[i])
            # print(sentences[i])
            # print("sims:")
            for j in range(i + 1, l):
                # print(sims[j])
                # print(corpus[j])
                # print(sentences[j])
                # print()
                shreshold = set_shreshold(len(corpus[i]), len(corpus[j]))
                if sims[j] >= shreshold:
                    if i not in G: G.add_node(i)
                    if j not in G: G.add_node(j)
                    G.add_edge(i, j)
                    # G.add_edge(i, j, weight=sims[j])

        # out_path = os.path.join(os.pardir, com_dir, "{}_{}_{}.txt".format("&".join(pair), G.number_of_nodes(), l))
        # image_path = os.path.join(os.pardir, com_dir, "{}_{}_{}.png".format("&".join(pair), G.number_of_nodes(), l))

        # Draw graph
        pos = nx.spring_layout(G)
        plt.figure(figsize=(19,12))
        plt.axis('off')
        nx.draw_networkx_nodes(G, pos, node_size=50)
        nx.draw_networkx_edges(G, pos, width=0.75)
        # plt.savefig(image_path)
        # plt.show()

        nnodes = G.number_of_nodes()

        if nnodes < 4:
            communities = []
            communities.append(G.nodes())
        elif nnodes <= 15:
            communities_generator = community.girvan_newman(G)
            temp_communities = next(communities_generator)
            communities = sorted(map(sorted, temp_communities))
        else:
            if nnodes < 50:
                part = 2 / 3
            else:
                part = 1 / 3
            # Detect communities
            communities_generator = community.girvan_newman(G)
            div_flag = True
            while div_flag:
                temp_communities = next(communities_generator)
                communities = sorted(map(sorted, temp_communities))
                div_flag = False
                for com in communities:
                    if len(com) > l * part:
                        div_flag = True
                        break
        num = 0
        graph_indices = set()
        bloblist = []
        clusters = []
        for com in communities:
            if len(com) > 1:
                doc = ""
                for i in com:
                    doc += topics[i] + " "
                bloblist.append(tb(doc))
                clusters.append(com)

        new_aspects[pair] = {}
        if True:
        # with open(out_path, "a") as out_file:
            for i, blob in enumerate(bloblist):
                # print("Top words in document {}".format(i + 1))
                scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
                sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                # word_num = 0
                aspect_keywords = []
                for word, score in sorted_words[:3]:
                    # out_file.write(word+", ")
                    aspect_keywords.append(word)
                new_aspects[pair][" ".join(aspect_keywords)] = set()
                # for word, score in sorted_words:
                #     if word_num == 3:
                #         break
                #     if tf(word, blob) >= 0.2:
                #         word_num += 1
                #         out_file.write(word+", ")
                #         print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
                # out_file.write("---------------------------------------------------\n\n")
                for j in clusters[i]:
                    new_aspects[pair][" ".join(aspect_keywords)].add(sentences[j])
                    # out_file.write(",".join(corpus[j])+"\n")
                    # out_file.write(sentences[j]+"\n")
                    graph_indices.add(j)
                num += 1
            # out_file.write("other---------------------------------------------------\n\n")
            # for j in range(len(sentences)):
            #     if j not in graph_indices:
            #         out_file.write(",".join(corpus[j])+"\n")
            #         out_file.write(sentences[j]+"\n")
        plt.close('all')


# main()

# for pair in pairs[3:5]:
#     main()
try:
    for pair in relations.keys():
        if len(relations[pair]) > 2 and len(relations[pair] < 200):
            print(pair)
            main()
finally:
    print(pair)

    print("no. of pairs: ", len(new_aspects.keys()))
    tt = set()
    for (a, b) in new_aspects.keys():
        tt.add(a)
        tt.add(b)
    print("no. of different techs: ", len(tt))

    with open(os.path.join(os.pardir, "v2", "new_aspects.pkl"), "wb") as new_aspects_file:
        pickle.dump(new_aspects, new_aspects_file)
    with open(os.path.join(os.pardir, "v2", "new_aspects.txt"), "a") as new_recordings_file:
        new_recordings_file.write(str(len(new_aspects))+"\n\n")
        for key, values in new_aspects.items():
            new_recordings_file.write("\t".join(key)+"---------------------------------------------------\n\n")
            for k, value in values.items():
                new_recordings_file.write(k+"\n")
                for v in value:
                    new_recordings_file.write(str(v)+'\n')
                new_recordings_file.write("\n")

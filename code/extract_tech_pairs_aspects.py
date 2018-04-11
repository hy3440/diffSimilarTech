# import community
import gensim, os, pickle
from gensim.corpora import Dictionary
from gensim.similarities import WmdSimilarity
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import community
from nltk import pos_tag
from nltk.tag.stanford import CoreNLPPOSTagger


#Setting
query_flag = False
ver_flag = True
if ver_flag:
    com_dir = "communities"
else:
    com_dir = "communities_"
flag = False # all sentences
pos_flag = True
if pos_flag:
    pos = ""
else:
    pos = "_without_pos_"

pairs = [("3des", "aes"), ("png", "bmp"), ("g++", "gcc"), # < 10
         ("postgresql", "mysql"), ("udp", "tcp"), # >100
         ("quicksort", "mergesort") # 50 ~ 100
         ("vmware", "virtualbox"), ("datamapper", "activerecord"), ("sortedlist", "sorteddictionary"), # 10 ~ 15
         ("testng", "junit"), ("jruby", "mri"), # 15 ~ 20
         ("rsa", "aes"), ("compiled-language", "interpreted-language"), ("google-chrome", "safari"), ("heapsort", "quicksort")] #20 ~ 50
# pair = ("postgresql", "mysql")
# pair = ("udp", "tcp")
# pair = ("datamapper", "activerecord")
# pair = ("sortedlist", "sorteddictionary")
# pair = ("png", "bmp")
# pair = ("3des", "aes")
# pair = ("nfa", "dfa")
# pair = ("awt", "swing")
pair = ("testng", "junit")
# pair = pairs[-1]

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
in_path = os.path.join(os.pardir, "data", "relations.pkl")
relations_file = open(in_path, 'rb')
relations = pickle.load(relations_file)
relations_file.close()


def main():
    sentences = set()
    for items in relations[pair]:
        sentences.add(items[5])
    sentences = list(sentences)
    l = len(sentences)
    corpus = []
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


        def set_shreshold(a, b):
            if ver_flag:
                if a == b:
                    return 0.5
                return 0.55 - 0.05 ** abs(a - b)
            else:
                if a == b:
                    return 0.55
                elif a > 3 or b > 3:
                    return 0.55 - 0.1 ** abs(a - b)
                return 0.55 - 0.05 ** abs(a - b)

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


        out_path = os.path.join(os.pardir, com_dir, "{}_{}_{}.txt".format("&".join(pair), G.number_of_nodes(), l))
        image_path = os.path.join(os.pardir, com_dir, "{}_{}_{}.png".format("&".join(pair), G.number_of_nodes(), l))

        # Draw graph
        pos = nx.spring_layout(G)
        plt.figure(figsize=(19,12))
        plt.axis('off')
        nx.draw_networkx_nodes(G, pos, node_size=50)
        nx.draw_networkx_edges(G, pos, width=0.75)
        plt.savefig(image_path)
        # plt.show()

        nnodes = G.number_of_nodes()

        if nnodes == 2:
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
        with open(out_path, "a") as out_file:
            for com in communities:
            # for com in next_communities:
                if len(com) > 1:
                    out_file.write("{}---------------------------------------------------\n\n".format(num))
                    for i in com:
                        out_file.write(",".join(corpus[i])+"\n")
                        out_file.write(sentences[i]+"\n")
                        graph_indices.add(i)
                    num += 1
            out_file.write("other---------------------------------------------------\n\n")
            for i in range(len(sentences)):
                if i not in graph_indices:
                    out_file.write(",".join(corpus[i])+"\n")
                    out_file.write(sentences[i]+"\n")

# for pair in relations.keys():
#     if len(relations[pair]) > 2:
#         main()

# for pair in pairs:
#    main()

main()

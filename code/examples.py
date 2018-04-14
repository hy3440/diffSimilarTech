import os, pickle


in_path = os.path.join(os.pardir, "data", "relations.pkl")
relations_file = open(in_path, 'rb')
relations = pickle.load(relations_file)
relations_file.close()
out_path = os.path.join(os.pardir, "communities", "examples.txt")

with open(out_path, "a") as out_file:
    for pair in relations.keys():
        for items in relations[pair]:
            if "functionalities" in items[5] or "functionality" in items[5] or "feature" in items[5] or "features" in items[5]:
                out_file.write(items[5])

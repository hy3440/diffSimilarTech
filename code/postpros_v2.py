import os, pickle

large_pairs = {("chars", "int"), ("double", "int"), ("for-loop", "loops"),
               ("google-chrome", "firefox"), ("post", "get"), ("innodb", "myisam"),
               ("max", "min"), ("multiplication", "addition"), ("multiplication", "addition"),
               ("parent", "children"),  ("height", "width")}

f = open(os.path.join(os.pardir, "v2", "new_aspects.pkl"), 'rb')
new_aspects = pickle.load(f)
f.close()

in_path = os.path.join(os.pardir, "out", "relations.pkl")
relations_file = open(in_path, 'rb')
relations = pickle.load(relations_file)
relations_file.close()

for pair in relations.keys():
    if pair in large_pairs:
        continue
    elif pair in aspects.keys():
        if len(aspects[pair]) == 0:
            new_aspects[pair]["other"] = set()
            for (ta, comp, tb, topic, id, sentence) in relations[pair]:
                aspects[pair].add((ta, comp, tb, "", id, sentence))
                new_aspects[pair]["other"].add((ta, comp, tb, "", id, sentence))
        else:
            temp = set()
            new_aspects[pair]["other"] = set()
            for itema in aspects[pair]:
                temp.add(itema[5])
            for itemb in relations[pair]:
                if itemb[5] not in temp:
                    ta, comp, tb, topic, id, sentence = itemb
                    aspects[pair].add((ta, comp, tb, "", id, sentence))
                    new_aspects[pair]["other"].add((ta, comp, tb, "", id, sentence))
    else:
        aspects[pair] = set()
        new_aspects[pair] = dict()
        new_aspects[pair]["other"] = set()
        for (ta, comp, tb, topic, id, sentence) in relations[pair]:
            aspects[pair].add((ta, comp, tb, "", id, sentence))
            new_aspects[pair]["other"].add((ta, comp, tb, "", id, sentence))

with open(os.path.join(os.pardir, "v1", "aspects.pkl"), "wb") as aspects_file:
    pickle.dump(aspects, aspects_file)
print("no. of pairs: ", len(aspects.keys()))
tt = set()
for (a, b) in aspects.keys():
    tt.add(a)
    tt.add(b)
print("no. of different techs: ", len(tt))
with open(os.path.join(os.pardir, "v1", "aspects.txt"), "a") as recordings_file:
    recordings_file.write(str(len(aspects))+"\n\n")
    for key, values in aspects.items():
        recordings_file.write(key[0]+"\t"+key[1]+"\t"+str(len(values))+"\n")
        for value in values:
            # recordings_file.write(" ".join(value)+"\n")
            recordings_file.write(str(value)+'\n')
        recordings_file.write("\n")

with open(os.path.join(os.pardir, "v1", "new_aspects.pkl"), "wb") as new_aspects_file:
    pickle.dump(new_aspects, new_aspects_file)
with open(os.path.join(os.pardir, "v1", "new_aspects.txt"), "a") as new_recordings_file:
    new_recordings_file.write(str(len(new_aspects))+"\n\n")
    for key, values in new_aspects.items():
        new_recordings_file.write("\t".join(key)+"---------------------------------------------------\n\n")
        for k, value in values.items():
            new_recordings_file.write(k+"\n")
            for v in value:
                new_recordings_file.write(str(v)+'\n')
            new_recordings_file.write("\n")

import os, pickle

in_path = "aspects.pkl"
out_path = "sitemap.txt"
with open(in_path, 'rb') as aspects_file:
    aspects = pickle.load(aspects_file)
with open(out_path, 'a') as out_file:
    for tag, simi in aspects.keys():
        if tag > simi:
            s = simi+"VS"+tag+"/\n"
        else:
            s = tag+"VS"+simi+"/\n"
        out_file.write("https://difftech.herokuapp.com/"+s)
    
# Save stop words

import os, pickle
from nltk.corpus import stopwords
from nltk import download
import ssl


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
download('stopwords')
stop_words = stopwords.words('english')
# stop_words.remove("more")
stop_words = set(stop_words)

stop_words.add("less")

stop_words.add("much")
stop_words.add("reason")
stop_words.add("reasons")
stop_words.add("case")
stop_words.add("cases")
stop_words.add("etc")
stop_words.add("question")
stop_words.add("questions")
stop_words.add("people")
stop_words.add("ok")
stop_words.add("everything")
stop_words.add("something")
stop_words.add("anything")
stop_words.add("many")
stop_words.add("way")
stop_words.add("jpg")
stop_words.add("vice-versa")
stop_words.add("fact")
stop_words.add("choice")
stop_words.add("library")
stop_words.add("canvas")
stop_words.add("java")
stop_words.add("video")
stop_words.add("logn")
stop_words.add("n")
stop_words.add("wpf")
stop_words.add("app")
stop_words.add("software")
stop_words.add("times")
stop_words.add("terms")
stop_words.add("overall")
stop_words.add("python")
stop_words.add("mouseenter")
stop_words.add("mouseout")
stop_words.add("jquery")
stop_words.add("imho")
stop_words.add("fm")

with open(os.path.join(os.pardir, "data", "stop_words.pkl"), 'wb') as stop_words_file:
    pickle.dump(stop_words, stop_words_file)

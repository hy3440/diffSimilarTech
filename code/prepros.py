import re


def get_cv_and_cin():
    cv = {"beat", "beats", "prefer", "prefers", "recommend", "recommends",
          "defeat", "defeats", "kill", "kills", "lead", "leads", "obliterate",
          "obliterates", "outclass", "outclasses", "outdo", "outdoes",
          "outperform", "outperforms", "outplay", "outplays", "overtake",
          "overtakes", "smack", "smacks", "subdue", "subdues", "surpass",
          "surpasses", "trump", "trumps", "win", "wins", "blow", "blows",
          "decimate", "decimates", "destroy", "destroys", "buy", "buys",
          "choose", "chooses", "favor", "favors", "grab", "grabs", "pick",
          "picks", "purchase", "purchases", "select", "selects", "race",
          "races", "compete", "competes", "match", "matches", "compare",
          "compares", "lose", "loses", "suck", "sucks"}
    cin = {"than", "over", "beyond", "upon", "as", "against", "out", "behind",
           "under", "between", "after", "unlike", "with", "by", "opposite"}
    return (cv, cin)


def add_patterns(matcher):
    matcher.add(0,
                None,
                [{'ORTH': 'JJR'}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}],
                [{'ORTH': 'JJR'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}],
                [{'ORTH': 'JJR'}, {'ORTH': 'CIN'}, {}, {'ORTH': 'APP'}],
                [{'ORTH': 'JJR'}, {}, {'ORTH': 'CIN'}, {}, {'ORTH': 'APP'}])
    matcher.add(1,
                None,
                [{'ORTH': 'RB'}, {'ORTH': 'JJ'}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}],
                [{'ORTH': 'RB'}, {'ORTH': 'JJ'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}])
    matcher.add(8,
                None,
                [{'ORTH': 'RBR'}, {'ORTH': 'JJ'}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}],
                [{'ORTH': 'RBR'}, {'ORTH': 'JJ'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}])
    matcher.add(2,
                None,
                [{'ORTH': 'CV'}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}],
                [{'ORTH': 'CV'}, {}, {'ORTH': 'CIN'}, {'ORTH': 'APP'}])
    matcher.add(3,
                None,
                [{'ORTH': 'CV'}, {'ORTH': 'VBG'}, {'ORTH': 'APP'}])
    matcher.add(4,
                None,
                [{'ORTH': 'CV'}, {'ORTH': 'APP'}])
    matcher.add(5,
                None,
                [{'ORTH': 'VB'}, {'ORTH': 'VBN'}, {'ORTH': 'APP'}],
                [{'ORTH': 'VB'}, {'ORTH': 'VBN'}, {}, {'ORTH': 'APP'}])
    matcher.add(6,
                None,
                [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {'ORTH': 'JJS'}],
                [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'JJS'}],
                [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJS'}],
                [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJS'}])
    matcher.add(10,
                None,
                [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {'ORTH': 'RBR'}],
                [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'RBR'}],
                [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBR'}],
                [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBR'}])
    matcher.add(7,
                None,
                [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {'ORTH': 'JJR'}],
                [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'JJR'}],
                [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJR'}],
                [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'JJR'}])
    matcher.add(9,
                None,
                [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
                [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {'ORTH': 'RBS'}],
                [{'ORTH': 'APP'}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}],
                [{'ORTH': 'APP'}, {}, {'ORTH': 'VBZ'}, {}, {'ORTH': 'RBS'}])


def process_data_regex(data):
    """Use regular expression to clean the raw data to get more readable data

    :param data: strings, which are converted from rows retrieved from the database
    :return: strings, which are the processed data
    """
    symbol_list = ['=', '*', '{', '}', '[', ']', '&', '$']
    pattern = re.sub("<code>(.*?)</code>",
                     lambda m: "" if any(symbol in m.group(
                         1) for symbol in symbol_list) else m.group(), data,
                     flags=re.S)

    pattern = re.sub(r"</?[a-z][^>]*>", " ", pattern)
    pattern = re.sub(
        r"&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;|e\.g\.|i\.e\.", " ", pattern)
    pattern = re.sub(r"\*|~|`", " ", pattern)
    pattern = re.sub(r"&#xA", ". ", pattern)

    # pattern = re.sub(r"https?://.+?&#xA", "&#xA", pattern)
    pattern = re.sub(r"https?://\S+", " ", pattern)
    # pattern = re.sub(r"https?://.+?$", "", pattern)
    pattern = pattern.lower()
    return pattern


def separate_sentence_and_word(processed_data):
    """Separate sentences and words in the processed data

    :param processed_data: strings, which are the output of __process_data_regrex
    :return: a two-dimensional list which contains all the words in the processed data.
             For example, [[i, like, football][this, python, module, is, very, confusing]]
    """
    word_list = []
    # sentence_list = re.split(r"&#xa;|&#xd;|!|\?|;|\. ", processed_data)
    sentence_list = re.split(r"&#xa;|&#xd;|!|;|\. ", processed_data)

    for sentence in sentence_list:
        if (not sentence.isspace()) and sentence:
            sentence = re.sub(r"\.$", "", sentence)
            if "?" in sentence:
                sentence = sentence.split("?")[1]
            word_list.append(
                re.sub(r"[^\w|\+|\.|#|-]", " ", sentence).split())
    # if len(word_list) != 0 and word_list[-1] == []:
    #     word_list = word_list[:-1]
    return word_list


def get_words(row):
    # for row in rows:
    processed_data = process_data_regex(str(row))
    word_list = separate_sentence_and_word(processed_data)
    return word_list

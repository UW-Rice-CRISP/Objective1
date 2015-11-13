# for each article, lemmatize, strip out stop words / punct, and dump output.
# mostly to avoid doing this over and over again b/c wordnet lemmatizer
# makes jupyter stall to uselessness.

import nltk
import os
import re

from nltk.corpus import stopwords
from nltk.corpus.reader import PlaintextCorpusReader
from nltk.stem import WordNetLemmatizer

article_dir = "../../TextData/CanterburyNewsStoriesCleaned"
output_dir = "../../../lemmatized-input"

corpus = PlaintextCorpusReader(article_dir, ".*\.txt", encoding="utf8")
lemmatizer = WordNetLemmatizer()
remove_these = set(stopwords.words("english"))
is_a_word = re.compile('[a-zA-Z]')

for fid in corpus.fileids():
    print (fid)

    words = corpus.words(fid)

    # not being particularly bright here
    better = [lemmatizer.lemmatize(w) for w in words]
    better = [w for w in better if is_a_word.search(w)]
    better = [w for w in better if w not in remove_these]

    with open(os.path.join(output_dir, fid), "w") as f:
        f.write(" ".join(better))

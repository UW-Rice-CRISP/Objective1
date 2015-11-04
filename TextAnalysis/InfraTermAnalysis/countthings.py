# simple word search / dump counts of specific words per file
# potential todo later: break down by category (energy, water, ...)
# usage: python countthings.py

from collections import defaultdict
import json
import os
import sys

import nltk
from nltk.corpus.reader import PlaintextCorpusReader

vocab_file = "vocab.txt"
article_dir = "../../TextData/CanterburyNewsStoriesCleaned"

with open(vocab_file, "r") as f:
    all_vocab = json.load(f)
vocab_set = {x for v in all_vocab.values() for x in v}

corpus = PlaintextCorpusReader(article_dir, ".*\.txt", encoding="utf8")

counts_per_file = {} # {filename: {'word1': count1, 'word2': count2, ...}}
counts_aggregate = defaultdict(int) # {'word1': count1, ...}
for fid in corpus.fileids():
    print (fid)

    words = corpus.words(fid)
    freqs = nltk.FreqDist(w.lower() for w in words)

    counts_per_file[fid] = {}
    for v in vocab_set:
        if v in freqs:
            counts_per_file[fid][v] = freqs[v]
            counts_aggregate[v] += freqs[v]

# dump output for future usage

counts_file = "counts_per_file.txt"
with open(counts_file, "w") as f:
    json.dump(counts_per_file, f)

counts_agg_file = "counts_aggregate.txt"
with open(counts_agg_file, "w") as f:
    json.dump(counts_aggregate, f)

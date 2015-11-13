# Preprocess input texts to be semafor-friendly:
# one sentence on each line but no extra newlines
# (else it'll vomit).

import nltk
import os

input_dir = "../CanterburyNewsStoriesCleaned/"
output_dir = "../../../semafor-input/"

for fn in os.listdir(input_dir):
    if not fn.endswith(".txt"):
        continue

    print (fn)
    with open(os.path.join(input_dir, fn), "r") as f:
        raw = f.read()

    sents = nltk.sent_tokenize(raw)
    sents = [s.replace('\n', ' ').strip() for s in sents]
    new = '\n'.join(sents)

    with open(os.path.join(output_dir, fn), "w") as f:
        f.write(new)


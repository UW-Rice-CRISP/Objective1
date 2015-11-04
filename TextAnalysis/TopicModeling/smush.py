import os
from types import *

from enum import Enum
from nltk import sent_tokenize
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import StanfordTokenizer

source = 'clean'
dest = 'input'

tokenizer = StanfordTokenizer()
tagger = StanfordPOSTagger('english-left3words-distsim.tagger')
nn_tags = {'NN', 'NNS', 'NNP', 'NNPS'}
adj_tags = {'JJ'}
TagState = Enum('TagState', 'other noun adj')

# don't want brackety tags to show up in the corpus
remove_tags = { '-LRB-', '-LSB-', '-LCB-',
                '-RRB-', '-RSB-', '-RCB-' }

def smush(text):
    tokens = tokenizer.tokenize(text)
    tags = tagger.tag(tokens)

    # walk through the sentence and greedily combine adj*nn+ into
    #   single chunks
    # (hopefully chunking doesn't mean something different :/)

    # some state holding
    chunks = []
    chunk = []
    state = TagState.other

    def reset_chunk():
        nonlocal chunks, chunk
        if len(chunk) > 0:
            chunks.append('_'.join(chunk))
            chunk = []

    # there is probably some prettier pythonic way to do this;
    # figure that out later
    for idx, tag in enumerate(tags):
        # figure out what this new word is
        if tag[1] in nn_tags:
            new_state = TagState.noun
        elif tag[1] in adj_tags:
            new_state = TagState.adj
        else:
            new_state = TagState.other

        if new_state == TagState.other:
            reset_chunk()
            if tag[0] not in remove_tags:
                chunks.append(tag[0]) # standalone chunk

        elif new_state == TagState.adj:
            if state == TagState.noun:
                # close out the old chunk and create new
                reset_chunk()

            chunk.append(tag[0])

        else: # if new_state == TagState.noun:
            chunk.append(tag[0])

        state = new_state

    # add last chunk
    reset_chunk()

    return ' '.join(chunks)


for directory, subdirs, filenames in os.walk(source):
    for fn in filenames:
        source_path = os.path.join(directory, fn)
        if not os.path.isfile(source_path):
            # whatever
            continue

        dest_path = os.path.join(dest, fn)
        if os.path.isfile(dest_path):
            # already done
            continue

        print(fn)

        with open(source_path, 'r+') as f:
            raw_text = f.read()

        new_text = smush(raw_text)

        with open(dest_path, 'w+') as f:
            f.write(new_text)

Topic modeling
==============

TODO: clean up these notes a bit more... (/ perhaps check in the preprocessed txt files and mallet model?)

Data preprocessing
------------------

In theory, we could just run topic modeling on the cleaned up text, but per advice from Noah: greedily mark (adj)\*(noun)+ as a single unit.

smush.py is an informal script that loops over all the files (assumed to be .txt) in a directory and outputs corresponding .txt files with the above items smushed together. For example, "Christchurch City Council" becomes a single unit, "Christchurch\_City\_Council" for the below.

This takes 1-2 sec. per input file on my Macbook Air; the expensive part is the POS tagging.

Requirements: python's nltk package and the Stanford [tokenizer](http://nlp.stanford.edu/software/tokenizer.shtml) and [POS tagger](http://nlp.stanford.edu/software/tagger.shtml). There is some [classpath fixing](https://github.com/nltk/nltk/wiki/Installing-Third-Party-Software#stanford-tagger-ner-tokenizer-and-parser) to do for nltk to recognize the tokenizer/tagger.


Using mallet to get a topic model
---------------------------------

Mallet: <http://mallet.cs.umass.edu/topics.php>

and a how-to guide: <http://programminghistorian.org/lessons/topic-modeling-and-mallet>

Installation is easy on OS X (/ dealing with ant and java and .jar stuff is painful):

    brew install homebrew/science/mallet

Below steps were done on the Canterbury/Christchurch articles; substitute directory names as desired. (Note that the names of the mallet output files are significant for the visualization tool used below.)

1. Getting the corpus in the right format:

    mkdir corpus
    mallet import-dir --input ./mallet-input --output corpus/corpus.mallet --keep-sequence --remove-stopwords --token-regex '[\p{L}_]+\p{L}'

2. Getting a topic model, e.g. w/25 topics:

    mkdir topics-25
    mallet train-topics --input corpus/corpus.mallet --num-topics 25 --optimize-interval 20 --output-model topics-25/lda.mallet --output-topic-keys topics-25/output-topic-keys.txt --topic-word-weights-file topics-25/topic-word-weights.txt --output-doc-topics topics-25/doc-topic-mixtures.txt --word-topic-counts-file topics-25/word-topic-counts.txt

(There are probably cleaner ways to script this up, but as a small-value-of-n-off it works.)

Visualization
-------------

(Because reading text files is no fun at all.)

Termite: <http://vis.stanford.edu/papers/termite>

Get the [termite-data-server package](https://github.com/uwdata/termite-data-server) from github; note that they claim support for specifically python 2.7 + OS X (Linux variants might work?).

The readme there notes a termite-visualization package and how you supposedly need both; I can't get those things to connect and termite-data-server already has visualizations anyways.

Install notes: from the root directory of termite-data-server, remember to do these:

    setup: bin/setup_corenlp.sh
    bin/setup_mallet.sh
    make -C utils/corenlp

(Annoyance: it doesn't use an already existing version of mallet.)

In theory, one could create topic models using this directly (there are some scripts in bin/ which call mallet), but (a) I didn't realize this was an option and (b) one would need to figure out what script to edit to include the token-regex parameter above.

(Another annoyance: code as the primary source of documentation.)

Otherwise, assuming that we have the topic model output from mallet...

Getting the corpus files they want is a bit roundabout. From the root directory of termite-data-server:

* corpus.db: positional parameters are \[output directory\] \[input files\], e.g.

    python bin/import_corpus.py ../corpus "../mallet-input/*"

* corpus.txt:  positional parameters are \[corpus.db directory\] \[output file\], e.g.

    python bin/export_corpus.py ../corpus ../corpus/corpus.txt

From this, we can import a mallet model (args: app\_name model\_path corpus\_path database\_path), e.g.:

    python bin/read_mallet.py quake25 ../topics-25 ../corpus ../corpus

From here, start up the data server:

    ./start_server.sh

There should be options to select a data set and then a visualization type.

README
======

Files (for now):

* jupyter notebook for some frequency calculations and graphs.

* vocab.txt: Infra words to search for; these are tentatively organized by "category" corresponding to the DHS page I was skimming through. Currently manually constructed from looking at the relevant DHS pages for power, water, and transportation; perhaps should shift to something via wordnet (/similar). Readable via json.load().

* countthings.py: Quick & dirty script (warning: hardcoded paths, filenames) to get counts of words from vocab.txt. Produces two files:

    * counts\_per\_file.txt: Contains the counts of words in vocab.txt per input text file. Readable via json.load(); format is {'filename1': {'term1': n11, 'term2': n12, ...}, 'filename2': {'term1': n21', ...}}, i.e. dictionary indexable by filename and then by the terms from vocab.txt.

    * counts\_aggregate.txt: Contains the total counts of words across all input texts. Readable via json.load(); format is {'term1': n1, 'term2': n2, ...}, i.e. dictionary of counts indexable by the infra words. Contents can be put into a nltk FreqDist for further analysis (-> e.g. fd.plot(20)).

* lemmatize.py: Another quick & dirty script to lemmatize / strip out stopwords and punctuation from input articles (should rerun vocab frequencies on this!).

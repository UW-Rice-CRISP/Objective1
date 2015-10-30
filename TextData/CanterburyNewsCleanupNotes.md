NZ article cleanup notes
========================

(Applicable to future article cleanup efforts.)

Setup
-----

[Newspaper](http://newspaper.readthedocs.org), among other things, extracts article text given raw HTML (which we have!).

Things to do to get Newspaper to work (using python 3.5; not sure if this applies to 2.x):

* Follow the Newspaper [install instructions](http://newspaper.readthedocs.org/en/latest/user_guide/install.html).
* Upgrade beautifulsoup to latest: this fixes an [issue between beautifulsoup and python 3.5](http://stackoverflow.com/questions/28745153/importing-bs4-in-python-3-5).
* Install pillow 2.9.0. This is somewhat finicky; at minimum may need to [reinstall pillow after Newspaper](http://stackoverflow.com/questions/8915296/python-image-library-fails-with-message-decoder-jpeg-not-available-pil), but the latest version, 3.0.0, [has its own issues](https://github.com/python-pillow/Pillow/issues/1474, at minimum reinstalling pillow might be required to get things to work).

Originally tried using [python-goose](https://github.com/grangier/python-goose), but the latest version did a poor job of extracting article text (lots of blank articles).

Cleanup
-------

Quick and dirty script: Scripts/cleaner.py

Nothing profound; this just walks through all the .html files in a source directory ./html, makes appropriate Newspaper api calls, and dumps corresponding cleaned up output files in another directory ./clean. Modify paths at the top of the file as needed.

After this, do a quick manual cleanup of irrelevant files that got scraped (e.g. search results, advertising). In this case, I killed the following:

* Articles with really small (< 100b) cleaned up output. (These were usually img galleries / video captions, which aren't too interesting here.)
* Articles with titles that don't look legit... the legit ones either have actual interesting titles or format "article-...". Example of something to kill is "eqc\_stuff.html" which is just advertising.

Quick stats
-----------

Total file count after quick manual cleanup: 1084

Total word count: 884272

    find . -type f -print0 | xargs -0 cat | wc -w

=> Average word count per article: ~816

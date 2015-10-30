# quick and dirty script
# for each file in source dir, dump the cleaned text into filename.txt in dest dir
# assumes that newspaper has been set up

from newspaper import Article
import os

# modify as needed
source = 'html'
dest = 'clean'

for directory, subdirs, filenames in os.walk(source):
    for fn in filenames:
        if not fn.endswith('.html'):
            continue

        print(fn)

        source_path = os.path.join(directory, fn)
        dest_path = os.path.join(dest, fn.replace('.html', '.txt'))
        
        if os.path.isfile(dest_path):
            # already exists!
            continue

        a = Article('') # not downloading from web; supply raw html manually

        with open(source_path, 'r+') as f:
            raw_html = f.read()

        a.set_html(raw_html)
        a.parse()

        # in the future: see if we can get interesting metadata?
        # e.g. if we scrape directly using this api

        with open(dest_path, 'w+') as f:
            f.write(a.text)

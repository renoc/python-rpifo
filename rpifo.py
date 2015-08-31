from random import randint
import os


dirlist = []
filedict = {}

for dirpath, dnames, fnames in os.walk("."):
    for filename in fnames:
        # exclude self and previous playlist result
        if len(dirpath) > 1:
            dirlist.append(dirpath)
            q = filedict.get(dirpath, [])
            q.append(filename)
            # not worth optimizing
            filedict[dirpath] = q

# sort files in folders alphabetically
for key in filedict:
    filedict[key].sort()

with open('rpifo.m3u', 'w') as the_file:
    while len(dirlist):
        dirpath = dirlist.pop(randint(1, len(dirlist)) - 1)
        filename = filedict[dirpath].pop(0)
        the_file.write('%s/%s\n' % (dirpath, filename))

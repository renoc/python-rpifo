from random import randint
import os


dirlist = []
filedict = {}

for dirpath, dnames, fnames in os.walk("."):
    for filename in fnames:
        dirlist.append(dirpath)
        q = filedict.get(dirpath, [])
        q.append(filename)
        filedict[dirpath] = q

for key in filedict:
    filedict[key].sort()

with open('rpifo.m3u', 'w') as the_file:
    while len(dirlist):
        dirpath = dirlist.pop(randint(0, len(dirlist)-1))
        filename = filedict[dirpath].pop(0)
        the_file.write('%s/%s\r\n' % (dirpath, filename))

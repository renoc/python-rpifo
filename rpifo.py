from random import randint
import os
import re


dirlist = []
extensions = []
filedict = {}


def set_extensions():
    global extensions
    filename = 'ext.txt'
    if not os.path.exists(filename):
        return False

    with open(filename, 'r') as open_file:
        for line in open_file:
            # strip . and \n
            pattern = re.compile('[\W_]+')
            ext = pattern.sub('', line)
            len(ext) and extensions.append(ext)


def check_filetype(filename):
    ext = filename.split('.')[-1]
    if ext in extensions:
        return True
    return False


set_extensions()
for dirpath, dnames, fnames in os.walk("."):
    for filename in fnames:
        valid_filetype = (not len(extensions)) or check_filetype(filename)
        # exclude self and previous playlist result
        if len(dirpath) > 1 and valid_filetype:
            dirlist.append(dirpath)
            q = filedict.get(dirpath, [])
            q.append(filename)
            # not worth optimizing
            filedict[dirpath] = q


# sort files in folders alphabetically
for key in filedict:
    filedict[key].sort()


with open('rpifo.m3u', 'w') as open_file:
    while len(dirlist):
        dirpath = dirlist.pop(randint(1, len(dirlist)) - 1)
        filename = filedict[dirpath].pop(0)
        open_file.write('%s/%s\n' % (dirpath, filename))

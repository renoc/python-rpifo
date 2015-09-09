from random import randint
from time import time
import os
import re


dirlist = []
extensions = []
filedict = {}
last_feedback = time()


def feedback(message):
    print message


def report_progress():
    global last_feedback
    now = time()
    if now - last_feedback > 3:
        feedback('Processing %s Files' % len(dirlist))
        last_feedback = now


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


def read_directories():
    feedback('Reading Directories...')

    def check_filetype(filename):
        # exclude self and previous playlist result
        if not len(extensions):
            return True
        ext = filename.split('.')[-1]
        if ext in extensions:
            return True
        return False

    for dirpath, dnames, fnames in os.walk("."):
        for filename in fnames:
            if len(dirpath) > 1 and check_filetype(filename):
                dirlist.append(dirpath)
                q = filedict.get(dirpath, [])
                q.append(filename)
                # not worth optimizing
                filedict[dirpath] = q
            report_progress()


def process_list():
    # sort files in folders alphabetically
    for key in filedict:
        filedict[key].sort()


def output_m3u():
    feedback('Outputting File rpifo.m3u')
    with open('rpifo.m3u', 'w') as open_file:
        while len(dirlist):
            report_progress()
            dirpath = dirlist.pop(randint(1, len(dirlist)) - 1)
            filename = filedict[dirpath].pop(0)
            open_file.write('%s/%s\n' % (dirpath, filename))
    feedback('...Done')


set_extensions()
read_directories()
process_list()
output_m3u()

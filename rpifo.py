from random import randint
from time import time
import os
import re

from pdabt import DABTree


MIN_FOLDER_SIZE = 1     # Suggested value 32
dabtree = DABTree()
dirlist = []
exclusions = []
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


def set_exclusions():
    global exclusions
    filename = 'rexclude.txt'
    if not os.path.exists(filename):
        return False

    with open(filename, 'r') as open_file:
        for line in open_file:
            exclude = re.split('\n', line)[0]
            len(exclude) and exclusions.append(re.compile(exclude, re.I))


def set_extensions():
    global extensions
    filename = 'ext.txt'
    if not os.path.exists(filename):
        return False

    with open(filename, 'r') as open_file:
        pattern = re.compile('[\W_]+')
        for line in open_file:
            # strip . and \n
            ext = pattern.sub('', line)
            len(ext) and extensions.append(ext)


def check_filetype(filename, dirpath):
    for pattern in exclusions:
        forbidden = pattern.search(filename) or pattern.search(dirpath)
        if forbidden:
            return False
    # exclude self and previous playlist result
    if len(extensions):
        ext = filename.split('.')[-1]
        if not ext.lower() in extensions:
            return False
    return True


def read_directories():
    feedback('Reading Directories...')
    for dirpath, dnames, fnames in os.walk(u'.'):
        for filename in fnames:
            if len(dirpath) > 1:
                dirlist.append(dirpath)
                q = filedict.get(dirpath, [])
                q.append(filename)
                # not worth optimizing
                filedict[dirpath] = q
            report_progress()


def process_list():
    # sort files in folders alphabetically
    feedback('Calculating Season Sizes...')
    for key in filedict:
        folder = filedict[key]
        folder.sort(key=lambda x: x.lower())
        assert len(folder) > 0
        place_season(folder, key, 1.0, dabtree)
        report_progress()


def place_season(folder, key, coverage, node):
    # create seasons / normalize time between episodes
    size = len(folder)
    if size > MIN_FOLDER_SIZE:
        node.add_value(value=coverage)
        return
    leaf = node.invoke_least()
    before = node.west is leaf
    for _ in range(size):
        dirlist.append(key)
        if before:
            folder.insert(0, '')
        else:
            folder.append('')
    place_season(folder, key, coverage/2.0, leaf)


def output_m3u():
    feedback('Outputting File rpifo.m3u')
    with open('rpifo.m3u', 'w') as open_file:
        while len(dirlist):
            report_progress()
            dirpath = dirlist.pop(randint(0, len(dirlist)) - 1)
            filename = filedict[dirpath].pop(0)
            if check_filetype(filename, dirpath):
                open_file.write(('%s/%s\n' % (dirpath, filename)).encode(
                    'utf8'))
    feedback('...Done')


set_exclusions()
set_extensions()
read_directories()
process_list()
output_m3u()

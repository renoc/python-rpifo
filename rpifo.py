from random import randint, shuffle
from time import time
import os
import re

from pdabt import DABTree


MIN_FOLDER_SIZE = 2     # Minmum effective value
dabtree = DABTree()
dirlist = []
exclusions = []
extensions = []
filedict = {}
last_feedback = time()


def print_message(message):
    print message


feedback = print_message


def report_progress():
    global last_feedback
    now = time()
    if now - last_feedback > 3:
        feedback('Processing %s Files' % len(dirlist))
        last_feedback = now


def load_settings():

    def set_exclusions():
        global exclusions
        for exclude in settings.REGEX_FILENAME_EXCLUSION:
            len(exclude) and exclusions.append(
                re.compile(exclude.strip(), re.I))

    def set_extensions():
        global extensions
        pattern = re.compile('[\W_]+')
        for ext in settings.EXTENTIONS:
            # strip . and \n
            ext = pattern.sub('', ext)
            len(ext) and extensions.append(ext)

    try:
        import settings
    except ImportError:
        feedback('Settings NOT FOUND')
        return False
    global MIN_FOLDER_SIZE
    feedback = settings.FEEDBACK
    MIN_FOLDER_SIZE = settings.MIN_FOLDER_SIZE
    set_exclusions()
    set_extensions()
    feedback('Settings loaded')


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

    def place_season(folder, key, count, node):
        # create seasons / normalize time between episodes
        size = len(folder)
        if size > MIN_FOLDER_SIZE:
            node.add_value(value=count)
            return
        leaf = node.invoke_least()
        before = node.west is leaf
        for _ in range(size):
            dirlist.append(key)
            if before:
                folder.insert(0, '')
            else:
                folder.append('')
        place_season(folder, key, count, leaf)

    # sort files in folders alphabetically
    feedback('Calculating Season Sizes...')
    keys = filedict.keys()
    shuffle(keys)
    for key in keys:
        folder = filedict[key]
        folder.sort(key=lambda x: x.lower())
        assert len(folder) > 0
        place_season(folder, key, len(folder), dabtree)
        report_progress()


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


load_settings()
read_directories()
process_list()
output_m3u()

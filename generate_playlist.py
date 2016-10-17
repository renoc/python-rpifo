from random import randint, shuffle
from time import time
import os
import re


def print_message(message):
    print message


class Playlist(object):
    MIN_FOLDER_SIZE = 2     # Minmum effective value
    dirlist = []
    evenly_spaced = True
    exclusions = []
    extensions = []
    filedict = {}
    feedback = print_message
    fullspread = []
    last_feedback = time()

    def __init__(self, *args, **kwargs):
        self.feedback = print_message

        try:
            import settings
        except ImportError:
            self.feedback('Settings NOT FOUND')
            return False

        def set_exclusions():
            for exclude in settings.FILENAME_EXCLUSION:
                len(exclude) and self.exclusions.append(
                    re.compile(exclude.strip(), re.I))

        def set_extensions():
            pattern = re.compile('[\W_]+')
            for ext in settings.EXTENTIONS:
                # strip . and \n
                ext = pattern.sub('', ext)
                len(ext) and self.extensions.append(ext)

        def set_fullspread():
            for folder in settings.FULLSPREAD_FOLDERS:
                len(folder) and self.fullspread.append(
                    re.compile(folder.strip(), re.I))

        self.feedback = settings.FEEDBACK
        self.MIN_FOLDER_SIZE = settings.MIN_FOLDER_SIZE
        self.evenly_spaced = settings.EVENLY_SPACED
        set_exclusions()
        set_extensions()
        set_fullspread()
        self.feedback('Settings loaded')

    def report_progress(self, operation='Processing'):
        now = time()
        if now - self.last_feedback > 3:
            self.feedback('%s %s Files' %(operation, len(self.dirlist)))
            self.last_feedback = now

    def check_filetype(self, filename, dirpath):
        for pattern in self.exclusions:
            forbidden = pattern.search(filename) or pattern.search(dirpath)
            if forbidden:
                return False
        if len(self.extensions):
            ext = filename.split('.')[-1]
            if not ext.lower() in self.extensions:
                return False
        return True

    def process_list(self):
        # sort files in folders alphabetically
        keys = self.filedict.keys()
        for key in keys:
            self.filedict[key].sort(key=lambda x: x.lower())
        try:
            from pdabt import DABTree
        except ImportError:
            self.feedback('DABTree NOT FOUND')
            return False

        def place_season(folder, key, count, node):
            # create seasons / normalize time between episodes
            size = len(folder)
            if size > self.MIN_FOLDER_SIZE:
                node.add_value(value=count)
                return
            leaf = node.invoke_least()
            for _ in range(size):
                self.dirlist.append(key)
                if node.west is leaf:
                    folder.insert(0, '')
                else:
                    folder.append('')
            place_season(folder, key, count, leaf)

        dabtree = DABTree()
        self.feedback('Calculating Season Sizes...')
        shuffle(keys)
        for key in keys:
            folder = self.filedict[key]
            assert len(folder) > 0
            exempt = False
            for pattern in self.fullspread:
                exempt = exempt or pattern.search(key)
            if not exempt:
                place_season(folder, key, len(folder), dabtree)
            self.report_progress()


def read_directories(playlist):
    playlist.feedback('Reading Directories...')
    for dirpath, dnames, fnames in os.walk(u'.'):
        for filename in fnames:
            # exclude self and previous playlist result
            if len(dirpath) > 1 and playlist.check_filetype(filename, dirpath):
                playlist.dirlist.append(dirpath)
                q = playlist.filedict.get(dirpath, [])
                q.append(filename)
                # not worth optimizing
                playlist.filedict[dirpath] = q
            playlist.report_progress('Reading')


def write_entry(playlist, open_file, dirpath):
    playlist.report_progress('Writing')
    filename = playlist.filedict[dirpath].pop(0)
    # remove season padding
    if not filename:
        return
    open_file.write(('%s/%s\n' % (dirpath, filename)).encode('utf8'))


def output_espifo_m3u(playlist):
    output = []
    for directory in sorted(playlist.filedict, key=lambda k: len(
                            playlist.filedict[k]), reverse=True):
        playlist.report_progress()
        varient = len(output) / (len(playlist.filedict[directory]) + 1.0)
        for index in range(len(playlist.filedict[directory]), 0, -1):
            output.insert(int(index * varient), directory)
    with open('playlist.m3u', 'w') as open_file:
        for dirpath in output:
            playlist.dirlist.pop(0)
            write_entry(playlist, open_file, dirpath)


def output_rpifo_m3u(playlist):
    # Reduce problem with 'programming blocks'
    shuffle(playlist.dirlist)
    with open('playlist.m3u', 'w') as open_file:
        while len(playlist.dirlist):
            dirpath = playlist.dirlist.pop(
                randint(0, len(playlist.dirlist)) - 1)
            write_entry(playlist, open_file, dirpath)


def gen_playlist():
    playlist = Playlist()
    read_directories(playlist)
    playlist.process_list()
    playlist.feedback('Outputting File playlist.m3u')
    if playlist.evenly_spaced is True:
        output_espifo_m3u(playlist)
    else:
        output_rpifo_m3u(playlist)
    playlist.feedback('...Done')


gen_playlist()

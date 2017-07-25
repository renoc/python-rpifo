# python-rpifo
Random Playlist In Folder Order


##Version
#### 3.1
* New option to evenly space entries


##Purpose
Simple script to create a randomized playlist where certain sets of files are
played in order, but not immediately concurrent. You can play all your podcasts
as serials and create your own radio station, or television station if they're
video podcasts. The show to be played is random but the episodes are in order.

Subsets are controlled by folder structure, order is alphabetical by filename.
The LazyTv plugin for Kodi(XBMC) has a similar function, but RPIFO will work
in far less steps, without complicated internet searching logic, and available
in a format compatible with multiple media players and platforms.


##Instructions
0. Organize your media into one folder per show (not per season) alphabetically
1. Place .py files in the parent directory that contains your media folders
    * Optional: Rename settings.py.sample to settings.py and edit
        * Recommended: Change MIN_FOLDER_SIZE, smaller folders will appear in a
        smaller section of the playlist, preventing long breaks in a series
2. Run the generate_playlist.py script
3. Open the resulting playlist.m3u in your media player.
    * Recommended: Change playlist name so it won't be overwritten by script


##Requirments
* Python 2.79
    * https://www.python.org/downloads/release/python-279/
    * Forwards compatibility: ????
    * Backwards compatibility: ????


##Software Compatibility
* Pass
    * Linux
    * Windows
    * Clementine
    * VLC
    * Winamp
* Fail
    * Media Player Classic


##Logical Assumptions
* No files in the working directory should be added to playlist
* Non-media files will be ignored/skipped quickly by the player if not filtered
* Large amounts of files can be quickly and eaisly renamed using Bulk Renamer
    * http://www.bulkrenameutility.co.uk/


##To-Do
* Path settings
* Make seperate pDABt project
* Shuffle Folders Regex
* Random/Even mixed options
* Feedback # kwarg

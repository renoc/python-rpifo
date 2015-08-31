# python-rpifo
Random Playlist In Folder Order


##Version
#### 1.0
* Live Testing Successful


##Purpose
Simple script to create a randomized playlist where certain sets of files are
played in order, but not immediately concurrent. You can play all your podcasts
as serials and create your own radio station, or television station if they're
video podcasts.

Subsets are controlled by folder structure, order is alphabetical by filename.
The LazyTv plugin for Kodi(XBMC) has a similar function, but RPIFO will work
in far less steps, without complicated internet searching logic, and available
in a format compatible with multiple media players and platforms.


##Instructions
0. Organize your media into one folder per show (not per season) alphabetically
1. Place rpifo.py in the parent directory that contains your media folders
2. Run the rpifo.py script
3. Open the resulting rpifo.m3u in your media player.


##Requirments
* Forwards compatibility: ????
* Python 2.79 https://www.python.org/downloads/release/python-279/
* Backwards compatibility: ????


##Software Compatibility
* Linux: Pass
* Windows: Pass
* VLC: Pass
* Winamp: Pass
* Fail: MPC


##Logical Assumptions
* Non-media files will be ignored/skipped quickly


##To-Do
* Exclusion Regex File
* Paths File
* Extentions Filter

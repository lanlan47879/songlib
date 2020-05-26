# songlib
A small CLI that provides easy access to study materials for songs you're learning.

## Background
I started learning to play the ukulele a couple months ago and got tired of hunting down 
all my song tabs and videos everything time I wanted to practice a song. And I figured this would be
a good example to get a bit more familiar with Python and JSON.

This is mostly for personal use so I only have support for adding tabs and videos to a
specific song, which is what I use, but I might add support for different types of materials at some point.

## Installation
I haven't figured out how to upload this to PyPi so for now I just have this installed by running `pip3 install .` in the repo directory.

## Usage
* [Adding materials](#add-materials-to-songs)
* [Listing available songs](#list-available-songs)
* [Opening materials](#open-song-materials)
* [Removing songs/materials](#removing-songs-and-materials)

### Add Materials to Songs
To add a material to a song use the following format:

      songlib add SONGNAME [tab|video] MAT_TITLE MAT_SOURCE

* SONGNAME is the name of the song you want to add the material to. Make sure to use '' around 
song names that contain whitespace.
* [tab|video] specifies what type of material you want to add.
* MAT_TITLE is the title given to the material you want to add.
* MAT_SOURCE is the file path or URL of the material you want to add.

For example if I wanted to add a tab to the song 'Build Me Up Buttercup', I would use the command:

      songlib add 'build me up buttercup' tab PDF ~/Documents/uke/build_me_up_buttercup.pdf

### List Available Songs
To list all the songs in your library use the following command:

      songlib ls

This would yield output similar to the following:
>[1] Banana Pancakes  
>[2] Build Me Up Buttercup  
>[3] Your Song  

### Open Song Materials
To open the materials for a song, use the following format:

      songlib mats SONGNAME

* SONGNAME is the name of the song that you want to open materials for. Make sure to use '' around 
song names that contain whitespace.

By default, the mats command will open a tab and a video for the specified song. It'll just open materials which you have, 
so if you have a tab but no video for a song, it'll just open the tab, and vice versa. 


* If you only want to open the tab for the song, use the `--tab/-t` option:

      songlib mats SONGNAME --tab or songlib mats SONGNAME -t

* If you only want to open the video for the song, use the `--video/-v` option:

      songlib mats SONGNAME --video or songlib mats SONGNAME -v
      
If you have multiple tabs and/or videos for the song, it'll prompt you for which one you want to open.
      
### Removing Songs and Materials
To remove a song, use the following format:

      songlib rm SONGNAME

* SONGNAME is the name of the song you want to remove. Make sure to use '' around 
song names that contain whitespace.

By default, the rm command will remove a song and all of its materials.

* If you only want to remove the tab for the song, use the `--tab/-t` option:

      songlib rm SONGNAME --tab or songlib rm SONGNAME -t

* If you only want to remove the video for the song, use the `--video/-v` option:

      songlib rm SONGNAME --video or songlib rm SONGNAME -v
      
If you have multiple tabs and/or videos for the song, it'll prompt you for which one you want to remove.

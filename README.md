MERGE-TILES
===========

Simple Python script to download and merging spatial raster tiles from any web-services

## Required

* Pillow

## Usage

### From console with options

    $ ./merge_tiles.py -h # show all options
    $ ./merge_tiles.py -b "50 104 56 110" -z 8 -t "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" -S "a,b,c" -N osm
    $ ./merge_tiles.py -b "50 104 56 110" -z 8 -s Google
    $ ./merge_tiles.py -b "50 104 56 110" -z 8 -s Bing
    
### From console wizard

Run
 
    $ ./tileparser_console.py
    
and answer the questions    


### GUI (unstable)

Required PyQt4

    $ ./tileparser_gui.py
    

## Programmatic

look an advanced using example in marge_tiles.py - PkkAreaMerger (line: 309) - download area image from ppk5 Rosreestr 


## Author
 
Artemiy Doroshkov -- rendrom@gmail.com


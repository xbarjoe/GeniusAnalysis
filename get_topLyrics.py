import os
import sys
import numpy as np
import np_utils
import pandas as pd
import lyricsgenius as lg
import nltk

#Method used for cleanly getting Artist names / Song titles for genius lyric requests
#Returns the list (copied directly from the genius website) and returns the tracks in the form [trackTitle / Artist]
def clean_requests():
    f = open(r"songs.txt",encoding="utf8")
    strings = list()
    for line in f:
        strings.append(line[:-5])

    for i in range(0,len(strings)):
        if "LYRICS" in strings[i]:
            strings[i] = strings[i].replace("LYRICS",", ")
        if str(i+1) in strings[i]:
            strings[i] = strings[i].replace(str(i+1),'')
        if strings[i][-1] == '1':
            strings[i] = strings[i][:-1]

    requests = list()
    for x in strings:
        requests.append(x.split(','))
    return requests
    
def main():
    #can be ignored, using existing API keys
    key = open(r'plies_key.txt','r')
    key_text = str(key.read())
    genius = lg.Genius(key_text,
    skip_non_songs=True,
    excluded_terms=["(Live)"],
    remove_section_headers=True)
    top100songs = clean_requests()
    for song in top100songs:
        song = genius.search_song(song[0],song[1])
        song.save_lyrics()
if __name__ == "__main__":
    main()
import sqlite3
import os.path
import numpy as np
import matplotlib.pyplot as plt


def jointables(dbname):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, dbname)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute('DROP TABLE JoinTable')
    except:
        pass
    c.execute("CREATE TABLE IF NOT EXISTS JoinTable (artist_names TEXT, Spotify_genres TEXT, Musixmatch_genres TEXT)")
    c.execute(
        '''
        INSERT INTO JoinTable SELECT Musixmatch_Genres.artist_names, Spotify_Genres.genres,Musixmatch_Genres.genres
        FROM Spotify_Genres
        INNER JOIN Musixmatch_Genres ON Musixmatch_Genres.artist_names=Spotify_Genres.artist_names;
        '''
    )
    conn.commit()
    c.close()

def jointables2(dbname):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, dbname)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute('DROP TABLE JoinTable2')
    except:
        pass
    c.execute("CREATE TABLE IF NOT EXISTS JoinTable2 (songs TEXT, Spotify_PopScores TEXT, Musixmatch_PopScores TEXT)")
    c.execute(
        '''
        INSERT INTO JoinTable2 SELECT Musixmatch_PopScores.songs, Spotify_PopScores.popularity, Musixmatch_PopScores.popularity
        FROM Spotify_PopScores
        INNER JOIN Musixmatch_PopScores ON Musixmatch_PopScores.songs=Spotify_PopScores.songs;
        '''
    )
    conn.commit()
    c.close()



def countsame(dbname):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, dbname)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM JoinTable")
    same_count = 0
    different_count = 0
    for row in c:
        if row[1].lower() == row[2].lower():
            same_count += 1
        else:
            different_count += 1 
    return same_count, different_count

def barchart_musixmatch(dbname):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, dbname)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    labels = []
    c.execute("SELECT * FROM Musixmatch_Genres")
    for row in c:
        labels.append(row[1])
    genres, counts = np.unique(labels, return_counts= True)
    x = np.arange(len(genres))
    width = .8
    fig, ax = plt.subplots()
    rects = ax.bar(x, counts, width, label='Counts', color='red')
    ax.set_xlabel('Genre')
    ax.set_ylabel('Genre Count')
    ax.set_title('Genre Count for MusixMatch')
    ax.set_xticks(x)
    ax.set_xticklabels(genres)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("MusixMatch_Genres")


def barchart_spotify(dbname):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, dbname)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    labels = []
    c.execute("SELECT * FROM Spotify_Genres")
    for row in c:
        labels.append(row[1])
    genres, counts = np.unique(labels, return_counts= True)
    x = np.arange(len(genres))
    width = .8
    fig, ax = plt.subplots()
    rects = ax.bar(x, counts, width, label='Counts', color='green')
    ax.set_xlabel('Genre')
    ax.set_ylabel('Genre Count')
    ax.set_title('Genre Count for Spotify')
    ax.set_xticks(x)
    ax.set_xticklabels(genres, size = 4)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("Spotify_Genres.pdf")



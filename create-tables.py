import sqlite3


conn = sqlite3.connect("Acorde.db")
sql_create_table_playlists = '''
CREATE TABLE IF NOT EXISTS playlists (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nomes Text);
'''

conn.execute(sql_create_table_playlists)
conn.close  

conn = sqlite3.connect("Acorde.db")
sql_create_table_info = '''
CREATE TABLE IF NOT EXISTS info (
id INTEGER PRIMARY KEY AUTOINCREMENT,
musica Text,
artista Text,
tablatura Text,
letra Text
);
'''
conn.execute(sql_create_table_info) 
conn.close()  

conn = sqlite3.connect("Acorde.db")
sql_create_table_infoplaylists = '''CREATE TABLE IF NOT EXISTS infoplaylists (
id INTEGER PRIMARY KEY AUTOINCREMENT, 
IdPlaylist Text,
IdFaixa Text);'''

conn.execute(sql_create_table_infoplaylists)
conn.close
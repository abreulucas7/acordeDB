import sqlite3

def adicionar_musica(musica, artista, tablatura, letra):
    with sqlite3.connect("Acorde.db") as conn:
        sql_insert_info = '''
        INSERT INTO info (musica, artista, tablatura, letra)
        VALUES (?, ?, ?, ?)
        '''
        cur = conn.execute(sql_insert_info, (musica, artista, tablatura, letra))
        return cur.lastrowid

def listar_musicas():
    with sqlite3.connect("Acorde.db") as conn:
        sql_listar_info = '''
        SELECT id, musica, artista, tablatura, letra
        FROM info
        '''
        cur = conn.cursor()        
        cur.execute(sql_listar_info)        
        return cur.fetchall()


def listar_musicas_com_playlists():
    with sqlite3.connect("Acorde.db") as conn:
        cur = conn.execute(
            """
            SELECT i.id, i.musica, i.artista, i.tablatura, i.letra,
                   GROUP_CONCAT(p.nomes, ', ') AS nomes_playlists
            FROM info i
            LEFT JOIN infoplaylists ip ON CAST(ip.IdFaixa AS INTEGER) = i.id
            LEFT JOIN playlists p ON CAST(ip.IdPlaylist AS INTEGER) = p.id
            GROUP BY i.id, i.musica, i.artista, i.tablatura, i.letra
            ORDER BY i.musica COLLATE NOCASE
            """
        )
        return cur.fetchall()


def listar_playlists():
    with sqlite3.connect("Acorde.db") as conn:
        sql_listar_playlists = '''
        SELECT nomes, id
        FROM playlists
        '''
        cur = conn.cursor()        
        cur.execute(sql_listar_playlists)        
        return cur.fetchall() 
    
def criar_playlist(nomes):
    with sqlite3.connect("Acorde.db") as conn:
        sql_criar_playlist = '''
        INSERT INTO playlists (nomes)
        VALUES (?)
        '''
        conn.execute(sql_criar_playlist, (nomes,))

def obter_playlist(id):
    with sqlite3.connect("Acorde.db") as conn:
        cur = conn.execute(
            "SELECT id, nomes FROM playlists WHERE id = ?",
            (id,),
        )
        return cur.fetchone()


def listar_faixas_da_playlist(id_playlist):
    with sqlite3.connect("Acorde.db") as conn:
        cur = conn.execute(
            """
            SELECT i.id, i.musica, i.artista, i.tablatura, i.letra
            FROM info i
            INNER JOIN infoplaylists ip ON CAST(ip.IdFaixa AS INTEGER) = i.id
            WHERE CAST(ip.IdPlaylist AS INTEGER) = ?
            ORDER BY i.musica COLLATE NOCASE
            """,
            (id_playlist,),
        )
        return cur.fetchall()


def adicionar_faixa_a_playlist(id_playlist, id_faixa):
    ps = str(id_playlist)
    fs = str(id_faixa)
    with sqlite3.connect("Acorde.db") as conn:
        cur = conn.execute(
            "SELECT 1 FROM infoplaylists WHERE IdPlaylist = ? AND IdFaixa = ?",
            (ps, fs),
        )
        if cur.fetchone():
            return False
        conn.execute(
            "INSERT INTO infoplaylists (IdPlaylist, IdFaixa) VALUES (?, ?)",
            (ps, fs),
        )
        return True


def remover_faixa_da_playlist(id_playlist, id_faixa):
    with sqlite3.connect("Acorde.db") as conn:
        conn.execute(
            "DELETE FROM infoplaylists WHERE IdPlaylist = ? AND IdFaixa = ?",
            (str(id_playlist), str(id_faixa)),
        )


def excluir_playlists(id):
    with sqlite3.connect("Acorde.db") as conn:
        conn.execute(
            "DELETE FROM infoplaylists WHERE IdPlaylist = ?",
            (str(id),),
        )
        sql_excluir_playlists = '''
        DELETE FROM playlists
        WHERE id = (?)
        '''
        conn.execute(sql_excluir_playlists, (id,))


def excluir_faixas(id):
    with sqlite3.connect("Acorde.db") as conn:
        conn.execute(
            "DELETE FROM infoplaylists WHERE IdFaixa = ?",
            (str(id),),
        )
        sql_excluir_faixas = '''
        DELETE FROM info
        WHERE id = (?)
        '''
        conn.execute(sql_excluir_faixas, (id,)) 

def seek_musica(id, musica):
    with sqlite3.connect("Acorde.db") as conn:
        sql_seek_musica = '''
        SELECT id,musica
        FROM info
        WHERE musica = (?)
        '''
        conn.execute(sql_seek_musica, (id,musica)) 


import sqlite3

def conectar():
    return sqlite3.connect("Acorde.db")


def adicionar_musica(musica, artista, tablatura, letra):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO info (musica, artista, tablatura, letra)
        VALUES (?, ?, ?, ?)
        """,
        (musica, artista, tablatura, letra),
    )
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id


def listar_musicas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, musica, artista, tablatura, letra
        FROM info
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def listar_musicas_com_playlists():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
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
    rows = cursor.fetchall()
    conn.close()
    return rows


def listar_playlists():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT nomes, id
        FROM playlists
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def criar_playlist(nomes):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO playlists (nomes)
        VALUES (?)
        """,
        (nomes,),
    )
    conn.commit()
    conn.close()


def obter_playlist(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nomes FROM playlists WHERE id = ?",
        (id,),
    )
    row = cursor.fetchone()
    conn.close()
    return row


def obter_faixa(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, musica FROM info WHERE id = ?",
        (id,),
    )
    row = cursor.fetchone()
    conn.close()
    return row


def listar_faixas_da_playlist(id_playlist):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT i.id, i.musica, i.artista, i.tablatura, i.letra
        FROM info i
        INNER JOIN infoplaylists ip ON CAST(ip.IdFaixa AS INTEGER) = i.id
        WHERE CAST(ip.IdPlaylist AS INTEGER) = ?
        ORDER BY i.musica COLLATE NOCASE
        """,
        (id_playlist,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def adicionar_faixa_a_playlist(id_playlist, id_faixa):
    ps = str(id_playlist)
    fs = str(id_faixa)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM infoplaylists WHERE IdPlaylist = ? AND IdFaixa = ?",
        (ps, fs),
    )
    if cursor.fetchone():
        conn.close()
        return False
    cursor.execute(
        "INSERT INTO infoplaylists (IdPlaylist, IdFaixa) VALUES (?, ?)",
        (ps, fs),
    )
    conn.commit()
    conn.close()
    return True


def remover_faixa_da_playlist(id_playlist, id_faixa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM infoplaylists WHERE IdPlaylist = ? AND IdFaixa = ?",
        (str(id_playlist), str(id_faixa)),
    )
    conn.commit()
    conn.close()


def excluir_playlists(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM infoplaylists WHERE IdPlaylist = ?",
        (str(id),),
    )
    cursor.execute(
        """
        DELETE FROM playlists
        WHERE id = (?)
        """,
        (id,),
    )
    conn.commit()
    conn.close()


def excluir_faixas(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM infoplaylists WHERE IdFaixa = ?",
        (str(id),),
    )
    cursor.execute(
        """
        DELETE FROM info
        WHERE id = (?)
        """,
        (id,),
    )
    conn.commit()
    conn.close()

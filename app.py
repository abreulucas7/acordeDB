from flask import Flask, render_template, request, redirect, flash

from secrets import token_hex

import model

import services.service as service

app = Flask(__name__)

app.secret_key = token_hex()

@app.get("/adicionar_musica")
def get_musica():
    listagem_musicas = model.listar_musicas()
    listagem_playlists = model.listar_playlists()
    return render_template(
        "/adicionar_musica.html",
        info=listagem_musicas,
        playlists=listagem_playlists,
        pag_nome="Adicionar Música",
    )


@app.post("/adicionar_musica")
def post_musica():
    musica = request.form["musica"]
    artista = request.form["artista"]
    tablatura = request.form["tablatura"]
    letra = request.form["letra"]
    service.adicionar_musica(musica, artista, tablatura, letra)
    playlist_id = request.form.get("playlist_id", type=int)
    service.obter_playlist(playlist_id, musica, artista, tablatura, letra)
    return redirect("/adicionar_musica") 
  

@app.get("/playlists")
def get_playlists():
    listagem_playlists = model.listar_playlists()
    return render_template("/playlists.html", pl = listagem_playlists, pag_nome = "Playlists")


@app.post("/playlists")
def post_playlists():
    playlistNome = request.form["playlistNome"]
    model.criar_playlist(playlistNome)

    return redirect("/playlists")


@app.get("/playlists/<int:playlist_id>")
def ver_playlist(playlist_id):
    playlist = model.obter_playlist(playlist_id)
    if not playlist:
        flash("Playlist não encontrada.")
        return redirect("/playlists")
    faixas = model.listar_faixas_da_playlist(playlist_id)
    todas = model.listar_musicas()
    ids_na_playlist = {row[0] for row in faixas}
    disponiveis = [m for m in todas if m[0] not in ids_na_playlist]
    return render_template(
        "playlist.html",
        playlist=playlist,
        faixas=faixas,
        disponiveis=disponiveis,
        pag_nome=playlist[1],
    )


@app.get("/reproduzir")
def get_faixa_particular():
    faixa = model.obter_faixa()
    return render_template ("reproduzir.html", faixa = faixa)


@app.post("/playlists/<int:playlist_id>/faixa")
def post_adicionar_faixa_playlist(playlist_id):
    if not model.obter_playlist(playlist_id):
        flash("Playlist não encontrada.")
        return redirect("/playlists")
    faixa_id = request.form.get("faixa_id", type=int)
    if faixa_id is None:
        return redirect(f"/playlists/{playlist_id}")
    if not model.adicionar_faixa_a_playlist(playlist_id, faixa_id):
        flash("Esta música já está na playlist.")
    return redirect(f"/playlists/{playlist_id}")


@app.get("/playlists/<int:playlist_id>/remover/<int:faixa_id>")
def get_remover_faixa_playlist(playlist_id, faixa_id):
    if not model.obter_playlist(playlist_id):
        flash("Playlist não encontrada.")
        return redirect("/playlists")
    model.remover_faixa_da_playlist(playlist_id, faixa_id)
    return redirect(f"/playlists/{playlist_id}")


@app.get("/excluir/playlists/<id>")
def get_excluir_playlist(id):
    model.excluir_playlists(id)
    return redirect("/playlists") 


@app.get("/excluir/faixa/<id>")
def get_excluir_faixa(id):
    model.excluir_faixas(id)
    return redirect("/")


@app.get("/")
def get_faixas():
    faixas = model.listar_musicas_com_playlists()
    return render_template("faixas.html", faixas=faixas, pag_nome = "Faixas") 


@app.get("/interface")
def get_styling():
    return render_template("/interface.html")


if __name__ == '__main__':
    app.run(debug=True)
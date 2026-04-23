from flask import Flask, render_template, request, redirect, flash

from secrets import token_hex


import model

def adicionar_musica(musica, artista, tablatura, letra):
    if musica is not None and artista is not None and tablatura is not None and letra is not None:
        return model.adicionar_musica(musica, artista, tablatura, letra)
    else:
        return False
    
def obter_playlist(playlist_id, musica, artista, tablatura, letra):
    if playlist_id and model.obter_playlist(playlist_id):
        return True 
    else: 
        model.adicionar_faixa_a_playlist(playlist_id, adicionar_musica(musica, artista, tablatura, letra))
        flash("Não foi possível adicionar à playlist (duplicado).")

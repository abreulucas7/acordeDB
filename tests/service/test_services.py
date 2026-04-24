##from unittest.mock import patch
##
##from app import post_musica
##
##@patch("services.service.adicionar_musica")
##class TestAdicionarMusica: 
##    def test_adicionar_musica_com_campos_vazios(self, mock_svc, client):
##        mock_svc.adicionar_musica.return_value =  None
##        resp = client.get("/api/musica")
##        assert resp.status_code == 400
##        body = resp.get_json()
##        assert body ["code"] == "not found"
##
##    def test_adicionar_musica_com_campos_validos(self, mock_svc, client):
##        mock_svc.adicionar_musica.return_value = [ post_musica( muscia = "Nome", artista = "Artista", tablatura = "Tab", letra = "Letra" )]
##        resp = client.get("/api/musica")
##        assert resp.status_code == 200
##        assert resp.get_json() == [ {"muscia" : "Nome", "artista" : "Artista", "tablatura" : "Tab", "letra" : "Letra"},]
##        mock_svc.adicionar_musica.assert_called_once()



# Acorde

Aplicação web simples em **Python (Flask)** para guardar **músicas** (com artista, tablatura e letra), organizá-las em **playlists** e ver tudo em uma **lista de faixas**. Os dados ficam em um banco **SQLite** (`Acorde.db`).

Este documento resume o projeto e descreve, de forma direta, **o que esta branch implementou** para ligar faixas a playlists (telas + backend). As primeiras seções ajudam quem está aprendendo; a parte central foca nas mudanças da branch.

---

## Conceitos rápidos (para quem está aprendendo)

### O que é Flask aqui?

O **servidor** recebe requisições HTTP (por exemplo “mostra a página inicial”) e responde com **HTML** gerado a partir de **templates** (arquivos `.html` com “buracos” que o Python preenche). Não existe uma aplicação React/Vue separada: o “frontend” são essas páginas servidas pelo Flask.

### O que é o banco de dados SQLite?

É um arquivo (`Acorde.db`) onde ficam **tabelas** (como planilhas do Excel relacionadas). O arquivo `create-tables.py` cria as tabelas se ainda não existirem. **Na primeira vez**, ou depois de apagar o banco, execute:

```bash
python create-tables.py
```

### Relação “muitas músicas ↔ muitas playlists”

Uma **música** pode estar em **várias** playlists. Uma **playlist** tem **várias** músicas. Isso é uma relação **muitos-para-muitos** (N:N).

No banco de dados isso não fica “dentro” da tabela `playlists` com uma coluna por música. Em vez disso usa-se uma **tabela de ligação** (às vezes chamada *junction table*):

| Tabela        | Papel |
|---------------|--------|
| `info`        | Cada linha é uma **faixa** (música no catálogo), com `id` único. |
| `playlists`   | Cada linha é uma **playlist**, com `id` e nome. |
| `infoplaylists` | Cada linha diz: “esta faixa (`IdFaixa`) pertence a esta playlist (`IdPlaylist`)”. |

**Exemplo imaginário:**

- Na tabela `info`, a música “Bohemian Rhapsody” tem `id = 5`.
- Na tabela `playlists`, “Rock clássico” tem `id = 2`.
- Na tabela `infoplaylists` existe uma linha: `IdPlaylist = 2`, `IdFaixa = 5`.

Se a mesma música estiver em outra playlist, aparece **outra linha** em `infoplaylists` com outro `IdPlaylist` e o mesmo `IdFaixa`.

> **Nota:** No `create-tables.py` original, `IdPlaylist` e `IdFaixa` estão como `Text`; no código Python guardamos valores como texto (por exemplo `"5"`) para ficarem compatíveis com o esquema. Os `JOIN` usam `CAST(... AS INTEGER)` quando é necessário comparar com os `id` numéricos das outras tabelas.

---

## Como rodar o projeto

### 1. Ambiente Python (recomendado: ambiente virtual)

Na pasta do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate    # no Windows: .venv\Scripts\activate
pip install flask
```

### 2. Criar as tabelas (se ainda não existirem)

```bash
python create-tables.py
```

### 3. Iniciar a aplicação

```bash
python app.py
```

Abra o navegador em **http://127.0.0.1:5000** (ou a URL que o terminal mostrar).

---

## O que foi implementado nesta branch (resumo)

Antes, a tabela `infoplaylists` **já existia** no esquema, mas a aplicação **não gravava nem lia** essas ligações. Nesta branch passamos a usar essa tabela no código, com rotas novas em `app.py`, funções em `model.py` e ajustes nas telas.

O arquivo `create-tables.py` **não ganhou colunas novas**: já existiam `IdFaixa` e `IdPlaylist` em `infoplaylists`.

---

## O que esta branch mudou na tela (só o que importa para faixas ↔ playlists)

A ideia aqui não é explicar Flask ou Jinja do zero — só **o que foi colocado na interface** para o usuário conseguir **colocar faixas em playlists** e **ver isso na lista**.

### 1. Formulário “Adicionar música” (`/adicionar_musica`)

Foi adicionado um **campo em formato de lista suspensa (dropdown)** com o rótulo **Playlist**.

- A **primeira opção** é algo como “só no catálogo, sem playlist” (valor vazio). Se o usuário deixar essa, a música é cadastrada normalmente e **não** entra em nenhuma playlist.
- As **demais opções** são as playlists que já existem no banco: o nome aparece para o usuário, e por baixo dos panos cada opção guarda o **id** da playlist.
- Ao clicar em enviar, o mesmo formulário manda os dados da música **e**, se houver escolha, o **id da playlist**. O servidor primeiro salva a música, pega o **id da faixa nova** e, se tiver playlist escolhida, grava o par playlist + faixa na tabela de ligação.

### 2. Página de uma playlist (`/playlists/<id>` — arquivo `playlist.html`)

Foi criada uma **tela só dessa playlist**. Nela dá para:

- Ver **quais músicas** já estão nela (tabela).
- Usar outro **dropdown** com músicas do catálogo que **ainda não** estão nessa playlist; ao enviar, a faixa **existente** é associada à playlist (útil quando a música já foi cadastrada antes).
- Clicar em **remover da playlist** — isso só tira a música **dessa** playlist, sem apagar a música do catálogo.

### 3. Lista de playlists (`/playlists`)

Cada nome de playlist virou um **link** que abre a página acima (`/playlists/<id>`). Antes o link estava errado na interface.

### 4. Lista de faixas na página inicial (`/`)

Foi adicionada uma **coluna “Playlist”** na tabela: mostra **em quais playlists** aquela faixa aparece (se estiver em mais de uma, os nomes vêm separados por vírgula). Assim dá para conferir de relance sem abrir cada playlist.

---

## Fluxo de utilização (exemplo)

1. Em **Playlists** (`/playlists`), crie “Estudos de guitarra”.
2. Clique no nome da playlist → você vai para `/playlists/3` (o número é o `id` da playlist).
3. Nessa página escolha uma música do catálogo e adicione — fica um registro em `infoplaylists`.
4. Na **página inicial** (`/`), na coluna **Playlist**, essa música pode aparecer como `Estudos de guitarra` (e mais nomes se estiver em várias).

**Ao adicionar música** (`/adicionar_musica`), você pode escolher no dropdown **“Playlist”**. Se escolher uma playlist, depois de inserir a linha em `info`, o programa usa o **novo `id`** da faixa e insere logo a ligação em `infoplaylists`.

---

## Rotas HTTP relevantes (mapa rápido)

| Método | Caminho | O que faz |
|--------|---------|-----------|
| `GET` | `/` | Lista todas as faixas (com coluna de playlists). |
| `GET` / `POST` | `/adicionar_musica` | Formulário e envio de nova música (com playlist opcional). |
| `GET` / `POST` | `/playlists` | Lista playlists e criação de uma nova. |
| `GET` | `/playlists/<id>` | Detalhe da playlist: músicas, adicionar, remover da playlist. |
| `POST` | `/playlists/<id>/faixa` | Adiciona uma faixa existente à playlist (formulário na página da playlist). |
| `GET` | `/playlists/<id>/remover/<faixa_id>` | Remove a faixa **só desta** playlist. |
| `GET` | `/excluir/playlists/<id>` | Apaga a playlist (e ligações em `infoplaylists`). |
| `GET` | `/excluir/faixa/<id>` | Apaga a faixa do catálogo (e ligações em `infoplaylists`). |

Mensagens temporárias (por exemplo “playlist não encontrada”) usam `flash()` do Flask e aparecem nas páginas que tratam disso.

---

## Funções importantes em `model.py` (ideia geral)

| Função | Ideia |
|--------|--------|
| `adicionar_musica(...)` | Insere em `info` e **retorna** `cur.lastrowid` (o `id` da nova faixa). |
| `adicionar_faixa_a_playlist(id_playlist, id_faixa)` | Insere em `infoplaylists` se ainda não existir par igual; retorna `False` se for duplicado. |
| `remover_faixa_da_playlist(...)` | Apaga **só** a linha de ligação. |
| `listar_faixas_da_playlist(id)` | `JOIN` entre `info` e `infoplaylists` para listar músicas dessa playlist. |
| `listar_musicas_com_playlists()` | Lista faixas com `GROUP_CONCAT` dos nomes das playlists (uma coluna extra). |
| `excluir_playlists` / `excluir_faixas` | Além de apagar na tabela principal, limpam `infoplaylists`. |

**Exemplo de ideia do SQL** para “nomes das playlists por música” (simplificado):

```sql
-- Várias playlists na mesma célula, separadas por vírgula
GROUP_CONCAT(p.nomes, ', ')
```

---

## Arquivos mais alterados nesta branch

| Arquivo | Alterações principais |
|---------|------------------------|
| `app.py` | Novas rotas para playlist; uso de `listar_musicas_com_playlists` na `/`; lógica do formulário de adicionar música + playlist. |
| `model.py` | Funções para `infoplaylists`; `adicionar_musica` passa a retornar id; limpeza em cascata ao apagar; listagem com playlists. |
| `templates/playlist.html` | **Novo** — UI da playlist. |
| `templates/playlists.html` | Links corretos para `/playlists/<id>`, mensagens `flash`. |
| `templates/adicionar_musica.html` | Dropdown de playlist, HTML corrigido. |
| `templates/faixas.html` | Coluna **Playlist**. |

---

## Dependências

- **Python 3** com o pacote **Flask** (`pip install flask`).
- O projeto tem também `package.json` (Bootstrap, Sass, VexFlow, etc.) para possíveis evoluções; **para rodar esta app Flask** você só precisa do Flask e do banco criado com `create-tables.py`.

---

## Dicas para estudar o código

1. Siga uma requisição do navegador: comece na rota em `app.py`, veja qual função de `model.py` é chamada e imagine o SQL no banco.
2. Abra o `Acorde.db` com um cliente SQLite (ou extensão no VS Code) e olhe as três tabelas depois de adicionar dados pela web.
3. Experimente apagar uma playlist e verifique se as linhas em `infoplaylists` com esse `IdPlaylist` somem — isso evita registros “órfãos”.

Se algo não funcionar (página em branco, erro 404), confira se você executou `python create-tables.py` e se está na pasta certa ao rodar `python app.py`.

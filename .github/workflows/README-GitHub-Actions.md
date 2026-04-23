# Guia: GitHub Actions neste projeto

Este documento explica **para que o GitHub Actions serve**, como o *pipeline* deste repositório funciona e um **passo a passo** para criar ou replicar a configuração, com o significado de cada parte.

---

## 1. Para que o GitHub Actions serve?

O **GitHub Actions** é a ferramenta de **automação** integrada ao GitHub. Ele permite definir *workflows* (arquivos em YAML) que o GitHub executa em **máquinas na nuvem** quando ocorrem eventos (por exemplo: alguém dá *push* ou abre um *pull request*).

Neste projeto, o objetivo é **integração contínua (CI)**:

- Sempre que o código muda, os **testes unitários** e os **testes E2E** **rodam** (são executados) **automaticamente**.
- As falhas aparecem na aba **Actions** do repositório, **antes** de o código ser integrado na *main*, o que ajuda a:
  - **Detectar** regressões cedo;
  - Garantir que o *app* e o Playwright continuam funcionando no ambiente Linux (parecido com o de muitos servidores/CI);
  - Não depender só de "no meu computador funciona".

**Resumindo:** o GitHub Actions **não substitui** testes manuais na sua máquina, mas **reexecuta** os testes de forma previsível a cada alteração, **para a equipe inteira**.

---

## 2. O que você precisa ter (pré-requisitos)

| Requisito | Observações |
|-----------|------------|
| Repositório no **GitHub** | O arquivo de *workflow* fica no Git, e o GitHub o detecta. |
| Arquivo em **`.github/workflows/<nome>.yml`** | A convenção do GitHub é a pasta **`.github/workflows/`** na **raiz** do repositório. |
| Código e dependências **instaláveis com `pip`** | No CI usamos um único `pip install ...` (sem `requirements.txt`), para alinhar a projetos que só têm o *venv* e instalam pacote a pacote. |
| (Opcional) Arquivo **`pytest.ini`** | Já existe no projeto: define `base_url` e `pythonpath` para os E2E. |

Se **você clonar** outro projeto e quiser o **mesmo tipo de pipeline**, dá para **copiar** a pasta **`.github`** e **ajustar** a linha do `pip install` (e a versão do Python), conforme o que a app e os testes exigem.

*Opcional (boa prática em equipe):* depois dá para criar um `requirements.txt` e trocar o *step* para `pip install -r requirements.txt`, se quiserem versões fixas e *cache* mais previsível.

---

## 3. Estrutura de arquivos relevante

No **FocusFluir** (e em projetos semelhantes) o que costuma importar para o CI é:

```
.
├── .github
│   └── workflows
│       └── ci.yml          # Define o pipeline (quando roda e o que roda)
├── pytest.ini               # Config do pytest (E2E com base_url)
├── app.py                   # App Flask
├── tests/                   # Testes unitários
└── e2e/                     # Testes E2E (Playwright)
```

- O **`ci.yml`** (pode ter outro nome, desde que termine em **`.yml` ou `.yaml`**) contém a “receita” do *pipeline*.

---

## 4. Passo a passo: como isso foi montado (replicar em outro repositório)

### Passo 1: Criar a pasta de *workflows*

1. Na **raiz** do repositório (junto a `app.py` ou `README.md`), crie a sequência de pastas:  
   **`.github`** → **`workflows`**.
2. Crie um arquivo, por exemplo o **`ci.yml`**.

> **Detalhe:** a pasta **`.github`** (com ponto no início) segue a convenção do GitHub, que procura aí os *workflows*.

### Passo 2: Fazer *commit* e *push* para o GitHub

- Trate a pasta **`.github`** como código normal: `git add`, `git commit`, `git push`.
- Depois do *push*, o GitHub **lê** os arquivos em **`.github/workflows/*.yml`** e **registra** o *workflow* na aba **Actions**.

### Passo 3: Abrir a aba *Actions* e acompanhar a execução

1. No repositório no GitHub, abra a aba **Actions**.
2. Escolha o *workflow* (ex.: o nome **definido** em `name: CI` no arquivo).
3. Clique em uma **execução** (*run*) para ver **cada *step***, os *logs* e se passou (verde) ou falhou (vermelho).

Se nada aparecer, confirme se o arquivo está de fato em **`.github/workflows/`** e se você deu *push* na *branch* correta.

### Passo 4: (Opcional) Rodar o *workflow* na mão

Neste repositório o arquivo inclui **`workflow_dispatch`**, o que permite, na interface do GitHub (**Actions** → o *workflow* **CI** → **Run workflow**), disparar uma execução **sem** dar *push*.

---

## 5. Explicação, bloco a bloco (conceitual) do `ci.yml`

A seguir, o que **cada parte** do *workflow* deste projeto **faz** e **por quê**.

### `name: CI`

- Nome amigável que **aparece** na interface do GitHub (na lista de *workflows* e de execuções).

### `on: [push, pull_request, workflow_dispatch]`

- **Quando** o *workflow* roda:
  - **`push`:** alguém envia alterações em qualquer *branch*;
  - **`pull_request`:** alguém abre ou atualiza um PR;
  - **`workflow_dispatch`:** você **pode rodar manualmente** a partir da interface (*UI*).

*Observação:* dá para **restringir** o *disparo* (por exemplo só a *branch* `main`); nesse caso você **troca** esse `on` por regras mais fechadas, conforme a [documentação oficial de `on`](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs).

### `jobs: test: runs-on: ubuntu-latest`

- **Job** = um “trabalho” a ser executado. Aqui existe um *job* chamado **`test`**;
- **`runs-on: ubuntu-latest`:** a máquina virtual é **Ubuntu** recente (padrão em muitos projetos *open source*).

### *Step* **Checkout** (`actions/checkout@v4`)

- Faz o **git clone** do repositório na máquina do *runner*, para o CI ter o código a testar. Sem isso, não haveria arquivos para o `pip` nem para o `pytest`.

### *Step* **Configurar Python** (`actions/setup-python@v5`)

- Instala a versão de **Python** indicada (neste projeto, `3.12`). **Não** usamos `cache: pip` aqui: o `setup-python` só consegue usar *cache* de *pip* se existir `requirements.txt` ou `pyproject.toml` no repositório. Sem esses arquivos, pôr `cache: pip` gera o erro *“No file … matched to requirements.txt or pyproject.toml”*.

### *Step* **Instalar dependências**

- O comando **`pip install flask pytest playwright pytest-playwright`** instala o que o *app* e os testes precisam, **sem** depender de um arquivo `requirements.txt` no repositório (útil quando o fluxo da turma é só *venv* + *pip* manual). Se quiser, no futuro dá para trocar por `pip install -r requirements.txt`.

### *Step* **Testes unitários**

- **`python -m pytest tests/ -v`**
- Roda **só** a pasta **`tests/`** (lógica isolada, geralmente com *mocks*), **sem** *browser* e **sem** servidor de E2E.

### *Step* **Instalar Chromium (Playwright)**

- O Playwright precisa do **binário do *browser***; o comando `playwright install --with-deps chromium` instala o **Chromium** e dependências de sistema no **Linux** (no CI isso é obrigatório; o `pip` sozinho **não** basta).

### *Step* **Preparar BD, subir Flask e E2E**

Esta etapa agrupa vários passos no mesmo *step* de *shell*:

| O que acontece | Por quê |
|----------------|---------|
| `set -e` | Se um comando falhar, o *script* interrompe (não continua em estado errado). |
| `rm -f focusfluir.db` | Começa com banco de dados **limpo** no *runner* (sem *lixo* de outra execução). |
| *Python* com `setup_database()` | Cria o *schema* SQLite (tabelas vazias), como no primeiro *run* local. O E2E `test_playlist_criar` cria a *playlist* pelo *browser*; **não** é necessário inserir dados no `ci.yml`. |
| `app.run(...)` em *background* com `&` | O Playwright acessa `http://127.0.0.1:5000` (como no `pytest.ini`); o *app* **precisa** estar de pé. |
| `sleep 3` após subir o Flask em *background* | Pausa curta para o servidor **começar a escutar** a porta **antes** do `pytest` E2E. Versão simples para aprender; em *pipelines* mais exigentes costuma-se usar *health check* (ex. `curl` em *loop* ou `wait-on`). |
| `python -m pytest e2e/ -v` | Roda **apenas** os arquivos em `e2e/`, com o *plugin* do Playwright (fixture `page`, `base_url`, etc.). |

---

## 6. Arquivos fora do *workflow*, mas essenciais do mesmo jeito

| Arquivo / comando | Papel no CI |
|---------|------------|
| **`pip install flask pytest playwright pytest-playwright` no *workflow*** | Garante os mesmos pacotes que a app e o pytest E2E importam, sem `requirements.txt`. |
| **`pytest.ini`** | Ajusta o *path* do Python e a **`base_url`** dos E2E (URL base `http://127.0.0.1:5000`). |
| **Testes E2E** (ex. `e2e/test_*.py`) | Usam `playwright` e, nessa configuração, o *app* levantado no *pipeline*. |

---

## 7. Dicas e problemas comuns

- **Falha ao instalar *browsers*:** confira se a linha com `playwright install --with-deps chromium` está presente; no **Linux** do GitHub, `--with-deps` cobre boa parte das dependências de sistema;
- **E2E com “connection refused”:** o Flask **não** subiu a tempo; tente **aumentar o `sleep`** (ex. de `3` para `5` segundos) ou, em projetos críticos, trocar por um *loop* com `curl` até a URL responder;
- **E2E que acessam a internet (ex.: YouTube):** o *runner* do GitHub **tem** rede, mas *APIs* externas podem ficar lentas ou indisponíveis; aí dá para **refinar o teste** ou usar *mock* no futuro;
- **Mudar a versão do Python:** ajuste **`python-version:`** no *step* `actions/setup-python` e, quando possível, alinhe com a versão que **você** usa no desenvolvimento.

---

## 8. Onde aprender mais (oficial)

- [GitHub Actions — documentação](https://docs.github.com/en/actions)  
- [Sintaxe do *workflow* (YAML)](https://docs.github.com/en/actions/writing-workflows)  
- [Arquivo de *workflow*: `on`, `jobs`, `steps`, `uses`, `run`](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does)

Com isso, você fica com o **contexto** (para quê o Actions), a **montagem** do arquivo no repositório e a **leitura** de cada *step* concreto deste *pipeline*.
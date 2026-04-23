
from playwright.sync_api import Page, expect 

#Sempre se usa (page: Page)
def test_home(page: Page):
    page.goto("/") #goto vai para a página especificada entre os parenteses ("/")
    #page.pause(); #pause congela a página  

def test_faixas(page: Page):
    page.goto("/")

def test_playlists(page: Page):
    page.goto("/playlists")
    page.get_by_role("link", name="Nova").click()

def test_home_button(page: Page):
    page.goto("/adicionar_musica")
    page.get_by_role("button", name="add").click
    expect(page).to_have_title("Adicionar Música")  

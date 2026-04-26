from bs4 import BeautifulSoup
import requests 

url = "https://www.letras.mus.br/darren-korb/coral-crown/"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

html = soup.find('div', class_ ="lyric-original")

letra = str(html)

print(type(html))
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def get_imoveis_urls():
    """
    Obtém as URLs de todos os imóveis da cidade de João Pessoa.

    Returns:
        list: Uma lista com as URLs de todos os imóveis.
    """
    imoveis_urls = []
    page = 1
    while True:
        url = f"https://www.orulo.com.br/buildings?map_sw_lat=-7.38160252972348&map_sw_lng=-35.244709276314666&map_ne_lat=-6.830226988194283&map_ne_lng=-34.52622672368301&page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        imoveis = soup.find_all("div", class_="building-card__image")
        if not imoveis:
            break
        for imovel in imoveis:
            imoveis_urls.append("https://www.orulo.com.br" + imovel.find("a")["href"])
        page += 1
    return imoveis_urls

def get_imovel_data(url):
    """
    Obtém os dados de um imóvel.

    Args:
        url (str): A URL do imóvel.

    Returns:
        dict: Um dicionário com os dados do imóvel.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    dados = {}

    # Extrai o título
    titulo = soup.find("h1", class_="building-header__title")
    dados["titulo"] = titulo.text.strip() if titulo else None

    # Extrai o endereço
    endereco = soup.find("p", class_="building-header__address")
    dados["endereco"] = endereco.text.strip() if endereco else None

    # Extrai o preço
    preco = soup.find("p", class_="building-pricing__value")
    dados["preco"] = preco.text.strip() if preco else None

    # Extrai a área
    area = soup.find("p", text="Área")
    if area:
        dados["area"] = area.find_next_sibling("p").text.strip()
    else:
        dados["area"] = None

    # Extrai o número de quartos
    quartos = soup.find("p", text="Quartos")
    if quartos:
        dados["quartos"] = quartos.find_next_sibling("p").text.strip()
    else:
        dados["quartos"] = None

    return dados

def main():
    """
    Função principal do script.
    """
    imoveis_urls = get_imoveis_urls()
    imoveis_data = []
    for url in imoveis_urls:
        imoveis_data.append(get_imovel_data(url))

    # Salva os dados em formato JSON
    with open("imoveis.json", "w", encoding="utf-8") as f:
        json.dump(imoveis_data, f, ensure_ascii=False, indent=4)

    # Salva os dados em formato CSV
    df = pd.DataFrame(imoveis_data)
    df.to_csv("imoveis.csv", index=False)

if __name__ == "__main__":
    main()

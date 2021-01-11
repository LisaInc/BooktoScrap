"""Module avec toutes les fonctions."""

import csv
from bs4 import BeautifulSoup
import requests
import re

import Livre


def get_url_book(url):
    """Retourne la liste des url de chaque livre d'une caté."""
    urlliste = []
    request = requests.get(url)
    html = request.content
    soup = BeautifulSoup(html, features="html.parser")
    for link in soup.find_all("a"):  # cibler
        book_urls = re.findall("^\.\.\/\.\.\/\.\.\/\w+.*$", link.get("href"))
        if book_urls:
            url = book_urls[0].replace("../../../", "/")
            url = f"http://books.toscrape.com/catalogue/{url}"
            urlliste.append(url)
    return urlliste


def scrap_livre(url):
    """Avec l'url du livre, extrait toutes les infos."""
    request = requests.get(url)
    html = request.content
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text()
    text = text.replace("\n", " ")
    return text


def tri_info(text, url):
    """Trie les informations, et les met dans une liste."""
    livre = Livre.Livre()
    # titre
    m = re.findall(r"^.+\|", text)
    livre.titre = m[0].replace("  ", "").replace("|", "")

    # description
    m = re.findall("Product Description .*Product Information", text)
    if m != []:
        livre.product_description = (
            m[0]
            .replace("Product Description ", "")
            .replace("...more", "")
            .replace("Product Information", "")
        )
    else:
        livre.product_description = "Sans description"

    # UPC
    m = re.findall("UPC.* Product TypeBooks", text)
    livre.upc = m[0].replace("UPC", "").replace(" Product TypeBooks", "")

    # prix avec taxe
    m = re.findall("incl. tax\).*Tax", text)
    livre.price_including_tax = m[0].replace("incl. tax)", "").replace(" Tax", "")

    # prix sans taxe
    m = re.findall("excl. tax\).* Price", text)
    livre.price_excluding_tax = m[0].replace("excl. tax)", "").replace("  Price", "")

    # stock
    m = re.findall("Availability .*   Number", text)
    livre.stock = m[0].replace("Availability ", "").replace("   Number", "")

    # etoiles

    # image

    return livre


def export(livre):
    """Export les donnees dans csv."""
    with open("eggs.csv", "w", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        writer.writerows(livre)

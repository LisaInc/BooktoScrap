"""Module avec toutes les fonctions."""

import csv
from bs4 import BeautifulSoup
import requests

import book


def get_url_categories(url):
    """Retrun a list of the categories's urls."""
    urls = []
    request = requests.get(url)
    html = request.content
    soup = BeautifulSoup(html, features="html.parser")
    soup_category = soup.find("ul", "nav nav-list")
    soup_category = soup_category.find_all("li")
    for i in soup_category:
        urls.append(i.a["href"])
    return urls


def get_url_books(url):
    """Retrun a list of the books's urls of 1 category."""
    urls_books = []
    request = requests.get(url)
    html = request.content
    soup = BeautifulSoup(html, features="html.parser")
    soup_books = soup.find_all("article", "product_pod")
    for i in soup_books:
        url = i.a["href"].replace("../", "")
        urls_books.append(url)
    return urls_books


def scrap_book(url):
    """Avec l'url du book, extrait toutes les infos."""
    request = requests.get(url)
    html = request.content
    soup = BeautifulSoup(html, features="html.parser")

    one_book = book.book()

    # title
    title = soup.find("title").get_text()
    title = title.replace("| Books to Scrape - Sandbox", "")
    one_book.title = title

    # description
    description = soup.find(attrs={"name": "description"})

    if description:
        one_book.description = (
            str(description)
            .replace('<meta content="\n', "")
            .replace('\n" name="description"/>', "")
        )
    else:
        one_book.product_description = "Sans description"

    # UPC

    # prix avec taxe

    # prix sans taxe

    # stock

    # etoiles

    # image
    # image = soup.find("div", "item active")  # .a("href")
    # print(image)
    return one_book


def export(book):
    """Export les donnees dans csv."""
    with open("eggs.csv", "w", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        writer.writerows(book)

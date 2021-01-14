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

    b = book.book()

    # title
    title = soup.find("title").get_text()
    title = title.replace("| Books to Scrape - Sandbox", "")
    b.title = title

    # description
    description = soup.find(attrs={"name": "description"})

    if description:
        b.description = (
            str(description)
            .replace('<meta content="\n', "")
            .replace('\n" name="description"/>', "")
        )
    else:
        b.product_description = "Sans description"

    table = soup.find("table", {"class": "table table-striped"})
    for row in table.find_all("tr"):
        th = row.find("th").get_text()
        td = row.find("td").get_text()
        # UPC
        if "UPC" in th:
            b.upc = td
        # price without tax
        if "Price (excl. tax)" in th:
            b.price_excluding_tax = td
        # price with tax
        if "Price (incl. tax)" in th:
            b.price_including_tax = td
        # stock
        if "Availability" in th:
            b.stock = td

    # rating

    # image
    # image = soup.find("div", "item active")  # .a("href")

    return b


def export(book):
    """Export les donnees dans csv."""
    with open("eggs.csv", "w", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        writer.writerows(book)

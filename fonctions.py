"""Module avec toutes les fonctions."""

import csv
from bs4 import BeautifulSoup
import requests
import subprocess

import book


def get_url_categories(url):
    """Retrun a list of the categories's urls."""
    urls = []
    request = requests.get(url)
    html = request.content
    soup = BeautifulSoup(html, features="html.parser")
    soup_category = soup.find("ul", "nav nav-list").ul
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

    category = soup.find("h1").get_text()

    for i in soup_books:
        url_book = i.a["href"].replace("../", "")
        urls_books.append(url_book)

    next_page = soup.find("li", "next")
    url = url.replace("index.html", "")
    while next_page:
        url_next_page = url + next_page.a["href"]
        print(url_next_page)
        request = requests.get(url_next_page)
        html = request.content
        soup = BeautifulSoup(html, features="html.parser")
        soup_books = soup.find_all("article", "product_pod")
        for i in soup_books:
            url_book = i.a["href"].replace("../", "")
            urls_books.append(url_book)
        next_page = soup.find("li", "next")

    return urls_books, category


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
    rate = soup.find("p", {"class": "star-rating"})
    b.rating = str(rate).split("\n")[0]
    b.rating = b.rating.replace('<p class="star-rating ', "").replace('">', "")
    # image
    image_link = soup.img["src"]
    url = "http://books.toscrape.com/"
    image_link = url + image_link.replace("../", "")
    b.image_url = image_link
    # cmd = ["wget", "-P image", image_link]
    # subprocess.Popen(cmd).communicate()
    return b


def export(b):
    """Export les donnees dans csv."""
    with open("data.csv", "w", newline="") as csvfile:
        fieldnames = [
            "title",
            "url",
            "upc",
            "price_including_tax",
            "price_excluding_tax",
            "description",
            "category",
            "stock",
            "rating",
            "image_url",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in b:
            writer.writerow(vars(i))

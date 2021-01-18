"""main module."""

import fonctions


def main():
    """Main fonction."""
    url = "http://books.toscrape.com"
    books = []
    urls_category = fonctions.get_url_categories(url)
    for url_category in urls_category:
        url = f"http://books.toscrape.com/{url_category}"
        print(url)
        urls_book, category = fonctions.get_url_books(url)
        for url_book in urls_book:
            url_book = f"http://books.toscrape.com/catalogue/{url_book}"
            book = fonctions.scrap_book(url_book)
            book.category = category
            books.append(book)
        fonctions.export(books, category)


if __name__ == "__main__":
    main()

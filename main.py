"""main module."""

import fonctions


def main():
    """Main fonction."""
    url = "http://books.toscrape.com"

    urls_category = fonctions.get_url_categories(url)
    for url_category in urls_category:
        url = f"http://books.toscrape.com/{url_category}"
        print(url)
        urls_book = fonctions.get_url_books(url)
        for url_book in urls_book:
            url_book = f"http://books.toscrape.com/{url_book}"
            print(url_book)


if __name__ == "__main__":
    main()

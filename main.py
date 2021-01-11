"""main module."""


import donnees
import fonctions

for i, category in enumerate(donnees.category, start=2):
    for j in range(10):
        if j == 1:
            url = f"http://books.toscrape.com/catalogue/category/books/{category}_{i}"
        else:
            url = (
                f"http://books.toscrape.com/catalogue/category/books/{category}_{i}"
                + category
                + "_"
                + str(i)
                + "/page-"
                + str(j)
                + ".html"
            )
        urlliste = fonctions.get_url_book(url)
        for url in urlliste:
            text = fonctions.scrap_livre(url)

            livre = fonctions.tri_info(text, url)
            livre.category = category
            livre.url = url
            print(
                livre.titre
                # + "\n"
                # + livre.upc
                # + "\n"
                # + livre.url
                # + "\n"
                # + livre.price_excluding_tax
                # + "\n"
                # + livre.price_including_tax
                + "\n"
                + livre.category
                + "\n"
                # + livre.stock
                # + "\n"
                # + livre.product_description
                # + "\n"
            )

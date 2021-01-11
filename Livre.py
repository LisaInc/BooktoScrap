"""Class livre."""


class Livre:
    """
    Classe definissant un livre.

    ->  url,
        upc,
        title,
        price_including_tax,
        price_excluding_tax,
        stock,
        product_description,
        category,
        review_rating,
        image_url.
    """

    def __init__(self):
        """Tout les attribut du livre."""
        self.titre = ""
        self.url = ""
        self.upc = ""
        self.price_including_tax = ""
        self.price_excluding_tax = ""
        self.product_description = ""
        self.category = ""
        self.stock = ""
        self.review_rating = ""
        self.image_url = ""

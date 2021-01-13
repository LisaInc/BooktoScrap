"""Class book."""


class book:
    """
    Class of a book.

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
        self.title = ""
        self.url = ""
        self.upc = ""
        self.price_including_tax = ""
        self.price_excluding_tax = ""
        self.description = ""
        self.category = ""
        self.stock = ""
        self.review_rating = ""
        self.image_url = ""

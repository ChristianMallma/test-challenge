from .entity import Product


class ProductRepositoryAbstract:

    def save(self, product: Product):
        pass

    def get_product_by_id(self, product_id):
        pass

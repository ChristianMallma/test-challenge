from store.domain.product.entity import ProductID, Product


def register_product(name,
                     status,
                     stock,
                     description,
                     price):
    _product_id = ProductID.generate()

    _name = name
    _status = status
    _stock = stock
    _description = description
    _price = price

    product = Product(_product_id=_product_id,
                      _name=_name,
                      _status=_status,
                      _stock=_stock,
                      _description=_description,
                      _price=_price)

    product.calculate_created_at()

    return product

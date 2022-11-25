from CQRS.cqrs import CQRSAbstract
from store.domain.product.entity import Product
from store.domain.product.factory import register_product


def save_product(cqrs: CQRSAbstract, product: Product):
    with cqrs.storage:
        cqrs.storage.products.save(product=product)
        cqrs.storage.commit()


def insert_new_product(cqrs: CQRSAbstract,
                       name: str,
                       status: bool,
                       stock: int,
                       description: str,
                       price: float):
    product = register_product(name=name,
                               status=status,
                               stock=stock,
                               description=description,
                               price=price)

    save_product(cqrs=cqrs, product=product)

    return product


def update_product_by_id(cqrs: CQRSAbstract,
                         product_id: str,
                         name: str = None,
                         status: bool = None,
                         stock: int = None,
                         description: str = None,
                         price: float = None):
    product = get_product_by_id(cqrs=cqrs,
                                product_id=product_id)

    if name is not None:
        product.update_name(new_name=name)

    if status is not None:
        product.update_status(new_status=status)

    if stock is not None:
        product.update_stock(new_stock=stock)

    if description is not None:
        product.update_description(new_description=description)

    if price is not None:
        product.update_price(new_price=price)

    product.calculate_updated_at()

    save_product(cqrs=cqrs, product=product)

    return product


def get_product_by_id(cqrs: CQRSAbstract, product_id):
    with cqrs.storage:
        product_object = cqrs.storage.products.get_product_by_id(product_id=product_id)

    return product_object

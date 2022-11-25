from store.domain.product.entity import Product, ProductID
from store.domain.product.repository import ProductRepositoryAbstract
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, ForeignKey, Time, Float, Integer
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

Base = declarative_base()


class ProductAdapter(Base):
    __tablename__ = "Product"
    id = Column("id", UUID, primary_key=True, nullable=False)
    name = Column("name", String(256))
    status = Column("status", Boolean)
    stock = Column("stock", Integer)
    description = Column("description", String(256))
    price = Column("price", Float)
    created = Column("created", TIMESTAMP)
    updated = Column("updated", TIMESTAMP)


class Repository(ProductRepositoryAbstract):

    def __init__(self, session: Session):
        self.session = session

    def save(self, product: Product):

        if not isinstance(product, Product):
            raise ValueError("The object to save must be a product object")

        uuid = product.product_id.id

        product_adapters = self.session.query(ProductAdapter).filter(ProductAdapter.id == uuid).all()
        if not product_adapters:
            self.__insert(product)

        else:
            tmp = product_adapters.pop()
            self.__update(tmp, product)

    def __insert(self, product: Product):
        product_adapter = ProductAdapter()

        product_adapter.id = product.product_id.id
        product_adapter.name = product.name
        product_adapter.status = product.status
        product_adapter.stock = product.stock
        product_adapter.description = product.description
        product_adapter.price = product.price
        product_adapter.created = product.created_at
        product_adapter.updated = product.updated_at

        self.session.add(product_adapter)

    def __update(self, product_adapter: ProductAdapter, product: Product):
        product_adapter.id = product.product_id.id
        product_adapter.name = product.name
        product_adapter.status = product.status
        product_adapter.stock = product.stock
        product_adapter.description = product.description
        product_adapter.price = product.price
        product_adapter.updated = product.updated_at

        self.session.commit()

    def get_product_by_id(self, product_id):
        product_adapters = self.session.query(ProductAdapter).filter(ProductAdapter.id == product_id).all()

        product_object = None
        if len(product_adapters) > 0:
            product_object = self.__retrieve_product(product_adapter=product_adapters[0])

        return product_object

    @staticmethod
    def __retrieve_product(product_adapter: ProductAdapter) -> Product:

        _product_id = ProductID(product_adapter.id)
        _name = product_adapter.name
        _status = product_adapter.status
        _stock = product_adapter.stock
        _description = product_adapter.description
        _price = product_adapter.price

        created = product_adapter.created
        _created = created.strftime("%Y/%m/%d").replace('/', '-')

        updated = product_adapter.updated
        _updated = updated.strftime("%Y/%m/%d").replace('/', '-')

        product = Product(_product_id=_product_id,
                          _name=_name,
                          _status=_status,
                          _stock=_stock,
                          _description=_description,
                          _price=_price,
                          created_at=_created,
                          updated_at=_updated)

        return product

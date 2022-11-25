from dataclasses import dataclass
from store.common.entity import Entity, EntityID


@dataclass(frozen=True)
class ProductID(EntityID):
    pass


@dataclass
class Product(Entity):
    """
    Product entity model
    """
    _product_id: ProductID = ProductID()
    _name: str = None
    _status: bool = True
    _stock: int = None
    _description: str = None
    _price: float = 0.0

    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @property
    def stock(self):
        return self._stock

    @property
    def description(self):
        return self._description

    @property
    def price(self):
        return self._price

    @property
    def created(self):
        return self.created_at

    @property
    def updated(self):
        return self.updated_at

    def to_dict(self):
        return {
            "product_id": self.product_id.id,
            "name": self.name,
            "status": self.status,
            "stock": self.stock,
            "description": self.description,
            "price": self.price,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    # To Update
    def update_name(self, new_name=None):
        self._name = new_name

    def update_status(self, new_status=None):
        self._status = new_status

    def update_stock(self, new_stock=None):
        self._stock = new_stock

    def update_description(self, new_description=None):
        self._description = new_description

    def update_price(self, new_price=None):
        self._price = new_price

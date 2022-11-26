import unittest
import random

from CQRS.cqrs import default_sqlalchemy_session_factory
from store.domain.product.factory import register_product
from store.repositories import product
from faker import Faker

fake_data = Faker()


class TestProductSqlalchemyRepository(unittest.TestCase):
    def setUp(self):
        self.session = default_sqlalchemy_session_factory()
        self.product_repo = product.sqlalchemy.Repository(session=self.session)

        self.name = fake_data.name()
        self.status = fake_data.boolean()
        self.stock = random.randrange(10, 100, 10)
        self.description = fake_data.text()
        self.price = random.randrange(50, 200, 10)

    def tearDown(self):
        self.session.close()

    def test_insert_new_product(self):
        product_object = register_product(name=self.name,
                                          status=self.status,
                                          stock=self.stock,
                                          description=self.description,
                                          price=self.price)

        self.product_repo.save(product=product_object)

        product_id = product_object.product_id.id
        product_loaded = self.product_repo.get_product_by_id(product_id=product_id)

        self.assertEqual(product_object.product_id.id, product_loaded.product_id.id)
        self.assertEqual(product_object.name, product_loaded.name)
        self.assertEqual(product_object.status, product_loaded.status)
        self.assertEqual(product_object.stock, product_loaded.stock)
        self.assertEqual(product_object.description, product_loaded.description)
        self.assertEqual(product_object.price, product_loaded.price)

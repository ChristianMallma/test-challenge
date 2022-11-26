import unittest
import random

from faker import Faker
from store.domain.product.factory import register_product

fake_data = Faker()


class TestProductEntity(unittest.TestCase):
    def setUp(self):
        self.name = fake_data.name()
        self.status = fake_data.boolean()
        self.stock = random.randrange(10, 100, 10)
        self.description = fake_data.text()
        self.price = random.randrange(50, 200, 10)

    def test_factory_function(self):
        product = register_product(name=self.name,
                                   status=self.status,
                                   stock=self.stock,
                                   description=self.description,
                                   price=self.price)

        self.assertEqual(product.name, self.name)
        self.assertEqual(product.status, self.status)
        self.assertEqual(product.stock, self.stock)
        self.assertEqual(product.description, self.description)
        self.assertEqual(product.price, self.price)

        return product

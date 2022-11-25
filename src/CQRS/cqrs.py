from abc import ABC, abstractmethod
from store.domain.product.repository import ProductRepositoryAbstract
from store.repositories import product
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE


db = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(user=POSTGRES_USER,
                                                                password=POSTGRES_PASSWORD,
                                                                host=POSTGRES_HOST,
                                                                port=POSTGRES_PORT,
                                                                db=POSTGRES_DATABASE)

engine = create_engine(db, pool_size=100, max_overflow=100, pool_use_lifo=True, pool_pre_ping=True)
default_sqlalchemy_session_factory = sessionmaker(engine, twophase=False)


class UnitOfWorkAbstract(ABC):
    products: ProductRepositoryAbstract

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        """"
        Persist changes in the repository
        """
        pass

    @abstractmethod
    def rollback(self):
        """
        Avoid write in the repository if something fail
        """
        pass


class CQRSAbstract(ABC):
    storage: UnitOfWorkAbstract


class UnitOfWorkPostgres(UnitOfWorkAbstract):

    def __init__(self, session_factory=default_sqlalchemy_session_factory):
        self.session_factory = scoped_session(session_factory)
        self.session = None

    def __enter__(self):
        self.session = self.session_factory
        self.products = product.sqlalchemy.Repository(session=self.session)

    def __exit__(self, *args):
        super().__exit__()
        self.session.remove()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class CQRS(CQRSAbstract):
    def __init__(self):
        self.storage = UnitOfWorkPostgres()


cqrs = CQRS()

import requests
import time

from functools import lru_cache, wraps
from fastapi.routing import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

from settings import SLEEP_PROCESS, TIME_IN_CACHE
from store.entrypoints.schemas.products import RegisterProductSchema, UpdateProductSchema
from store.services.products import insert_new_product, get_product_by_id, update_product_by_id
from CQRS.cqrs import cqrs


router = APIRouter()


def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


@timed_lru_cache(TIME_IN_CACHE)
def get_status_name(status: bool):
    time.sleep(SLEEP_PROCESS)  # Simulate processing time
    if status:
        return 'Active'
    return 'Inactive'


@router.post("/insert_product/", tags=['Products'])
async def insert_product(product: RegisterProductSchema):
    try:
        product_object = insert_new_product(cqrs=cqrs,
                                            name=product.name,
                                            status=product.status,
                                            stock=product.stock,
                                            description=product.description,
                                            price=product.price)

        return JSONResponse(content=product_object.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/get_product/", tags=['Products'])
async def get_product(product_id: str):
    try:
        product_object = get_product_by_id(cqrs=cqrs,
                                           product_id=product_id)
        product_dict = product_object.to_dict()

        response = requests.get('https://www.randomnumberapi.com/api/v1.0/random?min=1&max=100&count=1')
        discount = response.json()[0]

        product_dict['discount'] = discount
        product_dict['final_price'] = product_dict['price'] * (100 - discount) / 100

        status_name = get_status_name(status=product_dict['status'])
        product_dict['status_name'] = status_name

        return JSONResponse(content=product_dict)
    except Exception:
        raise HTTPException(status_code=404, detail="Producto no encontrado")


@router.put("/update_product/{product_id}", tags=['Products'])
async def update_product(product_id: str, product: UpdateProductSchema):
    try:
        product_object = update_product_by_id(cqrs=cqrs,
                                              product_id=product_id,
                                              name=product.name,
                                              status=product.status,
                                              stock=product.stock,
                                              description=product.description,
                                              price=product.price)

        return JSONResponse(content=product_object.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

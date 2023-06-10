from typing import List, Optional
from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel, Field, EmailStr, ValidationError

DATABASE_URL = 'sqlite:///online_store.db'
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table('users',
                         metadata,
                         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column('first_name', sqlalchemy.String()),
                         sqlalchemy.Column('last_name', sqlalchemy.String()),
                         sqlalchemy.Column('email', sqlalchemy.String()),
                         sqlalchemy.Column('password', sqlalchemy.String())
                         )

products = sqlalchemy.Table('products',
                            metadata,
                            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column('name', sqlalchemy.String()),
                            sqlalchemy.Column('description', sqlalchemy.String()),
                            sqlalchemy.Column('price', sqlalchemy.Float())
                            )

orders = sqlalchemy.Table('orders',
                          metadata,
                          sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("id_user", sqlalchemy.ForeignKey(users.c.id)),
                          sqlalchemy.Column("id_product", sqlalchemy.ForeignKey(products.c.id)),
                          sqlalchemy.Column("order_date", sqlalchemy.String()),
                          sqlalchemy.Column("is_active", sqlalchemy.String())
                          )

metadata.create_all(engine)


class User(BaseModel):
    id: int = Field(..., alias='user_id')
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(min_length=2)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)


class UserIn(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(min_length=2)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)


class Product(BaseModel):
    id: int = Field(..., alias='product_id')
    name: str = Field(..., max_length=32)
    description: str = Field(max_length=200)
    price: float = Field(...)


class ProductIn(BaseModel):
    name: str = Field(..., max_length=32)
    description: str = Field(max_length=200)
    price: float = Field(...)


class Order(BaseModel):
    id: int = Field(..., alias='order_id')
    id_user: int = Field(...)
    id_product: int = Field(...)
    order_date: Optional[str] = Field("YYYY-MM-DD")
    is_active: bool = Field(default=True)


class OrderIn(BaseModel):
    id_user: int = Field(...)
    id_product: int = Field(...)
    order_date: Optional[str] = Field("YYYY-MM-DD")
    is_active: bool = Field(default=True)


app = FastAPI()


# @app.get('/fake_users/{count}')
# async def create_note(count: int):
#     for i in range(count):
#         query = users.insert().values(first_name=f'first_name_{i}', last_name=f'last_name{i}',
#                                       email=f'user{i}@example.ru', password=f'password{i}')
#         await database.execute(query)
#     return {'message': f'{count} fake users created'}
#
#
# @app.get('/fake_products/{count}')
# async def create_note(count: int):
#     for i in range(count):
#         query = products.insert().values(name=f'name_{i}', description=f'description{i}', price=f'12{i}.99')
#         await database.execute(query)
#     return {'message': f'{count} fake products created'}
#
#
# @app.get('/fake_orders/{count}')
# async def create_note(count: int):
#     for i in range(count):
#         query = orders.insert().values(id_user=i, id_product=i, order_date=f'200{i}-{i}-{i}', is_active=True)
#         await database.execute(query)
#     return {'message': f'{count} fake orders created'}


@app.get('/users/', response_model=List[UserIn])
async def read_users():
    try:
        query = users.select()
        return await database.fetch_all(query)
    except ValidationError as e:
        print(e.json())


@app.get('/products/', response_model=List[ProductIn])
async def read_products():
    try:
        query = products.select()
        return await database.fetch_all(query)
    except ValidationError as e:
        print(e.json())


@app.get('/orders/', response_model=List[OrderIn])
async def read_orders():
    try:
        query = orders.select()
        return await database.fetch_all(query)
    except ValidationError as e:
        print(e.json())


@app.get('/user/{user_id}', response_model=UserIn)
async def read_user(user_id: int):
    try:
        query = users.select().where(users.c.id == user_id)
        return await database.fetch_one(query)
    except ValidationError as e:
        print(e.json())


@app.get('/product/{product_id}', response_model=ProductIn)
async def read_product(product_id: int):
    try:
        query = products.select().where(products.c.id == product_id)
        return await database.fetch_one(query)
    except ValidationError as e:
        print(e.json())


@app.get('/order/{order_id}', response_model=OrderIn)
async def read_order(order_id: int):
    try:
        query = orders.select().where(orders.c.id == order_id)
        return await database.fetch_one(query)
    except ValidationError as e:
        print(e.json())


@app.post('/user/', response_model=UserIn)
async def create_user(user: UserIn):
    try:
        query = users.insert().values(first_name=user.first_name, last_name=user.last_name,
                                      email=user.email, password=user.password)
        last_record_id = await database.execute(query)
        return {**user.dict(), 'id': last_record_id}
    except ValidationError as e:
        print(e.json())


@app.post('/product/', response_model=ProductIn)
async def create_product(product: ProductIn):
    try:
        query = products.insert().values(name=product.name, description=product.description, price=product.price)
        last_record_id = await database.execute(query)
        return {**product.dict(), 'id': last_record_id}
    except ValidationError as e:
        print(e.json())


@app.post('/order/', response_model=OrderIn)
async def create_order(order: OrderIn):
    try:
        query = orders.insert().values(id_user=order.id_user, id_product=order.id_product, order_date=order.order_date,
                                       is_active=order.is_active)
        last_record_id = await database.execute(query)
        return {**order.dict(), 'id': last_record_id}
    except ValidationError as e:
        print(e.json())


@app.put('/user/{user_id', response_model=UserIn)
async def update_user(user_id: int, new_user: UserIn):
    try:
        query = users.update().where(users.c.id == user_id).values(**new_user.dict())
        await database.execute(query)
        return {**new_user.dict(), 'id': user_id}
    except ValidationError as e:
        print(e.json())


@app.put('/product/{product_id', response_model=ProductIn)
async def update_product(product_id: int, new_product: ProductIn):
    try:
        query = products.update().where(products.c.id == product_id).values(**new_product.dict())
        await database.execute(query)
        return {**new_product.dict(), 'id': product_id}
    except ValidationError as e:
        print(e.json())


@app.put('/order/{order_id', response_model=OrderIn)
async def update_order(order_id: int, new_order: OrderIn):
    try:
        query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
        await database.execute(query)
        return {**new_order.dict(), 'id': order_id}
    except ValidationError as e:
        print(e.json())


@app.delete('/delete_user/{user_id}')
async def delete_user(user_id: int):
    try:
        query = users.delete().where(users.c.id == user_id)
        await database.execute(query)
        return {'message': 'User deleted'}
    except ValidationError as e:
        print(e.json())


@app.delete('/delete_product/{product_id}')
async def delete_product(product_id: int):
    try:
        query = products.delete().where(products.c.id == product_id)
        await database.execute(query)
        return {'message': 'Product deleted'}
    except ValidationError as e:
        print(e.json())


@app.delete('/delete_order/{order_id}')
async def delete_order(order_id: int):
    try:
        query = orders.delete().where(orders.c.id == order_id)
        await database.execute(query)
        return {'message': 'Order deleted'}
    except ValidationError as e:
        print(e.json())

from typing import List, Optional
from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel, Field, EmailStr


DATABASE_URL = 'sqlite:///mydb_2.db'
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table('users',
                         metadata,
                         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column('first_name', sqlalchemy.String()),
                         sqlalchemy.Column('last_name', sqlalchemy.String()),
                         sqlalchemy.Column('birthday', sqlalchemy.String()),
                         sqlalchemy.Column('email', sqlalchemy.String()),
                         sqlalchemy.Column('address', sqlalchemy.String())
                         )

metadata.create_all(engine)


class UserIn(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    birthday: Optional[str] = Field("YYYY-MM-DD")
    email: EmailStr
    address: str = Field(min_length=5)


class User(BaseModel):
    id: int = Field(... , alias='user_id')
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    birthday: Optional[str] = Field("YYYY-MM-DD")
    email: EmailStr
    address: str = Field(min_length=5)


app = FastAPI()


# @app.get('/fake_users/{count}')
# async def create_note(count: int):
#     for i in range(count):
#         query = users.insert().values(first_name=f'first_name_{i}', last_name=f'last_name{i}',
#                                       birthday=f'200{i}-{i}-{i}', email=f'user{i}@example.ru', address=f'address{i}')
#         await database.execute(query)
#     return {'message': f'{count} fake users created'}


@app.post('/users/', response_model=UserIn)
async def create_user(user: UserIn):
    query = users.insert().values(first_name=user.first_name, last_name=user.last_name,
                                  email=user.email, birthday=user.birthday, address=user.address)
    last_record_id = await database.execute(query)
    return {**user.dict(), 'id': last_record_id}


@app.get('/users/', response_model=List[UserIn])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/user/{user_id}', response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put('/user/{user_id', response_model=UserIn)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), 'id': user_id}


@app.delete('/delete/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}

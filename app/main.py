from fastapi import FastAPI,status,Depends,HTTPException
from databases import Database
from .core.database import sqlalchemy_engine,get_database
from .models.user import (metadata,users)
from .models.schemas.user import (UserCreate,User)

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        await get_database().connect()
    except Exception as e:
        print("connect db error, res is  {}".format(e))
    metadata.create_all(sqlalchemy_engine)
    
@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()
    
@app.get("/")
async def root():
    return {"message": "Ya dejame en paz tin tin"}


async def get_user_or_404(id: int, database: Database = Depends(get_database)) -> User:
    select_query = users.select().where(users.c.id == id)
    raw_post = await database.fetch_one(select_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return User(**raw_post)

@app.post("/users",response_model=User,status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate,db:Database = Depends(get_database)) -> User:
    insert_query = users.insert().values(user.dict())
    user_id = await db.execute(insert_query)
    
    user_db = await get_user_or_404(user_id,db)
    
    return user_db

@app.get("/users/{user_id}",response_model=User)
async def get_user(user_id:int,db:Database = Depends(get_database)) -> User:
    return await get_user_or_404(user_id,db)
from fastapi import FastAPI, Request,status
from tortoise.contrib.fastapi import register_tortoise
from schemas import UserBase
from models import User
app = FastAPI()

def db_init():
    TORTOISE_ORM = {
        "connections": {"default": "postgres://root:pL98wvcPfs@entryflow-test.cifrirvwybqx.us-east-1.rds.amazonaws.com/entryflow"},
        "apps": {
        "models": {
        "models": ["models"],
        "default_connection": "default",
        },
        },
    }
    
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )

db_init()
 
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users",response_model=UserBase,status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase) -> UserBase:
    user_obj = await User.create(**user.dict())
    return UserBase.from_orm(user_obj)


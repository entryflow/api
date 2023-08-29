from sqlalchemy import Session
from ..models import user as user_model
from ..models.schemas import user

def create_user(db:Session,user:user.UserCreate):
    hashed_password = "fakehashedpassword"
    db_user = user_model.User(name=user.name,email=user.email,hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
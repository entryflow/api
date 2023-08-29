import sqlalchemy
from databases import Database

DATABASE_URL = "postgresql://root:pL98wvcPfs@entryflow-test.cifrirvwybqx.us-east-1.rds.amazonaws.com/entryflow"
database = Database(DATABASE_URL)
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)

def get_database() -> Database:
    return database
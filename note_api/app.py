import hvac
from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
# from infra.sql_alchemy_db import SessionLocal
from model.note import Note
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


# This value should be stored in $env
vault_client = hvac.Client(url="http://localhost:8200")
vault_client.auth.approle.login(
    role_id="00e45e77-547c-5b16-6f2a-f491f8401edc",
    secret_id="4255f32e-1fea-d70e-bb74-53d60bda6b2a",
)


app = FastAPI()

secret_read_response = vault_client.read('/backend-secret/data/postgres')

if not secret_read_response:
    raise Exception("Cannot read secret from Vault")

username = secret_read_response['data']['data']['username']
password = secret_read_response['data']['data']['password']
db_engine = create_engine(
    f"postgresql+psycopg://{username}:{password}@localhost:5432/postgres"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return "This is the main API"


@app.get("/notes")
async def get_all_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()

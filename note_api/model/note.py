from sqlalchemy import Column, Integer, String
from infra.sql_alchemy_db import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, )

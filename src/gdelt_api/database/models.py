from sqlalchemy import CHAR, Column, Date, Float
from sqlalchemy.orm import DeclarativeBase  # type: ignore


class Base(DeclarativeBase):  # type:ignore
    pass


class RelationsModel(Base):
    date = Column(Date, primary_key=True)
    country_code_a = Column(CHAR(3), primary_key=True)
    country_code_b = Column(CHAR(3), primary_key=True)
    relations_score = Column(Float, nullable=False)

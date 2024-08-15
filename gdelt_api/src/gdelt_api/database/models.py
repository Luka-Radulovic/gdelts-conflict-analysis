from sqlalchemy import CHAR, Column, Date, Float, Index, Integer
from sqlalchemy.orm import DeclarativeBase  # type: ignore


class Base(DeclarativeBase):  # type:ignore
    pass


class RelationsModel(Base):
    __tablename__ = "relations"

    date = Column(Date, primary_key=True)
    country_code_a = Column(CHAR(3), primary_key=True)
    country_code_b = Column(CHAR(3), primary_key=True)
    relations_score = Column(Float, nullable=False)
    num_verbal_coop = Column(Integer, nullable=False)
    num_material_coop = Column(Integer, nullable=False)
    num_verbal_conf = Column(Integer, nullable=False)
    num_material_conf = Column(Integer, nullable=False)

    __table_args__ = (
        Index("idx_countrya_date", "country_code_a", "date"),
        Index("idx_countrya_countryb", "country_code_a", "country_code_b"),
        Index("idx_countrya_countryb_date", "country_code_a", "country_code_b", "date"),
    )

from sqlalchemy import Column, Integer, String, Float, text, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, nullable=False, primary_key=True)
    user_name = Column(String, nullable=False, unique=True)
    user_email = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    user_created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))


class Operation(Base):
    __tablename__ = "operations"

    operation_id = Column(Integer, nullable=False, primary_key=True)
    operation_kind = Column(String, nullable=False)
    operation_amount = Column(Float, nullable=False)
    operation_description = Column(String, nullable=False, server_default="")
    operation_created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("users.user_id"))

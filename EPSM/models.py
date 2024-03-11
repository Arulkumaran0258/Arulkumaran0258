from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))

class MallOwner(Base):
    __tablename__ = 'mall_owners'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    location = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="mall_owner")

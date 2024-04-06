from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime,Enum as EnumColumn
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from app.config import DATABASE_URL
from datetime import datetime
import bcrypt
from enum import Enum

from contextlib import contextmanager

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    _password = Column("password", String)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship('Transaction', back_populates='owner')
    categories = relationship('Category', back_populates='owner')
    
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    description = Column(String)
    date = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)

    owner = relationship('User', back_populates='transactions')
    category = relationship('Category', back_populates='transactions')
class TransactionType(Enum):
        INCOME = 'income'
        EXPENSE = 'expense'
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))


    type = Column(EnumColumn(TransactionType))  # Could be 'income' or 'expense'

    owner = relationship('User', back_populates='categories')
    transactions = relationship('Transaction', back_populates='category')


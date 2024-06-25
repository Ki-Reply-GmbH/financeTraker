from typing import Union
from app.models.models import TransactionType
from pydantic import BaseModel, Field
from datetime import date
from sqlalchemy import inspect



class CatagoryCreate(BaseModel):
    name: str = Field()
class Category(BaseModel):    
    id: int
    name: str
    class Config:
        orm_mode = True
    def model_dump(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
    def model_load(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        return self
    
class TransactionCreate(BaseModel):
    
    type: TransactionType = Field()
    source: str = Field()
    category: Union[int, str,Category] = Field()
    trxdate: date = Field(...)
    description: str = Field()
    amount: float = Field()
    
    def dict(self, **kwargs):
        model_dict = super().dict(**kwargs)
        # Convert the TransactionType enum to a string
        model_dict['type'] = model_dict['type'].value
        # Convert the date object to a string
        model_dict['trxdate'] = model_dict['trxdate'].isoformat()
        return model_dict
    
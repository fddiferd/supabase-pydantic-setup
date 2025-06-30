from datetime import datetime
from enum import Enum
from uuid import uuid4
from pydantic import BaseModel
from typing import Optional, Any



class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class Customer(BaseModel):
    id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    email: str | None = None
    phone_number: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    photo_url: str | None = None
    gender: Gender = Gender.MALE

    @staticmethod
    def new(email: str, **kw) -> "Customer":
        """Create a new Customer instance with a generated UUID and provided email."""
        customer = Customer(email=email, **kw)
        return customer
    
    @classmethod  
    def from_db(cls, data: dict) -> "Customer":
        """Create a Customer instance from database data (existing record)."""
        return cls(**data)


class CustomerData(BaseModel):
    id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    customer_id: str | None = None
    key: str | None = None
    value: str | None = None

    @staticmethod
    def new(customer_id: str, key: str, value: str) -> "CustomerData":
        return CustomerData(customer_id=customer_id, key=key, value=value)
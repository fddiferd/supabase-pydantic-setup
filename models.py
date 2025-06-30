from datetime import datetime
from enum import Enum
from uuid import uuid4
from pydantic import BaseModel
from typing import Optional, Any
from supadantic.models import BaseSBModel
from supadantic.query_builder import QueryBuilder


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class Customer(BaseSBModel):
    id: str | None = None
    email: str | None = None
    created_at: datetime | None = None
    phone_number: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    photo_url: str | None = None
    gender: Gender = Gender.MALE

    def add(self):
        """
        Add a new record to the database.
        Fails if record with this ID already exists.
        Requires both id and email to be set.
        """
            
        db_client = self._get_db_client()
        data = self.model_dump(exclude={'id'})
        
        # Remove None values to allow database defaults to be used
        insert_data = {k: v for k, v in data.items() if v is not None}

        query_builder = QueryBuilder()
        query_builder.set_insert_data(insert_data)

        response_data = db_client.execute(query_builder=query_builder)
        
        if isinstance(response_data, list) and len(response_data) > 0:
            return self.__class__(**response_data[0])
        else:
            raise Exception("Add operation failed - no data returned")

    def update(self):
        """
        Update an existing record in the database.
        Fails if record with this ID doesn't exist.
        """
        if not self.id:
            raise Exception("Cannot update record without ID")
            
        db_client = self._get_db_client()
        data = self.model_dump(exclude={'id', 'created_at'})
        
        # Remove None values to avoid overwriting existing data with nulls
        update_data = {k: v for k, v in data.items() if v is not None}

        query_builder = QueryBuilder()
        query_builder.set_equal(id=self.id)
        query_builder.set_update_data(update_data)

        response_data = db_client.execute(query_builder=query_builder)
        if isinstance(response_data, list) and len(response_data) > 0:
            return self.__class__(**response_data[0])
        else:
            raise Exception("Update operation failed - record not found or no data returned")

    def set(self):
        """
        Upsert operation: Update if record exists, insert if it doesn't.
        """
        if not self.id:
            # No ID provided, this must be an insert
            return self.add()
        
        # Try to update first
        try:
            return self.update()
        except Exception:
            # If update fails, try to add
            return self.add()

    @staticmethod
    def new(id: str, email: str, **kw) -> "Customer":
        """Create a new Customer instance with provided ID and email."""
        return Customer(id=id, email=email, **kw)
    
    @classmethod  
    def from_db(cls, data: dict) -> "Customer":
        """Create a Customer instance from database data (existing record)."""
        return cls(**data)
    

class CustomerData(BaseModel):
    id: str
    customer_id: str
    created_at: datetime
    updated_at: datetime
    key: str
    value: str
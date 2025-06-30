from typing import Any, Dict
from postgrest import SyncRequestBuilder
from supabase._sync.client import SyncClient
from models import Customer, CustomerData
from supabase_utils import get_client

# Define the client
client: SyncClient = get_client()

# Define the tables
customer_table: SyncRequestBuilder[Dict[str, Any]] = client.table('customer')
customer_data_table: SyncRequestBuilder[Dict[str, Any]] = client.table('customer_data')

# Create a new customer
new_customer: Customer = Customer.new(
    email="nato@test.com", 
    given_name="Nato"
)
customer_dict = new_customer.model_dump(exclude_none=True)
customer_response = customer_table.insert(customer_dict).execute()

# Get a customer
# new_customer: Customer = Customer.from_db(customer_table.select('*').eq('email', 'nato@test.com').execute().data[0])
# print(new_customer)

# Create a new customer data
customer_response_id = customer_response.data[0].get('id')
if customer_response_id is None:
    raise ValueError("Customer ID is required")
new_customer_data: CustomerData = CustomerData.new(
    customer_id=customer_response_id, 
    key="test_key", 
    value="test_value"
)
customer_data_table.insert(new_customer_data.model_dump(exclude_none=True)).execute()

# Delete a customer
customer_table.delete().eq('email', new_customer.email).execute()

# Delete a customer data
customer_data_table.delete().eq('customer_id', customer_response_id).execute()
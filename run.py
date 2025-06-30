from datetime import datetime
from dotenv import load_dotenv
import time
from uuid import uuid4

# Load environment variables BEFORE importing models
load_dotenv()

from models import Customer

# ---------- Create with Generated ID ----------
unique_email = f"ana_{int(time.time())}@example.com"
# Using new_with_generated_id since we want auto-generated UUID
ana = Customer.new_with_generated_id(unique_email, given_name="Ana").add()
print(f"Created customer (auto ID): {ana.id} - {ana.email}")

# ---------- Create with Provided ID ----------
unique_email2 = f"bob_{int(time.time())}@example.com"
custom_id = str(uuid4())
# Using new() method which requires both id and email
bob = Customer.new(custom_id, unique_email2, given_name="Bob").add()
print(f"Created customer (custom ID): {bob.id} - {bob.email}")

# ---------- Read ----------
ana_read = Customer.objects.get(id=ana.id)
print(f"Read customer: {ana_read.email} - {ana_read.given_name}")

# ---------- Update ----------
ana_read.family_name = "Smith"
ana_updated = ana_read.update()
print(f"Updated customer: {ana_updated.given_name} {ana_updated.family_name}")

# ---------- Delete ----------
ana_updated.delete()
print(f"Deleted customer: {ana_updated.id}")

# Clean up the second customer too
bob.delete()
print(f"Deleted customer: {bob.id}")
from supabase import create_client
import os
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if url and key:
    supabase = create_client(url, key)
    
    print("=== Testing direct insert ===")
    
    try:
        # Generate a proper UUID for the test
        test_id = str(uuid4())
        print(f"Using test ID: {test_id}")
        
        # Try inserting a test record directly
        result = supabase.table('customer').insert({
            'id': test_id,
            'email': 'test@example.com',
            'given_name': 'Test',
            'gender': 'male'
        }).execute()
        
        print(f"✅ Direct insert successful: {result}")
        
        # Now try to read it back
        read_result = supabase.table('customer').select('*').eq('id', test_id).execute()
        print(f"✅ Read back successful: {read_result}")
        
        # Clean up - delete the test record
        delete_result = supabase.table('customer').delete().eq('id', test_id).execute()
        print(f"✅ Cleanup successful: {delete_result}")
        
    except Exception as e:
        print(f"❌ Direct insert failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ Environment variables not found") 
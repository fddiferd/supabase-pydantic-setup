-- Drop table if exists and create customer_data table
DROP TABLE IF EXISTS customer_data CASCADE;
CREATE TABLE customer_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    customer_id UUID REFERENCES customer(id) ON DELETE CASCADE,
    key TEXT,
    value TEXT
);

-- Create index on customer_id for better query performance
CREATE INDEX IF NOT EXISTS idx_customer_data_customer_id ON customer_data(customer_id);

-- Create composite index on customer_id and key for unique lookups
CREATE INDEX IF NOT EXISTS idx_customer_data_customer_key ON customer_data(customer_id, key);

-- Drop trigger if it exists and create new one for updated_at
DROP TRIGGER IF EXISTS update_customer_data_updated_at ON customer_data;
CREATE TRIGGER update_customer_data_updated_at
    BEFORE UPDATE ON customer_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

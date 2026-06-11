import os
from dotenv import load_dotenv

# Load key-value pairs out of your local hidden .env file string
load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
DATABASE_URL: str = os.getenv("DATABASE_URL", "")

# Simple configuration validations
if not SUPABASE_URL or not SUPABASE_KEY:
    print("Warning: Supabase credentials are empty or missing inside .env context.")

if not DATABASE_URL:    print("Warning: DATABASE_URL target connection string is missing inside .env context.")
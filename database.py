import json
from sqlalchemy import create_engine, text
from supabase import create_client, Client
import config 

# REPLACE 'YOUR_PROJECT_ID' with the actual ID from your Supabase Dashboard
# database.py
from sqlalchemy import create_engine
import json

# Replace 'YOUR_PROJECT_ID' with your actual Supabase Project ID found in your dashboard
# Format: postgres.YOUR_PROJECT_ID
db_url = "postgresql+pg8000://postgres.knytvfmokibiadtukzzw:vanshika1215@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

# Use connect_args for SSL to avoid 'unexpected keyword argument' errors
engine = create_engine(
    db_url,
    connect_args={"ssl_context": True},
    echo=False
)

engine = create_engine(
    db_url,
    connect_args={"ssl_context": True}, # Safely handles SSL without keyword errors
    echo=False
)

# Initialize engine with 'connect_args' instead
engine = create_engine(
    db_url,
    connect_args={"ssl_context": True}, # Correct way to enable SSL
    echo=False
)
supabase_client: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def save_analysis_to_db(filename: str, storage_path: str, analysis_data: dict):
    sql_command = text("""
        INSERT INTO analyses (filename, storage_path, safety_score, summary, recommendations, clauses_json)
        VALUES (:filename, :storage_path, :safety_score, :summary, :recommendations, :clauses_json);
    """)
    
    recs = analysis_data.get("recommendations", [])
    if isinstance(recs, str): recs = [recs]

    with engine.begin() as connection:
        connection.execute(sql_command, {
            "filename": filename,
            "storage_path": storage_path,
            "safety_score": analysis_data.get("overall_safety_score", 0),
            "summary": analysis_data.get("executive_summary", ""),
            "recommendations": json.dumps(recs),
            "clauses_json": json.dumps(analysis_data.get("clauses", []))
        })

def get_all_history_records():
    sql_command = text("SELECT id, filename, safety_score FROM analyses ORDER BY id DESC;")
    with engine.connect() as connection:
        result = connection.execute(sql_command).fetchall()
        return [{"id": row[0], "filename": row[1], "safety_score": row[2]} for row in result]

def get_analysis_by_id(analysis_id: int):
    sql_command = text("SELECT filename, safety_score, summary, recommendations, clauses_json FROM analyses WHERE id = :id;")
    with engine.connect() as connection:
        row = connection.execute(sql_command, {"id": analysis_id}).fetchone()
        if not row: return None
        return {
            "filename": row[0], "safety_score": row[1], "summary": row[2],
            "recommendations": row[3] if isinstance(row[3], list) else json.loads(row[3] or "[]"),
            "clauses_json": json.loads(row[4]) if isinstance(row[4], str) else row[4]
        }

def delete_analysis_by_id(analysis_id: int):
    sql_command = text("DELETE FROM analyses WHERE id = :id;")
    with engine.begin() as connection:
        connection.execute(sql_command, {"id": analysis_id})
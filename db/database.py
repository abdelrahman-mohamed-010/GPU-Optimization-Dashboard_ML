import sqlite3
from sqlite3 import Error
from config import DB_PATH
from gpu.models import GPU

class DatabaseManager:
    def __init__(self,db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            print("Database connection established.")
        except Error as e:
            print(f"Error connecting to database {e}")
    
    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS gpu_static (
        id TEXT PRIMARY KEY,
        model TEXT,
        memory_total_gb REAL,
        compute_tflops REAL,
        bandwidth_gbps REAL
        );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table gpu_static created or already exixts.")
        except Exception as e:
            print(f"Error creating table: {e}")
    
    def insert_gpu(self, gpu:GPU):
        insert_sql="""
        INSERT OR REPLACE INTO gpu_static (id,model, memory_total_gb, compute_tflops, bandwidth_gbps)
        VALUES (?,?,?,?,?)
        """
        try:
            cursor=self.conn.cursor()
            cursor.execute(insert_sql,(gpu.id,gpu.model,gpu.memory_total_gb, gpu.compue_tflops, gpu.bandwidth_gbps))
            self.conn.commit()
            print(f"Inserted GPU into the database: {gpu}")
        except Exception as e:
            print(f"Error inserting GPU: {e}")
    
    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
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
    
    def create_dynamic_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS gpu_dynamic (
            id TEXT,
            timestamp DATETIME,
            utilization REAL,
            memory_used_gb REAL,
            temperature REAL,
            power_w REAL,
            FOREIGN KEY (id) REFERENCES gpu_statics(id)
        );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table gpu_dynamic created or already exists.")
        except Error as e:
            print(f"Error createing dynamic table: {e}")
    
    def insert_dynamic(self, gpu_id, data):
        insert_sql = """
        INSERT INTO gpu_dynamic (id, timestamp, utilization, memory_used_gb, temperature, power_w)
        VALUES (?, datetime('now'),?, ?, ?, ?)
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(insert_sql,(gpu_id, data['util'], data['mem'],data['temp'], data['power']))
            self.conn.commit()
            print(f"Inserted  dynamic data for GPU {gpu_id}: {data}")
        except Error as e:
            print(f"Error insearting dynamic data for GPU {gpu_id}:{e}")
    

    def get_gpu_state(self,gpu_id:str):
        try: 
            static_columns=["id","model" ,"memory_total_gb","compute_tflops","bandwidth_gbps"]
            dynamic_columns=["id", "timestamp", "utilization", "memory_used_gb", "temperature", "power_w"]
            cursor = self.conn.cursor()
            static = cursor.execute("SELECT * FROM gpu_static WHERE id = ?",(gpu_id,)).fetchone()
            dynamic = cursor.execute("SELECT * FROM gpu_dynamic WHERE id = ? ORDER BY timestamp DESC LIMIT 1", (gpu_id,)).fetchone()
            
            # Map rows to dictionaries
            static_dict = dict(zip(static_columns, static)) if static else None
            dynamic_dict = dict(zip(dynamic_columns, dynamic)) if dynamic else None
            return {"static":static_dict, "dynamic":dynamic_dict}
        except Error as e:
            print(f"Error while featching GPU static and dynamic stats, {gpu_id}: {e}") 
    
    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
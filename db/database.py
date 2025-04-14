import sqlite3
from sqlite3 import Error
from config import DB_PATH

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        try:
            # Enable multi-threaded access and WAL mode for better concurrency.
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.execute("PRAGMA journal_mode=WAL;")
            print("Database connection established.")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            # Vendors table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vendors (
                    vendor_name TEXT PRIMARY KEY
                );
            """)
            vendors = [("Nvidia",), ("AMD",), ("Intel",)]
            cursor.executemany("INSERT OR IGNORE INTO vendors (vendor_name) VALUES (?)", vendors)
            
            # Clusters table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clusters (
                    cluster_name TEXT PRIMARY KEY
                );
            """)
            
            # Racks table (10 racks per cluster)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS racks (
                    rack_id TEXT PRIMARY KEY,
                    cluster_name TEXT,
                    FOREIGN KEY(cluster_name) REFERENCES clusters(cluster_name)
                );
            """)
            
            # GPUs table: Each GPU has a unique UUID and foreign keys to racks and vendors.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gpus (
                    gpu_id TEXT PRIMARY KEY,
                    rack_id TEXT,
                    vendor TEXT,
                    model TEXT,
                    memory_total_gb INTEGER,
                    compute_tflops REAL,
                    bandwidth_gbps INTEGER,
                    FOREIGN KEY(rack_id) REFERENCES racks(rack_id),
                    FOREIGN KEY(vendor) REFERENCES vendors(vendor_name)
                );
            """)
            
            # GPU metrics table: Logs dynamic metrics.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gpu_metrics (
                    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    gpu_id TEXT,
                    utilization REAL,
                    memory_used_gb REAL,
                    temperature REAL,
                    power_watts REAL,
                    timestamp DATETIME,
                    FOREIGN KEY(gpu_id) REFERENCES gpus(gpu_id)
                );
            """)
            
            # RL performance table: Logs performance metrics from Federated PPO simulation.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rl_performance (
                    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    day TEXT,
                    average_reward REAL,
                    timestamp DATETIME
                );
            """)
            self.conn.commit()
            print("All tables created or already exist.")
        except Error as e:
            print(f"Error creating tables: {e}")

    def insert_cluster(self, cluster_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO clusters (cluster_name) VALUES (?)", (cluster_name,))
            self.conn.commit()
        except Error as e:
            print(f"Error inserting cluster {cluster_name}: {e}")

    def insert_rack(self, rack_id, cluster_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO racks (rack_id, cluster_name) VALUES (?, ?)", (rack_id, cluster_name))
            self.conn.commit()
        except Error as e:
            print(f"Error inserting rack {rack_id}: {e}")

    def insert_gpu(self, gpu_id, rack_id, vendor, model, memory_total_gb, compute_tflops, bandwidth_gbps):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO gpus (gpu_id, rack_id, vendor, model, memory_total_gb, compute_tflops, bandwidth_gbps)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (gpu_id, rack_id, vendor, model, memory_total_gb, compute_tflops, bandwidth_gbps))
            self.conn.commit()
        except Error as e:
            print(f"Error inserting GPU {gpu_id}: {e}")

    def insert_gpu_metrics_batch(self, records):
        try:
            cursor = self.conn.cursor()
            cursor.executemany("""
                INSERT INTO gpu_metrics (gpu_id, utilization, memory_used_gb, temperature, power_watts, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, records)
            self.conn.commit()
        except Error as e:
            print(f"Error inserting metrics batch: {e}")

    def insert_rl_performance(self, day, average_reward, timestamp):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO rl_performance (day, average_reward, timestamp)
                VALUES (?, ?, ?)
            """, (day, average_reward, timestamp))
            self.conn.commit()
        except Error as e:
            print(f"Error inserting RL performance: {e}")

    def get_all_gpus(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT gpu_id, model, memory_total_gb FROM gpus")
        return cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

import random
import uuid
from db.database import DatabaseManager
from config import DB_PATH

# GPU specifications dictionary (as provided; ensure this dictionary is defined above)
gpu_specs = {
    "RTX 4090": {"memory_total_gb": 24, "compute_tflops": 82, "bandwidth_gbps": 1008},
    "RTX 4080": {"memory_total_gb": 16, "compute_tflops": 49, "bandwidth_gbps": 720},
    "RTX 7900": {"memory_total_gb": 20, "compute_tflops": 60, "bandwidth_gbps": 600},
    "A100 80GB": {"memory_total_gb": 80, "compute_tflops": 19.5, "bandwidth_gbps": 1555},
    "V100 32GB": {"memory_total_gb": 32, "compute_tflops": 15, "bandwidth_gbps": 900},
    "V100 16GB": {"memory_total_gb": 16, "compute_tflops": 15, "bandwidth_gbps": 900},
    "H100": {"memory_total_gb": 80, "compute_tflops": 60, "bandwidth_gbps": 2000},
    "RTX 3080": {"memory_total_gb": 10, "compute_tflops": 29.8, "bandwidth_gbps": 760},
    "RTX 3070": {"memory_total_gb": 8, "compute_tflops": 20, "bandwidth_gbps": 512},
    "RTX 3060": {"memory_total_gb": 12, "compute_tflops": 13, "bandwidth_gbps": 360},
    "RTX 3090": {"memory_total_gb": 24, "compute_tflops": 35, "bandwidth_gbps": 936},
    "RTX 3050": {"memory_total_gb": 8, "compute_tflops": 9, "bandwidth_gbps": 224},
    "Quadro RTX 8000": {"memory_total_gb": 48, "compute_tflops": 16, "bandwidth_gbps": 672},
    "Quadro RTX 6000": {"memory_total_gb": 24, "compute_tflops": 14, "bandwidth_gbps": 432},
    "Titan RTX": {"memory_total_gb": 24, "compute_tflops": 16.3, "bandwidth_gbps": 672},
    "Tesla T4": {"memory_total_gb": 16, "compute_tflops": 8, "bandwidth_gbps": 320},
    "Tesla P100": {"memory_total_gb": 16, "compute_tflops": 10.6, "bandwidth_gbps": 732},
    "Tesla P40": {"memory_total_gb": 24, "compute_tflops": 12, "bandwidth_gbps": 346},
    "Tesla P4": {"memory_total_gb": 8, "compute_tflops": 5.5, "bandwidth_gbps": 192},
    "Quadro GV100": {"memory_total_gb": 32, "compute_tflops": 14, "bandwidth_gbps": 870},
    "AMD Radeon Instinct MI100": {"memory_total_gb": 32, "compute_tflops": 11.5, "bandwidth_gbps": 1200},
    "AMD Radeon Instinct MI200": {"memory_total_gb": 32, "compute_tflops": 14, "bandwidth_gbps": 1500},
    "AMD Radeon Instinct MI50": {"memory_total_gb": 16, "compute_tflops": 7, "bandwidth_gbps": 800},
    "AMD Radeon VII": {"memory_total_gb": 16, "compute_tflops": 13.8, "bandwidth_gbps": 1028},
    "AMD Radeon Pro W6800": {"memory_total_gb": 32, "compute_tflops": 16, "bandwidth_gbps": 1024},
    "AMD Radeon RX 6900 XT": {"memory_total_gb": 16, "compute_tflops": 23, "bandwidth_gbps": 512},
    "AMD Radeon RX 6800 XT": {"memory_total_gb": 16, "compute_tflops": 20, "bandwidth_gbps": 512},
    "AMD Radeon RX 6800": {"memory_total_gb": 16, "compute_tflops": 18, "bandwidth_gbps": 512},
    "AMD Radeon RX 6700 XT": {"memory_total_gb": 12, "compute_tflops": 13, "bandwidth_gbps": 384},
    "AMD Radeon Pro W5500": {"memory_total_gb": 8, "compute_tflops": 8, "bandwidth_gbps": 256},
    "AMD Radeon Pro WX 8200": {"memory_total_gb": 8, "compute_tflops": 6.7, "bandwidth_gbps": 256},
    "Intel Xe-HPG": {"memory_total_gb": 8, "compute_tflops": 10, "bandwidth_gbps": 256},
    "Intel Iris Xe Max": {"memory_total_gb": 4, "compute_tflops": 2, "bandwidth_gbps": 68},
    "Intel Arc A770": {"memory_total_gb": 8, "compute_tflops": 12, "bandwidth_gbps": 288},
    "Intel Arc A750": {"memory_total_gb": 8, "compute_tflops": 10, "bandwidth_gbps": 256},
    "Intel Xe-LP": {"memory_total_gb": 4, "compute_tflops": 4, "bandwidth_gbps": 64},
    "Intel Xe-HP": {"memory_total_gb": 16, "compute_tflops": 18, "bandwidth_gbps": 300},
    "NVIDIA Quadro RTX A6000": {"memory_total_gb": 48, "compute_tflops": 38.7, "bandwidth_gbps": 768},
    "NVIDIA Quadro RTX A5000": {"memory_total_gb": 24, "compute_tflops": 27, "bandwidth_gbps": 600},
    "NVIDIA A30": {"memory_total_gb": 24, "compute_tflops": 10, "bandwidth_gbps": 933},
    "NVIDIA A40": {"memory_total_gb": 48, "compute_tflops": 14, "bandwidth_gbps": 696},
    "NVIDIA A10": {"memory_total_gb": 24, "compute_tflops": 9, "bandwidth_gbps": 600},
    "NVIDIA A16": {"memory_total_gb": 32, "compute_tflops": 6, "bandwidth_gbps": 300},
    "AMD Radeon Instinct MI250": {"memory_total_gb": 64, "compute_tflops": 18, "bandwidth_gbps": 1800},
    "AMD Radeon RX 6600 XT": {"memory_total_gb": 8, "compute_tflops": 9, "bandwidth_gbps": 256},
    "AMD Radeon RX 6500 XT": {"memory_total_gb": 4, "compute_tflops": 6, "bandwidth_gbps": 128},
    "Intel Arc A580": {"memory_total_gb": 6, "compute_tflops": 7, "bandwidth_gbps": 192},
    "Intel Iris Xe Graphics": {"memory_total_gb": 4, "compute_tflops": 3, "bandwidth_gbps": 64},
    "Intel Arc A770M": {"memory_total_gb": 8, "compute_tflops": 11, "bandwidth_gbps": 256},
    "NVIDIA GeForce GTX 1660": {"memory_total_gb": 6, "compute_tflops": 5, "bandwidth_gbps": 192}
}

# Fixed rack codes for each cluster (10 racks per cluster)
rack_codes = ["A12", "B08", "C04", "D09", "E07", "F05", "G06", "H03", "I10", "J11"]

# Vendor helper function.
def get_vendor(model):
    model_lower = model.lower()
    if "intel" in model_lower or "iris" in model_lower or "arc" in model_lower or "xe-" in model_lower:
        return "Intel"
    elif "amd" in model_lower or "radeon" in model_lower:
        return "AMD"
    else:
        return "Nvidia"

def generate_static_data():
    db = DatabaseManager()
    db.connect()
    db.create_tables()

    # Check if clusters table already contains data.
    cur = db.conn.cursor()
    cur.execute("SELECT COUNT(*) FROM clusters")
    count = cur.fetchone()[0]
    if count > 0:
        print("Static data already exists. Skipping static data generation.")
        db.close()
        return

    # Generate 50 unique cluster names using directions and Greek letters.
    directions = ["East", "West", "North", "South", "Central"]
    greek_letters = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa"]
    clusters = [f"{d} {letter} Datacenter" for d in directions for letter in greek_letters]

    for cluster in clusters:
        db.insert_cluster(cluster)

    # Generate racks: for each cluster, 10 racks with IDs like "EastAlpha-A12".
    for cluster in clusters:
        parts = cluster.split()
        cluster_prefix = parts[0] + parts[1]  # e.g., "EastAlpha"
        for i, code in enumerate(rack_codes):
            rack_id = f"{cluster_prefix}-{code}"
            db.insert_rack(rack_id, cluster)

    # Insert GPUs: For each rack, 100 GPUs with unique UUIDs.
    cur.execute("SELECT rack_id FROM racks")
    all_racks = cur.fetchall()

    for (rack_id,) in all_racks:
        for _ in range(100):
            model = random.choice(list(gpu_specs.keys()))
            specs = gpu_specs[model]
            gpu_id = str(uuid.uuid4())
            vendor = get_vendor(model)
            db.insert_gpu(gpu_id, rack_id, vendor, model, specs["memory_total_gb"],
                          specs["compute_tflops"], specs["bandwidth_gbps"])
    db.close()
    print("Static data generated and inserted into the database.")

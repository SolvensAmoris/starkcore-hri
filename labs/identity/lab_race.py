# lab_race.py - COSMOS RACE TEST v0.3
# Objetivo: ¿EvidenceStore aguanta escrituras concurrentes reales?
import threading, json, time, os, hashlib, random

STORE_FILE = "evidence_race.json"

def compute_hash(i):
    return hashlib.sha256(f"NODE|{i}".encode()).hexdigest()[:12]

# --- Versión INSEGURA (sin lock) ---
def write_unsafe(node_id):
    # Simula lo que haría un Executor que escribe directo sin Gate
    data = {}
    if os.path.exists(STORE_FILE):
        try:
            with open(STORE_FILE, "r") as f:
                data = json.load(f)
        except:
            data = {}
    # ventana de carrera aquí: dos hilos leen el mismo archivo vacío
    data[str(node_id)] = compute_hash(node_id)
    time.sleep(0.001) # fuerza el intercalado
    with open(STORE_FILE, "w") as f:
        json.dump(data, f)

# --- Versión SEGURA (con lock = Gate -> Evidence) ---
lock = threading.Lock()
def write_safe(node_id):
    with lock:
        data = {}
        if os.path.exists(STORE_FILE):
            try:
                with open(STORE_FILE, "r") as f:
                    data = json.load(f)
            except:
                data = {}
        data[str(node_id)] = compute_hash(node_id)
        time.sleep(0.001)
        with open(STORE_FILE, "w") as f:
            json.dump(data, f)

def run_test(writer_fn, n=200, threads=50):
    if os.path.exists(STORE_FILE):
        os.remove(STORE_FILE)
    t0 = time.time()
    
    def worker(start):
        for i in range(start, start + n//threads):
            writer_fn(i)

    ths = []
    for t in range(threads):
        th = threading.Thread(target=worker, args=(t*(n//threads),))
        ths.append(th)
        th.start()
    for th in ths:
        th.join()

    elapsed = time.time() - t0
    if os.path.exists(STORE_FILE):
        with open(STORE_FILE, "r") as f:
            try:
                final = json.load(f)
                count = len(final)
            except:
                count = -1 # JSON corrupto por escritura simultánea
    else:
        count = 0
    
    print(f"Esperados: {n}, Encontrados en archivo: {count}, Tiempo: {elapsed:.3f}s")
    if count != n:
        print(f" >>> GRIETA DETECTADA: Se perdieron {n-count} evidencias por condicion de carrera!")
        if count == -1:
            print(" >>> JSON CORRUPTO: dos hilos escribieron al mismo tiempo")
    else:
        print(" OK: Integridad conservada")
    return count

print("COSMOS RACE TEST v0.3\n")
print("--- TEST 1: SIN LOCK (Executor -> Evidence directo) ---")
c1 = run_test(write_unsafe, n=200, threads=50)

print("\n--- TEST 2: CON LOCK (Executor -> Gate -> Evidence) ---")
c2 = run_test(write_safe, n=200, threads=50)

print("\nConclusion:")
print("Si TEST 1 pierde datos y TEST 2 no, acabas de probar por que tu diseño")
print("Parser | Planner | Gate | Executor | Evidence NO es opcional.")

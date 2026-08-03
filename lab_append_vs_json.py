# lab_append_vs_json.py - COSMOS RACE TEST v0.4
# JSON rewrite vs Append-only log
import threading, json, time, os, hashlib

LOG_FILE = "evidence.log"
JSON_FILE = "evidence.json"
lock = threading.Lock()

def h(i):
    return hashlib.sha256(f"NODE|{i}".encode()).hexdigest()[:8]

# 1. JSON con lock (tu solución actual segura pero lenta)
def write_json_lock(i):
    with lock:
        data={}
        if os.path.exists(JSON_FILE):
            try:
                with open(JSON_FILE,"r") as f: data=json.load(f)
            except: pass
        data[str(i)]=h(i)
        time.sleep(0.001)
        with open(JSON_FILE,"w") as f: json.dump(data,f)

# 2. APPEND-ONLY LOG (sin lock, solo añadir)
def write_append_log(i):
    # En POSIX, append de <4KB es atómico a nivel de OS
    line = json.dumps({str(i): h(i)}) + "\n"
    with open(LOG_FILE,"a") as f:
        f.write(line)

def run(fn, n, t, filename):
    if os.path.exists(filename): os.remove(filename)
    t0=time.time()
    def worker(s):
        for j in range(s, s + n//t):
            fn(j)
    ths=[threading.Thread(target=worker, args=(k*(n//t),)) for k in range(t)]
    for th in ths: th.start()
    for th in ths: th.join()
    elapsed=time.time()-t0
    
    count=0
    if os.path.exists(filename):
        try:
            if filename.endswith(".json"):
                with open(filename,"r") as f: count=len(json.load(f))
            else:
                with open(filename,"r") as f: count=len(f.readlines())
        except Exception as e:
            count=-1
    return elapsed, count

print("COSMOS RACE TEST v0.4 - JSON vs LOG\n")
print("--- 1. JSON con LOCK (seguro pero reescribe todo) ---")
t1,c1=run(write_json_lock, 500, 50, JSON_FILE)
print(f"Tiempo: {t1:.3f}s | Registros: {c1}/500 -> {'OK' if c1==500 else 'FAIL'}")

print("\n--- 2. APPEND-ONLY LOG (sin lock, solo añade) ---")
t2,c2=run(write_append_log, 500, 50, LOG_FILE)
print(f"Tiempo: {t2:.3f}s | Registros: {c2}/500 -> {'OK' if c2==500 else 'FAIL'}")

print(f"\nSpeedup: {t1/t2:.1f}x mas rapido")
print("\nConclusion:")
print("JSON rewrite = O(n) por escritura, lento y con lock obligatorio")
print("Append log = O(1) por escritura, rapido y atomico sin lock")
print("Luego un lector reconstruye el estado final leyendo las 500 lineas.")
print("\nEsto es exactamente lo que deberia hacer tu EvidenceStore real.")

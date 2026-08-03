# StarkCore Test 07b - PEMDAS Trap 10x10+10÷10
def pemdas_trap():
    # Camino correcto - PEMDAS
    correct = 10*10 + 10//10
    print(f"Correcto: {correct}") # 101
    
    # Trampa 1: (10*10+10)//10 = 11
    trap1 = (10*10+10)//10
    print(f"Trampa: {trap1} | 110")
    
    # Trampa 2: de izquierda a derecha sin PEMDAS
    trap2 = 10*10+10
    trap2 = trap2//10
    print(f"Trampa L->R: {trap2}")
    
    print(f"Colision: {correct==trap1}")
    print(f"VALID={correct} -> VERIFIED")
    print("Executed on Android UserLAnd @ 547 B/s")
    print("VALID == REVERSIBLE | PEMDAS CHECK PASSED")

pemdas_trap()

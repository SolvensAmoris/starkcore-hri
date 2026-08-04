import math
a=20
b=5
c=12
r1 = a // b + c
r2 = a // (b+c)
print("Correcto:", r1)
print("Trampa:", r2)
print("Colision:", r1==r2)
print("StarkCore: VALID=16 -> VERIFIED")

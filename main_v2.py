
from starkcore.sanctuary.temple import Sanctuary


s=Sanctuary()

s.load_constellation(
    "gold_sanctuary"
)


print("\n🔥 FLUJO NORMAL")

print(
s.invoke({})
)


print("\n🔥 FLUJO OFIUCO")

print(
s.invoke(
{"anomaly":True}
)
)

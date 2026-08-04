import os

print("🔱 Forjando StarkCore Sanctuary V2...")

paths = [
    "starkcore",
    "starkcore/sanctuary",
    "starkcore/knights",
    "starkcore/executors"
]

for p in paths:
    os.makedirs(p, exist_ok=True)
    open(f"{p}/__init__.py", "w").close()


# ===============================
# BASE KNIGHT
# ===============================

with open("starkcore/knights/base.py","w") as f:
    f.write("""
from typing import Dict, Any

Context = Dict[str, Any]


class Knight:

    NAME = "Unknown"
    HOUSE = 0
    ARCHETYPE = "Undefined"

    def __init__(self, executor=None):
        self.executor = executor

    def should_handle(self, ctx):
        return True

    def prepare(self, ctx):
        return ctx

    def execute(self, ctx):

        if self.executor:
            return self.executor.execute(ctx)

        return ctx

    def finalize(self, ctx):
        return ctx
""")


# ===============================
# ZODIAC
# ===============================

with open("starkcore/knights/zodiac.py","w") as f:
    f.write("""
from .base import Knight


def create(name, house, archetype):

    return type(
        name,
        (Knight,),
        {
            "NAME": name.replace("Knight",""),
            "HOUSE": house,
            "ARCHETYPE": archetype,

            "execute": lambda self,ctx:
                (
                    print(
                    f"  🏛️ Casa {self.HOUSE}: {self.NAME} ({self.ARCHETYPE})"
                    ),
                    ctx
                )[1]
        }
    )


AriesKnight=create("AriesKnight",1,"Bootstrap")
TaurusKnight=create("TaurusKnight",2,"Persistence")
GeminiKnight=create("GeminiKnight",3,"Redundancy")
CancerKnight=create("CancerKnight",4,"Firewall")
LeoKnight=create("LeoKnight",5,"Streaming")


class VirgoKnight(Knight):

    NAME="Shaka"
    HOUSE=6
    ARCHETYPE="Validation"

    def execute(self,ctx):

        print("  🏛️ Casa 6: Shaka (Validation)")

        if ctx.get("anomaly"):
            raise RuntimeError(
                "Anomalía crítica detectada"
            )

        return ctx


LibraKnight=create("LibraKnight",7,"Consensus")
ScorpioKnight=create("ScorpioKnight",8,"Cleanup")
SagittariusKnight=create("SagittariusKnight",9,"Routing")
CapricornKnight=create("CapricornKnight",10,"Kernel")
AquariusKnight=create("AquariusKnight",11,"Sandbox")
PiscesKnight=create("PiscesKnight",12,"Presentation")
""")


# ===============================
# OMEGA
# ===============================

with open("starkcore/sanctuary/omega.py","w") as f:
    f.write("""
import hashlib
import time


class OmegaObserver:

    def __init__(self):

        self.stream=[]
        self.memory={}


    def record(self,**event):

        event["time"]=time.time()
        self.stream.append(event)


    def hash_error(self,error,house):

        raw=f"{type(error).__name__}:{error}:{house}"

        return hashlib.sha256(
            raw.encode()
        ).hexdigest()[:12]


    def learn(self,h):

        self.memory[h]=self.memory.get(h,0)+1


    def frequency(self,h):

        return self.memory.get(h,0)
""")


# ===============================
# OFIUCO
# ===============================

with open("starkcore/knights/ophiuchus.py","w") as f:
    f.write("""
class OphiuchusKnight:

    NAME="Odysseus"
    HOUSE=13


    def investigate(self,error,house,ctx,omega):

        h=omega.hash_error(error,house)

        omega.learn(h)

        print()
        print("🐍 OFIUCO DESPIERTA")
        print("   Ley: Anomalía -> Evidencia")
        print("   Hash:",h)
        print("   Frecuencia:",omega.frequency(h))


        ctx["evidence"]=h
        ctx["learning_mode"]=True

        return ctx
""")


# ===============================
# STARMAP
# ===============================

with open("starkcore/sanctuary/starmap.py","w") as f:
    f.write("""
from starkcore.knights.zodiac import *


class StarMap:

    @staticmethod
    def load(name):

        return [

        AriesKnight(),
        TaurusKnight(),
        GeminiKnight(),
        CancerKnight(),
        LeoKnight(),
        VirgoKnight(),
        LibraKnight(),
        ScorpioKnight(),
        SagittariusKnight(),
        CapricornKnight(),
        AquariusKnight(),
        PiscesKnight()

        ]
""")


# ===============================
# TEMPLE
# ===============================

with open("starkcore/sanctuary/temple.py","w") as f:
    f.write("""
from .omega import OmegaObserver
from .starmap import StarMap
from starkcore.knights.ophiuchus import OphiuchusKnight


class Sanctuary:


    def __init__(self,observer=None):

        self.observer=observer or OmegaObserver()
        self.knights=[]
        self.ophiuchus=OphiuchusKnight()


    def load_constellation(self,name):

        self.knights=StarMap.load(name)


    def invoke(self,ctx):

        for k in self.knights:

            try:

                self.observer.record(
                    house=k.HOUSE,
                    knight=k.NAME,
                    action="ENTER"
                )

                ctx=k.execute(ctx)

            except Exception as e:

                self.observer.record(
                    house=k.HOUSE,
                    knight=k.NAME,
                    action="CRASH"
                )

                return self.ophiuchus.investigate(
                    e,
                    k.HOUSE,
                    ctx,
                    self.observer
                )

        return ctx
""")


# ===============================
# MAIN
# ===============================

with open("main_v2.py","w") as f:
    f.write("""
from starkcore.sanctuary.temple import Sanctuary


s=Sanctuary()

s.load_constellation(
    "gold_sanctuary"
)


print("\\n🔥 FLUJO NORMAL")

print(
s.invoke({})
)


print("\\n🔥 FLUJO OFIUCO")

print(
s.invoke(
{"anomaly":True}
)
)
""")


print("✅ Santuario V2 compilable generado.")

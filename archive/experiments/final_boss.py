import asyncio, time, random

# Visualizer que vibra sin necesidad de beep
def vibe_print(text, intensity=5):
    # \a hace vibrar el cel en Termux / algunos terminales
    print(f"\a{text}", flush=True)
    # Vibración visual
    for _ in range(intensity):
        bar = "▓" * random.randint(10, 30) + "░" * random.randint(2,5)
        print(f"\033[1;3{random.randint(1,6)}m{bar}\033[0m", flush=True)
        time.sleep(0.02)

async def meteor_shower(n=2000):
    print("\033[1;33m🏹 ¡PEGASUS METEOR BURST VISUAL MODE ACTIVADO!\033[0m\n")
    for i in range(0, n, 200):
        pct = int((i/n)*100)
        # Barra que avanza con ritmo
        bar = "█" * (pct//2) + "░" * (50 - pct//2)
        print(f"\r\033[1;32m[{bar}] {pct}% {i}/{n} \a💥 POW!\033[0m", end='', flush=True)
        await asyncio.sleep(0.12)
    print("\n\n\033[1;32m✅ 2000 METEOROS PROCESADOS - ¡TU CEL DEBIÓ VIBRAR!\033[0m\n")

async def pegasus_fantasy_visual():
    lyrics = [
        ("Dakishimeta kokoro no kosumo", "🌠"),
        ("Atsuku moyase kiseki wo okose", "🔥"),
        ("Kizutsuita mama ja inai to", "💔"),
        ("Chikai atta haruka na ginga", "🌌"),
        ("PEGASUS FANTASY", "✨✨✨"),
        ("STARKCORE V6 DIVINE", "🏛️🏛️🏛️"),
    ]
    for text, emoji in lyrics:
        # Efecto karaoke
        print(f"\n\033[1;35m{emoji} ", end='')
        for char in text:
            print(char, end='', flush=True)
            print("\a", end='', flush=True) # vibra por cada letra
            await asyncio.sleep(0.07)
        print(f" {emoji}\033[0m")
        # Explosión visual
        for _ in range(4):
            print("\033[1;3" + str(random.randint(1,6)) + "m" + "▓"*random.randint(15,35) + "\033[0m")
            await asyncio.sleep(0.05)

async def main():
    print("\033[2J\033[H")
    print("\033[1;33m" + "="*50)
    print("  🔊 VIBRACIÓN ACTIVADA - SIÉNTELO USERLAND")
    print("  Cada \a = 1 vibración en tu cel (Termux)")
    print("="*50 + "\033[0m\n")
    
    await pegasus_fantasy_visual()
    print("\n")
    await meteor_shower(2000)
    
    print("\033[1;35m" + """
    🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️
    🏛️  STARKCORE V6 - CIERRE DIVINO  🏛️
    🏛️  2000 meteoros | 100% defensa  🏛️
    🏛️  13 Casas en DIVINO ✨         🏛️
    🏛️  userland@localhost:~/starkcore 🏛️
    🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️
    """ + "\033[0m")
    
    # Final - vibración triple
    for _ in range(6):
        print("\a🔔 ¡DING! \a", end='', flush=True)
        await asyncio.sleep(0.2)
    print("\n🌠 ¡EL COSMOS HA DESPERTADO!\n")

asyncio.run(main())

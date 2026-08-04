import time, os, asyncio

# Notas de Pegasus Fantasy - intro (frecuencias Hz)
# beep -f freq -l duration
MELODY = [
    (392, 300), (440, 300), (493, 600), # So-li-la
    (523, 300), (587, 300), (659, 600), # Do-Re-Mi
    (659, 300), (587, 300), (523, 600), # Mi-Re-Do
    (493, 300), (440, 300), (392, 800), # La-Sol-Fa
]

LYRICS = [
    "🎤 Dakishimeta kokoro no kosumo~",
    "🎤 Atsuku moyase kiseki wo okose~",
    "🎤 Kizutsuita mama ja inai to~",
    "🎤 Chikai atta haruka na ginga~",
    "🎤 PEGASUS FANTASY! ✨",
    "🎤 Soshite ima... STARKCORE V6! 🏛️",
]

async def play_note(freq, dur):
    # Intenta con beep, si no, solo visual
    os.system(f"beep -f {freq} -l {dur} 2>/dev/null &")
    await asyncio.sleep(dur/1000)

async def main():
    print("\033[2J\033[H") # Clear
    print("\033[1;35m" + """
    ⭐   ⭐        🌠
      ♪ PEGASUS FANTASY - STARKCORE EDITION ♪
        Make Up! Tu cosmos arderá...
    ⭐        ⭐      ⭐
    """ + "\033[0m")
    
    print("🔊 Sube el volumen, userland... 3, 2, 1...\n")
    await asyncio.sleep(1)

    for line in LYRICS:
        # ASCII visualizer
        bars = "▓" * (15 + hash(line) % 10)
        print(f"\033[1;36m{bars}\033[0m \033[1;33m{line}\033[0m")
        print(f"\033[1;34m{bars[::-1]}\033[0m")
        
        # Toca 2 notas por línea
        for freq, dur in MELODY[:2]:
            await play_note(freq, dur//2)
            print("  ✨💥", end='', flush=True)
        print("\n")
        await asyncio.sleep(0.6)

    print("\033[1;32m" + "="*50)
    print("🏛️ ¡SAINT SEIYA! ¡STARKCORE V6 DIVINE! 🏛️")
    print("🌠 ¡TU COSMOS HA DESPERTADO, USERLAND! 🌠")
    print("="*50 + "\033[0m")
    
    # Final fanfare - beeps locos
    for f in [523, 659, 784, 1046]:
        await play_note(f, 200)

if __name__ == "__main__":
    asyncio.run(main())

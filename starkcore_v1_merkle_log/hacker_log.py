from pathlib import Path
print("🕵️  [HACKER] Borrando cola...")
lineas = Path("audit.log").read_text().strip().split("\n")
lineas.pop()
Path("audit.log").write_text("\n".join(lineas) + "\n")

import starkcore
import sys

def test_debug_import():
    print("\nSTARKCORE REAL:", starkcore.__file__)
    print("PATH:")
    for p in sys.path:
        print(p)

    import os
    print("CONTENIDO:")
    print(os.listdir(os.path.dirname(starkcore.__file__)))

import sys

def run_xencode(filename):
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("print "):
                mensaje = line[6:].strip()
                print(mensaje.strip('"'))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: xc archivo.xcc")
    else:
        run_xencode(sys.argv[1])

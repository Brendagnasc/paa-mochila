import random, subprocess, sys, re

def run(prog, inp):
    p = subprocess.run([prog], input=inp, capture_output=True, text=True)
    m = re.search(r"Lucro maximo:\s*(\d+)", p.stdout)
    return int(m.group(1)) if m else None

random.seed(42)
fails = 0
for t in range(400):
    n = random.randint(1, 14)
    W = random.randint(1, 40)
    V = random.randint(1, 40)
    lines = [f"{W} {V}"]
    for _ in range(n):
        w = random.randint(1, 20); l = random.randint(1, 20); val = random.randint(1, 50)
        lines.append(f"{w} {l} {val}")
    inp = "\n".join(lines) + "\n"
    a = run("./mochila_pd", inp)
    b = run("./mochila_bt", inp)
    c = run("./mochila_bb", inp)
    if not (a == b == c):
        fails += 1
        print("DIVERGENCIA:", a, b, c)
        print(inp)
        if fails > 5: break

print(f"Testes: 400 | Falhas: {fails}")
print("OK - os tres algoritmos concordam em todas as instancias" if fails == 0 else "ATENCAO: ha divergencias")

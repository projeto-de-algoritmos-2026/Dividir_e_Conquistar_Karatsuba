class Tracer:

    def entrar(self, x, y): pass
    def caso_base(self, x, y, r): pass
    def separar(self, x, y, n, m, x1, x0, y1, y0): pass
    def definir(self, x1, y1, soma_x, soma_y, x0, y0): pass
    def chamar(self, nome, a, b): pass
    def voltou(self, nome, valor): pass
    def montar(self, A, B, C, meio, m, resultado): pass
    def sair(self, resultado): pass


class TracerConsole(Tracer):

    def __init__(self):
        self.nivel = -1 

    def p(self, texto=""):
        print(f"{'│   ' * self.nivel}{texto}")

    def entrar(self, x, y):
        self.nivel += 1
        self.p(f"┌─ karatsuba(x={x:b}, y={y:b})")

    def caso_base(self, x, y, r):
        self.p(f"│  caso base (algum número tem 1 bit): {x:b} · {y:b} = {r:b}")

    def separar(self, x, y, n, m, x1, x0, y1, y0):
        self.p(f"│  n = {n} bits, m = n/2 = {m}")
        self.p(f"│  x = {x:b} (={x})")
        self.p(f"│     x1 = {x1:b}   x0 = {x0:b}")
        self.p(f"│  y = {y:b} (={y})")
        self.p(f"│     y1 = {y1:b}   y0 = {y0:b}")

    def definir(self, x1, y1, soma_x, soma_y, x0, y0):
        self.p("│")
        self.p("│  Definindo:")
        self.p(f"│     A = x1·y1           = {x1:b} · {y1:b}")
        self.p(f"│     B = (x1+x0)·(y1+y0) = {soma_x:b} · {soma_y:b}")
        self.p(f"│     C = x0·y0           = {x0:b} · {y0:b}")
        self.p("│")
        self.p("│  Resolvendo A, B e C:")

    def chamar(self, nome, a, b):
        self.p(f"│  >> {nome}: chamando recursivamente karatsuba({a:b}, {b:b})")

    def voltou(self, nome, valor):
        self.p(f"│  << voltou da recursão: {nome} = {valor:b}")

    def montar(self, A, B, C, meio, m, resultado):
        self.p("│")
        self.p("│  Montando o resultado:")
        self.p(f"│     x·y = 2^{2*m}·A + 2^{m}·(B - A - C) + C")
        self.p(f"│     x·y = 2^{2*m}·({A:b}) + 2^{m}·({B:b} - {A:b} - {C:b}) + {C:b}")
        self.p(f"│     x·y = 2^{2*m}·({A:b}) + 2^{m}·({meio:b}) + {C:b}")
        self.p(f"│     x·y = {A << (2*m):b} + {meio << m:b} + {C:b}")
        self.p(f"│     x·y = {resultado:b} (={resultado})")

    def sair(self, resultado):
        self.p(f"└─ retorna {resultado:b}")
        self.nivel -= 1
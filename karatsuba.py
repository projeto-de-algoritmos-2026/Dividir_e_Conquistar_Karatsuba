# karatsuba.py
"""Karatsuba em binário: só o algoritmo, sem nenhum print."""

from bits import tamanho, dividir, deslocar
from tracer import Tracer


def karatsuba(x, y, tracer=None):
    if tracer is None:
        tracer = Tracer()  # não imprime nada

    tracer.entrar(x, y)

    # Caso base: algum número tem 1 bit
    if x < 2 or y < 2:
        r = x * y
        tracer.caso_base(x, y, r)
        tracer.sair(r)
        return r

    # 1) Separar x e y
    n = tamanho(x, y)
    m = n // 2
    x1, x0 = dividir(x, m)
    y1, y0 = dividir(y, m)
    tracer.separar(x, y, n, m, x1, x0, y1, y0)

    # 2) Definir A, B e C
    soma_x = x1 + x0
    soma_y = y1 + y0
    tracer.definir(x1, y1, soma_x, soma_y, x0, y0)

    # 3) Resolver A, B e C (recursão)
    tracer.chamar("A", x1, y1)
    A = karatsuba(x1, y1, tracer)
    tracer.voltou("A", A)

    tracer.chamar("B", soma_x, soma_y)
    B = karatsuba(soma_x, soma_y, tracer)
    tracer.voltou("B", B)

    tracer.chamar("C", x0, y0)
    C = karatsuba(x0, y0, tracer)
    tracer.voltou("C", C)

    # 4) Montar o resultado
    meio = B - A - C
    resultado = deslocar(A, 2 * m) + deslocar(meio, m) + C
    tracer.montar(A, B, C, meio, m, resultado)

    tracer.sair(resultado)
    return resultado
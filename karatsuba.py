from bits import tamanho, dividir, deslocar


def karatsuba(x, y):
    if x < 2 or y < 2:
        return x * y

    n = tamanho(x, y)
    m = n // 2
    x1, x0 = dividir(x, m)
    y1, y0 = dividir(y, m)

    A = karatsuba(x1, y1)
    C = karatsuba(x0, y0)
    B = karatsuba(x1 + x0, y1 + y0)

    meio = B - A - C
    return deslocar(A, 2 * m) + deslocar(meio, m) + C
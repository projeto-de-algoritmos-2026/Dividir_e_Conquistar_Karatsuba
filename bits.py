def tamanho(x, y):
    """Quantidade de bits (n) do maior entre x e y."""
    return max(x.bit_length(), y.bit_length())

def dividir(x, m):
    """Separa x em (parte alta, parte baixa): x = alta*2^m + baixa."""
    alta = x >> m
    baixa = x & ((1 << m) - 1)
    return alta, baixa

def deslocar(x, k):
    """Multiplica x por 2^k (shift para a esquerda)."""
    return x << k
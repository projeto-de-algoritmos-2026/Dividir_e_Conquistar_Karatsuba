import random

import pytest

from karatsuba import karatsuba
from tracer import Tracer


def test_exemplo_do_quadro():
    # 1011 * 1001 = 11 * 9 = 99 = 1100011
    assert karatsuba(0b1011, 0b1001) == 0b1100011


@pytest.mark.parametrize(
    "x, y",
    [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        (0, 12345),
        (12345, 0),
        (1, 12345),
        (12345, 1),
        (2, 2),
        (2, 3),
        (3, 3),
        (3, 2),
    ],
)
def test_casos_de_borda(x, y):
    assert karatsuba(x, y) == x * y


@pytest.mark.parametrize("k", range(1, 40))
def test_potencias_de_2(k):
    assert karatsuba(2**k, 2**k) == 2 ** (2 * k)
    assert karatsuba(2**k, 7) == 7 * 2**k


@pytest.mark.parametrize("k", range(1, 40))
def test_todos_os_bits_1(k):
    # 2^k - 1 = 111...1 (pior caso de "vai-um" nas somas x1+x0)
    x = 2**k - 1
    assert karatsuba(x, x) == x * x


@pytest.mark.parametrize(
    "x, y",
    [
        (0b1, 0b1111),
        (0b101, 0b1111111),
        (0b1011, 0b1),
        (255, 3),
        (3, 255),
        (2**64 + 1, 5),
        (123456789, 98765),
    ],
)
def test_tamanhos_diferentes(x, y):
    assert karatsuba(x, y) == x * y


def test_comutativa():
    rng = random.Random(1)
    for _ in range(100):
        x, y = rng.getrandbits(32), rng.getrandbits(32)
        assert karatsuba(x, y) == karatsuba(y, x)


def test_aleatorios_pequenos():
    rng = random.Random(42)
    for _ in range(500):
        x, y = rng.randrange(0, 2**16), rng.randrange(0, 2**16)
        assert karatsuba(x, y) == x * y


@pytest.mark.parametrize("bits", [8, 16, 32, 64, 128, 256, 512])
def test_aleatorios_por_tamanho(bits):
    rng = random.Random(bits)
    for _ in range(50):
        x, y = rng.getrandbits(bits), rng.getrandbits(bits)
        assert karatsuba(x, y) == x * y


def test_numeros_gigantes():
    rng = random.Random(7)
    x, y = rng.getrandbits(4000), rng.getrandbits(4000)
    assert karatsuba(x, y) == x * y


def test_exaustivo_ate_6_bits():
    for x in range(64):
        for y in range(64):
            assert karatsuba(x, y) == x * y, f"falhou em {x} * {y}"


def test_sem_tracer_nao_imprime_nada(capsys):
    karatsuba(0b1011, 0b1001)
    assert capsys.readouterr().out == ""


def test_tracer_vazio_explicito_nao_imprime_nada(capsys):
    karatsuba(0b1011, 0b1001, Tracer())
    assert capsys.readouterr().out == ""


class Gravador(Tracer):
    """Tracer de teste: só anota quais métodos foram chamados."""

    def __init__(self):
        self.eventos = []

    def entrar(self, x, y):
        self.eventos.append("entrar")

    def caso_base(self, x, y, r):
        self.eventos.append("caso_base")

    def separar(self, *args):
        self.eventos.append("separar")

    def definir(self, *args):
        self.eventos.append("definir")

    def chamar(self, nome, a, b):
        self.eventos.append(f"chamar_{nome}")

    def voltou(self, nome, valor):
        self.eventos.append(f"voltou_{nome}")

    def montar(self, *args):
        self.eventos.append("montar")

    def sair(self, resultado):
        self.eventos.append("sair")


class TestTracerEhChamadoCorretamente:
    def test_todo_entrar_tem_um_sair(self):
        g = Gravador()
        karatsuba(0b1011, 0b1001, g)
        assert g.eventos.count("entrar") == g.eventos.count("sair")

    def test_comeca_com_entrar_e_termina_com_sair(self):
        g = Gravador()
        karatsuba(0b1011, 0b1001, g)
        assert g.eventos[0] == "entrar"
        assert g.eventos[-1] == "sair"

    def test_caso_base_nao_separa_nem_recursa(self):
        g = Gravador()
        karatsuba(1, 1, g)
        assert g.eventos == ["entrar", "caso_base", "sair"]

    def test_tres_chamadas_recursivas_por_nivel_nao_base(self):
        g = Gravador()
        karatsuba(0b10, 0b10, g)  # n = 2: separa e faz 3 chamadas base
        assert g.eventos.count("separar") == 1
        assert g.eventos.count("chamar_A") == 1
        assert g.eventos.count("chamar_B") == 1
        assert g.eventos.count("chamar_C") == 1
        assert g.eventos.count("caso_base") == 3

    def test_ordem_a_b_c(self):
        g = Gravador()
        karatsuba(0b10, 0b10, g)
        ordem = [e for e in g.eventos if e.startswith("chamar_")]
        assert ordem == ["chamar_A", "chamar_B", "chamar_C"]

    def test_cada_chamar_tem_seu_voltou(self):
        g = Gravador()
        karatsuba(0b1011, 0b1001, g)
        for nome in "ABC":
            assert g.eventos.count(f"chamar_{nome}") == g.eventos.count(f"voltou_{nome}")

    def test_chamadas_recursivas_sao_multiplo_de_3(self):
        g = Gravador()
        karatsuba(2**20 + 12345, 2**20 + 54321, g)
        total = sum(g.eventos.count(f"chamar_{n}") for n in "ABC")
        assert total % 3 == 0
        # cada chamada recursiva gera exatamente um "entrar"
        assert g.eventos.count("entrar") == total + 1

    def test_contagem_de_casos_base_cresce_menos_que_quadratico(self):
        """Dobrar o tamanho deve multiplicar os casos base por ~3 (e não por 4)."""

        def casos_base(bits):
            g = Gravador()
            karatsuba(2**bits - 1, 2**bits - 1, g)
            return g.eventos.count("caso_base")

        for bits in (8, 16, 32, 64):
            assert casos_base(2 * bits) <= 4 * casos_base(bits) * 0.8
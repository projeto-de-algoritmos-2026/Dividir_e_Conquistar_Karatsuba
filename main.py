from karatsuba import karatsuba
from tracer import TracerConsole


def main():
    x, y = 0b1011, 0b1001  # exemplo do quadro: 11 * 9 = 99

    r = karatsuba(x, y, TracerConsole())

    print()
    print(f"Karatsuba: {r:b} ({r})")
    print(f"Normal:    {x * y:b} ({x * y})")
    print("Correto!" if r == x * y else "ERRO!")


if __name__ == "__main__":
    main()
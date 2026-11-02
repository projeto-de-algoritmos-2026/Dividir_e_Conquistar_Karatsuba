from karatsuba import karatsuba

def main():
    x, y = 0b1011, 0b1001
    r = karatsuba(x, y)
    print(f"Karatsuba: {r:b} ({r})")
    print(f"Normal:    {x * y:b} ({x * y})")
    print("Correto!" if r == x * y else "ERRO!")


if __name__ == "__main__":
    main()
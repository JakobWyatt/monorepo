
def even_fib():
    sum = 0
    fib1 = 1
    fib2 = 1
    # temp = fib2
    # fib2 += fib1
    # fib1 = temp
    while fib2 < 4_000_000:
        if fib2 % 2 == 0:
            sum += fib2
        temp = fib2
        fib2 += fib1
        fib1 = temp
    return sum

if __name__ == "__main__":
    print(even_fib())

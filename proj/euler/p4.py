


def is_palindrome(x):
    s = str(x)
    for i in range(len(s) // 2):
        if s[i] != s[-i - 1]:
            return False
    return True

def ndigit_palindrome_products(n):
    palindrome_products = []
    for i in reversed(range(10 ** (n - 1), 10 ** n)):
        for j in reversed(range(i, 10 ** n)):
            if is_palindrome(i * j):
                palindrome_products.append(i * j)
    return palindrome_products

if __name__ == "__main__":
    print(max(ndigit_palindrome_products(3)))

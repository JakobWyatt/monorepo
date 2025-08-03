import math

def make_primes(max_prime):
    primes = [] # initial sieve
    for x in range(2, max_prime):
        is_prime = True
        max_factor = math.ceil(math.sqrt(x))
        for p in primes:
            if p > max_factor:
                break
            if x % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(x)
    return primes

def largest_prime_factor(x):
    # generate primes up to sqrt(x)
    # check divisibility from highest -> lowest
    max_prime = math.ceil(math.sqrt(x))
    primes = make_primes(max_prime)
    for p in reversed(primes):
        if x % p == 0:
            return p
    return x

if __name__ == "__main__":
    print(largest_prime_factor(600851475143))

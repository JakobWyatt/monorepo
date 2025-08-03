import math

def make_primes(max_prime):
    primes = [] # initial sieve
    for x in range(2, max_prime + 1):
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

def prime_factors(x):
    max_prime = math.ceil(math.sqrt(x))
    primes = make_primes(max_prime)
    factors = []
    i = 0
    while i < len(primes):
        p = primes[i]
        if x % p == 0:
            factors.append(p)
        else:
            i += 1
    return factors

# for 20 (2 * 2 * 5) given (2, 3, 5, 7, 11) will return (2, 0, 1, 0, 0)
def prime_factors_sparse(primes, x):
    factors = [0] * len(primes)
    i = 0
    while i < len(primes):
        p = primes[i]
        if x % p == 0:
            x = x // p
            factors[i] += 1
        else:
            i += 1
    return factors

def from_prime_factors_sparse(primes, sparse_factors):
    assert(len(primes) == len(sparse_factors))
    result = 1
    for p, f in zip(primes, sparse_factors):
        result *= p ** f
    return result

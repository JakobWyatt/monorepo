import math
import util

def max_factors_to_n(n):
    # for each number find prime factors
    # find MAX repeating prime factors for each number
    primes = util.make_primes(n)
    max_factors = [0] * len(primes)
    for x in range(2, n):
        sparse = util.prime_factors_sparse(primes, x)
        assert(len(sparse) == len(max_factors))
        for i, s in enumerate(sparse):
            max_factors[i] = max(max_factors[i], s)
    return util.from_prime_factors_sparse(primes, max_factors)

if __name__ == "__main__":
    print(max_factors_to_n(50000))

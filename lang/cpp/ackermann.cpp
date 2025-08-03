#include <iostream>
#include <vector>
#include <gmpxx.h>
#include <math.h>

//constexpr unsigned int mmax = 5;
//constexpr unsigned int nmax = 20;

mpz_class cache_ackermann(int m, mpz_class n);
mpz_class ackermann(int m, mpz_class n);

int main()
{
    /*for (unsigned int i = 0; i != mmax; i++)
    {
        for (unsigned int j = 0; j != nmax; j++)
        {
            std::cout << "Ack(" << i << ", " << j << ") = " << cache_ackermann(i, j) << std::endl;
        }
    }*/

    std::cout << cache_ackermann(4, 2);

    return 0;
}

mpz_class ackermann(int m, mpz_class n)
{
    if (m == 0)
    {
        return n + 1;
    } else if (n == 0)
    {
        return cache_ackermann(m - 1, 1);
    } else {
        return cache_ackermann(m - 1, cache_ackermann(m, n - 1));
    }
}

mpz_class opt_ackermann(int m, mpz_class n)
{
    if (m == 2)
    {
        return 3 + n * 2;
    } else if (m < 2)
    {
        return m + n + 1;
    } else if (m == 3)
    {
        return pow(2, n + 3) - 3;
    }
    else {
        return ackermann(m, n);
    }
}

mpz_class cache_ackermann(int m, mpz_class n)
{
    static std::vector<std::vector<mpz_class>> cache;

    if (m < 4)
    {
        return opt_ackermann(m, n);
    } else {
        while (cache.size() <= m - 4)
        {
            std::vector<mpz_class> temp = {};
            cache.push_back(temp);
        }
        size_t i = cache[m - 4].size();
        while (cache[m - 4].size() <= n)
        {
            std::cout << "Generating ack(" << m << ", " << i << ")\n";
            cache[m - 4].push_back(opt_ackermann(m, i));
            i++;
        }
        return cache[m - 4][n.get_ui()];
    }
}

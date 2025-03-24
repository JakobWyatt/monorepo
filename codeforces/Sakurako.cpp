/*
5
0 1
0 3
2 0
2 3
3 1

0 ones, 1 twos.
NO.
0, 3.
NO.
2, 0.
YES.
2, 3.
YES.

Anytime the number of ones is odd, the solution is impossible.
IF the number of twos is odd, we must have AT LEAST 2 in the ones column.
*/

#include <iostream>

bool sumZero(int a, int b)
{
    if (a % 2 != 0)
    {
        return false;
    }
    if (b % 2 != 0 && a < 2)
    {
        return false;
    }
    return true;
}

int main()
{
    size_t size = 0;
    int a = 0;
    int b = 0;
    std::cin >> size;
    for (size_t i = 0; i != size; ++i)
    {
        std::cin >> a >> b;
        if (sumZero(a, b))
        {
            std::cout << "YES\n";
        } else
        {
            std::cout << "NO\n";
        }
    }
}

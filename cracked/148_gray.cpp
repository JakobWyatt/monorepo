
// Gray code is a binary code where each successive value differs by only one bit.
// Generate a gray code given a number of bits n.
// e.g. n == 2 00 01 11 10
// can rotate the ordering (rot 1)
// 10 00 01 11

// some examples
// 0 1
// "as well as wrapping around"
// n == 3 010 000 001 011 111 101 100 110
// rotate 3 101 100 110 010 000 001 011 111

// n == 4 0101 0100 0110 0010 0000 0001 0011 0111 1111 1011 1001 1000 1010 1110 1100 1101
// rot 7, 1 past the middle 2 ^ (4 - 1) - 1

/// 00 01 10 11
// 000 001 010 011 100 101 110 111

#include <bitset>
#include <iostream>
#include <deque>
#include <bit>

template<typename T>
void RotateQueueRight(std::deque<T>& in, size_t rot)
{
    if (in.empty())
    {
        return;
    }
    for (size_t i = 0; i != rot; ++i)
    {
        in.emplace_back(in.front());
        in.pop_front();
    }
}

std::deque<uint64_t> GenerateGrayCode(int n)
{
    if (n < 1)
    {
        return {};
    }
    if (n == 1)
    {
        return {0, 1};
    }
    uint64_t halfSz = 1 << (n - 1);
    auto last = GenerateGrayCode(n - 1);
    RotateQueueRight(last, halfSz / 2 + 1);
    for (int64_t i = halfSz - 1; i >= 0; --i)
    {
        last.push_back(last.at(i) + halfSz);
    }

    return last;
}

void ValidateGrayCode(std::deque<uint64_t> in, int n)
{
    if (in.size() != 1 << n)
    {
        std::cout << "FAIL (element count) has: " << in.size() << " needs: " << (1 << n) << "\n";
    }
    // validate that we differ by one
    for (size_t i = 0; i != in.size(); ++i)
    {
        uint64_t cur = in.at(i);
        uint64_t next = in.at((i + 1) % in.size());
        if (std::popcount(cur ^ next) != 1)
        {
            std::cout << "FAIL (not off by one) " << cur << " " << next << "\n";
        }
    }
    // validate that we cover every value
    std::sort(in.begin(), in.end());
    uint64_t val = 0;
    for (auto c : in)
    {
        if (c != val)
        {
            std::cout << "FAIL (missed value) " << c << "\n";
        }
        ++val;
    }
    std::cout << "Validated " << in.size() << " elements.\n";
}

int main()
{
    constexpr int n = 20;
    auto code = GenerateGrayCode(n);
    ValidateGrayCode(code, n);
    for (int c : code)
    {
        std::cout << std::bitset<n>(c) << " ";
    }
    std::cout << std::endl;
}

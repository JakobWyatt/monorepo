#include <cassert>
#include <charconv>
#include <cstdlib>
#include <print>
#include <vector>

// n even, n / 2
// n odd, 3 * n + 1

// naive - faster than cached
// time ./release 100000000
// collatz cycle 63728127 has length 950
// real 0m22.574s

constexpr size_t CACHE_SZ = 1'000'000;

int64_t CollatzNext(int64_t x)
{
    if (x % 2 == 0) {
        return x / 2;
    }
    bool failure = __builtin_mul_overflow(x, 3, &x);
    failure = failure || __builtin_add_overflow(x, 1, &x); // optimize?
    if (failure) [[unlikely]] {
        std::println("integer overflow");
        std::exit(EXIT_FAILURE);
    }
    return x;
}

int64_t FindCollatzLength(int64_t x, std::vector<int64_t>& cache)
{
    std::vector<int64_t> visited;
    int64_t length = 1;
    while (x > 1) [[likely]] {
        if (x < CACHE_SZ) {
            int64_t cached = cache[x];
            if (cached != -1) {
                length += cached;
                x = 1;
            } else {
                visited.push_back(x);
                x = CollatzNext(x);
                ++length;
            }
        } else {
            x = CollatzNext(x);
            ++length;
        }
    }
    for (size_t i = 0; i < visited.size(); ++i) {
        cache[visited[i]] = length - i - 1;
    }
    return length;
}

int64_t FindCollatzLength(int64_t x)
{
    int64_t length = 1;
    while (x > 1) [[likely]] {
        x = CollatzNext(x);
        ++length;
    }
    return length;
}

void OutputCollatz(int64_t x)
{
    int64_t maxval = 0;
    int64_t maxlen = 0;
    std::vector<int64_t> cache(CACHE_SZ, -1);
    for (int64_t i = 1; i <= x; ++i) {
        auto length = FindCollatzLength(i, cache);
        if (length > maxlen) {
            maxlen = length;
            maxval = i;
        }
    }
    std::println("collatz cycle {} has length {}", maxval, maxlen);
}

int main(int argc, char** argv)
{
    // input
    if (argc != 2) {
        std::println("usage: ./collatz <maxlen>");
        return EXIT_FAILURE;
    }
    int64_t n = 0;
    char const* const end = argv[1] + strlen(argv[1]);
    auto res = std::from_chars(argv[1], end, n);
    if (res.ec != std::errc {} || res.ptr != end) {
        std::println("invalid input");
        return EXIT_FAILURE;
    }
    if (n < 1) {
        std::println("input < 1");
        return EXIT_FAILURE;
    }
    OutputCollatz(n);
}

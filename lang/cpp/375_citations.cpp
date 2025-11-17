#include <algorithm>
#include <cassert>
#include <print>
#include <vector>

// O(nlogn)
int CalculateHIndex(std::vector<int> citations)
{
    std::ranges::sort(citations, std::greater<>());
    size_t i = 0;
    while (i < citations.size() && citations.at(i) >= i + 1) {
        ++i;
    }
    return i;
}

// O(n) solution, H-Index bounded by citations.size()
int CalculateHIndexFast(std::vector<int> const& citations)
{
    std::vector<int> cache(citations.size() + 1, 0);
    for (auto const& value : citations) {
        assert(value >= 0);
        if (value >= cache.size()) {
            ++cache.back();
        } else {
            ++cache.at(value);
        }
    }
    int cumulativePapers = 0;
    while (cache.size() - 1 > cumulativePapers) {
        cumulativePapers += cache.back();
        cache.pop_back();
    }
    return cumulativePapers;
}

int main()
{
    std::vector<int> citations { 4, 0, 0, 2, 3 };
    std::println("H-Index: {} Citations: {}", CalculateHIndexFast(citations), citations);
}

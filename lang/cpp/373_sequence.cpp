#include <cassert>
#include <print>
#include <unordered_map>
#include <vector>

int MaximumConsecutiveSequenceLength(std::vector<int> const& input)
{
    // pass 1, presence map
    using HighestValue = std::optional<int>;
    std::unordered_map<int, HighestValue> cache;
    for (int a : input) {
        cache[a] = std::nullopt;
    }
    // pass 2, find max value of each subsequence
    // cache prevents elements from being revisited
    for (int a : input) {
        if (cache.at(a).has_value()) {
            continue;
        }
        int next = a + 1;
        while (cache.contains(next) && !cache.at(next).has_value()) {
            ++next;
        }
        int highest = next - 1;
        if (cache.contains(next)) {
            highest = cache.at(next).value();
        }
        --next;
        while (next >= a) {
            // validate that each element is only touched once
            assert(!cache.at(next).has_value());
            cache.at(next) = highest;
            --next;
        }
    }
    // pass 3, find max length
    int maxLength = 0;
    for (auto const [value, maximum] : cache) {
        assert(maximum.has_value());
        int const length = *maximum - value + 1;
        maxLength = std::max(maxLength, length);
    }
    return maxLength;
}

int main()
{
    std::vector<int> sequence { 5, 2, 99, 3, 4, 1, 100 };
    std::println("sequence {} has maximum consecutive length {}", sequence, MaximumConsecutiveSequenceLength(sequence));
}

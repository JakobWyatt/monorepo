#include <optional>
#include <print>
#include <vector>

// worst case O(n)
std::optional<int> NaiveLowestIndex(std::vector<int> const& input)
{
    for (size_t i = 0; i != input.size(); ++i) {
        if (input[i] == i) {
            return i;
        }
    }
    return std::nullopt;
}

std::optional<int> BinSearchLowestIndex(std::vector<int> const& input)
{
    size_t left = 0;
    size_t right = input.size();

    while (left < right) {
        int midpoint = (left + right) / 2;
        if (midpoint > input.at(midpoint)) {
            left = midpoint + 1;
        } else {
            right = midpoint;
        }
    }
    if (left < input.size() && input.at(left) == left) {
        return left;
    }
    return std::nullopt;
}

std::optional<int> BinSearchHighestIndex(std::vector<int> const& input)
{
    size_t left = 0;
    size_t right = input.size();

    while (left < right) {
        int midpoint = (left + right) / 2;
        if (midpoint >= input.at(midpoint)) {
            left = midpoint + 1;
        } else {
            right = midpoint;
        }
    }
    --left;
    if (left < input.size() && input.at(left) == left) {
        return left;
    }
    return std::nullopt;
}

int main()
{
    std::vector<int> input = { -5, -3, 2, 3, 4, 5, 15 };
    auto indexLow = BinSearchLowestIndex(input);
    auto indexHigh = BinSearchHighestIndex(input);
    if (indexLow.has_value() && indexHigh.has_value()) {
        std::println("{} -> {}", *indexLow, *indexHigh);
    } else {
        std::println("null");
    }
}

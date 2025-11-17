// print out the median of each window of size k
// use a 'left heap' including the odd median value, and a 'right heap' with n / n - 1 elements.
// when deleting a value, decrement the size of the heap, mark element as valid or invalid.

#include <cassert>
#include <cstddef>
#include <print>
#include <queue>
#include <span>
#include <unordered_map>

class MedianHeap {
public:
    void insert(int x);
    void erase(int x);
    [[nodiscard]] double median() const;

private:
    void balance();
    void prune();

    std::unordered_map<int, int /* count */> deleted;
    std::priority_queue<int> left;
    std::priority_queue<int, std::vector<int>, std::greater<>> right;
    size_t leftCount = 0;
    size_t rightCount = 0;
};

void MedianHeap::prune()
{
    while (!left.empty() && deleted[left.top()] > 0) {
        --deleted[left.top()];
        left.pop();
    }
    while (!right.empty() && deleted[right.top()] > 0) {
        --deleted[right.top()];
        right.pop();
    }
}

void MedianHeap::balance()
{
    if (rightCount > leftCount) {
        auto elem = right.top();
        right.pop();
        left.push(elem);
        ++leftCount;
        --rightCount;
    } else if (leftCount > rightCount + 1) {
        auto elem = left.top();
        left.pop();
        right.push(elem);
        ++rightCount;
        --leftCount;
    }
    assert(leftCount == rightCount || leftCount == rightCount + 1);
    prune();
    assert(left.empty() || right.empty() || left.top() <= right.top());
}

void MedianHeap::insert(int x)
{
    if (left.empty() || x <= left.top()) {
        left.emplace(x);
        ++leftCount;
    } else {
        right.emplace(x);
        ++rightCount;
    }
    balance();
}

void MedianHeap::erase(int x)
{
    if (x <= left.top()) {
        --leftCount;
        ++deleted[x];
    } else {
        --rightCount;
        ++deleted[x];
    }
    balance();
}

double MedianHeap::median() const
{
    assert(leftCount != 0);
    if (leftCount == rightCount) {
        return (left.top() + right.top()) / 2.0;
    }
    return left.top();
}

std::vector<double> FindWindows(std::vector<int> const& arr, int k)
{
    assert(arr.size() >= k && k > 0);
    std::vector<double> result;
    result.reserve(arr.size());

    MedianHeap cache;

    for (int i = 0; i != k; ++i) {
        cache.insert(arr.at(i));
    }

    for (int i = k; i < arr.size(); ++i) {
        result.push_back(cache.median());
        cache.insert(arr.at(i));
        cache.erase(arr.at(i - k));
    }
    result.push_back(cache.median());

    return result;
}

int main()
{
    std::vector<int> const input = { -1, 5, 13, 8, 2, 3, 3, 1 };
    int const window = 3;
    auto result = FindWindows(input, window);
    for (size_t i = 0; i != result.size(); ++i) {
        std::println("{} <- median of {}", result.at(i),
            std::span { input }.subspan(i, window));
    }
}

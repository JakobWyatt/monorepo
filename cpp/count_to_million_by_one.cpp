#include <iostream>
#include <vector>
#include <numeric>
#include <cstdint>
#include <string>
#include <chrono>

//converts all elements in a SequenceContainer
//to a string, given that those elements define a 
//	std::ostream& operator<<(std::ostream&, T&)
//	member function
//these elements are seperated by spaces
template<typename T> auto vec_to_string(const T& sequence_container) {
	std::string s;
	for (auto& i : sequence_container) {
		s += std::to_string(i) + " ";
	}
	return s;
};

void all_at_once() {
    std::vector<std::uint32_t> one_million(100000000);
    std::iota(one_million.begin(), one_million.end(), 1);

    std::cout << vec_to_string(one_million);
}

void one_at_a_time() {
	for(std::uint32_t i = 0; i != 100000000; ++i) {
		std::cout << i << " ";
	}
}

int main () {
	std::ios::sync_with_stdio(false);
	auto time1 = std::chrono::steady_clock::now();
	all_at_once();
	auto time2 = std::chrono::steady_clock::now();
	//one_at_a_time();
	//auto time3 = std::chrono::steady_clock::now();

	auto duration_fast = time2 - time1;
	//auto duration_slow = time3 - time2;

	std::cout << "\n\n\n\n\nFast: " << duration_fast.count();// << "\nSlow: " << duration_slow.count() << "\n\n";

    return 0;
}
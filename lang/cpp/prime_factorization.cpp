#include <chrono>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

//sets the indexes that are multiples of sieve_width to false,
//	without modifying the original sieve_with value
//for example, sieve_vec({true, true, true, true, true, true}, 2)
//	would return {true, true, true, false, true, false}
//	because 4 and 6 are multiples of 2
//and sieve_vec({true, true, true, true, true, true}, 3)
//	would return {true, true, true, true, true, false}
//	because 6 is a multiple of 3
template<typename T> void sieve_vec(std::vector<bool>& to_sieve, T sieve_with) {
	if (sieve_with < 2) {
		throw std::invalid_argument("We cannot sieve a vector with a number less than 2");
	}
	auto vec_size = to_sieve.size();
	for (std::int64_t i = sieve_with * 2; i < vec_size; i += sieve_with) {
		to_sieve[i] = false;
	}
}

//iterates over the elements of a vec<bool>
//if the element is true, then the index of this element is pushed onto a new vector,
//	which is returned
template<typename T> std::vector<T> generate_elem_vec_from_bool_vec(std::vector<bool>& vec) {
	std::vector<T> elem_vec;
	auto bool_vec_size = vec.size();
	for (auto i = 0; i != bool_vec_size; ++i) {
		if (vec[i] == true) {
			elem_vec.push_back(i);
		}
	}
	
	return elem_vec;
}

//generates a vector of primes less than the specified number
template<typename T> auto generate_primes(T limit) {
	//there are no primes below 2
	if (limit < 3) {
		return std::vector<T>();
	}

	//we shall use a sieve method to generate our primes
	std::vector<bool> sieve(limit, true);
	sieve[0] = false;
	sieve[1] = false;

	//naive algorithm loops through all elements in vector for now
	//we can refine it in future to not check even numbers

	//if an element in our vector is prime,
	//	we will eliminate all multiples of the number
	auto sieve_size = sieve.size();
	for (auto i = 0; i != sieve_size; ++i) {
		if (sieve[i] == true) {
			sieve_vec(sieve, i);
		}
	}

	return generate_elem_vec_from_bool_vec<T>(sieve);
}

//converts any object to a string, given that it has a
//	std::ostream& operator<<(std::ostream&, T&)
//	member function
template<typename T> auto to_string(const T& to_convert) {
	std::ostringstream s;
	s << to_convert;
	return s.str();
}

//converts all elements in a SequenceContainer
//to a string, given that those elements define a 
//	std::ostream& operator<<(std::ostream&, T&)
//	member function
//these elements are seperated by spaces
template<typename T> auto vec_to_string(const T& sequence_container) {
	std::string s;
	for (auto& i : sequence_container) {
		s += to_string(i) + " ";
	}
	return s;
};

//finds prime factors of a given number
//primes must contain all primes up to and including to_factorize
//to factorize must not be less than 2
template<typename T> auto find_prime_factors(T to_factorize, std::vector<T>& primes) {
	if (to_factorize < 2) {
		throw std::invalid_argument("any number less than 2 has no prime factors");
	}
	std::vector<T> prime_factors;
	typename std::vector<T>::size_type i = 0;
	//brute force method, beginning at small primes
	while (to_factorize != 1) {
		if (to_factorize % primes[i] == 0) {
			to_factorize /= primes[i];
			prime_factors.push_back(primes[i]);
		} else {
			++i;
		}
	}

	return prime_factors;
}

int main()
{
	/*
	const std::uint64_t max_num_to_factorize = 1000000;
	std::cout << "Finding prime factors of all numbers up to " << max_num_to_factorize << ".\n";

	std::cout << "Generating prime list...";
	auto before_prime_gen = std::chrono::steady_clock::now();

	//we will generate all primes up to num_to_factorise,
	//	however a future optimization is only generating 
	//	primes up to num_to_factorize/2
	auto primes = generate_primes(max_num_to_factorize);

	auto after_prime_gen = std::chrono::steady_clock::now();
	auto prime_calc_duration = after_prime_gen - before_prime_gen;
	//convert duration from nanoseconds to milliseconds
	std::cout << prime_calc_duration.count() / 1000000 << "ms\n";

	std::string s;
	for (std::int64_t i = 2; i != max_num_to_factorize; ++i) {
		auto prime_factors = find_prime_factors<std::uint64_t>(i, primes);
		s += "The prime factors of " + std::to_string(i) + " are " + vec_to_string(prime_factors) + "\n";
	}
	std::cout << s; */
 
	auto primes = generate_primes(1000000000);
	std::cout << "Finished generating\n";
	std::cout << "Number of primes: " << primes.size() << std::endl;
	std::cout << vec_to_string<>(primes);

    return 0;
}

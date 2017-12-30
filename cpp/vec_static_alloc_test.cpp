#include <vector>
#include <array>
#include <iostream>
#include <numeric>
#include <cstddef>

//This program verifies that std::array is statically allocated within std::vector,
//And is therefore fully contiguous.
//This is one of the few ways to easily implement cache-friendly nested containers,
//without delving into memory arenas and other such structures.
int main() {
    enum : std::size_t {
        array_size = 10,
        vec_size = 5,
    };

    auto ascending_array = [](){
        std::array<int, array_size> a;
        std::iota(a.begin(), a.end(), 0);
        return a; 
    };
    //create a vector of statically allocated std::arrays
    std::vector<std::array<int, array_size>> vec(vec_size, ascending_array());

    //our pointer to the first element of the first array in the vector
    int* ptr = &vec[0][0];

    //we then loop though this vector with our pointer, outputting the value of the dereferenced pointer.
    //std::vector is guarenteed by the c++ standard to be contiguous
    //std::array is statically allocated and contiguous
    //therefore this loop should print: "0 1 2 3 ... array_size", vec_size times.
    //If it doesnt, then static allocation within containers is bugged.
    for (std::size_t i = 0; i != array_size * vec_size; ++i) {
        std::cout << *ptr << " ";
        ++ptr;
    }

    return 0;
}
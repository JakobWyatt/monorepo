#include <array>
#include <cassert>
#include <iostream>
#include <new>
#include <print>
#include <string>
#include <string_view>
#include <vector>

std::vector<std::string> GenerateSubsequences(std::string const& str)
{
    size_t count = 1 << str.size();
    std::vector<std::string> result;
    result.reserve(count);
    for (size_t i = 0; i != count; ++i) {
        std::string sequence;
        sequence.reserve(str.size());
        for (size_t j = 0; j != str.size(); ++j) {
            bool const select = (i >> j) & 1;
            if (select) {
                sequence += str.at(j);
            }
        }
        result.emplace_back(sequence);
    }
    return result;
}

void StreamSubsequences(std::string const& str, std::ostream& out)
{
    // only flush buffer to ostream
    std::array<char, std::hardware_destructive_interference_size> buffer;
    std::string_view bufferView(buffer.data(), buffer.max_size());
    size_t bufferSize = 0;

    auto write = [&](char c) {
        buffer[bufferSize++] = c;
        if (bufferSize == buffer.max_size()) [[unlikely]] {
            out << bufferView;
            bufferSize = 0;
        }
    };

    for (size_t i = 0; i != 1 << str.size(); ++i) {
        size_t mask = i;
        while (mask) {
            write(str[std::countr_zero(mask)]);
            mask &= (mask - 1); // clear lowest bit
        }
        write('\n');
    }

    if (bufferSize != 0) [[unlikely]] {
        out << std::string_view(buffer.data(), bufferSize);
    }
}

int main(int argc, char** argv)
{
    if (argc != 2) {
        std::println("Usage: ./release <sequence>");
        return EXIT_FAILURE;
    }
    std::string input(argv[1]);
    StreamSubsequences(input, std::cout);
}

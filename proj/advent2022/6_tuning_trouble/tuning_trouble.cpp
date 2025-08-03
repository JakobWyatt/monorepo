#include <iostream>
#include <fstream>
#include <deque>
#include <unordered_map>
#include <chrono>
#include <array>

void insert_um(std::unordered_map<char, int>& um, char c) {
    if (!um.contains(c)) {
        um[c] = 0;
    }
    um[c] += 1;
}

void remove_um(std::unordered_map<char, int>& um, char c) {
    um[c] -= 1;
    if (um[c] == 0) {
        um.erase(um.find(c));
    }
}

// final version of puzzle takes 175800ns here
int find_start_of_packet(std::string s) {
    constexpr int contig = 14;
    std::unordered_map<char, int> um;
    um.reserve(26);
    // initial fill
    for (int i = 0; i != contig; ++i) {
        insert_um(um, s[i]);
    }
    // hot loop
    for (int i = contig; i != s.length(); ++i) {
        if (um.size() == contig) {
            return i;
        }
        insert_um(um, s[i]);
        remove_um(um, s[i - contig]);
    }
    return 0;
}

// lowercase chars
int find_start_of_packet_fast(std::string s) {
    constexpr int contig = 14;
    std::array<int, 26> charnum{};
    int charnumsz = 0;
    // initial fill
    for (int i = 0; i != contig; ++i) {
        if (charnum[s[i] - 'a'] == 0) {
            charnumsz += 1;
        }
        charnum[s[i] - 'a'] += 1;
    }
    // hot loop
    for (int i = contig; i != s.length(); ++i) {
        // check
        if (charnumsz == contig) {
            return i;
        }
        // insert
        if (charnum[s[i] - 'a'] == 0) {
            charnumsz += 1;
        }
        charnum[s[i] - 'a'] += 1;
        // remove
        if (charnum[s[i - contig] - 'a'] == 1) {
            charnumsz -= 1;
        }
        charnum[s[i - contig] - 'a'] -= 1;
    }
    return 0;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cout << "Usage: supply_stacks.exe <filename>";
    }
    // read top line from file
    auto file = std::ifstream(argv[1]);
    std::string line;
    std::getline(file, line);
    int pos = 0;
    constexpr int time_loops = 100;
    auto t1 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i != time_loops; ++i) {
        pos = find_start_of_packet_fast(line);
    }
    auto t2 = std::chrono::high_resolution_clock::now();
    auto dur = std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count() / time_loops;
    std::cout << "Answer was " << pos << " found in " << dur << "ns.\n";
    return 0;
}

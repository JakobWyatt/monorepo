#include <vector>
#include <string>
#include <iostream>

int main (int argc, char *argv[]) {
    std::vector<std::string> command_line_args(argv, argv + argc);

    for (auto& i : command_line_args) {
        std::cout << i << "\n";
    }
    return 0;
}

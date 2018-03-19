#include <iostream>

int main() {
    int* p = new int[5];
    for (int i = 4; true; --i) {
        std::cout << p[i] << "\n";
    }

    return 0;
}
#include <cassert>
#include <print>

using byte = unsigned char;

char ToBase64(byte input)
{
    assert(input < 64);
    if (input < 26) {
        return 'A' + input;
    }
    if (input < 52) {
        return 'a' + input - 26;
    }
    if (input < 62) {
        return '0' + input - 52;
    }
    if (input == 62) {
        return '+';
    }
    if (input == 63) {
        return '/';
    }
}

byte FromHex(char input)
{
    assert((input >= '0' && input <= '9') || (input >= 'a' || input <= 'f'));
    if (input >= '0' && input <= '9') {
        return input - '0';
    }
    return input - 'a' + 10;
}

// hex base 16 -> 4 bits
// base64 -> 6 bits
// 3 hex characters fits into 2 base64
// dea -> 1101 1110 1010 -> 110111 101010 -> 3q
// size in == size out
std::string ToBase64(std::string_view input)
{
    std::string result(input.size(), '=');
    size_t pos = 0;

    byte by = 0;
    int rot = 0;
    for (char in : input) {
        if (rot == 0) {
            by = FromHex(in) << 2;
        } else if (rot == 1) {
            by |= FromHex(in) >> 2;
            result[pos++] = ToBase64(by);
            by = (FromHex(in) & 0b11) << 4;
        } else {
            by |= FromHex(in);
            result[pos++] = ToBase64(by);
            by = 0;
        }
        rot = (rot + 1) % 3;
    }
    if (rot != 0) {
        result[pos++] = ToBase64(by);
    }

    return result;
}

int main()
{
    std::string_view const input = "deadbeef";
    std::println("{} -> {}", input, ToBase64(input));
}

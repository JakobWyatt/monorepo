#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <stack>
#include <utility>
#include <ranges>
#include <regex>

struct Move {
    int n;
    int from;
    int to;
};

typedef std::stack<char> Stack;

std::vector<Stack> parse_stacks(const std::vector<std::string>& stack_input, int n) {
    auto stacks = std::vector<Stack>(n);
    for (int i = 0; i != n; ++i) {
        for (const auto& line: stack_input | std::views::reverse) {
            char elem = line[4 * i + 1];
            if (elem != ' ') {
                stacks[i].push(elem);
            }
        }
    }
    return stacks;
}

Move parse_move(const std::string& s) {
    Move move;
    std::smatch match;
    std::regex re("move (\\d+) from (\\d+) to (\\d+)");
    std::regex_match(s, match, re);
    return {std::stoi(match[1].str()), std::stoi(match[2].str()) - 1, std::stoi(match[3].str()) - 1};
}

std::pair<std::vector<Move>, std::vector<Stack>> parse_input(std::ifstream& file) {
    // STACKS
    std::vector<std::string> stack_input;
    std::string line;
    do {
        std::getline(file, line);
        stack_input.push_back(line);
    } while (!line.empty()); // get stack description
    stack_input.pop_back();
    int n = (stack_input.back().length() + 1) / 4; // multiple of 4
    stack_input.pop_back();
    // MOVES
    std::vector<Move> moves;
    while (std::getline(file, line)) {
        moves.push_back(parse_move(line));
    }
    return std::make_pair(moves, parse_stacks(stack_input, n));
}

void execute_moves_9000(const std::vector<Move>& moves, std::vector<Stack>& stacks) {
    for (const auto& move: moves) {
        for (int i = 0; i != move.n; ++i) {
            stacks[move.to].push(stacks[move.from].top());
            stacks[move.from].pop();
        }
    }
}

void execute_moves_9001(const std::vector<Move>& moves, std::vector<Stack>& stacks) {
    Stack flip;
    for (const auto& move: moves) {
        for (int i = 0; i != move.n; ++i) {
            flip.push(stacks[move.from].top());
            stacks[move.from].pop();
        }
        while (!flip.empty()) {
            stacks[move.to].push(flip.top());
            flip.pop();
        }
    }
}

std::vector<char> get_stacks_top(const std::vector<Stack>& stacks) {
    std::vector<char> stacks_top;
    for (const auto& stack: stacks) {
        stacks_top.push_back(stack.top());
    }
    return stacks_top;
}

void print_stack(Stack s) {
    while (!s.empty()) {
        std::cout << s.top() << ' ';
        s.pop();
    }
}

void print_move(Move m) {
    std::cout << "move " << m.n << " from " << m.from << " to " << m.to << "\n";
}

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cout << "Usage: supply_stacks.exe <filename>";
    }
    auto file = std::ifstream(argv[1]);
    auto [moves, stacks] = parse_input(file);
    execute_moves_9001(moves, stacks);
    auto stacks_top = get_stacks_top(stacks);
    std::cout << std::string(stacks_top.begin(), stacks_top.end());
    return 0;
}

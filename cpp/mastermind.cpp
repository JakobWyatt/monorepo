#include <iostream>
#include <array>
#include <vector>

enum class pin {
    WHITE,
    YELLOW,
    PURPLE,
    BLUE,
    ORANGE,
    RED,
    VIOLET,
    GREEN
};

typedef std::array<pin, 4> code;

std::vector<code> generate_combinations()
{
    //nested for loops
    //because I am tired and can't think of a recursive sln
    std::vector<code> combinations;
    code temp;
    for ( int i = 0; i != 8; ++i )
    {
        temp[0]= (pin)i;
        for ( int j = 0; j != 8; ++j )
        {
            temp[1] = (pin)j;
            for ( int k = 0; k != 8; ++k )
            {
                temp[2] = (pin)k;
                for( int l = 0; l != 8; ++l )
                {
                    temp[3] = (pin)l;
                    combinations.push_back( temp );
                }
            }
        }
    }
    return combinations;
}

int main()
{
    std::vector<code> combinations = generate_combinations();
    return 0;
}

clang++-20 -Weverything -Wno-c++98-compat -Wno-missing-prototypes -std=c++26 -stdlib=libc++ -lc++abi -O3 -static -o release $1
clang++-20 -Weverything -Wno-c++98-compat -Wno-missing-prototypes -std=c++26 -stdlib=libc++ -lc++abi -O0 -g -static -o debug $1

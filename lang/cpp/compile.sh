FLAGS="clang++-20 -Weverything -Wno-unsafe-buffer-usage -Wno-c++98-compat -Wno-missing-prototypes -std=c++26 -stdlib=libc++ -lc++abi -static"
$FLAGS -O3 -o release $1
$FLAGS -O0 -g -o debug $1

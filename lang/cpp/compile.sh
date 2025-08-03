#!/bin/bash
docker run --rm -v "$PWD":/src -w /src silkeh/clang clang++ -Wall -Wextra -std=c++26 -stdlib=libc++ -lc++abi -pthread -fuse-ld=lld -static -O2 $1

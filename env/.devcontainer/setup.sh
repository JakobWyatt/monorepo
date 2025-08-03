#!/bin/bash
# package manager installs
sudo apt update
sudo apt upgrade
sudo apt install -y racket
sudo apt install -y vim
sudo apt install -y ccache
sdk install kotlin
cd ~
# update cmake in order to build clang
wget https://github.com/Kitware/CMake/releases/download/v4.0.2/cmake-4.0.2-linux-x86_64.sh
/bin/sh cmake-4.0.2-linux-x86_64.sh
sudo ln -sf ~/cmake-4.0.2-linux-x86_64/bin/cmake /usr/local/bin/
# build clang
git clone https://github.com/llvm/llvm-project.git
cd llvm-project
git checkout llvmorg-20.1.6
cmake -S llvm -B build -G Ninja -DLLVM_PARALLEL_LINK_JOBS=1 -DLLVM_PARALLEL_COMPILE_JOBS=8 -DLLVM_PARALLEL_TABLEGEN_JOBS=4 -DLLVM_ENABLE_PROJECTS="clang;lld" -DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_RUNTIMES="libcxxabi;libcxx;libunwind" -DLLVM_CCACHE_BUILD=ON
cmake --build build

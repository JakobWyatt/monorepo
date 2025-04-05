#!/bin/bash
# package manager installs
sudo apt update
sudo apt upgrade
sudo apt install -y racket
sudo apt install -y vim
sdk install kotlin
cd ~
# update cmake in order to build clang
wget https://github.com/Kitware/CMake/releases/download/v4.0.0/cmake-4.0.0-linux-x86_64.sh
/bin/sh cmake-4.0.0-linux-x86_64.sh
git clone https://github.com/llvm/llvm-project.git
cd llvm-project
git checkout llvmorg-20.1.1
~/cmake-4.0.0-linux-x86_64/bin/cmake -S llvm -B build -G Ninja -DLLVM_ENABLE_PROJECTS="clang;lld" -DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_RUNTIMES="libcxxabi;libcxx;libunwind"
~/cmake-4.0.0-linux-x86_64/bin/cmake --build build

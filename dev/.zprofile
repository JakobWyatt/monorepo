
eval "$(/opt/homebrew/bin/brew shellenv zsh)"

function linux {
  container run --volume $(pwd):/work -w /work linux "$@"
}

function linux-cc {
    local CC=clang++-20
    local CFLAGS=(
        -Weverything
        -Wno-unsafe-buffer-usage
        -Wno-c++98-compat
        -Wno-missing-prototypes
        -std=c++26
        -stdlib=libc++
        -lc++abi
        -static
    )

    linux "$CC" "${CFLAGS[@]}" -O3 -o release "$1"
    linux "$CC" "${CFLAGS[@]}" -O0 -g -o debug "$1"
}

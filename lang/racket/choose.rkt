#lang racket
(define choices '("racket" "rust" "python" "go" "kotlin" "C" "C++"))
(list-ref choices (random (length choices)))

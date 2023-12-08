import sys
import math

"""
Time:        51     92     68     90
Distance:   222   2031   1126   1225

Second:
51926890
222203111261225

Assume button held for t milliseconds.
d = (T - t) * t = t^2 - T*t
Find d(t) == D => 0 = t^2 - T*t - D
t_w = T / 2 +- sqrt(T^2 - 4D) / 2
winning configs: floor(sqrt(T^2 - 4D) - epsi)

solve example T=30, D=200 ans = 20
"""

def find_winning(T, D):
    buffer = math.sqrt(T**2 - 4*D) - 1e-9
    if T / D == T // D:
        return math.floor(buffer - 1e-9)
    else:
        return math.floor(buffer - 1e-9) + 1

def problem1():
    print(find_winning(51926890, 222203111261225))

def problem2(input):
    pass

def main():
    #with open(sys.argv[1]) as f:
    #    input = f.read().splitlines()
    problem1()

if __name__ == "__main__":
    main()

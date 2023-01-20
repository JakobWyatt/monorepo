import sys
import jax.numpy as jnp
from jax import grad, jit

# top to bottom visibility matrix
def visible_oneaxis(input):
    visibility = jnp.full_like(input, 0)
    cur_height = jnp.full(input.shape[0], -1.0)
    for i in range(input.shape[0]):
        visibility = visibility.at[i].set(input[i] > cur_height)
        cur_height = jnp.maximum(input[i], cur_height)
    return visibility

def visible(input):
    top_bottom = visible_oneaxis(input)
    left_right = jnp.rot90(visible_oneaxis(jnp.rot90(input, -1)), 1)
    bottom_top = jnp.rot90(visible_oneaxis(jnp.rot90(input, -2)), 2)
    right_left = jnp.rot90(visible_oneaxis(jnp.rot90(input, -3)), 3)
    return top_bottom + left_right + bottom_top + right_left

def main():
    with open(sys.argv[1]) as f:
        input = [[int(y) for y in list(x)] for x in f.read().splitlines()]
    x = jnp.array(input)
    y = visible(x)
    print(jnp.count_nonzero(y))

if __name__ == "__main__":
    main()

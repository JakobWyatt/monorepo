import sys
import jax.numpy as jnp
from jax import grad, jit, vmap
from tqdm import tqdm

# top to bottom visibility matrix
def visible_oneaxis(input):
    visibility = jnp.full_like(input, 0)
    cur_height = jnp.full(input.shape[1], -1)
    for i in range(input.shape[0]):
        visibility = visibility.at[i].set(input[i] > cur_height)
        cur_height = jnp.maximum(input[i], cur_height)
    return visibility

def score_from_tree_heights(i, x, trees):
    # find the shortest distance we can see
    #block = jnp.max(trees[x:]) dynamic slicing doesn't work in jax
    return i - jnp.max(jnp.where(x <= jnp.arange(10), trees, 0))

score_from_tree_heights_p = jit(vmap(score_from_tree_heights, (None, 0, 0), 0))

def update_tree_heights(trees, input, it):
    for i in range(input.shape[1]):
        trees = trees.at[(i, input[it,i])].set(it)
    return trees

update_tree_heights_jit = jit(update_tree_heights)

# top to bottom visibility score
def score_oneaxis(input):
    score = jnp.full_like(input, 1)
    # dim: input length by 10 (discrete heights)
    # -1 if we haven't seen a tree of this height yet (otherwise, index)
    tree_heights = jnp.full((input.shape[1], 10), 0)
    for i in tqdm(range(input.shape[0])):
        score = score.at[i].set(score_from_tree_heights_p(i, input[i], tree_heights))
        tree_heights = update_tree_heights_jit(tree_heights, input, i)
    return score

def score(input):
    top_bottom = score_oneaxis(input)
    left_right = jnp.rot90(score_oneaxis(jnp.rot90(input, -1)), 1)
    bottom_top = jnp.rot90(score_oneaxis(jnp.rot90(input, -2)), 2)
    right_left = jnp.rot90(score_oneaxis(jnp.rot90(input, -3)), 3)
    return jnp.multiply(jnp.multiply(top_bottom, left_right), jnp.multiply(bottom_top, right_left))

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
    y = score(x)
    print(y)
    print(jnp.max(y))

if __name__ == "__main__":
    main()

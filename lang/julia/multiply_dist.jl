using Plots
using Distributions
pyplot()

function gen_rand_uniform_mult(min1, max1, min2, max2, n)
    rand(Uniform(min1, max1), n) .* rand(Uniform(min2, max2), n)
end

histogram(gen_rand_uniform_mult(0, 10, 35, 40, 10000))

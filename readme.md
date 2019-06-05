# Snack & Hacks Genetic Algorithms

There are two challenges available for this episode of Snacks & Hacks:

1. Use genetic algorithms to generate a custom image of simple shapes (moderate level, no hardware requirements)
2. Use genetic algorithms to generate your face using nvidia's StyleGAN for hyper-realistic faces (advanced level, GPU needed)

## Challenge 1
The instructions for the first moderate level challenge can be found in the file genetic_polygons.py in this repository.

## Challenge 2
The second advanced level challenge makes use of tensorflow and the contents of this repo: https://github.com/NVlabs/stylegan. **Note that to do this assignment you need to have an nvidia GPU with CUDA environment setup**. Alternatively, you can use cloud computing, like Google Cloud Platform, but there may be costs associated with it, there will be added complexity, and it may take some time before you get the necessary approval for your GPU quota.

The idea of the challenge is to use adapt the code from https://github.com/NVlabs/stylegan/blob/master/pretrained_example.py to generate face phenotypes using either the input layer or activation in one of the hidden layers as genotypes. The fitness function should be based on similarity between a phenotype and a target face that we're trying to generate (for instance your own face).

This challenge is certainly not for the faint-hearted, so unless you know what you're doing, you should go for Challenge 1.

Good luck!

## More information

Blog post providing a brief intro to genetic algorithms: https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3

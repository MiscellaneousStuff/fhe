# Fully Homomorphic Encryption

## Concrete-ML (MNIST Benchmarks)

```bash
________________________________________________________________________________
[Memory] Calling sklearn.datasets._openml.fetch_openml...
fetch_openml('mnist_784')
_____________________________________________________fetch_openml - 8.6s, 0.1min
  epoch    train_loss    valid_acc    valid_loss     dur
-------  ------------  -----------  ------------  ------
      1        0.4050       0.9253        0.2556  6.2361
      2        0.2114       0.9337        0.2260  5.2169
      3        0.1828       0.9523        0.1799  4.7537
      4        0.1991       0.9313        0.2253  4.5051
      5        0.1863       0.9471        0.2042  4.2031
      6        0.1695       0.9490        0.2069  4.0555
      7        0.1660       0.9345        0.2470  3.6413
<class 'concrete.ml.sklearn.qnn.NeuralNetClassifier'>[uninitialized](
  module__activation_function=<class 'torch.nn.modules.activation.ReLU'>,
  module__input_dim=784,
  module__n_a_bits=4,
  module__n_hidden_neurons_multiplier=0.5,
  module__n_layers=2,
  module__n_outputs=10,
  module__n_w_bits=4,
)
The test accuracy of the clear model is 0.93
Circuit of 13-bits (FHE simulation)
The test accuracy (with FHE simulation) of the FHE model is 0.93
FHE circuit of 13-bits
Key generation time: 47.76 seconds
Execution time in FHE: 184.92 seconds per sample

Expected values: [0, 4, 1]
Simulated prediction values: [0 4 1]
FHE prediction values: [0 4 1]
(base) user@MacBook-Air fhe % 
```

## Types of FHE

### Bootstrapping (Turing Complete)

- TFHE (10s of ms for bootstrapping)

### Levelled (Noise Budget)

<!-- What is the typical mutiplicative depth here? -->
- BFV
- BGV
- CKKS

## Packing

- Encrypting multiple values in one ciphertext?

## Approaches

- Start off with implementing levelled FHE as its fast building
  block for everything else? TFHE?

## Techniques

### Binary Tree Multiplication

Traditional approach:

```
match = match₀ × match₁ × ... × match₇  (depth 7)
```

Binary tree approach:
```
Level 1: m₀₁ = m₀×m₁, m₂₃ = m₂×m₃, m₄₅ = m₄×m₅, m₆₇ = m₆×m₇
Level 2: m₀₁₂₃ = m₀₁×m₂₃, m₄₅₆₇ = m₄₅×m₆₇
Level 3: result = m₀₁₂₃×m₄₅₆₇  (depth only 3)
```

Same number of multiplications but the second approach has a lower depth.
This means that:
1) Lower noise accumulation per branch (3 vs 7)
2) Parallelism gain for binary tree approach

In principle this could be massively improved using something like an
`n-ary` tree to improve both the noise reduction and parallelism.

```
Thoughts: Does the n-ary approach massively improve the performance of
neural networks for FHE applications?
```

## Types

- TFHE (bit encryption)
- BGV / BFV / CKKS (integer encryption)

## Terms

### Polynomials

- degree: the highest power of the variable in the polynomial
- term degree: sum of all powers in a term

Eg.

$$ 3x^2 + 5x^3 $$

This would be a polynomial of degree 3.

## Non-Linearity

Must satisfy both of these:
$$ f(x + y) = f(x) + f(y) $$
$$ f(\alpha x) = \alpha f(x) \text{ for scalar } \alpha $$

## Bootstrapping

1. key switching: secret key enc with pub key, creating "enc sec key"
   (ie. eval keys or bootstrapping keys)
2. homomorphic decryption: system evals decrypt func homomorphically
   - input := noisy ciphertext
   - dec func applied using enc secret key
   - produces enc result of dec
3. re-encrypt

## Naive Lookup

1. Perform bitwise AND on each enc(bit)
2. AND across all results (bubble AND?)
3. Multiply final sum (0 or 1) for each possible matching idx
4. Return non-zero value?
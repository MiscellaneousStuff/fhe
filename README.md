# Fully Homomorphic Encryption

## Overview

- Chinese Remainder Theorem (CRT) (aka: Dimensionality reduction)
  - Applied to modulo numbers to reduce their size of storage + compute
    then reconstructed. Operations on those smaller numbers before
    reconstruction are mathematically identical to operating on the original
    number.
  - Very similar to FFT for switching between time and frequency domain

## Optimisation

### Neural Networks

- Replace multiplication with repeated addition to avoid noise growth
  - Possibly a good idea for deep networks, or heavy sequential behaviour
  - Removes need for bootstrapping, especially when the constant which the
    value is being multiplied by is low enough where repeated addition is
    efficient.
- Param (plain vs cipher) size scaling factor (NOTE: from 3.7 claude, need to validate)
  - BGV/BFV:
    - 1 byte -> 2,000 - 10,000x (2KB-10KB) expansion
    - 32-bit integer - 8-40KB ciphertext
    - Typical params: 8KB-128KB ciphertext
  - CKKS:
    - Similar to BGV/BFV
    - Optimised for floats
    - 10KB - 100KB per ciphertext
  - TFHE:
    - 1 bit -> 1-2KB ciphertext
    - 1 byte -> 8-16KB ciphertext

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

## Chinese Remainder Theorem

### Overview

Find number that satisfies multiple remainder conditions at once.
It allows us to optimise calculations involving massive numbers
into multiple smaller ones.
This allows us to optimise calculations happening within
encryption space, which is useful because calculations within
encryption space are very costly in general, especially
multiplication.

Decomposition of the large number happens in outer cipherspace,
then the computations happen in the now more efficient and parallel
inner cipherspace, and then reconstructed in outer cipherspace.

So it's effectively dimensionality reduction mainly in inner cipherspace
with the decomposition and reconstruction happening in the outerspace.

- Coprime req: Works when moduli are pairwise coprime (have no common factors)
- Guaranteed solution: Guarantees unique solution modulo the product of all moduli

Big O:
$$ O(n * log^2 M) $$
where
$$ n \text{ is the number of moduli} $$
$$ M \text{ is the product of all moduli} $$

### Remainder vs Residue

- Remainder just refers to the remaining part after division
- Residue has two meanings:
1) Same as remainder
2) Every single possible value after a modulo operation
For eg. for module 5, it would be
$$ \{ 0, 1, 2, 3, 4 \} $$

### Implementations (according to claude 3.7 sonnet)

- Microsoft SEAL: typically uses 3-10 primes for its RNS base
- HElib: can use dozens of moduli in its modulus chain
- TFHE: uses different decomposition strategies for its bootstrapping keys
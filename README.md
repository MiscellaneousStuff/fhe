# Fully Homomorphic Encryption

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
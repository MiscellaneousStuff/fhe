import sys
sys.set_int_max_str_digits(1_000_000)
# """Arithmetic"""
# def enc(R, p, r, m, N):
#     """enc(m) = R * p + r * 2 + m"""
#     a = R * p
#     b = r * N
#     o = a + b + m
#     return o

# def dec(p, c, N):
#     """dec(m) = (c % p) % 2"""
#     return (c % p) % N

# n1 = 4
# n2 = 8

# R = 30
# p = 17
# r = 17
# N = 2 ** 8

# # c1 = enc(R, p, r, 1, N)
# # c2 = enc(R, p, r, 1, N)
# # s = c1

# # for i in range(100):
# #     s *= c2

# # o = dec(p, s, N)
# # print(s, o)

# """Noise Accumluation"""
# def enc(R, p, r, m, N):
#     """enc(m) = R * p + r * 2 + m"""
#     a = R * p
#     b = r * N
#     o = a + b + m
#     return o

# def dec(p, c, N):
#     """dec(m) = (c % p) % 2"""
#     return (c % p) % N

# def bootstrap(c, p, R, r, N):
#     """
#     Simulate bootstrapping by homomorphically evaluating the decryption function.
#     In a real FHE system, this would be done without access to the secret key.
#     """
#     # Step 1: Extract the "effective" plaintext bit (this simulates homomorphic decryption)
#     plaintext_bit = dec(p, c, N)
    
#     # Step 2: Re-encrypt with fresh, minimal noise
#     fresh_ciphertext = enc(R, p, r, plaintext_bit, N)
    
#     return fresh_ciphertext

# R = 3
# R2 = 40
# p = 17
# r = 4
# N = 2

# # Encrypt a message
# m = 1
# c = enc(R, p, r, m, N)
# d = enc(R, p, r, m, N)
# print(f"Initial ciphertext: {c}, decrypts to {dec(p, c, N)}")

# # Perform multiplications (squaring for faster noise growth)
# for i in range(1, 10):
#     c = c * c
#     d = d * d
#     result = dec(p, c, N)
#     result_bootstrapped = dec(p, d, N)
#     d = bootstrap(d, p, R, r, N)
#     print(f"After {i} squaring operations: decrypts to {result}")
#     print(f"(Bootstrap) After {i} squaring operations: decrypts to {result_bootstrapped}")
#     # Calculate noise level (in this simple model)
#     noise = (c % p) - (result % N)
#     noise_bootstrapped = (d % p) - (result % N)
#     print(f"Noise level: {noise}")
#     print(f"(Bootstrap) Noise level: {noise_bootstrapped}")
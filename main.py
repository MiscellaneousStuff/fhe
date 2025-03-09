def enc(R, p, r, m, N):
    """enc(m) = R * p + r * 2 + m"""
    a = R * p
    b = r * N
    o = a + b + m
    return o

def dec(p, c, N):
    """dec(m) = (c % p) % 2"""
    return (c % p) % N

n1 = 4
n2 = 8

R = 30
p = 17
r = 17
N = 2

c1 = enc(R, p, r, 0, N)
c2 = enc(R, p, r, 0, N)
c3 = enc(R, p, r, 1, N)
c4 = enc(R, p, r, 0, N)
c5 = enc(R, p, r, 0, N)

s = c1 + c2 + c3 + c4 + c5
o = dec(p, s, N)
print(s, o)
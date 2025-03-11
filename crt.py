"""Understanding chinese remainder theorem (CRT).

This is used to decompose a large number (modulo form)
into smaller numbers with equivalent properties.

Basically dimensionality reduction for computing
modulo numbers.

Big O:
$$ O(n * log^2 M) $$
where
$$ n \text{ is the number of moduli} $$
$$ M \text{ is the product of all moduli} $$
"""

def findMinX(num, rem, k):
    # Initialize result
    x = 1 # what is this lol

    # As per the Chinise remainder
    # theorem, this loop will
    # always break.
    while(True):
        # Check if remainder of x % num[j] is rem[j] or not (for all j from 0 to k-1)
        j = 0
        while(j < k):
            if (x % num[j] != rem[j]):
                break
            j += 1

        # If all remainders 
        # matched, we found x
        if (j == k):
            return x

        # Else try next number
        x += 1

# Driver Code
if __name__ == "__main__":
    num = [5, 7] # moduli (divisors)
    rem = [4, 2] # residues
    k = len(num)
    print("x is", findMinX(num, rem, k))
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from matplotlib.lines import Line2D

# LWE parameters
n = 3  # 3D for visualization
p = 23  # Small prime for modulus
error_range = 0

# Generate secret key (first element set to 1)
key = np.array([1, 7, 15])  # Simple key for illustration

def encrypt(message, key):
    """Encrypt a bit (0 or 1) using LWE"""
    # Random vector for encryption
    a = np.random.randint(0, p, size=n)
    
    # Small error
    e = np.random.randint(-error_range, error_range + 1)
    
    # Target dot product
    target = (message + 2*e) % p
    
    # Original dot product
    dot = np.dot(a, key) % p
    
    # Adjust first element to get desired dot product
    a[0] = (a[0] + target - dot) % p
    
    return a, e, message

def decrypt(c, key):
    """Decrypt an LWE ciphertext"""
    dot = np.dot(c, key) % p
    # Center the result around 0
    centered = dot if dot <= p//2 else dot - p
    return centered % 2

# Create figure
fig = plt.figure(figsize=(16, 10))
ax = fig.add_subplot(111, projection='3d')

# Generate encryptions
c0, e0, m0 = encrypt(0, key)
c1, e1, m1 = encrypt(1, key)

# Homomorphic addition
c_sum = (c0 + c1) % p
m_sum = decrypt(c_sum, key)
e_sum = (e0 + e1)  # Combined error

# Vectors to plot
vectors = [
    (key, 'red', 'Secret Key'),
    (c0, 'blue', f'Ciphertext 0 (e={e0})'),
    (c1, 'green', f'Ciphertext 1 (e={e1})'),
    (c_sum, 'purple', f'C0 + C1 (e≈{e_sum})')
]

# Origin
origin = np.zeros(3)

# Plot the vectors
# for v, color, label in vectors:
#     arrow = Arrow3D([0, v[0]], [0, v[1]], [0, v[2]], 
#                     mutation_scale=20, lw=3, arrowstyle='-|>', color=color, label=label)
#     ax.add_artist(arrow)

for v, color, label in vectors:
    ax.quiver(0, 0, 0, v[0], v[1], v[2], 
              color=color, label=label, arrow_length_ratio=0.1, linewidths=2)

# Plot a semi-transparent plane representing the key hyperplane
xx, yy = np.meshgrid(range(-5, 30), range(-5, 30))
# For the key plane: k[0]*x + k[1]*y + k[2]*z = 0 => z = -(k[0]*x + k[1]*y)/k[2]
z1 = -(key[0] * xx + key[1] * yy) / key[2]
ax.plot_surface(xx, yy, z1 % p, alpha=0.2, color='gray')

# For message=1 plane: k[0]*x + k[1]*y + k[2]*z = 1 => z = (1 - k[0]*x - k[1]*y)/k[2]
z2 = (1 - key[0] * xx - key[1] * yy) / key[2]
ax.plot_surface(xx, yy, z2 % p, alpha=0.1, color='orange')

# Decorations
ax.set_xlim([0, p])
ax.set_ylim([0, p])
ax.set_zlim([0, p])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('LWE in 3D Space - Encryption, Decryption, and Homomorphic Addition')

# Create a custom legend
custom_lines = [Line2D([0], [0], color=v[1], lw=4) for v in vectors]
custom_labels = [label for _, _, label in vectors]
ax.legend(custom_lines, custom_labels, loc='upper right')

# Add text annotations for decryption results
ax.text(p*0.7, p*0.1, p*0.9, f"Dec(c0) = {decrypt(c0, key)}", color='blue', fontsize=12)
ax.text(p*0.7, p*0.1, p*0.8, f"Dec(c1) = {decrypt(c1, key)}", color='green', fontsize=12)
ax.text(p*0.7, p*0.1, p*0.7, f"Dec(c0 + c1) = {m_sum}", color='purple', fontsize=12)

# Add explanatory text
fig.text(0.02, 0.02, 
         "LWE Visualization:\n"
         "- Gray plane: points where <k,x> = 0 mod p (encryptions of 0 are near this plane)\n"
         "- Orange plane: points where <k,x> = 1 mod p (encryptions of 1 are near this plane)\n"
         "- Dot product of ciphertexts with key gives message + small even error\n"
         "- Homomorphic addition: vector addition preserves message addition (mod 2)",
         fontsize=12)

plt.tight_layout()
plt.show()

# Print numerical results for reference
print(f"Key: {key}")
print(f"Ciphertext for 0: {c0}, dot product: {np.dot(c0, key) % p}, decrypts to {decrypt(c0, key)}")
print(f"Ciphertext for 1: {c1}, dot product: {np.dot(c1, key) % p}, decrypts to {decrypt(c1, key)}")
print(f"Sum ciphertext: {c_sum}, dot product: {np.dot(c_sum, key) % p}, decrypts to {m_sum}")
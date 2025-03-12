# -*- coding: utf-8 -*-
"""
High-Resolution Mathematical Equation Art (Cropped)
Created: 2025-02-09
Author: S Perkins
Company: Geo Consulting Limited
Purpose: Generates a 5000x3000 pixel image with equations,
         sorts them by brightness, saves as TIFF, 
         then trims 25% off each side (final size: 2500x1500).
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image  # For cropping

# Output filenames
output_file = "high_res_math_art.tiff"
cropped_file = "high_res_math_art_cropped.tiff"

# Define shading range (min = 25%, max = 100%)
min_shade = 0.25  # 25% gray (darker, further away)
max_shade = 1.0   # 100% gray (brighter, closer)

# Define font size range
min_font = 6   # Font size when at min_shade
max_font = 11  # Font size when at max_shade

# Number of equations
num_equations = 1300

# Image dimensions
original_width, original_height = 5000, 3000
crop_margin_x = int(original_width * 0.25)  # 25% of width (1250 pixels per side)
crop_margin_y = int(original_height * 0.25) # 25% of height (750 pixels per side)
cropped_width = original_width - (2 * crop_margin_x)  # 2500
cropped_height = original_height - (2 * crop_margin_y) # 1500

# List of mathematical equations

equations = [
    # Physics & Relativity
    r"E = mc^2",
    r"F = G \frac{m_1 m_2}{r^2}",
    r"pV = nRT",
    r"S = k \ln \Omega",
    r"H = T + V",
    r"\oint_{\Sigma} \mathbf{B} \cdot d\mathbf{A} = 0",
    r"\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}",
    r"\langle \psi | \hat{H} | \psi \rangle = E",
    r"i\hbar\frac{d}{dt}|\psi\rangle = H|\psi\rangle",
    r"\frac{1}{\sqrt{1 - v^2/c^2}}",
    
    # Calculus & Integration
    r"\int_a^b f(x)dx = F(b) - F(a)",
    r"\frac{d}{dx} e^x = e^x",
    r"\frac{d}{dx} \ln x = \frac{1}{x}",
    r"\frac{d}{dx} \tan x = \sec^2 x",
    r"\oint_C \mathbf{F} \cdot d\mathbf{r} = \iint_S \nabla \times \mathbf{F} \cdot d\mathbf{S}",
    r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}",
    r"\sum_{n=0}^{\infty} \frac{x^n}{n!} = e^x",
    r"\Gamma(n) = (n-1)!",
    
    # Algebra & Number Theory
    r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
    r"a^2 + b^2 = c^2",
    r"\sin^2\theta + \cos^2\theta = 1",
    r"\lim_{x \to \infty} \frac{1}{x} = 0",
    r"\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s}",
    
    # Probability & Statistics
    r"\mathbb{P}(X \leq x) = F(x)",
    r"\Phi(x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{x} e^{-t^2/2} dt",
    r"S = -k_B \sum p_i \ln p_i",
    r"\operatorname{Var}(X) = \mathbb{E}[X^2] - \mathbb{E}[X]^2",
    
    # Quantum Mechanics
    r"i\hbar \frac{\partial}{\partial t} \psi = \hat{H} \psi",
    r"\hat{H} = -\frac{\hbar^2}{2m} \nabla^2 + V",
    r"|\psi(t)\rangle = e^{-i\hat{H}t/\hbar} |\psi(0)\rangle",
    
    # Maxwell's Equations (Electromagnetism)
    r"\nabla \cdot \mathbf{E} = \frac{\rho}{\epsilon_0}",
    r"\nabla \cdot \mathbf{B} = 0",
    r"\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}",
    r"\nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0 \epsilon_0 \frac{\partial \mathbf{E}}{\partial t}",
    
    # Fluid Dynamics
    r"\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} = -\frac{1}{\rho} \frac{\partial p}{\partial x} + \nu \frac{\partial^2 u}{\partial x^2}",
    r"\nabla \cdot \mathbf{v} = 0",
    
    # Fourier Transforms
    r"\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x) e^{-2\pi i x \xi} dx",
    r"f(x) = \int_{-\infty}^{\infty} \hat{f}(\xi) e^{2\pi i x \xi} d\xi",
    
    # Thermodynamics
    r"dU = TdS - PdV",
    r"PV^\gamma = \text{constant}",
    
    # Matrix & Linear Algebra
    r"\det(A) = \prod_{i=1}^{n} \lambda_i",
    r"\operatorname{div}(\operatorname{grad} f) = \Delta f",
    
    # Special Constants
    r"e^{i\pi} + 1 = 0",
    r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
    # r"\sum_{k=0}^{n} {n \choose k} = 2^n",
    r"\sum_{k=0}^{n} \binom{n}{k} = 2^n",
    
    # Complex Numbers
    r"z = x + iy",
    r"e^{ix} = \cos x + i \sin x",
    
    # Geometry & Trigonometry
    r"\alpha + \beta + \gamma = 180^\circ",
    r"\tan \theta = \frac{\sin \theta}{\cos \theta}",
    
    # Chaos & Fractals
    r"x_{n+1} = r x_n (1 - x_n)",
    r"z_{n+1} = z_n^2 + c",
]





# Store equation data (before drawing)
equation_data = []

for _ in range(num_equations):
    eq = np.random.choice(equations)  # Pick a random equation
    x, y = np.random.uniform(0, 1), np.random.uniform(0, 1)  # Random position
    angle = np.random.uniform(-45, 45)  # Random rotation

    # Generate random grayscale color in the defined range
    gray_value = np.random.uniform(min_shade, max_shade)

    # Adjust font size based on brightness (brighter = larger)
    fontsize = min_font + (gray_value - min_shade) * (max_font - min_font) / (max_shade - min_shade)

    # Store as tuple
    equation_data.append((gray_value, fontsize, eq, x, y, angle))

# Sort equations by brightness (darkest first, brightest last)
equation_data.sort(key=lambda e: e[0])  # Sorting by gray_value

# Create high-resolution figure
fig, ax = plt.subplots(figsize=(original_width / 300, original_height / 300), dpi=300)
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Draw sorted equations
for gray_value, fontsize, eq, x, y, angle in equation_data:
    color = (gray_value, gray_value, gray_value)  # RGB tuple
    ax.text(x, y, f"${eq}$", color=color, fontsize=fontsize,
            ha='center', va='center', rotation=angle,
            transform=ax.transAxes, alpha=0.8)

# Hide axes
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

# Save the full-sized image as an uncompressed TIFF
plt.savefig(output_file, dpi=300, format='tiff', pil_kwargs={"compression": None})
plt.close(fig)  # Close figure to free memory

print(f"Saved {output_file}")

# === Crop the image using Pillow ===
# Open the saved image
img = Image.open(output_file)

# Define cropping box: (left, top, right, bottom)
crop_box = (crop_margin_x, crop_margin_y, original_width - crop_margin_x, original_height - crop_margin_y)

# Perform cropping
cropped_img = img.crop(crop_box)

# Save the cropped image as an uncompressed TIFF
cropped_img.save(cropped_file, format="TIFF", compression=None)

print(f"Saved cropped image: {cropped_file}")

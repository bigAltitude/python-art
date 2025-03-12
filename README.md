# Artistic Python Scripts: Circle & Equation Art

This repository contains two Python scripts that generate digital art through algorithmic processes. Each script utilizes mathematical principles and randomized algorithms to create visually engaging artworks.

## Repository Contents

### circle_art.py

- **Description:**  
  Generates a 7500x7500 pixel image by dynamically fitting circles on a canvas. The script employs an intelligent free pixel mask to determine optimal circle placement, ensuring that circles do not overlap. It logs progress and generates intermediate thumbnails during execution.

- **Output:**  
  A TIFF image named `circle_field_blue_random.tiff`.

### equation_art.py

- **Description:**  
  Creates a high-resolution 5000x3000 pixel image populated with a curated list of mathematical equations. The equations are sorted by brightness, with corresponding adjustments in font size to enhance visual hierarchy. The script also produces a cropped version of the image, refining the final presentation.

- **Output:**  
  Two TIFF images: `high_res_math_art.tiff` and `high_res_math_art_cropped.tiff`.

## Features

- **Dynamic Circle Fitting:**  
  The `circle_art.py` script uses a free pixel mask and iterative placement algorithm to fill a large canvas with non-overlapping, blue-shaded circles.

- **Mathematical Equation Rendering:**  
  The `equation_art.py` script displays a selection of equations from physics, calculus, algebra, and other fields, rendering them with variable brightness and font sizes to create depth and visual interest.

- **High-Resolution Output:**  
  Both scripts generate images in TIFF format, ensuring high-quality outputs suitable for professional presentations.

## Requirements

Ensure that you have Python 3.x installed along with the following packages:

- numpy
- Pillow (PIL)
- matplotlib (required for `equation_art.py`)

Install the dependencies using pip:

```bash
pip install numpy pillow matplotlib
```

## Usage

Clone the repository and navigate to the project directory. Execute the scripts as follows:

### Running the Circle Art Script

```bash
python circle_art.py
```

### Running the Equation Art Script

```bash
python equation_art.py
```

The resulting TIFF images will be saved in the repository’s root directory.

## Acknowledgments

Developed by **S Perkins** at **Geo Consulting Limited** as part of a project in Geo-Science Engineering, these scripts demonstrate the integration of mathematical concepts and creative coding to produce digital art.

## License

*Include license information here.*

---

This repository is designed for those interested in exploring the convergence of art and algorithmic design through professional and well-structured code. Enjoy exploring and expanding upon these creative tools.

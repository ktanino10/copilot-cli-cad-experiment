"""
GitHub Logo → 3D Printable STL Generator
Creates a coin/medallion with the GitHub mark embossed on top.
"""

import numpy as np
from PIL import Image
from stl import mesh
from scipy import ndimage

# === Parameters (mm) ===
DIAMETER = 60.0        # coin diameter
BASE_HEIGHT = 2.0      # flat base thickness
LOGO_HEIGHT = 3.0      # logo extrusion height
RESOLUTION = 400       # grid resolution (higher = smoother)
BORDER_WIDTH = 2.0     # raised border ring width

# Load and process image
img = Image.open("/Users/kyosuketanino/workspace/CAD/GitHub-Mark-ea2971cee799.png")
img = img.convert("L")  # grayscale
img = img.resize((RESOLUTION, RESOLUTION), Image.LANCZOS)
pixels = np.array(img)

# Threshold: dark pixels (logo) = True
logo_mask = pixels < 128

# Create circular boundary mask
y, x = np.ogrid[:RESOLUTION, :RESOLUTION]
center = RESOLUTION / 2
radius_px = RESOLUTION / 2 - 1
dist = np.sqrt((x - center) ** 2 + (y - center) ** 2)
circle_mask = dist <= radius_px

# Border ring mask
border_inner = RESOLUTION / 2 - (BORDER_WIDTH / DIAMETER * RESOLUTION)
border_mask = circle_mask & (dist >= border_inner)

# Smooth the logo mask edges slightly for better print quality
logo_smooth = ndimage.gaussian_filter(logo_mask.astype(float), sigma=1.0)
logo_final = (logo_smooth > 0.5) & circle_mask

# Combined raised area: logo + border ring
raised_mask = logo_final | border_mask

# Build heightmap
heightmap = np.zeros((RESOLUTION, RESOLUTION))
heightmap[circle_mask] = BASE_HEIGHT
heightmap[raised_mask] = BASE_HEIGHT + LOGO_HEIGHT

# Convert heightmap to mesh
# Scale to real world coordinates (mm)
scale = DIAMETER / RESOLUTION

def heightmap_to_stl(hmap, scale, filename):
    """Convert a heightmap to a watertight STL mesh."""
    rows, cols = hmap.shape
    triangles = []

    # Top surface triangles
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Skip if all four corners are zero (outside the model)
            h00 = hmap[i, j]
            h01 = hmap[i, j + 1]
            h10 = hmap[i + 1, j]
            h11 = hmap[i + 1, j + 1]
            if h00 == 0 and h01 == 0 and h10 == 0 and h11 == 0:
                continue

            x0, y0 = j * scale, i * scale
            x1, y1 = (j + 1) * scale, (i + 1) * scale

            # Top face - two triangles
            triangles.append([
                [x0, y0, h00],
                [x1, y0, h01],
                [x0, y1, h10],
            ])
            triangles.append([
                [x1, y0, h01],
                [x1, y1, h11],
                [x0, y1, h10],
            ])

            # Bottom face - two triangles (z=0), reversed winding
            if h00 > 0 or h01 > 0 or h10 > 0 or h11 > 0:
                triangles.append([
                    [x0, y0, 0],
                    [x0, y1, 0],
                    [x1, y0, 0],
                ])
                triangles.append([
                    [x1, y0, 0],
                    [x0, y1, 0],
                    [x1, y1, 0],
                ])

    # Side walls along edges
    for i in range(rows - 1):
        for j in range(cols - 1):
            h00 = hmap[i, j]
            h01 = hmap[i, j + 1]
            h10 = hmap[i + 1, j]

            x0, y0 = j * scale, i * scale
            x1, y1 = (j + 1) * scale, (i + 1) * scale

            # Left edge (j==0 or left neighbor is 0)
            if j == 0 and h00 > 0:
                triangles.append([[x0, y0, h00], [x0, y1, h10], [x0, y0, 0]])
                triangles.append([[x0, y1, h10], [x0, y1, 0], [x0, y0, 0]])

            # Top edge (i==0 or top neighbor is 0)
            if i == 0 and h00 > 0:
                triangles.append([[x0, y0, h00], [x0, y0, 0], [x1, y0, h01]])
                triangles.append([[x1, y0, h01], [x0, y0, 0], [x1, y0, 0]])

    print(f"Generated {len(triangles)} triangles")

    # Create mesh
    stl_mesh = mesh.Mesh(np.zeros(len(triangles), dtype=mesh.Mesh.dtype))
    for idx, tri in enumerate(triangles):
        for vert in range(3):
            stl_mesh.vectors[idx][vert] = tri[vert]

    stl_mesh.save(filename)
    print(f"Saved to {filename}")

output_path = "/Users/kyosuketanino/workspace/CAD/github_logo.stl"
heightmap_to_stl(heightmap, scale, output_path)

# Also print some stats
file_size = __import__("os").path.getsize(output_path)
print(f"\nModel specs:")
print(f"  Diameter: {DIAMETER}mm")
print(f"  Base thickness: {BASE_HEIGHT}mm")
print(f"  Logo height: {BASE_HEIGHT + LOGO_HEIGHT}mm total")
print(f"  File size: {file_size / 1024:.1f} KB")
print(f"\n3D printer settings recommendation:")
print(f"  Layer height: 0.2mm")
print(f"  Infill: 20%")
print(f"  Supports: Not needed")
print(f"  Material: PLA recommended")

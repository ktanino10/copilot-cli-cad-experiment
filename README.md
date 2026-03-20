# 🧪 GitHub Copilot CLI × CAD File Generation Experiment

> 🇯🇵 **日本語版はこちら → [README.ja.md](README.ja.md)**

## Overview

This is a record of an experiment to see if **GitHub Copilot CLI** can load an image (GitHub Octocat logo) and automatically generate 3D-printable STL files and various CAD formats.

## What We Did

### Input
- **Image**: GitHub Mark (Octocat logo) PNG image (`GitHub-Mark-ea2971cee799.png`)

![GitHub Mark](GitHub-Mark-ea2971cee799.png)

### Process
1. Passed the image file to GitHub Copilot CLI and asked: "Create a 3D-printable CAD from this image"
2. Copilot CLI automatically generated and executed Python scripts
3. The image was converted: Grayscale → Binarization → Mesh generation → Cut-through 3D models
4. The STL files were then converted to multiple CAD formats (OBJ, DXF, etc.)
5. Multiple formats were exported for editing in Fusion 360, AutoCAD, etc.

### Two Generated Models

Two types of **cut-through models** were generated from the black and white areas of the image:

#### ① `octocat_black_solid` — Black Areas are Solid
- The **black circular ring** from the original image becomes the solid body
- The **Octocat silhouette is hollow (cut-through hole)**
- Use cases: Frame/border type, cookie cutter outer frame, etc.

#### ② `octocat_white_solid` — White Areas (Octocat Silhouette) are Solid
- Only the **Octocat silhouette (white cat shape)** becomes a solid body
- The surrounding black areas do not exist
- Use cases: Octocat figurine, stamp, keychain, etc.

### Model Specifications

| Parameter | Value |
|---|---|
| Size | 60mm × 60mm |
| Height (thickness) | 5mm |
| Shape | Cut-through (with hollow sections) |
| Resolution | 500 × 500 pixel-based |

## Generated Files

### 3D Files (for 3D Printing / 3D CAD Software)

| File | Format | Description | Compatible Software |
|---|---|---|---|
| `octocat_black_solid.stl` | STL | Black solid (3D printing standard) | Cura, PrusaSlicer, Fusion 360, AutoCAD |
| `octocat_black_solid.obj` | OBJ | Black solid (universal 3D) | Fusion 360, Blender, 3ds Max, Maya |
| `octocat_black_solid.3mf` | 3MF | Black solid (next-gen 3D printing) | Cura, PrusaSlicer, Windows 3D Viewer |
| `octocat_black_solid.ply` | PLY | Black solid | MeshLab, CloudCompare, Fusion 360 |
| `octocat_black_solid.off` | OFF | Black solid | MeshLab, Geomview |
| `octocat_white_solid.stl` | STL | Octocat solid (3D printing standard) | Cura, PrusaSlicer, Fusion 360, AutoCAD |
| `octocat_white_solid.obj` | OBJ | Octocat solid (universal 3D) | Fusion 360, Blender, 3ds Max, Maya |
| `octocat_white_solid.3mf` | 3MF | Octocat solid (next-gen 3D printing) | Cura, PrusaSlicer, Windows 3D Viewer |
| `octocat_white_solid.ply` | PLY | Octocat solid | MeshLab, CloudCompare, Fusion 360 |
| `octocat_white_solid.off` | OFF | Octocat solid | MeshLab, Geomview |

### 2D Files (for 2D CAD Software / Vector Editing)

| File | Format | Description | Compatible Software |
|---|---|---|---|
| `octocat_black_solid.dxf` | DXF | Black area 2D contour | **AutoCAD**, Fusion 360, Illustrator |
| `octocat_white_solid.dxf` | DXF | Octocat silhouette 2D contour | **AutoCAD**, Fusion 360, Illustrator |

### Other Files

| File | Description |
|---|---|
| `GitHub-Mark-ea2971cee799.png` | Input image (source data) |
| `generate_cutout.py` | Cut-through model generation script |
| `generate_stl.py` | Initial version (coin/medallion type) generation script |

## Recommended 3D Print Settings

```
Layer height:  0.2mm
Infill:        100% (recommended for cut-through models for strength)
Supports:      Not needed
Material:      PLA recommended
Nozzle temp:   200-210°C
Bed temp:      60°C
```

## How to Edit in CAD Software

### Fusion 360
1. **3D editing**: Import `.obj` or `.stl` → "Mesh" → "Convert to BRep" for full editing
2. **2D → 3D**: Import `.dxf` → Loads as sketch → "Extrude" to desired thickness

### AutoCAD
1. **2D drawing**: Open `.dxf` directly → Editable as polylines
2. **3D model**: Import `.stl`

### Blender
- Import `.obj` → Edit with modifiers

## Findings

- **Image to STL**: Copilot CLI auto-generated Python code to create watertight mesh 3D models from image pixel data
- **Cut-through models**: By inverting black/white, two patterns ("frame" and "silhouette") were automatically generated
- **Format conversion**: Conversion from STL to OBJ, PLY, 3MF, DXF, etc. was done simply by asking
- **Parametric**: Model size and thickness can be easily customized by changing script parameters
- **Limitations**: Since it's image-based, surface smoothness depends on pixel resolution. For smoother models, convert to BRep in Fusion 360 and apply smoothing

## Environment

- **Tool**: GitHub Copilot CLI
- **Language**: Python 3
- **Libraries**: Pillow, NumPy, numpy-stl, scipy, trimesh, ezdxf
- **Date**: March 20, 2026


## ⚠️ Disclaimer / Non-Commercial Use

- This project is for **personal and educational purposes only**. It is **not intended for commercial use**.
- The GitHub logo and Octocat are **trademarks of GitHub, Inc.** This project is not affiliated with, endorsed by, or sponsored by GitHub.
- Please refer to the [GitHub Logo Usage Guidelines](https://github.com/logos) before using or distributing any output.


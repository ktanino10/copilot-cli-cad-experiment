"""
GitHub Octocat → 2つの貫通型3Dモデル生成
1. octocat_black_solid.stl - 黒部分が残り、白部分（Octocat）が空洞
2. octocat_white_solid.stl - 白部分（Octocatシルエット）が残り、黒部分が空洞
"""

import numpy as np
from PIL import Image
from scipy import ndimage
from stl import mesh as stlmesh

# === Parameters (mm) ===
EXTRUDE_HEIGHT = 5.0   # 押し出し高さ
RESOLUTION = 500       # グリッド解像度
TARGET_SIZE = 60.0     # モデルの最大幅 (mm)

# Load and process image
img = Image.open("/Users/kyosuketanino/workspace/CAD/GitHub-Mark-ea2971cee799.png")
img = img.convert("L")
img = img.resize((RESOLUTION, RESOLUTION), Image.LANCZOS)
pixels = np.array(img)

# 二値化: 黒(dark)=True
black_mask = pixels < 128

# 少しスムージングしてギザギザを減らす
smoothed = ndimage.gaussian_filter(black_mask.astype(float), sigma=1.5)
black_mask = smoothed > 0.5

# スケール計算
scale = TARGET_SIZE / RESOLUTION


def mask_to_watertight_stl(mask, scale, height, filename):
    """
    2Dマスクから貫通型（空洞あり）の水密STLメッシュを生成。
    mask=Trueのピクセルだけが立体になり、Falseは完全に空洞。
    """
    rows, cols = mask.shape
    triangles = []

    # 各ピクセルを柱(column)として処理
    for i in range(rows):
        for j in range(cols):
            if not mask[i, j]:
                continue

            x0 = j * scale
            y0 = i * scale
            x1 = (j + 1) * scale
            y1 = (i + 1) * scale

            # Top face (z = height)
            triangles.append([[x0, y0, height], [x1, y0, height], [x0, y1, height]])
            triangles.append([[x1, y0, height], [x1, y1, height], [x0, y1, height]])

            # Bottom face (z = 0), reversed winding
            triangles.append([[x0, y0, 0], [x0, y1, 0], [x1, y0, 0]])
            triangles.append([[x1, y0, 0], [x0, y1, 0], [x1, y1, 0]])

            # Side walls - only where adjacent pixel is empty
            # Right wall (j+1 is empty or edge)
            if j + 1 >= cols or not mask[i, j + 1]:
                triangles.append([[x1, y0, 0], [x1, y1, 0], [x1, y0, height]])
                triangles.append([[x1, y1, 0], [x1, y1, height], [x1, y0, height]])

            # Left wall (j-1 is empty or edge)
            if j - 1 < 0 or not mask[i, j - 1]:
                triangles.append([[x0, y0, 0], [x0, y0, height], [x0, y1, 0]])
                triangles.append([[x0, y1, 0], [x0, y0, height], [x0, y1, height]])

            # Bottom wall (i+1 is empty or edge)
            if i + 1 >= rows or not mask[i + 1, j]:
                triangles.append([[x0, y1, 0], [x0, y1, height], [x1, y1, 0]])
                triangles.append([[x1, y1, 0], [x0, y1, height], [x1, y1, height]])

            # Top wall (i-1 is empty or edge)
            if i - 1 < 0 or not mask[i - 1, j]:
                triangles.append([[x0, y0, 0], [x1, y0, 0], [x0, y0, height]])
                triangles.append([[x1, y0, 0], [x1, y0, height], [x0, y0, height]])

    print(f"  Triangles: {len(triangles)}")

    stl_obj = stlmesh.Mesh(np.zeros(len(triangles), dtype=stlmesh.Mesh.dtype))
    for idx, tri in enumerate(triangles):
        for v in range(3):
            stl_obj.vectors[idx][v] = tri[v]

    stl_obj.save(filename)
    size_kb = __import__("os").path.getsize(filename) / 1024
    print(f"  Saved: {filename} ({size_kb:.0f} KB)")


# === Model 1: 黒部分が残る（Octocatが空洞） ===
print("Model 1: 黒部分ソリッド（Octocatシルエットが貫通空洞）")
mask_to_watertight_stl(
    black_mask, scale, EXTRUDE_HEIGHT,
    "/Users/kyosuketanino/workspace/CAD/octocat_black_solid.stl"
)

# === Model 2: 白部分が残る（Octocatシルエットだけ立体） ===
print("\nModel 2: 白部分ソリッド（Octocatシルエットが立体）")
# 白部分 = 画像内のOctocatシルエット
# 外側の白い余白は除外したいので、円の範囲内の白だけ残す
y, x = np.ogrid[:RESOLUTION, :RESOLUTION]
center = RESOLUTION / 2
radius_px = RESOLUTION * 0.48  # 円の半径（画像に合わせる）
circle_mask = ((x - center) ** 2 + (y - center) ** 2) <= radius_px ** 2

white_in_circle = (~black_mask) & circle_mask

mask_to_watertight_stl(
    white_in_circle, scale, EXTRUDE_HEIGHT,
    "/Users/kyosuketanino/workspace/CAD/octocat_white_solid.stl"
)

print("\n✅ 完了！")
print(f"  サイズ: {TARGET_SIZE}mm × {TARGET_SIZE}mm × {EXTRUDE_HEIGHT}mm")

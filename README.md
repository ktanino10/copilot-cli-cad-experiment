# 🧪 GitHub Copilot CLI × CADファイル生成実験

## 概要

**GitHub Copilot CLI** に画像を読み込ませ、そこから3Dプリント可能なSTLファイルおよび各種CADフォーマットを自動生成できるか実験した記録です。

## 実験内容

### 入力
- **画像**: GitHub Mark（Octocatロゴ）の PNG画像（`GitHub-Mark-ea2971cee799.png`）

### やったこと
1. GitHub Copilot CLI に画像ファイルを渡し、「この画像を元に3Dプリント用のCADを作って」と依頼
2. Copilot CLI が Python スクリプト（`generate_stl.py`）を自動生成・実行
3. 画像をグレースケール化 → 二値化 → 高さマップ生成 → メッシュ化 の工程を自動実行
4. STLファイルからさらに複数のCADフォーマットへ変換

### 生成されたモデル仕様

| パラメータ | 値 |
|---|---|
| 直径 | 60mm |
| ベース厚さ | 2mm |
| ロゴ浮き彫り高さ | 3mm |
| 合計高さ | 5mm |
| 形状 | コイン型メダリオン（縁付き） |

## 生成ファイル一覧

### 3Dファイル（3Dプリント / 3D CADソフト向け）

| ファイル | 形式 | 用途 | 対応ソフト |
|---|---|---|---|
| `github_logo.stl` | STL | 3Dプリントの標準形式 | Cura, PrusaSlicer, Fusion 360, AutoCAD |
| `github_logo.obj` | OBJ (Wavefront) | 汎用3Dフォーマット | Fusion 360, Blender, 3ds Max, Maya |
| `github_logo.3mf` | 3MF | 次世代3Dプリント形式 | Cura, PrusaSlicer, Windows 3D Viewer |
| `github_logo.ply` | PLY | 3Dスキャン/ポイントクラウド | MeshLab, CloudCompare, Fusion 360 |
| `github_logo.off` | OFF | シンプル3Dメッシュ | MeshLab, Geomview |

### 2Dファイル（2D CADソフト / ベクター編集向け）

| ファイル | 形式 | 用途 | 対応ソフト |
|---|---|---|---|
| `github_logo.dxf` | DXF | 2D CAD図面 | **AutoCAD**, Fusion 360, Illustrator |
| `github_logo.svg` | SVG | ベクター画像 | Inkscape, Illustrator, レーザーカッター |

### その他

| ファイル | 説明 |
|---|---|
| `GitHub-Mark-ea2971cee799.png` | 入力画像（元データ） |
| `generate_stl.py` | Copilot CLIが生成したPythonスクリプト |

## 3Dプリント推奨設定

```
レイヤー高さ: 0.2mm
インフィル:   20%
サポート:     不要
素材:         PLA推奨
ノズル温度:   200-210°C
ベッド温度:   60°C
```

## CADソフトでの編集方法

### Fusion 360 で開く場合
1. **3D編集**: `github_logo.obj` または `github_logo.stl` をインポート → メッシュ → BRep変換で編集可能に
2. **2D編集**: `github_logo.dxf` をインポート → スケッチとして読み込まれる → 押し出し等で3D化

### AutoCAD で開く場合
1. **2D図面**: `github_logo.dxf` を直接開く → ポリラインとして編集可能
2. **3Dモデル**: `github_logo.stl` をインポート

### Blender で開く場合
- `github_logo.obj` をインポート → モディファイアで編集

## 実験の感想

- **画像からSTL生成**: Copilot CLI がPythonコードを自動生成して、画像のピクセルデータからハイトマップベースのSTLメッシュを作成してくれた
- **フォーマット変換**: STLから OBJ, PLY, 3MF, DXF, SVG 等への変換も指示するだけで自動実行
- **パラメトリック**: `generate_stl.py` のパラメータ（直径、厚み等）を変えれば簡単にサイズ変更可能
- **制限**: 画像ベースのため、曲面のスムーズさはピクセル解像度に依存する。より滑らかなモデルが必要な場合はFusion 360等でBRep変換後に編集するのがベター

## 環境

- **ツール**: GitHub Copilot CLI
- **言語**: Python 3
- **ライブラリ**: Pillow, NumPy, numpy-stl, scipy, trimesh, ezdxf
- **日付**: 2026年3月20日

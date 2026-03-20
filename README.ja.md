# 🧪 GitHub Copilot CLI × CADファイル生成実験

> 🇺🇸 **English version here → [README.md](README.md)**

## 概要

**GitHub Copilot CLI** に画像（GitHub Octocatロゴ）を読み込ませ、3Dプリント可能なSTLファイルおよび各種CADフォーマットを自動生成できるか実験した記録です。

## 実験内容

### 入力
- **画像**: GitHub Mark（Octocatロゴ）の PNG画像（`GitHub-Mark-ea2971cee799.png`）

![GitHub Mark](GitHub-Mark-ea2971cee799.png)

### やったこと
1. GitHub Copilot CLI に画像ファイルを渡し、「この画像を元に3Dプリント用のCADを作って」と依頼
2. Copilot CLI が Python スクリプトを自動生成・実行
3. 画像をグレースケール化 → 二値化 → メッシュ化 → 貫通型3Dモデルを生成
4. STLファイルからさらに複数のCADフォーマット（OBJ, DXF等）へ変換
5. Fusion 360 や AutoCAD でも編集できるよう複数形式を出力

### 生成した2つのモデル

画像の白黒を使って **2種類の貫通型モデル** を生成：

#### ① `octocat_black_solid` — 黒部分がソリッド
- 元画像の **黒い円リング部分** がそのまま立体になる
- **Octocatシルエット部分は空洞（貫通穴）** になっている
- 用途：額縁・フレーム型、クッキー型の外枠など

#### ② `octocat_white_solid` — 白部分（Octocatシルエット）がソリッド
- 元画像の **Octocatシルエット（白い猫の形）** だけが立体になる
- 周囲の黒い部分は存在しない
- 用途：Octocatフィギュア、スタンプ、キーホルダーなど

### モデル仕様

| パラメータ | 値 |
|---|---|
| サイズ | 60mm × 60mm |
| 高さ（厚み） | 5mm |
| 形状 | 貫通型（空洞あり） |
| 解像度 | 500 × 500 ピクセルベース |

## 生成ファイル一覧

### 3Dファイル（3Dプリント / 3D CADソフト向け）

| ファイル | 形式 | 説明 | 対応ソフト |
|---|---|---|---|
| `octocat_black_solid.stl` | STL | 黒部分ソリッド（3Dプリント標準） | Cura, PrusaSlicer, Fusion 360, AutoCAD |
| `octocat_black_solid.obj` | OBJ | 黒部分ソリッド（汎用3D） | Fusion 360, Blender, 3ds Max, Maya |
| `octocat_black_solid.3mf` | 3MF | 黒部分ソリッド（次世代3Dプリント） | Cura, PrusaSlicer, Windows 3D Viewer |
| `octocat_black_solid.ply` | PLY | 黒部分ソリッド | MeshLab, CloudCompare, Fusion 360 |
| `octocat_black_solid.off` | OFF | 黒部分ソリッド | MeshLab, Geomview |
| `octocat_white_solid.stl` | STL | Octocatソリッド（3Dプリント標準） | Cura, PrusaSlicer, Fusion 360, AutoCAD |
| `octocat_white_solid.obj` | OBJ | Octocatソリッド（汎用3D） | Fusion 360, Blender, 3ds Max, Maya |
| `octocat_white_solid.3mf` | 3MF | Octocatソリッド（次世代3Dプリント） | Cura, PrusaSlicer, Windows 3D Viewer |
| `octocat_white_solid.ply` | PLY | Octocatソリッド | MeshLab, CloudCompare, Fusion 360 |
| `octocat_white_solid.off` | OFF | Octocatソリッド | MeshLab, Geomview |

### 2Dファイル（2D CADソフト / ベクター編集向け）

| ファイル | 形式 | 説明 | 対応ソフト |
|---|---|---|---|
| `octocat_black_solid.dxf` | DXF | 黒部分の2D輪郭 | **AutoCAD**, Fusion 360, Illustrator |
| `octocat_white_solid.dxf` | DXF | Octocatシルエットの2D輪郭 | **AutoCAD**, Fusion 360, Illustrator |

### その他

| ファイル | 説明 |
|---|---|
| `GitHub-Mark-ea2971cee799.png` | 入力画像（元データ） |
| `generate_cutout.py` | 貫通型モデル生成スクリプト |
| `generate_stl.py` | 初期版（コイン型メダリオン）生成スクリプト |

## 3Dプリント推奨設定

```
レイヤー高さ: 0.2mm
インフィル:   100%（貫通型なので中身は詰めた方が丈夫）
サポート:     不要
素材:         PLA推奨
ノズル温度:   200-210°C
ベッド温度:   60°C
```

## CADソフトでの編集方法

### Fusion 360 で開く場合
1. **3D編集**: `.obj` または `.stl` をインポート → 「メッシュ」→「BRep変換」で自由に編集可能
2. **2D → 3D**: `.dxf` をインポート → スケッチとして読み込み → 「押し出し」で好きな厚みに3D化

### AutoCAD で開く場合
1. **2D図面**: `.dxf` を直接開く → ポリラインとして編集可能
2. **3Dモデル**: `.stl` をインポート

### Blender で開く場合
- `.obj` をインポート → モディファイアで編集

## 実験の感想

- **画像からSTL生成**: Copilot CLI がPythonコードを自動生成し、画像のピクセルデータから水密メッシュの3Dモデルを作成してくれた
- **貫通型モデル**: 白黒の反転で「型」と「シルエット」の2パターンを自動生成できた
- **フォーマット変換**: STLから OBJ, PLY, 3MF, DXF 等への変換も指示するだけで自動実行
- **パラメトリック**: スクリプトのパラメータ（サイズ、厚み等）を変えれば簡単にカスタマイズ可能
- **制限**: 画像ベースのため、曲面のスムーズさはピクセル解像度に依存。より滑らかにしたい場合はFusion 360でBRep変換後にスムージングするのがベター

## 環境

- **ツール**: GitHub Copilot CLI
- **言語**: Python 3
- **ライブラリ**: Pillow, NumPy, numpy-stl, scipy, trimesh, ezdxf
- **日付**: 2026年3月20日

# ase_mymodule

ASE（Atomic Simulation Environment）向けの小さな補助ユーティリティ集です。  
現在は以下の2機能を提供しています。

- Fortran 形式の namelist 風入力ファイルを Python の辞書へ変換
- ASE の `Vasp` 計算機で、標準パラメータ以外の INCAR タグを追記

> ⚠️ 個人用途を前提とした実装です。利用は自己責任でお願いします。

---

## インストール

### 開発中のリポジトリをそのまま使う

```bash
pip install -e .
```

### 通常インストール

```bash
pip install .
```

---

## 使い方

### 1) namelist の読み込み

```python
from ase_mymodule import parse_input_namelist

params = parse_input_namelist("input.in")
print(params)
# 例: {'control': {'calculation': 'scf', 'nstep': 100}}
```

`parse_input_namelist` は `&section ... /` ブロックを読み取り、
キーを小文字化して辞書にします。

### 2) 追加 INCAR タグ付き VASP 計算機

```python
from ase_mymodule.vasp_any_param import VaspExtraTags

calc = VaspExtraTags(
    directory="calc",
    xc="PBE",
    encut=500,
    kpts=(4, 4, 1),
    extra_incar={
        "ESMALPHA": 1.0,
        "LDIPOL": True,
        "DIPOL": [0.5, 0.5, 0.5],
    },
)
```

`write_input` 実行時、ASE が通常の `INCAR` を生成した後に
`extra_incar` の内容が追記されます。

---

## ディレクトリ構成

```text
.
├── ase_mymodule/
│   ├── __init__.py        # 公開 API
│   ├── get_params.py      # namelist パーサ
│   └── vasp_any_param.py  # extra INCAR 対応 VASP 計算機
├── examples/
│   └── parse_namelist_example.py
├── README.md
├── setup.py
└── .gitignore
```

生成物（`*.egg-info/`, `build/`, `__pycache__/` など）は
リポジトリに含めない方針です。

---

## 開発メモ

```bash
python -m compileall ase_mymodule
```

必要に応じて `pip install -e .` 後に手元のスクリプトから動作確認してください。

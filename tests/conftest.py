# tests/conftest.py

import sys
from pathlib import Path

# このファイルから見て、1つ上の階層がプロジェクトルート
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# プロジェクトルートを Python パスの先頭に追加
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


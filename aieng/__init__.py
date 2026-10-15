from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"  # git-ignored: datasets, checkpoints, downloads
DATA.mkdir(exist_ok=True)

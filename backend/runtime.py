"""Separate immutable source data from disposable cloud calculation caches."""
import os
from pathlib import Path
from tempfile import gettempdir

ROOT = Path(__file__).resolve().parents[1]
SERVERLESS = os.environ.get('VERCEL') == '1'
RUNTIME_ROOT = Path(gettempdir()) / 'agrohydro' if SERVERLESS else ROOT


def writable_path(relative):
    return RUNTIME_ROOT / relative

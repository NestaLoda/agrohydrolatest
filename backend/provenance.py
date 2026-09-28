"""Append-only local provenance. Raw bytes are verified, never rewritten."""
import hashlib
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

class ProvenanceStore:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as c:
            c.execute("CREATE TABLE IF NOT EXISTS datasets (id TEXT PRIMARY KEY, sha256 TEXT NOT NULL, metadata TEXT NOT NULL)")
            c.execute("CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, request TEXT NOT NULL, result TEXT NOT NULL)")

    @contextmanager
    def connection(self):
        connection=sqlite3.connect(self.path, timeout=10)
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def register(self, metadata: dict, raw: bytes):
        actual = digest(raw)
        if metadata.get("content_sha256") != actual:
            raise ValueError("Ham dosyanın SHA-256 değeri kaynak kaydıyla uyuşmuyor.")
        for key in ("dataset_id", "provider", "source_url", "classification", "access_date", "units", "license"):
            if not metadata.get(key):
                raise ValueError(f"Kaynak kaydında zorunlu alan eksik: {key}")
        encoded = canonical(metadata)
        with self.connection() as c:
            old = c.execute("SELECT sha256,metadata FROM datasets WHERE id=?", (metadata["dataset_id"],)).fetchone()
            if old and (old[0] != actual or old[1] != encoded):
                raise ValueError("Bu veri kimliği farklı içerik/metadata ile kayıtlı; yeni sürüm kimliği gerekli.")
            c.execute("INSERT OR IGNORE INTO datasets VALUES (?,?,?)", (metadata["dataset_id"], actual, encoded))

    def record_run(self, request: dict, result: dict):
        encoded = canonical({"request": request, "result": result})
        run_id = digest(encoded.encode())[:24]
        with self.connection() as c:
            c.execute("INSERT OR IGNORE INTO runs VALUES (?,?,?,?)", (run_id, datetime.now(timezone.utc).isoformat(), canonical(request), canonical(result)))
        return run_id

    def datasets(self):
        with self.connection() as c:
            return [json.loads(row[0]) for row in c.execute("SELECT metadata FROM datasets ORDER BY id")]

def immutable_write(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as f:
            f.write(data)
    except FileExistsError:
        if path.read_bytes() != data:
            raise ValueError("Ham dosya değiştirilemez; yeni içerik kimliği kullanın.")

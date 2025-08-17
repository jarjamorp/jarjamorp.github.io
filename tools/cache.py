from __future__ import annotations
from pathlib import Path
import hashlib, json

def _ensure_dir(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)

def load_manifest(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "entries": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        # start fresh if corrupted
        return {"version": 1, "entries": {}}

def save_manifest(path: Path, data: dict) -> None:
    _ensure_dir(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)

def _stable_options_bytes(options: dict) -> bytes:
    # Stable, order-independent serialization of options
    # Tip: include a pipeline version string in options (see call site)
    s = json.dumps(options, sort_keys=True, separators=(",", ":"))
    return s.encode("utf-8")

def file_digest(path: Path, options: dict) -> str:
    """
    Digest of file bytes + options (to detect either content or option changes).
    Uses BLAKE2 for speed; SHA256 would also be fine.
    """
    h = hashlib.blake2b(digest_size=20)
    # include options first so even missing files can be handled consistently if needed
    h.update(_stable_options_bytes(options))
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def key_for(src: Path, project_root: Path) -> str:
    """
    Use a normalized, forward-slash relative path as the manifest key, so it’s stable across OSes.
    """
    rel = src.resolve().relative_to(project_root.resolve())
    return rel.as_posix()

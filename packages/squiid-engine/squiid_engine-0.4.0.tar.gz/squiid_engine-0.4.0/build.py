from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

RUST_DIR = Path(__file__).resolve().parent / "squiid-engine-rust"
DEST_DIR = Path(__file__).resolve().parent / "squiid_engine"


def find_shared_object() -> Path | None:
    target_dir = RUST_DIR / "target"

    # Ensure the target directory exists
    if not target_dir.exists():
        raise FileNotFoundError(f"The target directory '{target_dir}' does not exist.")

    # check base release directory
    if (target_dir / "release").is_dir():
        for file in (target_dir / "release").iterdir():
            if any(file.match(ext) for ext in ["*.so", "*.dll", "*.dylib"]):
                return file

    # check other target directories
    for directory in target_dir.iterdir():
        if directory.is_dir() and (directory / "release").is_dir():
            for file in (directory / "release").iterdir():
                if any(file.match(ext) for ext in ["*.so", "*.dll", "*.dylib"]):
                    return file

    return None


def build_shared_object() -> None:
    _ = subprocess.run(
        ["cargo", "build", "--lib", "--release", "--features", "ffi"],
        cwd=RUST_DIR,
        check=True,
    )

    shared_library = find_shared_object()

    if shared_library is None:
        raise FileNotFoundError("Shared library not found")

    # remove old shared objects
    for f in DEST_DIR.glob("*.so"):
        f.unlink()

    for f in DEST_DIR.glob("*.dll"):
        f.unlink()

    for f in DEST_DIR.glob("*.dylib"):
        f.unlink()

    target_path = DEST_DIR / shared_library.name
    shutil.copy(shared_library, target_path)
    print(f"Copied {shared_library} to {target_path}")


if __name__ == "__main__":
    build_shared_object()

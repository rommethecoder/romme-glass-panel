#!/usr/bin/env python3
"""Validate or install a user-level style without applying it to the current session."""

import hashlib
import argparse
import json
import os
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

ID = "romme-glass-panel"
SOURCE = Path(__file__).resolve().parent / "theme"
FILES = {
    "metadata.json",
    "plasmarc",
    "widgets/panel-background.svg",
    ".romme-glass-panel-install",
}


def check(source=SOURCE):
    meta = json.loads((source / "metadata.json").read_text())
    if meta.get("KPackageStructure") != "Plasma/Theme" or meta["KPlugin"]["Id"] != ID:
        raise ValueError("Unexpected style identity.")
    tree = ET.parse(source / "widgets/panel-background.svg")
    ids = {n.get("id") for n in tree.iter()}
    if (
        not {
            "center",
            "top",
            "bottom",
            "left",
            "right",
            "topleft",
            "topright",
            "bottomleft",
            "bottomright",
        }
        <= ids
    ):
        raise ValueError("Missing nine-slice elements.")
    return meta


def target(data_home):
    root = Path(data_home).expanduser()
    for parent in [root, *root.parents]:
        if parent.is_symlink():
            raise ValueError("Data directory must not contain symlinks.")
    dest = root / "plasma/desktoptheme" / ID
    for parent in [dest.parent, *dest.parent.parents]:
        if parent.is_symlink():
            raise ValueError("Style parent directory must not contain symlinks.")
    return dest


def install(data_home):
    check()
    dest = target(data_home)
    if dest.exists() or dest.is_symlink():
        raise ValueError(
            "Style already exists; back up and remove the old package explicitly first."
        )
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, dest)
    hashes = {
        name: hashlib.sha256((dest / name).read_bytes()).hexdigest()
        for name in FILES
        if not name.startswith(".")
    }
    (dest / ".romme-glass-panel-install").write_text(
        json.dumps({"version": 1, "hashes": hashes})
    )
    return dest


def uninstall(data_home):
    dest = target(data_home)
    if dest.is_symlink() or not (dest / ".romme-glass-panel-install").is_file():
        raise ValueError("Only packages installed by this script can be removed.")
    actual = {p.relative_to(dest).as_posix() for p in dest.rglob("*") if not p.is_dir()}
    if actual != FILES or any(p.is_symlink() for p in dest.rglob("*")):
        raise ValueError("Package contents changed; back up and remove manually.")
    manifest = json.loads((dest / ".romme-glass-panel-install").read_text())
    if (
        manifest.get("version") != 1
        or any(
            hashlib.sha256((dest / name).read_bytes()).hexdigest() != digest
            for name, digest in manifest["hashes"].items()
        )
        or set(manifest["hashes"]) != FILES - {".romme-glass-panel-install"}
    ):
        raise ValueError("Installed files changed; back up and remove manually.")
    check(dest)
    shutil.rmtree(dest)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["check", "install", "uninstall"])
    p.add_argument(
        "--data-home", default=os.environ.get("XDG_DATA_HOME", "~/.local/share")
    )
    p.add_argument("--confirm", action="store_true")
    a = p.parse_args()
    try:
        if a.action == "check":
            print(json.dumps(check(), indent=2))
        elif a.action == "install":
            print(install(a.data_home))
        elif not a.confirm:
            p.error(
                "Uninstall needs --confirm; switch styles in System Settings first."
            )
        else:
            uninstall(a.data_home)
            print("Style removed.")
    except (OSError, ValueError, ET.ParseError) as e:
        p.exit(1, str(e) + "\n")


if __name__ == "__main__":
    main()

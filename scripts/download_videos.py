#!/usr/bin/env python3
"""Download EgoArgus videos from the release manifest."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import pathlib
import sys
import urllib.request

UTC = dt.timezone.utc


def sha256sum(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, output_path: pathlib.Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response:
        with output_path.open("wb") as handle:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)


def parse_expiry(value: str) -> dt.datetime | None:
    value = value.strip()
    if not value:
        return None
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="metadata/video_manifest.csv",
        type=pathlib.Path,
        help="CSV manifest with file_name, download_url, and optional sha256 columns.",
    )
    parser.add_argument(
        "--out-dir",
        default="videos",
        type=pathlib.Path,
        help="Directory for downloaded videos.",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Verify existing files without downloading missing assets.",
    )
    parser.add_argument(
        "--allow-expired",
        action="store_true",
        help="Attempt downloads even when url_expires_at is in the past.",
    )
    args = parser.parse_args()

    with args.manifest.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    for row in rows:
        file_name = row.get("file_name", "").strip()
        url = (row.get("download_url") or row.get("r2_url") or "").strip()
        expires_at = parse_expiry(row.get("url_expires_at", ""))
        expected_sha256 = row.get("sha256", "").strip()
        if not file_name:
            raise ValueError("Manifest row is missing file_name")

        output_path = args.out_dir / file_name
        if expires_at and expires_at <= dt.datetime.now(UTC) and not args.allow_expired:
            raise ValueError(
                f"Manifest URL for {file_name} expired at {expires_at.isoformat()}. "
                "Refresh the manifest or pass --allow-expired to try anyway."
            )

        if not output_path.exists():
            if args.verify_only:
                raise FileNotFoundError(output_path)
            if not url:
                raise ValueError(f"Manifest row for {file_name} is missing download_url")
            print(f"Downloading {file_name}")
            try:
                download(url, output_path)
            except Exception:
                if output_path.exists():
                    output_path.unlink()
                raise

        if expected_sha256:
            actual_sha256 = sha256sum(output_path)
            if actual_sha256 != expected_sha256:
                raise ValueError(
                    f"Checksum mismatch for {file_name}: "
                    f"expected {expected_sha256}, got {actual_sha256}"
                )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)

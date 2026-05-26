#!/usr/bin/env python3
"""Fill a video manifest with Cloudflare Worker-signed download URLs."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hmac
import os
import pathlib
from hashlib import sha256
from urllib.parse import quote

UTC = dt.timezone.utc


def sign(secret: str, method: str, path: str, expires_at: int) -> str:
    payload = f"{method}\n{path}\n{expires_at}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), payload, sha256).hexdigest()


def build_url(base_url: str, object_key: str, secret: str, expires_at: int) -> str:
    base = base_url.rstrip("/")
    path = "/" + quote(object_key.lstrip("/"), safe="/~.-_")
    signature = sign(secret, "GET", path, expires_at)
    return f"{base}{path}?exp={expires_at}&sig={signature}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--base-url", required=True, help="Worker base URL.")
    parser.add_argument(
        "--secret-env",
        default="EGOARGUS_URL_SIGNING_SECRET",
        help="Environment variable containing the Worker URL signing secret.",
    )
    parser.add_argument("--days", type=int, default=60)
    parser.add_argument(
        "--expires-at",
        default="",
        help="Optional ISO-8601 UTC expiry timestamp. Overrides --days.",
    )
    return parser.parse_args()


def expiry_from_args(args: argparse.Namespace) -> dt.datetime:
    if args.expires_at:
        value = args.expires_at
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        parsed = dt.datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)
    return dt.datetime.now(UTC) + dt.timedelta(days=args.days)


def main() -> None:
    args = parse_args()
    secret = os.environ.get(args.secret_env)
    if not secret:
        raise SystemExit(f"Missing signing secret env var: {args.secret_env}")

    expires = expiry_from_args(args)
    expires_epoch = int(expires.timestamp())
    expires_iso = expires.isoformat(timespec="seconds").replace("+00:00", "Z")

    with args.manifest.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    required_fields = ["download_url", "url_expires_at", "access_mode"]
    for field in required_fields:
        if field not in fieldnames:
            fieldnames.append(field)

    for row in rows:
        object_key = (row.get("r2_object_key") or "").strip()
        if not object_key:
            raise SystemExit(
                f"Row for {row.get('video_id') or row.get('file_name') or '<unknown>'} "
                "is missing r2_object_key"
            )
        row["download_url"] = build_url(args.base_url, object_key, secret, expires_epoch)
        row["url_expires_at"] = expires_iso
        row["access_mode"] = "worker_signed"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()

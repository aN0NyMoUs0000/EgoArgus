# R2 Video Access

EgoArgus videos are hosted in Cloudflare R2 and referenced from
`metadata/video_manifest.csv`.

## Access Policy

Use R2 for video storage. Do not commit raw videos to GitHub.

For anonymous review, the target link lifetime is two months. In practical
release terms, use one of the following:

- `worker_signed`: a Cloudflare Worker validates a URL signature and expiry,
  then reads from a private R2 bucket. This supports a 60-day review window
  without exposing R2 API credentials.
- `public`: a public/custom-domain R2 URL that is intentionally available for
  the review window, then disabled, moved, or rotated after the deadline.
- `r2_presigned`: native R2 presigned URLs. Use this only for short-lived smoke
  tests or refreshed handoff packages because native presigned URLs expire after
  at most seven days.

The planned two-month review window is 60 days (`5,184,000` seconds). For a
release on 2026-05-26, the calendar target is 2026-07-26.

## Worker-Signed URL Flow

1. Upload or mirror videos into R2.
2. Populate `metadata/video_manifest.csv` with `r2_object_key` and file
   metadata.
3. Deploy `workers/r2_signed_download_worker.js` with an R2 bucket binding and
   `URL_SIGNING_SECRET`.
4. Run `scripts/sign_worker_urls.py` with the same secret to fill
   `download_url`, `url_expires_at`, and `access_mode`.
5. Commit the manifest, not the secret.

The example Worker configuration is in `wrangler.example.toml`. Copy it to
`wrangler.toml`, set the real bucket name locally, and do not commit secrets.

Deploy outline:

```bash
cp wrangler.example.toml wrangler.toml
# edit wrangler.toml bucket_name locally
npx wrangler deploy
npx wrangler secret put URL_SIGNING_SECRET
```

Example:

```bash
export EGOARGUS_URL_SIGNING_SECRET="..."
python scripts/sign_worker_urls.py \
  --manifest metadata/video_manifest.csv \
  --base-url https://egoargus-review.example.workers.dev \
  --days 60 \
  --output metadata/video_manifest.csv
```

## Existing VISTA API

The VISTA server already has an R2 signer/upload endpoint that reads the
standard `R2_*` environment variables and caches uploads. It is useful for smoke
tests and handoff refreshes. Its native R2 presigned URLs should stay within the
seven-day R2 limit, so they are not the right static paper URL format for a
two-month review window.

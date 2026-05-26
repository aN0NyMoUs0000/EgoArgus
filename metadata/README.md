# Metadata

`video_manifest.csv` should contain one row per hosted video asset:

- `video_id`: stable identifier used by the CSV metadata
- `scenario`: scenario or condition name
- `split`: benchmark split
- `file_name`: local file name after download
- `r2_object_key`: Cloudflare R2 object key
- `download_url`: public, Worker-signed, or short-lived presigned download URL
- `url_expires_at`: ISO-8601 expiry timestamp for time-limited URLs
- `access_mode`: for example `worker_signed`, `public`, or `r2_presigned`
- `sha256`: optional checksum for verification
- `size_bytes`: optional file size

Native R2 presigned URLs expire after at most seven days. Use Worker-signed or
public/custom-domain URLs for the two-month anonymous review window.

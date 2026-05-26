# Metadata

`video_manifest.csv` should contain one row per hosted video asset:

- `video_id`: stable identifier used by the CSV metadata
- `scenario`: scenario or condition name
- `split`: benchmark split
- `file_name`: local file name after download
- `r2_url`: public or signed object-storage URL
- `sha256`: optional checksum for verification
- `size_bytes`: optional file size

# EgoArgus

**Benchmarking VLMs as Situational Assistants for Modality-Grounded User Supports**

This repository provides the anonymous review release scaffold for the EgoArgus
benchmark. The benchmark evaluates whether vision-language models can provide
situational user support grounded in the correct modality evidence.

## Release Contents

- `data/` contains scenario-level metadata CSV files.
- `metadata/` contains video manifests and checksums for externally hosted
  assets.
- `scripts/` contains utilities for signing and downloading video assets from
  R2-backed object storage.
- `workers/` contains an optional Cloudflare Worker template for two-month
  signed review links.

Large video files are hosted outside GitHub. The repository is designed so the
submission URL can remain stable while data files and manifests are updated after
the review deadline.

## Video Access

Videos are hosted in Cloudflare R2. For the anonymous review release, use
manifest URLs with a two-month access window, such as Worker-signed R2 download
URLs. Native R2 presigned URLs are only suitable for short refresh windows
because their maximum expiry is seven days.

The current video manifest enumerates 344 R2-hosted videos copied under the
anonymous `egoargus/review-20260526/videos/` object prefix.

The planned review window is 60 days (`5,184,000` seconds). For a release made
on 2026-05-26, the corresponding calendar target is 2026-07-26.

## Included CSV Files

The review release includes the following metadata CSV files:

- `aggregated_corrected_samples.csv`: 2,000 samples, containing the
  multimodal grounded and contradictory scenarios
- `offtopic_samples.csv`: 2,000 video-grounded off-topic samples
- `ontopic_samples.csv`: 2,000 video-grounded on-topic samples
- `text_grounded_samples.csv`: 978 text-grounded samples

## Versioning

For paper review, use a fixed Git tag or GitHub release, for example:

```bash
git tag v1.0-submission
git push origin v1.0-submission
```

Subsequent updates can continue on `main` while the submitted version remains
recoverable.

## Citation

```bibtex
@misc{egoargus2026,
  title = {EgoArgus: Benchmarking VLMs as Situational Assistants for Modality-Grounded User Supports},
  year = {2026},
  note = {Anonymous review release}
}
```

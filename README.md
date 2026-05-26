# EgoArgus

**Benchmarking VLMs as Situational Assistants for Modality-Grounded User Supports**

This repository provides the anonymous review release scaffold for the EgoArgus
benchmark. The benchmark evaluates whether vision-language models can provide
situational user support grounded in the correct modality evidence.

## Release Contents

- `data/` contains scenario-level metadata CSV files.
- `metadata/` contains video manifests and checksums for externally hosted
  assets.
- `scripts/` contains utilities for downloading video assets from object
  storage.

Large video files are hosted outside GitHub. The repository is designed so the
submission URL can remain stable while data files and manifests are updated after
the review deadline.

## Expected CSV Files

The review release is expected to include the following CSV files once access to
the source data is available:

- `aggregated_corrected_samples.csv`, containing the multimodal grounded and
  contradictory samples
- three scenario-specific CSV files matching the source release names

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

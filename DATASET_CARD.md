# Dataset Card

## Dataset Summary

EgoArgus is an egocentric video benchmark for evaluating whether
vision-language models can act as situational assistants. Each example pairs a
video with metadata describing the user-support scenario and the modality
evidence required to answer appropriately.

## Task

Models are evaluated on whether their support is grounded in the relevant
visual, textual, or cross-modal evidence instead of relying on unsupported
assumptions.

## Data Fields

The exact CSV schema will be documented with the finalized metadata release. The
release is expected to include identifiers for videos, scenarios, prompts,
support targets, and split assignments.

## Video Assets

Videos are not stored in GitHub. Use `metadata/video_manifest.csv` to map each
example to an externally hosted object-storage URL. Use
`scripts/download_videos.py` to fetch and verify assets once the manifest is
populated.

## Intended Use

This release is intended for anonymous paper review and reproducible benchmark
evaluation.

## Limitations

The anonymous review scaffold may omit final licensing, hosting, and checksum
details until the official dataset release is prepared.

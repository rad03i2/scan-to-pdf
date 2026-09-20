# Security Policy

Scan to PDF is a local file-processing utility. It intentionally has no network feature, credential handling, telemetry, or remote execution path.

## Reporting
Please report security concerns through GitHub's private vulnerability reporting feature when available. Do not publish confidential documents or personal data in an issue. Provide a minimal synthetic reproducer.

## Scope and safe-use notes
- Source images are read-only from the application's perspective.
- Existing output files are rejected unless `--overwrite` is explicitly supplied.
- Generated PDFs are not encrypted and may retain visual sensitive information present in the source pixels.
- Treat untrusted image files cautiously and keep Pillow updated, because image decoding is performed by Pillow.

Security contact identity: **Radwan Abdulhadi Ahmed / رضوان عبدالهادي أحمد / @rad03i2**.

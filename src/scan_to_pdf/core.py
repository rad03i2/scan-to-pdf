from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Iterable

from PIL import Image, ImageEnhance, ImageOps, UnidentifiedImageError

SUPPORTED = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}


class ScanError(Exception):
    """A user-facing conversion error."""


@dataclass(frozen=True)
class Options:
    grayscale: bool = False
    auto_contrast: bool = False
    rotate: int = 0
    brightness: float = 1.0
    quality: int = 90
    dpi: int = 150


def collect_inputs(paths: Iterable[str], recursive: bool = False) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw).expanduser()
        if p.is_dir():
            iterator = p.rglob("*") if recursive else p.glob("*")
            files.extend(x for x in iterator if x.is_file() and x.suffix.lower() in SUPPORTED)
        elif p.is_file() and p.suffix.lower() in SUPPORTED:
            files.append(p)
        elif not p.exists():
            raise ScanError(f"Input does not exist: {p}")
        else:
            raise ScanError(f"Unsupported input: {p}")
    # Stable natural-ish order suitable for scan-001, scan-002, ...
    return sorted(dict.fromkeys(x.resolve() for x in files), key=lambda x: str(x).lower())


def _prepare(path: Path, options: Options) -> Image.Image:
    try:
        with Image.open(path) as source:
            source.load()
            image = ImageOps.exif_transpose(source)
            if options.rotate:
                image = image.rotate(-options.rotate, expand=True)
            if options.grayscale:
                image = ImageOps.grayscale(image)
            if options.auto_contrast:
                image = ImageOps.autocontrast(image.convert("L") if image.mode not in ("L", "RGB") else image)
            if options.brightness != 1.0:
                image = ImageEnhance.Brightness(image).enhance(options.brightness)
            # PDF/JPEG-friendly modes; flatten alpha on white instead of producing black transparency.
            if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
                rgba = image.convert("RGBA")
                background = Image.new("RGBA", rgba.size, "white")
                image = Image.alpha_composite(background, rgba).convert("RGB")
            elif image.mode not in ("RGB", "L"):
                image = image.convert("RGB")
            return image.copy()
    except (UnidentifiedImageError, OSError) as exc:
        raise ScanError(f"Cannot read image {path}: {exc}") from exc


def convert(paths: Iterable[str], output: str, options: Options, recursive: bool = False, overwrite: bool = False) -> dict:
    if options.rotate not in (0, 90, 180, 270):
        raise ScanError("rotate must be 0, 90, 180, or 270")
    if not 1 <= options.quality <= 100 or not 72 <= options.dpi <= 600 or options.brightness <= 0:
        raise ScanError("quality must be 1..100, dpi 72..600, and brightness > 0")
    files = collect_inputs(paths, recursive)
    if not files:
        raise ScanError("No supported images found")
    target = Path(output).expanduser().resolve()
    if target.suffix.lower() != ".pdf":
        raise ScanError("Output must use the .pdf extension")
    if target in files:
        raise ScanError("Output cannot be an input file")
    if target.exists() and not overwrite:
        raise ScanError(f"Output exists: {target}; pass --overwrite to replace it")
    target.parent.mkdir(parents=True, exist_ok=True)
    images = [_prepare(p, options) for p in files]
    temp_path: Path | None = None
    try:
        with NamedTemporaryFile(prefix=f".{target.stem}-", suffix=".pdf", dir=target.parent, delete=False) as tmp:
            temp_path = Path(tmp.name)
        first, rest = images[0], images[1:]
        first.save(temp_path, "PDF", save_all=True, append_images=rest, resolution=options.dpi, quality=options.quality)
        temp_path.replace(target)
    except OSError as exc:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise ScanError(f"Failed to write PDF: {exc}") from exc
    finally:
        for image in images:
            image.close()
    return {"output": str(target), "pages": len(files), "inputs": [str(p) for p in files], "bytes": target.stat().st_size}

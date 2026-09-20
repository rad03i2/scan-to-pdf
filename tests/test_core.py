from pathlib import Path
import pytest
from PIL import Image
from scan_to_pdf.core import Options, ScanError, collect_inputs, convert


def make_image(path: Path, color="white"):
    Image.new("RGB", (80, 120), color).save(path)


def test_collect_is_stable_and_filters(tmp_path):
    make_image(tmp_path / "02.png")
    make_image(tmp_path / "01.jpg")
    (tmp_path / "note.txt").write_text("ignore")
    assert [p.name for p in collect_inputs([str(tmp_path)])] == ["01.jpg", "02.png"]


def test_multi_page_pdf(tmp_path):
    make_image(tmp_path / "01.png")
    make_image(tmp_path / "02.png", "gray")
    out = tmp_path / "scan.pdf"
    result = convert([str(tmp_path / "01.png"), str(tmp_path / "02.png")], str(out), Options(grayscale=True, auto_contrast=True))
    assert result["pages"] == 2
    data = out.read_bytes()
    assert data.startswith(b"%PDF")
    assert data.rstrip().endswith(b"%%EOF")
    assert result["bytes"] == len(data)


def test_refuses_overwrite(tmp_path):
    image = tmp_path / "scan.png"; make_image(image)
    out = tmp_path / "out.pdf"; out.write_bytes(b"keep")
    with pytest.raises(ScanError, match="Output exists"):
        convert([str(image)], str(out), Options())
    assert out.read_bytes() == b"keep"


def test_validation(tmp_path):
    image = tmp_path / "scan.png"; make_image(image)
    with pytest.raises(ScanError, match="dpi"):
        convert([str(image)], str(tmp_path / "x.pdf"), Options(dpi=10))
    with pytest.raises(ScanError, match=".pdf"):
        convert([str(image)], str(tmp_path / "x.txt"), Options())


def test_recursive(tmp_path):
    nested = tmp_path / "a"; nested.mkdir(); make_image(nested / "page.webp")
    assert collect_inputs([str(tmp_path)], recursive=False) == []
    assert len(collect_inputs([str(tmp_path)], recursive=True)) == 1

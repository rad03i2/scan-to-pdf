# Scan to PDF

A small, privacy-friendly command-line tool that turns scanned images or photographed pages into a clean multi-page PDF **entirely on your computer**.

**Author:** Radwan Abdulhadi Ahmed · رضوان عبدالهادي أحمد · GitHub: @rad03i2

## Why it exists
Scanner apps often upload documents or lock basic export behind an account. Scan to PDF provides a predictable local workflow for assembling page images, with useful cleanup controls and safe output behavior.

## Features
- JPEG, PNG, TIFF, BMP and WebP input via Pillow.
- One image, many images, or a directory; optional recursive discovery.
- Stable filename ordering for numbered scans.
- Multi-page PDF output.
- EXIF orientation correction, grayscale, automatic contrast, 90° rotation and brightness adjustment.
- Configurable PDF DPI and image quality.
- Transparent images are flattened onto white.
- Existing output is protected unless `--overwrite` is explicit.
- Temporary-file write before final replacement.
- Human-readable or JSON result output.
- No cloud service, telemetry, account, API key, or `.env` file.

## Requirements & installation
Python 3.10+ is required.

```bash
git clone https://github.com/rad03i2/scan-to-pdf.git
cd scan-to-pdf
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -e .
```

For development/tests: `pip install -e . pytest`.

## Usage
```bash
# Two pages in explicit order
scan-to-pdf page-01.jpg page-02.jpg -o document.pdf

# A scan directory, cleaned for readability
scan-to-pdf ./scans -o document.pdf --grayscale --auto-contrast --dpi 200

# Include nested folders, rotate clockwise, machine-readable result
scan-to-pdf ./scans -o document.pdf --recursive --rotate 90 --json

# Explicitly replace an existing result
scan-to-pdf ./scans -o document.pdf --overwrite
```
Run `scan-to-pdf --help` for every option. Files discovered from directories are sorted by resolved path; pass files explicitly when you need a custom page order.

## Configuration
There is intentionally no persistent configuration. CLI arguments make each conversion reproducible. Defaults are quality 90, 150 DPI, normal color/contrast, brightness 1.0, and no overwrite.

## Preview / screenshots
This is a CLI project. A useful repository preview is a terminal capture showing the source page filenames, the conversion command, and the resulting PDF open in a desktop PDF viewer. Do not commit personal scanned documents as screenshots.

## Project structure
```text
src/scan_to_pdf/core.py   image discovery, preprocessing and PDF writing
src/scan_to_pdf/cli.py    command-line interface
tests/test_core.py        functional and safety tests
.github/workflows/ci.yml  cross-platform CI
pyproject.toml             packaging and metadata
```

## Testing
```bash
pip install -e . pytest
pytest -q
```
CI runs the suite on Windows, Linux and macOS with multiple supported Python versions. Tests generate their own temporary images and do not need private sample documents.

## Security & privacy
Processing is local. The program does not send files anywhere. It refuses accidental overwrite by default and does not modify source images. Still keep backups of important scans. PDF output is **not encrypted**, and this tool does not redact sensitive pixels or perform forensic metadata sanitization.

## Limitations
- Input is image-based; existing PDF files are not accepted as pages.
- No OCR/searchable text layer.
- No scanner hardware/WIA/TWAIN integration or GUI.
- Cleanup is deliberately conservative: no deskew, dewarp, crop detection, denoise, or background removal.
- Very large batches are prepared in memory before PDF writing.
- PDF page size follows the raster image dimensions/resolution rather than forcing A4/Letter.

## Optional roadmap
OCR, streaming large batches, automatic deskew/crop, and explicit A4/Letter fitting are reasonable future additions; they are not implemented today.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes focused, tested, local-first, and backwards-compatible where practical.

## License
MIT — see [LICENSE](LICENSE).

## Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# العربية — تحويل المسح إلى PDF

أداة سطر أوامر صغيرة وتركّز على الخصوصية لتحويل صور الصفحات الممسوحة أو المصوّرة إلى ملف PDF متعدد الصفحات، مع تنفيذ المعالجة **محليًا على جهازك**.

**المؤلف:** Radwan Abdulhadi Ahmed · رضوان عبدالهادي أحمد · GitHub: @rad03i2

## لماذا هذا المشروع؟
بعض تطبيقات المسح ترفع المستندات إلى خوادم خارجية أو تتطلب حسابًا للتصدير. يوفر هذا المشروع طريقة محلية واضحة لجمع صور الصفحات في PDF مع تحسينات أساسية وحماية من الاستبدال العرضي.

## المميزات
- دعم JPEG وPNG وTIFF وBMP وWebP بواسطة Pillow.
- قبول صورة واحدة أو عدة صور أو مجلد كامل، مع بحث متداخل اختياري.
- ترتيب ثابت للملفات المكتشفة، مناسب للأسماء المرقمة.
- إنشاء PDF متعدد الصفحات.
- تصحيح اتجاه EXIF، وتحويل رمادي، وتحسين تباين تلقائي، وتدوير 90 درجة، وضبط السطوع.
- التحكم بالدقة DPI والجودة.
- وضع خلفية بيضاء للشفافية.
- عدم استبدال الناتج الموجود إلا عند تمرير `--overwrite` صراحةً.
- الكتابة إلى ملف مؤقت قبل اعتماد الناتج النهائي.
- نتيجة نصية أو JSON للأتمتة.
- بلا سحابة أو تتبع أو حساب أو مفتاح API.

## المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث.

```bash
git clone https://github.com/rad03i2/scan-to-pdf.git
cd scan-to-pdf
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -e .
```

للتطوير والاختبارات: `pip install -e . pytest`.

## الاستخدام
```bash
scan-to-pdf page-01.jpg page-02.jpg -o document.pdf
scan-to-pdf ./scans -o document.pdf --grayscale --auto-contrast --dpi 200
scan-to-pdf ./scans -o document.pdf --recursive --rotate 90 --json
scan-to-pdf ./scans -o document.pdf --overwrite
```
استخدم `scan-to-pdf --help` لرؤية جميع الخيارات. الملفات القادمة من المجلدات تُرتب حسب المسار؛ مرر أسماء الملفات يدويًا إذا احتجت ترتيب صفحات خاصًا.

## الإعداد
لا يوجد ملف إعداد دائم عمدًا؛ معاملات CLI تجعل عملية التحويل قابلة للتكرار. القيم الافتراضية: جودة 90، ودقة 150 DPI، وسطوع 1.0، ولا يوجد استبدال تلقائي.

## المعاينة والصور
لأن المشروع CLI، يمكن أن تكون صورة المعاينة لقطة طرفية تعرض أسماء الصفحات وأمر التحويل ثم ملف PDF الناتج في قارئ PDF. لا ترفع مستندات شخصية إلى المستودع لأغراض العرض.

## بنية المشروع
`core.py` للاكتشاف والمعالجة والكتابة، و`cli.py` لواجهة الأوامر، و`tests/` للاختبارات، و`.github/workflows/ci.yml` للتكامل المستمر، و`pyproject.toml` للحزمة والبيانات الوصفية.

## الاختبارات
```bash
pip install -e . pytest
pytest -q
```
تولّد الاختبارات صورها المؤقتة بنفسها ولا تحتاج مستندات شخصية، ويشغّل CI الاختبارات على Windows وLinux وmacOS وإصدارات Python متعددة.

## الأمان والخصوصية
المعالجة محلية ولا تُرسل الملفات لأي جهة. الأداة لا تعدّل صور المصدر وترفض استبدال الناتج افتراضيًا. مع ذلك احتفظ بنسخة احتياطية من المستندات المهمة. ملف PDF الناتج **غير مشفر**، والأداة ليست أداة تنقيح للمعلومات الحساسة أو تنظيف جنائي للبيانات الوصفية.

## القيود
لا تقبل ملفات PDF كمدخلات، ولا توفر OCR أو طبقة نص قابلة للبحث، ولا تتصل مباشرة بالماسح الضوئي ولا توفر GUI. كذلك لا يوجد deskew أو dewarp أو اكتشاف تلقائي للحواف أو إزالة ضوضاء، وتُجهز الدفعات الكبيرة في الذاكرة. حجم الصفحة يتبع أبعاد ودقة الصورة ولا يُفرض A4 أو Letter.

## تطويرات اختيارية مستقبلية
يمكن لاحقًا إضافة OCR، ومعالجة تدفقية للدفعات الكبيرة، وتصحيح الميل والقص التلقائي، وملاءمة A4/Letter. هذه ليست ميزات موجودة حاليًا.

## المساهمة
راجع [CONTRIBUTING.md](CONTRIBUTING.md). يجب أن تبقى التغييرات محددة ومختبرة ومحلية المعالجة قدر الإمكان.

## الترخيص
MIT — راجع [LICENSE](LICENSE).

## المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

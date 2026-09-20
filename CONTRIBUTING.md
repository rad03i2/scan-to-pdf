# Contributing / المساهمة

Thanks for improving Scan to PDF. Please keep changes focused and avoid introducing network services into the core conversion path.

1. Create a branch from `main`.
2. Install with `pip install -e . pytest`.
3. Add or update tests for behavioral changes.
4. Run `pytest -q` before opening a pull request.
5. Update both English and Arabic README sections when user-facing behavior changes.

Bug reports should include OS, Python version, command used, image format, and the error text. Never attach confidential scanned documents; create a synthetic reproduction instead.

---

شكرًا لمساهمتك. اجعل التغييرات محددة، وأضف اختبارات للسلوك الجديد، وشغّل `pytest -q` قبل طلب الدمج. عند تغيير سلوك المستخدم حدّث قسمي README الإنجليزي والعربي. لا ترفق مستندات ممسوحة سرية في البلاغات؛ استخدم مثالًا اصطناعيًا بدلًا منها.

Maintainer / المشرف: **Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — @rad03i2**

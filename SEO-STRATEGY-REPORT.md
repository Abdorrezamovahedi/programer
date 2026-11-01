# گزارش سئوی MCD Code Up
تاریخ: 2026-10-31
پایه URL: https://abdorrezamovahedi.github.io/programer

## مشکلات یافت‌شده (قبلی)
- نام فایل فارسی در ZIP قدیمی خراب بود → اصلاح شد
- دو درس HTML خالی → پر شد
- بخشی از indexهای بخش PHP نبود → ساخته شد
- هدف‌گذاری کلمه کلیدی صفحه اصلی و زبان‌ها یکدست و رقابتی نبود

## تغییرات این مرحله
### صفحه اصلی
- کلمه اصلی: آموزش برنامه‌نویسی از صفر
- Title: آموزش برنامه‌نویسی از صفر و رایگان | MCD Code Up
- H1: آموزش برنامه‌نویسی از صفر تا ساخت پروژه
- Schema: WebSite + Organization

### Python
- کلمه اصلی: آموزش پایتون از صفر
- Title/H1 مطابق استراتژی
- H2های مسیر واقعی دوره + لینک داخلی

### HTML / CSS / JavaScript / PHP
- Title، Description، H1، lead و H2های مرتبط با دسته واقعی
- Canonical خودارجاع
- BreadcrumbList

### فنی
- robots.txt با Allow و Sitemap
- sitemap.xml از فایل‌های واقعی
- Twitter card و OG پایه روی صفحات کلیدی

## دامنه اختصاصی
دامنه `.ir` توسط مالک اعلام نشده است. تمام Canonical و Sitemap فعلاً روی GitHub Pages است.
پس از اعلام دامنه باید: CNAME، DNS، به‌روزرسانی Canonical/Sitemap/OG انجام شود.
Redirect واقعی 301 از `/programer/` به ریشه دامنه در GitHub Pages محدود است؛ راهکار: Cloudflare یا هاست با قوانین Redirect.

## محدودیت آزمایش
PageSpeed / Search Console از این محیط اجرا نشد — نیاز به اقدام مالک پس از Deploy.

## کار مالک
1. Deploy کامل ZIP در ریشه مخزن
2. ثبت Search Console و ارسال sitemap
3. اعلام دامنه `.ir` برای مرحله انتقال

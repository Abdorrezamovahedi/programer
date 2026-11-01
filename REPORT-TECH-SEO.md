# گزارش اجرای فنی و سئو — MCD Code Up
تاریخ: 2026-10-31
Base URL: https://abdorrezamovahedi.github.io/programer

## انجام‌شده
- پردازش دسته‌ای 1773 صفحه HTML
- charset، viewport، theme-color، lang=fa
- canonical خودارجاع برای همه صفحات آموزشی
- title برای صفحات فاقد عنوان معنادار
- description برای صفحات فاقد توضیح
- robots index,follow (404: noindex)
- sitemap با 1771 URL
- بهینه‌سازی جزئی CSS (تصویر و content-visibility لیست‌ها)
- H1 برای صفحات بدون H1

## انجام‌نشده / محدودیت
- PageSpeed/Lighthouse واقعی: اجرا نشد
- Search Console: نیاز به مالک
- Redirect 301 سمت سرور: محدودیت GitHub Pages
- hreflang بین‌المللی: اضافه نشد (مسیرهای python/html زبان برنامه‌نویسی‌اند نه locale)
- بازنویسی دستی محتوای آموزشی تک‌تک درس‌ها: در این مرحله خودکارسازی متا/ساختار بود نه بازنویسی متن درس
- دامنه .ir: اعلام نشده

## Deploy
1. محتویات ZIP را در ریشه مخزن قرار دهید
2. .nojekyll را نگه دارید
3. Push و صبر برای GitHub Pages
4. Sitemap را در Search Console ثبت کنید

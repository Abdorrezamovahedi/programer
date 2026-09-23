#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate formal educational pages for 30 programming languages/topics."""

import os
import zipfile
from pathlib import Path

BASE = Path("/home/workdir/artifacts/site")
ZABAN = BASE / "zaban"

# Shared CSS (formal dark theme)
SHARED_CSS = '''
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Vazirmatn", system-ui, -apple-system, sans-serif;
  background-color: #0f1419;
  color: #e6edf3;
  line-height: 1.7;
  font-size: 16px;
}
a { text-decoration: none; color: inherit; }
header {
  width: 100%;
  background-color: #0d1117;
  border-bottom: 1px solid #21262d;
  padding: 16px 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
}
.logo { color: #58a6ff; font-size: 22px; font-weight: 700; }
.logo span { color: #8b949e; font-weight: 400; font-size: 13px; margin-right: 8px; }
nav { display: flex; gap: 6px; }
nav a {
  color: #8b949e; font-size: 14px; font-weight: 500;
  padding: 8px 14px; border-radius: 6px;
  transition: color 0.2s, background-color 0.2s;
}
nav a:hover { color: #e6edf3; background-color: #161b22; }
.hero {
  text-align: center;
  padding: 48px 24px 40px;
  background: linear-gradient(180deg, #0d1117 0%, #0f1419 100%);
  border-bottom: 1px solid #21262d;
}
.hero h1 {
  font-size: 32px; font-weight: 700; color: #e6edf3;
  margin-bottom: 12px; letter-spacing: -0.5px;
}
.hero p { color: #8b949e; font-size: 17px; max-width: 560px; margin: 0 auto; }
.container {
  width: 92%; max-width: 1280px; margin: 36px auto;
  display: grid; grid-template-columns: 280px 1fr; gap: 28px;
}
.sidebar {
  background-color: #0d1117;
  border: 1px solid #21262d;
  border-radius: 12px;
  padding: 20px 14px;
  height: fit-content;
  position: sticky; top: 80px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
}
.sidebar h2 {
  font-size: 12px; font-weight: 600; color: #8b949e;
  text-transform: uppercase; letter-spacing: 0.5px;
  margin-bottom: 14px; padding: 0 10px;
}
.sidebar-section { margin-bottom: 20px; }
.sidebar-section h3 {
  font-size: 12px; font-weight: 600; color: #58a6ff;
  margin: 12px 0 6px; padding: 0 10px;
}
.pythons {
  display: block; padding: 7px 10px; margin: 1px 0;
  border-radius: 6px; font-size: 13.5px; color: #c9d1d9;
  transition: background-color 0.15s, color 0.15s;
}
.pythons:hover { background-color: #161b22; color: #58a6ff; }
.pythons.active { background-color: #1f6feb22; color: #58a6ff; font-weight: 500; }
.content { display: flex; flex-direction: column; gap: 20px; }
.card {
  background-color: #0d1117;
  border: 1px solid #21262d;
  border-radius: 12px;
  padding: 26px 30px;
}
.card h2 {
  font-size: 20px; font-weight: 600; color: #e6edf3;
  margin-bottom: 14px;
}
.card p { color: #8b949e; font-size: 15.5px; line-height: 1.9; }
.cards {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;
}
.mini-card {
  background-color: #0d1117;
  border: 1px solid #21262d;
  border-radius: 10px;
  padding: 20px;
  transition: border-color 0.2s, transform 0.2s;
}
.mini-card:hover { border-color: #388bfd; transform: translateY(-2px); }
.mini-card h3 { font-size: 15px; font-weight: 600; color: #e6edf3; margin-bottom: 6px; }
.mini-card p { font-size: 13.5px; color: #8b949e; line-height: 1.6; }
.code-box {
  direction: ltr; text-align: left;
  background-color: #010409;
  border: 1px solid #21262d;
  border-radius: 8px;
  padding: 18px 22px;
  overflow-x: auto;
  margin-top: 8px;
}
.code-box code {
  font-family: "SF Mono", "Fira Code", Consolas, monospace;
  color: #7ee787; font-size: 14.5px; line-height: 1.7; white-space: pre;
}
footer {
  margin-top: 56px; padding: 28px 24px; text-align: center;
  background-color: #0d1117; border-top: 1px solid #21262d;
  color: #6e7681; font-size: 13px;
}
@media (max-width: 900px) {
  header { flex-direction: column; gap: 10px; padding: 14px 18px; }
  nav { flex-wrap: wrap; justify-content: center; }
  .hero h1 { font-size: 26px; }
  .container { grid-template-columns: 1fr; }
  .sidebar { position: static; max-height: none; }
  .cards { grid-template-columns: 1fr; }
}
'''

HEADER = '''
<header>
  <div class="logo">مدرسه برنامه‌نویسان <span>خاص</span></div>
  <nav>
    <a href="../../index.html">خانه</a>
    <a href="#">آموزش‌ها</a>
    <a href="#">تمرین‌ها</a>
    <a href="#">درباره ما</a>
  </nav>
</header>
'''

FOOTER = '''
<footer>
  مدرسه برنامه‌نویسان خاص · یادگیری ساختاریافته برنامه‌نویسی
</footer>
'''

# Language definitions: slug, name_fa, name_en, description, features, sample_code, sidebar_sections
LANGUAGES = [
  {
    "slug": "python",
    "name_fa": "پایتون",
    "name_en": "Python",
    "icon": "🐍",
    "desc": "پایتون یک زبان برنامه‌نویسی سطح بالا، قدرتمند و نسبتاً ساده است که برای ساخت برنامه‌ها، وب‌سایت‌ها، هوش مصنوعی، تحلیل داده و بسیاری از پروژه‌های دیگر استفاده می‌شود.",
    "features": [
      ("ساده و خوانا", "نحو پایتون به زبان طبیعی نزدیک است و یادگیری آن برای مبتدیان مناسب است."),
      ("قدرتمند و مقیاس‌پذیر", "از پروژه‌های کوچک تا سیستم‌های بزرگ سازمانی می‌توان با پایتون توسعه داد."),
      ("مناسب هوش مصنوعی", "یکی از اصلی‌ترین زبان‌های حوزه یادگیری ماشین و هوش مصنوعی است."),
    ],
    "code": 'print("Hello World!")\n\nname = "Abdorreza"\nprint(name)',
    "path_hint": "ابتدا با متغیرها و انواع داده آشنا شوید، سپس شرط‌ها، حلقه‌ها و توابع را یاد بگیرید. بعد از آن می‌توانید سراغ پروژه‌های واقعی بروید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه پایتون", "شروع کار", "ساختار نوشتاری", "خروجی (print)", "توضیحات"]),
      ("متغیرها و انواع داده", ["متغیرها", "نام‌گذاری متغیر", "انواع داده", "اعداد", "تبدیل نوع", "رشته‌ها", "برش رشته", "متدهای رشته", "بولین"]),
      ("عملگرها", ["عملگرهای حسابی", "انتسابی", "مقایسه‌ای", "منطقی", "هویتی", "عضویت", "بیتی", "اولویت عملگرها"]),
      ("ساختارهای داده", ["لیست‌ها", "تاپل‌ها", "مجموعه‌ها", "دیکشنری", "متدهای لیست", "متدهای دیکشنری"]),
      ("کنترل جریان", ["if / elif / else", "match", "حلقه while", "حلقه for", "break و continue"]),
      ("توابع", ["تعریف تابع", "آرگومان‌ها", "*args و **kwargs", "لامبدا", "بازگشت", "حوزه دسترسی"]),
      ("شی‌گرایی", ["کلاس‌ها", "متدها", "وراثت", "چندریختی", "کپسوله‌سازی"]),
      ("فایل و ماژول", ["خواندن فایل", "نوشتن فایل", "ماژول‌ها", "try / except", "محیط مجازی"]),
    ]
  },
  {
    "slug": "html",
    "name_fa": "اچ‌تی‌ام‌ال",
    "name_en": "HTML",
    "icon": "📄",
    "desc": "HTML زبان نشانه‌گذاری استاندارد برای ساخت صفحات وب است. ساختار و محتوای هر صفحه وب با HTML تعریف می‌شود.",
    "features": [
      ("پایه وب", "بدون HTML هیچ صفحه وبی ساخته نمی‌شود."),
      ("ساده برای شروع", "یادگیری تگ‌های اصلی بسیار سریع است."),
      ("استاندارد جهانی", "توسط تمام مرورگرها پشتیبانی می‌شود."),
    ],
    "code": '<!DOCTYPE html>\n<html>\n<head>\n  <title>صفحه من</title>\n</head>\n<body>\n  <h1>سلام دنیا</h1>\n  <p>اولین صفحه من</p>\n</body>\n</html>',
    "path_hint": "ابتدا تگ‌های پایه، سپس فرم‌ها، جداول و المان‌های معنایی را یاد بگیرید. در ادامه با دسترسی‌پذیری و بهترین روش‌ها آشنا شوید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه HTML", "ویرایشگر", "عناصر پایه", "ویژگی‌ها", "عناوین"]),
      ("متن و محتوا", ["پاراگراف", "استایل‌ها", "فرمت‌بندی", "نقل‌قول", "توضیحات", "رنگ‌ها"]),
      ("لینک و تصویر", ["لینک‌ها", "تصاویر", "مسیر فایل", "تصویر به‌عنوان لینک"]),
      ("جداول و لیست", ["جداول", "لیست‌های مرتب", "لیست‌های نامرتب", "لیست تعریف"]),
      ("فرم‌ها", ["فرم", "ورودی‌ها", "دکمه‌ها", "لیست انتخاب", "اعتبارسنجی"]),
      ("چیدمان", ["بلاک و اینلاین", "کلاس و آی‌دی", "iframe", "layout"]),
      ("HTML5", ["عناصر معنایی", "ویدیو", "صدا", "canvas", "SVG"]),
      ("پیشرفته", ["دسترسی‌پذیری", "بهینه‌سازی SEO", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "css",
    "name_fa": "سی‌اس‌اس",
    "name_en": "CSS",
    "icon": "🎨",
    "desc": "CSS زبان استایل‌دهی صفحات وب است. با CSS ظاهر، چیدمان، رنگ‌ها و انیمیشن‌های صفحه را کنترل می‌کنید.",
    "features": [
      ("کنترل ظاهر", "طراحی کامل رابط کاربری با CSS امکان‌پذیر است."),
      ("جداسازی محتوا و ظاهر", "HTML ساختار و CSS ظاهر را مدیریت می‌کند."),
      ("انعطاف‌پذیر", "از موبایل تا دسکتاپ با یک استایل‌شیت."),
    ],
    "code": 'body {\n  background-color: #0f1419;\n  color: #e6edf3;\n  font-family: Vazirmatn, sans-serif;\n}\n\nh1 {\n  color: #58a6ff;\n  text-align: center;\n}',
    "path_hint": "ابتدا انتخاب‌گرها و ویژگی‌های پایه، سپس باکس‌مدل، فلکس و گرید را یاد بگیرید. در ادامه انیمیشن و طراحی واکنش‌گرا را تمرین کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه CSS", "نحوه اضافه کردن", "انتخاب‌گرها", "توضیحات"]),
      ("رنگ و پس‌زمینه", ["رنگ‌ها", "پس‌زمینه", "گرادیان", "شفافیت"]),
      ("متن و فونت", ["متن", "فونت", "آیکون‌ها", "لینک‌ها"]),
      ("باکس‌مدل", ["باکس‌مدل", "حاشیه", "پدینگ", "مارجین", "عرض و ارتفاع"]),
      ("چیدمان", ["Display", "Position", "Z-index", "Overflow", "Float"]),
      ("Flexbox و Grid", ["Flexbox", "Grid", "تراز کردن", "فاصله‌گذاری"]),
      ("واکنش‌گرا", ["Media Query", "واحدهای نسبی", "تصاویر واکنش‌گرا"]),
      ("افکت‌ها", ["Transition", "Animation", "Transform", "سایه"]),
    ]
  },
  {
    "slug": "javascript",
    "name_fa": "جاوااسکریپت",
    "name_en": "JavaScript",
    "icon": "⚡",
    "desc": "جاوااسکریپت زبان برنامه‌نویسی وب است که صفحات را پویا و تعاملی می‌کند. تقریباً در تمام مرورگرها اجرا می‌شود.",
    "features": [
      ("زبان وب", "تنها زبانی که به‌صورت بومی در مرورگر اجرا می‌شود."),
      ("پویا و تعاملی", "برای ساخت رابط‌های کاربری مدرن ضروری است."),
      ("اکوسیستم بزرگ", "فریم‌ورک‌هایی مانند React و Vue بر پایه آن ساخته شده‌اند."),
    ],
    "code": 'console.log("Hello World!");\n\nlet name = "Abdorreza";\ndocument.getElementById("demo").innerHTML = name;',
    "path_hint": "با متغیرها، شرط‌ها و توابع شروع کنید. سپس DOM، رویدادها و آسنکرون را یاد بگیرید و بعد سراغ فریم‌ورک‌ها بروید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه JS", "کجا بنویسیم", "خروجی", "دستورات"]),
      ("متغیرها و انواع", ["متغیرها", "انواع داده", "اعداد", "رشته‌ها", "آرایه‌ها", "اشیا"]),
      ("عملگرها و شرط", ["عملگرها", "if / else", "سوئیچ", "حلقه‌ها"]),
      ("توابع", ["توابع", "پارامترها", "فلش فانکشن", "کال‌بک"]),
      ("DOM", ["انتخاب عناصر", "تغییر محتوا", "رویدادها", "فرم‌ها"]),
      ("پیشرفته", ["آسنکرون", "Promise", "async/await", "Fetch API"]),
      ("مدرن", ["ماژول‌ها", "کلاس‌ها", "JSON", "LocalStorage"]),
      ("ابزارها", ["دیباگ", "بهترین روش‌ها", "ES6+"]),
    ]
  },
  {
    "slug": "sql",
    "name_fa": "اس‌کیو‌ال",
    "name_en": "SQL",
    "icon": "🗄️",
    "desc": "SQL زبان استاندارد برای کار با پایگاه‌های داده رابطه‌ای است. با آن داده را ذخیره، بازیابی و مدیریت می‌کنید.",
    "features": [
      ("استاندارد جهانی", "تقریباً تمام دیتابیس‌های رابطه‌ای از SQL پشتیبانی می‌کنند."),
      ("قدرتمند در کوئری", "برای گزارش‌گیری و تحلیل داده بسیار مناسب است."),
      ("پایه بک‌اند", "دانش SQL برای هر توسعه‌دهنده بک‌اند ضروری است."),
    ],
    "code": "SELECT * FROM Customers\nWHERE Country = 'Iran'\nORDER BY CustomerName;",
    "path_hint": "با SELECT و WHERE شروع کنید. سپس JOIN، گروه‌بندی و زیرکوئری‌ها را یاد بگیرید. در نهایت طراحی جدول و ایندکس را تمرین کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه SQL", "نحو", "SELECT", "WHERE"]),
      ("فیلتر و مرتب‌سازی", ["AND / OR", "NOT", "ORDER BY", "NULL", "LIMIT"]),
      ("توابع", ["MIN / MAX", "COUNT", "AVG", "SUM"]),
      ("گروه‌بندی", ["GROUP BY", "HAVING", "Alias"]),
      ("JOIN", ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "Self Join"]),
      ("تغییر داده", ["INSERT", "UPDATE", "DELETE", "TRUNCATE"]),
      ("ساختار", ["CREATE TABLE", "ALTER", "DROP", "Constraints", "Indexes"]),
      ("پیشرفته", ["View", "Stored Procedure", "Transaction", "Injection"]),
    ]
  },
  {
    "slug": "java",
    "name_fa": "جاوا",
    "name_en": "Java",
    "icon": "☕",
    "desc": "جاوا یک زبان شی‌گرا، قدرتمند و چندسکویی است که در برنامه‌های سازمانی، اندروید و سیستم‌های بزرگ کاربرد گسترده دارد.",
    "features": [
      ("یک‌بار بنویس، همه‌جا اجرا کن", "برنامه روی هر پلتفرمی که JVM دارد اجرا می‌شود."),
      ("شی‌گرایی قوی", "طراحی شی‌گرا یکی از نقاط قوت اصلی جاوا است."),
      ("اکوسیستم بزرگ", "کتابخانه‌ها و فریم‌ورک‌های بسیار متنوعی دارد."),
    ],
    "code": 'public class Main {\n  public static void main(String[] args) {\n    System.out.println("Hello World!");\n  }\n}',
    "path_hint": "با نحو پایه و متغیرها شروع کنید. سپس کلاس‌ها، وراثت و کالکشن‌ها را یاد بگیرید. در ادامه چندریسمانی و I/O را تمرین کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Java", "نصب", "نحو", "خروجی", "توضیحات"]),
      ("متغیرها", ["متغیرها", "انواع داده", "Type Casting", "عملگرها", "رشته‌ها"]),
      ("کنترل جریان", ["if / else", "سوئیچ", "حلقه while", "حلقه for", "break / continue"]),
      ("آرایه و متد", ["آرایه‌ها", "متدها", "پارامترها", "بازگشت", "Scope"]),
      ("شی‌گرایی", ["کلاس و شی", "سازنده", "وراثت", "چندریختی", "اینترفیس", "انتزاع"]),
      ("کالکشن", ["ArrayList", "LinkedList", "HashMap", "HashSet"]),
      ("پیشرفته", ["Exception", "فایل", "Threads", "Lambda", "Date"]),
      ("ابزارها", ["Package", "API", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "c",
    "name_fa": "سی",
    "name_en": "C",
    "icon": "⚙️",
    "desc": "زبان C یک زبان سطح متوسط و قدرتمند است که پایه بسیاری از زبان‌های مدرن محسوب می‌شود و در سیستم‌عامل و برنامه‌های سیستمی کاربرد دارد.",
    "features": [
      ("پایه زبان‌های مدرن", "C++، Java و بسیاری زبان‌ها از C الهام گرفته‌اند."),
      ("کنترل سخت‌افزار", "نزدیک به سخت‌افزار و مناسب برنامه‌نویسی سیستم است."),
      ("کارایی بالا", "کد تولیدشده بسیار بهینه و سریع است."),
    ],
    "code": '#include <stdio.h>\n\nint main() {\n  printf("Hello World!\\n");\n  return 0;\n}',
    "path_hint": "با نحو، متغیرها و اشاره‌گرها شروع کنید. سپس آرایه، ساختار و فایل را یاد بگیرید. در نهایت حافظه پویا و پیش‌پردازنده را تمرین کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه C", "نصب", "نحو", "خروجی", "توضیحات"]),
      ("متغیرها", ["متغیرها", "انواع داده", "ثابت‌ها", "عملگرها", "رشته‌ها"]),
      ("کنترل جریان", ["if", "سوئیچ", "حلقه‌ها", "break / continue", "goto"]),
      ("توابع و آرایه", ["توابع", "آرایه‌ها", "آرایه چندبعدی", "رشته‌ها"]),
      ("اشاره‌گر", ["اشاره‌گرها", "اشاره‌گر و آرایه", "اشاره‌گر و تابع"]),
      ("ساختار", ["struct", "union", "enum", "typedef"]),
      ("فایل و حافظه", ["فایل‌ها", "حافظه پویا", "پیش‌پردازنده"]),
      ("پیشرفته", ["خطاها", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "cpp",
    "name_fa": "سی‌پلاس‌پلاس",
    "name_en": "C++",
    "icon": "🔧",
    "desc": "C++ توسعه یافته C است و امکانات شی‌گرایی، قالب‌ها و کتابخانه استاندارد قدرتمند را اضافه کرده است. در بازی‌ها و سیستم‌های با کارایی بالا استفاده می‌شود.",
    "features": [
      ("کارایی و کنترل", "مناسب بازی، موتورهای گرافیکی و سیستم‌های real-time."),
      ("شی‌گرایی", "کلاس، وراثت و چندریختی کامل دارد."),
      ("کتابخانه غنی", "STL مجموعه‌ای قدرتمند از ساختارهای داده و الگوریتم است."),
    ],
    "code": '#include <iostream>\nusing namespace std;\n\nint main() {\n  cout << "Hello World!" << endl;\n  return 0;\n}',
    "path_hint": "ابتدا نحو و مفاهیم C را مرور کنید. سپس کلاس‌ها، قالب‌ها و STL را یاد بگیرید. در ادامه مدیریت حافظه و الگوهای طراحی را تمرین کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه C++", "نصب", "نحو", "خروجی", "توضیحات"]),
      ("پایه", ["متغیرها", "انواع داده", "عملگرها", "رشته‌ها", "شرط و حلقه"]),
      ("توابع و آرایه", ["توابع", "آرایه‌ها", "اشاره‌گرها", "ارجاع"]),
      ("شی‌گرایی", ["کلاس", "سازنده و مخرب", "وراثت", "چندریختی", "انتزاع"]),
      ("پیشرفته", ["قالب‌ها", "Exception", "فایل", "فضای نام"]),
      ("STL", ["vector", "map", "set", "algorithm"]),
      ("مدرن", ["C++11/14/17", "smart pointer", "lambda"]),
      ("بهترین روش‌ها", ["مدیریت حافظه", "الگوهای طراحی"]),
    ]
  },
  {
    "slug": "csharp",
    "name_fa": "سی‌شارپ",
    "name_en": "C#",
    "icon": "💠",
    "desc": "C# زبان مدرن مایکروسافت است که روی پلتفرم .NET اجرا می‌شود و برای ساخت برنامه‌های ویندوز، وب و بازی (با Unity) کاربرد دارد.",
    "features": [
      ("مدرن و ایمن", "تایپ قوی و مدیریت حافظه خودکار دارد."),
      ("اکوسیستم .NET", "ابزارها و کتابخانه‌های قدرتمند مایکروسافت."),
      ("چندمنظوره", "از دسکتاپ تا وب و موبایل و بازی."),
    ],
    "code": 'using System;\n\nclass Program {\n  static void Main() {\n    Console.WriteLine("Hello World!");\n  }\n}',
    "path_hint": "با نحو و انواع داده شروع کنید. سپس کلاس‌ها، LINQ و async را یاد بگیرید. در ادامه ASP.NET یا Unity را انتخاب کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه C#", "نصب", "نحو", "خروجی"]),
      ("پایه", ["متغیرها", "انواع داده", "عملگرها", "رشته‌ها", "شرط و حلقه"]),
      ("متد و آرایه", ["متدها", "آرایه‌ها", "لیست‌ها"]),
      ("شی‌گرایی", ["کلاس", "وراثت", "اینترفیس", "انتزاع", "Properties"]),
      ("پیشرفته", ["Exception", "فایل", "Generic", "Delegate"]),
      ("مدرن", ["LINQ", "async / await", "Lambda", "Nullable"]),
      ("فریم‌ورک", ["ASP.NET", "Entity Framework", "WPF"]),
      ("ابزارها", ["Visual Studio", "NuGet", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "php",
    "name_fa": "پی‌اچ‌پی",
    "name_en": "PHP",
    "icon": "🐘",
    "desc": "PHP یک زبان سمت سرور است که به‌طور گسترده برای ساخت وب‌سایت‌های پویا و سیستم‌های مدیریت محتوا استفاده می‌شود.",
    "features": [
      ("محبوب در وب", "بسیاری از سایت‌های بزرگ با PHP نوشته شده‌اند."),
      ("یادگیری نسبتاً آسان", "برای شروع توسعه وب سرور مناسب است."),
      ("اکوسیستم CMS", "وردپرس، لاراول و بسیاری فریم‌ورک‌ها بر پایه آن هستند."),
    ],
    "code": '<?php\necho "Hello World!";\n\n$name = "Abdorreza";\necho $name;\n?>',
    "path_hint": "با نحو و متغیرها شروع کنید. سپس فرم‌ها، کار با دیتابیس و سشن را یاد بگیرید. در ادامه فریم‌ورک لاراول را بررسی کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه PHP", "نصب", "نحو", "خروجی"]),
      ("پایه", ["متغیرها", "انواع داده", "عملگرها", "رشته‌ها", "آرایه‌ها"]),
      ("کنترل جریان", ["if", "سوئیچ", "حلقه‌ها", "توابع"]),
      ("فرم و داده", ["فرم‌ها", "GET / POST", "اعتبارسنجی", "آپلود فایل"]),
      ("دیتابیس", ["MySQL", "اتصال", "CRUD", "Prepared Statement"]),
      ("سشن و کوکی", ["Session", "Cookie", "امنیت"]),
      ("شی‌گرایی", ["کلاس", "وراثت", "Namespace"]),
      ("پیشرفته", ["فایل", "JSON", "API", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "typescript",
    "name_fa": "تایپ‌اسکریپت",
    "name_en": "TypeScript",
    "icon": "📘",
    "desc": "TypeScript نسخه تایپ‌دار جاوااسکریپت است که توسط مایکروسافت توسعه یافته و کد را ایمن‌تر و قابل‌نگهداری‌تر می‌کند.",
    "features": [
      ("تایپ استاتیک", "خطاها را قبل از اجرا پیدا می‌کند."),
      ("سازگار با JS", "هر کد جاوااسکریپت در TypeScript معتبر است."),
      ("ابزار عالی", "پشتیبانی عالی در VS Code و فریم‌ورک‌ها."),
    ],
    "code": 'let message: string = "Hello World!";\nconsole.log(message);\n\nfunction greet(name: string): string {\n  return `سلام ${name}`;\n}',
    "path_hint": "ابتدا جاوااسکریپت را خوب یاد بگیرید. سپس انواع، اینترفیس و جنریک را تمرین کنید و در پروژه‌های React یا Node به‌کار ببرید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه TS", "نصب", "کامپایلر", "تنظیمات"]),
      ("انواع", ["انواع پایه", "آرایه و تاپل", "Enum", "Any / Unknown", "Union"]),
      ("توابع", ["توابع", "پارامتر اختیاری", "Rest", "Overload"]),
      ("شی و اینترفیس", ["Interface", "Type Alias", "Optional", "Readonly"]),
      ("کلاس", ["کلاس", "Access Modifier", "وراثت", "Abstract"]),
      ("جنریک", ["Generic", "Constraints", "Utility Types"]),
      ("پیشرفته", ["Module", "Namespace", "Declaration", "Strict Mode"]),
      ("ابزارها", ["tsconfig", "با React", "با Node"]),
    ]
  },
  {
    "slug": "go",
    "name_fa": "گو",
    "name_en": "Go",
    "icon": "🐹",
    "desc": "Go (Golang) زبان مدرن گوگل است که برای ساخت سرویس‌های مقیاس‌پذیر، همزمانی بالا و ابزارهای سیستمی طراحی شده است.",
    "features": [
      ("ساده و سریع", "نحو ساده و زمان کامپایل بسیار کوتاه."),
      ("همزمانی عالی", "goroutine و channel قدرت بالایی در concurrency دارند."),
      ("مناسب بک‌اند", "برای میکروسرویس و API بسیار محبوب است."),
    ],
    "code": 'package main\n\nimport "fmt"\n\nfunc main() {\n  fmt.Println("Hello World!")\n}',
    "path_hint": "با نحو و پکیج‌ها شروع کنید. سپس slice، map و struct را یاد بگیرید. در ادامه concurrency و ساخت API را تمرین کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Go", "نصب", "نحو", "پکیج‌ها"]),
      ("پایه", ["متغیرها", "انواع", "ثابت‌ها", "عملگرها", "رشته‌ها"]),
      ("کنترل جریان", ["if", "سوئیچ", "حلقه for", "defer"]),
      ("توابع", ["توابع", "چند مقدار بازگشتی", "متد", "بستار"]),
      ("ساختار داده", ["آرایه", "Slice", "Map", "Struct"]),
      ("اشاره‌گر و اینترفیس", ["Pointer", "Interface", "Method"]),
      ("همزمانی", ["Goroutine", "Channel", "Select", "Mutex"]),
      ("پیشرفته", ["Error", "فایل", "تست", "ماژول"]),
    ]
  },
  {
    "slug": "kotlin",
    "name_fa": "کاتلین",
    "name_en": "Kotlin",
    "icon": "🟣",
    "desc": "Kotlin زبان مدرن جت‌برینز است که به‌طور رسمی برای اندروید پشتیبانی می‌شود و با جاوا کاملاً سازگار است.",
    "features": [
      ("رسمی اندروید", "زبان پیشنهادی گوگل برای توسعه اندروید."),
      ("مدرن و ایمن", "Null-safety و نحو مختصر."),
      ("سازگار با Java", "می‌تواند در کنار کد جاوا استفاده شود."),
    ],
    "code": 'fun main() {\n  println("Hello World!")\n\n  val name = "Abdorreza"\n  println(name)\n}',
    "path_hint": "با نحو پایه و null-safety شروع کنید. سپس کلاس‌ها و کوروتین را یاد بگیرید و یک اپ اندروید ساده بسازید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Kotlin", "نصب", "نحو", "خروجی"]),
      ("پایه", ["متغیرها", "انواع", "Null Safety", "عملگرها", "رشته‌ها"]),
      ("کنترل جریان", ["if", "when", "حلقه‌ها", "Range"]),
      ("توابع", ["توابع", "Default Argument", "Lambda", "Extension"]),
      ("کلاس", ["کلاس", "Data Class", "Object", "وراثت", "Interface"]),
      ("کالکشن", ["List", "Set", "Map", "Sequence"]),
      ("پیشرفته", ["Coroutine", "Flow", "Generic", "Delegation"]),
      ("اندروید", ["Activity", "ViewModel", "Jetpack Compose"]),
    ]
  },
  {
    "slug": "rust",
    "name_fa": "راست",
    "name_en": "Rust",
    "icon": "🦀",
    "desc": "Rust زبان مدرن با تمرکز روی ایمنی حافظه و کارایی است که بدون garbage collector کار می‌کند و در سیستم‌های حساس استفاده می‌شود.",
    "features": [
      ("ایمنی حافظه", "بدون GC و بدون خطای segmentation fault."),
      ("کارایی بالا", "رقابت با C و C++ در سرعت."),
      ("ابزار عالی", "Cargo و سیستم پکیج بسیار قوی."),
    ],
    "code": 'fn main() {\n  println!("Hello World!");\n\n  let name = "Abdorreza";\n  println!("{}", name);\n}',
    "path_hint": "با ownership و borrowing شروع کنید. سپس struct، enum و trait را یاد بگیرید. در ادامه async و unsafe را با احتیاط تمرین کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Rust", "نصب", "Cargo", "نحو"]),
      ("پایه", ["متغیرها", "انواع", "Ownership", "Borrowing", "Slice"]),
      ("کنترل جریان", ["if", "match", "حلقه‌ها", "Pattern"]),
      ("ساختار", ["Struct", "Enum", "Method", "Trait"]),
      ("کالکشن", ["Vector", "String", "HashMap"]),
      ("خطا", ["Result", "Option", "panic!", "Error Handling"]),
      ("پیشرفته", ["Lifetime", "Closure", "Iterator", "Smart Pointer"]),
      ("عملی", ["ماژول", "فایل", "تست", "Async"]),
    ]
  },
  {
    "slug": "r",
    "name_fa": "آر",
    "name_en": "R",
    "icon": "📊",
    "desc": "R زبان تخصصی آمار و تحلیل داده است که در پژوهش‌های علمی، یادگیری ماشین و مصورسازی داده کاربرد فراوان دارد.",
    "features": [
      ("قدرتمند در آمار", "توابع آماری بسیار غنی و آماده."),
      ("مصورسازی عالی", "ggplot2 یکی از بهترین ابزارهای visualization است."),
      ("جامعه علمی", "استاندارد در بسیاری از حوزه‌های تحقیقاتی."),
    ],
    "code": 'print("Hello World!")\n\nname <- "Abdorreza"\nprint(name)\n\n# محاسبه میانگین\nmean(c(1, 2, 3, 4, 5))',
    "path_hint": "با ساختار داده و فریم‌دیتا شروع کنید. سپس dplyr و ggplot2 را یاد بگیرید و پروژه‌های تحلیل داده انجام دهید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه R", "نصب", "RStudio", "نحو"]),
      ("پایه", ["متغیرها", "بردار", "ماتریس", "لیست", "دیتا فریم"]),
      ("عملیات", ["عملگرها", "شرط", "حلقه", "توابع"]),
      ("داده", ["خواندن فایل", "dplyr", "tidyr", "پاکسازی"]),
      ("آمار", ["خلاصه آماری", "توزیع", "آزمون فرض", "رگرسیون"]),
      ("مصورسازی", ["plot پایه", "ggplot2", "نمودارهای آماری"]),
      ("پیشرفته", ["مدل‌سازی", "Machine Learning", "Shiny"]),
      ("ابزارها", ["پکیج‌ها", "R Markdown", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "ruby",
    "name_fa": "روبی",
    "name_en": "Ruby",
    "icon": "💎",
    "desc": "Ruby زبانی ساده و زیبا با تمرکز روی شادی برنامه‌نویس است. فریم‌ورک Ruby on Rails آن را در توسعه وب بسیار محبوب کرده است.",
    "features": [
      ("نحو زیبا", "کد خوانا و نزدیک به زبان طبیعی."),
      ("Rails", "یکی از بهترین فریم‌ورک‌های وب سریع‌توسعه."),
      ("شی‌گرایی خالص", "همه‌چیز شی است."),
    ],
    "code": 'puts "Hello World!"\n\nname = "Abdorreza"\nputs name',
    "path_hint": "با نحو و شی‌گرایی شروع کنید. سپس بلوک‌ها و ماژول را یاد بگیرید و یک پروژه ساده با Rails بسازید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Ruby", "نصب", "نحو", "خروجی"]),
      ("پایه", ["متغیرها", "انواع", "عملگرها", "رشته‌ها", "آرایه و هش"]),
      ("کنترل جریان", ["if", "case", "حلقه‌ها", "Iterator"]),
      ("متد و بلوک", ["متدها", "بلوک", "Proc", "Lambda", "Yield"]),
      ("شی‌گرایی", ["کلاس", "وراثت", "ماژول", "Mixin"]),
      ("پیشرفته", ["Exception", "فایل", "Symbol", "Meta-programming"]),
      ("Rails", ["MVC", "Routing", "ActiveRecord", "Views"]),
      ("ابزارها", ["Gem", "Bundler", "تست", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "swift",
    "name_fa": "سوییفت",
    "name_en": "Swift",
    "icon": "🐦",
    "desc": "Swift زبان رسمی اپل برای ساخت اپلیکیشن‌های iOS، macOS و سایر پلتفرم‌های اپل است. مدرن، ایمن و سریع طراحی شده است.",
    "features": [
      ("رسمی اپل", "زبان اصلی توسعه برای اکوسیستم اپل."),
      ("ایمن و مدرن", "Optionals و type safety قوی."),
      ("کارایی بالا", "رقابت با زبان‌های کامپایل‌شده."),
    ],
    "code": 'print("Hello World!")\n\nlet name = "Abdorreza"\nprint(name)',
    "path_hint": "با نحو و Optionals شروع کنید. سپس struct، class و پروتکل را یاد بگیرید و یک اپ ساده با SwiftUI بسازید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Swift", "Xcode", "نحو", "Playground"]),
      ("پایه", ["ثابت و متغیر", "انواع", "Optional", "عملگرها", "رشته‌ها"]),
      ("کنترل جریان", ["if", "guard", "سوئیچ", "حلقه‌ها"]),
      ("توابع", ["توابع", "Closure", "Higher-order"]),
      ("ساختار", ["Struct", "Class", "Enum", "Protocol"]),
      ("پیشرفته", ["Generic", "Error Handling", "Extension", "Memory"]),
      ("UI", ["UIKit", "SwiftUI", "Combine"]),
      ("ابزارها", ["SPM", "تست", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "dart",
    "name_fa": "دارت",
    "name_en": "Dart",
    "icon": "🎯",
    "desc": "Dart زبان گوگل است که به‌ویژه با فریم‌ورک Flutter برای ساخت اپلیکیشن‌های چندسکویی (موبایل، وب، دسکتاپ) استفاده می‌شود.",
    "features": [
      ("Flutter", "ابزار اصلی ساخت UI زیبا و سریع چندسکویی."),
      ("یک زبان برای همه", "موبایل، وب و دسکتاپ با یک کدبیس."),
      ("مدرن", "نحو تمیز و پشتیبانی خوب از async."),
    ],
    "code": 'void main() {\n  print("Hello World!");\n\n  var name = "Abdorreza";\n  print(name);\n}',
    "path_hint": "با نحو دارت شروع کنید. سپس widgetها و state management در Flutter را یاد بگیرید و یک اپ ساده بسازید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Dart", "نصب", "نحو", "خروجی"]),
      ("پایه", ["متغیرها", "انواع", "Null Safety", "عملگرها", "رشته‌ها"]),
      ("کنترل جریان", ["if", "سوئیچ", "حلقه‌ها", "Exception"]),
      ("توابع", ["توابع", "پارامترها", "Arrow", "Async"]),
      ("کلاس", ["کلاس", "Constructor", "وراثت", "Mixin", "Abstract"]),
      ("کالکشن", ["List", "Set", "Map", "Iterable"]),
      ("Flutter", ["Widget", "State", "Layout", "Navigation"]),
      ("پیشرفته", ["Stream", "Isolate", "Package", "تست"]),
    ]
  },
  {
    "slug": "nodejs",
    "name_fa": "نود‌جی‌اس",
    "name_en": "Node.js",
    "icon": "🟢",
    "desc": "Node.js محیط اجرای جاوااسکریپت در سمت سرور است که امکان ساخت سرورهای مقیاس‌پذیر و API را فراهم می‌کند.",
    "features": [
      ("جاوااسکریپت در سرور", "یک زبان برای فرانت و بک."),
      ("غیرمسدودکننده", "مدل event-driven مناسب I/O بالا."),
      ("اکوسیستم npm", "بزرگ‌ترین مخزن پکیج جهان."),
    ],
    "code": 'const http = require("http");\n\nconst server = http.createServer((req, res) => {\n  res.end("Hello World!");\n});\n\nserver.listen(3000);',
    "path_hint": "ابتدا جاوااسکریپت را مسلط شوید. سپس ماژول‌ها، Express و کار با دیتابیس را یاد بگیرید و یک API بسازید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Node", "نصب", "REPL", "ماژول‌ها"]),
      ("پایه", ["require / import", "fs", "path", "os", "events"]),
      ("HTTP", ["http module", "Request / Response", "Routing ساده"]),
      ("Express", ["نصب Express", "Route", "Middleware", "Template"]),
      ("داده", ["فایل", "MongoDB", "MySQL", "ORM"]),
      ("آسنکرون", ["Callback", "Promise", "async/await", "Stream"]),
      ("پیشرفته", ["Authentication", "REST API", "WebSocket", "Cluster"]),
      ("ابزارها", ["npm", "nodemon", "تست", "Deploy"]),
    ]
  },
  {
    "slug": "react",
    "name_fa": "ری‌اکت",
    "name_en": "React",
    "icon": "⚛️",
    "desc": "React کتابخانه جاوااسکریپت برای ساخت رابط کاربری است که توسط فیسبوک توسعه یافته و بر اساس کامپوننت کار می‌کند.",
    "features": [
      ("کامپوننت‌محور", "UI را به قطعات قابل‌استفاده مجدد تقسیم می‌کند."),
      ("اکوسیستم بزرگ", "ابزارها و جامعه بسیار فعال."),
      ("اعلامی", "وضعیت UI را به‌صورت declarative تعریف می‌کنید."),
    ],
    "code": 'function App() {\n  return (\n    <div>\n      <h1>Hello World!</h1>\n    </div>\n  );\n}\n\nexport default App;',
    "path_hint": "ابتدا جاوااسکریپت و JSX را یاد بگیرید. سپس state، props و hooks را مسلط شوید و یک پروژه کوچک بسازید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه React", "نصب", "JSX", "کامپوننت"]),
      ("پایه", ["Props", "State", "Event", "Conditional Render"]),
      ("لیست و فرم", ["Lists", "Keys", "Forms", "Controlled Component"]),
      ("Hooks", ["useState", "useEffect", "useContext", "useRef", "Custom Hook"]),
      ("پیشرفته", ["Context", "Reducer", "Memo", "Callback"]),
      ("مسیریابی", ["React Router", "Nested Routes", "Navigation"]),
      ("داده", ["Fetch", "Axios", "React Query"]),
      ("ابزارها", ["Vite", "Testing", "Deploy", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "jquery",
    "name_fa": "جی‌کوئری",
    "name_en": "jQuery",
    "icon": "💙",
    "desc": "jQuery کتابخانه سبک جاوااسکریپت است که کار با DOM، رویدادها و AJAX را بسیار ساده می‌کند.",
    "features": [
      ("ساده‌سازی DOM", "انتخاب و تغییر عناصر با نحو کوتاه."),
      ("سازگاری مرورگر", "مشکلات قدیمی مرورگرها را حل می‌کند."),
      ("هنوز کاربردی", "در بسیاری از پروژه‌های موجود استفاده می‌شود."),
    ],
    "code": '$(document).ready(function() {\n  $("h1").text("Hello World!");\n  $("#btn").click(function() {\n    alert("کلیک شد!");\n  });\n});',
    "path_hint": "با انتخاب‌گرها و متدهای DOM شروع کنید. سپس رویدادها و AJAX را یاد بگیرید. در پروژه‌های جدید ترجیحاً جاوااسکریپت خالص یا فریم‌ورک مدرن استفاده کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه jQuery", "نصب", "نحو", "Document Ready"]),
      ("انتخاب‌گر", ["انتخاب‌گرها", "فیلترها", "Traversal"]),
      ("DOM", ["دریافت و تنظیم", "افزودن و حذف", "کلاس و CSS"]),
      ("رویداد", ["رویدادها", "Mouse", "Keyboard", "Form"]),
      ("افکت", ["Hide / Show", "Fade", "Slide", "Animate"]),
      ("AJAX", ["load", "get / post", "ajax", "JSON"]),
      ("پلاگین", ["ساخت پلاگین", "پلاگین‌های محبوب"]),
      ("نکات", ["بهترین روش‌ها", "مهاجرت به JS مدرن"]),
    ]
  },
  {
    "slug": "bootstrap",
    "name_fa": "بوت‌استرپ",
    "name_en": "Bootstrap",
    "icon": "🅱️",
    "desc": "Bootstrap محبوب‌ترین فریم‌ورک CSS برای ساخت رابط‌های واکنش‌گرا و مدرن با سرعت بالا است.",
    "features": [
      ("سریع‌توسعه", "کامپوننت‌های آماده برای اکثر نیازهای UI."),
      ("واکنش‌گرا", "از موبایل تا دسکتاپ به‌صورت پیش‌فرض."),
      ("سفارشی‌سازی", "با متغیرهای SASS قابل تنظیم است."),
    ],
    "code": '<div class="container">\n  <div class="row">\n    <div class="col-md-6">\n      <h1 class="text-primary">سلام دنیا</h1>\n      <button class="btn btn-success">کلیک کنید</button>\n    </div>\n  </div>\n</div>',
    "path_hint": "با سیستم گرید و utility classها شروع کنید. سپس کامپوننت‌ها را تمرین کنید و در نهایت با SASS سفارشی‌سازی کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Bootstrap", "نصب", "Container", "Grid"]),
      ("تایپوگرافی", ["عنوان‌ها", "متن", "رنگ‌ها", "فاصله‌ها"]),
      ("کامپوننت", ["دکمه", "کارت", "ناوبری", "مودال", "فرم"]),
      ("Utility", ["Display", "Flex", "Spacing", "Position"]),
      ("واکنش‌گرا", ["Breakpoint", "Display responsive", " تصاویر"]),
      ("پیشرفته", ["SASS", "Customize", "Icons", "RTL"]),
      ("جاوااسکریپت", ["Collapse", "Carousel", "Tooltip", "Toast"]),
      ("بهترین روش‌ها", ["دسترسی‌پذیری", "عملکرد", "تم"]),
    ]
  },
  {
    "slug": "mysql",
    "name_fa": "مای‌اس‌کیوال",
    "name_en": "MySQL",
    "icon": "🐬",
    "desc": "MySQL یکی از محبوب‌ترین سیستم‌های مدیریت پایگاه‌داده رابطه‌ای متن‌باز است که در بسیاری از وب‌سایت‌ها استفاده می‌شود.",
    "features": [
      ("رایگان و قدرتمند", "متن‌باز با عملکرد بالا."),
      ("استاندارد وب", "ترکیب کلاسیک با PHP و لینوکس."),
      ("ابزارهای خوب", "phpMyAdmin و MySQL Workbench."),
    ],
    "code": "CREATE DATABASE shop;\nUSE shop;\n\nCREATE TABLE products (\n  id INT PRIMARY KEY AUTO_INCREMENT,\n  name VARCHAR(100),\n  price DECIMAL(10,2)\n);",
    "path_hint": "با SQL پایه شروع کنید. سپس طراحی جدول، ایندکس و بهینه‌سازی کوئری را یاد بگیرید و با زبان‌های سمت سرور ترکیب کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه MySQL", "نصب", "اتصال", "دیتابیس"]),
      ("جداول", ["CREATE TABLE", "انواع داده", "Constraints", "ALTER", "DROP"]),
      ("داده", ["INSERT", "SELECT", "UPDATE", "DELETE"]),
      ("کوئری پیشرفته", ["JOIN", "Subquery", "View", "Index"]),
      ("توابع", ["توابع رشته", "عددی", "تاریخ", "تجمیعی"]),
      ("امنیت", ["کاربر و دسترسی", "Injection", "Backup"]),
      ("اداره", ["Transaction", "Stored Procedure", "Trigger"]),
      ("ابزارها", ["WorkBench", "phpMyAdmin", "بهینه‌سازی"]),
    ]
  },
  {
    "slug": "mongodb",
    "name_fa": "مونگو‌دی‌بی",
    "name_en": "MongoDB",
    "icon": "🍃",
    "desc": "MongoDB یک پایگاه‌داده NoSQL سندگرا است که داده را به‌صورت JSON-مانند (BSON) ذخیره می‌کند و برای داده‌های انعطاف‌پذیر مناسب است.",
    "features": [
      ("انعطاف در اسکما", "بدون نیاز به ساختار ثابت جدول."),
      ("مقیاس‌پذیری افقی", "مناسب داده‌های بزرگ و توزیع‌شده."),
      ("محبوب با Node", "ترکیب عالی با جاوااسکریپت و Express."),
    ],
    "code": 'db.users.insertOne({\n  name: "Abdorreza",\n  age: 25,\n  skills: ["Python", "JavaScript"]\n})\n\ndb.users.find({ age: { $gt: 20 } })',
    "path_hint": "با مفهوم document و collection شروع کنید. سپس CRUD، aggregation و ایندکس را یاد بگیرید و با Mongoose در Node استفاده کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه MongoDB", "نصب", "Shell", "Database"]),
      ("سند و کالکشن", ["Document", "Collection", "Schema Design"]),
      ("CRUD", ["insert", "find", "update", "delete"]),
      ("کوئری", ["فیلتر", "Projection", "Sort", "Limit", "Operator"]),
      ("Aggregation", ["Pipeline", "Group", "Match", "Lookup"]),
      ("ایندکس", ["Index", "Text Search", "Geospatial"]),
      ("پیشرفته", ["Replication", "Sharding", "Transaction"]),
      ("ابزارها", ["Compass", "Mongoose", "Atlas"]),
    ]
  },
  {
    "slug": "git",
    "name_fa": "گیت",
    "name_en": "Git",
    "icon": "📦",
    "desc": "Git سیستم کنترل نسخه توزیع‌شده است که برای ردیابی تغییرات کد و همکاری تیمی ضروری است.",
    "features": [
      ("استاندارد صنعت", "تقریباً تمام پروژه‌های نرم‌افزاری از Git استفاده می‌کنند."),
      ("توزیع‌شده", "هر توسعه‌دهنده کپی کامل تاریخچه را دارد."),
      ("GitHub / GitLab", "پلتفرم‌های همکاری قدرتمند."),
    ],
    "code": 'git init\ngit add .\ngit commit -m "اولین کامیت"\ngit remote add origin <url>\ngit push -u origin main',
    "path_hint": "با مفاهیم پایه commit و branch شروع کنید. سپس merge، rebase و کار با remote را یاد بگیرید و در GitHub تمرین کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Git", "نصب", "پیکربندی", "مفاهیم"]),
      ("پایه", ["init", "add", "commit", "status", "log"]),
      ("شاخه", ["branch", "checkout", "merge", "rebase"]),
      ("ریموت", ["remote", "push", "pull", "clone", "fetch"]),
      ("لغو تغییرات", ["restore", "reset", "revert", "stash"]),
      ("همکاری", ["Pull Request", "Conflict", "Code Review"]),
      ("پیشرفته", ["tag", "hook", "submodule", "bisect"]),
      ("پلتفرم", ["GitHub", "GitLab", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "json",
    "name_fa": "جی‌سان",
    "name_en": "JSON",
    "icon": "📋",
    "desc": "JSON فرمت سبک تبادل داده است که به‌طور گسترده در APIها و ذخیره تنظیمات استفاده می‌شود.",
    "features": [
      ("سبک و خوانا", "متن ساده و قابل‌فهم برای انسان و ماشین."),
      ("استاندارد وب", "تقریباً تمام APIهای مدرن از JSON استفاده می‌کنند."),
      ("پشتیبانی گسترده", "در تمام زبان‌های برنامه‌نویسی پشتیبانی می‌شود."),
    ],
    "code": '{\n  "name": "Abdorreza",\n  "age": 25,\n  "skills": ["Python", "HTML", "CSS"],\n  "active": true\n}',
    "path_hint": "ساختار JSON را یاد بگیرید. سپس پارس و ساخت آن را در زبان مورد علاقه‌تان تمرین کنید و با REST API کار کنید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه JSON", "نحو", "انواع داده"]),
      ("ساختار", ["Object", "Array", "تودرتو", "قوانین"]),
      ("در جاوااسکریپت", ["parse", "stringify", "دسترسی"]),
      ("در پایتون", ["json module", "load / dump", "dict"]),
      ("API", ["REST و JSON", "Header", "Status Code"]),
      ("اعتبارسنجی", ["Schema", "ابزارهای آنلاین"]),
      ("مقایسه", ["JSON vs XML", "JSON vs YAML"]),
      ("بهترین روش‌ها", ["نام‌گذاری", "حجم", "امنیت"]),
    ]
  },
  {
    "slug": "xml",
    "name_fa": "ایکس‌ام‌ال",
    "name_en": "XML",
    "icon": "📰",
    "desc": "XML زبان نشانه‌گذاری قابل‌گسترش برای ذخیره و انتقال داده ساخت‌یافته است که هنوز در بسیاری از سیستم‌های سازمانی استفاده می‌شود.",
    "features": [
      ("ساخت‌یافته", "داده را با تگ‌های معنادار سازمان می‌دهد."),
      ("استاندارد قدیمی", "در بسیاری از پروتکل‌ها و فایل‌های پیکربندی."),
      ("قابل‌گسترش", "می‌توانید تگ‌های خود را تعریف کنید."),
    ],
    "code": '<?xml version="1.0" encoding="UTF-8"?>\n<note>\n  <to>کاربر</to>\n  <from>سیستم</from>\n  <message>سلام دنیا</message>\n</note>',
    "path_hint": "با نحو و قوانین XML شروع کنید. سپس DTD/Schema، XPath و استفاده در زبان‌های برنامه‌نویسی را یاد بگیرید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه XML", "نحو", "درخت سند"]),
      ("قوانین", ["تگ‌ها", "ویژگی‌ها", "تودرتو", "اعتبارسنجی"]),
      ("DTD و Schema", ["DTD", "XSD", "Namespace"]),
      ("دسترسی", ["DOM", "SAX", "XPath", "XQuery"]),
      ("تبدیل", ["XSLT", "تبدیل به HTML"]),
      ("در زبان‌ها", ["با JS", "با Python", "با Java"]),
      ("کاربرد", ["پیکربندی", "SOAP", "RSS / Atom"]),
      ("مقایسه", ["XML vs JSON", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "bash",
    "name_fa": "بش",
    "name_en": "Bash",
    "icon": "💻",
    "desc": "Bash زبان شل استاندارد لینوکس و یونیکس است که برای اتوماسیون، مدیریت سیستم و اسکریپت‌نویسی استفاده می‌شود.",
    "features": [
      ("ابزار سیستم", "برای مدیریت سرور و اتوماسیون ضروری است."),
      ("قدرتمند در پایپ‌لاین", "ترکیب دستورات با pipe بسیار قوی است."),
      ("همه‌جا موجود", "روی تقریباً تمام سیستم‌های یونیکس/لینوکس."),
    ],
    "code": '#!/bin/bash\necho "Hello World!"\n\nNAME="Abdorreza"\necho "سلام $NAME"',
    "path_hint": "با دستورات پایه و متغیرها شروع کنید. سپس شرط، حلقه و پایپ‌لاین را یاد بگیرید و اسکریپت‌های کاربردی بنویسید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Bash", "ترمینال", "دستورات پایه"]),
      ("فایل و مسیر", ["cd / ls / pwd", "mkdir / rm", "cp / mv", "مجوزها"]),
      ("متغیر و ورودی", ["متغیرها", "آرگومان", "خواندن ورودی", "محیط"]),
      ("کنترل جریان", ["if", "case", "حلقه for", "while", "until"]),
      ("متن", ["echo / printf", "grep", "sed", "awk"]),
      ("پایپ و هدایت", ["Pipe", "Redirect", "خروجی و خطا"]),
      ("توابع و اسکریپت", ["توابع", "exit code", "set options"]),
      ("عملی", ["Cron", "اتوماسیون", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "perl",
    "name_fa": "پرل",
    "name_en": "Perl",
    "icon": "🐪",
    "desc": "Perl زبان قدرتمند پردازش متن و اسکریپت‌نویسی است که در مدیریت سیستم، بیوانفورماتیک و وب قدیمی کاربرد داشته است.",
    "features": [
      ("پردازش متن قوی", "عبارت منظم در قلب زبان قرار دارد."),
      ("انعطاف‌پذیر", "چندین راه برای انجام یک کار دارد."),
      ("میراث غنی", "در بسیاری از ابزارهای قدیمی و علمی هنوز استفاده می‌شود."),
    ],
    "code": '#!/usr/bin/perl\nuse strict;\nuse warnings;\n\nprint "Hello World!\\n";\n\nmy $name = "Abdorreza";\nprint "$name\\n";',
    "path_hint": "با نحو و متغیرهای اسکالر شروع کنید. سپس آرایه، هش و regex را مسلط شوید و اسکریپت‌های پردازش متن بنویسید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Perl", "نصب", "نحو", "strict"]),
      ("متغیرها", ["Scalar", "Array", "Hash", "Reference"]),
      ("عملگر و شرط", ["عملگرها", "if", "unless", "حلقه‌ها"]),
      ("رشته و regex", ["رشته‌ها", "Regex", "Substitution", "Split / Join"]),
      ("توابع", ["سابروتین", "پارامترها", "بازگشت", "ماژول"]),
      ("فایل و I/O", ["باز کردن فایل", "خواندن", "نوشتن", "Directory"]),
      ("پیشرفته", ["OOP", "CPAN", "CGI", "DBI"]),
      ("عملی", ["اسکریپت سیستم", "پردازش لاگ", "بهترین روش‌ها"]),
    ]
  },
  {
    "slug": "scala",
    "name_fa": "اسکالا",
    "name_en": "Scala",
    "icon": "🔴",
    "desc": "Scala زبان مدرن روی JVM است که برنامه‌نویسی شی‌گرا و تابعی را ترکیب می‌کند و در داده‌های بزرگ (Spark) محبوب است.",
    "features": [
      ("ترکیب OOP و FP", "بهترین هر دو پارادایم را ارائه می‌دهد."),
      ("روی JVM", "سازگار با اکوسیستم جاوا."),
      ("داده بزرگ", "زبان اصلی Apache Spark."),
    ],
    "code": 'object Main {\n  def main(args: Array[String]): Unit = {\n    println("Hello World!")\n  }\n}',
    "path_hint": "با نحو و تفاوت‌هایش با جاوا شروع کنید. سپس مجموعه توابع، pattern matching و اکوسیستم Spark را یاد بگیرید.",
    "sections": [
      ("مقدمه", ["خانه", "مقدمه Scala", "نصب", "نحو", "sbt"]),
      ("پایه", ["val / var", "انواع", "توابع", "عبارت"]),
      ("کنترل جریان", ["if", "match", "for comprehension", "Exception"]),
      ("کالکشن", ["List", "Map", "Set", "Option", "Either"]),
      ("شی‌گرایی", ["Class", "Object", "Trait", "Case Class"]),
      ("تابعی", ["Higher-order", "Currying", "Implicits", "Type Class"]),
      ("پیشرفته", ["Generic", "Future", "Akka", "Cats"]),
      ("داده", ["Spark", "بهترین روش‌ها"]),
    ]
  },
]


def make_sidebar(sections):
    html = ['    <aside class="sidebar">', '      <h2>فهرست مطالب</h2>']
    for i, (title, items) in enumerate(sections):
        html.append('      <div class="sidebar-section">')
        if i == 0:
            # first section without h3 or with
            pass
        else:
            html.append(f'        <h3>{title}</h3>')
        for j, item in enumerate(items):
            active = ' active' if i == 0 and j == 0 else ''
            html.append(f'        <a href="#" class="pythons{active}">{item}</a>')
        html.append('      </div>')
    html.append('    </aside>')
    return '\n'.join(html)


def make_features(features):
    cards = []
    for title, desc in features:
        cards.append(f'''        <div class="mini-card">
          <h3>{title}</h3>
          <p>{desc}</p>
        </div>''')
    return '\n'.join(cards)


def generate_language_page(lang):
    sidebar = make_sidebar(lang["sections"])
    features = make_features(lang["features"])
    code = lang["code"]

    page = f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>آموزش {lang["name_en"]} | مدرسه برنامه‌نویسان خاص</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>{SHARED_CSS}</style>
</head>
<body>
{HEADER}
  <section class="hero">
    <h1>{lang["icon"]} آموزش {lang["name_fa"]} ({lang["name_en"]})</h1>
    <p>مسیر یادگیری ساختاریافته از صفر تا سطح کاربردی</p>
  </section>

  <main class="container">
{sidebar}

    <section class="content">
      <div class="card">
        <h2>{lang["name_en"]} چیست؟</h2>
        <p>{lang["desc"]}</p>
      </div>

      <div class="cards">
{features}
      </div>

      <div class="card">
        <h2>اولین کد {lang["name_en"]}</h2>
        <div class="code-box">
          <code>{code}</code>
        </div>
      </div>

      <div class="card">
        <h2>مسیر یادگیری پیشنهادی</h2>
        <p>{lang["path_hint"]}</p>
      </div>
    </section>
  </main>
{FOOTER}
</body>
</html>
'''
    return page


def generate_index(languages):
    cards = []
    for lang in languages:
        cards.append(f'''      <a href="zaban/{lang["slug"]}/{lang["slug"]}.html" class="lang-card">
        <div class="icon">{lang["icon"]}</div>
        <h2>{lang["name_en"]}</h2>
        <p>{lang["name_fa"]}</p>
      </a>''')

    cards_html = "\n".join(cards)

    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>مدرسه برنامه‌نویسان خاص</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: "Vazirmatn", system-ui, sans-serif;
      background-color: #0f1419;
      color: #e6edf3;
      line-height: 1.7;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    a {{ text-decoration: none; color: inherit; }}
    header {{
      width: 100%; background-color: #0d1117;
      border-bottom: 1px solid #21262d;
      padding: 16px 48px;
      display: flex; align-items: center; justify-content: space-between;
    }}
    .logo {{ color: #58a6ff; font-size: 22px; font-weight: 700; }}
    .logo span {{ color: #8b949e; font-weight: 400; font-size: 13px; margin-right: 8px; }}
    nav {{ display: flex; gap: 6px; }}
    nav a {{
      color: #8b949e; font-size: 14px; font-weight: 500;
      padding: 8px 14px; border-radius: 6px;
      transition: color 0.2s, background-color 0.2s;
    }}
    nav a:hover {{ color: #e6edf3; background-color: #161b22; }}
    main {{
      flex: 1; padding: 48px 24px;
      display: flex; flex-direction: column; align-items: center;
    }}
    .hero {{
      text-align: center; max-width: 720px; margin-bottom: 48px;
    }}
    .hero h1 {{
      font-size: 34px; font-weight: 700; color: #e6edf3;
      margin-bottom: 14px; line-height: 1.4;
    }}
    .hero p {{ color: #8b949e; font-size: 16px; max-width: 540px; margin: 0 auto; }}
    .languages {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: 16px;
      width: 100%; max-width: 1000px;
    }}
    .lang-card {{
      background-color: #0d1117;
      border: 1px solid #21262d;
      border-radius: 12px;
      padding: 24px 16px;
      display: flex; flex-direction: column; align-items: center; gap: 8px;
      transition: border-color 0.2s, transform 0.2s, background-color 0.2s;
    }}
    .lang-card:hover {{
      border-color: #388bfd;
      background-color: #161b22;
      transform: translateY(-3px);
    }}
    .lang-card .icon {{ font-size: 32px; }}
    .lang-card h2 {{ font-size: 16px; font-weight: 600; color: #e6edf3; }}
    .lang-card p {{ font-size: 12px; color: #8b949e; }}
    footer {{
      padding: 24px; text-align: center;
      background-color: #0d1117; border-top: 1px solid #21262d;
      color: #6e7681; font-size: 13px;
    }}
    @media (max-width: 700px) {{
      header {{ flex-direction: column; gap: 10px; padding: 14px 18px; }}
      .hero h1 {{ font-size: 26px; }}
      .languages {{ grid-template-columns: repeat(2, 1fr); }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="logo">مدرسه برنامه‌نویسان <span>خاص</span></div>
    <nav>
      <a href="index.html">خانه</a>
      <a href="#">آموزش‌ها</a>
      <a href="#">تمرین‌ها</a>
      <a href="#">درباره ما</a>
    </nav>
  </header>

  <main>
    <section class="hero">
      <h1>به مدرسه برنامه‌نویسان خاص<br>خوش آمدید</h1>
      <p>
        بیش از ۳۰ زبان و فناوری برنامه‌نویسی با مسیر یادگیری ساختاریافته.
        زبان مورد نظر خود را انتخاب کنید و از صفر شروع کنید.
      </p>
    </section>

    <section class="languages">
{cards_html}
    </section>
  </main>

  <footer>
    مدرسه برنامه‌نویسان خاص · یادگیری ساختاریافته برنامه‌نویسی
  </footer>
</body>
</html>
'''


def main():
    ZABAN.mkdir(parents=True, exist_ok=True)

    # Generate each language page
    for lang in LANGUAGES:
        folder = ZABAN / lang["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        page = generate_language_page(lang)
        (folder / f'{lang["slug"]}.html').write_text(page, encoding="utf-8")
        print(f"Generated: {lang['slug']}")

    # Generate index
    index = generate_index(LANGUAGES)
    (BASE / "index.html").write_text(index, encoding="utf-8")
    print("Generated: index.html")

    # Create ZIP
    zip_path = Path("/home/workdir/artifacts/madrase-barnameh-nevisan.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(BASE):
            for f in files:
                full = Path(root) / f
                arc = full.relative_to(BASE)
                zf.write(full, arc)
    print(f"ZIP created: {zip_path}")
    print(f"Total languages: {len(LANGUAGES)}")


if __name__ == "__main__":
    main()

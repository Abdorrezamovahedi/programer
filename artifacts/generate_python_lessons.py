#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate full Python tutorial lessons based on W3Schools structure."""

import os
from pathlib import Path

BASE = Path("/home/workdir/artifacts/site/zaban/python")
BASE.mkdir(parents=True, exist_ok=True)

CSS = '''
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Vazirmatn", system-ui, sans-serif;
  background: #0f1419; color: #e6edf3; line-height: 1.75; font-size: 16px;
}
a { text-decoration: none; color: inherit; }
header {
  background: #0d1117; border-bottom: 1px solid #21262d;
  padding: 14px 40px; display: flex; align-items: center; justify-content: space-between;
  position: sticky; top: 0; z-index: 100;
}
.logo { color: #58a6ff; font-size: 20px; font-weight: 700; }
.logo span { color: #8b949e; font-weight: 400; font-size: 12px; margin-right: 6px; }
nav a {
  color: #8b949e; font-size: 13px; padding: 6px 12px; border-radius: 6px; margin-right: 4px;
}
nav a:hover { color: #e6edf3; background: #161b22; }
.container {
  width: 94%; max-width: 1280px; margin: 28px auto;
  display: grid; grid-template-columns: 260px 1fr; gap: 24px;
}
.sidebar {
  background: #0d1117; border: 1px solid #21262d; border-radius: 12px;
  padding: 16px 12px; position: sticky; top: 70px;
  max-height: calc(100vh - 90px); overflow-y: auto;
}
.sidebar h2 {
  font-size: 11px; color: #8b949e; text-transform: uppercase;
  letter-spacing: 0.5px; margin-bottom: 10px; padding: 0 8px;
}
.sidebar-section { margin-bottom: 16px; }
.sidebar-section h3 {
  font-size: 11px; color: #58a6ff; margin: 10px 0 4px; padding: 0 8px; font-weight: 600;
}
.side-link {
  display: block; padding: 6px 10px; border-radius: 6px; font-size: 13px;
  color: #c9d1d9; margin: 1px 0;
}
.side-link:hover, .side-link.active {
  background: #1f6feb22; color: #58a6ff;
}
.content { display: flex; flex-direction: column; gap: 18px; }
.card {
  background: #0d1117; border: 1px solid #21262d; border-radius: 12px;
  padding: 24px 28px;
}
.card h1 {
  font-size: 26px; font-weight: 700; color: #e6edf3; margin-bottom: 12px;
}
.card h2 {
  font-size: 18px; font-weight: 600; color: #e6edf3; margin: 22px 0 10px;
  padding-top: 12px; border-top: 1px solid #21262d;
}
.card h2:first-of-type { border-top: none; padding-top: 0; margin-top: 8px; }
.card p, .card li { color: #8b949e; font-size: 15px; margin-bottom: 10px; }
.card ul, .card ol { padding-right: 22px; margin-bottom: 12px; }
.card li { margin-bottom: 6px; }
.code-box {
  direction: ltr; text-align: left;
  background: #010409; border: 1px solid #21262d; border-radius: 8px;
  padding: 16px 18px; overflow-x: auto; margin: 12px 0 16px;
}
.code-box code {
  font-family: "SF Mono", Consolas, monospace;
  color: #7ee787; font-size: 14px; line-height: 1.65; white-space: pre;
}
.note {
  background: #1f6feb15; border: 1px solid #388bfd44; border-radius: 8px;
  padding: 12px 16px; margin: 14px 0; color: #79b8ff; font-size: 14px;
}
.nav-lessons {
  display: flex; justify-content: space-between; gap: 12px; margin-top: 8px;
}
.nav-lessons a {
  background: #161b22; border: 1px solid #30363d; border-radius: 8px;
  padding: 10px 16px; color: #58a6ff; font-size: 13px; font-weight: 500;
}
.nav-lessons a:hover { border-color: #58a6ff; }
footer {
  margin-top: 40px; padding: 22px; text-align: center;
  background: #0d1117; border-top: 1px solid #21262d;
  color: #6e7681; font-size: 13px;
}
@media (max-width: 900px) {
  .container { grid-template-columns: 1fr; }
  .sidebar { position: static; max-height: none; }
  header { flex-direction: column; gap: 8px; padding: 12px 16px; }
}
'''

# Sidebar structure: (title, [(slug, label), ...])
SIDEBAR = [
  ("مقدمه", [
    ("index", "خانه"),
    ("intro", "مقدمه پایتون"),
    ("syntax", "ساختار نوشتاری"),
    ("output", "خروجی (print)"),
    ("comments", "توضیحات"),
  ]),
  ("متغیرها و انواع داده", [
    ("variables", "متغیرها"),
    ("variable-names", "نام‌گذاری متغیر"),
    ("multiple-values", "اختصاص چند مقدار"),
    ("data-types", "انواع داده"),
    ("numbers", "اعداد"),
    ("casting", "تبدیل نوع"),
    ("strings", "رشته‌ها"),
    ("string-slicing", "برش رشته"),
    ("string-methods", "متدهای رشته"),
    ("booleans", "بولین"),
  ]),
  ("عملگرها", [
    ("operators", "عملگرها"),
    ("operators-arithmetic", "عملگرهای حسابی"),
    ("operators-comparison", "عملگرهای مقایسه‌ای"),
    ("operators-logical", "عملگرهای منطقی"),
  ]),
  ("ساختارهای داده", [
    ("lists", "لیست‌ها"),
    ("lists-access", "دسترسی به آیتم‌ها"),
    ("lists-methods", "متدهای لیست"),
    ("tuples", "تاپل‌ها"),
    ("sets", "مجموعه‌ها"),
    ("dictionaries", "دیکشنری"),
  ]),
  ("کنترل جریان", [
    ("if-else", "if / elif / else"),
    ("match", "match"),
    ("while", "حلقه while"),
    ("for", "حلقه for"),
  ]),
  ("توابع", [
    ("functions", "توابع"),
    ("arguments", "آرگومان‌ها"),
    ("lambda", "لامبدا"),
    ("scope", "حوزه دسترسی"),
  ]),
  ("شی‌گرایی", [
    ("classes", "کلاس‌ها"),
    ("inheritance", "وراثت"),
  ]),
  ("فایل و خطا", [
    ("files", "کار با فایل"),
    ("try-except", "try / except"),
    ("modules", "ماژول‌ها"),
  ]),
]

LESSONS = {}

# ========== LESSON CONTENTS (based on W3Schools) ==========

LESSONS["index"] = {
  "title": "آموزش پایتون",
  "prev": None,
  "next": "intro",
  "body": '''
    <h1>🐍 آموزش پایتون</h1>
    <p>پایتون یک زبان برنامه‌نویسی سطح بالا، قدرتمند و نسبتاً ساده است که برای ساخت برنامه‌ها، وب‌سایت‌ها، هوش مصنوعی، تحلیل داده و بسیاری از پروژه‌های دیگر استفاده می‌شود.</p>
    <h2>چرا پایتون؟</h2>
    <ul>
      <li><strong>ساده و خوانا:</strong> نحو پایتون به زبان طبیعی نزدیک است.</li>
      <li><strong>قدرتمند:</strong> از پروژه‌های کوچک تا سیستم‌های بزرگ.</li>
      <li><strong>محبوب در هوش مصنوعی:</strong> یکی از اصلی‌ترین زبان‌های ML و AI.</li>
    </ul>
    <h2>اولین کد</h2>
    <div class="code-box"><code>print("Hello World!")

name = "Abdorreza"
print(name)</code></div>
    <div class="note">از منوی سمت راست بخش مورد نظر را انتخاب کنید و قدم‌به‌قدم یاد بگیرید. ساختار این آموزش بر اساس W3Schools طراحی شده است.</div>
  '''
}

LESSONS["intro"] = {
  "title": "مقدمه پایتون",
  "prev": "index",
  "next": "syntax",
  "body": '''
    <h1>مقدمه پایتون</h1>
    <p>پایتون در سال ۱۹۹۱ توسط <strong>Guido van Rossum</strong> منتشر شد. هدف اصلی آن خوانایی بالا و سادگی بود.</p>
    <h2>کاربردهای رایج</h2>
    <ul>
      <li>توسعه وب (Django, Flask)</li>
      <li>هوش مصنوعی و یادگیری ماشین</li>
      <li>تحلیل داده و علم داده</li>
      <li>اتوماسیون و اسکریپت‌نویسی</li>
      <li>توسعه نرم‌افزارهای دسکتاپ</li>
    </ul>
    <h2>نصب پایتون</h2>
    <p>از سایت رسمی <code>python.org</code> نسخه مناسب سیستم‌عامل خود را دانلود و نصب کنید. پس از نصب، در ترمینال بنویسید:</p>
    <div class="code-box"><code>python --version</code></div>
    <p>یا در برخی سیستم‌ها:</p>
    <div class="code-box"><code>python3 --version</code></div>
  '''
}

LESSONS["syntax"] = {
  "title": "ساختار نوشتاری (Syntax)",
  "prev": "intro",
  "next": "output",
  "body": '''
    <h1>ساختار نوشتاری پایتون</h1>
    <p>پایتون برخلاف بسیاری از زبان‌ها از <strong>تورفتگی (Indentation)</strong> برای مشخص کردن بلوک کد استفاده می‌کند، نه از آکولاد <code>{}</code>.</p>
    <h2>تورفتگی</h2>
    <p>تورفتگی باید یکسان باشد (معمولاً ۴ فاصله یا یک Tab):</p>
    <div class="code-box"><code>if 5 > 2:
    print("پنج بزرگ‌تر از دو است")</code></div>
    <div class="note">اگر تورفتگی اشتباه باشد، پایتون خطای IndentationError می‌دهد.</div>
    <h2>نام فایل</h2>
    <p>فایل‌های پایتون معمولاً با پسوند <code>.py</code> ذخیره می‌شوند، مثلاً <code>hello.py</code>.</p>
  '''
}

LESSONS["output"] = {
  "title": "خروجی با print",
  "prev": "syntax",
  "next": "comments",
  "body": '''
    <h1>خروجی در پایتون — تابع print</h1>
    <p>برای نمایش خروجی در پایتون از تابع <code>print()</code> استفاده می‌کنیم.</p>
    <h2>مثال ساده</h2>
    <div class="code-box"><code>print("سلام دنیا")
print(123)
print(3 + 5)</code></div>
    <h2>چند آرگومان</h2>
    <p>می‌توانید چند مقدار را با کاما جدا کنید:</p>
    <div class="code-box"><code>print("نام:", "عبدالرضا")
print("جمع =", 10 + 20)</code></div>
    <h2>پارامتر sep و end</h2>
    <div class="code-box"><code>print("A", "B", "C", sep="-")
# خروجی: A-B-C

print("خط اول", end=" ")
print("ادامه همان خط")</code></div>
  '''
}

LESSONS["comments"] = {
  "title": "توضیحات (Comments)",
  "prev": "output",
  "next": "variables",
  "body": '''
    <h1>توضیحات در پایتون</h1>
    <p>توضیحات (کامنت) برای نوشتن یادداشت در کد استفاده می‌شوند و توسط پایتون اجرا نمی‌شوند.</p>
    <h2>کامنت تک‌خطی</h2>
    <p>با علامت <code>#</code> شروع می‌شود:</p>
    <div class="code-box"><code># این یک توضیح است
print("سلام")  # توضیح بعد از کد</code></div>
    <h2>کامنت چندخطی</h2>
    <p>از سه نقل‌قول استفاده کنید:</p>
    <div class="code-box"><code>"""
این یک توضیح
چندخطی است
"""
print("کد اصلی")</code></div>
  '''
}

LESSONS["variables"] = {
  "title": "متغیرها",
  "prev": "comments",
  "next": "variable-names",
  "body": '''
    <h1>متغیرها در پایتون</h1>
    <p>متغیرها ظرف‌هایی برای ذخیره مقادیر داده هستند. در پایتون نیازی به اعلام نوع متغیر نیست؛ با اولین مقداردهی ایجاد می‌شوند.</p>
    <h2>ایجاد متغیر</h2>
    <div class="code-box"><code>x = 5
y = "John"
print(x)
print(y)</code></div>
    <h2>تغییر نوع</h2>
    <p>متغیر می‌تواند بعداً نوعش را عوض کند:</p>
    <div class="code-box"><code>x = 4       # int
x = "Sally" # حالا str
print(x)</code></div>
    <h2>Casting (تبدیل صریح)</h2>
    <div class="code-box"><code>x = str(3)    # '3'
y = int(3)    # 3
z = float(3)  # 3.0</code></div>
    <h2>دریافت نوع با type()</h2>
    <div class="code-box"><code>x = 5
print(type(x))  # &lt;class 'int'&gt;</code></div>
  '''
}

LESSONS["variable-names"] = {
  "title": "نام‌گذاری متغیر",
  "prev": "variables",
  "next": "multiple-values",
  "body": '''
    <h1>قوانین نام‌گذاری متغیر</h1>
    <ul>
      <li>باید با حرف یا زیرخط <code>_</code> شروع شود.</li>
      <li>نمی‌تواند با عدد شروع شود.</li>
      <li>فقط حروف، اعداد و <code>_</code> مجاز است.</li>
      <li>به حروف بزرگ و کوچک حساس است (<code>age</code> با <code>Age</code> فرق دارد).</li>
    </ul>
    <h2>مثال‌های معتبر</h2>
    <div class="code-box"><code>myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"</code></div>
    <h2>مثال‌های نامعتبر</h2>
    <div class="code-box"><code>2myvar = "John"   # اشتباه
my-var = "John"   # اشتباه
my var = "John"   # اشتباه</code></div>
    <h2>سبک‌های رایج</h2>
    <ul>
      <li><strong>snake_case:</strong> <code>my_variable_name</code> (پیشنهادی در پایتون)</li>
      <li><strong>camelCase:</strong> <code>myVariableName</code></li>
      <li><strong>PascalCase:</strong> <code>MyVariableName</code></li>
    </ul>
  '''
}

LESSONS["multiple-values"] = {
  "title": "اختصاص چند مقدار",
  "prev": "variable-names",
  "next": "data-types",
  "body": '''
    <h1>اختصاص چند مقدار به متغیرها</h1>
    <h2>چند مقدار به چند متغیر</h2>
    <div class="code-box"><code>x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)</code></div>
    <h2>یک مقدار به چند متغیر</h2>
    <div class="code-box"><code>x = y = z = "Orange"
print(x)
print(y)
print(z)</code></div>
    <h2>باز کردن مجموعه (Unpack)</h2>
    <div class="code-box"><code>fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)</code></div>
  '''
}

LESSONS["data-types"] = {
  "title": "انواع داده",
  "prev": "multiple-values",
  "next": "numbers",
  "body": '''
    <h1>انواع داده در پایتون</h1>
    <p>نوع داده مشخص می‌کند چه عملیاتی روی مقدار قابل انجام است.</p>
    <h2>انواع داخلی پایتون</h2>
    <ul>
      <li><strong>متن:</strong> <code>str</code></li>
      <li><strong>عددی:</strong> <code>int</code>, <code>float</code>, <code>complex</code></li>
      <li><strong>دنباله:</strong> <code>list</code>, <code>tuple</code>, <code>range</code></li>
      <li><strong>نگاشت:</strong> <code>dict</code></li>
      <li><strong>مجموعه:</strong> <code>set</code>, <code>frozenset</code></li>
      <li><strong>بولین:</strong> <code>bool</code></li>
      <li><strong>باینری:</strong> <code>bytes</code>, <code>bytearray</code>, <code>memoryview</code></li>
      <li><strong>None:</strong> <code>NoneType</code></li>
    </ul>
    <h2>دریافت نوع</h2>
    <div class="code-box"><code>x = 5
print(type(x))

y = "Hello"
print(type(y))

z = 20.5
print(type(z))</code></div>
    <h2>تنظیم نوع با مقداردهی</h2>
    <div class="code-box"><code>x = "Hello World"   # str
x = 20              # int
x = 20.5            # float
x = ["a", "b"]      # list
x = ("a", "b")      # tuple
x = {"name": "Ali"} # dict
x = True            # bool</code></div>
  '''
}

LESSONS["numbers"] = {
  "title": "اعداد",
  "prev": "data-types",
  "next": "casting",
  "body": '''
    <h1>اعداد در پایتون</h1>
    <p>سه نوع عددی وجود دارد: <code>int</code>، <code>float</code> و <code>complex</code>.</p>
    <h2>مثال</h2>
    <div class="code-box"><code>x = 1      # int
y = 2.8    # float
z = 1j     # complex

print(type(x))
print(type(y))
print(type(z))</code></div>
    <h2>Int</h2>
    <p>عدد صحیح با طول نامحدود:</p>
    <div class="code-box"><code>x = 1
y = 35656222554887711
z = -3255522</code></div>
    <h2>Float</h2>
    <p>عدد اعشاری:</p>
    <div class="code-box"><code>x = 1.10
y = 1.0
z = -35.59
a = 35e3   # 35000.0</code></div>
    <h2>تبدیل بین انواع</h2>
    <div class="code-box"><code>x = 1
y = 2.8
a = float(x)   # 1.0
b = int(y)     # 2
c = complex(x) # (1+0j)</code></div>
  '''
}

LESSONS["casting"] = {
  "title": "تبدیل نوع (Casting)",
  "prev": "numbers",
  "next": "strings",
  "body": '''
    <h1>تبدیل نوع داده</h1>
    <p>با توابع <code>int()</code>، <code>float()</code> و <code>str()</code> می‌توانید نوع را تغییر دهید.</p>
    <h2>به عدد صحیح</h2>
    <div class="code-box"><code>x = int(1)      # 1
y = int(2.8)    # 2
z = int("3")    # 3</code></div>
    <h2>به اعشار</h2>
    <div class="code-box"><code>x = float(1)      # 1.0
y = float(2.8)    # 2.8
z = float("3")    # 3.0
w = float("4.2")  # 4.2</code></div>
    <h2>به رشته</h2>
    <div class="code-box"><code>x = str("s1")  # 's1'
y = str(2)     # '2'
z = str(3.0)   # '3.0'</code></div>
  '''
}

LESSONS["strings"] = {
  "title": "رشته‌ها",
  "prev": "casting",
  "next": "string-slicing",
  "body": '''
    <h1>رشته‌ها در پایتون</h1>
    <p>رشته با نقل‌قول تکی یا دوتایی نوشته می‌شود.</p>
    <div class="code-box"><code>print("Hello")
print('Hello')</code></div>
    <h2>رشته چندخطی</h2>
    <div class="code-box"><code>a = """این یک رشته
چندخطی است
در پایتون"""
print(a)</code></div>
    <h2>رشته به‌عنوان آرایه</h2>
    <div class="code-box"><code>a = "Hello"
print(a[1])  # e</code></div>
    <h2>طول رشته</h2>
    <div class="code-box"><code>a = "Hello World"
print(len(a))  # 11</code></div>
    <h2>بررسی وجود</h2>
    <div class="code-box"><code>txt = "The best things in life are free!"
print("free" in txt)  # True</code></div>
  '''
}

LESSONS["string-slicing"] = {
  "title": "برش رشته",
  "prev": "strings",
  "next": "string-methods",
  "body": '''
    <h1>برش (Slicing) رشته</h1>
    <p>با استفاده از ایندکس می‌توانید بخشی از رشته را بگیرید.</p>
    <h2>برش از موقعیت شروع تا پایان</h2>
    <div class="code-box"><code>b = "Hello, World!"
print(b[2:5])  # llo</code></div>
    <h2>از ابتدا</h2>
    <div class="code-box"><code>print(b[:5])  # Hello</code></div>
    <h2>تا انتها</h2>
    <div class="code-box"><code>print(b[2:])  # llo, World!</code></div>
    <h2>ایندکس منفی</h2>
    <div class="code-box"><code>print(b[-5:-2])  # orl</code></div>
  '''
}

LESSONS["string-methods"] = {
  "title": "متدهای رشته",
  "prev": "string-slicing",
  "next": "booleans",
  "body": '''
    <h1>متدهای پرکاربرد رشته</h1>
    <div class="code-box"><code>a = " Hello, World! "

print(a.upper())        # HELLO, WORLD!
print(a.lower())        # hello, world!
print(a.strip())        # Hello, World!
print(a.replace("H", "J"))
print(a.split(","))     # [' Hello', ' World! ']

print("Hello".startswith("He"))  # True
print("Hello".endswith("lo"))    # True
print("hello".capitalize())      # Hello
print("hello world".title())     # Hello World</code></div>
    <h2>قالب‌بندی با f-string</h2>
    <div class="code-box"><code>name = "علی"
age = 25
print(f"نام من {name} است و {age} سال دارم.")</code></div>
  '''
}

LESSONS["booleans"] = {
  "title": "بولین",
  "prev": "string-methods",
  "next": "operators",
  "body": '''
    <h1>نوع بولین (Boolean)</h1>
    <p>مقادیر بولین فقط دو حالت دارند: <code>True</code> و <code>False</code>.</p>
    <h2>مقایسه</h2>
    <div class="code-box"><code>print(10 > 9)   # True
print(10 == 9)  # False
print(10 < 9)   # False</code></div>
    <h2>تابع bool()</h2>
    <div class="code-box"><code>print(bool("Hello"))  # True
print(bool(15))       # True
print(bool(""))       # False
print(bool(0))        # False
print(bool([]))       # False
print(bool(None))     # False</code></div>
  '''
}

LESSONS["operators"] = {
  "title": "عملگرها",
  "prev": "booleans",
  "next": "operators-arithmetic",
  "body": '''
    <h1>عملگرها در پایتون</h1>
    <p>عملگرها برای انجام عملیات روی متغیرها و مقادیر استفاده می‌شوند.</p>
    <h2>دسته‌های اصلی</h2>
    <ul>
      <li>عملگرهای حسابی</li>
      <li>عملگرهای انتساب</li>
      <li>عملگرهای مقایسه‌ای</li>
      <li>عملگرهای منطقی</li>
      <li>عملگرهای هویتی (is / is not)</li>
      <li>عملگرهای عضویت (in / not in)</li>
      <li>عملگرهای بیتی</li>
    </ul>
    <p>در صفحات بعدی هر دسته را جداگانه بررسی می‌کنیم.</p>
  '''
}

LESSONS["operators-arithmetic"] = {
  "title": "عملگرهای حسابی",
  "prev": "operators",
  "next": "operators-comparison",
  "body": '''
    <h1>عملگرهای حسابی</h1>
    <div class="code-box"><code>x = 10
y = 3

print(x + y)   # 13  جمع
print(x - y)   # 7   تفریق
print(x * y)   # 30  ضرب
print(x / y)   # 3.333... تقسیم
print(x % y)   # 1   باقی‌مانده
print(x ** y)  # 1000 توان
print(x // y)  # 3   تقسیم صحیح</code></div>
  '''
}

LESSONS["operators-comparison"] = {
  "title": "عملگرهای مقایسه‌ای",
  "prev": "operators-arithmetic",
  "next": "operators-logical",
  "body": '''
    <h1>عملگرهای مقایسه‌ای</h1>
    <div class="code-box"><code>x = 5
y = 3

print(x == y)  # False  برابر
print(x != y)  # True   نابرابر
print(x > y)   # True   بزرگ‌تر
print(x < y)   # False  کوچک‌تر
print(x >= y)  # True   بزرگ‌تر یا مساوی
print(x <= y)  # False  کوچک‌تر یا مساوی</code></div>
  '''
}

LESSONS["operators-logical"] = {
  "title": "عملگرهای منطقی",
  "prev": "operators-comparison",
  "next": "lists",
  "body": '''
    <h1>عملگرهای منطقی</h1>
    <div class="code-box"><code>x = 5

print(x > 3 and x < 10)   # True
print(x > 3 or x < 4)     # True
print(not(x > 3 and x < 10))  # False</code></div>
    <div class="note"><code>and</code> وقتی True است که هر دو شرط درست باشند. <code>or</code> وقتی یکی درست باشد. <code>not</code> نتیجه را برعکس می‌کند.</div>
  '''
}

LESSONS["lists"] = {
  "title": "لیست‌ها",
  "prev": "operators-logical",
  "next": "lists-access",
  "body": '''
    <h1>لیست‌ها در پایتون</h1>
    <p>لیست مجموعه‌ای مرتب و قابل‌تغییر است. آیتم‌ها می‌توانند تکراری باشند.</p>
    <h2>ایجاد لیست</h2>
    <div class="code-box"><code>thislist = ["apple", "banana", "cherry"]
print(thislist)
print(len(thislist))  # 3
print(type(thislist))</code></div>
    <h2>سازنده list()</h2>
    <div class="code-box"><code>thislist = list(("apple", "banana", "cherry"))
print(thislist)</code></div>
    <div class="note">لیست با براکت <code>[]</code> ساخته می‌شود و می‌تواند انواع مختلف داده را نگه دارد.</div>
  '''
}

LESSONS["lists-access"] = {
  "title": "دسترسی به آیتم‌های لیست",
  "prev": "lists",
  "next": "lists-methods",
  "body": '''
    <h1>دسترسی به آیتم‌های لیست</h1>
    <div class="code-box"><code>thislist = ["apple", "banana", "cherry"]
print(thislist[1])    # banana
print(thislist[-1])   # cherry
print(thislist[1:3])  # ['banana', 'cherry']
print(thislist[:2])   # ['apple', 'banana']
print(thislist[1:])   # ['banana', 'cherry']</code></div>
    <h2>بررسی وجود</h2>
    <div class="code-box"><code>if "apple" in thislist:
    print("بله، apple در لیست هست")</code></div>
  '''
}

LESSONS["lists-methods"] = {
  "title": "متدهای لیست",
  "prev": "lists-access",
  "next": "tuples",
  "body": '''
    <h1>متدهای مهم لیست</h1>
    <div class="code-box"><code>fruits = ["apple", "banana", "cherry"]

fruits.append("orange")      # اضافه در انتها
fruits.insert(1, "kiwi")     # اضافه در موقعیت
fruits.remove("banana")      # حذف با مقدار
fruits.pop(1)                # حذف با ایندکس
fruits.clear()               # خالی کردن

nums = [3, 1, 4, 1, 5]
nums.sort()                  # مرتب‌سازی
nums.reverse()               # برعکس
print(nums.count(1))         # تعداد تکرار
print(nums.index(4))         # پیدا کردن ایندکس</code></div>
  '''
}

LESSONS["tuples"] = {
  "title": "تاپل‌ها",
  "prev": "lists-methods",
  "next": "sets",
  "body": '''
    <h1>تاپل (Tuple)</h1>
    <p>تاپل مشابه لیست است اما <strong>غیرقابل‌تغییر (immutable)</strong> است.</p>
    <div class="code-box"><code>thistuple = ("apple", "banana", "cherry")
print(thistuple)
print(thistuple[1])
print(len(thistuple))</code></div>
    <h2>تاپل تک‌عضوی</h2>
    <div class="code-box"><code>thistuple = ("apple",)  # کاما الزامی است
print(type(thistuple))</code></div>
    <h2>باز کردن تاپل</h2>
    <div class="code-box"><code>fruits = ("apple", "banana", "cherry")
(x, y, z) = fruits
print(x)</code></div>
  '''
}

LESSONS["sets"] = {
  "title": "مجموعه‌ها (Set)",
  "prev": "tuples",
  "next": "dictionaries",
  "body": '''
    <h1>مجموعه (Set)</h1>
    <p>مجموعه نامرتب، بدون ایندکس و بدون تکرار است.</p>
    <div class="code-box"><code>thisset = {"apple", "banana", "cherry"}
print(thisset)

thisset.add("orange")
thisset.remove("banana")
print("apple" in thisset)</code></div>
    <h2>عملیات مجموعه‌ای</h2>
    <div class="code-box"><code>a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)   # اتحاد
print(a & b)   # اشتراک
print(a - b)   # تفاضل</code></div>
  '''
}

LESSONS["dictionaries"] = {
  "title": "دیکشنری",
  "prev": "sets",
  "next": "if-else",
  "body": '''
    <h1>دیکشنری (Dictionary)</h1>
    <p>دیکشنری داده را به‌صورت جفت کلید-مقدار ذخیره می‌کند.</p>
    <div class="code-box"><code>thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict)
print(thisdict["brand"])
print(thisdict.get("model"))</code></div>
    <h2>تغییر و افزودن</h2>
    <div class="code-box"><code>thisdict["year"] = 2020
thisdict["color"] = "red"
thisdict.update({"year": 2021})</code></div>
    <h2>حذف</h2>
    <div class="code-box"><code>thisdict.pop("model")
del thisdict["year"]
thisdict.clear()</code></div>
    <h2>حلقه روی دیکشنری</h2>
    <div class="code-box"><code>for key, value in thisdict.items():
    print(key, value)</code></div>
  '''
}

LESSONS["if-else"] = {
  "title": "شرط if / elif / else",
  "prev": "dictionaries",
  "next": "match",
  "body": '''
    <h1>دستورات شرطی</h1>
    <h2>if</h2>
    <div class="code-box"><code>a = 33
b = 200
if b > a:
    print("b بزرگ‌تر از a است")</code></div>
    <h2>elif و else</h2>
    <div class="code-box"><code>a = 33
b = 33
if b > a:
    print("b بزرگ‌تر")
elif a == b:
    print("برابر هستند")
else:
    print("a بزرگ‌تر")</code></div>
    <h2>شرط کوتاه (Ternary)</h2>
    <div class="code-box"><code>a = 2
b = 330
print("A") if a > b else print("B")</code></div>
    <h2>and / or / not</h2>
    <div class="code-box"><code>a = 200
b = 33
c = 500
if a > b and c > a:
    print("هر دو شرط درست است")</code></div>
  '''
}

LESSONS["match"] = {
  "title": "دستور match",
  "prev": "if-else",
  "next": "while",
  "body": '''
    <h1>دستور match (از پایتون ۳.۱۰)</h1>
    <p>مشابه switch در زبان‌های دیگر عمل می‌کند.</p>
    <div class="code-box"><code>day = 4
match day:
    case 1:
        print("شنبه")
    case 2:
        print("یکشنبه")
    case 3:
        print("دوشنبه")
    case 4:
        print("سه‌شنبه")
    case _:
        print("روز دیگری")</code></div>
  '''
}

LESSONS["while"] = {
  "title": "حلقه while",
  "prev": "match",
  "next": "for",
  "body": '''
    <h1>حلقه while</h1>
    <p>تا زمانی که شرط True باشد، بلوک اجرا می‌شود.</p>
    <div class="code-box"><code>i = 1
while i < 6:
    print(i)
    i += 1</code></div>
    <h2>break</h2>
    <div class="code-box"><code>i = 1
while i < 6:
    print(i)
    if i == 3:
        break
    i += 1</code></div>
    <h2>continue</h2>
    <div class="code-box"><code>i = 0
while i < 6:
    i += 1
    if i == 3:
        continue
    print(i)</code></div>
  '''
}

LESSONS["for"] = {
  "title": "حلقه for",
  "prev": "while",
  "next": "functions",
  "body": '''
    <h1>حلقه for</h1>
    <p>برای پیمایش روی یک دنباله (لیست، رشته، range و ...) استفاده می‌شود.</p>
    <div class="code-box"><code>fruits = ["apple", "banana", "cherry"]
for x in fruits:
    print(x)</code></div>
    <h2>روی رشته</h2>
    <div class="code-box"><code>for x in "banana":
    print(x)</code></div>
    <h2>range()</h2>
    <div class="code-box"><code>for x in range(6):
    print(x)  # 0 تا 5

for x in range(2, 6):
    print(x)  # 2 تا 5

for x in range(2, 30, 3):
    print(x)  # با گام ۳</code></div>
    <h2>else در for</h2>
    <div class="code-box"><code>for x in range(6):
    print(x)
else:
    print("تمام شد")</code></div>
  '''
}

LESSONS["functions"] = {
  "title": "توابع",
  "prev": "for",
  "next": "arguments",
  "body": '''
    <h1>توابع در پایتون</h1>
    <p>تابع بلوکی از کد است که فقط وقتی صدا زده شود اجرا می‌شود.</p>
    <h2>تعریف و فراخوانی</h2>
    <div class="code-box"><code>def my_function():
    print("Hello from a function")

my_function()</code></div>
    <h2>پارامتر و آرگومان</h2>
    <div class="code-box"><code>def greet(name):
    print("سلام", name)

greet("علی")</code></div>
    <h2>مقدار بازگشتی</h2>
    <div class="code-box"><code>def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8</code></div>
  '''
}

LESSONS["arguments"] = {
  "title": "آرگومان‌ها",
  "prev": "functions",
  "next": "lambda",
  "body": '''
    <h1>انواع آرگومان</h1>
    <h2>آرگومان پیش‌فرض</h2>
    <div class="code-box"><code>def greet(name="مهمان"):
    print("سلام", name)

greet()
greet("رضا")</code></div>
    <h2>*args</h2>
    <div class="code-box"><code>def my_function(*kids):
    print("کوچک‌ترین فرزند:", kids[2])

my_function("Emil", "Tobias", "Linus")</code></div>
    <h2>**kwargs</h2>
    <div class="code-box"><code>def my_function(**kid):
    print("نام خانوادگی:", kid["lname"])

my_function(fname="Tobias", lname="Refsnes")</code></div>
  '''
}

LESSONS["lambda"] = {
  "title": "لامبدا",
  "prev": "arguments",
  "next": "scope",
  "body": '''
    <h1>توابع لامبدا</h1>
    <p>لامبدا یک تابع کوچک و ناشناس است.</p>
    <div class="code-box"><code>x = lambda a: a + 10
print(x(5))  # 15

x = lambda a, b: a * b
print(x(5, 6))  # 30</code></div>
    <h2>استفاده رایج</h2>
    <div class="code-box"><code>def myfunc(n):
    return lambda a: a * n

mydoubler = myfunc(2)
print(mydoubler(11))  # 22</code></div>
  '''
}

LESSONS["scope"] = {
  "title": "حوزه دسترسی (Scope)",
  "prev": "lambda",
  "next": "classes",
  "body": '''
    <h1>حوزه دسترسی متغیرها</h1>
    <h2>متغیر محلی</h2>
    <div class="code-box"><code>def myfunc():
    x = 300
    print(x)

myfunc()</code></div>
    <h2>متغیر سراسری</h2>
    <div class="code-box"><code>x = 300

def myfunc():
    print(x)

myfunc()
print(x)</code></div>
    <h2>کلمه کلیدی global</h2>
    <div class="code-box"><code>x = 300

def myfunc():
    global x
    x = 200

myfunc()
print(x)  # 200</code></div>
  '''
}

LESSONS["classes"] = {
  "title": "کلاس‌ها و اشیاء",
  "prev": "scope",
  "next": "inheritance",
  "body": '''
    <h1>کلاس و شی در پایتون</h1>
    <p>کلاس یک قالب برای ساخت اشیاء است.</p>
    <div class="code-box"><code>class MyClass:
    x = 5

p1 = MyClass()
print(p1.x)</code></div>
    <h2>تابع __init__</h2>
    <div class="code-box"><code>class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("John", 36)
print(p1.name)
print(p1.age)</code></div>
    <h2>متد</h2>
    <div class="code-box"><code>class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def myfunc(self):
        print("سلام، نام من " + self.name)

p1 = Person("John", 36)
p1.myfunc()</code></div>
  '''
}

LESSONS["inheritance"] = {
  "title": "وراثت",
  "prev": "classes",
  "next": "files",
  "body": '''
    <h1>وراثت (Inheritance)</h1>
    <p>وراثت امکان استفاده از خصوصیات کلاس والد در کلاس فرزند را می‌دهد.</p>
    <div class="code-box"><code>class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def printname(self):
        print(self.firstname, self.lastname)

class Student(Person):
    pass

x = Student("Mike", "Olsen")
x.printname()</code></div>
    <h2>اضافه کردن __init__ در فرزند</h2>
    <div class="code-box"><code>class Student(Person):
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)
        self.graduationyear = year</code></div>
  '''
}

LESSONS["files"] = {
  "title": "کار با فایل",
  "prev": "inheritance",
  "next": "try-except",
  "body": '''
    <h1>کار با فایل در پایتون</h1>
    <h2>خواندن فایل</h2>
    <div class="code-box"><code>f = open("demofile.txt", "r")
print(f.read())
f.close()</code></div>
    <h2>خواندن خط به خط</h2>
    <div class="code-box"><code>f = open("demofile.txt", "r")
print(f.readline())
f.close()</code></div>
    <h2>نوشتن / ایجاد</h2>
    <div class="code-box"><code>f = open("demofile2.txt", "w")
f.write("محتوای جدید")
f.close()</code></div>
    <h2>با with (پیشنهادی)</h2>
    <div class="code-box"><code>with open("demofile.txt", "r") as f:
    print(f.read())</code></div>
  '''
}

LESSONS["try-except"] = {
  "title": "try / except",
  "prev": "files",
  "next": "modules",
  "body": '''
    <h1>مدیریت خطا با try / except</h1>
    <div class="code-box"><code>try:
    print(x)
except:
    print("خطایی رخ داد")</code></div>
    <h2>انواع خاص خطا</h2>
    <div class="code-box"><code>try:
    print(x)
except NameError:
    print("متغیر x تعریف نشده")
except:
    print("خطای دیگری")</code></div>
    <h2>else و finally</h2>
    <div class="code-box"><code>try:
    print("سلام")
except:
    print("خطا")
else:
    print("خطایی نبود")
finally:
    print("این بخش همیشه اجرا می‌شود")</code></div>
  '''
}

LESSONS["modules"] = {
  "title": "ماژول‌ها",
  "prev": "try-except",
  "next": None,
  "body": '''
    <h1>ماژول‌ها در پایتون</h1>
    <p>ماژول فایلی حاوی کد پایتون است که می‌توان آن را وارد کرد.</p>
    <h2>ساخت و استفاده</h2>
    <div class="code-box"><code># فایل mymodule.py
def greeting(name):
    print("Hello, " + name)

# فایل اصلی
import mymodule
mymodule.greeting("Jonathan")</code></div>
    <h2>نام مستعار</h2>
    <div class="code-box"><code>import mymodule as mx
mx.greeting("Ali")</code></div>
    <h2>از ماژول داخلی</h2>
    <div class="code-box"><code>import platform
print(platform.system())

from math import sqrt
print(sqrt(16))</code></div>
  '''
}


def build_sidebar(active_slug):
    html = ['    <aside class="sidebar">', '      <h2>فهرست مطالب</h2>']
    for section_title, items in SIDEBAR:
        html.append('      <div class="sidebar-section">')
        html.append(f'        <h3>{section_title}</h3>')
        for slug, label in items:
            cls = "side-link active" if slug == active_slug else "side-link"
            href = f"{slug}.html" if slug != "index" else "python.html"
            # For index we use python.html as main
            if slug == "index":
                href = "python.html"
            else:
                href = f"{slug}.html"
            html.append(f'        <a href="{href}" class="{cls}">{label}</a>')
        html.append('      </div>')
    html.append('    </aside>')
    return "\n".join(html)


def build_page(slug, lesson):
    sidebar = build_sidebar(slug)
    prev_link = ""
    next_link = ""
    if lesson.get("prev"):
        p = lesson["prev"]
        href = "python.html" if p == "index" else f"{p}.html"
        prev_link = f'<a href="{href}">← درس قبلی</a>'
    if lesson.get("next"):
        n = lesson["next"]
        href = f"{n}.html"
        next_link = f'<a href="{href}">درس بعدی →</a>'

    filename = "python.html" if slug == "index" else f"{slug}.html"

    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{lesson["title"]} | آموزش پایتون</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>
  <header>
    <div class="logo">مدرسه برنامه‌نویسان <span>خاص</span></div>
    <nav>
      <a href="../../index.html">خانه</a>
      <a href="python.html">پایتون</a>
      <a href="#">تمرین‌ها</a>
    </nav>
  </header>

  <main class="container">
{sidebar}
    <section class="content">
      <div class="card">
{lesson["body"]}
        <div class="nav-lessons">
          {prev_link}
          {next_link}
        </div>
      </div>
    </section>
  </main>

  <footer>
    مدرسه برنامه‌نویسان خاص · آموزش پایتون بر اساس ساختار W3Schools
  </footer>
</body>
</html>
'''


def main():
    for slug, lesson in LESSONS.items():
        filename = "python.html" if slug == "index" else f"{slug}.html"
        path = BASE / filename
        path.write_text(build_page(slug, lesson), encoding="utf-8")
        print(f"Created: {filename}")
    print(f"Total lessons: {len(LESSONS)}")


if __name__ == "__main__":
    main()

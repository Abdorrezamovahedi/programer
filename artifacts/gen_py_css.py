# -*- coding: utf-8 -*-
"""Rebuild Python + CSS curricula in rich multi-example teaching style."""
import json, re, html as H

src = open("/workspace/artifacts/madrase-complete.html", encoding="utf-8").read()
m = re.search(r"const LESSONS = (\{.*\});\nlet currentLang", src, re.S)
data = json.loads(m.group(1))
STYLE = re.search(r"<style>(.*?)</style>", src, re.S).group(1)

EXTRA_CSS = """
.card h3{font-size:16px;color:#79b8ff;margin:22px 0 10px}
.card ul{padding-right:22px;margin:10px 0 14px}
.card li{color:#b1bac4;margin-bottom:6px;font-size:14.5px}
.warn{background:#f8514918;border:1px solid #f8514944;border-radius:8px;padding:12px 14px;margin:14px 0;color:#ffa198;font-size:14px}
.sum{background:#161b22;border-radius:8px;padding:12px 16px;margin:16px 0}
.sum b{color:#e6edf3;display:block;margin-bottom:8px}
"""
if ".warn{" not in STYLE:
    STYLE += EXTRA_CSS

def esc(s):
    return H.escape(s) if s else ""

def block_code(code):
    return f'<div class="code">{esc(code)}</div>'

def block_exp(lines):
    if not lines:
        return ""
    if isinstance(lines, str):
        return f'<div class="exp">{lines}</div>'
    return '<div class="exp">' + "<br>\n".join(lines) + "</div>"

def rich(title, intro, sections, summary=None, warn=None, where=None):
    """sections: list of dicts {h, p, code, exp}"""
    parts = [f"<h2>{esc(title)}</h2>", f"<p>{intro}</p>"]
    if where:
        parts.append(f"<p><strong>کجا به درد می‌خورد؟</strong> {where}</p>")
    for sec in sections:
        if sec.get("h"):
            parts.append(f"<h3>{esc(sec['h'])}</h3>")
        if sec.get("p"):
            parts.append(f"<p>{sec['p']}</p>")
        if sec.get("code"):
            parts.append(block_code(sec["code"]))
        if sec.get("exp"):
            parts.append(block_exp(sec["exp"]))
        if sec.get("warn"):
            parts.append(f'<div class="warn">{sec["warn"]}</div>')
    if warn:
        parts.append(f'<div class="warn">{warn}</div>')
    if summary:
        items = "".join(f"<li>{x}</li>" for x in summary)
        parts.append(f'<div class="sum"><b>جمع‌بندی سریع</b><ul>{items}</ul></div>')
    return {"t": title, "h": "\n".join(parts)}

# ---------------- PYTHON TITLES ----------------
PY_TITLES = [
"خانه (HOME)","مقدمه (Intro)","شروع کار (Get Started)","ساختار نوشتاری (Syntax)","دستورات (Statements)",
"خروجی (Output)","چاپ اعداد (Print Numbers)","توضیحات (Comments)","متغیرها (Variables)","آزمون (متغیرها)",
"نام متغیرها (Variable Names)","اختصاص چند مقدار (Assign Multiple Values)","نمایش متغیرها (Output Variables)",
"متغیرهای سراسری (Global Variables)","تمرین متغیرها (Variable Exercises)","نوع داده ها (Data Types)",
"اعداد (Numbers)","تبدیل نوع داده (Casting)","رشته ها (Strings)","آزمون (رشته ها)",
"برش رشته (Slicing Strings)","آزمون (برش رشته)","تغییر رشته (Modify Strings)","آزمون (تغییر رشته)",
"ترکیب رشته ها (Concatenate Strings)","آزمون (ترکیب رشته ها)","قالب بندی رشته ها (Format Strings)",
"آزمون (قالب بندی رشته ها)","کاراکتر فرار (Escape Characters)","متدهای رشته (String Methods)",
"تمرین رشته ها (String Exercises)","بولین ها (Booleans)","عملگرها (Operators)",
"عملگرهای حسابی (Arithmetic Operators)","عملگرهای انتسابی (Assignment Operators)",
"عملگرهای مقایسه ای (Comparison Operators)","عملگرهای منطقی (Logical Operators)",
"عملگرهای هویتی (Identity Operators)","عملگرهای عضویت (Membership Operators)",
"عملگرهای بیتی (Bitwise Operators)","اولویت عملگرها (Operator Precedence)",
"لیست ها (Lists)","آزمون (لیست ها)","دسترسی به آیتم ها (Access List Items)","آزمون (دسترسی به آیتم های لیست)",
"تغییر آیتم ها (Change List Items)","آزمون (تغییر آیتم های لیست)","افزودن آیتم (Add List Items)",
"آزمون (افزودن آیتم)","حذف آیتم (Remove List Items)","آزمون (حذف آیتم)",
"حلقه روی لیست (Loop Lists)","آزمون (حلقه روی لیست)","درک لیست (List Comprehension)",
"آزمون (درک لیست)","مرتب سازی لیست (Sort Lists)","آزمون (مرتب سازی لیست)",
"کپی لیست (Copy Lists)","آزمون (کپی لیست)","ادغام لیست ها (Join Lists)","آزمون (ادغام لیست ها)",
"متدهای لیست (List Methods)","تمرین لیست ها (List Exercises)",
"تاپل ها (Tuples)","آزمون (تاپل ها)","دسترسی به تاپل ها (Access Tuples)","آزمون (دسترسی به تاپل ها)",
"به روزرسانی تاپل ها (Update Tuples)","آزمون (به روزرسانی تاپل ها)","باز کردن تاپل ها (Unpack Tuples)",
"آزمون (باز کردن تاپل ها)","حلقه تاپل ها (Loop Tuples)","آزمون (حلقه تاپل ها)",
"ادغام تاپل ها (Join Tuples)","آزمون (ادغام تاپل ها)","متدهای تاپل (Tuple Methods)","تمرین تاپل ها (Tuple Exercises)",
"مجموعه ها (Sets)","آزمون (مجموعه ها)","دسترسی به مجموعه (Access Set Items)","آزمون (دسترسی به مجموعه)",
"افزودن به مجموعه (Add Set Items)","آزمون (افزودن به مجموعه)","حذف از مجموعه (Remove Set Items)",
"آزمون (حذف از مجموعه)","حلقه مجموعه ها (Loop Sets)","آزمون (حلقه مجموعه ها)",
"ادغام مجموعه ها (Join Sets)","آزمون (ادغام مجموعه ها)","فروزن ست (Frozenset)",
"متدهای مجموعه (Set Methods)","تمرین مجموعه ها (Set Exercises)",
"دیکشنری ها (Dictionaries)","آزمون (دیکشنری ها)","دسترسی به آیتم های دیکشنری (Access Items)",
"آزمون (دسترسی دیکشنری)","تغییر آیتم های دیکشنری (Change Items)","آزمون (تغییر دیکشنری)",
"افزودن آیتم های دیکشنری (Add Items)","آزمون (افزودن دیکشنری)","حذف آیتم های دیکشنری (Remove Items)",
"آزمون (حذف دیکشنری)","حلقه دیکشنری ها (Loop Dictionaries)","آزمون (حلقه دیکشنری)",
"کپی دیکشنری ها (Copy Dictionaries)","آزمون (کپی دیکشنری)","تو در تو (Nested Dictionaries)",
"آزمون (دیکشنری تو در تو)","متدهای دیکشنری (Dictionary Methods)","تمرین دیکشنری (Dictionary Exercises)",
"if / elif / else","شرط کوتاه (Shorthand If)","عملگرهای منطقی در شرط","شرط تو در تو (Nested If)",
"pass (Pass Statement)","match (Match)","حلقه while (While Loops)","حلقه for (For Loops)",
"توابع (Functions)","آرگومان ها (Arguments)","*args / **kwargs","حوزه دسترسی (Scope)",
"دکوراتور ها (Decorators)","لانبدا (Lambda)","بازگشت (Recursion)","جنریتور ها (Generators)",
"بازه (Range)","آرایه ها (Arrays)","ایتریتورها (Iterators)","ماژول ها (Modules)",
"تاریخ ها (Dates)","ریاضی (Math)","جیسون (JSON)","عبارات منظم (RegEx)","مدیر بسته ها (PIP)",
"try...except","قالب بندی رشته (String Formatting)","None","ورودی کاربر (User Input)",
"محیط مجازی (VirtualEnv)","شیءگرایی (OOP)","کلاس ها/اشیا (Classes/Objects)","متد init (init Method)",
"پارامتر self (self Parameter)","خصوصیات کلاس (Class Properties)","متدهای کلاس (Class Methods)",
"وراثت (Inheritance)","چندریختی (Polymorphism)","کپسوله سازی (Encapsulation)","کلاس های داخلی (Inner Classes)",
"کار با فایل (File Handling)","خواندن فایل (Read Files)","نوشتن/ایجاد فایل (Write/Create Files)","حذف فایل (Delete Files)",
"آموزش SciPy (SciPy Tutorial)","Matplotlib مقدمه (Matplotlib Intro)","شروع با Matplotlib (Matplotlib Get Started)",
"Pyplot (Matplotlib Pyplot)","نمودارسازی (Matplotlib Plotting)","نشانگرها (Matplotlib Markers)",
"خط (Matplotlib Line)","برچسب ها (Matplotlib Labels)","شبکه (Matplotlib Grid)","زیرنمودار (Matplotlib Subplot)",
"پراکندگی (Matplotlib Scatter)","میله ای (Matplotlib Bars)","هیستوگرام (Matplotlib Histograms)","دایره ای (Matplotlib Pie Charts)",
"یادگیری ماشین: شروع (Getting Started)","میانگین/میانه/نما (Mean Median Mode)","انحراف معیار (Standard Deviation)",
"صدک (Percentile)","توزیع داده (Data Distribution)","توزیع نرمال (Normal Data Distribution)",
"نمودار پراکندگی (Scatter Plot)","رگرسیون خطی (Linear Regression)","رگرسیون چندجمله ای (Polynomial Regression)",
"رگرسیون چندمتغیره (Multiple Regression)","مقیاس بندی (Scale)","آموزش/آزمون (Train/Test)",
"درخت تصمیم (Decision Tree)","ماتریس اغتشاش (Confusion Matrix)","خوشه بندی سلسله مراتبی (Hierarchical Clustering)",
"رگرسیون لجستیک (Logistic Regression)","جست وجوی شبکه ای (Grid Search)","پیش پردازش داده های دسته ای (Categorical Data)",
"K-means","بگینگ (Bootstrap Aggregation)","اعتبارسنجی متقابل (Cross Validation)","منحنی AUC-ROC (AUC-ROC Curve)",
"KNN (K-nearest neighbors)","DSA: معرفی (Python DSA)","لیست ها و آرایه ها (Lists and Arrays)",
"پشته ها (Stacks)","صف ها (Queues)","لیست های پیوندی (Linked Lists)","هش تیبل ها (Hash Tables)",
"درخت ها (Trees)","درخت های دودویی (Binary Trees)","BST (Binary Search Trees)","درخت های AVL (AVL Trees)",
"گراف ها (Graphs)","جستجوی خطی (Linear Search)","جستجوی دودویی (Binary Search)",
"مرتب سازی حبابی (Bubble Sort)","مرتب سازی انتخابی (Selection Sort)","مرتب سازی درج (Insertion Sort)",
"مرتب سازی سریع (Quick Sort)","مرتب سازی شمارشی (Counting Sort)","مرتب سازی رادیکس (Radix Sort)","مرتب سازی ادغامی (Merge Sort)",
"MySQL: شروع (MySQL Get Started)","ایجاد پایگاه داده (Create Database)","ایجاد جدول (Create Table)",
"درج رکورد (Insert)","انتخاب (Select)","شرط Where","مرتب سازی (Order By)","حذف (Delete)",
"حذف جدول (Drop Table)","به روزرسانی (Update)","Limit","Join",
"MongoDB: شروع (Get Started)","ایجاد پایگاه داده Mongo (Create DB)","ایجاد کالکشن (Collection)",
"درج Mongo (Insert)","پیدا کردن (Find)","کوئری (Query)","مرتب سازی Mongo (Sort)",
"حذف Mongo (Delete)","حذف کالکشن (Drop Collection)","به روزرسانی Mongo (Update)","Limit Mongo",
"مرجع: مرور کلی (Overview)","توابع درون ساخته (Built-in Functions)","مرجع متدهای رشته (String Methods Ref)",
"مرجع متدهای لیست (List Methods Ref)","مرجع متدهای دیکشنری (Dictionary Methods Ref)",
"مرجع متدهای تاپل (Tuple Methods Ref)","مرجع متدهای مجموعه (Set Methods Ref)","متدهای فایل (File Methods)",
"کلیدواژه ها (Keywords)","استثناها (Exceptions)","واژه نامه (Glossary)","مرجع ماژول ها (Built-in Modules)",
"ماژول random (Random Module)","ماژول requests (Requests Module)","ماژول statistics (Statistics Module)",
"ماژول math (Math Module)","ماژول cmath (cMath Module)",
"حذف موارد تکراری لیست (Remove List Duplicates)","برعکس کردن رشته (Reverse a String)","جمع دو عدد (Add Two Numbers)",
]

CORE = {}

def C(title, **kw):
    CORE[title] = kw

C("خانه (HOME)",
  intro="این صفحه شروع مسیر پایتون است. از صفر جلو می‌رویم؛ هر درس چند مثال دارد تا دستت گرم شود.",
  where="هر بار که نمی‌دانی از کجا شروع کنی، برگرد اینجا و درس بعد را به ترتیب بخوان.",
  sections=[
    {"h":"اولین خط","p":"print یعنی نشان بده. متن را داخل گیومه بگذار.","code":'print("به آموزش پایتون خوش آمدید")',"exp":["این خط فقط یک پیام چاپ می‌کند.","اگر خطا دیدی، گیومه‌ها را چک کن."]},
  ],
  summary=["از مقدمه شروع کن.","هر مثال را خودت تایپ کن، کپی خالی کافی نیست."])

C("مقدمه (Intro)",
  intro="پایتون یک زبان برنامه‌نویسی خوانا است. جمله‌هایش به حرف زدن نزدیک است، برای همین برای شروع خوب است.",
  where="وب، داده، هوش مصنوعی، اسکریپت‌های روزمره، ربات، خودکار کردن کار تکراری.",
  sections=[
    {"h":"چرا ساده است؟","p":"برای چاپ متن فقط یک دستور لازم است.","code":'print("Hello, Python!")',"exp":["print تابع آماده است.","متن داخل پرانتز همان خروجی است."]},
    {"h":"یک محاسبه کوچک","p":"پایتون ماشین‌حساب هم هست.","code":"print(2 + 3)\nprint(10 / 2)","exp":["جمع ۵ می‌شود.","تقسیم ۵.۰ می‌شود چون تقسیم معمولی اعشار می‌دهد."]},
  ],
  summary=["پایتون خوانا است.","print اولین ابزار دیدن نتیجه است.","بعداً متغیر و شرط می‌آید."])

C("شروع کار (Get Started)",
  intro="پایتون را نصب کن، یک فایل با پسوند .py بساز و اجرا کن. مثل این که قبل از نوشتن، قلم داشته باشی.",
  where="هر پروژه واقعی با نصب و یک فایل خالی شروع می‌شود.",
  sections=[
    {"h":"چک کردن نصب","p":"در ترمینال این را بزن.","code":"python --version","exp":["اگر عددی مثل 3.12 دیدی نصب درست است.","اگر خطا بود python3 را امتحان کن."]},
    {"h":"اولین فایل","p":"فایل را hello.py ذخیره کن.","code":'print("اولین برنامه من")',"exp":["بعد در همان پوشه بنویس: python hello.py"]},
  ],
  summary=["نصب را چک کن.","پسوند فایل باید py باشد.","اجرا از ترمینال است نه فقط باز کردن با دفترچه."])

C("ساختار نوشتاری (Syntax)",
  intro="سینتکس یعنی قانون نوشتن. در پایتون تورفتگی (فاصله اول خط) اجباری است. این فاصله می‌گوید کدام خط مال کدام بلوک است.",
  where="بدون تورفتگی درست، برنامه اصلاً اجرا نمی‌شود.",
  sections=[
    {"h":"تورفتگی","p":"خط بعد از : باید تو برود. معمولاً ۴ فاصله.","code":"if 5 > 2:\n    print(\"پنج بزرگ‌تر است\")","exp":["if شرط را چک می‌کند.","print داخل if است چون تو رفته."]},
    {"h":"اشتباه رایج","p":"اگر تو نروی خطا می‌گیری.","code":"if 5 > 2:\nprint(\"خطا\")  # IndentationError","exp":["این چاپ مال if حساب نمی‌شود."]},
  ],
  warn="مخلوط distanc تب و فاصله نکن. یکی را انتخاب کن (بهتر: ۴ فاصله).",
  summary=["بعد از : خط بعد تو می‌رود.","حساس به حروف بزرگ و کوچک است: Print با print فرق دارد."])

C("اعداد (Numbers)",
  intro="در پایتون، اعداد سه نوع اصلی دارند: int، float و complex. نوع داده یعنی شکل عدد و کارهایی که می‌تواند انجام دهد.",
  where="شمارش، قیمت، معدل، فیزیک و هر محاسبه‌ای.",
  sections=[
    {"h":"انواع عددی","p":"int عدد صحیح است، float اعشار است، complex بخش موهومی با j دارد.","code":"x = 1\ny = 2.8\nz = 1j\nprint(type(x))\nprint(type(y))\nprint(type(z))","exp":["type نوع را نشان می‌دهد.","x از جنس int است.","y از جنس float است.","z از جنس complex است."]},
    {"h":"int: اعداد صحیح","p":"int یعنی عدد کامل بدون اعشار؛ طولش عملاً محدود نیست. مثل تعداد دانش‌آموز کلاس.","code":"x = 1\ny = 35656222554887711\nz = -3255522\nprint(type(x))\nprint(type(y))\nprint(type(z))","exp":["مثبت، خیلی بزرگ، یا منفی؛ همه int هستند."]},
    {"h":"float: اعداد اعشاری","p":"float یعنی عدد با ممیز. مثل معدل یا سرعت دانلود.","code":"x = 1.10\ny = 1.0\nz = -35.59\nprint(type(x))\nprint(type(y))\nprint(type(z))","exp":["حتی 1.0 هم float است چون نقطه دارد."]},
    {"h":"نمایش علمی","p":"e یعنی ضربدر توان ۱۰. 35e3 یعنی ۳۵ × ۱۰³.","code":"x = 35e3\ny = 12E4\nz = -87.7e100\nprint(type(x))\nprint(type(y))\nprint(type(z))","exp":["E و e فرقی ندارند.","خروجی عدد بزرگ float است."]},
    {"h":"complex: اعداد مختلط","p":"بخش موهومی با j نوشته می‌شود. در فیزیک و برق زیاد می‌بینی.","code":"x = 3 + 5j\ny = 5j\nz = -5j\nprint(type(x))\nprint(type(y))\nprint(type(z))","exp":["3 بخش حقیقی، 5j بخش موهومی."]},
    {"h":"تبدیل نوع","p":"با int و float و complex نوع را عوض می‌کنی.","code":"x = 1\ny = 2.8\nz = 1j\na = float(x)\nb = int(y)\nc = complex(x)\nprint(a)\nprint(b)\nprint(c)\nprint(type(a))\nprint(type(b))\nprint(type(c))","exp":["float(1) می‌شود 1.0.","int(2.8) اعشار را می‌بُرد می‌شود 2 نه گرد.","complex(1) می‌شود 1+0j."]},
    {"h":"عدد تصادفی","p":"ماژول random ابزار آماده است.","code":"import random\nprint(random.randrange(1, 10))","exp":["از ۱ تا قبل از ۱۰ یک عدد صحیح تصادفی."]},
  ],
  warn="complex را مستقیم به int تبدیل نکن؛ پایتون اجازه نمی‌دهد.",
  summary=["int برای شمارش بدون اعشار.","float برای اعشار و علمی با e.","complex بخش j دارد.","تبدیل با int/float/complex.","تصادفی با ماژول random."])

C("متغیرها (Variables)",
  intro="متغیر جعبه‌ای با اسم است. مقدار را داخلش می‌گذاری تا بعداً استفاده کنی. در پایتون لازم نیست نوع را از قبل اعلام کنی.",
  where="نام کاربر، قیمت، امتیاز بازی، هر داده‌ای که چند بار لازم داری.",
  sections=[
    {"h":"ساخت و نمایش","p":"با = مقدار می‌دهی.","code":'name = "سارا"\nage = 18\nprint(name)\nprint(age)',"exp":["name متن است.","age عدد است.","print محتویات جعبه را نشان می‌دهد."]},
    {"h":"عوض کردن مقدار","p":"همان اسم را دوباره پر کن.","code":"x = 5\nprint(x)\nx = 10\nprint(x)","exp":["اول ۵.","بعد ۱۰؛ مقدار قبلی پاک می‌شود."]},
  ],
  summary=["اسم با معنی بهتر از x تنها است.","نوع از روی مقدار مشخص می‌شود.","= یعنی بگذار داخل جعبه، نه تساوی ریاضی."])

C("رشته ها (Strings)",
  intro="رشته یعنی متن. بین ' یا \" نوشته می‌شود. نویسه‌ها از صفر شماره می‌خورند.",
  where="نام، پیام، آدرس، عنوان صفحه.",
  sections=[
    {"h":"ساخت و طول","p":"len تعداد نویسه‌ها را می‌دهد.","code":'s = "پایتون"\nprint(s)\nprint(len(s))',"exp":["متن داخل s.","len تعداد نویسه‌ها (برای فارسی ممکن است بایت فرق کند؛ در عمل برای یادگیری len کافی است)."]},
    {"h":"ایندکس","p":"اولین نویسه ایندکس ۰ است. -1 یعنی از آخر.","code":'s = "Hello"\nprint(s[0])\nprint(s[-1])',"exp":["H اول است.","o آخر است."]},
  ],
  summary=["گیومه متن را مشخص می‌کند.","شمارش از صفر.","بعداً برش و متدها می‌آید."])

C("لیست ها (Lists)",
  intro="لیست چند مقدار را پشت‌سرهم نگه می‌دارد و می‌شود کم و زیادشان کرد. با [] ساخته می‌شود.",
  where="لیست خرید، نمرات، نام‌ها.",
  sections=[
    {"h":"ساخت","p":"اعضا با کاما جدا می‌شوند.","code":'names = ["علی", "سارا", "مینا"]\nprint(names)\nprint(len(names))',"exp":["سه اسم.","len تعداد اعضا: ۳."]},
    {"h":"خواندن عضو","p":"ایندکس از صفر.","code":'print(names[0])\nprint(names[-1])',"exp":["اول علی.","آخر مینا."]},
  ],
  summary=["[] یعنی لیست.","قابل تغییر است.","عضو با ایندکس خوانده می‌شود."])

C("دیکشنری ها (Dictionaries)",
  intro="دیکشنری با کلید به مقدار می‌رسد؛ مثل دفترچه: اسم → شماره. با {} و : نوشته می‌شود.",
  where="پروفایل کاربر، تنظیمات، یک ردیف جدول.",
  sections=[
    {"h":"ساخت و خواندن","p":"کلید معمولاً متن است.","code":'user = {"name": "مینا", "age": 22}\nprint(user["name"])\nprint(user.get("city", "نامشخص"))',"exp":["با [کلید] می‌خوانی.","get اگر نبود پیش‌فرض می‌دهد و خطا نمی‌دهد."]},
  ],
  summary=["کلید یکتا است.","خواندن با کلید نه با شماره (مگر کلید عدد باشد)."])

# Auto content by keyword
PY_SNIPS = [
    ("آزمون", "quiz",
     [{"h":"چند سؤال","p":"اول بدون نگاه به جواب فکر کن.","code":"# 1) خروجی print(2**3) چیست؟\n# 2) ایندکس اولین عضو لیست چند است؟\n# 3) برای متن از چه گیومه‌ای می‌شود استفاده کرد؟","exp":["جواب ۱: ۸ چون ۲×۲×۲.","جواب ۲: صفر.","جواب ۳: ' یا \"."]}],
     ["اگر غلط جواب دادی همان درس اصلی را دوباره بخوان."]),
    ("تمرین", "ex",
     [{"h":"کار عملی","p":"این را خودت در فایل بنویس و اجرا کن.","code":"# تمرین: یک متغیر بساز و چاپ کن\nmsg = \"انجام شد\"\nprint(msg)","exp":["اگر چاپ شد تمرین اول قبول است."]}],
     ["تمرین را تغییر بده تا مال خودت شود."]),
    ("برش", "slice",
     [{"h":"سینتکس","p":"s[شروع:پایان] تا قبل از پایان را می‌گیرد.","code":'s = "HelloWorld"\nprint(s[0:5])\nprint(s[5:])\nprint(s[:5])\nprint(s[::-1])',"exp":["Hello","World","Hello","برعکس کل متن."]}],
     ["پایان داخل برش نیست.","گام منفی متن را برعکس می‌کند."]),
    ("کامنت", "cmt",
     [{"h":"یک خط و چند خط","p":"# برای یک خط. سه گیومه برای چند خط.","code":"# توضیح\nprint(1)\n'''\nچند خط\n'''","exp":["# اجرا نمی‌شود.","print اجرا می‌شود."]}],
     ["کامنت خوب «چرا» را می‌گوید."]),
    ("for", "for",
     [{"h":"روی بازه","p":"range تعداد تکرار را می‌سازد.","code":"for i in range(3):\n    print(i)","exp":["۰ سپس ۱ سپس ۲."]},
      {"h":"روی لیست","p":"هر عضو را یکی‌یکی می‌آورد.","code":'for n in ["a","b"]:\n    print(n)',"exp":["اول a بعد b."]}],
     ["بدنه حلقه باید تو برود."]),
    ("while", "wh",
     [{"h":"تا وقتی شرط","p":"شرط را هر دور چک می‌کند.","code":"i = 0\nwhile i < 3:\n    print(i)\n    i += 1","exp":["اگر i زیاد نشود حلقه تمام نمی‌شود."]}],
     ["شرط خروج را فراموش نکن."]),
    ("تابع", "fn",
     [{"h":"تعریف","p":"def اسم و پرانتز و :","code":"def add(a, b):\n    return a + b\nprint(add(2, 3))","exp":["return نتیجه را برمی‌گرداند.","خروجی ۵."]}],
     ["یک تابع یک کار مشخص بکند."]),
    ("کلاس", "cls",
     [{"h":"قالب شیء","p":"class نقشه است؛ new با صدا زدن کلاس نمونه می‌سازد.","code":"class Person:\n    def __init__(self, name):\n        self.name = name\n    def hello(self):\n        print(\"سلام\", self.name)\n\np = Person(\"علی\")\np.hello()","exp":["__init__ موقع ساخت اجرا می‌شود.","self یعنی همین شیء."]}],
     ["شیء داده + رفتار است."]),
    ("فایل", "file",
     [{"h":"نوشتن و خواندن","p":"with فایل را خودکار می‌بندد.","code":"with open(\"a.txt\", \"w\", encoding=\"utf-8\") as f:\n    f.write(\"سلام\\n\")\nwith open(\"a.txt\", encoding=\"utf-8\") as f:\n    print(f.read())","exp":["w از صفر می‌نویسد.","encoding برای فارسی."]}],
     ["همیشه encoding را مشخص کن."]),
    ("JSON", "json",
     [{"h":"تبدیل","p":"dumps به متن، loads از متن.","code":"import json\ns = json.dumps({\"name\": \"علی\"}, ensure_ascii=False)\nprint(s)\nprint(json.loads(s)[\"name\"])","exp":["ensure_ascii=False فارسی را درست نگه می‌دارد."]}],
     ["JSON پل بین برنامه‌ها است."]),
    ("خطا", "err",
     [{"h":"try except","p":"اگر خطا شد برنامه نایستد.","code":"try:\n    print(int(\"x\"))\nexcept ValueError:\n    print(\"عدد نبود\")","exp":["int('x') خطا می‌دهد.","except همان را می‌گیرد."]}],
     ["نوع خطا را مشخص کن بهتر از except خالی است."]),
]

def py_auto(title):
    short = title.split("(")[0].strip()
    sections = None
    summary = None
    intro = f"در این درس «{short}» را در پایتون با مثال می‌بینی. اول معنی، بعد کد، بعد خط‌به‌خط."
    where = f"هر وقت در برنامه به «{short}» رسیدی."
    # match snippets
    for key, _, secs, sm in PY_SNIPS:
        if key in title:
            sections = secs
            summary = sm
            break
    if sections is None:
        # topic-specific codes
        code = 'print("موضوع: ' + short.replace('"','') + '")'
        extra = None
        if "لیست" in title or "List" in title:
            code = 'a = [3, 1, 2]\na.append(4)\nprint(a)\nprint(sorted(a))'
            extra = ["append به آخر اضافه می‌کند.","sorted لیست جدید مرتب می‌دهد."]
        elif "تاپل" in title or "Tuple" in title:
            code = 't = (1, 2, 3)\nprint(t[0])\nprint(len(t))'
            extra = ["تاپل با () است.","بعد از ساخت معمولاً عوض نمی‌شود."]
        elif "مجموعه" in title or "Set" in title:
            code = 's = {1, 2, 2, 3}\nprint(s)\ns.add(4)'
            extra = ["تکراری نگه نمی‌دارد."]
        elif "دیکشنری" in title or "Dict" in title:
            code = 'd = {"a": 1}\nd["b"] = 2\nfor k, v in d.items():\n    print(k, v)'
            extra = ["items کلید و مقدار."]
        elif "رشته" in title or "String" in title:
            code = 's = "Python"\nprint(s.upper())\nprint(s.replace("P", "J"))'
            extra = ["upper کپی بزرگ می‌دهد.","replace جایگزینی می‌کند."]
        elif "عملگر" in title or "Operator" in title:
            code = 'print(10 + 3)\nprint(10 > 3)\nprint(True and False)'
            extra = ["حساب.","مقایسه.","منطق."]
        elif "Matplotlib" in title or "نمودار" in title or "میله" in title or "هیستو" in title:
            code = 'import matplotlib.pyplot as plt\nplt.plot([1, 2, 3], [1, 4, 9])\nplt.title("نمونه")\n# plt.show()'
            extra = ["plot خط می‌کشد.","title عنوان است."]
        elif "MySQL" in title or "Select" in title or "Insert" in title:
            code = '# pip install mysql-connector-python\n# conn = mysql.connector.connect(host="localhost", user="root", password="", database="test")'
            extra = ["اول اتصال، بعد cursor، بعد execute."]
        elif "Mongo" in title:
            code = '# from pymongo import MongoClient\n# db = MongoClient()["shop"]\n# db.users.insert_one({"name": "علی"})'
            extra = ["کالکشن مثل جدول است ولی سند JSON می‌گیرد."]
        elif "مرتب" in title or "Sort" in title:
            code = 'a = [4, 1, 3]\nprint(sorted(a))\nfor i in range(len(a)):\n    for j in range(len(a)-1):\n        if a[j] > a[j+1]:\n            a[j], a[j+1] = a[j+1], a[j]\nprint(a)'
            extra = ["sorted ساده است.","حلقه دوتایی ایده حبابی است."]
        elif "جستجو" in title or "Search" in title or "KNN" in title:
            code = 'a = [1, 3, 5, 7]\nprint(3 in a)\n# دودویی روی لیست مرتب\nlo, hi = 0, len(a)-1\nx = 5\nwhile lo <= hi:\n    mid = (lo+hi)//2\n    if a[mid] == x:\n        print("پیدا", mid); break\n    elif a[mid] < x:\n        lo = mid+1\n    else:\n        hi = mid-1'
            extra = ["in ساده است.","دودویی فقط روی مرتب."]
        elif "ماشین" in title or "رگرسیون" in title or "K-means" in title or "درخت تصمیم" in title:
            code = 'xs = [1, 2, 3, 4]\nys = [2, 4, 6, 8]\n# ایده خط: y ≈ 2x\nprint([2*x for x in xs])'
            extra = ["مدل رابطه ورودی و خروجی را یاد می‌گیرد."]
        elif "random" in title:
            code = 'import random\nprint(random.randint(1, 6))\nprint(random.choice(["a", "b", "c"]))'
            extra = ["randint دو سر را شامل می‌شود."]
        elif "math" in title.lower() or "ریاضی" in title:
            code = 'import math\nprint(math.sqrt(16))\nprint(math.pi)\nprint(math.floor(3.7))'
            extra = ["sqrt ریشه.","floor کف."]
        elif "PIP" in title or "Virtual" in title:
            code = 'python -m venv .venv\n# .venv\\Scripts\\activate  (ویندوز)\n# pip install requests'
            extra = ["venv محیط جدا است تا کتابخانه‌ها قاطی نشوند."]
        elif "lambda" in title or "لانبدا" in title:
            code = 'f = lambda x: x * 2\nprint(f(5))\nprint(list(map(lambda x: x+1, [1, 2])))'
            extra = ["تابع یک‌خطی."]
        elif "Decorator" in title or "دکوراتور" in title:
            code = 'def wrap(fn):\n    def inner():\n        print("قبل")\n        fn()\n        print("بعد")\n    return inner\n@wrap\ndef hi():\n    print("hi")\nhi()'
            extra = ["@wrap یعنی hi را بپیچ."]
        elif "Generator" in title or "جنریتور" in title:
            code = 'def g():\n    yield 1\n    yield 2\nfor x in g():\n    print(x)'
            extra = ["yield مقدار را یکی‌یکی می‌دهد بدون ساخت کل لیست."]
        elif "args" in title:
            code = 'def f(*args, **kwargs):\n    print(args)\n    print(kwargs)\nf(1, 2, a=3)'
            extra = ["*args تاپل نامشخص.","**kwargs دیکشنری نام‌دار."]
        elif "None" in title:
            code = 'x = None\nprint(x is None)\nprint(x == None)  # بهتر: is'
            extra = ["None یعنی خالی.","با is مقایسه کن."]
        elif "ورودی" in title or "Input" in title:
            code = 'name = input("اسمت؟ ")\nprint("سلام", name)\n# n = int(input("عدد؟ "))'
            extra = ["input همیشه رشته برمی‌گرداند."]
        elif "match" in title.lower():
            code = 'x = 2\nmatch x:\n    case 1:\n        print("یک")\n    case 2:\n        print("دو")\n    case _:\n        print("دیگر")'
            extra = ["شبیه switch. _ یعنی پیش‌فرض."]
        elif "pass" in title.lower():
            code = 'if True:\n    pass  # بعداً پر می‌کنم\nprint("ادامه")'
            extra = ["pass یعنی هیچ کاری نکن؛ جای خالی قانونی."]
        elif "if" in title.lower() or "شرط" in title:
            code = 'score = 14\nif score >= 17:\n    print("عالی")\nelif score >= 10:\n    print("قبول")\nelse:\n    print("مردود")'
            extra = ["اولین شرط درست اجرا می‌شود."]
        elif "وراثت" in title or "Inherit" in title:
            code = 'class Animal:\n    def speak(self):\n        print("صدا")\nclass Dog(Animal):\n    pass\nDog().speak()'
            extra = ["Dog متد پدر را دارد."]
        elif "self" in title:
            code = 'class A:\n    def __init__(self, v):\n        self.v = v\n    def show(self):\n        print(self.v)\nA(5).show()'
            extra = ["self همان شیء صدا زننده است."]
        elif "init" in title:
            code = 'class Box:\n    def __init__(self, n):\n        self.n = n\nprint(Box(3).n)'
            extra = ["موقع Box(3) اجرا می‌شود."]
        elif "Stack" in title or "پشته" in title:
            code = 'st = []\nst.append(1)\nst.append(2)\nprint(st.pop())  # 2'
            extra = ["آخرین ورود، اولین خروج."]
        elif "Queue" in title or "صف" in title:
            code = 'from collections import deque\nq = deque()\nq.append(1)\nq.append(2)\nprint(q.popleft())  # 1'
            extra = ["اولین ورود، اولین خروج."]
        elif "درخت" in title or "Graph" in title or "گراف" in title or "BST" in title or "AVL" in title:
            code = 'class Node:\n    def __init__(self, v):\n        self.v = v\n        self.left = None\n        self.right = None\nroot = Node(5)\nroot.left = Node(3)'
            extra = ["هر گره مقدار و فرزند دارد."]
        elif "Hash" in title or "هش" in title:
            code = 'print(hash("علی"))\nd = {}\nd["علی"] = 1  # دیکشنری از هش استفاده می‌کند'
            extra = ["جستجو تقریباً سریع است."]
        elif "requests" in title:
            code = '# import requests\n# r = requests.get("https://example.com")\n# print(r.status_code)'
            extra = ["pip install requests"]
        elif "SciPy" in title:
            code = '# from scipy import stats\n# print(stats.describe([1,2,3,4]))'
            extra = ["برای علمی و آمار."]
        elif "کپی" in title or "Copy" in title:
            code = 'a = [1, 2]\nb = a.copy()\nb.append(3)\nprint(a, b)'
            extra = ["بدون copy هر دو همان لیست‌اند."]
        elif "ادغام" in title or "Join" in title:
            code = 'print([1,2] + [3])\nprint({1,2} | {2,3})'
            extra = ["لیست با +. مجموعه با |."]
        elif "متد" in title or "Methods" in title:
            code = 's = "  Hi "\nprint(s.strip().lower())\na = [1, 2]\na.extend([3])\nprint(a)'
            extra = ["متد با نقطه صدا زده می‌شود."]
        elif "Range" in title or "بازه" in title:
            code = 'print(list(range(3)))\nprint(list(range(1, 5, 2)))'
            extra = ["پایان داخل بازه نیست. گام ۲ یعنی یکی در میان."]
        elif "Iterator" in title or "ایتریتور" in title:
            code = 'it = iter([10, 20])\nprint(next(it))\nprint(next(it))'
            extra = ["next عضو بعدی."]
        elif "ماژول" in title or "Module" in title:
            code = 'import math\nfrom math import sqrt\nprint(math.pi, sqrt(9))'
            extra = ["import کل ماژول. from یک اسم."]
        elif "تاریخ" in title or "Date" in title:
            code = 'from datetime import datetime, timedelta\nprint(datetime.now())\nprint(datetime.now() + timedelta(days=1))'
            extra = ["timedelta فاصله زمانی."]
        elif "RegEx" in title or "منظم" in title:
            code = 'import re\nprint(re.findall(r"\\d+", "a12 b34"))\nprint(bool(re.match(r"^09\\d{9}$", "09121234567")))'
            extra = ["\\d یعنی رقم."]
        elif "PIP" in title:
            code = 'pip install requests\npip list'
            extra = ["نصب بسته از اینترنت."]
        elif "کلیدواژه" in title or "Keyword" in title:
            code = 'import keyword\nprint(keyword.iskeyword("if"))\n# if = 1  # خطا: if کلمه رزرو است'
            extra = ["کلمات رزرو را اسم متغیر نگذار."]
        elif "واژه" in title or "Overview" in title or "Glossary" in title or "مرجع" in title:
            code = '# متغیر، رشته، لیست، دیکشنری، تابع، کلاس، ماژول'
            extra = ["این‌ها واژه‌های پایه مسیرند."]
        elif "برعکس" in title:
            code = 's = "abcd"\nprint(s[::-1])\nprint("".join(reversed(s)))'
            extra = ["[::-1] ساده‌ترین راه."]
        elif "تکراری" in title or "Duplicate" in title:
            code = 'a = [1, 1, 2, 3, 2]\nprint(list(dict.fromkeys(a)))'
            extra = ["dict.fromkeys ترتیب را نگه می‌دارد."]
        elif "جمع دو" in title or "Add Two" in title:
            code = 'a, b = 4, 7\nprint(a + b)\n# a = int(input()); b = int(input())'
            extra = ["ورودی را int کن وگرنه متن به هم می‌چسبد."]
        elif "print" in title.lower() or "خروجی" in title or "چاپ" in title:
            code = 'print("سلام")\nprint(2, 3, sep="-")\nprint("هم", end=" ")\nprint("خط")'
            extra = ["sep بین مقادیر.","end پایان خط را عوض می‌کند."]
        elif "نام متغیر" in title or "Variable Names" in title:
            code = 'my_name = "علی"\ntotal_price = 1500\n# 2name = 1   خطا\n# my-name = 1  خطا'
            extra = ["حرف یا _ اول. فاصله و - ممنوع. snake_case رایج است."]
        elif "سراسری" in title or "Global" in title:
            code = 'x = 10\ndef f():\n    global x\n    x = 20\nf()\nprint(x)'
            extra = ["بدون global داخل تابع x محلی است."]
        elif "اختصاص" in title or "Assign" in title:
            code = 'x, y, z = 1, 2, 3\na = b = 0\nprint(x, y, z, a, b)'
            extra = ["تعداد دو طرف باید برابر باشد."]
        elif "نمایش متغیر" in title or "Output Variables" in title:
            code = 'name, age = "علی", 20\nprint("نام:", name)\nprint(f"سن: {age}")'
            extra = ["f-string خواناترین راه است."]
        elif "تبدیل" in title or "Casting" in title:
            code = 'print(int("25") + 5)\nprint(str(100) + "!")\nprint(float("3.5"))'
            extra = ["ورودی کاربر متن است؛ برای حساب int کن."]
        elif "بولین" in title or "Boolean" in title:
            code = 'print(bool(1), bool(0), bool(""), bool("x"))\nprint(10 > 3)'
            extra = ["۰ و رشته خالی False اند."]
        elif "فرار" in title or "Escape" in title:
            code = 'print("خط\\nبعد")\nprint("او گفت: \\"سلام\\"")'
            extra = ["\\n خط جدید. \\\" گیومه."]
        elif "قالب" in title or "Format" in title:
            code = 'name = "سارا"\nprint(f"سلام {name}")\nprint("سلام {}".format(name))'
            extra = ["f-string پیشنهادی است."]
        elif "ترکیب" in title or "Concat" in title:
            code = 'print("سلام " + "دنیا")\nprint("a" * 3)'
            extra = ["+ می‌چسباند. * تکرار می‌کند."]
        elif "تغییر رشته" in title or "Modify" in title:
            code = 's = "  Hello "\nprint(s.strip())\nprint(s.lower())\nprint(s.replace("H", "J"))'
            extra = ["اصل s عوض نمی‌شود مگر دوباره ذخیره کنی."]
        elif "افزودن" in title or "Add List" in title or "Add Items" in title:
            code = 'a = [1]\na.append(2)\na.insert(0, 0)\nprint(a)'
            extra = ["append آخر. insert جای مشخص."]
        elif "حذف" in title and "List" in title or "Remove List" in title or "حذف آیتم" in title:
            code = 'a = [1, 2, 3, 2]\na.remove(2)\nprint(a)\nprint(a.pop())'
            extra = ["remove اولین ۲. pop آخر را برمی‌دارد."]
        elif "درک لیست" in title or "Comprehension" in title:
            code = 'print([x*x for x in range(5)])\nprint([x for x in range(6) if x % 2 == 0])'
            extra = ["کوتاه‌نویسی حلقه + شرط."]
        elif "مرتب سازی لیست" in title:
            code = 'a = [3, 1, 2]\nprint(sorted(a))\na.sort(reverse=True)\nprint(a)'
            extra = ["sorted جدید می‌سازد. sort روی خودش."]
        elif "unpack" in title.lower() or "باز کردن" in title:
            code = 'a, b, *rest = [1, 2, 3, 4]\nprint(a, b, rest)'
            extra = ["* بقیه را در لیست می‌ریزد."]
        elif "Frozenset" in title or "فروزن" in title:
            code = 'f = frozenset([1, 2, 2])\nprint(f)\n# f.add(3)  خطا'
            extra = ["مجموعه قفل‌شده؛ کلید دیکشنری می‌تواند باشد."]
        elif "تو در تو" in title or "Nested" in title:
            code = 'users = {"u1": {"name": "علی"}}\nprint(users["u1"]["name"])'
            extra = ["دو کلید پشت سر هم."]
        elif "شرط کوتاه" in title or "Shorthand" in title:
            code = 'age = 20\nmsg = "بالغ" if age >= 18 else "نوجوان"\nprint(msg)'
            extra = ["if یک‌خطی."]
        elif "منطقی" in title:
            code = 'print(True and False)\nprint(True or False)\nprint(not True)'
            extra = ["and هر دو. or یکی. not برعکس."]
        elif "هویت" in title or "Identity" in title:
            code = 'a = [1]\nb = a\nc = [1]\nprint(a is b)\nprint(a is c)\nprint(a == c)'
            extra = ["is همان شیء در حافظه. == مقدار برابر."]
        elif "عضویت" in title or "Membership" in title:
            code = 'print(2 in [1,2,3])\nprint("a" not in "bc")'
            extra = ["in یعنی داخل است."]
        elif "بیتی" in title or "Bitwise" in title:
            code = 'print(5 & 3)\nprint(5 | 3)\nprint(5 << 1)'
            extra = ["و بیتی، یا بیتی، شیفت."]
        elif "اولویت" in title or "Precedence" in title:
            code = 'print(2 + 3 * 4)\nprint((2 + 3) * 4)'
            extra = ["ضرب زودتر از جمع. پرانتز اولویت را عوض می‌کند."]
        elif "حسابی" in title or "Arithmetic" in title:
            code = 'print(10 + 3)\nprint(10 - 3)\nprint(10 * 3)\nprint(10 / 3)\nprint(10 // 3)\nprint(10 % 3)\nprint(2 ** 3)'
            extra = ["/ اعشار. // صحیح. % باقی‌مانده. ** توان."]
        elif "انتساب" in title or "Assignment" in title:
            code = 'x = 5\nx += 2\nprint(x)'
            extra = ["+= یعنی قبلی به‌علاوه."]
        elif "مقایسه" in title or "Comparison" in title:
            code = 'print(5 == 5)\nprint(5 != 3)\nprint(5 > 2)\nprint(5 <= 5)'
            extra = ["== تساوی مقدار. != نامساوی."]
        elif "type" in title.lower() or "نوع داده" in title:
            code = 'print(type(10), type(1.5), type("a"), type(True), type([1]), type({"a":1}))'
            extra = ["int float str bool list dict."]
        elif "دستور" in title or "Statement" in title:
            code = 'x = 1\nx = x + 1\nprint(x)'
            extra = ["از بالا به پایین یکی‌یکی."]
        elif "SciPy" in title or "percentile" in title.lower() or "انحراف" in title or "میانگین" in title:
            code = 'nums = [1, 2, 2, 3, 10]\nprint(sum(nums)/len(nums))\nprint(sorted(nums)[len(nums)//2])'
            extra = ["میانگین جمع÷تعداد. میانه عضو وسط مرتب."]
        elif "Join" == title or title.endswith("Join"):
            code = 'print("SELECT * FROM a JOIN b ON a.id=b.a_id")'
            extra = ["اتصال دو جدول با کلید مشترک."]
        elif "Limit" in title:
            code = '# SELECT * FROM users LIMIT 10 OFFSET 20'
            extra = ["صفحه‌بندی."]
        elif "Where" in title:
            code = '# cursor.execute("SELECT * FROM users WHERE age>%s", (18,))'
            extra = ["فیلتر ردیف. مقدار را جدا بده تا تزریق نشود."]
        elif "Drop" in title:
            code = '# DROP TABLE IF EXISTS temp;'
            extra = ["برگشت ندارد؛ با احتیاط."]
        elif "Update" in title:
            code = '# UPDATE users SET name=%s WHERE id=%s'
            extra = ["WHERE یادت نرود."]
        elif "Delete" in title and "Mongo" not in title:
            code = '# DELETE FROM users WHERE id=%s'
            extra = ["بدون WHERE همه پاک می‌شود."]
        elif "Find" in title or "Query" in title:
            code = '# db.users.find({"age": {"$gt": 18}})'
            extra = ["فیلتر سندها در Mongo."]
        elif "Collection" in title:
            code = '# db.create_collection("users")'
            extra = ["کالکشن ظرف سندها است."]
        elif "Built-in" in title or "درون ساخته" in title:
            code = 'print(len("ab"), max([1,9]), min([1,9]), sum([1,2]), abs(-3))'
            extra = ["توابع همیشه آماده‌اند بدون import (بعضی‌ها)."]
        elif "File Methods" in title or "متدهای فایل" in title:
            code = 'f = open("a.txt", "w", encoding="utf-8")\nf.write("x")\nf.close()'
            extra = ["بهتر است with استفاده کنی."]
        elif "استثنا" in title or "Exception" in title:
            code = 'try:\n    1/0\nexcept ZeroDivisionError as e:\n    print(type(e).__name__, e)'
            extra = ["نام خطا را بخوان."]
        elif "cmath" in title:
            code = 'import cmath\nprint(cmath.sqrt(-1))'
            extra = ["برای اعداد مختلط."]
        elif "statistics" in title:
            code = 'import statistics as st\nprint(st.mean([1,2,3]))\nprint(st.median([1,2,9]))'
            extra = ["میانگین و میانه آماده."]
        elif "AUC" in title or "Cross" in title or "Bagging" in title or "Grid Search" in title or "Confusion" in title or "Categorical" in title or "Scale" in title or "Train" in title:
            code = '# ایده: داده را دو بخش کن — آموزش و آزمون\ntrain, test = [1,2,3], [4]\nprint(len(train), len(test))'
            extra = ["مدل را روی آموزش یاد بده، روی آزمون بسنج."]
        elif "چندریختی" in title or "Poly" in title:
            code = 'class A:\n    def f(self): print("A")\nclass B(A):\n    def f(self): print("B")\nfor o in (A(), B()):\n    o.f()'
            extra = ["همین اسم متد، رفتار متفاوت."]
        elif "کپسول" in title or "Encaps" in title:
            code = 'class A:\n    def __init__(self):\n        self.__x = 1\n    def get(self):\n        return self.__x\nprint(A().get())'
            extra = ["__x از بیرون مستقیم توصیه نمی‌شود."]
        elif "داخلی" in title or "Inner" in title:
            code = 'class Outer:\n    class Inner:\n        def hi(self): print("in")\nOuter.Inner().hi()'
            extra = ["کلاس داخل کلاس."]
        elif "حذف فایل" in title:
            code = 'import os\n# os.remove("a.txt")\nprint(os.path.exists("a.txt"))'
            extra = ["قبل از حذف وجود را چک کن."]
        elif "خواندن فایل" in title:
            code = 'open("a.txt","w",encoding="utf-8").write("سلام\\nخط2\\n")\nwith open("a.txt",encoding="utf-8") as f:\n    for line in f:\n        print(line.strip())'
            extra = ["حلقه روی فایل خط‌به‌خط می‌خواند."]
        elif "نوشتن" in title:
            code = 'with open("a.txt","a",encoding="utf-8") as f:\n    f.write("خط جدید\\n")'
            extra = ["a یعنی اضافه به انتها. w پاک می‌کند و از نو."]
        elif "خصوصیات" in title or "Properties" in title or "متدهای کلاس" in title:
            code = 'class C:\n    n = 0\n    def __init__(self):\n        C.n += 1\nC(); C()\nprint(C.n)'
            extra = ["n مال کلاس است، مشترک بین نمونه‌ها."]
        elif "OOP" in title or "شیءگرایی" in title:
            code = 'class Dog:\n    def __init__(self, n):\n        self.n = n\n    def bark(self):\n        print(self.n, "واق")\nDog("پشمکی").bark()'
            extra = ["داده n و رفتار bark با هم."]
        elif "آرگومان" in title or "Arguments" in title:
            code = 'def f(a, b=2, *, c=3):\n    print(a, b, c)\nf(1)\nf(1, c=9)'
            extra = ["b پیش‌فرض دارد. c فقط نام‌دار."]
        elif "حوزه" in title or "Scope" in title:
            code = 'x = "بیرون"\ndef f():\n    x = "داخل"\n    print(x)\nf()\nprint(x)'
            extra = ["داخل تابع، x جدا است."]
        elif "بازگشت" in title or "Recursion" in title:
            code = 'def fact(n):\n    if n <= 1:\n        return 1\n    return n * fact(n-1)\nprint(fact(5))'
            extra = ["تابع خودش را صدا می‌زند. شرط توقف واجب است."]
        elif "آرایه" in title and "Arrays" in title:
            code = 'from array import array\na = array("i", [1, 2, 3])\nprint(a[0])'
            extra = ["برای نوع یکسان و صرفه‌جویی حافظه. در کار روزمره لیست کافی است."]
        elif "نشانگر" in title or "Marker" in title or "خط (" in title or "برچسب" in title or "شبکه (" in title or "زیرنمودار" in title or "پراکندگی" in title or "دایره" in title:
            code = 'import matplotlib.pyplot as plt\nplt.scatter([1,2,3],[3,1,2])\nplt.grid(True)\nplt.xlabel("x")\n# plt.show()'
            extra = ["scatter نقطه. grid خط‌کشی. xlabel محور."]
        elif "Pyplot" in title or "Matplotlib" in title:
            code = 'import matplotlib.pyplot as plt\nplt.plot([1,2,3])\nplt.ylabel("مقدار")'
            extra = ["pyplot رابط ساده matplotlib است."]
        elif "رگرسیون خطی" in title:
            code = '# y ≈ mx+b\nxs=[1,2,3]\nys=[2,4,6]\nm = 2; b = 0\nprint([m*x+b for x in xs])'
            extra = ["خطی یعنی رابطه مستقیم."]
        elif "K-means" in title:
            code = '# ایده: نقطه را به نزدیک‌ترین مرکز بچسبان، مرکز را میانگین کن، تکرار کن\nprint("۲ خوشه روی داده")'
            extra = ["بدون برچسب؛ کشف گروه."]
        elif "KNN" in title:
            code = '# برای نقطه جدید، k تا نزدیک‌ترین همسایه را ببین و رأی اکثریت'
            extra = ["k فرد باشد تا تساوی کمتر شود."]
        elif "درخت تصمیم" in title:
            code = '# اگر سن>18 و درآمد>x آنگاه بله'
            extra = ["شاخه شرطی شبیه if تو در تو."]
        elif "لجستیک" in title:
            code = '# خروجی بین ۰ و ۱: احتمال کلاس'
            extra = ["برای بله/خیر."]
        elif "DSA" in title:
            code = '# ساختار داده + الگوریتم = برنامه کارآمد'
            extra = ["لیست، پشته، صف، درخت، گراف و مرتب‌سازی."]
        elif "پیوندی" in title or "Linked" in title:
            code = 'class N:\n    def __init__(self, v):\n        self.v = v\n        self.next = None\na = N(1); a.next = N(2)\nprint(a.v, a.next.v)'
            extra = ["هر گره به بعدی اشاره می‌کند."]
        elif "حبابی" in title:
            code = 'a=[3,1,2]\nfor _ in range(len(a)):\n    for i in range(len(a)-1):\n        if a[i]>a[i+1]:\n            a[i],a[i+1]=a[i+1],a[i]\nprint(a)'
            extra = ["همسایه‌ها را مقایسه و عوض کن."]
        elif "انتخابی" in title or "Selection" in title:
            code = 'a=[3,1,2]\nfor i in range(len(a)):\n    m=i\n    for j in range(i+1,len(a)):\n        if a[j]<a[m]: m=j\n    a[i],a[m]=a[m],a[i]\nprint(a)'
            extra = ["هر بار کوچک‌ترین باقی‌مانده را اول بگذار."]
        elif "درج" in title and "Insertion" in title:
            code = 'a=[3,1,2]\nfor i in range(1,len(a)):\n    key=a[i]; j=i-1\n    while j>=0 and a[j]>key:\n        a[j+1]=a[j]; j-=1\n    a[j+1]=key\nprint(a)'
            extra = ["مثل مرتب کردن کارت در دست."]
        elif "سریع" in title and "Quick" in title:
            code = 'def q(a):\n    if len(a)<=1: return a\n    p=a[-1]\n    L=[x for x in a[:-1] if x<=p]\n    R=[x for x in a[:-1] if x>p]\n    return q(L)+[p]+q(R)\nprint(q([3,1,2,4]))'
            extra = ["یک محور انتخاب کن، کوچک‌ترها چپ، بزرگ‌ترها راست."]
        elif "ادغامی" in title or "Merge Sort" in title:
            code = 'def mrg(a):\n    if len(a)<=1: return a\n    mid=len(a)//2\n    L,R=mrg(a[:mid]), mrg(a[mid:])\n    o=[]; i=j=0\n    while i<len(L) and j<len(R):\n        if L[i]<R[j]: o.append(L[i]); i+=1\n        else: o.append(R[j]); j+=1\n    return o+L[i:]+R[j:]\nprint(mrg([3,1,2]))'
            extra = ["نصف کن، مرتب کن، ادغام کن."]
        elif "شمارشی" in title or "Counting" in title:
            code = 'a=[2,1,2,0]\nc=[0]*3\nfor x in a: c[x]+=1\nout=[]\nfor i,n in enumerate(c):\n    out += [i]*n\nprint(out)'
            extra = ["وقتی بازه اعداد کوچک است سریع است."]
        elif "رادیکس" in title or "Radix" in title:
            code = '# رقم به رقم از راست مرتب کن (برای اعداد صحیح)'
            extra = ["چند پاس Counting روی رقم‌ها."]
        elif "خطی" in title and "Search" in title:
            code = 'a=[4,1,7]; x=7\nprint(next((i for i,v in enumerate(a) if v==x), -1))'
            extra = ["از اول تا آخر یکی‌یکی."]
        elif "دودویی" in title and "Search" in title:
            code = 'a=[1,3,5,7]; x=5\nlo,hi=0,len(a)-1\nans=-1\nwhile lo<=hi:\n    mid=(lo+hi)//2\n    if a[mid]==x:\n        ans=mid; break\n    if a[mid]<x: lo=mid+1\n    else: hi=mid-1\nprint(ans)'
            extra = ["لیست باید مرتب باشد."]
        elif "Create Database" in title or "ایجاد پایگاه" in title:
            code = '# CREATE DATABASE shop CHARACTER SET utf8mb4;'
            extra = ["utf8mb4 برای فارسی."]
        elif "Create Table" in title or "ایجاد جدول" in title:
            code = '# CREATE TABLE users (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50));'
            extra = ["PRIMARY KEY یکتا."]
        elif title.startswith("درج") or title == "درج رکورد (Insert)":
            code = '# INSERT INTO users (name) VALUES (%s)'
            extra = ["مقدار را با placeholder بده."]
        elif title.startswith("انتخاب") or title == "انتخاب (Select)":
            code = '# SELECT id, name FROM users;'
            extra = ["* همه ستون‌ها؛ بهتر است نام ستون را بنویسی."]
        elif "Order By" in title:
            code = '# SELECT * FROM users ORDER BY id DESC;'
            extra = ["DESC نزولی."]
        elif "خانه" in title:
            code = 'print("شروع پایتون")'
            extra = ["از درس بعد به ترتیب برو."]
        elif "مقدمه" in title:
            code = 'print("Python")'
            extra = ["زبان خوانا برای شروع."]
        elif "شروع کار" in title:
            code = 'python --version'
            extra = ["نسخه را ببین."]
        elif "سینتکس" in title or "ساختار نوشتاری" in title:
            code = 'if True:\n    print("تورفتگی")'
            extra = ["فاصله اول خط مهم است."]

        sections = [
            {"h": short, "p": f"موضوع این صفحه «{short}» است. مثال را آرام بخوان و بعد خودت عوض کن.", "code": code, "exp": extra or ["هر خط را با خروجی‌اش تطبیق بده."]},
        ]
        summary = [f"مفهوم اصلی: {short}.", "مثال را اجرا کن.", "یک ورودی را تغییر بده و دوباره ببین."]
    return rich(title, intro, sections, summary=summary, where=where)

def build_py():
    out = []
    for t in PY_TITLES:
        if t in CORE:
            kw = CORE[t]
            out.append(rich(t, kw["intro"], kw["sections"], summary=kw.get("summary"), warn=kw.get("warn"), where=kw.get("where")))
        else:
            out.append(py_auto(t))
    return out

# ---------------- CSS TITLES ----------------
CSS_TITLES = [
"خانه (HOME)","معرفی (Introduction)","نحو نگارش (Syntax)","انتخاب گرها (Selectors)","نحوه استفاده (How To)",
"توضیحات (Comments)","خطاها (Errors)","رنگ ها (Colors)","رنگ های RGB (RGB Colors)","رنگ های HEX (HEX Colors)",
"رنگ های HSL (HSL Colors)","پس زمینه (Backgrounds)","تصویر پس زمینه (Background Image)","تکرار پس زمینه (Background Repeat)",
"پیوست پس زمینه (Background Attachment)","کوتاه نویسی پس زمینه (Background Shorthand)","حاشیه ها (Borders)",
"عرض حاشیه (Border Width)","رنگ حاشیه (Border Color)","طرف های حاشیه (Border Sides)","کوتاه نویسی حاشیه (Border Shorthand)",
"حاشیه های گرد (Rounded Borders)","حاشیه بیرونی (Outline)","عرض حاشیه بیرونی (Outline Width)","رنگ حاشیه بیرونی (Outline Color)",
"کوتاه نویسی حاشیه بیرونی (Outline Shorthand)","فاصله حاشیه بیرونی (Outline Offset)","حاشیه داخلی (Padding)",
"ارتفاع و عرض (Height/Width)","مدل جعبه ای (Box Model)","متن (Text)","تراز متن (Text Alignment)",
"تزئین متن (Text Decoration)","تبدیل متن (Text Transformation)","فاصله متن (Text Spacing)","سایه متن (Text Shadow)",
"فونت ها (Fonts)","فونت های وب سیف (Web Safe Fonts)","جایگزین های فونت (Font Fallbacks)","سبک فونت (Font Style)",
"اندازه فونت (Font Size)","فونت گوگل (Google Fonts)","ترکیب فونت ها (Font Pairings)","کوتاه نویسی فونت (Font Shorthand)",
"آیکون ها (Icons)","لینک ها (Links)","فهرست ها (Lists)","جداول (Tables)","اندازه جدول (Table Size)",
"تراز جدول (Table Alignment)","استایل جدول (Table Styling)","جدول واکنش گرا (Responsive Table)",
"نمایش (Display)","حداکثر عرض (Max-width)","موقعیت دهی (Position)","شاخص Z (Z-index)","سرریز (Overflow)",
"شناور (Float)","پاک سازی (Clear)","نمونه های شناور (Float Examples)","نمایش خطی-بلوک (Inline-block)",
"تراز کردن (Align)","ترکیب کننده ها (Combinators)","شبه کلاس ها (Pseudo-classes)","شفافیت (Opacity)",
"نوار ناوبری (Navigation Bars)","ناوبری عمودی (Vertical Navbar)","ناوبری افقی (Horizontal Navbar)",
"منوهای کشویی (Dropdowns)","گالری تصاویر (Image Gallery)","تصاویر اسپریت (Image Sprites)",
"انتخاب گرهای ویژگی (Attribute Selectors)","فرم ها (Forms)","شمارنده ها (Counters)","واحدها (Units)",
"ویژگی اختصاصی سازی (Specificity)","ویژگی !important","توابع ریاضی (Math Functions)","بهینه سازی (Optimization)",
"دسترس پذیری (Accessibility)","چیدمان وب سایت (Website Layout)","گوشه های گرد (Rounded Corners)",
"تصاویر حاشیه (Border Images)","پس زمینه های چندگانه (Multiple Backgrounds)","اندازه پس زمینه (Background Size)",
"مبدأ پس زمینه (Background Origin)","برش پس زمینه (Background Clip)","کلیدواژه های رنگ (Color Keywords)",
"گرادیان ها (Gradients)","گرادیان شعاعی (Radial Gradients)","گرادیان مخروطی (Conic Gradients)",
"سایه ها (Shadows)","سایه جعبه (Box Shadow)","افکت های متن (Text Effects)","فونت های سفارشی (Custom Fonts)",
"تبدیل های دو بعدی (2D Transforms)","تبدیل های سه بعدی (3D Transforms)","انتقال ها (Transitions)",
"انیمیشن ها (Animations)","توضیحات راهنما (Tooltips)","استایل دهی تصاویر (Image Styling)","مودال تصویر (Image Modal)",
"تراز مرکز تصویر (Image Centering)","فیلترهای تصویر (Image Filters)","اشکال تصویر (Image Shapes)",
"ویژگی object-fit","ویژگی object-position","ماسک گذاری (Masking)","ماسک گرادیان (Masking-Gradients)",
"ماسک SVG (Masking-SVG)","دکمه ها (Buttons)","صفحه بندی (Pagination)","چند ستونه (Multiple Columns)",
"رابط کاربری (User Interface)","متغیرها (Variables)","بازنویسی متغیرها (Overriding Variables)",
"متغیرها و جاوااسکریپت (Variables and JavaScript)","متغیرها در Media Query (Variables in MQ)",
"ویژگی @property","اندازه جعبه (Box Sizing)","پرس وجوهای رسانه ای (Media Queries)","نمونه های MQ (MQ Examples)",
"فلکس باکس (Flexbox Intro)","ظرف فلکس (Flex Container)","آیتم های فلکس (Flex Items)","فلکس واکنش گرا (Flex Responsive)",
"شبکه (Grid Intro)","ظرف شبکه (Grid Container)","ردیف و ستون شبکه (Grid Tracks)","فاصله شبکه (Grid Gaps)",
"تراز شبکه (Grid Align)","آیتم شبکه (Grid Items)","نام گذاری آیتم (Grid Item Named)","تراز آیتم شبکه (Grid Item Align)",
"ترتیب آیتم شبکه (Grid Item Order)","چیدمان 12 ستونه (Grid 12-column Layout)","قانون @supports",
"واکنش گرا (RWD Intro)","نما (Viewport)","چیدمان شبکه واکنش گرا (RWD Grid View)",
"پرس وجوهای رسانه ای واکنش گرا (RWD Media Queries)","تصاویر واکنش گرا (RWD Images)","ویدیوهای واکنش گرا (RWD Videos)",
"چارچوب های واکنش گرا (RWD Frameworks)","قالب های واکنش گرا (RWD Templates)",
]

CSS_CORE = {}
def CC(title, **kw):
    CSS_CORE[title] = kw

CC("مدل جعبه ای (Box Model)",
   intro="هر عنصر یک جعبه است. جعبه چهار لایه دارد: محتوا (content)، فاصله داخلی (padding)، خط دور (border) و فاصله بیرونی (margin).",
   where="هر دکمه، کارت، ستون و تصویر؛ اگر عرض عجیب شد اول باکس‌مدل را چک کن.",
   sections=[
     {"h":"چهار لایه","p":"از داخل به بیرون: محتوا، padding، border، margin.","code":".box {\n  width: 300px;\n  padding: 20px;\n  border: 5px solid gray;\n  margin: 10px;\n}","exp":["width عرض محتوا است (در حالت پیش‌فرض).","padding فضای داخل تا خط.","border خود خط.","margin فاصله تا دیگران."]},
     {"h":"جمع عرض","p":"اگر box-sizing پیش‌فرض باشد، عرض کل = width + padding + border.","code":".box {\n  width: 300px;\n  padding: 20px;\n  border: 5px solid gray;\n  box-sizing: content-box;\n}","exp":["اینجا عرض دیده‌شده بیشتر از ۳۰۰ است: 300+40+10."]},
     {"h":"border-box","p":"با border-box همان width شامل padding و border می‌شود — کار روزمره راحت‌تر است.","code":"* { box-sizing: border-box; }\n.box {\n  width: 300px;\n  padding: 20px;\n  border: 5px solid gray;\n}","exp":["حالا کل جعبه ۳۰۰ پیکسل می‌ماند."]},
   ],
   warn="margin روی هم می‌افتد (collapse) بین دو بلوک عمودی؛ اگر فاصله عجیب دیدی این را به یاد بیاور.",
   summary=["محتوا + padding + border + margin.","برای کنترل عرض از border-box استفاده کن.","padding داخل است، margin بیرون."])

CC("فلکس باکس (Flexbox Intro)",
   intro="فلکس جعبه بچه‌ها را در یک راستا می‌چیند: ردیف یا ستون. برای نوار منو و وسط‌چین عالی است.",
   where="هدر، ردیف دکمه‌ها، کارت‌های کنار هم.",
   sections=[
     {"h":"ظرف","p":"display:flex روی پدر.","code":".row {\n  display: flex;\n  gap: 12px;\n  justify-content: space-between;\n  align-items: center;\n}","exp":["gap فاصله بین بچه‌ها.","justify روی محور اصلی.","align روی محور عمود."]},
     {"h":"جهت","p":"row افقی، column عمودی.","code":".col { display: flex; flex-direction: column; }","exp":["بچه‌ها زیر هم می‌آیند."]},
   ],
   summary=["فلکس روی پدر فعال می‌شود.","یک‌بعدی است (یک راستا).","برای صفحه کامل دو‌بعدی Grid را ببین."])

CC("شبکه (Grid Intro)",
   intro="گرید ردیف و ستون با هم می‌سازد. برای کل صفحه و گالری مناسب است.",
   where="چیدمان سایت، کارت محصولات.",
   sections=[
     {"h":"ستون‌ها","p":"grid-template-columns تعداد و عرض ستون.","code":".grid {\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  gap: 16px;\n}","exp":["سه ستون مساوی.","fr یعنی سهم باقی‌مانده."]},
   ],
   summary=["گرید دو‌بعدی است.","fr سهم نسبی است.","gap فاصله خط‌ها."])

def css_auto(title):
    short = title.split("(")[0].strip()
    intro = f"در CSS «{short}» ظاهر صفحه را عوض می‌کند. HTML اسکلت است؛ CSS رنگ و فاصله و چیدمان است."
    where = f"وقتی می‌خواهی «{short}» را روی صفحه اعمال کنی."
    code = "/* " + short + " */\nbody { font-family: Vazirmatn, sans-serif; }"
    extra = ["قانون = انتخاب‌گر + { ویژگی: مقدار; }"]
    if "انتخاب" in title or "Selector" in title:
        code = "p { color: #58a6ff; }\n.box { padding: 12px; }\n#main { max-width: 900px; }"
        extra = ["نام تگ.","نقطه یعنی کلاس.","# یعنی id."]
    elif "رنگ" in title or "Color" in title or "RGB" in title or "HEX" in title or "HSL" in title:
        code = "h1 { color: #79b8ff; }\np { color: rgb(200, 200, 200); }\nspan { color: hsl(210, 80%, 70%); }"
        extra = ["هگز با #.","rgb سه عدد ۰ تا ۲۵۵.","hsl رنگ، اشباع، روشنایی."]
    elif "پس زمینه" in title or "Background" in title:
        code = "body {\n  background-color: #0f1419;\n  background-image: url(\"bg.jpg\");\n  background-size: cover;\n}"
        extra = ["رنگ زیر.","تصویر.","cover کل ناحیه را می‌پوشاند."]
    elif "حاشیه" in title or "Border" in title or "Outline" in title:
        code = ".card {\n  border: 1px solid #30363d;\n  border-radius: 10px;\n  outline: 2px solid #58a6ff;\n  outline-offset: 4px;\n}"
        extra = ["border جزء جعبه است.","outline روی جعبه حساب نمی‌شود.","radius گوشه گرد."]
    elif "Padding" in title or "حاشیه داخلی" in title:
        code = ".box { padding: 16px; padding-inline: 20px; }"
        extra = ["فاصله داخل تا محتوا.","padding-inline برای راست و چپ منطقی."]
    elif "Width" in title or "Height" in title or "عرض" in title or "ارتفاع" in title or "Max-width" in title:
        code = ".wrap { width: 100%; max-width: 980px; min-height: 40vh; }"
        extra = ["max-width نمی‌گذارد در دسکتاپ خیلی پهن شود."]
    elif "Box Model" in title or "جعبه" in title or "Box Sizing" in title:
        code = "* { box-sizing: border-box; }\n.box { width: 300px; padding: 20px; border: 5px solid gray; }"
        extra = ["با border-box عرض شامل پدینگ است."]
    elif "متن" in title or "Text" in title or "تراز متن" in title:
        code = "p {\n  text-align: justify;\n  line-height: 1.9;\n  letter-spacing: 0.02em;\n  text-decoration: none;\n}"
        extra = ["تراز.","ارتفاع خط خوانایی.","فاصله حروف."]
    elif "سایه متن" in title or "Text Shadow" in title or "Text Effects" in title:
        code = "h1 { text-shadow: 0 2px 8px rgba(0,0,0,.4); }"
        extra = ["x y محو رنگ."]
    elif "فونت" in title or "Font" in title:
        code = "body {\n  font-family: Vazirmatn, Tahoma, sans-serif;\n  font-size: 16px;\n  font-weight: 400;\n}"
        extra = ["اگر اولی نبود دومی.","size اندازه.","weight ضخامت."]
    elif "لینک" in title or "Links" in title:
        code = "a { color: #58a6ff; text-decoration: none; }\na:hover { text-decoration: underline; }"
        extra = ["حالت عادی.","hover وقتی ماوس روی لینک است."]
    elif "فهرست" in title or "List" in title:
        code = "ul { list-style: none; padding: 0; }\nli { padding: 6px 0; }"
        extra = ["نقطه پیش‌فرض را بردار برای منو."]
    elif "جدول" in title or "Table" in title:
        code = "table { width: 100%; border-collapse: collapse; }\ntd, th { border: 1px solid #30363d; padding: 8px; }"
        extra = ["collapse خط‌های دوبل را یکی می‌کند."]
    elif "Display" in title or "نمایش" in title or "Inline-block" in title:
        code = ".a { display: block; }\n.b { display: inline; }\n.c { display: inline-block; }\n.d { display: none; }"
        extra = ["block تمام خط.","inline در جریان متن.","none پنهان."]
    elif "Position" in title or "موقعیت" in title:
        code = ".rel { position: relative; }\n.abs { position: absolute; top: 8px; left: 8px; }\n.fix { position: fixed; bottom: 0; }"
        extra = ["relative مرجع مطلق.","fixed به صفحه می‌چسبد."]
    elif "Z-index" in title or "شاخص" in title:
        code = ".a { position: relative; z-index: 1; }\n.b { position: relative; z-index: 5; }"
        extra = ["عدد بزرگ‌تر روی بقیه می‌آید. position لازم است."]
    elif "Overflow" in title or "سرریز" in title:
        code = ".box { max-height: 120px; overflow: auto; }"
        extra = ["اگر محتوا زیاد شد اسکرول."]
    elif "Float" in title or "شناور" in title or "Clear" in title:
        code = "img { float: right; margin: 0 0 8px 8px; }\n.clear { clear: both; }"
        extra = ["برای متن دور عکس. برای چیدمان کلی Flex/Grid بهتر است."]
    elif "Combinator" in title or "ترکیب کننده" in title:
        code = "div p { }\ndiv > p { }\ndiv + p { }\ndiv ~ p { }"
        extra = ["نسل.","فرزند مستقیم.","همسایه بعدی.","همسایه‌های بعدی."]
    elif "Pseudo" in title or "شبه" in title:
        code = "a:hover { color: white; }\nli:first-child { font-weight: 700; }\ninput:focus { outline: 2px solid #58a6ff; }"
        extra = ["حالت.","اولین بچه.","وقتی فیلد انتخاب است."]
    elif "Opacity" in title or "شفاف" in title:
        code = ".ghost { opacity: 0.6; }\n.ghost:hover { opacity: 1; }"
        extra = ["۰ نامرئی، ۱ کامل."]
    elif "Nav" in title or "ناوبری" in title or "Dropdown" in title:
        code = "nav { display: flex; gap: 12px; }\nnav a { padding: 8px 12px; }"
        extra = ["منوی افقی با فلکس."]
    elif "گالری" in title or "Gallery" in title or "Sprite" in title:
        code = ".gal { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }\n.gal img { width: 100%; }"
        extra = ["سه ستون تصویر."]
    elif "Attribute" in title or "ویژگی" in title and "Selector" in title:
        code = 'input[type="email"] { direction: ltr; }\na[target="_blank"] { color: #ffa657; }'
        extra = ["انتخاب بر اساس ویژگی HTML."]
    elif "Form" in title or "فرم" in title:
        code = "input, textarea {\n  width: 100%;\n  padding: 10px;\n  border: 1px solid #30363d;\n  background: #0d1117;\n  color: #e6edf3;\n  border-radius: 8px;\n}"
        extra = ["ورودی تمام‌عرض و خوانا."]
    elif "واحد" in title or "Units" in title:
        code = "html { font-size: 16px; }\nh1 { font-size: 1.6rem; }\n.hero { min-height: 50vh; width: 90%; }"
        extra = ["rem نسبت به ریشه.","vh ارتفاع صفحه.","% نسبت به پدر."]
    elif "Specificity" in title or "اختصاصی" in title:
        code = "p { color: gray; }\n.box p { color: #58a6ff; }\n#x { color: red; }"
        extra = ["id از کلاس قوی‌تر، کلاس از تگ قوی‌تر."]
    elif "important" in title:
        code = "p { color: red !important; }"
        extra = ["فقط وقتی مجبوری. معمولاً انتخاب‌گر را قوی‌تر کن."]
    elif "Math" in title or "ریاضی" in title:
        code = ".x { width: calc(100% - 32px); font-size: clamp(14px, 2vw, 18px); }"
        extra = ["calc حساب.","clamp حداقل، ترجیح، حداکثر."]
    elif "Gradient" in title or "گرادیان" in title:
        code = ".hero {\n  background: linear-gradient(180deg, #161b22, #0f1419);\n}"
        extra = ["از رنگ اول به دوم."]
    elif "Shadow" in title or "سایه" in title:
        code = ".card { box-shadow: 0 8px 24px rgba(0,0,0,.35); }"
        extra = ["x y محو پخش رنگ."]
    elif "Transform" in title or "تبدیل" in title:
        code = ".card:hover { transform: translateY(-4px) scale(1.02); }"
        extra = ["جابه‌جایی و کمی بزرگ شدن."]
    elif "Transition" in title or "انتقال" in title:
        code = "button { transition: opacity .2s ease, transform .2s ease; }"
        extra = ["تغییر نرم به‌جای پرش."]
    elif "Animation" in title or "انیمیشن" in title:
        code = "@keyframes fade {\n  from { opacity: 0; }\n  to { opacity: 1; }\n}\n.box { animation: fade .4s ease both; }"
        extra = ["from تا to. both ابتدا و انتها را نگه می‌دارد."]
    elif "Filter" in title or "فیلتر" in title:
        code = "img { filter: grayscale(1); }\nimg:hover { filter: none; }"
        extra = ["سیاه‌سفید تا هاور."]
    elif "object-fit" in title or "object-position" in title:
        code = "img { width: 200px; height: 120px; object-fit: cover; object-position: center; }"
        extra = ["cover برش می‌دهد تا پر شود."]
    elif "Mask" in title or "ماسک" in title:
        code = ".hero { -webkit-mask-image: linear-gradient(#000, transparent); mask-image: linear-gradient(#000, transparent); }"
        extra = ["پایین تصویر محو می‌شود."]
    elif "دکمه" in title or "Button" in title:
        code = "button {\n  background: #1f6feb;\n  color: #fff;\n  border: 0;\n  border-radius: 8px;\n  padding: 10px 16px;\n}\nbutton:hover { filter: brightness(1.1); }"
        extra = ["دکمه واضح و قابل کلیک."]
    elif "Pagination" in title or "صفحه بندی" in title:
        code = ".pages { display: flex; gap: 6px; }\n.pages a { padding: 6px 10px; border: 1px solid #30363d; }"
        extra = ["شماره صفحات کنار هم."]
    elif "Column" in title or "ستونه" in title:
        code = "article { column-count: 2; column-gap: 24px; }"
        extra = ["متن روزنامه دو ستونه."]
    elif "Variable" in title or "متغیر" in title or "@property" in title:
        code = ":root { --bg: #0f1419; --text: #e6edf3; }\nbody { background: var(--bg); color: var(--text); }"
        extra = ["-- نام متغیر. var() استفاده."]
    elif "Media" in title or "MQ" in title or "پرس وجو" in title or "واکنش" in title or "RWD" in title or "Viewport" in title:
        code = "@media (max-width: 700px) {\n  .row { flex-direction: column; }\n  body { font-size: 14px; }\n}"
        extra = ["از این عرض به پایین قوانین داخل اعمال می‌شود."]
    elif "Flex" in title or "فلکس" in title:
        code = ".row { display: flex; gap: 12px; flex-wrap: wrap; }\n.item { flex: 1 1 180px; }"
        extra = ["wrap می‌شکند. flex رشد و پایه عرض."]
    elif "Grid" in title or "شبکه" in title or "12" in title:
        code = ".g { display: grid; grid-template-columns: repeat(12, 1fr); gap: 12px; }\n.span-6 { grid-column: span 6; }"
        extra = ["۱۲ ستون. span 6 یعنی نصف."]
    elif "@supports" in title:
        code = "@supports (display: grid) {\n  .layout { display: grid; }\n}"
        extra = ["اگر مرورگر گرید داشت."]
    elif "Tooltip" in title or "راهنما" in title:
        code = ".tip { position: relative; }\n.tip:hover::after { content: attr(data-tip); position: absolute; bottom: 100%; }"
        extra = ["::after متن راهنما."]
    elif "Image" in title or "تصویر" in title or "مودال" in title:
        code = "img { max-width: 100%; height: auto; border-radius: 8px; }"
        extra = ["از ظرف بیرون نزند."]
    elif "Icons" in title or "آیکون" in title:
        code = ".icon { width: 24px; height: 24px; display: inline-block; }"
        extra = ["اندازه ثابت برای تراز."]
    elif "Accessibility" in title or "دسترس" in title:
        code = ":focus-visible { outline: 2px solid #58a6ff; outline-offset: 2px; }\n.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; }"
        extra = ["فوکوس کیبورد را پاک نکن."]
    elif "Optimization" in title or "بهینه" in title:
        code = "img { loading: lazy; }\n/* CSS را minify کن؛ انتخاب‌گر خیلی عمیق ننویس */"
        extra = ["حجم کمتر = بارگذاری سریع‌تر."]
    elif "Layout" in title or "چیدمان" in title:
        code = ".page {\n  display: grid;\n  grid-template-columns: 240px 1fr;\n  min-height: 100vh;\n}\n@media (max-width: 800px) { .page { grid-template-columns: 1fr; } }"
        extra = ["سایدبار + محتوا. موبایل یک ستون."]
    elif "Comments" in title or "توضیحات" in title:
        code = "/* این استایل موقتی است */\nbody { margin: 0; }"
        extra = ["/* */ در CSS. در خروجی صفحه دیده نمی‌شود."]
    elif "Errors" in title or "خطا" in title:
        code = "p { color: red }\n/* اگر ; نباشد ممکن است قانون بعدی هم خراب شود */"
        extra = ["نقطه‌ویرگول را فراموش نکن."]
    elif "Syntax" in title or "نحو" in title:
        code = "selector {\n  property: value;\n}"
        extra = ["آکولاد باز و بسته. هر ویژگی ; دارد."]
    elif "How To" in title or "نحوه" in title:
        code = '<link rel="stylesheet" href="style.css">'
        extra = ["فایل CSS جدا بهتر از استایل خطی است."]
    elif "خانه" in title or "معرفی" in title:
        code = "body { background: #0f1419; color: #e6edf3; }"
        extra = ["تم تاریک ساده برای شروع."]
    elif "Framework" in title or "قالب" in title or "Templates" in title:
        code = "/* چارچوب یعنی کلاس‌های آماده؛ اول CSS خام را یاد بگیر */\n.container { max-width: 1100px; margin-inline: auto; }"
        extra = ["container محتوا را وسط می‌چیند."]
    elif "Videos" in title or "ویدیو" in title:
        code = "video { width: 100%; height: auto; max-width: 720px; }"
        extra = ["مثل تصویر واکنش‌گرا."]
    elif "User Interface" in title or "رابط" in title:
        code = "button { cursor: pointer; }\n::selection { background: #1f6feb; color: #fff; }"
        extra = ["نشانگر دست روی دکمه. رنگ انتخاب متن."]
    elif "Counters" in title or "شمارنده" in title:
        code = "ol { counter-reset: n; }\nli::before { counter-increment: n; content: counter(n) \". \"; }"
        extra = ["شماره سفارشی برای لیست."]
    elif "Rounded" in title or "گرد" in title:
        code = ".ava { border-radius: 50%; width: 64px; height: 64px; object-fit: cover; }"
        extra = ["۵۰٪ دایره کامل."]
    elif "Border Image" in title or "تصاویر حاشیه" in title:
        code = ".box { border: 10px solid; border-image: url(frame.png) 30 round; }"
        extra = ["لبه از روی تصویر."]
    elif "Origin" in title or "Clip" in title and "Background" in title:
        code = ".b { background-clip: content-box; background-origin: padding-box; }"
        extra = ["کجا رنگ شروع شود و کجا بریده شود."]
    elif "align" in title.lower() or "تراز" in title:
        code = ".row { display: flex; align-items: center; justify-content: center; min-height: 40vh; }"
        extra = ["وسط افقی و عمودی."]
    elif "Gap" in title or "فاصله شبکه" in title:
        code = ".g { display: grid; gap: 12px 20px; }"
        extra = ["اول ردیف بعد ستون."]
    elif "Tracks" in title or "ردیف و ستون" in title:
        code = ".g { grid-template-columns: 200px 1fr; grid-template-rows: auto 1fr auto; }"
        extra = ["سایدبار ثابت، محتوا انعطاف، هدر/فوتر auto."]
    elif "Named" in title or "نام گذاری" in title:
        code = '.g { grid-template-areas: "h h" "s m"; }\n.header { grid-area: h; }'
        extra = ["ناحیه نام‌دار خواناتر است."]
    elif "Order" in title or "ترتیب" in title:
        code = ".item { order: 2; }"
        extra = ["ترتیب دیداری جدا از ترتیب HTML — با دسترس‌پذیری مراقب باش."]
    elif "Container" in title or "ظرف" in title:
        code = ".wrap { display: flex; }\n/* یا display:grid روی همین پدر */"
        extra = ["همیشه ویژگی چیدمان روی پدر است."]
    elif "Items" in title or "آیتم" in title:
        code = ".item { flex: 1; min-width: 0; }"
        extra = ["min-width:0 جلوی بیرون زدن متن را می‌گیرد."]

    return rich(
        title, intro,
        [{"h": short, "p": f"این ویژگی مربوط به «{short}» است. مقدار را عوض کن و در مرورگر ببین.", "code": code, "exp": extra}],
        summary=[f"{short} را روی یک مثال کوچک امتحان کن.", "اگر اثر ندیدی انتخاب‌گر یا لینک CSS را چک کن.", "رفرش سخت (Ctrl+F5) کش را خالی می‌کند."],
        where=where,
    )

def build_css():
    out = []
    for t in CSS_TITLES:
        if t in CSS_CORE:
            kw = CSS_CORE[t]
            out.append(rich(t, kw["intro"], kw["sections"], summary=kw.get("summary"), warn=kw.get("warn"), where=kw.get("where")))
        else:
            out.append(css_auto(t))
    return out

data["python"] = build_py()
data["css"] = build_css()
print("python", len(data["python"]), "css", len(data["css"]))

langs_js = json.dumps([
    {"id":"python","name":"Python","fa":"پایتون","icon":"🐍"},
    {"id":"html","name":"HTML","fa":"اچ‌تی‌ام‌ال","icon":"📄"},
    {"id":"css","name":"CSS","fa":"سی‌اس‌اس","icon":"🎨"},
    {"id":"javascript","name":"JavaScript","fa":"جاوااسکریپت","icon":"⚡"},
    {"id":"php","name":"PHP","fa":"پی‌اچ‌پی","icon":"🐘"},
], ensure_ascii=False)
lessons_js = json.dumps(data, ensure_ascii=False)

doc = '''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مدرسه برنامه‌نویسان — آموزش کامل</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700&display=swap" rel="stylesheet">
<style>''' + STYLE + '''</style>
</head>
<body>
<header>
<div class="logo">مدرسه برنامه‌نویسان <span>آموزش مستقیم و کامل</span></div>
<nav><a href="#" id="btnHome" class="active">خانه</a></nav>
</header>
<div class="wrap">
<div id="homeBlock">
<div class="hero">
<h1>پایتون · HTML · CSS · JavaScript · PHP</h1>
<p>هر درس: چیست · چند مثال · توضیح خط‌به‌خط · جمع‌بندی</p>
</div>
<div class="langs" id="langGrid"></div>
</div>
<div id="lessonArea" style="display:none">
<div class="layout">
<aside class="side" id="sideMenu"></aside>
<article class="card" id="lessonCard"></article>
</div>
</div>
</div>
<footer>مثال واقعی · بدون حاشیه · مناسب موبایل</footer>
<script>
const LANGS = ''' + langs_js + ''';
const LESSONS = ''' + lessons_js + ''';
let currentLang = null, currentIdx = 0;
const grid = document.getElementById("langGrid");
LANGS.forEach(function(L) {
  const d = document.createElement("div");
  d.className = "lang";
  const count = (LESSONS[L.id] && LESSONS[L.id].length) ? LESSONS[L.id].length : 0;
  d.innerHTML = '<span class="ic">' + L.icon + '</span><b>' + L.name + '</b><small>' + L.fa + ' · ' + count + ' درس</small>';
  d.onclick = function() { openLang(L.id); };
  grid.appendChild(d);
});
document.getElementById("btnHome").onclick = function(e) {
  e.preventDefault();
  currentLang = null;
  document.getElementById("homeBlock").style.display = "block";
  document.getElementById("lessonArea").style.display = "none";
  document.getElementById("btnHome").classList.add("active");
};
function openLang(id) {
  currentLang = id;
  currentIdx = 0;
  document.getElementById("homeBlock").style.display = "none";
  document.getElementById("lessonArea").style.display = "block";
  document.getElementById("btnHome").classList.remove("active");
  renderSide();
  renderLesson();
}
function renderSide() {
  const list = LESSONS[currentLang] || [];
  const side = document.getElementById("sideMenu");
  side.innerHTML = "<h3>درس‌ها (" + list.length + ")</h3>";
  list.forEach(function(les, i) {
    const a = document.createElement("a");
    a.href = "#";
    a.textContent = (i + 1) + ". " + les.t;
    if (i === currentIdx) a.className = "on";
    a.onclick = function(e) { e.preventDefault(); currentIdx = i; renderSide(); renderLesson(); };
    side.appendChild(a);
  });
}
function renderLesson() {
  const list = LESSONS[currentLang] || [];
  const les = list[currentIdx];
  const card = document.getElementById("lessonCard");
  if (!les) { card.innerHTML = "<p>—</p>"; return; }
  var nav = '<div class="navbtn">';
  nav += currentIdx > 0 ? '<button type="button" id="prevBtn">← قبلی</button>' : '<span></span>';
  nav += currentIdx < list.length - 1 ? '<button type="button" id="nextBtn">بعدی →</button>' : '';
  nav += '</div>';
  card.innerHTML = les.h + nav;
  var p = document.getElementById("prevBtn"), n = document.getElementById("nextBtn");
  if (p) p.onclick = function() { currentIdx--; renderSide(); renderLesson(); };
  if (n) n.onclick = function() { currentIdx++; renderSide(); renderLesson(); };
}
</script>
</body>
</html>
'''
open("/workspace/artifacts/madrase-complete.html","w",encoding="utf-8").write(doc)
open("/workspace/artifacts/madrase-test.html","w",encoding="utf-8").write(doc)
print("bytes", len(doc.encode()))
for k,v in data.items():
    print(k, len(v))
# sanity numbers lesson
nb = [x for x in data["python"] if x["t"].startswith("اعداد")][0]
print("numbers has int section", "int: اعداد صحیح" in nb["h"])
print("numbers codes", nb["h"].count('class="code"'))

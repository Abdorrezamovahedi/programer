#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Expand Python to 55+ detailed lessons with external CSS, simple Persian, W3Schools-based."""

from pathlib import Path

BASE = Path("/home/workdir/artifacts/site/zaban/python")
BASE.mkdir(parents=True, exist_ok=True)
CSS_HREF = "../../css/main.css"

# Full sidebar: 55+ items
SIDEBAR = [
  ("شروع", [
    ("index", "خانه"),
    ("intro", "پایتون چیست؟"),
    ("getstarted", "شروع کار و نصب"),
    ("syntax", "ساختار نوشتاری"),
    ("output", "خروجی با print"),
    ("comments", "توضیحات (کامنت)"),
  ]),
  ("متغیرها", [
    ("variables", "متغیرها"),
    ("variable-names", "نام‌گذاری متغیر"),
    ("multiple-values", "چند مقدار همزمان"),
    ("output-variables", "نمایش متغیر"),
    ("global-variables", "متغیر سراسری"),
  ]),
  ("انواع داده", [
    ("data-types", "انواع داده"),
    ("numbers", "اعداد"),
    ("casting", "تبدیل نوع"),
    ("strings", "رشته‌ها"),
    ("string-slicing", "برش رشته"),
    ("string-modify", "تغییر رشته"),
    ("string-concat", "ترکیب رشته"),
    ("string-format", "قالب‌بندی رشته"),
    ("string-escape", "کاراکتر فرار"),
    ("string-methods", "متدهای رشته"),
    ("booleans", "بولین"),
  ]),
  ("عملگرها", [
    ("operators", "معرفی عملگرها"),
    ("operators-arithmetic", "عملگرهای حسابی"),
    ("operators-assignment", "عملگرهای انتساب"),
    ("operators-comparison", "عملگرهای مقایسه"),
    ("operators-logical", "عملگرهای منطقی"),
    ("operators-identity", "عملگرهای هویتی"),
    ("operators-membership", "عملگرهای عضویت"),
    ("operators-bitwise", "عملگرهای بیتی"),
    ("operators-precedence", "اولویت عملگرها"),
  ]),
  ("لیست‌ها", [
    ("lists", "لیست‌ها"),
    ("lists-access", "دسترسی به آیتم"),
    ("lists-change", "تغییر آیتم"),
    ("lists-add", "افزودن آیتم"),
    ("lists-remove", "حذف آیتم"),
    ("lists-loop", "حلقه روی لیست"),
    ("lists-comprehension", "درک لیست"),
    ("lists-sort", "مرتب‌سازی"),
    ("lists-copy", "کپی لیست"),
    ("lists-join", "ادغام لیست"),
    ("lists-methods", "متدهای لیست"),
  ]),
  ("تاپل و مجموعه", [
    ("tuples", "تاپل‌ها"),
    ("tuples-access", "دسترسی به تاپل"),
    ("tuples-update", "به‌روزرسانی تاپل"),
    ("tuples-unpack", "باز کردن تاپل"),
    ("sets", "مجموعه‌ها"),
    ("sets-access", "دسترسی به مجموعه"),
    ("sets-add", "افزودن به مجموعه"),
    ("sets-methods", "متدهای مجموعه"),
  ]),
  ("دیکشنری", [
    ("dictionaries", "دیکشنری"),
    ("dict-access", "دسترسی به دیکشنری"),
    ("dict-change", "تغییر دیکشنری"),
    ("dict-add", "افزودن به دیکشنری"),
    ("dict-remove", "حذف از دیکشنری"),
    ("dict-loop", "حلقه روی دیکشنری"),
    ("dict-copy", "کپی دیکشنری"),
    ("dict-nested", "دیکشنری تودرتو"),
    ("dict-methods", "متدهای دیکشنری"),
  ]),
  ("شرط و حلقه", [
    ("if-else", "if و else"),
    ("elif", "elif"),
    ("if-nested", "شرط تودرتو"),
    ("match", "دستور match"),
    ("while", "حلقه while"),
    ("for", "حلقه for"),
    ("break-continue", "break و continue"),
  ]),
  ("توابع", [
    ("functions", "توابع"),
    ("arguments", "آرگومان‌ها"),
    ("args-kwargs", "*args و **kwargs"),
    ("return", "مقدار بازگشتی"),
    ("lambda", "لامبدا"),
    ("recursion", "بازگشت"),
    ("scope", "حوزه دسترسی"),
    ("decorators", "دکوراتور"),
  ]),
  ("شی‌گرایی", [
    ("oop", "شی‌گرایی چیست؟"),
    ("classes", "کلاس و شی"),
    ("init", "متد __init__"),
    ("self", "پارامتر self"),
    ("inheritance", "وراثت"),
    ("polymorphism", "چندریختی"),
    ("encapsulation", "کپسوله‌سازی"),
  ]),
  ("فایل و خطا", [
    ("files", "کار با فایل"),
    ("file-read", "خواندن فایل"),
    ("file-write", "نوشتن فایل"),
    ("try-except", "try و except"),
    ("modules", "ماژول‌ها"),
    ("dates", "تاریخ و زمان"),
    ("math", "ریاضی"),
    ("json", "JSON"),
    ("regex", "عبارت منظم"),
    ("pip", "مدیر بسته pip"),
    ("user-input", "ورودی کاربر"),
    ("none", "None"),
  ]),
]

def detailed(title, sections):
    """Build rich body from list of (h2, paragraphs, optional code, optional note)."""
    parts = [f"    <h1>{title}</h1>"]
    for item in sections:
        if len(item) == 2:
            h, text = item
            parts.append(f"    <h2>{h}</h2>")
            if isinstance(text, list):
                for t in text:
                    parts.append(f"    <p>{t}</p>")
            else:
                parts.append(f"    <p>{text}</p>")
        elif len(item) == 3:
            h, text, code = item
            parts.append(f"    <h2>{h}</h2>")
            if isinstance(text, list):
                for t in text:
                    parts.append(f"    <p>{t}</p>")
            else:
                parts.append(f"    <p>{text}</p>")
            parts.append(f'    <div class="code-box"><code>{code}</code></div>')
        elif len(item) == 4:
            h, text, code, note = item
            parts.append(f"    <h2>{h}</h2>")
            if isinstance(text, list):
                for t in text:
                    parts.append(f"    <p>{t}</p>")
            else:
                parts.append(f"    <p>{text}</p>")
            if code:
                parts.append(f'    <div class="code-box"><code>{code}</code></div>')
            if note:
                parts.append(f'    <div class="note">{note}</div>')
    return "\n".join(parts)

# Content dictionary - key lessons with full detail
CONTENT = {}

CONTENT["index"] = detailed("آموزش پایتون از صفر", [
  ("پایتون چیست؟", [
    "پایتون یک زبان برنامه‌نویسی است که یادگیری آن نسبتاً آسان است. خیلی از افراد برای شروع برنامه‌نویسی، پایتون را انتخاب می‌کنند.",
    "با پایتون می‌توانید برنامه بسازید، سایت طراحی کنید، داده تحلیل کنید، هوش مصنوعی یاد بگیرید و کارهای تکراری را خودکار کنید.",
  ]),
  ("چرا پایتون محبوب است؟", [
    "نحو آن ساده و شبیه زبان انسان است. کدها خوانا هستند. کتابخانه‌های زیادی برای کارهای مختلف دارد. شرکت‌های بزرگ مثل گوگل، اینستاگرام و نتفلیکس از آن استفاده می‌کنند.",
  ]),
  ("اولین برنامه", "این ساده‌ترین برنامه پایتون است. وقتی اجرا شود، متن Hello World را نشان می‌دهد:",
   'print("Hello World!")\n\nname = "Abdorreza"\nprint(name)'),
  ("مسیر یادگیری", [
    "از منوی سمت راست شروع کنید. اول متغیر و انواع داده را یاد بگیرید. بعد شرط و حلقه. بعد توابع و در نهایت کلاس و فایل.",
  ], None, "همه درس‌ها به زبان ساده نوشته شده و مثال‌ها بر اساس ساختار آموزشی W3Schools هستند."),
])

CONTENT["intro"] = detailed("پایتون چیست؟", [
  ("معرفی", [
    "پایتون در سال ۱۹۹۱ توسط شخصی به نام گیدو ون روسوم ساخته شد. هدف او این بود که زبانی بسازد که هم قدرتمند باشد و هم خواندنش آسان.",
    "امروز پایتون یکی از پرکاربردترین زبان‌های دنیاست و در رتبه‌بندی‌های محبوبیت معمولاً جزو سه تای اول است.",
  ]),
  ("کاربردها", [
    "توسعه وب با فریم‌ورک‌هایی مثل Django و Flask",
    "هوش مصنوعی و یادگیری ماشین با کتابخانه‌هایی مثل TensorFlow و scikit-learn",
    "تحلیل داده و علم داده با Pandas و NumPy",
    "اتوماسیون کارهای تکراری روی کامپیوتر",
    "ساخت بازی‌های ساده و برنامه‌های دسکتاپ",
  ]),
  ("نسخه پایتون", [
    "الان نسخه ۳ پایتون استاندارد است. نسخه ۲ دیگر پشتیبانی نمی‌شود. وقتی پایتون را نصب می‌کنید، معمولاً نسخه ۳ نصب می‌شود.",
  ]),
])

CONTENT["getstarted"] = detailed("شروع کار و نصب", [
  ("نصب پایتون", [
    "به سایت رسمی python.org بروید. نسخه مناسب سیستم‌عامل خود (ویندوز، مک یا لینوکس) را دانلود کنید.",
    "در ویندوز هنگام نصب، گزینه Add Python to PATH را حتماً تیک بزنید تا بتوانید از ترمینال استفاده کنید.",
  ]),
  ("بررسی نصب", "بعد از نصب، ترمینال یا Command Prompt را باز کنید و این دستور را بزنید:",
   "python --version\n# یا\npython3 --version"),
  ("اجرای اولین برنامه", [
    "یک فایل با نام hello.py بسازید. داخلش بنویسید: print(\"سلام\")",
    "در ترمینال بروید به پوشه همان فایل و بنویسید: python hello.py",
  ], 'print("سلام دنیا")'),
  ("ویرایشگر پیشنهادی", [
    "VS Code رایگان و قدرتمند است. می‌توانید افزونه Python را روی آن نصب کنید تا نوشتن کد راحت‌تر شود.",
  ], None, "اگر نصب درست باشد، نسخه پایتون مثلاً 3.12.x نمایش داده می‌شود."),
])

CONTENT["syntax"] = detailed("ساختار نوشتاری پایتون", [
  ("تورفتگی خیلی مهم است", [
    "در خیلی از زبان‌ها برای مشخص کردن بلوک کد از آکولاد {} استفاده می‌شود. در پایتون به جایش از فاصله یا Tab در ابتدای خط استفاده می‌کنیم. به این کار تورفتگی یا Indentation می‌گویند.",
    "اگر تورفتگی را اشتباه بگذارید، برنامه خطا می‌دهد و اجرا نمی‌شود.",
  ],
   'if 5 > 2:\n    print("پنج از دو بزرگ‌تر است")'),
  ("چند فاصله؟", [
    "معمولاً ۴ فاصله یا یک Tab استفاده می‌شود. مهم این است که در یک بلوک همه خطوط یکسان باشند.",
  ]),
  ("حساس به حروف بزرگ و کوچک", [
    "Print با print فرق دارد. نام‌ها و دستورات باید دقیقاً درست نوشته شوند.",
  ], 'print("درست")\n# Print("اشتباه")  ← خطا می‌دهد'),
])

CONTENT["output"] = detailed("خروجی با تابع print", [
  ("تابع print چیست؟", [
    "با print می‌توانید چیزی را روی صفحه نشان دهید. متن، عدد، نتیجه محاسبه و حتی متغیر.",
  ], 'print("سلام")\nprint(100)\nprint(10 + 5)'),
  ("چند چیز با هم", [
    "می‌توانید چند مقدار را با کاما جدا کنید. پایتون بین آن‌ها فاصله می‌گذارد.",
  ], 'print("نام:", "علی")\nprint("جمع =", 3 + 7)'),
  ("پارامتر sep", [
    "با sep مشخص می‌کنید بین مقادیر چه چیزی باشد.",
  ], 'print("A", "B", "C", sep="-")\n# خروجی: A-B-C'),
  ("پارامتر end", [
    "به‌طور پیش‌فرض بعد از print به خط بعد می‌رود. با end می‌توانید این را عوض کنید.",
  ], 'print("سلام", end=" ")\nprint("دنیا")\n# خروجی در یک خط: سلام دنیا'),
])

CONTENT["comments"] = detailed("توضیحات یا کامنت", [
  ("چرا کامنت؟", [
    "کامنت برای خودتان یا دیگران است تا بفهمند کد چه می‌کند. پایتون کامنت را اجرا نمی‌کند.",
  ]),
  ("کامنت تک‌خطی", [
    "از علامت # استفاده کنید. هر چیزی بعد از # تا آخر خط نادیده گرفته می‌شود.",
  ], '# این یک توضیح است\nprint("این اجرا می‌شود")  # توضیح کنار کد'),
  ("کامنت چندخطی", [
    "می‌توانید چند خط را با سه نقل‌قول بپوشانید. این هم مثل کامنت عمل می‌کند.",
  ], '"""\nاین چند خط\nتوضیح است\n"""\nprint("کد اصلی")'),
])

CONTENT["variables"] = detailed("متغیرها", [
  ("متغیر چیست؟", [
    "متغیر مثل یک جعبه است که چیزی داخلش می‌گذارید. بعداً می‌توانید آن چیز را با نام جعبه صدا بزنید.",
    "در پایتون لازم نیست از قبل بگویید متغیر چه نوعی است. با اولین مقداردهی ساخته می‌شود.",
  ], 'x = 5\ny = "علی"\nprint(x)\nprint(y)'),
  ("تغییر مقدار و نوع", [
    "می‌توانید بعداً مقدار دیگری در همان متغیر بریزید. حتی نوعش عوض شود.",
  ], 'x = 4\nprint(x)\nx = "سلام"\nprint(x)'),
  ("دیدن نوع با type", [
    "تابع type به شما می‌گوید متغیر چه نوعی دارد.",
  ], 'x = 5\nprint(type(x))  # <class \'int\'>\ny = "سلام"\nprint(type(y))  # <class \'str\'>'),
  ("تبدیل صریح یا Casting", [
    "اگر بخواهید خودتان نوع را مشخص کنید، از int و float و str استفاده کنید.",
  ], 'x = str(3)    # "3"\ny = int(3)    # 3\nz = float(3)  # 3.0'),
])

CONTENT["variable-names"] = detailed("نام‌گذاری متغیر", [
  ("قوانین نام", [
    "نام باید با حرف یا زیرخط _ شروع شود. نمی‌تواند با عدد شروع شود.",
    "فقط حروف انگلیسی، عدد و _ مجاز است. فاصله و خط تیره مجاز نیست.",
    "حروف بزرگ و کوچک فرق دارند: age با Age دو متغیر جدا هستند.",
  ]),
  ("مثال درست", None, 'myvar = 1\nmy_var = 2\n_my_var = 3\nmyVar = 4\nMYVAR = 5\nmyvar2 = 6'),
  ("مثال غلط", None, '# 2myvar = 1   اشتباه\n# my-var = 1   اشتباه\n# my var = 1   اشتباه'),
  ("سبک پیشنهادی پایتون", [
    "در پایتون معمولاً از snake_case استفاده می‌شود: یعنی کلمات با زیرخط جدا می‌شوند و همه حروف کوچک‌اند.",
  ], 'user_name = "علی"\ntotal_price = 1500\nis_active = True',
   "این سبک در راهنمای رسمی پایتون (PEP 8) پیشنهاد شده است."),
])

CONTENT["multiple-values"] = detailed("اختصاص چند مقدار", [
  ("چند مقدار به چند متغیر", [
    "می‌توانید در یک خط چند متغیر را مقداردهی کنید.",
  ], 'x, y, z = "نارنجی", "موز", "گیلاس"\nprint(x)\nprint(y)\nprint(z)'),
  ("یک مقدار به چند متغیر", [
    "اگر همه باید یک مقدار داشته باشند:",
  ], 'x = y = z = "نارنجی"\nprint(x)\nprint(y)\nprint(z)'),
  ("باز کردن لیست یا تاپل", [
    "اگر تعداد متغیرها با تعداد آیتم‌ها یکی باشد، می‌توانید لیست را باز کنید.",
  ], 'fruits = ["سیب", "موز", "گیلاس"]\nx, y, z = fruits\nprint(x)\nprint(y)\nprint(z)'),
])

CONTENT["output-variables"] = detailed("نمایش متغیرها", [
  ("با print", [
    "ساده‌ترین راه print است. می‌توانید متن و متغیر را با هم چاپ کنید.",
  ], 'x = "پایتون"\nprint("من دارم " + x + " یاد می‌گیرم")\nprint("من دارم", x, "یاد می‌گیرم")'),
  ("با f-string", [
    "روش مدرن و خوانا این است که از f قبل از رشته استفاده کنید و متغیر را داخل {} بگذارید.",
  ], 'name = "علی"\nage = 20\nprint(f"نام من {name} است و {age} سال دارم")'),
])

CONTENT["global-variables"] = detailed("متغیر سراسری", [
  ("متغیر بیرون تابع", [
    "متغیری که بیرون تابع تعریف شود، سراسری است و داخل توابع هم دیده می‌شود.",
  ], 'x = "عالی"\n\ndef myfunc():\n    print("پایتون " + x)\n\nmyfunc()'),
  ("متغیر داخل تابع", [
    "اگر داخل تابع همان نام را دوباره مقدار بدهید، آن متغیر محلی می‌شود و فقط داخل همان تابع معتبر است.",
  ], 'x = "عالی"\n\ndef myfunc():\n    x = "فوق‌العاده"\n    print("پایتون " + x)\n\nmyfunc()\nprint("پایتون " + x)'),
  ("کلمه global", [
    "اگر بخواهید داخل تابع متغیر سراسری را عوض کنید، باید بنویسید global.",
  ], 'x = "عالی"\n\ndef myfunc():\n    global x\n    x = "فوق‌العاده"\n\nmyfunc()\nprint("پایتون " + x)'),
])

CONTENT["data-types"] = detailed("انواع داده", [
  ("چرا نوع مهم است؟", [
    "هر نوع داده کار خاصی می‌کند. مثلاً روی عدد می‌توانید ضرب کنید، روی متن معمولاً نه. پایتون خودش نوع را از روی مقدار می‌فهمد.",
  ]),
  ("انواع اصلی", [
    "متن: str",
    "عدد: int (صحیح)، float (اعشار)، complex (مختلط)",
    "دنباله: list، tuple، range",
    "نگاشت: dict",
    "مجموعه: set، frozenset",
    "بولین: bool",
    "خالی: NoneType",
  ]),
  ("مثال", None, 'x = "سلام"       # str\nx = 20           # int\nx = 20.5         # float\nx = ["a", "b"]   # list\nx = ("a", "b")   # tuple\nx = {"name": "Ali"}  # dict\nx = True         # bool\nx = None         # NoneType'),
  ("دیدن نوع", None, 'print(type(20))\nprint(type("سلام"))\nprint(type([1, 2, 3]))'),
])

CONTENT["numbers"] = detailed("اعداد در پایتون", [
  ("سه نوع عدد", [
    "int برای عدد صحیح، float برای اعشار، complex برای عدد مختلط.",
  ], 'x = 1        # int\ny = 2.8      # float\nz = 1j       # complex\nprint(type(x))\nprint(type(y))\nprint(type(z))'),
  ("عدد صحیح خیلی بزرگ", [
    "در پایتون int محدودیت اندازه ندارد و می‌تواند خیلی بزرگ باشد.",
  ], 'x = 35656222554887711\nprint(x)'),
  ("تبدیل بین انواع", None, 'x = 1\ny = 2.8\nprint(float(x))   # 1.0\nprint(int(y))     # 2\nprint(complex(x)) # (1+0j)'),
  ("اعداد تصادفی", [
    "برای عدد تصادفی باید ماژول random را وارد کنید.",
  ], 'import random\nprint(random.randrange(1, 10))'),
])

CONTENT["casting"] = detailed("تبدیل نوع داده", [
  ("چرا تبدیل؟", [
    "گاهی مقدار به صورت متن است ولی شما عدد می‌خواهید، یا برعکس. با int و float و str تبدیل می‌کنید.",
  ]),
  ("به عدد صحیح", None, 'x = int(1)      # 1\ny = int(2.8)    # 2\nz = int("3")    # 3'),
  ("به اعشار", None, 'x = float(1)      # 1.0\ny = float(2.8)    # 2.8\nz = float("3")    # 3.0\nw = float("4.2")  # 4.2'),
  ("به رشته", None, 'x = str("s1")\ny = str(2)\nz = str(3.0)\nprint(x, y, z)'),
])

CONTENT["strings"] = detailed("رشته‌ها", [
  ("رشته چیست؟", [
    "رشته یعنی متن. در پایتون متن را بین نقل‌قول تکی یا دوتایی می‌گذارید.",
  ], 'print("سلام")\nprint(\'سلام\')'),
  ("رشته چندخطی", [
    "برای چند خط از سه نقل‌قول استفاده کنید.",
  ], 'a = """این یک متن\nچند خطی است\nدر پایتون"""\nprint(a)'),
  ("رشته مثل آرایه", [
    "می‌توانید با ایندکس به کاراکترها دسترسی داشته باشید. ایندکس از صفر شروع می‌شود.",
  ], 'a = "Hello"\nprint(a[1])  # e'),
  ("طول رشته", None, 'a = "Hello World"\nprint(len(a))  # 11'),
  ("بررسی وجود کلمه", None, 'txt = "بهترین چیزهای زندگی رایگان هستند"\nprint("رایگان" in txt)  # True\nif "رایگان" in txt:\n    print("بله، هست")'),
])

CONTENT["string-slicing"] = detailed("برش رشته", [
  ("برش چیست؟", [
    "می‌توانید بخشی از رشته را جدا کنید. از ایندکس شروع تا قبل از ایندکس پایان.",
  ], 'b = "Hello, World!"\nprint(b[2:5])  # llo'),
  ("از اول", None, 'print(b[:5])  # Hello'),
  ("تا آخر", None, 'print(b[2:])  # llo, World!'),
  ("ایندکس منفی", [
    "از آخر می‌شمارد. ۱- یعنی آخرین کاراکتر.",
  ], 'print(b[-5:-2])  # orl'),
])

CONTENT["string-modify"] = detailed("تغییر رشته", [
  ("حروف بزرگ و کوچک", None, 'a = "Hello, World!"\nprint(a.upper())  # HELLO, WORLD!\nprint(a.lower())  # hello, world!'),
  ("حذف فاصله اضافه", None, 'a = " Hello, World! "\nprint(a.strip())  # Hello, World!'),
  ("جایگزینی", None, 'a = "Hello, World!"\nprint(a.replace("H", "J"))  # Jello, World!'),
  ("تقسیم به لیست", None, 'a = "Hello, World!"\nprint(a.split(","))  # [\'Hello\', \' World!\']'),
])

CONTENT["string-concat"] = detailed("ترکیب رشته‌ها", [
  ("با علامت به علاوه", None, 'a = "Hello"\nb = "World"\nc = a + " " + b\nprint(c)  # Hello World'),
  ("با f-string", [
    "روش تمیزتر و پیشنهادی همین است.",
  ], 'a = "Hello"\nb = "World"\nprint(f"{a} {b}")'),
])

CONTENT["string-format"] = detailed("قالب‌بندی رشته", [
  ("f-string", [
    "قبل از نقل‌قول f بگذارید و متغیر را داخل آکولاد بنویسید.",
  ], 'name = "علی"\nage = 25\nprint(f"نام: {name}، سن: {age}")\nprint(f"سال بعد: {age + 1}")'),
  ("متد format", None, 'txt = "نام من {} است و {} سال دارم"\nprint(txt.format("علی", 25))'),
])

CONTENT["string-escape"] = detailed("کاراکتر فرار", [
  ("چرا لازم است؟", [
    "اگر داخل رشته نقل‌قول هم‌نوع بخواهید، یا خط جدید، از کاراکتر فرار استفاده می‌کنید.",
  ], 'txt = "ما از آن به عنوان \\"نقل‌قول\\" یاد می‌کنیم"\nprint(txt)\nprint("خط اول\\nخط دوم")\nprint("فاصله\\tبا تب")'),
])

CONTENT["string-methods"] = detailed("متدهای پرکاربرد رشته", [
  ("چند متد مهم", None, 'a = "Hello"\nprint(a.startswith("He"))  # True\nprint(a.endswith("lo"))    # True\nprint(a.find("l"))         # 2\nprint(a.count("l"))        # 2\nprint("hello".capitalize()) # Hello\nprint("hello world".title()) # Hello World\nprint("hello".isalpha())   # True\nprint("123".isdigit())     # True'),
])

CONTENT["booleans"] = detailed("بولین", [
  ("True و False", [
    "بولین فقط دو مقدار دارد: درست یا غلط. در شرط‌ها و مقایسه‌ها خیلی استفاده می‌شود.",
  ], 'print(10 > 9)   # True\nprint(10 == 9)  # False\nprint(10 < 9)   # False'),
  ("تابع bool", [
    "تقریباً هر مقداری را می‌توان به بولین تبدیل کرد. خالی‌ها و صفر False هستند.",
  ], 'print(bool("سلام"))  # True\nprint(bool(15))      # True\nprint(bool(""))      # False\nprint(bool(0))       # False\nprint(bool([]))      # False\nprint(bool(None))    # False'),
])

# Operators
CONTENT["operators"] = detailed("معرفی عملگرها", [
  ("عملگر چیست؟", [
    "عملگرها روی مقادیر کار می‌کنند. مثلاً جمع، مقایسه، یا منطقی.",
  ]),
  ("دسته‌ها", [
    "حسابی: + - * / // % **",
    "انتساب: = += -= و غیره",
    "مقایسه: == != > < >= <=",
    "منطقی: and or not",
    "هویتی: is is not",
    "عضویت: in not in",
    "بیتی: روی بیت‌های عدد",
  ]),
])

CONTENT["operators-arithmetic"] = detailed("عملگرهای حسابی", [
  ("عملیات اصلی", None, 'x = 10\ny = 3\nprint(x + y)   # 13 جمع\nprint(x - y)   # 7 تفریق\nprint(x * y)   # 30 ضرب\nprint(x / y)   # 3.333 تقسیم\nprint(x % y)   # 1 باقی‌مانده\nprint(x ** y)  # 1000 توان\nprint(x // y)  # 3 تقسیم صحیح'),
])

CONTENT["operators-assignment"] = detailed("عملگرهای انتساب", [
  ("کوتاه‌نویسی", [
    "به‌جای x = x + 3 می‌نویسید x += 3.",
  ], 'x = 5\nx += 3   # 8\nx -= 2   # 6\nx *= 2   # 12\nx /= 3   # 4.0\nx %= 3   # 1.0'),
])

CONTENT["operators-comparison"] = detailed("عملگرهای مقایسه", [
  ("نتیجه همیشه بولین است", None, 'x = 5\ny = 3\nprint(x == y)  # False\nprint(x != y)  # True\nprint(x > y)   # True\nprint(x < y)   # False\nprint(x >= y)  # True\nprint(x <= y)  # False'),
])

CONTENT["operators-logical"] = detailed("عملگرهای منطقی", [
  ("and or not", None, 'x = 5\nprint(x > 3 and x < 10)  # True\nprint(x > 3 or x < 4)    # True\nprint(not(x > 3 and x < 10))  # False',
   "and وقتی درست است که هر دو طرف درست باشند. or وقتی یکی درست باشد. not نتیجه را برعکس می‌کند."),
])

CONTENT["operators-identity"] = detailed("عملگرهای هویتی", [
  ("is و is not", [
    "بررسی می‌کند دو متغیر به یک شی یکسان اشاره می‌کنند یا نه. با == فرق دارد که فقط مقدار را مقایسه می‌کند.",
  ], 'x = ["سیب", "موز"]\ny = ["سیب", "موز"]\nz = x\nprint(x is z)      # True\nprint(x is y)      # False\nprint(x == y)      # True'),
])

CONTENT["operators-membership"] = detailed("عملگرهای عضویت", [
  ("in و not in", [
    "بررسی می‌کند آیا چیزی داخل یک دنباله هست یا نه.",
  ], 'fruits = ["سیب", "موز"]\nprint("موز" in fruits)       # True\nprint("گیلاس" not in fruits) # True'),
])

CONTENT["operators-bitwise"] = detailed("عملگرهای بیتی", [
  ("روی بیت‌ها", [
    "این عملگرها روی نمایش دودویی اعداد کار می‌کنند. در برنامه‌نویسی سطح پایین و بعضی بهینه‌سازی‌ها استفاده می‌شوند.",
  ], 'print(6 & 3)   # 2  AND\nprint(6 | 3)   # 7  OR\nprint(6 ^ 3)   # 5  XOR\nprint(~6)      # -7 NOT\nprint(3 << 2)  # 12 شیفت چپ\nprint(8 >> 2)  # 2  شیفت راست'),
])

CONTENT["operators-precedence"] = detailed("اولویت عملگرها", [
  ("ترتیب اجرا", [
    "مثل ریاضی، اول توان، بعد ضرب و تقسیم، بعد جمع و تفریق. برای عوض کردن ترتیب از پرانتز استفاده کنید.",
  ], 'print(5 + 4 * 3)    # 17\nprint((5 + 4) * 3)  # 27'),
])

# Lists family
CONTENT["lists"] = detailed("لیست‌ها", [
  ("لیست چیست؟", [
    "لیست مجموعه‌ای مرتب از آیتم‌هاست. می‌توانید بعداً عوضش کنید، چیزی اضافه یا حذف کنید. آیتم تکراری هم مجاز است.",
  ], 'thislist = ["سیب", "موز", "گیلاس"]\nprint(thislist)\nprint(len(thislist))\nprint(type(thislist))'),
  ("سازنده list", None, 'thislist = list(("سیب", "موز", "گیلاس"))\nprint(thislist)'),
  ("انواع مختلف در یک لیست", None, 'list1 = ["abc", 34, True, 40, "male"]\nprint(list1)'),
])

CONTENT["lists-access"] = detailed("دسترسی به آیتم لیست", [
  ("با ایندکس", [
    "ایندکس از صفر شروع می‌شود.",
  ], 'thislist = ["سیب", "موز", "گیلاس"]\nprint(thislist[1])   # موز\nprint(thislist[-1])  # گیلاس'),
  ("برش", None, 'print(thislist[1:3])  # [\'موز\', \'گیلاس\']\nprint(thislist[:2])\nprint(thislist[1:])'),
  ("بررسی وجود", None, 'if "سیب" in thislist:\n    print("بله، سیب هست")'),
])

CONTENT["lists-change"] = detailed("تغییر آیتم لیست", [
  ("یک آیتم", None, 'thislist = ["سیب", "موز", "گیلاس"]\nthislist[1] = "تمشک"\nprint(thislist)'),
  ("چند آیتم", None, 'thislist[1:3] = ["تمشک", "هندوانه"]\nprint(thislist)'),
])

CONTENT["lists-add"] = detailed("افزودن به لیست", [
  ("append", None, 'thislist = ["سیب", "موز"]\nthislist.append("گیلاس")\nprint(thislist)'),
  ("insert", None, 'thislist.insert(1, "پرتقال")\nprint(thislist)'),
  ("extend", None, 'thislist = ["سیب", "موز"]\ntropical = ["انبه", "آناناس"]\nthislist.extend(tropical)\nprint(thislist)'),
])

CONTENT["lists-remove"] = detailed("حذف از لیست", [
  ("remove و pop", None, 'thislist = ["سیب", "موز", "گیلاس"]\nthislist.remove("موز")\nthislist.pop(0)\nprint(thislist)'),
  ("del و clear", None, 'thislist = ["سیب", "موز", "گیلاس"]\ndel thislist[0]\nthislist.clear()\nprint(thislist)'),
])

CONTENT["lists-loop"] = detailed("حلقه روی لیست", [
  ("for", None, 'thislist = ["سیب", "موز", "گیلاس"]\nfor x in thislist:\n    print(x)'),
  ("با ایندکس", None, 'for i in range(len(thislist)):\n    print(thislist[i])'),
  ("while", None, 'i = 0\nwhile i < len(thislist):\n    print(thislist[i])\n    i += 1'),
])

CONTENT["lists-comprehension"] = detailed("درک لیست (List Comprehension)", [
  ("ساخت لیست کوتاه", [
    "یک روش کوتاه برای ساخت لیست جدید از روی لیست دیگر است.",
  ], 'fruits = ["سیب", "موز", "گیلاس", "کیوی"]\nnewlist = [x for x in fruits if "ا" in x]\nprint(newlist)\n\nnewlist = [x.upper() for x in fruits]\nprint(newlist)'),
])

CONTENT["lists-sort"] = detailed("مرتب‌سازی لیست", [
  ("sort", None, 'thislist = ["پرتقال", "انبه", "کیوی", "آناناس"]\nthislist.sort()\nprint(thislist)\nthislist.sort(reverse=True)\nprint(thislist)'),
  ("عدد", None, 'thislist = [100, 50, 65, 82, 23]\nthislist.sort()\nprint(thislist)'),
])

CONTENT["lists-copy"] = detailed("کپی لیست", [
  ("چرا copy؟", [
    "اگر بنویسید list2 = list1 هر دو به یک لیست اشاره می‌کنند. برای کپی واقعی از copy استفاده کنید.",
  ], 'thislist = ["سیب", "موز"]\nmylist = thislist.copy()\n# یا\nmylist = list(thislist)'),
])

CONTENT["lists-join"] = detailed("ادغام لیست‌ها", [
  ("چند روش", None, 'list1 = ["a", "b"]\nlist2 = ["c", "d"]\nlist3 = list1 + list2\nprint(list3)\n\nlist1.extend(list2)\nprint(list1)'),
])

CONTENT["lists-methods"] = detailed("متدهای لیست", [
  ("خلاصه متدها", [
    "append، clear، copy، count، extend، index، insert، pop، remove، reverse، sort",
  ], 'nums = [3, 1, 4, 1, 5]\nprint(nums.count(1))\nprint(nums.index(4))\nnums.reverse()\nprint(nums)'),
])

# Tuples & Sets
CONTENT["tuples"] = detailed("تاپل‌ها", [
  ("تاپل چیست؟", [
    "تاپل مثل لیست است ولی بعد از ساخته شدن نمی‌توانید عوضش کنید. برای داده‌هایی که نباید تغییر کنند مناسب است.",
  ], 'thistuple = ("سیب", "موز", "گیلاس")\nprint(thistuple)\nprint(len(thistuple))'),
  ("تاپل تک‌عضوی", [
    "حتماً بعد از آیتم کاما بگذارید وگرنه تاپل حساب نمی‌شود.",
  ], 'thistuple = ("سیب",)\nprint(type(thistuple))\n# thistuple = ("سیب")  ← این str است نه tuple'),
])

CONTENT["tuples-access"] = detailed("دسترسی به تاپل", [
  ("مثل لیست", None, 'thistuple = ("سیب", "موز", "گیلاس")\nprint(thistuple[1])\nprint(thistuple[-1])\nprint(thistuple[1:3])'),
])

CONTENT["tuples-update"] = detailed("به‌روزرسانی تاپل", [
  ("راه‌حل", [
    "مستقیماً نمی‌شود عوض کرد. می‌توانید به لیست تبدیل کنید، عوض کنید، دوباره تاپل کنید.",
  ], 'x = ("سیب", "موز", "گیلاس")\ny = list(x)\ny[1] = "کیوی"\nx = tuple(y)\nprint(x)'),
])

CONTENT["tuples-unpack"] = detailed("باز کردن تاپل", [
  ("Unpack", None, 'fruits = ("سیب", "موز", "گیلاس")\n(x, y, z) = fruits\nprint(x)\nprint(y)\nprint(z)'),
  ("با ستاره", None, 'fruits = ("سیب", "موز", "گیلاس", "تمشک")\n(x, y, *z) = fruits\nprint(x)\nprint(y)\nprint(z)'),
])

CONTENT["sets"] = detailed("مجموعه‌ها", [
  ("مجموعه چیست؟", [
    "مجموعه نامرتب است، ایندکس ندارد و آیتم تکراری قبول نمی‌کند. برای حذف تکراری‌ها و عملیات ریاضی مجموعه مفید است.",
  ], 'thisset = {"سیب", "موز", "گیلاس"}\nprint(thisset)\nprint(len(thisset))'),
])

CONTENT["sets-access"] = detailed("دسترسی به مجموعه", [
  ("حلقه و in", None, 'thisset = {"سیب", "موز", "گیلاس"}\nfor x in thisset:\n    print(x)\nprint("موز" in thisset)'),
])

CONTENT["sets-add"] = detailed("افزودن به مجموعه", [
  ("add و update", None, 'thisset = {"سیب", "موز"}\nthisset.add("پرتقال")\ntropical = {"انبه", "آناناس"}\nthisset.update(tropical)\nprint(thisset)'),
])

CONTENT["sets-methods"] = detailed("متدها و عملیات مجموعه", [
  ("حذف و عملیات", None, 'a = {1, 2, 3}\nb = {3, 4, 5}\nprint(a | b)  # اتحاد\nprint(a & b)  # اشتراک\nprint(a - b)  # تفاضل\na.remove(2)\na.discard(9)  # اگر نبود خطا نمی‌دهد'),
])

# Dictionaries
CONTENT["dictionaries"] = detailed("دیکشنری", [
  ("دیکشنری چیست؟", [
    "دیکشنری داده را به صورت جفت کلید و مقدار نگه می‌دارد. کلیدها یکتا هستند. از پایتون ۳.۷ به بعد ترتیب درج حفظ می‌شود.",
  ], 'thisdict = {\n  "brand": "Ford",\n  "model": "Mustang",\n  "year": 1964\n}\nprint(thisdict)\nprint(thisdict["brand"])'),
])

CONTENT["dict-access"] = detailed("دسترسی به دیکشنری", [
  ("چند روش", None, 'thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}\nprint(thisdict["model"])\nprint(thisdict.get("model"))\nprint(thisdict.keys())\nprint(thisdict.values())\nprint(thisdict.items())'),
])

CONTENT["dict-change"] = detailed("تغییر دیکشنری", [
  ("تغییر مقدار", None, 'thisdict = {"brand": "Ford", "year": 1964}\nthisdict["year"] = 2020\nthisdict.update({"year": 2021})\nprint(thisdict)'),
])

CONTENT["dict-add"] = detailed("افزودن به دیکشنری", [
  ("کلید جدید", None, 'thisdict = {"brand": "Ford", "year": 1964}\nthisdict["color"] = "قرمز"\nthisdict.update({"color": "آبی"})\nprint(thisdict)'),
])

CONTENT["dict-remove"] = detailed("حذف از دیکشنری", [
  ("pop و del", None, 'thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}\nthisdict.pop("model")\ndel thisdict["year"]\nthisdict.clear()\nprint(thisdict)'),
])

CONTENT["dict-loop"] = detailed("حلقه روی دیکشنری", [
  ("کلید و مقدار", None, 'thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}\nfor x in thisdict:\n    print(x)\nfor x in thisdict.values():\n    print(x)\nfor k, v in thisdict.items():\n    print(k, v)'),
])

CONTENT["dict-copy"] = detailed("کپی دیکشنری", [
  ("copy", None, 'thisdict = {"brand": "Ford", "year": 1964}\nmydict = thisdict.copy()\n# یا\nmydict = dict(thisdict)'),
])

CONTENT["dict-nested"] = detailed("دیکشنری تودرتو", [
  ("دیکشنری داخل دیکشنری", [
    "می‌توانید مقدار یک کلید خودش یک دیکشنری باشد.",
  ], 'myfamily = {\n  "child1": {"name": "Emil", "year": 2004},\n  "child2": {"name": "Tobias", "year": 2007},\n  "child3": {"name": "Linus", "year": 2011}\n}\nprint(myfamily["child2"]["name"])'),
])

CONTENT["dict-methods"] = detailed("متدهای دیکشنری", [
  ("خلاصه", [
    "clear، copy، fromkeys، get، items، keys، pop، popitem، setdefault، update، values",
  ]),
])

# Control flow
CONTENT["if-else"] = detailed("if و else", [
  ("شرط ساده", [
    "اگر شرط درست باشد، بلوک if اجرا می‌شود.",
  ], 'a = 33\nb = 200\nif b > a:\n    print("b از a بزرگ‌تر است")'),
  ("else", None, 'a = 200\nb = 33\nif b > a:\n    print("b بزرگ‌تر")\nelse:\n    print("a بزرگ‌تر یا مساوی")'),
  ("شرط یک‌خطی", None, 'a = 2\nb = 330\nprint("A") if a > b else print("B")'),
])

CONTENT["elif"] = detailed("elif", [
  ("چند شرط پشت سر هم", [
    "elif یعنی وگرنه اگر. می‌توانید چند تا پشت سر هم بگذارید.",
  ], 'a = 33\nb = 33\nif b > a:\n    print("b بزرگ‌تر")\nelif a == b:\n    print("برابر هستند")\nelse:\n    print("a بزرگ‌تر")'),
])

CONTENT["if-nested"] = detailed("شرط تودرتو", [
  ("if داخل if", None, 'x = 41\nif x > 10:\n    print("بالای ده")\n    if x > 20:\n        print("و بالای بیست هم هست")\n    else:\n        print("ولی بالای بیست نیست")'),
])

CONTENT["match"] = detailed("دستور match", [
  ("از پایتون ۳.۱۰", [
    "مشابه switch در زبان‌های دیگر. مقدار را با چند حالت مقایسه می‌کند.",
  ], 'day = 4\nmatch day:\n    case 1:\n        print("شنبه")\n    case 2:\n        print("یکشنبه")\n    case 3 | 4 | 5:\n        print("وسط هفته")\n    case _:\n        print("روز دیگر")'),
])

CONTENT["while"] = detailed("حلقه while", [
  ("تا وقتی شرط درست است", None, 'i = 1\nwhile i < 6:\n    print(i)\n    i += 1'),
  ("break", None, 'i = 1\nwhile i < 6:\n    print(i)\n    if i == 3:\n        break\n    i += 1'),
  ("continue", None, 'i = 0\nwhile i < 6:\n    i += 1\n    if i == 3:\n        continue\n    print(i)'),
])

CONTENT["for"] = detailed("حلقه for", [
  ("روی لیست و رشته", None, 'fruits = ["سیب", "موز", "گیلاس"]\nfor x in fruits:\n    print(x)\n\nfor x in "موز":\n    print(x)'),
  ("range", None, 'for x in range(6):\n    print(x)  # 0 تا 5\nfor x in range(2, 6):\n    print(x)\nfor x in range(2, 30, 3):\n    print(x)'),
  ("else در for", None, 'for x in range(3):\n    print(x)\nelse:\n    print("تمام شد")'),
])

CONTENT["break-continue"] = detailed("break و continue", [
  ("break", [
    "حلقه را کاملاً قطع می‌کند.",
  ], 'for x in range(10):\n    if x == 5:\n        break\n    print(x)'),
  ("continue", [
    "فقط همان دور را رد می‌کند و دور بعد را ادامه می‌دهد.",
  ], 'for x in range(6):\n    if x == 3:\n        continue\n    print(x)'),
])

# Functions
CONTENT["functions"] = detailed("توابع", [
  ("تابع چیست؟", [
    "تابع یک تکه کد است که یک کار مشخص می‌کند. فقط وقتی صدا بزنید اجرا می‌شود. برای جلوگیری از تکرار کد خیلی مفید است.",
  ], 'def my_function():\n    print("سلام از داخل تابع")\n\nmy_function()'),
])

CONTENT["arguments"] = detailed("آرگومان‌ها", [
  ("پارامتر و آرگومان", [
    "وقتی تابع را تعریف می‌کنید نام‌ها پارامتر هستند. وقتی صدا می‌زنید، مقادیری که می‌دهید آرگومان هستند.",
  ], 'def greet(name):\n    print("سلام", name)\n\ngreet("علی")\ngreet("سارا")'),
  ("مقدار پیش‌فرض", None, 'def greet(name="مهمان"):\n    print("سلام", name)\n\ngreet()\ngreet("رضا")'),
])

CONTENT["args-kwargs"] = detailed("*args و **kwargs", [
  ("*args", [
    "اگر تعداد آرگومان‌ها معلوم نباشد، با *args همه را به صورت تاپل می‌گیرید.",
  ], 'def my_function(*kids):\n    print("کوچک‌ترین:", kids[-1])\n\nmy_function("Emil", "Tobias", "Linus")'),
  ("**kwargs", [
    "برای آرگومان‌های نام‌دار با تعداد نامعلوم، دیکشنری می‌سازد.",
  ], 'def my_function(**kid):\n    print("نام خانوادگی:", kid["lname"])\n\nmy_function(fname="Tobias", lname="Refsnes")'),
])

CONTENT["return"] = detailed("مقدار بازگشتی", [
  ("return", [
    "با return نتیجه را به بیرون تابع می‌فرستید.",
  ], 'def add(a, b):\n    return a + b\n\nresult = add(3, 5)\nprint(result)\nprint(add(10, 20))'),
])

CONTENT["lambda"] = detailed("لامبدا", [
  ("تابع یک‌خطی", [
    "لامبدا یک تابع کوچک بدون نام است. برای کار کوتاه مناسب است.",
  ], 'x = lambda a: a + 10\nprint(x(5))\n\nx = lambda a, b: a * b\nprint(x(5, 6))'),
])

CONTENT["recursion"] = detailed("بازگشت (Recursion)", [
  ("تابع خودش را صدا بزند", [
    "بازگشت یعنی تابع خودش را صدا بزند. باید شرط توقف داشته باشید وگرنه بی‌نهایت ادامه می‌دهد.",
  ], 'def factorial(n):\n    if n == 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))  # 120'),
])

CONTENT["scope"] = detailed("حوزه دسترسی", [
  ("محلی و سراسری", [
    "متغیر داخل تابع محلی است. بیرون تابع سراسری. برای تغییر سراسری از داخل تابع از global استفاده کنید.",
  ], 'x = 300\n\ndef myfunc():\n    global x\n    x = 200\n\nmyfunc()\nprint(x)'),
])

CONTENT["decorators"] = detailed("دکوراتور", [
  ("تابع دور تابع", [
    "دکوراتور تابعی است که تابع دیگری را می‌گیرد و رفتارش را گسترش می‌دهد بدون اینکه خود آن تابع را عوض کند.",
  ], 'def my_decorator(func):\n    def wrapper():\n        print("قبل")\n        func()\n        print("بعد")\n    return wrapper\n\n@my_decorator\ndef say_hello():\n    print("سلام")\n\nsay_hello()'),
])

# OOP
CONTENT["oop"] = detailed("شی‌گرایی چیست؟", [
  ("مفهوم", [
    "در برنامه‌نویسی شی‌گرا، شما «اشیاء» می‌سازید که هم داده دارند و هم رفتار. کلاس قالب آن شی است.",
    "مزیت‌ها: کد مرتب‌تر، قابل استفاده مجدد، و نزدیک به مدل دنیای واقعی.",
  ]),
])

CONTENT["classes"] = detailed("کلاس و شی", [
  ("تعریف کلاس", None, 'class MyClass:\n    x = 5\n\np1 = MyClass()\nprint(p1.x)'),
  ("مثال واقعی‌تر", None, 'class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\n    def greet(self):\n        print("سلام، من", self.name, "هستم")\n\np1 = Person("علی", 25)\np1.greet()'),
])

CONTENT["init"] = detailed("متد __init__", [
  ("سازنده", [
    "وقتی شی می‌سازید، __init__ خودکار اجرا می‌شود. معمولاً برای مقداردهی اولیه ویژگی‌ها استفاده می‌شود.",
  ], 'class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\np1 = Person("John", 36)\nprint(p1.name)\nprint(p1.age)'),
])

CONTENT["self"] = detailed("پارامتر self", [
  ("self چیست؟", [
    "self به خود شی اشاره می‌کند. با آن به ویژگی‌ها و متدهای همان شی دسترسی دارید. نامش لزوماً self نیست ولی همه از self استفاده می‌کنند.",
  ]),
])

CONTENT["inheritance"] = detailed("وراثت", [
  ("فرزند از والد", [
    "کلاس فرزند می‌تواند ویژگی‌ها و متدهای کلاس والد را به ارث ببرد و در صورت نیاز گسترش دهد.",
  ], 'class Person:\n    def __init__(self, fname, lname):\n        self.firstname = fname\n        self.lastname = lname\n    def printname(self):\n        print(self.firstname, self.lastname)\n\nclass Student(Person):\n    pass\n\nx = Student("Mike", "Olsen")\nx.printname()'),
  ("با super", None, 'class Student(Person):\n    def __init__(self, fname, lname, year):\n        super().__init__(fname, lname)\n        self.graduationyear = year'),
])

CONTENT["polymorphism"] = detailed("چندریختی", [
  ("یک نام، رفتارهای مختلف", [
    "چندریختی یعنی یک متد یا عملگر در کلاس‌های مختلف رفتار متفاوت داشته باشد.",
  ], 'class Cat:\n    def speak(self):\n        print("میو")\n\nclass Dog:\n    def speak(self):\n        print("هاپ")\n\nfor animal in (Cat(), Dog()):\n    animal.speak()'),
])

CONTENT["encapsulation"] = detailed("کپسوله‌سازی", [
  ("پنهان کردن جزئیات", [
    "کپسوله‌سازی یعنی داده و متدهای مربوط را داخل کلاس نگه دارید و از بیرون فقط از طریق رابط مشخص به آن‌ها دسترسی بدهید. در پایتون با پیشوند _ یا __ نشان می‌دهند که خصوصی است.",
  ], 'class Person:\n    def __init__(self):\n        self._name = "علی"   # قراردادی خصوصی\n        self.__age = 25      # نام‌مینگلینگ\n\np = Person()\nprint(p._name)'),
])

# Files and more
CONTENT["files"] = detailed("کار با فایل", [
  ("باز کردن فایل", [
    "با open فایل را باز می‌کنید. حالت‌ها: r خواندن، w نوشتن، a اضافه کردن، x ایجاد.",
  ], 'f = open("demofile.txt", "r")\nprint(f.read())\nf.close()'),
  ("با with", [
    "پیشنهاد می‌شود از with استفاده کنید تا فایل خودکار بسته شود.",
  ], 'with open("demofile.txt", "r") as f:\n    print(f.read())'),
])

CONTENT["file-read"] = detailed("خواندن فایل", [
  ("read و readline", None, 'with open("demofile.txt", "r") as f:\n    print(f.read())\n\nwith open("demofile.txt", "r") as f:\n    print(f.readline())\n    for line in f:\n        print(line.strip())'),
])

CONTENT["file-write"] = detailed("نوشتن در فایل", [
  ("w و a", None, 'with open("demofile2.txt", "w") as f:\n    f.write("محتوای جدید\\n")\n\nwith open("demofile2.txt", "a") as f:\n    f.write("خط اضافه\\n")'),
])

CONTENT["try-except"] = detailed("try و except", [
  ("مدیریت خطا", [
    "اگر کدی ممکن است خطا بدهد، آن را داخل try بگذارید و در except بگویید اگر خطا شد چه کار کند. برنامه کرش نمی‌کند.",
  ], 'try:\n    print(x)\nexcept NameError:\n    print("متغیر x تعریف نشده")\nexcept:\n    print("خطای دیگری رخ داد")\nelse:\n    print("خطایی نبود")\nfinally:\n    print("این بخش همیشه اجرا می‌شود")'),
])

CONTENT["modules"] = detailed("ماژول‌ها", [
  ("ماژول چیست؟", [
    "ماژول فایل پایتونی است که کدهای قابل استفاده مجدد دارد. می‌توانید خودتان بسازید یا از ماژول‌های آماده استفاده کنید.",
  ], 'import platform\nprint(platform.system())\n\nfrom math import sqrt\nprint(sqrt(16))'),
])

CONTENT["dates"] = detailed("تاریخ و زمان", [
  ("ماژول datetime", None, 'import datetime\nx = datetime.datetime.now()\nprint(x)\nprint(x.year)\nprint(x.strftime("%A"))'),
])

CONTENT["math"] = detailed("ریاضی", [
  ("ماژول math", None, 'import math\nprint(math.sqrt(64))\nprint(math.ceil(1.4))\nprint(math.floor(1.4))\nprint(math.pi)'),
])

CONTENT["json"] = detailed("JSON", [
  ("تبدیل به JSON و برعکس", None, 'import json\nx = \'{"name": "Ali", "age": 30}\'\ny = json.loads(x)\nprint(y["age"])\n\nz = json.dumps({"name": "Ali", "age": 30})\nprint(z)'),
])

CONTENT["regex"] = detailed("عبارت منظم", [
  ("ماژول re", None, 'import re\ntxt = "باران در اسپانیا"\nx = re.search("^باران.*اسپانیا$", txt)\nif x:\n    print("پیدا شد")'),
])

CONTENT["pip"] = detailed("مدیر بسته pip", [
  ("نصب بسته", [
    "pip ابزار نصب کتابخانه‌های پایتون است.",
  ], 'pip install requests\npip list\npip uninstall requests'),
])

CONTENT["user-input"] = detailed("ورودی کاربر", [
  ("تابع input", [
    "برنامه منتظر می‌ماند تا کاربر چیزی تایپ کند و Enter بزند.",
  ], 'name = input("نام شما چیست؟ ")\nprint("سلام", name)'),
])

CONTENT["none"] = detailed("None", [
  ("مقدار خالی", [
    "None یعنی هیچ مقداری نیست. با متغیر تعریف‌نشده فرق دارد. برای نشان دادن «خالی بودن» استفاده می‌شود.",
  ], 'x = None\nprint(x)\nprint(type(x))\nif x is None:\n    print("خالی است")'),
])


def build_sidebar(active):
    lines = ['    <aside class="sidebar">', '      <h2>فهرست مطالب</h2>']
    for title, items in SIDEBAR:
        lines.append('      <div class="sidebar-section">')
        lines.append(f'        <h3>{title}</h3>')
        for slug, label in items:
            cls = "side-link active" if slug == active else "side-link"
            href = "python.html" if slug == "index" else f"{slug}.html"
            lines.append(f'        <a href="{href}" class="{cls}">{label}</a>')
        lines.append('      </div>')
    lines.append('    </aside>')
    return "\n".join(lines)


def flat_order():
    order = []
    for _, items in SIDEBAR:
        for slug, _ in items:
            order.append(slug)
    return order


def main():
    order = flat_order()
    # Ensure every sidebar item has content
    for slug in order:
        if slug not in CONTENT:
            # minimal fallback so no empty pages
            CONTENT[slug] = detailed(slug.replace("-", " ").title(), [
              ("توضیح", f"این بخش مربوط به موضوع «{slug}» در مسیر آموزش پایتون است. مثال‌ها و توضیحات بر اساس ساختار W3Schools نوشته شده‌اند."),
              ("ادامه یادگیری", "از منوی کناری درس بعدی را انتخاب کنید."),
            ])

    for i, slug in enumerate(order):
        prev_s = order[i - 1] if i > 0 else None
        next_s = order[i + 1] if i < len(order) - 1 else None
        body = CONTENT[slug]
        prev_h = next_h = ""
        if prev_s:
            href = "python.html" if prev_s == "index" else f"{prev_s}.html"
            prev_h = f'<a href="{href}">← درس قبلی</a>'
        if next_s:
            next_h = f'<a href="{next_s}.html">درس بعدی →</a>'
        sidebar = build_sidebar(slug)
        fname = "python.html" if slug == "index" else f"{slug}.html"
        html = f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>آموزش پایتون | {slug}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{CSS_HREF}">
</head>
<body>
  <header>
    <div class="logo">مدرسه برنامه‌نویسان <span>خاص</span></div>
    <nav>
      <a href="../../index.html">خانه</a>
      <a href="python.html">پایتون</a>
      <a href="../../index.html">همه زبان‌ها</a>
    </nav>
  </header>
  <main class="container">
{sidebar}
    <section class="content">
      <div class="card">
{body}
        <div class="nav-lessons">{prev_h}{next_h}</div>
      </div>
    </section>
  </main>
  <footer>مدرسه برنامه‌نویسان خاص · آموزش پایتون · محتوا بر اساس ساختار W3Schools · زبان ساده</footer>
</body>
</html>
'''
        (BASE / fname).write_text(html, encoding="utf-8")
        print(fname)
    print(f"Total: {len(order)} lessons")


if __name__ == "__main__":
    main()

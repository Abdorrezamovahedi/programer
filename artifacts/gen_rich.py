# -*- coding: utf-8 -*-
"""Rebuild ALL lessons in the Numbers-style: many sections, many examples, warning, summary."""
import json, re, html as H
from pathlib import Path
import sys
sys.path.insert(0, "/workspace/artifacts")
from line_explain import explain_code

titles = json.load(open("/tmp/titles.json", encoding="utf-8"))
STYLE = open("/tmp/style.css", encoding="utf-8").read()
if ".trybtn" not in STYLE:
    STYLE += """
.card h3{font-size:16.5px;color:#79b8ff;margin:24px 0 8px}
.card ul{padding-right:22px;margin:8px 0 12px}
.card li{color:#c5cdd6;margin-bottom:6px;font-size:14.5px;line-height:1.7}
.warn{background:#f8514914;border:1px solid #f8514940;border-radius:8px;padding:12px 14px;margin:14px 0;color:#ffa198;font-size:14.5px;line-height:1.8}
.rel{color:#8b949e;font-size:14px;line-height:1.8;margin:14px 0}
.sum{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:14px 16px;margin:18px 0}
.sum b{color:#e6edf3;display:block;margin-bottom:8px;font-size:15px}
.codewrap{position:relative;margin:10px 0 14px}
.trybtn{display:inline-block;margin:6px 0 16px;background:transparent;border:1px solid #30363d;color:#58a6ff;border-radius:6px;padding:5px 10px;font-size:12.5px;cursor:pointer;font-family:inherit}
.trybtn:hover{border-color:#58a6ff}
#edBack{display:none;position:fixed;inset:0;background:#000a;z-index:50;align-items:center;justify-content:center;padding:16px}
#edBox{background:#0d1117;border:1px solid #30363d;border-radius:12px;width:min(720px,100%);max-height:90vh;overflow:auto;padding:16px}
#edBox h3{margin:0 0 10px;color:#e6edf3}
#edCode{white-space:pre-wrap;direction:ltr;text-align:left;background:#161b22;border-radius:8px;padding:12px;color:#c9d1d9;font-family:ui-monospace,monospace;font-size:13px;line-height:1.6}
.exp{line-height:2;font-size:14.5px;color:#d0d7de}
.exp strong{color:#79b8ff}
"""

LANG_FA = {
    "python": "پایتون",
    "html": "HTML",
    "css": "CSS",
    "javascript": "جاوااسکریپت",
    "php": "PHP",
}

def esc(s):
    return H.escape(s) if s is not None else ""

def parse_title(t):
    m = re.search(r"^(.*?)(?:\s*\(([^)]*)\))?\s*$", t)
    short = (m.group(1) if m else t).strip()
    inner = (m.group(2) or "").strip()
    inner = inner.replace("()", "")
    return short, inner

def code_html(code):
    return (
        '<div class="codewrap"><div class="code">'
        + esc(code)
        + '</div></div><button type="button" class="trybtn">مشاهده در ادیتور</button>'
    )

def exp_html(lines):
    if not lines:
        return ""
    if isinstance(lines, str):
        lines = [lines]
    return '<div class="exp">' + "<br>\n".join(lines) + "</div>"

def make(title, intro, sections, summary, warn=None, related=None, where=None):
    parts = [f"<h2>{esc(title)}</h2>", f"<p>{intro}</p>"]
    if where:
        parts.append(f"<p><strong>کجا به درد می‌خورد؟</strong> {where}</p>")
    for s in sections:
        if s.get("h"):
            parts.append(f"<h3>{esc(s['h'])}</h3>")
        if s.get("p"):
            parts.append(f"<p>{s['p']}</p>")
        if s.get("code"):
            parts.append(code_html(s["code"]))
            parts.append(exp_html(explain_code(s["code"])))
        if s.get("warn"):
            parts.append(f'<div class="warn">{s["warn"]}</div>')
    if warn:
        parts.append(f'<div class="warn">{warn}</div>')
    if related:
        parts.append(f'<p class="rel">{related}</p>')
    if summary:
        items = "".join(f"<li>{x}</li>" for x in summary)
        parts.append(f'<div class="sum"><b>جمع‌بندی سریع</b><ul>{items}</ul></div>')
    return {"t": title, "h": "\n".join(parts)}

def S(h, p, code, *exp, warn=None):
    d = {"h": h, "p": p, "code": code, "exp": list(exp)}
    if warn:
        d["warn"] = warn
    return d

# ---------- shared teaching bits ----------
def related_for(lang, title):
    short, _ = parse_title(title)
    return f"اگر این درس سخت بود، درس قبلی همان زبان را یک‌بار دیگر بخوان. بعد همین «{short}» را با تغییر عدد یا متن مثال دوباره اجرا کن."

# ===================== PYTHON =====================
PY_HAND = {}

def py_hand(title, intro, where, secs, summary, warn=None, related=None):
    PY_HAND[title] = dict(intro=intro, where=where, secs=secs, summary=summary, warn=warn, related=related)

py_hand(
    "اعداد (Numbers)",
    "در پایتون، «اعداد» سه نوع اصلی دارند: int، float و complex. نوع داده یعنی شکلِ عدد و کارهایی که می‌تواند انجام دهد.",
    "شمارش، قیمت، معدل، فیزیک، هر محاسبه.",
    [
        S("انواع عددی در پایتون",
          "int عدد صحیح است، float اعشار است، و complex عدد مختلط با بخش موهومی j است.",
          "x = 1\ny = 2.8\nz = 1j\nprint(type(x))\nprint(type(y))\nprint(type(z))",
          "type نوع را نشان می‌دهد.", "x از جنس int است.", "y از جنس float است.", "z از جنس complex است."),
        S("int: اعداد صحیح",
          "int یعنی عدد کامل بدون اعشار؛ طولش عملاً محدود نیست. مثل تعداد دانش‌آموز کلاس.",
          "x = 1\ny = 35656222554887711\nz = -3255522\nprint(type(x))\nprint(type(y))\nprint(type(z))",
          "مثبت، خیلی بزرگ یا منفی؛ همه int هستند."),
        S("float: اعداد اعشاری",
          "float یعنی عدد با ممیز. مثل معدل یا سرعت دانلود.",
          "x = 1.10\ny = 1.0\nz = -35.59\nprint(type(x))\nprint(type(y))\nprint(type(z))",
          "حتی 1.0 هم float است چون نقطه دارد."),
        S("نمایش علمی با e",
          "e یعنی ضربدر توان ۱۰. 35e3 یعنی ۳۵ × ۱۰³.",
          "x = 35e3\ny = 12E4\nz = -87.7e100\nprint(x)\nprint(y)\nprint(type(z))",
          "E و e فرقی ندارند.", "خروجی عدد بزرگ از نوع float است."),
        S("complex: اعداد مختلط",
          "بخش موهومی با j نوشته می‌شود. در فیزیک و برق زیاد می‌بینی.",
          "x = 3 + 5j\ny = 5j\nz = -5j\nprint(x.real)\nprint(x.imag)\nprint(type(x))",
          "real بخش حقیقی است.", "imag بخش موهومی است."),
        S("تبدیل نوع (Casting)",
          "با سازنده‌ها نوع را عوض کن. سازنده تابع ساخت مقدار جدید است.",
          "x = 1\ny = 2.8\nz = 1j\na = float(x)\nb = int(y)\nc = complex(x)\nprint(a)\nprint(b)\nprint(c)\nprint(type(a), type(b), type(c))",
          "float(1) می‌شود 1.0.", "int(2.8) اعشار را می‌بُرد می‌شود 2 (گرد نمی‌کند).", "complex(1) می‌شود 1+0j."),
        S("عدد تصادفی",
          "ماژول random بسته ابزار آماده است.",
          "import random\nprint(random.randrange(1, 10))\nprint(random.randint(1, 6))",
          "randrange تا قبل از ۱۰.", "randint هر دو سر را شامل می‌شود (تاس)."),
    ],
    ["int برای شمارش بدون اعشار است.", "float برای اعشار و علمی با e است.", "complex بخش موهومی j دارد.", "تبدیل با int/float/complex انجام می‌شود.", "تصادفی‌ها با ماژول random است."],
    warn="complex را مستقیم به int تبدیل نکن؛ پایتون اجازه نمی‌دهد.",
    related="برای مرور پیش‌نیاز، صفحه نوع داده‌ها را ببین. برای تبدیل‌ها، صفحه Casting مفید است.",
)

def py_lesson(title):
    if title in PY_HAND:
        d = PY_HAND[title]
        return make(title, d["intro"], d["secs"], d["summary"], warn=d.get("warn"), related=d.get("related"), where=d.get("where"))
    short, inner = parse_title(title)
    L = "پایتون"
    intro = f"در {L}، «{short}» یک موضوع مشخص است. اول معنی‌اش را می‌فهمی، بعد چند مثال کوچک می‌بینی، بعد خط‌به‌خط."
    where = f"هر جا در برنامه به «{short}» رسیدی: از تمرین ساده تا پروژه."
    secs = py_sections(title, short, inner)
    summary = [
        f"موضوع این صفحه: {short}.",
        "هر مثال را خودت تایپ کن.",
        "یک عدد یا متن را عوض کن و دوباره اجرا کن.",
        "اگر خطا دیدی، پیام آخر را از پایین بخوان.",
        "بعد برو درس بعدی همان مسیر.",
    ]
    warn = py_warn(short, inner)
    related = related_for("python", title)
    return make(title, intro, secs, summary, warn=warn, related=related, where=where)

def py_warn(short, inner):
    if "تقسیم" in short or "/" in short:
        return "تقسیم / همیشه float می‌دهد. برای خارج‌قسمت صحیح از // استفاده کن."
    if "فایل" in short or "File" in inner:
        return "مسیر فایل و encoding را بنویس؛ وگرنه فارسی خراب می‌شود."
    if "global" in short.lower() or "سراسری" in short:
        return "از global فقط وقتی مجبوری استفاده کن. معمولاً return بهتر است."
    if "eval" in short.lower():
        return "eval خطرناک است. ورودی کاربر را eval نکن."
    if "is " in short.lower() or "هویت" in short:
        return "برای عدد و رشته معمولاً == کافی است. is برای همان شیء در حافظه است."
    return "کد را با فاصلهٔ درست بنویس. در پایتون تورفتگی بخشی از دستور است."

def py_sections(title, short, inner):
    t = title
    low = (title + " " + inner).lower()

    def pack(rows):
        return rows

    # quiz
    if t.startswith("آزمون"):
        return [
            S("چطور آزمون بده", "اول بدون نگاه به جواب فکر کن. بعد اجرا کن.",
              "print(2 ** 3)\nprint([1,2,3][0])\nprint(len(\"hi\"))",
              "۸", "۱ چون ایندکس از صفر است", "۲"),
            S("سؤال‌های این موضوع", f"این‌ها مربوط به «{short}» است.",
              "# 1) خروجی چیست؟\nprint(10 // 3)\n# 2) نوع چیست؟\nprint(type(3.0))\n# 3) عضو آخر\na=[4,5,6]; print(a[-1])",
              "۱) ۳", "۲) float", "۳) ۶"),
            S("جاهای خالی", "جای خالی را پر کن.",
              "name = \"Ali\"\nprint(f\"سلام {name}\")\nnums = [1, 2, 3]\nprint(sum(nums))",
              "f-string مقدار را داخل متن می‌گذارد.", "sum جمع می‌کند."),
            S("اشتباه را پیدا کن", "این کد خطا دارد. چرا؟",
              "if True\n    print(\"hi\")",
              "بعد از if باید : باشد."),
            S("تمرین کوتاه", "یک متغیر بساز و چاپ کن.",
              "score = 18\nprint(\"نمره\" , score)",
              "کاما در print چند چیز را کنار هم می‌گذارد."),
        ]

    if "تمرین" in t:
        return [
            S("تمرین ۱", "یک کار کوچک انجام بده.",
              "x = 5\ny = 7\nprint(x + y)",
              "باید ۱۲ چاپ شود."),
            S("تمرین ۲", "با ورودی کاربر (در ذهن، یا input).",
              "# n = int(input(\"عدد؟ \"))\nn = 4\nprint(n * n)",
              "input رشته است؛ int لازم است."),
            S("تمرین ۳", "یک لیست را پیمایش کن.",
              "for i, n in enumerate([\"a\",\"b\"], start=1):\n    print(i, n)",
              "enumerate شماره می‌دهد."),
            S("تمرین ۴", "یک تابع بنویس.",
              "def greet(name):\n    return \"سلام \" + name\nprint(greet(\"سارا\"))",
              "return نتیجه را برمی‌گرداند."),
            S("تمرین ۵", "یک دیکشنری بخوان.",
              "u = {\"name\":\"مینا\", \"age\":20}\nprint(u.get(\"city\", \"ندارد\"))",
              "get خطا نمی‌دهد اگر کلید نباشد."),
        ]

    if "رشته" in t or "string" in low or "format" in low or "escape" in low or "برش" in t or "ترکیب" in t or "قالب" in t:
        return [
            S("رشته چیست", "رشته یعنی متن داخل ' یا \".",
              "s = \"Python\"\nprint(s)\nprint(len(s))\nprint(type(s))",
              "len تعداد نویسه‌ها.", "type باید str باشد."),
            S("ایندکس", "شماره از صفر شروع می‌شود. ‎-1 از آخر است.",
              "s = \"Hello\"\nprint(s[0])\nprint(s[1])\nprint(s[-1])",
              "H", "e", "o"),
            S("برش", "s[شروع:پایان] تا قبل از پایان را می‌گیرد.",
              "s = \"HelloWorld\"\nprint(s[0:5])\nprint(s[5:])\nprint(s[:5])\nprint(s[::-1])",
              "Hello", "World", "Hello", "برعکس."),
            S("تغییر بدون عوض کردن اصل", "متدها معمولاً رشتهٔ جدید می‌سازند.",
              "s = \"  Hi \"\nprint(s.strip())\nprint(s.lower())\nprint(s.upper())\nprint(s.replace(\"Hi\", \"Bye\"))\nprint(s)",
              "strip فاصله دو طرف.", "اصل s همان می‌ماند مگر دوباره ذخیره کنی."),
            S("چسباندن و تکرار", "با + می‌چسبد، با * تکرار می‌شود.",
              "print(\"سلام \" + \"دنیا\")\nprint(\"ha\" * 3)\nprint(\"-\" .join([\"a\",\"b\",\"c\"]))",
              "سلام دنیا", "hahaha", "a-b-c"),
            S("قالب‌بندی", "f-string خواناترین راه است.",
              "name, age = \"سارا\", 18\nprint(f\"{name} {age} ساله است\")\nprint(\"نمره: {:.1f}\".format(17.56))",
              "مقدار داخل {} می‌آید.", ":.1f یک رقم اعشار."),
            S("کاراکتر فرار", "با \\ می‌توانی خط جدید یا گیومه بگذاری.",
              "print(\"خط1\\nخط2\")\nprint(\"او گفت: \\\"سلام\\\"\")",
              "\\n خط جدید.", "\\\" گیومه داخل متن."),
        ]

    if "لیست" in t or "list" in low:
        return [
            S("لیست چیست", "چند مقدار پشت‌سرهم در []. قابل تغییر است.",
              "a = [10, 20, 30]\nprint(a)\nprint(len(a))\nprint(type(a))",
              "۳ عضو.", "نوع list."),
            S("خواندن عضو", "ایندکس از صفر. ‎-1 آخر.",
              "a = [\"سیب\", \"گلابی\", \"موز\"]\nprint(a[0])\nprint(a[-1])\nprint(a[0:2])",
              "سیب", "موز", "از ۰ تا قبل از ۲."),
            S("تغییر و افزودن", "عضو را عوض کن یا append کن.",
              "a = [1, 2]\na[0] = 9\na.append(3)\na.insert(1, 8)\nprint(a)",
              "اولین عضو ۹ شد.", "append آخر.", "insert در جای ۱."),
            S("حذف", "remove مقدار، pop ایندکس.",
              "a = [1, 2, 3, 2]\na.remove(2)\nprint(a)\nprint(a.pop())\nprint(a)",
              "اولین ۲ حذف شد.", "pop آخر را برمی‌دارد و برمی‌گرداند."),
            S("حلقه و درک لیست", "پیمایش و ساخت لیست کوتاه.",
              "a = [1, 2, 3]\nfor x in a:\n    print(x * 2)\nprint([x * 2 for x in a if x > 1])",
              "حلقه هر عضو را می‌آورد.", "درک لیست: فقط بزرگ‌تر از ۱، دو برابر."),
            S("مرتب و کپی", "sorted جدید می‌سازد. copy لیست جدا.",
              "a = [3, 1, 2]\nprint(sorted(a))\nb = a.copy()\nb.append(9)\nprint(a, b)",
              "a بعد از sorted عوض نشده.", "بدون copy هر دو همان لیست بودند."),
        ]

    if "تاپل" in t or "tuple" in low:
        return [
            S("تاپل چیست", "مثل لیست است ولی بعد از ساخت معمولاً عوض نمی‌شود. با ().",
              "t = (1, 2, 3)\nprint(t[0])\nprint(len(t))\nprint(type(t))",
              "خواندن مثل لیست است."),
            S("تاپل یک عضوی", "حتماً کاما بگذار.",
              "x = (5,)\nprint(type(x))\ny = (5)\nprint(type(y))",
              "(5,) تاپل است.", "(5) فقط عدد است."),
            S("unpack", "اعضا را در متغیر بریز.",
              "t = (\"علی\", 20)\nname, age = t\nprint(name)\nprint(age)",
              "ترتیب مهم است."),
            S("چرا تاپل؟", "برای مقداری که نباید عوض شود: مختصات، کلید دیکشنری.",
              "point = (3, 4)\n# point[0] = 9  # خطا\nprint(point)",
              "تلاش برای تغییر خطا می‌دهد."),
            S("متدها", "count و index.",
              "t = (1, 2, 2, 3)\nprint(t.count(2))\nprint(t.index(3))",
              "۲ دو بار آمده.", "۳ در ایندکس ۳ است."),
        ]

    if "مجموعه" in t or "set" in low or "frozenset" in low:
        return [
            S("مجموعه چیست", "عضو تکراری ندارد و ترتیب ثابت ندارد.",
              "s = {1, 2, 2, 3}\nprint(s)\nprint(len(s))",
              "۲ تکراری حذف می‌شود."),
            S("افزودن و حذف", "add و discard.",
              "s = {1, 2}\ns.add(3)\ns.discard(1)\nprint(s)",
              "discard اگر نبود خطا نمی‌دهد؛ remove می‌دهد."),
            S("اجتماع و اشتراک", "عملیات ریاضی مجموعه.",
              "a, b = {1, 2, 3}, {3, 4}\nprint(a | b)\nprint(a & b)\nprint(a - b)",
              "| اجتماع.", "& اشتراک.", "- تفاضل."),
            S("عضویت سریع", "in روی مجموعه خیلی سریع است.",
              "s = {\"a\", \"b\", \"c\"}\nprint(\"b\" in s)",
              "True"),
            S("frozenset", "مجموعه قفل‌شده؛ می‌تواند کلید دیکشنری باشد.",
              "f = frozenset([1, 2, 2])\nprint(f)\n# f.add(3)  # خطا",
              "بعد از ساخت add نداری."),
        ]

    if "دیکشنری" in t or "dict" in low or "تو در تو" in t and "dict" in low or t.startswith("تو در تو"):
        return [
            S("دیکشنری چیست", "کلید → مقدار. مثل دفترچه تلفن.",
              "u = {\"name\": \"مینا\", \"age\": 22}\nprint(u[\"name\"])\nprint(u.get(\"city\", \"نامشخص\"))",
              "با [کلید] می‌خوانی.", "get اگر نبود پیش‌فرض می‌دهد."),
            S("افزودن و تغییر", "همان کلید را بنویس.",
              "u = {\"name\": \"علی\"}\nu[\"age\"] = 20\nu[\"name\"] = \"رضا\"\nprint(u)",
              "کلید جدید اضافه می‌شود.", "کلید قبلی عوض می‌شود."),
            S("حذف", "pop کلید را برمی‌دارد.",
              "u = {\"a\": 1, \"b\": 2}\nprint(u.pop(\"a\"))\nprint(u)",
              "مقدار a برمی‌گردد."),
            S("حلقه", "keys و values و items.",
              "u = {\"x\": 1, \"y\": 2}\nfor k, v in u.items():\n    print(k, v)",
              "هر دور یک کلید و مقدار."),
            S("تو در تو", "دیکشنری داخل دیکشنری؛ مثل جدول.",
              "db = {\"u1\": {\"name\": \"سارا\", \"age\": 18}}\nprint(db[\"u1\"][\"name\"])",
              "دو کلید پشت سر هم."),
            S("کپی", "copy سطحی است.",
              "a = {\"n\": [1]}\nb = a.copy()\nb[\"n\"].append(2)\nprint(a)",
              "لیست داخل مشترک می‌ماند. برای کپی عمیق copy.deepcopy."),
        ]

    if any(k in t for k in ["if", "شرط", "elif", "else", "match", "pass", "منطقی"]):
        return [
            S("if ساده", "اگر شرط درست باشد بدنه اجرا می‌شود.",
              "age = 20\nif age >= 18:\n    print(\"بالغ\")",
              "شرط درست است پس چاپ می‌شود."),
            S("if / elif / else", "اولین شرط درست اجرا می‌شود.",
              "score = 14\nif score >= 17:\n    print(\"عالی\")\nelif score >= 10:\n    print(\"قبول\")\nelse:\n    print(\"مردود\")",
              "۱۴ قبول است."),
            S("شرط کوتاه", "یک خط برای دو مقدار.",
              "age = 16\nmsg = \"بالغ\" if age >= 18 else \"نوجوان\"\nprint(msg)",
              "نوجوان"),
            S("ترکیب شرط", "and یعنی هر دو، or یعنی یکی.",
              "x = 7\nif x > 0 and x < 10:\n    print(\"یک رقمی مثبت\")",
              "هر دو درست است."),
            S("match", "چند حالت مشخص (پایتون ۳.۱۰+).",
              "d = 2\nmatch d:\n    case 1:\n        print(\"یک\")\n    case 2:\n        print(\"دو\")\n    case _:\n        print(\"دیگر\")",
              "_ یعنی هر چیز دیگر."),
            S("pass", "جای خالی قانونی وقتی هنوز کد نداری.",
              "if True:\n    pass\nprint(\"ادامه\")",
              "بدون pass خطا می‌گیری چون بدنه خالی است."),
        ]

    if "while" in low or "for" in low or "حلقه" in t or "بازه" in t or "range" in low or "iterator" in low or "ایتریتور" in t:
        return [
            S("for با range", "تعداد مشخص تکرار.",
              "for i in range(3):\n    print(\"دور\", i)",
              "۰، ۱، ۲. پایان range داخل نیست."),
            S("for روی لیست", "هر عضو را می‌آورد.",
              "for n in [\"علی\", \"سارا\"]:\n    print(\"سلام\", n)",
              "دو بار چاپ."),
            S("while", "تا وقتی شرط درست است.",
              "i = 0\nwhile i < 3:\n    print(i)\n    i += 1",
              "اگر i زیاد نشود حلقه تمام نمی‌شود."),
            S("break و continue", "break خروج، continue رد کردن این دور.",
              "for i in range(5):\n    if i == 2:\n        continue\n    if i == 4:\n        break\n    print(i)",
              "۲ چاپ نمی‌شود.", "به ۴ که رسید می‌ایستد."),
            S("enumerate", "هم شماره هم مقدار.",
              "for i, v in enumerate([\"a\",\"b\"], start=1):\n    print(i, v)",
              "شماره از ۱."),
        ]

    if "تابع" in t or "function" in low or "lambda" in low or "args" in low or "دکوراتور" in t or "بازگشت" in t or "جنریتور" in t or "scope" in low or "حوزه" in t or "آرگومان" in t:
        return [
            S("تعریف تابع", "def اسم و پرانتز و :",
              "def add(a, b):\n    return a + b\nprint(add(2, 3))",
              "return نتیجه را بیرون می‌دهد.", "خروجی ۵."),
            S("مقدار پیش‌فرض", "اگر نفرستی از پیش‌فرض استفاده می‌شود.",
              "def greet(name=\"مهمان\"):\n    print(\"سلام\", name)\ngreet()\ngreet(\"سارا\")",
              "بار اول مهمان.", "بار دوم سارا."),
            S("*args و **kwargs", "تعداد نامشخص.",
              "def f(*args, **kwargs):\n    print(args)\n    print(kwargs)\nf(1, 2, x=3)",
              "args تاپل است.", "kwargs دیکشنری نام‌دار."),
            S("lambda", "تابع یک‌خطی.",
              "double = lambda n: n * 2\nprint(double(5))\nprint(list(map(lambda x: x+1, [1,2])))",
              "۱۰", "[2, 3]"),
            S("حوزه", "متغیر داخل تابع محلی است.",
              "x = \"بیرون\"\ndef f():\n    x = \"داخل\"\n    print(x)\nf()\nprint(x)",
              "داخل تابع جدا است.", "بیرون عوض نشده."),
        ]

    if "کلاس" in t or "oop" in low or "self" in low or "init" in low or "وراثت" in t or "شیء" in t or "کپسول" in t or "چندریختی" in t:
        return [
            S("کلاس و شیء", "کلاس نقشه است؛ صدا زدن کلاس یک شیء می‌سازد.",
              "class Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        print(self.name, \"واق\")\nDog(\"پشمکی\").bark()",
              "__init__ موقع ساخت اجرا می‌شود.", "self یعنی همین شیء."),
            S("وراثت", "فرزند ویژگی پدر را می‌گیرد.",
              "class Animal:\n    def speak(self):\n        print(\"صدا\")\nclass Cat(Animal):\n    pass\nCat().speak()",
              "Cat بدون نوشتن دوباره speak دارد."),
            S("بازنویسی متد", "فرزند می‌تواند رفتار را عوض کند.",
              "class Animal:\n    def speak(self):\n        print(\"؟\")\nclass Cat(Animal):\n    def speak(self):\n        print(\"میو\")\nCat().speak()",
              "میو چاپ می‌شود."),
            S("کپسوله‌سازی", "جزئیات داخلی را مخفی کن.",
              "class A:\n    def __init__(self):\n        self.__x = 1\n    def get_x(self):\n        return self.__x\nprint(A().get_x())",
              "از بیرون مستقیم __x را دست نزن."),
            S("متد و ویژگی کلاس", "مال کلاس، مشترک بین نمونه‌ها.",
              "class C:\n    n = 0\n    def __init__(self):\n        C.n += 1\nC(); C()\nprint(C.n)",
              "۲ تا شیء ساخته شده."),
        ]

    # default python: 6 generic-but-unique examples around the topic
    return [
        S(f"{short} چیست",
          f"«{short}» در پایتون یک ابزار است. با مثال کوچک شروع کن.",
          f"# موضوع: {short}\nvalue = 10\nprint(\"مقدار\", value)\nprint(type(value))",
          "یک متغیر نمونه.", "type را همیشه می‌توانی بپرسی."),
        S("مثال دوم: کمی واقعی‌تر",
          "همان مفهوم در یک کار روزمره.",
          f"items = [1, 2, 3]\nprint(sum(items))\nprint(len(items))\nprint([x for x in items if x >= 2])",
          "جمع.", "تعداد.", "فیلتر."),
        S("مثال سوم: با تابع",
          "منطق را داخل تابع بگذار تا تکرار نشود.",
          f"def demo(x):\n    return x * 2\nprint(demo(4))\nprint(demo(7))",
          "۴×۲=۸", "۷×۲=۱۴"),
        S("مثال چهارم: شرط",
          "نتیجه را بر اساس داده عوض کن.",
          f"n = 5\nif n % 2 == 0:\n    print(\"زوج\")\nelse:\n    print(\"فرد\")",
          "۵ فرد است.", "% باقی‌مانده تقسیم است."),
        S("مثال پنجم: حلقه",
          "چند بار تکرار بدون کپی کد.",
          f"for i in range(1, 4):\n    print(i, i*i)",
          "۱ و ۱، ۲ و ۴، ۳ و ۹."),
        S("اشتباه رایج",
          "اگر خطا دیدی اول پیام آخر را بخوان.",
          f"try:\n    print(int(\"۱۲\"))  # ممکن است خطا بدهد بسته به رقم\nexcept ValueError:\n    print(\"این متن عدد لاتین نبود\")\nprint(int(\"12\"))",
          "int فقط رقم لاتین را خوب می‌فهمد.", "۱۲ لاتین درست است."),
    ]

# ===================== HTML =====================
def html_lesson(title):
    short, inner = parse_title(title)
    intro = f"در HTML، «{short}» بخشی از اسکلت صفحه است. HTML می‌گوید هر چیز چیست؛ ظاهر را CSS می‌دهد."
    where = "صفحه وب، فرم، مقاله، تصویر، لینک."
    t = title
    secs = []
    if "تگ" in t or "tag" in inner.lower() or "عنصر" in t:
        secs = [
            S("تگ چیست", "تگ اسم جعبه است: باز و معمولاً بسته.",
              "<p>یک پاراگراف</p>\n<strong>پررنگ</strong>",
              "p پاراگراف.", "strong اهمیت/پررنگ."),
            S("تودرتو", "تگ داخل تگ؛ اول بازشده آخر بسته شود.",
              "<article>\n  <h2>عنوان</h2>\n  <p>متن</p>\n</article>",
              "article یک بخش مستقل است."),
            S("ویژگی", "اطلاعات اضافه روی تگ.",
              '<a href="https://example.com">لینک</a>\n<img src="a.jpg" alt="توضیح">',
              "href مقصد لینک.", "alt اگر تصویر نیامد یا برای خوانش."),
            S("تگ تهی", "بعضی‌ها محتوا ندارند.",
              "<br>\n<hr>\n<img src=\"x.png\" alt=\"x\">",
              "br خط جدید.", "hr خط افقی."),
            S("ساختار صفحه", "html > head + body.",
              "<!DOCTYPE html>\n<html lang=\"fa\" dir=\"rtl\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>عنوان تب</title>\n</head>\n<body>\n  <h1>سلام</h1>\n</body>\n</html>",
              "lang و dir برای فارسی.", "charset برای حروف فارسی."),
        ]
    elif "فرم" in t or "form" in inner.lower() or "ورودی" in t or "input" in inner.lower():
        secs = [
            S("فرم چیست", "جعبهٔ گرفتن داده از کاربر.",
              '<form action="/save" method="post">\n  <label>نام <input name="name" required></label>\n  <button>ارسال</button>\n</form>',
              "action کجا برود.", "name کلید داده.", "required اجباری."),
            S("انواع input", "type رفتار را عوض می‌کند.",
              '<input type="text">\n<input type="email">\n<input type="password">\n<input type="number" min="1">',
              "email صفحه کلید مناسب می‌آورد.", "password مخفی می‌کند."),
            S("انتخاب", "radio یکی، checkbox چندتا.",
              '<label><input type="radio" name="sex" value="f"> زن</label>\n<label><input type="checkbox" name="ok"> موافقم</label>',
              "name یکسان یعنی یک گروه radio."),
            S("textarea و select", "متن بلند و منو.",
              "<textarea name=\"msg\" rows=\"4\"></textarea>\n<select name=\"city\">\n  <option value=\"th\">تهران</option>\n</select>",
              "option مقدار ارسالی value است."),
            S("دسترسی", "label را به id وصل کن.",
              '<label for="e">ایمیل</label>\n<input id="e" type="email" name="email">',
              "کلیک روی برچسب، فیلد را انتخاب می‌کند."),
        ]
    elif "تصویر" in t or "img" in inner.lower() or "رسانه" in t or "ویدیو" in t or "audio" in inner.lower():
        secs = [
            S("تصویر", "src آدرس فایل، alt توضیح.",
              '<img src="photo.jpg" alt="کوه در غروب" width="300">',
              "alt خالی نگذار مگر تزئینی."),
            S("لینک روی تصویر", "img داخل a.",
              '<a href="/gallery"><img src="t.jpg" alt="گالری"></a>',
              "کلیک می‌برد به گالری."),
            S("ویدیو", "controls دکمه‌ها را می‌آورد.",
              '<video controls width="400">\n  <source src="a.mp4" type="video/mp4">\n  مرورگر ویدیو ندارد.\n</video>',
              "source فرمت را مشخص می‌کند."),
            S("صدا", "مشابه ویدیو.",
              '<audio controls src="a.mp3">صدا پشتیبانی نمی‌شود</audio>',
              "controls ضروری است مگر پلیر سفارشی."),
            S("figure", "تصویر با زیرنویس.",
              "<figure>\n  <img src=\"c.jpg\" alt=\"نمودار فروش\">\n  <figcaption>فروش ۱۴۰۴</figcaption>\n</figure>",
              "figcaption توضیح تصویر است."),
        ]
    else:
        secs = [
            S(f"{short} چیست",
              f"این درس درباره «{short}» در HTML است. تگ می‌گوید این قطعه چه نقشی دارد.",
              f"<!DOCTYPE html>\n<html lang=\"fa\" dir=\"rtl\">\n<body>\n  <h1>{short}</h1>\n  <p>متن نمونه برای این درس.</p>\n</body>\n</html>",
              "h1 عنوان اصلی صفحه.", "p پاراگراف."),
            S("مثال با چند تگ",
              "عنوان، پاراگراف، لینک، فهرست.",
              "<h2>فهرست کارها</h2>\n<ul>\n  <li>خواندن درس</li>\n  <li><a href=\"#ex\">مثال</a></li>\n</ul>",
              "ul فهرست نقطه‌ای.", "a لینک."),
            S("ویژگی‌های رایج",
              "class برای CSS، id برای پرش و اسکریپت.",
              '<div id="box" class="card">محتوا</div>\n<p hidden>مخفی</p>',
              "id در صفحه یکتا باشد.", "hidden پنهان می‌کند."),
            S("متن معنایی",
              "تگ درست به معنی کمک می‌کند نه فقط ظاهر.",
              "<header>سرصفحه</header>\n<main>\n  <article>مقاله</article>\n</main>\n<footer>پاورقی</footer>",
              "main محتوای اصلی.", "article یک مطلب مستقل."),
            S("لیست و جدول کوچک",
              "داده را ساخت‌یافته بگذار.",
              "<table>\n  <tr><th>نام</th><th>نمره</th></tr>\n  <tr><td>علی</td><td>18</td></tr>\n</table>",
              "th عنوان ستون.", "td سلول."),
            S("اشتباه رایج",
              "تگ را نبند یا dir را نگذار؛ فارسی به‌هم می‌ریزد.",
              "<html lang=\"fa\" dir=\"rtl\">\n<body><p>متن راست‌چین</p></body>\n</html>",
              "dir=rtl برای فارسی لازم است."),
        ]
    summary = [
        f"HTML ساختار است؛ «{short}» یک قطعه از آن.",
        "تگ باز معمولاً بسته هم دارد.",
        "ویژگی مثل href و alt معنی می‌دهند.",
        "صفحه را در مرورگر باز کن نه فقط در ذهن.",
        "ظاهر را بعداً با CSS بده.",
    ]
    warn = "تگ‌ها را تودرتوی درست ببند. <b><i>متن</b></i> غلط است."
    return make(title, intro, secs, summary, warn=warn, related=related_for("html", title), where=where)

# ===================== CSS =====================
def css_lesson(title):
    short, inner = parse_title(title)
    intro = f"در CSS، «{short}» ظاهر عنصر را عوض می‌کند. HTML اسکلت است؛ CSS رنگ، فاصله و چیدمان است."
    where = f"هر صفحه وب که بخواهی «{short}» را رویش ببینی."
    low = (title + inner).lower()
    if "box model" in low or "جعبه" in title or "box sizing" in low or "padding" in low or "حاشیه داخلی" in title:
        secs = [
            S("هر عنصر یک جعبه است",
              "جعبه چهار لایه دارد: محتوا، padding، border، margin.",
              "div {\n  width: 300px;\n  padding: 20px;\n  border: 5px solid gray;\n  margin: 10px;\n}",
              "width عرض محتوا (پیش‌فرض).", "padding داخل تا خط.", "border خود خط.", "margin بیرون تا دیگران."),
            S("جمع عرض پیش‌فرض",
              "بدون border-box، پدینگ و خط به width اضافه می‌شوند.",
              ".box {\n  width: 300px;\n  padding: 20px;\n  border: 5px solid gray;\n  box-sizing: content-box;\n}",
              "عرض دیده‌شده: 300 + 40 + 10."),
            S("border-box",
              "همان width شامل پدینگ و خط می‌شود — کار روزمره راحت‌تر است.",
              "* { box-sizing: border-box; }\n.box {\n  width: 300px;\n  padding: 20px;\n  border: 5px solid gray;\n}",
              "حالا کل جعبه ۳۰۰ می‌ماند."),
            S("padding جداگانه",
              "می‌توانی هر طرف را جدا بدهی.",
              ".card { padding: 12px 16px; }\n.card { padding-top: 8px; }",
              "۱۲ بالا/پایین، ۱۶ چپ/راست."),
            S("margin روی هم",
              "دو margin عمودی گاهی یکی می‌شوند.",
              ".a { margin-bottom: 20px; }\n.b { margin-top: 30px; }\n/* فاصله بینشان اغلب 30px است نه 50 */",
              "اگر فاصله عجیب دیدی collapse را به یاد بیاور."),
        ]
        warn = "برای کنترل عرض در کل سایت معمولاً * { box-sizing: border-box; } بگذار."
    elif "flex" in low or "فلکس" in title:
        secs = [
            S("فلکس چیست", "بچه‌ها را در یک راستا می‌چیند.",
              ".row {\n  display: flex;\n  gap: 12px;\n  align-items: center;\n  justify-content: space-between;\n}",
              "gap فاصله بین بچه‌ها.", "justify محور اصلی.", "align محور عمود."),
            S("جهت", "row افقی، column عمودی.",
              ".col { display: flex; flex-direction: column; gap: 8px; }",
              "زیر هم می‌آیند."),
            S("رشد آیتم", "flex می‌گوید چقدر از فضای خالی بگیرد.",
              ".item { flex: 1 1 180px; }\n.row { display: flex; flex-wrap: wrap; }",
              "wrap در عرض کم می‌شکند."),
            S("منوی افقی", "کاربرد واقعی.",
              "nav { display: flex; gap: 16px; }\nnav a { padding: 8px 12px; }",
              "لینک‌ها کنار هم."),
            S("وسط‌چین", "افقی و عمودی.",
              ".hero {\n  display: flex;\n  min-height: 40vh;\n  align-items: center;\n  justify-content: center;\n}",
              "محتوا وسط صفحه."),
        ]
        warn = "display:flex روی پدر است نه روی هر بچه."
    elif "grid" in low or "شبکه" in title:
        secs = [
            S("گرید چیست", "ردیف و ستون با هم.",
              ".g {\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  gap: 16px;\n}",
              "سه ستون مساوی.", "fr سهم باقی‌مانده."),
            S("۱۲ ستونه", "مثل چارچوب‌های قدیمی.",
              ".g { display: grid; grid-template-columns: repeat(12, 1fr); gap: 12px; }\n.span-6 { grid-column: span 6; }",
              "span 6 یعنی نصف ردیف."),
            S("نواحی نام‌دار", "خواناتر برای کل صفحه.",
              '.page {\n  display: grid;\n  grid-template-areas:\n    "h h"\n    "s m";\n}\n.header { grid-area: h; }',
              "h هدر، s ساید، m محتوا."),
            S("فاصله", "gap ردیف و ستون.",
              ".g { display: grid; gap: 12px 20px; }",
              "۱۲ عمودی، ۲۰ افقی."),
            S("موبایل", "یک ستون شود.",
              "@media (max-width: 700px) {\n  .g { grid-template-columns: 1fr; }\n}",
              "از ۷۰۰ به پایین یک ستون."),
        ]
        warn = "گرید دو‌بعدی است؛ فلکس یک‌بعدی. برای کل صفحه گرید مناسب‌تر است."
    else:
        secs = [
            S(f"{short} چیست",
              f"با «{short}» ظاهر را عوض می‌کنی. قانون = انتخاب‌گر + ویژگی.",
              f"/* {short} */\n.box {{\n  color: #e6edf3;\n  background: #161b22;\n  padding: 12px;\n}}",
              "color رنگ متن.", "background پشت.", "padding فاصله داخل."),
            S("انتخاب‌گر",
              "تگ، کلاس یا id.",
              "p { line-height: 1.8; }\n.note { color: #ffa657; }\n#main { max-width: 900px; }",
              "نقطه کلاس است.", "# یعنی id."),
            S("مثال کاربردی",
              "یک کارت ساده.",
              ".card {\n  border: 1px solid #30363d;\n  border-radius: 10px;\n  padding: 16px;\n  box-shadow: 0 8px 24px rgba(0,0,0,.3);\n}",
              "radius گوشه گرد.", "سایه عمق می‌دهد."),
            S("حالت‌ها",
              "hover وقتی ماوس روی عنصر است.",
              "a { color: #58a6ff; text-decoration: none; }\na:hover { text-decoration: underline; }\nbutton:focus-visible { outline: 2px solid #58a6ff; }",
              "فوکوس کیبورد را پاک نکن."),
            S("واکنش‌گرا",
              "در عرض کم قوانین عوض شود.",
              "@media (max-width: 700px) {\n  .row { flex-direction: column; }\n  body { font-size: 14px; }\n}",
              "موبایل یک ستون."),
            S("اشتباه رایج",
              "اگر اثر ندیدی لینک CSS یا غلط املایی ویژگی را چک کن.",
              '<link rel="stylesheet" href="style.css">\n/* نام فایل باید دقیقاً همین باشد */',
              "مسیر غلط یعنی هیچ استایلی نمی‌آید."),
        ]
        warn = "نقطه‌ویرگول انتهای هر ویژگی را نگذار؛ قانون بعدی هم ممکن است خراب شود."
    summary = [
        f"موضوع: {short}.",
        "قانون CSS روی انتخاب‌گر اعمال می‌شود.",
        "اول روی یک جعبه کوچک امتحان کن.",
        "در عرض موبایل هم چک کن.",
        "اگر نشد، کش مرورگر را تازه کن.",
    ]
    return make(title, intro, secs, summary, warn=warn if 'warn' in dir() else "ویژگی را درست بنویس: color نه colour در CSS استاندارد وب (هر دو بعضی جاها کار می‌کند اما color استاندارد است).", related=related_for("css", title), where=where)

# ===================== JAVASCRIPT =====================
def js_lesson(title):
    short, inner = parse_title(title)
    intro = f"در جاوااسکریپت، «{short}» بخشی از رفتار صفحه است. JS بعد از HTML/CSS اجرا می‌شود و صفحه را زنده می‌کند."
    where = f"کلیک، فرم، محاسبه، درخواست به سرور؛ هر جا به «{short}» نیاز داری."
    low = (title + " " + inner).lower()

    if any(k in low for k in ["variable", "let", "const", "var", "متغیر"]):
        secs = [
            S("متغیر چیست", "جعبه با اسم. let قابل تغییر، const بعد از مقداردهی عوض نمی‌شود.",
              "let age = 18;\nconst PI = 3.14;\nage = 19;\nconsole.log(age, PI);",
              "age را می‌شود عوض کرد.", "PI را عوض کنی خطا می‌گیری."),
            S("چرا const پیش‌فرض خوب است", "جلوی عوض شدن تصادفی را می‌گیرد.",
              "const name = \"سارا\";\n// name = \"علی\";  // TypeError\nconsole.log(name);",
              "برای مقدار ثابت از const."),
            S("محدوده بلوک", "let و const داخل {} می‌میرند.",
              "{\n  let x = 1;\n}\n// console.log(x);  // ReferenceError",
              "بیرون بلوک x نیست."),
            S("انواع ساده", "عدد، رشته، بولین.",
              "let n = 10;\nlet s = \"hi\";\nlet ok = true;\nconsole.log(typeof n, typeof s, typeof ok);",
              "typeof نوع را به رشته می‌گوید."),
            S("آرایه و شیء با const", "خود جعبه ثابت است؛ داخلش می‌تواند عوض شود.",
              "const a = [1];\na.push(2);\nconsole.log(a);",
              "push مجاز است.", "a = [] خطا است."),
        ]
    elif any(k in low for k in ["string", "رشته"]):
        secs = [
            S("رشته چیست", "متن داخل ' یا \" یا `.",
              "const s = \"JavaScript\";\nconsole.log(s.length);\nconsole.log(s[0]);",
              "length تعداد نویسه‌ها.", "[0] اولی."),
            S("قالب قالبی", "داخل ` می‌توانی ${} بگذاری.",
              "const n = \"علی\";\nconsole.log(`سلام ${n}`);",
              "مقدار داخل متن می‌آید."),
            S("جستجو", "includes و indexOf.",
              "const t = \"hello world\";\nconsole.log(t.includes(\"world\"));\nconsole.log(t.indexOf(\"o\"));",
              "true", "اولین o در ایندکس ۱."),
            S("برش و جایگزینی", "slice و replace.",
              "const t = \"JavaScript\";\nconsole.log(t.slice(0, 4));\nconsole.log(t.replace(\"Java\", \"Type\"));",
              "Java", "TypeScript — اصل t عوض نمی‌شود."),
            S("شکستن", "split آرایه می‌سازد.",
              "console.log(\"a,b,c\".split(\",\"));\nconsole.log([\"a\",\"b\"].join(\"- \"));",
              "سه عضو.", "a- b"),
        ]
    elif any(k in low for k in ["array", "آرایه"]):
        secs = [
            S("آرایه چیست", "لیست مرتب با []. ایندکس از صفر.",
              "const a = [\"قرمز\", \"آبی\"];\nconsole.log(a[0], a.length);",
              "قرمز", "۲"),
            S("افزودن و حذف", "push آخر، pop آخر را برمی‌دارد.",
              "const a = [1, 2];\na.push(3);\nconsole.log(a.pop());\nconsole.log(a);",
              "pop مقدار ۳ را می‌دهد.", "می‌ماند [1,2]."),
            S("map و filter", "آرایه جدید بدون حلقه دستی.",
              "const a = [1, 2, 3, 4];\nconsole.log(a.map(x => x * 2));\nconsole.log(a.filter(x => x % 2 === 0));",
              "دو برابر.", "زوج‌ها."),
            S("find و includes", "جستجو.",
              "const a = [{id:1,n:\"a\"},{id:2,n:\"b\"}];\nconsole.log(a.find(x => x.id === 2));\nconsole.log([1,2].includes(2));",
              "شیء با id ۲.", "true"),
            S("مرتب‌سازی", "sort روی خودش. برای عدد تابع مقایسه بده.",
              "const a = [10, 2, 5];\na.sort((x, y) => x - y);\nconsole.log(a);",
              "بدون تابع، مرتب‌سازی رشته‌ای است و ۱۰ قبل ۲ می‌آید."),
        ]
    elif any(k in low for k in ["function", "تابع", "arrow"]):
        secs = [
            S("تابع معمولی", "function اسم و پرانتز.",
              "function add(a, b) {\n  return a + b;\n}\nconsole.log(add(2, 3));",
              "۵"),
            S("تابع پیکانی", "کوتاه‌تر.",
              "const add = (a, b) => a + b;\nconsole.log(add(2, 3));",
              "اگر یک عبارت باشد return لازم نیست."),
            S("پیش‌فرض", "اگر نفرستی.",
              "function greet(name = \"مهمان\") {\n  return \"سلام \" + name;\n}\nconsole.log(greet());",
              "سلام مهمان"),
            S("callback", "تابع را به تابع دیگر بده.",
              "[1,2,3].forEach(function (n) {\n  console.log(n);\n});",
              "هر عضو یک‌بار."),
            S("return", "بدون return مقدار undefined است.",
              "function f() { 2 + 2; }\nconsole.log(f());",
              "undefined چون return نبود."),
        ]
    elif any(k in low for k in ["dom", "document", "event", "رویداد"]):
        secs = [
            S("DOM چیست", "درخت تگ‌های صفحه که JS می‌تواند عوضش کند.",
              "const el = document.querySelector(\"#box\");\nel.textContent = \"سلام\";",
              "querySelector اولین مطابق را می‌گیرد."),
            S("ساختن عنصر", "createElement و append.",
              "const li = document.createElement(\"li\");\nli.textContent = \"آیتم\";\ndocument.querySelector(\"ul\").append(li);",
              "به فهرست اضافه می‌شود."),
            S("رویداد کلیک", "addEventListener.",
              "document.querySelector(\"button\").addEventListener(\"click\", () => {\n  alert(\"کلیک\");\n});",
              "هر کلیک تابع را صدا می‌زند."),
            S("خواندن فرم", "مقدار input.",
              "const v = document.querySelector(\"#name\").value.trim();\nconsole.log(v);",
              "trim فاصله اول و آخر."),
            S("classList", "کلاس را روشن/خاموش کن.",
              "document.body.classList.toggle(\"dark\");",
              "toggle اگر بود برمی‌دارد اگر نبود می‌گذارد."),
        ]
    elif any(k in low for k in ["fetch", "ajax", "json", "promise", "async"]):
        secs = [
            S("JSON چیست", "متن استاندارد برای داده.",
              "const t = JSON.stringify({name: \"علی\"});\nconsole.log(t);\nconsole.log(JSON.parse(t).name);",
              "stringify به متن.", "parse برگشت به شیء."),
            S("Promise", "کاری که بعداً تمام می‌شود.",
              "Promise.resolve(5).then(n => console.log(n + 1));",
              "۶ بعد از تمام شدن."),
            S("async/await", "خواناتر از then.",
              "async function run() {\n  const n = await Promise.resolve(3);\n  console.log(n);\n}\nrun();",
              "await فقط داخل async."),
            S("fetch", "درخواست شبکه.",
              "async function load() {\n  const r = await fetch(\"/api.json\");\n  const data = await r.json();\n  console.log(data);\n}",
              "دو await: یکی پاسخ، یکی بدنه."),
            S("خطا", "شبکه ممکن است شکست بخورد.",
              "async function load() {\n  try {\n    const r = await fetch(\"/x\");\n    if (!r.ok) throw new Error(r.status);\n  } catch (e) {\n    console.log(\"نشد\", e.message);\n  }\n}",
              "ok یعنی وضعیت ۲xx."),
        ]
    else:
        secs = [
            S(f"{short} چیست",
              f"«{short}» در جاوااسکریپت یک قطعه رفتار است. با console.log ببین چه می‌شود.",
              f"// {short}\nconst value = 10;\nconsole.log(\"مقدار\", value);\nconsole.log(typeof value);",
              "console.log در ابزار توسعه‌دهنده دیده می‌شود."),
            S("مثال با شرط",
              "مسیر برنامه را عوض کن.",
              "const n = 7;\nif (n % 2 === 0) {\n  console.log(\"زوج\");\n} else {\n  console.log(\"فرد\");\n}",
              "=== هم مقدار هم نوع را چک می‌کند."),
            S("مثال با حلقه",
              "تکرار کار.",
              "for (let i = 1; i <= 3; i++) {\n  console.log(i, i * i);\n}",
              "let i فقط مال این حلقه است."),
            S("مثال با آرایه",
              "چند مقدار.",
              "const nums = [2, 4, 6];\nconst doubled = nums.map(x => x * 2);\nconsole.log(doubled);",
              "map آرایه جدید می‌سازد."),
            S("مثال با تابع",
              "منطق را جمع کن.",
              "function sum(arr) {\n  return arr.reduce((a, b) => a + b, 0);\n}\nconsole.log(sum([1,2,3]));",
              "reduce از ۰ جمع می‌کند → ۶."),
            S("اشتباه رایج",
              "== تبدیل نوع می‌کند؛ معمولاً === بگذار.",
              "console.log(0 == \"0\");\nconsole.log(0 === \"0\");",
              "اولی true.", "دومی false."),
        ]
    summary = [
        f"موضوع: {short}.",
        "با console.log خروجی را ببین.",
        "=== برای مقایسه دقیق.",
        "const را پیش‌فرض بگذار.",
        "خطا را در کنسول بخوان نه حدس.",
    ]
    warn = "JS داخل مرورگر است. فایل را با زنده کردن صفحه ببین؛ بعضی چیزها بدون تگ HTML معنی ندارند."
    return make(title, intro, secs, summary, warn=warn, related=related_for("javascript", title), where=where)

# ===================== PHP =====================
def php_family(fn, short):
    f = (fn or short).lower()
    if f.startswith("array") or f in {"count","sizeof","in_array","sort","rsort","asort","ksort","usort","shuffle","range","compact","extract","list","current","end","next","prev","reset","key"}:
        return "array"
    if f.startswith("str") or f.startswith("substr") or f in {"trim","ltrim","rtrim","explode","implode","join","strlen","sprintf","printf","nl2br","htmlspecialchars","strip_tags","md5","sha1","ucfirst","ucwords","lcfirst","chr","ord","addslashes","stripslashes","number_format","wordwrap"}:
        return "string"
    if f.startswith("date") or f.startswith("time") or f.startswith("strtotime") or f.startswith("gm") or f.startswith("timezone") or f.startswith("cal_") or "jd" in f:
        return "date"
    if f.startswith("preg_") or "regex" in f:
        return "regex"
    if f.startswith("file") or f.startswith("fopen") or f.startswith("fwrite") or f.startswith("fread") or f in {"unlink","mkdir","rmdir","copy","rename","glob","is_file","is_dir","move_uploaded_file"}:
        return "file"
    if f.startswith("json"):
        return "json"
    if f.startswith("mysqli") or f in {"query","prepare","fetch_assoc","insert_id","commit","rollback"}:
        return "db"
    if f.startswith("ftp_"):
        return "ftp"
    if f.startswith("xml") or f.startswith("simplexml") or f.startswith("libxml"):
        return "xml"
    if f.startswith("filter_"):
        return "filter"
    if f.startswith("ob_"):
        return "ob"
    if f.startswith("zip_"):
        return "zip"
    if f.startswith("ftp") or f.startswith("mail"):
        return "net"
    if f in {"abs","ceil","floor","round","sqrt","pow","max","min","sin","cos","tan","pi","log","exp","intdiv"} or f.startswith("mt_") or f in {"rand","srand"}:
        return "math"
    if f.startswith("is_"):
        return "type"
    return "misc"

def php_lesson(title):
    short, inner = parse_title(title)
    fn = inner.split()[0] if inner else ""
    fn = fn.replace("()", "")
    intro = f"در PHP، «{short}» یک ابزار سمت سرور است. PHP روی سرور اجرا می‌شود و معمولاً HTML یا JSON برای مرورگر می‌فرستد."
    where = f"فرم، فایل، دیتابیس، API؛ هر جا به «{short}» نیاز داری."
    fam = php_family(fn, short)
    secs = php_secs(title, short, fn, fam)
    summary = [
        f"موضوع: {short}" + (f" — {fn}()" if fn and re.match(r"^[A-Za-z_]", fn) else "") + ".",
        "کد را در فایل .php با سرور محلی اجرا کن.",
        "خروجی را در مرورگر ببین نه با دوبار کلیک خام.",
        "ورودی کاربر را مستقیم داخل SQL نچسبان.",
        "خطا را از پایین پیام بخوان.",
    ]
    warn = php_warn(fam, fn)
    return make(title, intro, secs, summary, warn=warn, related=related_for("php", title), where=where)

def php_warn(fam, fn):
    if fam == "db":
        return "هرگز متغیر کاربر را به SQL نچسبان. از prepare و ? استفاده کن."
    if fam == "file":
        return "نام فایل آپلودی را مستقیم استفاده نکن. basename و نوع فایل را چک کن."
    if fn in ("eval", "extract"):
        return f"{fn} خطرناک است اگر داده از بیرون بیاید."
    if fam == "net":
        return "mail و FTP به تنظیم سرور واقعی نیاز دارند؛ روی سیستم خانگی ممکن است کار نکنند."
    return "کد PHP باید داخل <?php ?> باشد (در فایل خالص PHP تگ پایان لازم نیست)."

def php_secs(title, short, fn, fam):
    call = fn if fn and re.match(r"^[A-Za-z_]", fn) else None
    if fam == "array":
        return [
            S("آرایه چیست", "چند مقدار در یک متغیر. اندیسی یا با کلید متنی.",
              "<?php\n$a = [\"سیب\", \"گلابی\"];\necho $a[0];\n$u = [\"name\" => \"مینا\"];\necho $u[\"name\"];\n?>",
              "ایندکس از صفر.", "کلید name."),
            S("افزودن", "[] خالی به انتها اضافه می‌کند.",
              "<?php\n$a = [1];\n$a[] = 2;\narray_push($a, 3, 4);\nprint_r($a);\n?>",
              "array_push چندتا با هم."),
            S("پیمایش", "foreach بهترین حلقه روی آرایه است.",
              "<?php\n$a = [\"a\" => 1, \"b\" => 2];\nforeach ($a as $k => $v) {\n  echo \"$k = $v\\n\";\n}\n?>",
              "هر دور کلید و مقدار."),
            S("توابع آماده", "count و in_array و sort.",
              "<?php\n$a = [3, 1, 2];\necho count($a);\nvar_dump(in_array(1, $a));\nsort($a);\nprint_r($a);\n?>",
              "sort خود آرایه را عوض می‌کند."),
            S("ادغام", "array_merge دو لیست را می‌چسباند.",
              "<?php\nprint_r(array_merge([1, 2], [3]));\n?>",
              "[1,2,3]"),
        ]
    if fam == "string":
        return [
            S("رشته در PHP", "متن داخل ' یا \".",
              "<?php\n$s = \"PHP\";\necho strlen($s);\necho $s[0];\n?>",
              "strlen تعداد بایت/نویسه (برای فارسی mb_strlen بهتر است).", "اولین نویسه."),
            S("چسباندن", "با نقطه .",
              "<?php\n$name = \"علی\";\necho \"سلام \" . $name;\n?>",
              "نقطه یعنی بچسبان."),
            S("جایگزینی و برش", "str_replace و substr.",
              "<?php\necho str_replace(\"a\", \"b\", \"banana\");\necho substr(\"Hello\", 0, 2);\n?>",
              "bnbnnb", "He"),
            S("تمیز کردن", "trim فاصله را برمی‌دارد.",
              "<?php\necho trim(\"  hi  \");\necho strtolower(\"PHP\");\n?>",
              "hi", "php"),
            S("خروجی امن در HTML", "htmlspecialchars جلوی تگ تزریقی را می‌گیرد.",
              "<?php\n$user = \"<b>x</b>\";\necho htmlspecialchars($user, ENT_QUOTES, \"UTF-8\");\n?>",
              "تگ اجرا نمی‌شود، متن دیده می‌شود."),
        ]
    if fam == "math":
        n = call or "abs"
        return [
            S(f"{n} چیست",
              f"تابع {n} یک محاسبه عددی انجام می‌دهد.",
              f"<?php\necho abs(-12);\necho \"\\n\";\necho abs(3.5);\n?>",
              "قدر مطلق ۱۲.", "۳.۵ همان می‌ماند."),
            S("با متغیر",
              "اول مقدار را در جعبه بگذار.",
              f"<?php\n$a = -7;\n$b = abs($a);\necho $b;\n?>",
              "۷"),
            S("در محاسبه واقعی",
              "فاصله دو عدد همیشه مثبت است.",
              "<?php\n$x = 10;\n$y = 18;\necho abs($x - $y);\n?>",
              "۸"),
            S("چند تابع کنار هم",
              "round و ceil و floor.",
              "<?php\necho round(3.6);\necho ceil(3.1);\necho floor(3.9);\n?>",
              "۴", "۴", "۳"),
            S("تصادفی",
              "برای تاس یا تمرین. برای امنیت random_int.",
              "<?php\necho rand(1, 6);\necho random_int(1, 6);\n?>",
              "هر دو بین ۱ و ۶.", "random_int برای چیزهای جدی‌تر."),
        ]
    if fam == "date":
        return [
            S("زمان سرور", "date قالب را روی زمان فعلی می‌گذارد.",
              "<?php\ndate_default_timezone_set(\"Asia/Tehran\");\necho date(\"Y-m-d H:i\");\n?>",
              "سال-ماه-روز ساعت:دقیقه."),
            S("مهر زمانی", "time ثانیه‌ها از ۱۹۷۰.",
              "<?php\necho time();\necho date(\"Y-m-d\", time() + 86400);\n?>",
              "۸۶۴۰۰ ثانیه = یک روز بعد."),
            S("از متن به زمان", "strtotime زبان آدمیزاد را می‌فهمد.",
              "<?php\necho date(\"Y-m-d\", strtotime(\"+1 week\"));\necho date(\"Y-m-d\", strtotime(\"2026-01-01\"));\n?>",
              "هفته بعد."),
            S("اختلاف دو تاریخ", "DateTime و diff.",
              "<?php\n$a = new DateTime(\"2026-01-01\");\n$b = new DateTime(\"2026-01-20\");\necho $a->diff($b)->days;\n?>",
              "۱۹ روز."),
            S("اعتبار تاریخ", "checkdate ماه و روز را چک می‌کند.",
              "<?php\nvar_dump(checkdate(2, 29, 2024));\nvar_dump(checkdate(2, 29, 2025));\n?>",
              "۲۰۲۴ کبیسه است.", "۲۰۲۵ نیست."),
        ]
    if fam == "file":
        return [
            S("نوشتن ساده", "file_put_contents یک‌خطی می‌نویسد.",
              "<?php\nfile_put_contents(\"a.txt\", \"سلام\\n\");\necho file_get_contents(\"a.txt\");\n?>",
              "بعد همان را می‌خواند."),
            S("باز و بست", "fopen / fwrite / fclose.",
              "<?php\n$f = fopen(\"log.txt\", \"a\");\nfwrite($f, date(\"c\") . \" ok\\n\");\nfclose($f);\n?>",
              "a یعنی به انتها اضافه کن."),
            S("وجود فایل", "قبل از خواندن چک کن.",
              "<?php\nif (file_exists(\"a.txt\")) {\n  echo filesize(\"a.txt\");\n} else {\n  echo \"نیست\";\n}\n?>",
              "filesize به بایت."),
            S("آپلود", "از $_FILES و move_uploaded_file.",
              "<?php\n$tmp = $_FILES[\"f\"][\"tmp_name\"] ?? \"\";\n$name = basename($_FILES[\"f\"][\"name\"] ?? \"file.bin\");\nif ($tmp && is_uploaded_file($tmp)) {\n  move_uploaded_file($tmp, \"uploads/\" . $name);\n}\n?>",
              "basename مسیر را می‌بُرد.", "is_uploaded_file امنیت."),
            S("پوشه", "mkdir و scandir.",
              "<?php\nif (!is_dir(\"tmp_dir\")) mkdir(\"tmp_dir\");\nprint_r(scandir(\".\"));\n?>",
              "scandir نام فایل‌ها را می‌دهد."),
        ]
    if fam == "db":
        return [
            S("اتصال", "mysqli به MySQL وصل می‌شود.",
              "<?php\n$mysqli = new mysqli(\"localhost\", \"root\", \"\", \"test\");\nif ($mysqli->connect_error) {\n  die(\"اتصال نشد\");\n}\n$mysqli->set_charset(\"utf8mb4\");\n?>",
              "utf8mb4 برای فارسی و ایموجی."),
            S("درج امن", "prepare با ?.",
              "<?php\n$stmt = $mysqli->prepare(\"INSERT INTO users (name) VALUES (?)\");\n$stmt->bind_param(\"s\", $name);\n$name = \"سارا\";\n$stmt->execute();\necho $mysqli->insert_id;\n?>",
              "s یعنی رشته.", "insert_id آخرین id."),
            S("خواندن", "SELECT و fetch_assoc.",
              "<?php\n$r = $mysqli->query(\"SELECT id, name FROM users LIMIT 10\");\nwhile ($row = $r->fetch_assoc()) {\n  echo htmlspecialchars($row[\"name\"]);\n}\n?>",
              "هر دور یک ردیف."),
            S("به‌روزرسانی", "UPDATE با WHERE.",
              "<?php\n$stmt = $mysqli->prepare(\"UPDATE users SET name=? WHERE id=?\");\n$stmt->bind_param(\"si\", $name, $id);\n$name = \"رضا\"; $id = 1;\n$stmt->execute();\n?>",
              "بدون WHERE همه ردیف‌ها عوض می‌شوند."),
            S("تراکنش", "چند کار یا همه یا هیچ‌کدام.",
              "<?php\n$mysqli->begin_transaction();\ntry {\n  $mysqli->query(\"INSERT INTO t (n) VALUES (1)\");\n  $mysqli->commit();\n} catch (Exception $e) {\n  $mysqli->rollback();\n}\n?>",
              "rollback برمی‌گرداند."),
        ]
    if fam == "json":
        return [
            S("encode", "آرایه به متن JSON.",
              "<?php\necho json_encode([\"name\" => \"علی\"], JSON_UNESCAPED_UNICODE);\n?>",
              "بدون UNESCAPED_UNICODE فارسی \\u می‌شود."),
            S("decode", "متن به آرایه.",
              "<?php\n$o = json_decode('{\"a\":1}', true);\necho $o[\"a\"];\n?>",
              "true یعنی آرایه انجمنی نه شیء."),
            S("API کوچک", "هدر JSON بفرست.",
              "<?php\nheader(\"Content-Type: application/json; charset=utf-8\");\necho json_encode([\"ok\" => true]);\n?>",
              "مرورگر/JS می‌فهمد نوع JSON است."),
            S("خطای decode", "json_last_error_msg.",
              "<?php\njson_decode(\"{bad\");\necho json_last_error_msg();\n?>",
              "پیام می‌گوید JSON خراب است."),
            S("لیست", "آرایه عددی JSON آرایه می‌شود.",
              "<?php\necho json_encode([1, 2, 3]);\n?>",
              "[1,2,3]"),
        ]
    if fam == "regex":
        return [
            S("تطبیق", "preg_match آیا الگو هست.",
              "<?php\nvar_dump(preg_match(\"/^\\\\d+$/\", \"123\"));\n?>",
              "فقط رقم از اول تا آخر."),
            S("همه تطبیق‌ها", "preg_match_all.",
              "<?php\npreg_match_all(\"/\\\\d+/\", \"a12 b34\", $m);\nprint_r($m[0]);\n?>",
              "12 و 34."),
            S("جایگزینی", "preg_replace.",
              "<?php\necho preg_replace(\"/\\\\s+/\", \" \", \"a   b\");\n?>",
              "فاصله‌های اضافه یکی می‌شود."),
            S("شکستن", "preg_split.",
              "<?php\nprint_r(preg_split(\"/\s*,\\s*/\", \"a, b,c\"));\n?>",
              "کاما با فاصله دورش."),
            S("ایمیل ساده", "filter_var معمولاً بهتر از regex دستی است.",
              "<?php\nvar_dump(filter_var(\"a@b.com\", FILTER_VALIDATE_EMAIL));\n?>",
              "فرمت را چک می‌کند نه وجود صندوق را."),
        ]
    if fam == "filter":
        return [
            S("filter_var", "اعتبارسنجی یا پاک‌سازی.",
              "<?php\nvar_dump(filter_var(\"a@b.com\", FILTER_VALIDATE_EMAIL));\necho filter_var(\"42abc\", FILTER_SANITIZE_NUMBER_INT);\n?>",
              "ایمیل معتبر.", "رقم‌ها می‌مانند."),
            S("ورودی فرم", "filter_input مستقیم از GET/POST.",
              "<?php\n$e = filter_input(INPUT_POST, \"email\", FILTER_VALIDATE_EMAIL);\nif (!$e) echo \"ایمیل بد\";\n?>",
              "false یعنی نامعتبر."),
            S("عدد با بازه", "گزینه min و max.",
              "<?php\n$opts = [\"options\" => [\"min_range\" => 1, \"max_range\" => 120]];\nvar_dump(filter_var(20, FILTER_VALIDATE_INT, $opts));\n?>",
              "۲۰ قبول است."),
            S("لیست فیلترها", "چه فیلترهایی هست.",
              "<?php\nprint_r(filter_list());\n?>",
              "نام‌ها را می‌بینی."),
            S("آرایه ورودی", "چند فیلد با هم.",
              "<?php\n$def = [\"age\" => FILTER_VALIDATE_INT, \"name\" => FILTER_UNSAFE_RAW];\n# filter_input_array(INPUT_POST, $def);\n?>",
              "هر فیلد فیلتر خودش را دارد."),
        ]
    # generic 5 examples
    demo = call or "strlen"
    return [
        S(f"{short} چیست",
          f"این درس «{short}» را با مثال کوچک نشان می‌دهد" + (f". نام تابع: {demo}()" if call else ".") + "",
          f"<?php\n// {short}\n$x = \"سلام PHP\";\necho $x;\necho \"\\n\";\necho strlen(\"PHP\");\n?>",
          "echo چاپ می‌کند.", "strlen برای نمونه یک تابع آماده است."),
        S("با متغیر",
          "مقدار را اول ذخیره کن بعد استفاده کن.",
          "<?php\n$name = \"سارا\";\n$n = 18;\necho $name . \" \" . $n;\n?>",
          "نقطه متن‌ها را می‌چسباند."),
        S("با شرط",
          "بر اساس داده مسیر عوض می‌شود.",
          "<?php\n$age = 20;\nif ($age >= 18) {\n  echo \"بالغ\";\n} else {\n  echo \"نوجوان\";\n}\n?>",
          "شرط درست است."),
        S("با آرایه",
          "چند مقدار با foreach.",
          "<?php\n$a = [1, 2, 3];\nforeach ($a as $v) {\n  echo $v * 2 . \" \";\n}\n?>",
          "۲ ۴ ۶"),
        S("با تابع خودت",
          "منطق تکراری را جمع کن.",
          "<?php\nfunction double($n) {\n  return $n * 2;\n}\necho double(5);\n?>",
          "۱۰"),
        S("خروجی امن",
          "اگر داده از کاربر است htmlspecialchars.",
          "<?php\n$q = $_GET[\"q\"] ?? \"\";\necho htmlspecialchars($q, ENT_QUOTES, \"UTF-8\");\n?>",
          "?? اگر نبود رشته خالی."),
    ]

# ===================== BUILD =====================
builders = {
    "python": py_lesson,
    "html": html_lesson,
    "css": css_lesson,
    "javascript": js_lesson,
    "php": php_lesson,
}

data = {}
for lang, ts in titles.items():
    fn = builders[lang]
    data[lang] = [fn(t) for t in ts]
    print(lang, len(data[lang]), "avg", int(sum(len(x["h"]) for x in data[lang]) / len(data[lang])), "codes0", data[lang][0]["h"].count("class=\"code\""))

# verify python numbers
nb = next(x for x in data["python"] if x["t"].startswith("اعداد"))
print("numbers codes", nb["h"].count("class=\"code\""), "has int section", "int: اعداد صحیح" in nb["h"])

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
<div class="logo">مدرسه برنامه‌نویسان <span>چند مثال در هر درس</span></div>
<nav>
<a href="#" id="btnHome" class="active">خانه</a>
<a href="/madrase-complete.html" id="btnDl" download="madrase-complete.html">دانلود فایل</a>
</nav>
</header>
<div class="wrap">
<div id="homeBlock">
<div class="hero">
<h1>پایتون · HTML · CSS · JavaScript · PHP</h1>
<p>هر درس مثل «اعداد»: چند بخش · چند مثال · مشاهده در ادیتور · جمع‌بندی</p>
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
<div id="edBack"><div id="edBox">
<h3>مشاهده در ادیتور</h3>
<pre id="edCode"></pre>
<div class="navbtn">
<button type="button" id="edCopy">کپی</button>
<button type="button" id="edClose">بستن</button>
</div>
</div></div>
<footer>مثال زیاد · توضیح ساده · بدون حاشیه</footer>
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
  if (p) p.onclick = function() { currentIdx--; renderSide(); renderLesson(); window.scrollTo(0,0); };
  if (n) n.onclick = function() { currentIdx++; renderSide(); renderLesson(); window.scrollTo(0,0); };
  card.querySelectorAll(".trybtn").forEach(function(btn) {
    btn.onclick = function() {
      var wrap = btn.previousElementSibling;
      var codeEl = wrap && wrap.querySelector ? wrap.querySelector(".code") : wrap;
      document.getElementById("edCode").textContent = codeEl ? codeEl.textContent : "";
      document.getElementById("edBack").style.display = "flex";
    };
  });
}
document.getElementById("edClose").onclick = function(){ document.getElementById("edBack").style.display = "none"; };
document.getElementById("edBack").onclick = function(e){ if (e.target.id === "edBack") document.getElementById("edBack").style.display = "none"; };
document.getElementById("edCopy").onclick = function(){
  var t = document.getElementById("edCode").textContent;
  if (navigator.clipboard) navigator.clipboard.writeText(t);
};
</script>
</body>
</html>
'''
outp = Path("/workspace/artifacts/madrase-complete.html")
outp.write_text(doc, encoding="utf-8")
Path("/workspace/artifacts/madrase-test.html").write_text(doc, encoding="utf-8")
Path("/workspace/public/index.html").write_text(doc, encoding="utf-8")
Path("/workspace/public/madrase-complete.html").write_text(doc, encoding="utf-8")
print("BYTES", len(doc.encode("utf-8")))
for k,v in data.items():
    codes = [x["h"].count('class="code"') for x in v]
    print(k, "lessons", len(v), "min_codes", min(codes), "avg_codes", round(sum(codes)/len(codes),1), "avg_len", int(sum(len(x["h"]) for x in v)/len(v)))

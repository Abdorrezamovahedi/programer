# -*- coding: utf-8 -*-
"""Line-by-line Persian explanations for example code."""
import re

FA = "۱۲۳۴۵۶۷۸۹۰"
# keep 1,2,3 in explanations; clearer with mixed code

def _n(i):
    return str(i)

def detect_lang(code):
    s = code.strip()
    if s.startswith("<?php") or "<?php" in s[:40]:
        return "php"
    if s.startswith("<!DOCTYPE") or (s.startswith("<") and "<?" not in s[:15] and not s.startswith("<!--")):
        return "html"
    if "console.log" in s or re.search(r"\b(const|let|document)\b", s) or "addEventListener" in s:
        return "js"
    if re.search(r"\{[^}]*:[^}]*;[^}]*\}", s, re.S) or (re.search(r"^\s*[.#@a-zA-Z].*\{", s, re.M) and ";" in s and "def " not in s and "function " not in s):
        return "css"
    if s.startswith("pip ") or s.startswith("python "):
        return "shell"
    return "python"

def explain_code(code):
    lang = detect_lang(code)
    out = []
    i = 0
    for raw in code.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        i += 1
        text = explain_line(lang, line.strip(), raw)
        out.append(f"<strong>خط {_n(i)}:</strong> {text}")
    if not out:
        out.append("این بلوک خالی است؛ هنوز دستوری برای اجرا ندارد.")
    return out

def explain_line(lang, s, raw=""):
    if lang == "python":
        return py_line(s)
    if lang == "js":
        return js_line(s)
    if lang == "php":
        return php_line(s)
    if lang == "css":
        return css_line(s)
    if lang == "html":
        return html_line(s)
    return shell_line(s)

def strip_comment_py(s):
    if s.strip().startswith("#"):
        return None, s.strip()[1:].strip()
    if " #" in s:
        code, c = s.split(" #", 1)
        return code.strip(), c.strip()
    return s, None

def py_line(s):
    code, cmt = strip_comment_py(s)
    if code is None:
        return f"این خط فقط توضیح است و اجرا نمی‌شود. نوشته: «{cmt}». کامنت برای انسان است تا هدف کد را بفهمد."
    extra = f" بعد از دستور، توضیح نویسنده آمده: «{cmt}»." if cmt else ""
    t = code

    if t.startswith("import ") and " as " in t:
        m = re.match(r"import (\S+) as (\S+)", t)
        if m:
            return f"ماژول «{m.group(1)}» را می‌آورد و اسم کوتاه «{m.group(2)}» به آن می‌دهد. ماژول یعنی بسته ابزار آماده. از این به بعد با اسم کوتاه صدا زده می‌شود.{extra}"
    if t.startswith("import "):
        name = t.split()[1].split(",")[0]
        return f"ماژول «{name}» را وارد برنامه می‌کند. بدون این خط، ابزارهای داخل آن ماژول شناخته نمی‌شوند.{extra}"
    if t.startswith("from "):
        m = re.match(r"from (\S+) import (.+)", t)
        if m:
            return f"از ماژول «{m.group(1)}» فقط «{m.group(2)}» را برمی‌دارد تا لازم نباشد هر بار اسم ماژول را بنویسی.{extra}"

    if t.startswith("def "):
        name = re.match(r"def\s+(\w+)", t)
        nm = name.group(1) if name else "تابع"
        args = ""
        if "(" in t:
            args = t[t.find("(")+1:t.rfind(")") if ")" in t else None]
            args = args or "بدون ورودی"
        return f"یک تابع با اسم «{nm}» می‌سازد. تابع یعنی یک کار با اسم، که بعداً صدا می‌زنی. پرانتز جای ورودی است ({args}). دو نقطه یعنی بدنه از خط بعد با تورفتگی شروع می‌شود.{extra}"
    if t.startswith("class "):
        name = re.match(r"class\s+(\w+)", t)
        nm = name.group(1) if name else "کلاس"
        more = " داخل پرانتز نام کلاس پدر است؛ یعنی از آن ارث می‌برد." if "(" in t and not t.endswith("():") and "()" not in t[:t.find(":")+1] else " این یک قالب خالی برای ساخت شیء است."
        if re.search(r"class\s+\w+\(\w+\)", t):
            more = " نام داخل پرانتز کلاس پدر است؛ این کلاس ویژگی‌های پدر را می‌گیرد (وراثت)."
        return f"کلاس «{nm}» را تعریف می‌کند. کلاس نقشه است؛ بعداً با صدا زدن اسمش شیء می‌سازی.{more}{extra}"
    if t.startswith("return "):
        val = t[7:].strip()
        return f"نتیجه را از تابع بیرون می‌فرستد و تابع همین‌جا تمام می‌شود. مقداری که برمی‌گردد: «{val}». کسی که تابع را صدا زده این مقدار را تحویل می‌گیرد.{extra}"
    if t == "return":
        return f"از تابع بیرون می‌آید بدون اینکه مقداری برگرداند (نتیجه None است).{extra}"
    if t.startswith("yield "):
        return f"یک مقدار را به بیرون می‌دهد ولی تابع را کامل نمی‌بندد (جنریتور). دفعه بعد از همین‌جا ادامه می‌دهد. مقدار: «{t[6:]}».{extra}"

    if t.startswith("if ") and t.endswith(":"):
        cond = t[3:-1].strip()
        return f"شرط را چک می‌کند: «{cond}». اگر این عبارت درست (True) باشد، خط‌های تو رفتهٔ بعدی اجرا می‌شوند. دو نقطه یعنی شروع بلوک. در پایتون فاصلهٔ اول خط نشان می‌دهد این خط مال همین if است.{extra}"
    if t.startswith("elif ") and t.endswith(":"):
        return f"اگر ifهای قبلی غلط بودند، این شرط را چک کن: «{t[5:-1].strip()}». فقط اولین شرط درست اجرا می‌شود.{extra}"
    if t == "else:" or t.startswith("else:"):
        return f"اگر هیچ‌کدام از شرط‌های قبلی درست نبود، این بخش اجرا می‌شود. مثل راه آخر.{extra}"
    if t.startswith("for ") and " in " in t:
        m = re.match(r"for\s+(.+?)\s+in\s+(.+):", t)
        if m:
            return f"حلقه: برای هر عضو داخل «{m.group(2).rstrip(':')}» یک دور تکرار می‌کند و آن عضو را در «{m.group(1)}» می‌گذارد. تا عضو تمام نشود ادامه دارد.{extra}"
    if t.startswith("while ") and t.endswith(":"):
        return f"تا وقتی شرط «{t[6:-1].strip()}» درست است، بدنه را تکرار می‌کند. اگر شرط هیچ‌وقت غلط نشود حلقه تمام نمی‌شود؛ پس داخل بدنه باید چیزی عوض شود.{extra}"
    if t.startswith("try:"):
        return f"این کار را امتحان کن. اگر وسطش خطا آمد برنامه نایستد و برو به except.{extra}"
    if t.startswith("except"):
        return f"اگر خطای گفته‌شده رخ داد، به‌جای خراب شدن برنامه این بخش را اجرا کن. «{t}» مشخص می‌کند کدام نوع خطا گرفته شود.{extra}"
    if t.startswith("finally:"):
        return f"چه خطا بشود چه نشود، آخر کار این بخش اجرا می‌شود (مثلاً بستن فایل).{extra}"
    if t.startswith("with "):
        return f"مدیریت منبع: «{t}». with فایل یا اتصال را باز می‌کند و وقتی بلوک تمام شد خودکار می‌بندد تا یادت نرود.{extra}"
    if t.startswith("pass"):
        return f"عمداً هیچ کاری نکن. فقط جای خالی قانونی است تا پایتون به‌خاطر بدنهٔ خالی خطا ندهد.{extra}"
    if t.startswith("break"):
        return f"از حلقه یا match همین حالا خارج شو؛ بقیهٔ دورها اجرا نمی‌شوند.{extra}"
    if t.startswith("continue"):
        return f"این دور حلقه را رها کن و برو دور بعد. خط‌های پایین‌تر این دور اجرا نمی‌شوند.{extra}"
    if t.startswith("global "):
        return f"می‌گوید متغیر «{t[7:]}» همان متغیر بیرون تابع است؛ نه یک جعبهٔ جدید داخل تابع.{extra}"
    if t.startswith("lambda ") or " lambda " in t:
        return f"یک تابع خیلی کوتاه در همین خط می‌سازد. سمت چپ ورودی است، سمت راست بعد از : نتیجه. «{t}».{extra}"
    if t.startswith("match ") and t.endswith(":"):
        return f"مقدار «{t[6:-1].strip()}» را با چند حالت (case) مقایسه می‌کند؛ شبیه چند if پشت سر هم ولی خواناتر.{extra}"
    if t.startswith("case "):
        return f"اگر مقدار match با «{t[5:].rstrip(':')}» یکی بود، این بخش اجرا شود.{extra}"

    if t.startswith("print("):
        inner = t[6:-1] if t.endswith(")") else t[6:]
        if inner.startswith("type("):
            return f"اول type نوع مقدار داخل پرانتز را می‌فهمد (مثلاً int یا str)، بعد print همان نوع را روی صفحه نشان می‌دهد تا ببینی جعبه چه جنسی است. داخل: {inner}.{extra}"
        if inner.startswith("len("):
            return f"len تعداد عضو یا نویسه را می‌شمارد؛ print همان عدد را نشان می‌دهد. داخل: {inner}.{extra}"
        return f"نتیجه را روی صفحه نشان می‌دهد تا ببینی برنامه چه کرده. چیزی که چاپ می‌شود داخل پرانتز است: {inner}. اگر چند چیز با کاما جدا شوند، کنار هم چاپ می‌شوند.{extra}"

    if "+=" in t or "-=" in t or "*=" in t or "/=" in t:
        op = re.search(r"(\+=|-=|\*=|/=)", t).group(1)
        name = t.split(op)[0].strip()
        val = t.split(op)[1].strip()
        mean = {"+=": "به مقدار قبلی اضافه کن", "-=": "از مقدار قبلی کم کن", "*=": "در مقدار قبلی ضرب کن", "/=": "بر مقدار قبلی تقسیم کن"}[op]
        return f"متغیر «{name}» را درجا عوض می‌کند: {mean} ({val}). یعنی اول حساب کن، بعد همان جعبه را با نتیجهٔ جدید پر کن.{extra}"

    if t.endswith(":") and not t.startswith("@") and "=" not in t.split(":")[0]:
        return f"شروع یک بلوک جدید است («{t}»). خط‌های بعد باید تو بروند تا مال همین بلوک حساب شوند.{extra}"

    if t.startswith("@"):
        return f"دکوراتور «{t}»: تابع پایینی را می‌پیچد؛ یعنی قبل/بعد از اجرای آن کار اضافه می‌کند.{extra}"

    # assignment
    if re.match(r"^[\w,\s\.\*]+ = ", t) and "==" not in t.split("=")[0]:
        left, right = t.split("=", 1)
        left, right = left.strip(), right.strip()
        if "input(" in right:
            return f"از کاربر سؤال می‌کند و جواب را در «{left}» می‌گذارد. توجه: input همیشه متن برمی‌گرداند؛ اگر عدد می‌خواهی باید int کنی.{extra}"
        if right.startswith("[") and right.endswith("]"):
            return f"یک لیست می‌سازد و در «{left}» می‌گذارد. [] یعنی چند مقدار پشت‌سرهم. اعضا با کاما جدا می‌شوند: {right}.{extra}"
        if right.startswith("{") and ":" in right:
            return f"یک دیکشنری می‌سازد (کلید به مقدار) و در «{left}» می‌گذارد. سمت چپ : کلید است، سمت راست مقدار.{extra}"
        if right.startswith("{") and ":" not in right:
            return f"یک مجموعه (set) می‌سازد و در «{left}» می‌گذارد. عضو تکراری نگه داشته نمی‌شود.{extra}"
        if right.startswith("(") and right.endswith(")"):
            return f"یک تاپل می‌سازد و در «{left}» می‌گذارد. تاپل مثل لیست است ولی معمولاً بعداً عوض نمی‌شود.{extra}"
        if right.startswith(("int(", "float(", "str(", "bool(", "list(", "dict(", "set(", "tuple(", "complex(")):
            fn = right.split("(")[0]
            return f"مقدار را به نوع «{fn}» تبدیل می‌کند و در «{left}» می‌گذارد. خود مقدار قبلی عوض نمی‌شود؛ یک مقدار جدید ساخته می‌شود.{extra}"
        if right.startswith(("len(", "type(", "sum(", "max(", "min(", "sorted(", "abs(")):
            fn = right.split("(")[0]
            meanings = {
                "len": "تعداد را می‌شمارد",
                "type": "جنس مقدار را می‌گوید",
                "sum": "همه را جمع می‌کند",
                "max": "بزرگ‌ترین را برمی‌دارد",
                "min": "کوچک‌ترین را برمی‌دارد",
                "sorted": "نسخهٔ مرتب می‌سازد بدون عوض کردن اصل",
                "abs": "قدر مطلق می‌گیرد (منفی را مثبت می‌کند)",
            }
            return f"تابع آمادهٔ {fn} {meanings.get(fn, 'کار مشخصی')} روی ورودی داخل پرانتز. نتیجه در «{left}» ذخیره می‌شود.{extra}"
        if "." in right and "(" in right:
            return f"روی یک شیء متد صدا می‌زند: «{right}». نقطه یعنی «از این شیء این کار را بخواه». نتیجه در «{left}» ذخیره می‌شود.{extra}"
        if right in ("True", "False", "None"):
            mean = {"True": "درست", "False": "غلط", "None": "خالی / هیچ"}[right]
            return f"جعبه «{left}» با مقدار {right} ({mean}) پر می‌شود.{extra}"
        if right.startswith(("f\"", "f'", "F\"", "F'")):
            return f"یک متن قالبی می‌سازد و در «{left}» می‌گذارد. f قبل گیومه یعنی داخل {{}} مقدار متغیر جایگزین شود.{extra}"
        if right[0] in "\"'":
            return f"جعبه «{left}» با متن پر می‌شود. گیومه می‌گوید این عدد نیست، نوشته است: {right}.{extra}"
        return f"جعبه «{left}» ساخته یا به‌روز می‌شود و مقدار سمت راست داخلش می‌رود: {right}. علامت = یعنی بگذار داخل جعبه، نه تساوی ریاضی.{extra}"

    if t.endswith(")") and "(" in t and "=" not in t.split("(")[0]:
        fn = t.split("(")[0].strip()
        inner = t[t.find("(")+1:t.rfind(")")]
        hints = {
            "append": "به آخر لیست یک عضو اضافه می‌کند",
            "insert": "در یک جای مشخص عضو می‌گذارد",
            "remove": "اولین مقدار برابر را از لیست حذف می‌کند",
            "pop": "یک عضو را برمی‌دارد و برمی‌گرداند (پیش‌فرض آخر)",
            "sort": "همان لیست را سر جایش مرتب می‌کند",
            "reverse": "ترتیب همان لیست را برعکس می‌کند",
            "extend": "اعضای یک لیست دیگر را به این یکی می‌چسباند",
            "clear": "همه اعضا را خالی می‌کند",
            "copy": "یک کپی جدا می‌سازد",
            "get": "از دیکشنری می‌خواند؛ اگر نبود پیش‌فرض می‌دهد",
            "items": "کلید و مقدار را با هم می‌دهد تا در حلقه استفاده شود",
            "keys": "فقط کلیدها را می‌دهد",
            "values": "فقط مقدارها را می‌دهد",
            "update": "دیکشنری را با کلیدهای جدید به‌روز می‌کند",
            "add": "به مجموعه عضو اضافه می‌کند",
            "discard": "از مجموعه حذف می‌کند و اگر نبود خطا نمی‌دهد",
            "strip": "فاصله اول و آخر متن را می‌بُرد",
            "split": "متن را از روی جداکننده می‌شکند و لیست می‌سازد",
            "join": "اعضای لیست را با یک جداکننده به یک متن تبدیل می‌کند",
            "replace": "در متن، یک تکه را با تکه دیگر عوض می‌کند",
            "upper": "حروف را بزرگ می‌کند و متن جدید می‌دهد",
            "lower": "حروف را کوچک می‌کند",
            "format": "جاهای خالی متن را با مقدار پر می‌کند",
            "read": "محتوای فایل را می‌خواند",
            "write": "داخل فایل می‌نویسد",
            "close": "فایل را می‌بندد",
            "append": "به آخر اضافه می‌کند",
        }
        base = fn.split(".")[-1]
        if "." in fn:
            obj = fn.rsplit(".", 1)[0]
            mean = hints.get(base, f"متد {base} را روی «{obj}» اجرا می‌کند")
            return f"از «{obj}» کار «{base}» را می‌خواهد. {mean}. ورودی داخل پرانتز: {inner or 'بدون ورودی'}.{extra}"
        mean = hints.get(base, f"تابع {fn} را صدا می‌زند")
        return f"{mean}. پرانتز یعنی این تابع را الان اجرا کن. ورودی‌ها: {inner or 'هیچ'}.{extra}"

    if t.startswith("#"):
        return f"توضیح است، اجرا نمی‌شود: «{t[1:].strip()}»."
    return f"این دستور را اجرا می‌کند: «{t}». از چپ به راست خوانده می‌شود؛ پرانتز ورودی تابع است و نقطه یعنی دسترسی به بخش یا متد.{extra}"


def js_line(s):
    t = s.strip()
    extra = ""
    if "//" in t and not t.startswith("//"):
        t, c = t.split("//", 1)
        t, extra = t.strip(), f" توضیح کنارش: «{c.strip()}»."
    if t.startswith("//"):
        return f"این خط کامنت است و اجرا نمی‌شود: «{t[2:].strip()}»."
    if t.startswith("/*") or t.startswith("*") or t.endswith("*/"):
        return "این خط بخشی از توضیح چندخطی است و اجرا نمی‌شود."
    if t.startswith("const "):
        rest = t[6:]
        name = rest.split("=")[0].strip().strip(";")
        return f"جعبه ثابت «{name}» را می‌سازد. const یعنی خود این اسم را نمی‌شود بعداً به چیز دیگری وصل کرد. اگر آرایه/شیء باشد، داخلش هنوز قابل تغییر است.{extra}"
    if t.startswith("let "):
        name = t[4:].split("=")[0].strip().strip(";")
        return f"متغیر «{name}» را می‌سازد. let یعنی بعداً می‌شود مقدارش را عوض کرد. محدودهٔ آن معمولاً همان بلوک {{ }} است.{extra}"
    if t.startswith("var "):
        return f"متغیر قدیمی با var: «{t}». در کد جدید بهتر است let یا const استفاده شود.{extra}"
    if t.startswith("function "):
        name = t.split()[1].split("(")[0]
        return f"تابع «{name}» را تعریف می‌کند. پرانتز جای ورودی است. آکولاد باز یعنی بدنه از اینجا شروع می‌شود.{extra}"
    if "=>" in t:
        return f"تابع پیکانی است: سمت چپ ورودی، سمت راست بعد از => کار تابع. کوتاه‌تر از function است. «{t}».{extra}"
    if t.startswith("if ") or t.startswith("if("):
        return f"شرط را چک می‌کند. اگر درست باشد بلوک بعدی اجرا می‌شود. شرط: داخل پرانتز. «{t}».{extra}"
    if t.startswith("else if"):
        return f"اگر if قبلی غلط بود این شرط را چک کن.{extra}"
    if t.startswith("else"):
        return f"اگر هیچ شرطی درست نبود این راه اجرا شود.{extra}"
    if t.startswith("for ") or t.startswith("for("):
        return f"حلقه تکرار. در for کلاسیک سه بخش است: شروع؛ شرط ادامه؛ افزایش. «{t}».{extra}"
    if t.startswith("while"):
        return f"تا وقتی شرط درست است تکرار می‌کند. مراقب باش شرط بالاخره غلط شود.{extra}"
    if t.startswith("return"):
        return f"نتیجه را از تابع برمی‌گرداند و تابع تمام می‌شود. «{t}».{extra}"
    if t.startswith("console.log"):
        inner = t[t.find("(")+1:t.rfind(")")] if "(" in t else ""
        return f"در کنسول مرورگر چاپ می‌کند تا تو ببینی چه شده. کاربر عادی سایت این را نمی‌بیند. مقدار: {inner}.{extra}"
    if t.startswith("document.querySelector"):
        return f"اولین عنصر صفحه که با این انتخاب‌گر جور است را پیدا می‌کند. مثل CSS: {t}.{extra}"
    if "addEventListener" in t:
        return f"گوش می‌دهد تا یک رویداد (مثلاً کلیک) رخ بدهد؛ بعد تابع را اجرا می‌کند. «{t}».{extra}"
    if t.startswith("async "):
        return f"تابع ناهمگام: می‌تواند await داشته باشد و بدون قفل کردن صفحه صبر کند.{extra}"
    if t.startswith("await "):
        return f"صبر کن تا این کار تمام شود، بعد برو خط بعد. فقط داخل async مجاز است. «{t}».{extra}"
    if "JSON.stringify" in t:
        return f"شیء یا آرایه را به متن JSON تبدیل می‌کند تا بشود فرستاد یا ذخیره کرد.{extra}"
    if "JSON.parse" in t:
        return f"متن JSON را برمی‌گرداند به شیء/آرایه تا در برنامه استفاده شود.{extra}"
    if t.startswith("try"):
        return "این کار را امتحان کن؛ اگر خطا شد catch اجرا می‌شود."
    if t.startswith("catch"):
        return "خطا را می‌گیرد تا برنامه نایستد. پارامتر داخل پرانتز همان شیء خطا است."
    if t.startswith("throw"):
        return f"عمداً خطا می‌سازد تا کسی بالاتر آن را بگیرد. «{t}»."
    if t in ("{", "}"):
        return "آکولاد شروع یا پایان یک بلوک است. دستورهای داخل یک گروه می‌شوند."
    if t.endswith("{") or t.endswith("}"):
        return f"شروع یا پایان بلوک کد. «{t}»."
    if re.search(r"\b(const|let)?\s*\w+\s*=", t) and "===" not in t and "==" not in t:
        return f"مقدار سمت راست را در متغیر سمت چپ می‌گذارد. = یعنی قرار بده. «{t}».{extra}"
    if "===" in t:
        return f"مقایسه سخت: هم مقدار هم نوع باید یکی باشد. «{t}». برای تساوی معمولی در JS معمولاً === بهتر از == است.{extra}"
    if t.endswith(";") :
        return f"یک دستور کامل است و با نقطه‌ویرگول تمام می‌شود: «{t[:-1].strip()}». نقطه‌ویرگول می‌گوید این جمله کد تمام شد.{extra}"
    return f"این دستور جاوااسکریپت را اجرا می‌کند: «{t}». پرانتز یعنی صدا زدن تابع، نقطه یعنی دسترسی به بخش یک شیء.{extra}"


def php_line(s):
    t = s.strip()
    extra = ""
    if t.startswith("//") or t.startswith("#"):
        return f"توضیح است و اجرا نمی‌شود: «{t.lstrip('/#').strip()}»."
    if t.startswith("/*") or t.startswith("*") or t.endswith("*/"):
        return "بخشی از کامنت چندخطی است؛ PHP آن را اجرا نمی‌کند."
    if t in ("<?php", "<?php"):
        return "شروع بلوک PHP. از اینجا به بعد سرور کد را اجرا می‌کند، نه اینکه همان متن را به مرورگر بدهد."
    if t == "?>":
        return "پایان بلوک PHP. بعد از این اگر HTML باشد، همان‌طور به مرورگر می‌رود."
    if t.startswith("echo ") or t.startswith("echo("):
        val = t[4:].strip().rstrip(";")
        return f"نتیجه را برای مرورگر می‌فرستد تا کاربر ببیند. چیزی که چاپ می‌شود: {val}. نقطه اگر باشد یعنی چند متن را به هم چسبانده.{extra}"
    if t.startswith("print ") or t.startswith("print("):
        return f"مثل echo چاپ می‌کند. «{t}».{extra}"
    if t.startswith("function "):
        name = t.split()[1].split("(")[0]
        return f"تابع «{name}» را می‌سازد تا همان کار را چند بار صدا بزنی. پرانتز ورودی‌ها است.{extra}"
    if t.startswith("class "):
        return f"کلاس می‌سازد: نقشهٔ شیء. «{t}».{extra}"
    if t.startswith("if ") or t.startswith("if("):
        return f"شرط را چک می‌کند؛ اگر درست باشد آکولاد بعدی اجرا می‌شود. «{t}».{extra}"
    if t.startswith("elseif") or t.startswith("else if"):
        return "اگر شرط‌های قبلی غلط بود این را چک کن."
    if t.startswith("else"):
        return "راه آخر وقتی هیچ شرطی درست نبود."
    if t.startswith("foreach"):
        return f"روی هر عضو آرایه یک دور می‌چرخد. as یعنی هر عضو را در آن متغیر بگذار. «{t}».{extra}"
    if t.startswith("for ") or t.startswith("for("):
        return f"حلقه با شمارنده: شروع، شرط، افزایش. «{t}».{extra}"
    if t.startswith("while"):
        return f"تا وقتی شرط درست است تکرار کن. «{t}».{extra}"
    if t.startswith("return"):
        return f"نتیجه را از تابع برگردان و تابع را تمام کن. «{t}».{extra}"
    if t.startswith("require") or t.startswith("include"):
        return f"فایل PHP دیگری را همین‌جا می‌آورد. require اگر فایل نباشد برنامه می‌ایستد؛ include معمولاً فقط هشدار می‌دهد. «{t}».{extra}"
    if "bind_param" in t:
        return f"مقدارها را جدا به SQL وصل می‌کند. رشتهٔ اول نوع را می‌گوید (s متن، i عدد). این کار جلوی تزریق SQL را می‌گیرد.{extra}"
    if "prepare(" in t:
        return f"قالب SQL را آماده می‌کند؛ جای مقدارها علامت ? است تا بعد جدا پر شود. امن‌تر از چسباندن متن به SQL است.{extra}"
    if "->query(" in t:
        return f"یک دستور SQL را روی دیتابیس اجرا می‌کند. «{t}». برای دادهٔ کاربر از prepare استفاده کن نه query خام.{extra}"
    if t.startswith("header("):
        return f"یک سربرگ HTTP می‌فرستد (مثلاً نوع پاسخ یا ریدایرکت). باید قبل از هر خروجی متنی باشد. «{t}».{extra}"
    if "htmlspecialchars" in t:
        return f"نویسه‌های خطرناک HTML مثل < را تبدیل می‌کند تا اگر کاربر تگ فرستاد اجرا نشود؛ فقط متن دیده شود.{extra}"
    if t.startswith("try"):
        return "این کار را امتحان کن؛ اگر استثنا پرتاب شد catch می‌گیرد."
    if t.startswith("catch"):
        return "خطا را می‌گیرد و برنامه را زنده نگه می‌دارد. داخل پرانتز نوع خطا و متغیر پیام است."
    if t.startswith("throw"):
        return f"عمداً خطا می‌سازد. «{t}»."
    if t.startswith("$") and "=" in t and "==" not in t.split("=")[0]:
        left, right = t.split("=", 1)
        left = left.strip()
        right = right.strip().rstrip(";")
        return f"متغیر «{left}» در PHP با $ شروع می‌شود. مقدار سمت راست داخلش می‌رود: {right}. = یعنی بگذار داخل جعبه.{extra}"
    if t.startswith("$") and "->" in t:
        return f"از روی یک شیء، ویژگی یا متد را صدا می‌زند. -> یعنی «از این شیء». «{t}».{extra}"
    if t in ("{", "}"):
        return "آکولاد شروع یا پایان گروه دستورها است."
    if t.endswith(";"):
        return f"یک دستور کامل PHP است. نقطه‌ویرگول پایان جمله است: «{t[:-1].strip()}».{extra}"
    return f"این دستور PHP اجرا می‌شود: «{t}». نام متغیر با $ است و تابع با پرانتز صدا زده می‌شود.{extra}"


def css_line(s):
    t = s.strip()
    if t.startswith("/*"):
        body = t.strip("/* ").strip("*/").strip()
        return f"توضیح CSS است و روی صفحه اثر ندارد: «{body}»."
    if t.startswith("*/"):
        return "پایان توضیح چندخطی CSS."
    if t.startswith("@media"):
        return f"قانون شرطی برای اندازه صفحه. داخل پرانتز شرط است (مثلاً حداکثر عرض). فقط وقتی شرط درست باشد قوانین داخلش اعمال می‌شوند. «{t}»."
    if t.startswith("@keyframes"):
        return f"مراحل یک انیمیشن را نام‌گذاری می‌کند. بعد با animation از این اسم استفاده می‌کنی. «{t}»."
    if t.startswith("@import") or t.startswith("@font-face") or t.startswith("@supports"):
        return f"یک دستور خاص CSS است: «{t}». @ یعنی این یک قاعده معمولی ویژگی نیست، یک فرمان بالاتر است."
    if t == "{":
        return "آکولاد باز: از اینجا ویژگی‌های این انتخاب‌گر شروع می‌شود."
    if t == "}":
        return "آکولاد بسته: قانون این انتخاب‌گر تمام شد."
    if t.endswith("{") and ":" not in t.split("{")[0]:
        sel = t[:-1].strip()
        kind = "کلاس (نقطه یعنی class)" if sel.startswith(".") else "شناسه (مربع یعنی id)" if sel.startswith("#") else "عنصر HTML" if re.match(r"^[a-zA-Z]", sel) else "انتخاب‌گر ترکیبی"
        return f"انتخاب می‌کند چه چیزی استایل بگیرد: «{sel}». این {kind} است. آکولاد باز یعنی ویژگی‌ها از خط بعد شروع می‌شوند."
    if ":" in t and "{" not in t:
        prop, val = t.split(":", 1)
        prop, val = prop.strip(), val.strip().rstrip(";").strip()
        meanings = {
            "color": "رنگ متن",
            "background": "پس‌زمینه",
            "background-color": "رنگ پس‌زمینه",
            "background-image": "تصویر پس‌زمینه",
            "background-size": "اندازه تصویر پس‌زمینه",
            "width": "عرض جعبه",
            "height": "ارتفاع جعبه",
            "max-width": "حداکثر عرض؛ از این بیشتر نشود",
            "min-height": "حداقل ارتفاع",
            "padding": "فاصله داخلی از محتوا تا لبه",
            "margin": "فاصله بیرونی تا عنصرهای دیگر",
            "border": "خط دور جعبه",
            "border-radius": "گردی گوشه‌ها",
            "display": "نوع نمایش (بلوک، فلکس، گرید، مخفی…)",
            "flex-direction": "جهت چیدن بچه‌ها در فلکس",
            "justify-content": "چینش روی محور اصلی",
            "align-items": "چینش روی محور عمود",
            "gap": "فاصله بین بچه‌ها",
            "font-size": "اندازه نوشته",
            "font-family": "نوع قلم",
            "font-weight": "ضخامت قلم",
            "line-height": "فاصله خطوط متن؛ برای خوانایی",
            "text-align": "تراز افقی متن",
            "text-decoration": "زیرخط یا خط روی متن",
            "box-sizing": "عرض شامل پدینگ و بوردر بشود یا نه",
            "position": "نحوه قرارگیری (relative, absolute, fixed)",
            "top": "فاصله از بالا وقتی position غیر static است",
            "left": "فاصله از چپ",
            "right": "فاصله از راست",
            "bottom": "فاصله از پایین",
            "z-index": "کدام روی دیگری بیاید؛ عدد بزرگ‌تر رو است",
            "overflow": "اگر محتوا نخورد چه شود (اسکرول یا مخفی)",
            "opacity": "شفافیت از ۰ نامرئی تا ۱ کامل",
            "box-shadow": "سایه دور جعبه",
            "transition": "تغییر نرم به‌جای پرش",
            "transform": "جابه‌جایی، چرخش یا مقیاس",
            "grid-template-columns": "تعداد و عرض ستون‌های گرید",
            "grid-column": "این آیتم چند ستون را بگیرد",
            "object-fit": "تصویر چطور در قاب جا شود",
            "cursor": "شکل نشانگر ماوس",
            "outline": "خط دور برای فوکوس؛ در مدل جعبه حساب نمی‌شود",
        }
        mean = meanings.get(prop, f"ویژگی «{prop}»")
        return f"{mean} را برابر «{val}» می‌گذارد. اول نام ویژگی، بعد دو نقطه، بعد مقدار. نقطه‌ویرگول پایان این ویژگی است تا ویژگی بعدی قاطی نشود."
    return f"یک قانون یا بخش CSS: «{t}». انتخاب‌گر می‌گوید روی چه چیزی، آکولاد ویژگی‌ها را گروه می‌کند."


def html_line(s):
    t = s.strip()
    if t.startswith("<!--"):
        return "توضیح HTML است؛ در صفحه دیده نمی‌شود."
    if t.startswith("<!DOCTYPE"):
        return "به مرورگر می‌گوید این سند HTML5 است تا با قوانین قدیمی اشتباه گرفته نشود."
    m = re.match(r"</(\w+)", t)
    if m:
        return f"تگ بسته «{m.group(1)}» یعنی جعبهٔ {m.group(1)} تمام شد. بدون بستن، تگ بعدی ممکن است قاطی شود."
    m = re.match(r"<(\w+)([^>]*)>(.*)", t)
    if not m:
        if t.startswith("<") and t.endswith(">"):
            name = re.match(r"<(\w+)", t)
            nm = name.group(1) if name else "تگ"
            return f"تگ «{nm}» را باز می‌کند. اگر /> داشته باشد خودش بسته است (مثل img یا br)."
        return f"متن داخل صفحه است و کاربر همان را می‌بیند: «{t}»."
    name, attrs, rest = m.group(1), m.group(2), m.group(3)
    hints = {
        "html": "ریشه کل صفحه",
        "head": "اطلاعات صفحه مثل عنوان تب؛ در خود صفحه دیده نمی‌شود",
        "body": "هر چیزی که کاربر می‌بیند داخل body است",
        "title": "متن تب مرورگر",
        "meta": "اطلاعات کمکی؛ charset برای فارسی لازم است",
        "p": "یک پاراگراف متن",
        "h1": "بزرگ‌ترین عنوان صفحه؛ معمولاً یکی در هر صفحه",
        "h2": "عنوان بخش",
        "h3": "عنوان زیربخش",
        "a": "لینک؛ href می‌گوید کجا برود",
        "img": "تصویر؛ src آدرس فایل و alt توضیح است",
        "ul": "فهرست نقطه‌ای",
        "ol": "فهرست شماره‌دار",
        "li": "یک آیتم فهرست",
        "div": "جعبه عمومی برای چیدمان",
        "span": "تکه متن داخل خط",
        "form": "فرم فرستادن داده",
        "input": "فیلد ورودی کاربر",
        "button": "دکمه",
        "label": "برچسب فیلد؛ کلیک روی آن فیلد را انتخاب می‌کند",
        "table": "جدول",
        "tr": "یک ردیف جدول",
        "td": "یک سلول",
        "th": "عنوان ستون",
        "header": "سرصفحه معنایی",
        "main": "محتوای اصلی",
        "footer": "پاورقی",
        "nav": "منوی ناوبری",
        "section": "یک بخش موضوعی",
        "article": "یک مطلب مستقل",
        "strong": "متن مهم/پررنگ",
        "em": "تأکید/ایتالیک",
        "br": "خط را می‌شکند",
        "hr": "خط افقی جداکننده",
        "link": "معمولاً فایل CSS را وصل می‌کند",
        "script": "کد جاوااسکریپت",
        "video": "پخش ویدیو",
        "audio": "پخش صدا",
        "select": "منوی کشویی",
        "option": "یک گزینه منو",
        "textarea": "جعبه متن چندخطی",
    }
    mean = hints.get(name, f"عنصر {name}")
    attr_txt = ""
    if attrs.strip():
        parts = []
        for am in re.finditer(r'(\w+)(?:=("[^"]*"|\'[^\']*\'|\S+))?', attrs):
            k, v = am.group(1), am.group(2) or "بدون مقدار"
            ad = {
                "href": "آدرس مقصد لینک",
                "src": "آدرس فایل",
                "alt": "توضیح تصویر اگر نیامد یا برای خوانش صفحه",
                "id": "شناسه یکتا در صفحه",
                "class": "گروه برای استایل CSS",
                "type": "نوع فیلد یا دکمه",
                "name": "کلید داده وقتی فرم ارسال می‌شود",
                "value": "مقدار ارسالی یا اولیه",
                "charset": "کدگذاری حروف؛ UTF-8 برای فارسی",
                "lang": "زبان صفحه",
                "dir": "جهت متن؛ rtl برای فارسی",
                "rel": "رابطه فایل لینک‌شده",
                "action": "کجا فرم فرستاده شود",
                "method": "روش ارسال get یا post",
                "placeholder": "متن راهنما داخل فیلد",
                "required": "پر کردنش اجباری است",
                "controls": "دکمه‌های پخش را نشان بده",
                "width": "عرض",
                "height": "ارتفاع",
                "for": "این برچسب مال کدام id است",
            }.get(k, f"ویژگی {k}")
            parts.append(f"{k} ({ad}) = {v}")
        attr_txt = " ویژگی‌ها: " + "؛ ".join(parts) + "."
    inner = re.sub(r"</\w+>\s*$", "", rest).strip()
    inner_txt = f" متن داخل تگ که کاربر می‌بیند: «{inner}»." if inner and not inner.startswith("<") else ""
    return f"تگ «{name}»: {mean}.{attr_txt}{inner_txt}"


def shell_line(s):
    t = s.strip()
    if t.startswith("#"):
        return f"توضیح دستور است، اجرا نمی‌شود: «{t[1:].strip()}»."
    if t.startswith("python"):
        return f"مفسر پایتون را صدا می‌زند. «{t}». مثلاً --version نسخه را نشان می‌دهد یا نام فایل را اجرا می‌کند."
    if t.startswith("pip"):
        return f"مدیر بسته پایتون: کتابخانه را نصب یا فهرست می‌کند. «{t}»."
    return f"این دستور در ترمینال اجرا می‌شود: «{t}»."

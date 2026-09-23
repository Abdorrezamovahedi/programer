#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate real W3Schools-style lessons for HTML, CSS, JavaScript, SQL."""

from pathlib import Path

SITE = Path("/home/workdir/artifacts/site/zaban")

CSS = r'''
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Vazirmatn", system-ui, sans-serif; background: #0f1419; color: #e6edf3; line-height: 1.75; font-size: 16px; }
a { text-decoration: none; color: inherit; }
header { background: #0d1117; border-bottom: 1px solid #21262d; padding: 14px 40px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }
.logo { color: #58a6ff; font-size: 20px; font-weight: 700; }
.logo span { color: #8b949e; font-weight: 400; font-size: 12px; margin-right: 6px; }
nav a { color: #8b949e; font-size: 13px; padding: 6px 12px; border-radius: 6px; margin-right: 4px; }
nav a:hover { color: #e6edf3; background: #161b22; }
.container { width: 94%; max-width: 1280px; margin: 28px auto; display: grid; grid-template-columns: 260px 1fr; gap: 24px; }
.sidebar { background: #0d1117; border: 1px solid #21262d; border-radius: 12px; padding: 16px 12px; position: sticky; top: 70px; max-height: calc(100vh - 90px); overflow-y: auto; }
.sidebar h2 { font-size: 11px; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; padding: 0 8px; }
.sidebar-section { margin-bottom: 16px; }
.sidebar-section h3 { font-size: 11px; color: #58a6ff; margin: 10px 0 4px; padding: 0 8px; font-weight: 600; }
.side-link { display: block; padding: 6px 10px; border-radius: 6px; font-size: 13px; color: #c9d1d9; margin: 1px 0; }
.side-link:hover, .side-link.active { background: #1f6feb22; color: #58a6ff; }
.content { display: flex; flex-direction: column; gap: 18px; }
.card { background: #0d1117; border: 1px solid #21262d; border-radius: 12px; padding: 24px 28px; }
.card h1 { font-size: 26px; font-weight: 700; color: #e6edf3; margin-bottom: 12px; }
.card h2 { font-size: 18px; font-weight: 600; color: #e6edf3; margin: 22px 0 10px; padding-top: 12px; border-top: 1px solid #21262d; }
.card h2:first-of-type { border-top: none; padding-top: 0; margin-top: 8px; }
.card p, .card li { color: #8b949e; font-size: 15px; margin-bottom: 10px; }
.card ul, .card ol { padding-right: 22px; margin-bottom: 12px; }
.card li { margin-bottom: 6px; }
.code-box { direction: ltr; text-align: left; background: #010409; border: 1px solid #21262d; border-radius: 8px; padding: 16px 18px; overflow-x: auto; margin: 12px 0 16px; }
.code-box code { font-family: "SF Mono", Consolas, monospace; color: #7ee787; font-size: 14px; line-height: 1.65; white-space: pre; }
.note { background: #1f6feb15; border: 1px solid #388bfd44; border-radius: 8px; padding: 12px 16px; margin: 14px 0; color: #79b8ff; font-size: 14px; }
.nav-lessons { display: flex; justify-content: space-between; gap: 12px; margin-top: 8px; }
.nav-lessons a { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 10px 16px; color: #58a6ff; font-size: 13px; font-weight: 500; }
.nav-lessons a:hover { border-color: #58a6ff; }
footer { margin-top: 40px; padding: 22px; text-align: center; background: #0d1117; border-top: 1px solid #21262d; color: #6e7681; font-size: 13px; }
@media (max-width: 900px) { .container { grid-template-columns: 1fr; } .sidebar { position: static; max-height: none; } }
'''

def page(lang_name, lang_slug, home_file, sidebar_data, active, title, body, prev_slug, next_slug):
    # build sidebar
    parts = ['    <aside class="sidebar">', '      <h2>فهرست مطالب</h2>']
    for sec_title, items in sidebar_data:
        parts.append('      <div class="sidebar-section">')
        parts.append(f'        <h3>{sec_title}</h3>')
        for slug, label in items:
            cls = "side-link active" if slug == active else "side-link"
            href = home_file if slug == "index" else f"{slug}.html"
            parts.append(f'        <a href="{href}" class="{cls}">{label}</a>')
        parts.append('      </div>')
    parts.append('    </aside>')
    sidebar = "\n".join(parts)

    prev_html = next_html = ""
    if prev_slug:
        href = home_file if prev_slug == "index" else f"{prev_slug}.html"
        prev_html = f'<a href="{href}">← درس قبلی</a>'
    if next_slug:
        next_html = f'<a href="{next_slug}.html">درس بعدی →</a>'

    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | آموزش {lang_name}</title>
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
      <a href="{home_file}">{lang_name}</a>
      <a href="../../index.html">زبان‌ها</a>
    </nav>
  </header>
  <main class="container">
{sidebar}
    <section class="content">
      <div class="card">
{body}
        <div class="nav-lessons">{prev_html}{next_html}</div>
      </div>
    </section>
  </main>
  <footer>مدرسه برنامه‌نویسان خاص · آموزش {lang_name} بر اساس ساختار W3Schools</footer>
</body>
</html>
'''

# ===================== HTML =====================
HTML_SIDEBAR = [
  ("مقدمه", [("index", "خانه"), ("intro", "مقدمه HTML"), ("editors", "ویرایشگر"), ("basic", "عناصر پایه"), ("attributes", "ویژگی‌ها"), ("headings", "عناوین")]),
  ("متن", [("paragraphs", "پاراگراف"), ("styles", "استایل‌ها"), ("formatting", "فرمت‌بندی"), ("comments", "توضیحات")]),
  ("لینک و تصویر", [("links", "لینک‌ها"), ("images", "تصاویر")]),
  ("جداول و لیست", [("tables", "جداول"), ("lists", "لیست‌ها")]),
  ("فرم", [("forms", "فرم‌ها"), ("form-input", "ورودی‌ها")]),
  ("HTML5", [("semantic", "عناصر معنایی"), ("media", "ویدیو و صدا")]),
]

HTML_LESSONS = {
  "index": ("خانه HTML", None, "intro", '''
    <h1>📄 آموزش HTML</h1>
    <p>HTML زبان نشانه‌گذاری استاندارد برای ساخت صفحات وب است. ساختار و محتوای هر صفحه وب با HTML تعریف می‌شود.</p>
    <h2>اولین صفحه</h2>
    <div class="code-box"><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;title&gt;صفحه من&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;h1&gt;سلام دنیا&lt;/h1&gt;
  &lt;p&gt;اولین صفحه من&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></div>
    <div class="note">محتوای این آموزش بر اساس ساختار و مثال‌های W3Schools نوشته شده است. از منوی سمت راست درس‌ها را انتخاب کنید.</div>
  '''),
  "intro": ("مقدمه HTML", "index", "editors", '''
    <h1>مقدمه HTML</h1>
    <p>HTML مخفف <strong>Hyper Text Markup Language</strong> است. HTML توصیف‌کننده ساختار صفحات وب است.</p>
    <h2>HTML چیست؟</h2>
    <ul>
      <li>HTML مخفف Hyper Text Markup Language است</li>
      <li>HTML زبان نشانه‌گذاری استاندارد برای صفحات وب است</li>
      <li>HTML عناصر HTML را توصیف می‌کند</li>
      <li>مرورگرها HTML را برای نمایش صفحات وب تفسیر می‌کنند</li>
    </ul>
    <h2>یک سند ساده HTML</h2>
    <div class="code-box"><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;body&gt;
  &lt;h1&gt;My First Heading&lt;/h1&gt;
  &lt;p&gt;My first paragraph.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></div>
  '''),
  "editors": ("ویرایشگر HTML", "intro", "basic", '''
    <h1>ویرایشگر HTML</h1>
    <p>برای نوشتن HTML به نرم‌افزار خاصی نیاز نیست. می‌توانید از Notepad (ویندوز) یا TextEdit (مک) استفاده کنید.</p>
    <h2>مراحل</h2>
    <ol>
      <li>ویرایشگر متن را باز کنید</li>
      <li>کد HTML را بنویسید</li>
      <li>فایل را با پسوند <code>.html</code> ذخیره کنید</li>
      <li>فایل را در مرورگر باز کنید</li>
    </ol>
    <div class="note">ویرایشگرهای پیشنهادی: VS Code، Sublime Text، Notepad++</div>
  '''),
  "basic": ("عناصر پایه", "editors", "attributes", '''
    <h1>عناصر پایه HTML</h1>
    <p>یک سند HTML از عناصر تشکیل شده است. عنصر معمولاً از تگ شروع، محتوا و تگ پایان تشکیل می‌شود.</p>
    <div class="code-box"><code>&lt;tagname&gt;محتوا&lt;/tagname&gt;</code></div>
    <h2>مثال‌های رایج</h2>
    <div class="code-box"><code>&lt;h1&gt;عنوان بزرگ&lt;/h1&gt;
&lt;p&gt;یک پاراگراف&lt;/p&gt;
&lt;br&gt;
&lt;hr&gt;</code></div>
    <div class="note">بعضی تگ‌ها مثل <code>&lt;br&gt;</code> و <code>&lt;hr&gt;</code> خودبسته هستند و تگ پایان ندارند.</div>
  '''),
  "attributes": ("ویژگی‌ها (Attributes)", "basic", "headings", '''
    <h1>ویژگی‌های HTML</h1>
    <p>ویژگی‌ها اطلاعات اضافی درباره عناصر می‌دهند و همیشه در تگ شروع نوشته می‌شوند.</p>
    <div class="code-box"><code>&lt;a href="https://www.w3schools.com"&gt;لینک به W3Schools&lt;/a&gt;
&lt;img src="img.jpg" width="500" height="600"&gt;</code></div>
    <h2>ویژگی‌های مهم</h2>
    <ul>
      <li><code>href</code> — آدرس لینک</li>
      <li><code>src</code> — مسیر تصویر</li>
      <li><code>width</code> / <code>height</code> — اندازه</li>
      <li><code>alt</code> — متن جایگزین تصویر</li>
      <li><code>style</code> — استایل CSS</li>
      <li><code>id</code> و <code>class</code> — شناسه و کلاس</li>
    </ul>
  '''),
  "headings": ("عناوین", "attributes", "paragraphs", '''
    <h1>عناوین HTML</h1>
    <p>عناوین با تگ‌های <code>&lt;h1&gt;</code> تا <code>&lt;h6&gt;</code> تعریف می‌شوند.</p>
    <div class="code-box"><code>&lt;h1&gt;عنوان ۱&lt;/h1&gt;
&lt;h2&gt;عنوان ۲&lt;/h2&gt;
&lt;h3&gt;عنوان ۳&lt;/h3&gt;
&lt;h4&gt;عنوان ۴&lt;/h4&gt;
&lt;h5&gt;عنوان ۵&lt;/h5&gt;
&lt;h6&gt;عنوان ۶&lt;/h6&gt;</code></div>
    <div class="note"><code>&lt;h1&gt;</code> مهم‌ترین عنوان و <code>&lt;h6&gt;</code> کم‌اهمیت‌ترین است. برای SEO فقط یک h1 در هر صفحه پیشنهاد می‌شود.</div>
  '''),
  "paragraphs": ("پاراگراف", "headings", "styles", '''
    <h1>پاراگراف‌ها</h1>
    <p>پاراگراف با تگ <code>&lt;p&gt;</code> تعریف می‌شود. مرورگر به‌طور خودکار فاصله قبل و بعد اضافه می‌کند.</p>
    <div class="code-box"><code>&lt;p&gt;این یک پاراگراف است.&lt;/p&gt;
&lt;p&gt;این پاراگراف دیگری است.&lt;/p&gt;</code></div>
    <h2>خط جدید با br</h2>
    <div class="code-box"><code>&lt;p&gt;این یک خط است.&lt;br&gt;این خط بعدی است.&lt;/p&gt;</code></div>
  '''),
  "styles": ("استایل‌ها", "paragraphs", "formatting", '''
    <h1>استایل در HTML</h1>
    <p>ویژگی <code>style</code> برای افزودن استایل CSS به عنصر استفاده می‌شود.</p>
    <div class="code-box"><code>&lt;p style="color:red;"&gt;متن قرمز&lt;/p&gt;
&lt;p style="color:blue;"&gt;متن آبی&lt;/p&gt;
&lt;h1 style="font-size:60px;"&gt;عنوان بزرگ&lt;/h1&gt;
&lt;p style="background-color:powderblue;"&gt;پس‌زمینه آبی&lt;/p&gt;</code></div>
  '''),
  "formatting": ("فرمت‌بندی متن", "styles", "comments", '''
    <h1>فرمت‌بندی متن</h1>
    <div class="code-box"><code>&lt;b&gt;ضخیم&lt;/b&gt; — &lt;strong&gt;مهم&lt;/strong&gt;
&lt;i&gt;ایتالیک&lt;/i&gt; — &lt;em&gt;تأکید&lt;/em&gt;
&lt;mark&gt;هایلایت&lt;/mark&gt;
&lt;small&gt;کوچک&lt;/small&gt;
&lt;del&gt;خط‌خورده&lt;/del&gt;
&lt;ins&gt;درج‌شده&lt;/ins&gt;
&lt;sub&gt;زیرنویس&lt;/sub&gt; — &lt;sup&gt;بالانویس&lt;/sup&gt;</code></div>
  '''),
  "comments": ("توضیحات", "formatting", "links", '''
    <h1>توضیحات HTML</h1>
    <p>توضیحات در صفحه نمایش داده نمی‌شوند و برای یادداشت برنامه‌نویس هستند.</p>
    <div class="code-box"><code>&lt;!-- این یک توضیح است --&gt;
&lt;p&gt;این پاراگراف در مرورگر دیده می‌شود.&lt;/p&gt;</code></div>
  '''),
  "links": ("لینک‌ها", "comments", "images", '''
    <h1>لینک‌ها در HTML</h1>
    <p>لینک با تگ <code>&lt;a&gt;</code> و ویژگی <code>href</code> ساخته می‌شود.</p>
    <div class="code-box"><code>&lt;a href="https://www.w3schools.com"&gt;بازدید از W3Schools&lt;/a&gt;
&lt;a href="https://www.w3schools.com" target="_blank"&gt;باز در تب جدید&lt;/a&gt;
&lt;a href="mailtoxavier.y@example.org"&gt;ارسال ایمیل&lt;/a&gt;</code></div>
  '''),
  "images": ("تصاویر", "links", "tables", '''
    <h1>تصاویر در HTML</h1>
    <div class="code-box"><code>&lt;img src="img_girl.jpg" alt="دختر" width="500" height="600"&gt;
&lt;img src="img_chania.jpg" alt="Chania" style="width:128px;height:128px;"&gt;</code></div>
    <div class="note">ویژگی <code>alt</code> وقتی تصویر لود نشود یا برای دسترس‌پذیری صفحه‌خوان‌ها مهم است.</div>
  '''),
  "tables": ("جداول", "images", "lists", '''
    <h1>جداول HTML</h1>
    <div class="code-box"><code>&lt;table&gt;
  &lt;tr&gt;
    &lt;th&gt;شرکت&lt;/th&gt;
    &lt;th&gt;تماس&lt;/th&gt;
  &lt;/tr&gt;
  &lt;tr&gt;
    &lt;td&gt;Alfreds Futterkiste&lt;/td&gt;
    &lt;td&gt;Maria Anders&lt;/td&gt;
  &lt;/tr&gt;
&lt;/table&gt;</code></div>
    <p><code>&lt;th&gt;</code> سلول عنوان، <code>&lt;td&gt;</code> سلول داده، <code>&lt;tr&gt;</code> ردیف است.</p>
  '''),
  "lists": ("لیست‌ها", "tables", "forms", '''
    <h1>لیست‌ها در HTML</h1>
    <h2>لیست نامرتب</h2>
    <div class="code-box"><code>&lt;ul&gt;
  &lt;li&gt;قهوه&lt;/li&gt;
  &lt;li&gt;چای&lt;/li&gt;
  &lt;li&gt;شیر&lt;/li&gt;
&lt;/ul&gt;</code></div>
    <h2>لیست مرتب</h2>
    <div class="code-box"><code>&lt;ol&gt;
  &lt;li&gt;قهوه&lt;/li&gt;
  &lt;li&gt;چای&lt;/li&gt;
  &lt;li&gt;شیر&lt;/li&gt;
&lt;/ol&gt;</code></div>
  '''),
  "forms": ("فرم‌ها", "lists", "form-input", '''
    <h1>فرم‌های HTML</h1>
    <p>فرم برای جمع‌آوری ورودی کاربر استفاده می‌شود.</p>
    <div class="code-box"><code>&lt;form action="/action_page.php"&gt;
  &lt;label for="fname"&gt;نام:&lt;/label&gt;
  &lt;input type="text" id="fname" name="fname"&gt;
  &lt;input type="submit" value="ارسال"&gt;
&lt;/form&gt;</code></div>
  '''),
  "form-input": ("انواع ورودی", "forms", "semantic", '''
    <h1>انواع input</h1>
    <div class="code-box"><code>&lt;input type="text"&gt;
&lt;input type="password"&gt;
&lt;input type="email"&gt;
&lt;input type="number"&gt;
&lt;input type="date"&gt;
&lt;input type="checkbox"&gt;
&lt;input type="radio"&gt;
&lt;input type="file"&gt;
&lt;input type="submit"&gt;
&lt;input type="button" value="کلیک"&gt;</code></div>
  '''),
  "semantic": ("عناصر معنایی HTML5", "form-input", "media", '''
    <h1>عناصر معنایی HTML5</h1>
    <p>این عناصر معنای محتوا را مشخص می‌کنند:</p>
    <div class="code-box"><code>&lt;header&gt;...&lt;/header&gt;
&lt;nav&gt;...&lt;/nav&gt;
&lt;main&gt;...&lt;/main&gt;
&lt;article&gt;...&lt;/article&gt;
&lt;section&gt;...&lt;/section&gt;
&lt;aside&gt;...&lt;/aside&gt;
&lt;footer&gt;...&lt;/footer&gt;</code></div>
  '''),
  "media": ("ویدیو و صدا", "semantic", None, '''
    <h1>ویدیو و صدا در HTML5</h1>
    <div class="code-box"><code>&lt;video width="320" height="240" controls&gt;
  &lt;source src="movie.mp4" type="video/mp4"&gt;
&lt;/video&gt;

&lt;audio controls&gt;
  &lt;source src="audio.mp3" type="audio/mpeg"&gt;
&lt;/audio&gt;</code></div>
  '''),
}

# ===================== CSS =====================
CSS_SIDEBAR = [
  ("مقدمه", [("index", "خانه"), ("intro", "مقدمه CSS"), ("syntax", "نحو"), ("selectors", "انتخاب‌گرها")]),
  ("رنگ و پس‌زمینه", [("colors", "رنگ‌ها"), ("background", "پس‌زمینه")]),
  ("متن", [("text", "متن"), ("fonts", "فونت")]),
  ("باکس‌مدل", [("box-model", "باکس‌مدل"), ("borders", "حاشیه"), ("margin", "مارجین"), ("padding", "پدینگ")]),
  ("چیدمان", [("display", "Display"), ("position", "Position"), ("flexbox", "Flexbox"), ("grid", "Grid")]),
  ("واکنش‌گرا", [("media", "Media Query")]),
]

CSS_LESSONS = {
  "index": ("خانه CSS", None, "intro", '''
    <h1>🎨 آموزش CSS</h1>
    <p>CSS زبان استایل‌دهی صفحات وب است. با CSS ظاهر، چیدمان، رنگ‌ها و انیمیشن‌ها را کنترل می‌کنید.</p>
    <div class="code-box"><code>body {
  background-color: #0f1419;
  color: #e6edf3;
  font-family: Vazirmatn, sans-serif;
}
h1 {
  color: #58a6ff;
  text-align: center;
}</code></div>
    <div class="note">محتوا بر اساس ساختار W3Schools است. از منوی کناری درس‌ها را باز کنید.</div>
  '''),
  "intro": ("مقدمه CSS", "index", "syntax", '''
    <h1>مقدمه CSS</h1>
    <p>CSS مخفف Cascading Style Sheets است و ظاهر HTML را توصیف می‌کند.</p>
    <h2>سه روش افزودن CSS</h2>
    <ul>
      <li><strong>Inline:</strong> با ویژگی style روی خود عنصر</li>
      <li><strong>Internal:</strong> داخل تگ <code>&lt;style&gt;</code> در head</li>
      <li><strong>External:</strong> فایل جدا با پسوند .css</li>
    </ul>
    <div class="code-box"><code>&lt;link rel="stylesheet" href="styles.css"&gt;</code></div>
  '''),
  "syntax": ("نحو CSS", "intro", "selectors", '''
    <h1>نحو CSS</h1>
    <div class="code-box"><code>selector {
  property: value;
  property: value;
}</code></div>
    <div class="code-box"><code>p {
  color: red;
  text-align: center;
}</code></div>
  '''),
  "selectors": ("انتخاب‌گرها", "syntax", "colors", '''
    <h1>انتخاب‌گرهای CSS</h1>
    <div class="code-box"><code>/* عنصر */
p { color: red; }

/* کلاس */
.center { text-align: center; }

/* آی‌دی */
#para1 { color: blue; }

/* گروهی */
h1, h2, p { text-align: center; }</code></div>
  '''),
  "colors": ("رنگ‌ها", "selectors", "background", '''
    <h1>رنگ‌ها در CSS</h1>
    <div class="code-box"><code>h1 { color: red; }
h1 { color: #ff0000; }
h1 { color: rgb(255, 0, 0); }
h1 { color: rgba(255, 0, 0, 0.5); }
h1 { color: hsl(0, 100%, 50%); }</code></div>
  '''),
  "background": ("پس‌زمینه", "colors", "text", '''
    <h1>پس‌زمینه</h1>
    <div class="code-box"><code>body {
  background-color: lightblue;
  background-image: url("img.jpg");
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
}</code></div>
  '''),
  "text": ("متن", "background", "fonts", '''
    <h1>استایل متن</h1>
    <div class="code-box"><code>h1 {
  color: red;
  text-align: center;
  text-decoration: underline;
  text-transform: uppercase;
  letter-spacing: 2px;
  line-height: 1.8;
}</code></div>
  '''),
  "fonts": ("فونت", "text", "box-model", '''
    <h1>فونت در CSS</h1>
    <div class="code-box"><code>p {
  font-family: "Vazirmatn", Arial, sans-serif;
  font-size: 16px;
  font-weight: bold;
  font-style: italic;
}</code></div>
  '''),
  "box-model": ("باکس‌مدل", "fonts", "borders", '''
    <h1>Box Model</h1>
    <p>هر عنصر یک جعبه است شامل: content، padding، border و margin.</p>
    <div class="code-box"><code>div {
  width: 300px;
  padding: 20px;
  border: 5px solid gray;
  margin: 10px;
  box-sizing: border-box;
}</code></div>
  '''),
  "borders": ("حاشیه", "box-model", "margin", '''
    <h1>Border</h1>
    <div class="code-box"><code>p {
  border: 2px solid red;
  border-radius: 8px;
  border-top: 5px solid blue;
}</code></div>
  '''),
  "margin": ("مارجین", "borders", "padding", '''
    <h1>Margin</h1>
    <div class="code-box"><code>p {
  margin: 20px;
  margin-top: 10px;
  margin: 10px 20px 10px 20px; /* top right bottom left */
  margin: 0 auto; /* وسط‌چین افقی */
}</code></div>
  '''),
  "padding": ("پدینگ", "margin", "display", '''
    <h1>Padding</h1>
    <div class="code-box"><code>p {
  padding: 20px;
  padding-left: 30px;
  padding: 10px 20px;
}</code></div>
  '''),
  "display": ("Display", "padding", "position", '''
    <h1>ویژگی display</h1>
    <div class="code-box"><code>div { display: block; }
span { display: inline; }
div { display: inline-block; }
div { display: none; }
div { display: flex; }
div { display: grid; }</code></div>
  '''),
  "position": ("Position", "display", "flexbox", '''
    <h1>Position</h1>
    <div class="code-box"><code>div { position: static; }
div { position: relative; top: 10px; }
div { position: absolute; top: 0; left: 0; }
div { position: fixed; bottom: 0; }
div { position: sticky; top: 0; }</code></div>
  '''),
  "flexbox": ("Flexbox", "position", "grid", '''
    <h1>Flexbox</h1>
    <div class="code-box"><code>.container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  gap: 16px;
}
.item { flex: 1; }</code></div>
  '''),
  "grid": ("Grid", "flexbox", "media", '''
    <h1>CSS Grid</h1>
    <div class="code-box"><code>.container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}
.item { grid-column: span 2; }</code></div>
  '''),
  "media": ("Media Query", "grid", None, '''
    <h1>Media Query (واکنش‌گرا)</h1>
    <div class="code-box"><code>/* موبایل */
@media (max-width: 600px) {
  .container { flex-direction: column; }
}

/* تبلت و بالاتر */
@media (min-width: 768px) {
  body { font-size: 18px; }
}</code></div>
  '''),
}

# ===================== JavaScript =====================
JS_SIDEBAR = [
  ("مقدمه", [("index", "خانه"), ("intro", "مقدمه JS"), ("where", "کجا بنویسیم"), ("output", "خروجی")]),
  ("متغیرها", [("variables", "متغیرها"), ("datatypes", "انواع داده"), ("strings", "رشته‌ها"), ("arrays", "آرایه‌ها"), ("objects", "اشیا")]),
  ("عملگر و شرط", [("operators", "عملگرها"), ("ifelse", "if / else"), ("switch", "سوئیچ"), ("loops", "حلقه‌ها")]),
  ("توابع", [("functions", "توابع"), ("arrow", "فلش فانکشن")]),
  ("DOM", [("dom", "DOM"), ("events", "رویدادها")]),
  ("پیشرفته", [("async", "آسنکرون"), ("json", "JSON")]),
]

JS_LESSONS = {
  "index": ("خانه JavaScript", None, "intro", '''
    <h1>⚡ آموزش JavaScript</h1>
    <p>جاوااسکریپت زبان برنامه‌نویسی وب است که صفحات را پویا و تعاملی می‌کند.</p>
    <div class="code-box"><code>console.log("Hello World!");
let name = "Abdorreza";
document.getElementById("demo").innerHTML = name;</code></div>
    <div class="note">محتوا بر اساس ساختار W3Schools است.</div>
  '''),
  "intro": ("مقدمه JavaScript", "index", "where", '''
    <h1>مقدمه JavaScript</h1>
    <ul>
      <li>JavaScript زبان برنامه‌نویسی وب است</li>
      <li>می‌تواند HTML و CSS را تغییر دهد</li>
      <li>می‌تواند داده را محاسبه و اعتبارسنجی کند</li>
      <li>در تمام مرورگرهای مدرن اجرا می‌شود</li>
    </ul>
  '''),
  "where": ("کجا بنویسیم", "intro", "output", '''
    <h1>جاوااسکریپت را کجا بنویسیم؟</h1>
    <div class="code-box"><code>&lt;script&gt;
  document.getElementById("demo").innerHTML = "Hello";
&lt;/script&gt;

&lt;!-- یا فایل خارجی --&gt;
&lt;script src="myscript.js"&gt;&lt;/script&gt;</code></div>
  '''),
  "output": ("خروجی", "where", "variables", '''
    <h1>روش‌های خروجی</h1>
    <div class="code-box"><code>// داخل HTML
document.getElementById("demo").innerHTML = 5 + 6;

// پنجره هشدار
window.alert(5 + 6);

// کنسول
console.log(5 + 6);

// نوشتن در سند (با احتیاط)
document.write(5 + 6);</code></div>
  '''),
  "variables": ("متغیرها", "output", "datatypes", '''
    <h1>متغیرها در JavaScript</h1>
    <div class="code-box"><code>var x = 5;      // قدیمی
let y = 6;      // پیشنهادی
const z = 7;    // ثابت

let name = "Ali";
let age = 25;</code></div>
    <div class="note"><code>let</code> و <code>const</code> از ES6 هستند و محدوده بلوکی دارند.</div>
  '''),
  "datatypes": ("انواع داده", "variables", "strings", '''
    <h1>انواع داده</h1>
    <div class="code-box"><code>let length = 16;          // Number
let lastName = "Johnson"; // String
let x = true;             // Boolean
let y = null;             // Null
let z;                    // Undefined
let arr = [1, 2, 3];      // Array
let obj = {a: 1};         // Object</code></div>
  '''),
  "strings": ("رشته‌ها", "datatypes", "arrays", '''
    <h1>رشته‌ها</h1>
    <div class="code-box"><code>let text = "Hello World";
console.log(text.length);
console.log(text.toUpperCase());
console.log(text.slice(0, 5));
console.log(text.replace("World", "Ali"));
console.log(`سلام ${text}`);</code></div>
  '''),
  "arrays": ("آرایه‌ها", "strings", "objects", '''
    <h1>آرایه‌ها</h1>
    <div class="code-box"><code>const cars = ["Saab", "Volvo", "BMW"];
console.log(cars[0]);
cars.push("Audi");
cars.pop();
console.log(cars.length);
cars.forEach(c => console.log(c));</code></div>
  '''),
  "objects": ("اشیا", "arrays", "operators", '''
    <h1>اشیا (Objects)</h1>
    <div class="code-box"><code>const person = {
  firstName: "John",
  lastName: "Doe",
  age: 50,
  fullName: function() {
    return this.firstName + " " + this.lastName;
  }
};
console.log(person.firstName);
console.log(person["age"]);
console.log(person.fullName());</code></div>
  '''),
  "operators": ("عملگرها", "objects", "ifelse", '''
    <h1>عملگرها</h1>
    <div class="code-box"><code>let x = 10;
x += 5;           // 15
console.log(x == 15);   // true
console.log(x === "15"); // false (نوع هم چک می‌شود)
console.log(x > 5 && x < 20);</code></div>
  '''),
  "ifelse": ("if / else", "operators", "switch", '''
    <h1>شرط if / else</h1>
    <div class="code-box"><code>let hour = 14;
if (hour < 12) {
  console.log("صبح بخیر");
} else if (hour < 18) {
  console.log("ظهر بخیر");
} else {
  console.log("عصر بخیر");
}

// کوتاه
let result = (hour < 12) ? "صبح" : "بعدازظهر";</code></div>
  '''),
  "switch": ("سوئیچ", "ifelse", "loops", '''
    <h1>switch</h1>
    <div class="code-box"><code>let day = 2;
switch (day) {
  case 1:
    console.log("شنبه");
    break;
  case 2:
    console.log("یکشنبه");
    break;
  default:
    console.log("روز دیگر");
}</code></div>
  '''),
  "loops": ("حلقه‌ها", "switch", "functions", '''
    <h1>حلقه‌ها</h1>
    <div class="code-box"><code>for (let i = 0; i < 5; i++) {
  console.log(i);
}

let i = 0;
while (i < 5) {
  console.log(i);
  i++;
}

const arr = ["a", "b", "c"];
for (let item of arr) {
  console.log(item);
}</code></div>
  '''),
  "functions": ("توابع", "loops", "arrow", '''
    <h1>توابع</h1>
    <div class="code-box"><code>function myFunction(a, b) {
  return a * b;
}
console.log(myFunction(4, 3));

function greet(name = "مهمان") {
  return "سلام " + name;
}</code></div>
  '''),
  "arrow": ("فلش فانکشن", "functions", "dom", '''
    <h1>Arrow Function</h1>
    <div class="code-box"><code>const add = (a, b) => a + b;
console.log(add(2, 3));

const hello = () => "Hello World!";
const hello2 = name => "Hello " + name;</code></div>
  '''),
  "dom": ("DOM", "arrow", "events", '''
    <h1>DOM — کار با صفحه</h1>
    <div class="code-box"><code>document.getElementById("demo").innerHTML = "سلام";
document.querySelector(".title").style.color = "red";
document.querySelectorAll("p").forEach(p => {
  p.style.fontSize = "18px";
});</code></div>
  '''),
  "events": ("رویدادها", "dom", "async", '''
    <h1>رویدادها (Events)</h1>
    <div class="code-box"><code>&lt;button onclick="myFunction()"&gt;کلیک&lt;/button&gt;

&lt;script&gt;
function myFunction() {
  alert("کلیک شد!");
}

document.getElementById("btn").addEventListener("click", function() {
  console.log("کلیک با listener");
});
&lt;/script&gt;</code></div>
  '''),
  "async": ("آسنکرون", "events", "json", '''
    <h1>آسنکرون — Promise و async/await</h1>
    <div class="code-box"><code>fetch("https://api.example.com/data")
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));

async function getData() {
  const res = await fetch("https://api.example.com/data");
  const data = await res.json();
  console.log(data);
}</code></div>
  '''),
  "json": ("JSON", "async", None, '''
    <h1>JSON در JavaScript</h1>
    <div class="code-box"><code>const obj = { name: "Ali", age: 25 };
const text = JSON.stringify(obj);
const parsed = JSON.parse(text);
console.log(parsed.name);</code></div>
  '''),
}

# ===================== SQL =====================
SQL_SIDEBAR = [
  ("مقدمه", [("index", "خانه"), ("intro", "مقدمه SQL"), ("select", "SELECT"), ("where", "WHERE")]),
  ("فیلتر", [("and-or", "AND / OR"), ("orderby", "ORDER BY"), ("null", "NULL")]),
  ("توابع", [("min-max", "MIN / MAX"), ("count", "COUNT / AVG / SUM")]),
  ("JOIN", [("join", "INNER JOIN"), ("left-join", "LEFT JOIN")]),
  ("تغییر داده", [("insert", "INSERT"), ("update", "UPDATE"), ("delete", "DELETE")]),
  ("ساختار", [("create", "CREATE TABLE"), ("alter", "ALTER"), ("drop", "DROP")]),
]

SQL_LESSONS = {
  "index": ("خانه SQL", None, "intro", '''
    <h1>🗄️ آموزش SQL</h1>
    <p>SQL زبان استاندارد برای کار با پایگاه‌های داده رابطه‌ای است.</p>
    <div class="code-box"><code>SELECT * FROM Customers
WHERE Country = 'Iran'
ORDER BY CustomerName;</code></div>
    <div class="note">محتوا بر اساس ساختار W3Schools است.</div>
  '''),
  "intro": ("مقدمه SQL", "index", "select", '''
    <h1>مقدمه SQL</h1>
    <ul>
      <li>SQL = Structured Query Language</li>
      <li>برای دسترسی و دستکاری دیتابیس</li>
      <li>استاندارد ANSI / ISO</li>
    </ul>
    <h2>دستورات مهم</h2>
    <p>SELECT, UPDATE, DELETE, INSERT, CREATE, ALTER, DROP, WHERE, JOIN, ...</p>
  '''),
  "select": ("SELECT", "intro", "where", '''
    <h1>دستور SELECT</h1>
    <div class="code-box"><code>SELECT column1, column2 FROM table_name;
SELECT * FROM Customers;
SELECT CustomerName, City FROM Customers;</code></div>
  '''),
  "where": ("WHERE", "select", "and-or", '''
    <h1>شرط WHERE</h1>
    <div class="code-box"><code>SELECT * FROM Customers
WHERE Country = 'Mexico';

SELECT * FROM Customers
WHERE CustomerID = 1;</code></div>
  '''),
  "and-or": ("AND / OR / NOT", "where", "orderby", '''
    <h1>AND / OR / NOT</h1>
    <div class="code-box"><code>SELECT * FROM Customers
WHERE Country = 'Germany' AND City = 'Berlin';

SELECT * FROM Customers
WHERE City = 'Berlin' OR City = 'München';

SELECT * FROM Customers
WHERE NOT Country = 'Germany';</code></div>
  '''),
  "orderby": ("ORDER BY", "and-or", "null", '''
    <h1>مرتب‌سازی ORDER BY</h1>
    <div class="code-box"><code>SELECT * FROM Customers
ORDER BY Country;

SELECT * FROM Customers
ORDER BY Country DESC;

SELECT * FROM Customers
ORDER BY Country, CustomerName;</code></div>
  '''),
  "null": ("NULL", "orderby", "min-max", '''
    <h1>مقادیر NULL</h1>
    <div class="code-box"><code>SELECT * FROM Customers
WHERE Address IS NULL;

SELECT * FROM Customers
WHERE Address IS NOT NULL;</code></div>
  '''),
  "min-max": ("MIN و MAX", "null", "count", '''
    <h1>MIN و MAX</h1>
    <div class="code-box"><code>SELECT MIN(Price) AS SmallestPrice
FROM Products;

SELECT MAX(Price) AS LargestPrice
FROM Products;</code></div>
  '''),
  "count": ("COUNT / AVG / SUM", "min-max", "join", '''
    <h1>توابع تجمیعی</h1>
    <div class="code-box"><code>SELECT COUNT(*) FROM Products;
SELECT AVG(Price) FROM Products;
SELECT SUM(Quantity) FROM OrderDetails;</code></div>
  '''),
  "join": ("INNER JOIN", "count", "left-join", '''
    <h1>INNER JOIN</h1>
    <div class="code-box"><code>SELECT Orders.OrderID, Customers.CustomerName
FROM Orders
INNER JOIN Customers
ON Orders.CustomerID = Customers.CustomerID;</code></div>
  '''),
  "left-join": ("LEFT JOIN", "join", "insert", '''
    <h1>LEFT JOIN</h1>
    <div class="code-box"><code>SELECT Customers.CustomerName, Orders.OrderID
FROM Customers
LEFT JOIN Orders
ON Customers.CustomerID = Orders.CustomerID
ORDER BY Customers.CustomerName;</code></div>
  '''),
  "insert": ("INSERT", "left-join", "update", '''
    <h1>درج داده — INSERT</h1>
    <div class="code-box"><code>INSERT INTO Customers (CustomerName, City, Country)
VALUES ('Cardinal', 'Stavanger', 'Norway');</code></div>
  '''),
  "update": ("UPDATE", "insert", "delete", '''
    <h1>به‌روزرسانی — UPDATE</h1>
    <div class="code-box"><code>UPDATE Customers
SET ContactName = 'Alfred', City = 'Frankfurt'
WHERE CustomerID = 1;</code></div>
    <div class="note">حتماً WHERE بگذارید وگرنه همه ردیف‌ها عوض می‌شوند!</div>
  '''),
  "delete": ("DELETE", "update", "create", '''
    <h1>حذف — DELETE</h1>
    <div class="code-box"><code>DELETE FROM Customers
WHERE CustomerName = 'Alfreds Futterkiste';</code></div>
  '''),
  "create": ("CREATE TABLE", "delete", "alter", '''
    <h1>ساخت جدول</h1>
    <div class="code-box"><code>CREATE TABLE Persons (
  PersonID int,
  LastName varchar(255),
  FirstName varchar(255),
  Address varchar(255),
  City varchar(255)
);</code></div>
  '''),
  "alter": ("ALTER TABLE", "create", "drop", '''
    <h1>تغییر جدول — ALTER</h1>
    <div class="code-box"><code>ALTER TABLE Customers
ADD Email varchar(255);

ALTER TABLE Customers
DROP COLUMN Email;</code></div>
  '''),
  "drop": ("DROP", "alter", None, '''
    <h1>حذف جدول / دیتابیس</h1>
    <div class="code-box"><code>DROP TABLE Persons;
DROP DATABASE testDB;</code></div>
    <div class="note">این دستورات غیرقابل‌بازگشت هستند. با احتیاط استفاده کنید.</div>
  '''),
}


def generate_lang(folder_name, home_file, lang_name, sidebar, lessons):
    folder = SITE / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    for slug, (title, prev, nxt, body) in lessons.items():
        html = page(lang_name, folder_name, home_file, sidebar, slug, title, body, prev, nxt)
        fname = home_file if slug == "index" else f"{slug}.html"
        (folder / fname).write_text(html, encoding="utf-8")
        print(f"  {folder_name}/{fname}")


def main():
    print("Generating HTML lessons...")
    generate_lang("html", "html.html", "HTML", HTML_SIDEBAR, HTML_LESSONS)
    print("Generating CSS lessons...")
    generate_lang("css", "css.html", "CSS", CSS_SIDEBAR, CSS_LESSONS)
    print("Generating JavaScript lessons...")
    generate_lang("javascript", "javascript.html", "JavaScript", JS_SIDEBAR, JS_LESSONS)
    print("Generating SQL lessons...")
    generate_lang("sql", "sql.html", "SQL", SQL_SIDEBAR, SQL_LESSONS)
    print("Done.")


if __name__ == "__main__":
    main()

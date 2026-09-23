#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CSS lessons with long, simple Persian explanations (W3Schools-based) + external CSS."""

from pathlib import Path

BASE = Path("/home/workdir/artifacts/site/zaban/css")
BASE.mkdir(parents=True, exist_ok=True)
CSS_HREF = "../../css/main.css"

SIDEBAR = [
  ("مقدمه", [
    ("index", "خانه"),
    ("intro", "CSS چیست؟"),
    ("howto", "چطور CSS اضافه کنیم"),
    ("syntax", "نحو نوشتن CSS"),
    ("selectors", "انتخاب‌گرها"),
    ("comments", "توضیحات در CSS"),
  ]),
  ("رنگ و پس‌زمینه", [
    ("colors", "رنگ‌ها"),
    ("background", "پس‌زمینه"),
    ("background-image", "تصویر پس‌زمینه"),
  ]),
  ("متن و فونت", [
    ("text", "استایل متن"),
    ("fonts", "فونت"),
    ("icons", "آیکون‌ها"),
    ("links", "لینک‌ها"),
  ]),
  ("باکس‌مدل", [
    ("box-model", "باکس‌مدل چیست؟"),
    ("borders", "حاشیه (border)"),
    ("margin", "فاصله بیرونی (margin)"),
    ("padding", "فاصله داخلی (padding)"),
    ("width-height", "عرض و ارتفاع"),
    ("box-sizing", "box-sizing"),
  ]),
  ("چیدمان", [
    ("display", "ویژگی display"),
    ("position", "موقعیت (position)"),
    ("z-index", "z-index"),
    ("overflow", "overflow"),
    ("float", "float"),
  ]),
  ("Flex و Grid", [
    ("flexbox", "Flexbox"),
    ("flex-container", "کانتینر Flex"),
    ("flex-item", "آیتم Flex"),
    ("grid", "CSS Grid"),
    ("grid-container", "کانتینر Grid"),
  ]),
  ("واکنش‌گرا و افکت", [
    ("media", "Media Query"),
    ("units", "واحدهای اندازه"),
    ("transition", "Transition"),
    ("animation", "Animation"),
    ("transform", "Transform"),
    ("shadow", "سایه"),
  ]),
]

def page(active, title, body, prev_s, next_s):
    def side():
        lines = ['    <aside class="sidebar">', '      <h2>فهرست مطالب</h2>']
        for sec, items in SIDEBAR:
            lines.append('      <div class="sidebar-section">')
            lines.append(f'        <h3>{sec}</h3>')
            for slug, label in items:
                cls = "side-link active" if slug == active else "side-link"
                href = "css.html" if slug == "index" else f"{slug}.html"
                lines.append(f'        <a href="{href}" class="{cls}">{label}</a>')
            lines.append('      </div>')
        lines.append('    </aside>')
        return "\n".join(lines)

    prev_h = next_h = ""
    if prev_s:
        href = "css.html" if prev_s == "index" else f"{prev_s}.html"
        prev_h = f'<a href="{href}">← درس قبلی</a>'
    if next_s:
        next_h = f'<a href="{next_s}.html">درس بعدی →</a>'

    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | آموزش CSS</title>
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
      <a href="css.html">CSS</a>
      <a href="../../index.html">همه زبان‌ها</a>
    </nav>
  </header>
  <main class="container">
{side()}
    <section class="content">
      <div class="card">
{body}
        <div class="nav-lessons">{prev_h}{next_h}</div>
      </div>
    </section>
  </main>
  <footer>مدرسه برنامه‌نویسان خاص · آموزش CSS · توضیح ساده · بر اساس ساختار W3Schools</footer>
</body>
</html>
'''

# ========== DETAILED CONTENT ==========

L = {}

L["index"] = (None, "intro", '''
    <h1>آموزش CSS از صفر</h1>
    <p>CSS زبانی است که ظاهر صفحات وب را کنترل می‌کند. با HTML ساختار صفحه را می‌سازید و با CSS رنگ، اندازه، فاصله، چیدمان و انیمیشن را تعیین می‌کنید.</p>
    <p>بدون CSS صفحات وب ساده و شبیه سند متنی خام به نظر می‌رسند. تقریباً هر سایتی که می‌بینید از CSS استفاده می‌کند.</p>
    <h2>یک مثال ساده</h2>
    <p>کد زیر رنگ پس‌زمینه صفحه و ظاهر عنوان را عوض می‌کند:</p>
    <div class="code-box"><code>body {
  background-color: #0f1419;
  color: #e6edf3;
  font-family: Vazirmatn, sans-serif;
}

h1 {
  color: #58a6ff;
  text-align: center;
}</code></div>
    <div class="note">از منوی سمت راست درس‌ها را به ترتیب بخوانید. توضیحات به زبان ساده نوشته شده و مثال‌ها بر اساس ساختار آموزشی W3Schools هستند.</div>
''')

L["intro"] = ("index", "howto", '''
    <h1>CSS چیست؟</h1>
    <p>CSS مخفف <strong>Cascading Style Sheets</strong> است. معنی‌اش تقریباً «برگه‌های استایل آبشاری» است. آبشاری یعنی اگر چند قانون روی یک عنصر اعمال شود، اولویت‌ها مشخص می‌کنند کدام قانون برنده شود.</p>
    <p>CSS ظاهر HTML را توصیف می‌کند: رنگ متن، اندازه فونت، فاصله بین عناصر، چیدمان ستون‌ها، انیمیشن و خیلی چیزهای دیگر.</p>
    <h2>چرا CSS را جدا می‌نویسند؟</h2>
    <p>اگر استایل را داخل خود HTML بنویسید، وقتی سایت بزرگ شود نگهداری سخت می‌شود. با فایل جداگانه CSS می‌توانید:</p>
    <ul>
      <li>ظاهر همه صفحات را از یک جا عوض کنید</li>
      <li>کد HTML را تمیز و خوانا نگه دارید</li>
      <li>همان استایل را در چند صفحه استفاده کنید</li>
    </ul>
    <h2>CSS چه کارهایی می‌کند؟</h2>
    <ul>
      <li>رنگ متن و پس‌زمینه</li>
      <li>اندازه و نوع فونت</li>
      <li>فاصله و حاشیه اطراف عناصر</li>
      <li>چیدمان صفحه (مثلاً دو ستونه یا سه ستونه)</li>
      <li>طراحی واکنش‌گرا برای موبایل و تبلت</li>
      <li>انیمیشن و افکت‌های حرکتی</li>
    </ul>
''')

L["howto"] = ("intro", "syntax", '''
    <h1>چطور CSS را به صفحه اضافه کنیم؟</h1>
    <p>سه روش رایج وجود دارد. بهتر است بیشتر وقت‌ها از روش خارجی (فایل جدا) استفاده کنید.</p>
    <h2>۱. فایل خارجی (پیشنهادی)</h2>
    <p>یک فایل با پسوند <code>.css</code> می‌سازید و در بخش head صفحه به آن لینک می‌دهید:</p>
    <div class="code-box"><code>&lt;link rel="stylesheet" href="styles.css"&gt;</code></div>
    <p>محتوای فایل styles.css مثلاً این است:</p>
    <div class="code-box"><code>body {
  background-color: lightblue;
}
h1 {
  color: navy;
}</code></div>
    <h2>۲. استایل داخلی (Internal)</h2>
    <p>داخل همان صفحه HTML، در head، تگ style می‌گذارید:</p>
    <div class="code-box"><code>&lt;style&gt;
  body { background-color: lightblue; }
  h1 { color: navy; }
&lt;/style&gt;</code></div>
    <h2>۳. استایل خطی (Inline)</h2>
    <p>مستقیماً روی خود عنصر با ویژگی style:</p>
    <div class="code-box"><code>&lt;h1 style="color: blue;"&gt;عنوان آبی&lt;/h1&gt;</code></div>
    <div class="note">استایل خطی فقط برای موارد خیلی خاص مناسب است. برای کل سایت از فایل خارجی استفاده کنید.</div>
''')

L["syntax"] = ("howto", "selectors", '''
    <h1>نحو نوشتن CSS</h1>
    <p>هر قانون CSS از دو قسمت اصلی تشکیل می‌شود: <strong>انتخاب‌گر</strong> و <strong>اعلان</strong>.</p>
    <p>انتخاب‌گر می‌گوید کدام عنصر(ها) را می‌خواهید تغییر دهید. اعلان می‌گوید چه ویژگی‌هایی و با چه مقداری.</p>
    <div class="code-box"><code>selector {
  property: value;
  property: value;
}</code></div>
    <h2>مثال واقعی</h2>
    <div class="code-box"><code>p {
  color: red;
  text-align: center;
}</code></div>
    <p>معنی این کد: همه پاراگراف‌ها (<code>p</code>) رنگ متنشان قرمز شود و متن وسط‌چین باشد.</p>
    <h2>نکات مهم</h2>
    <ul>
      <li>بعد از هر مقدار نقطه‌ویرگول <code>;</code> بگذارید</li>
      <li>اعلان‌ها داخل آکولاد <code>{}</code> هستند</li>
      <li>بین نام ویژگی و مقدار دو نقطه <code>:</code> می‌آید</li>
      <li>حروف بزرگ و کوچک در نام ویژگی‌ها معمولاً مهم نیست، ولی همه با حروف کوچک می‌نویسند</li>
    </ul>
''')

L["selectors"] = ("syntax", "comments", '''
    <h1>انتخاب‌گرها (Selectors)</h1>
    <p>انتخاب‌گر مشخص می‌کند قانون CSS روی کدام قسمت صفحه اعمال شود. یادگیری انتخاب‌گرها پایه کار با CSS است.</p>
    <h2>انتخاب‌گر عنصر</h2>
    <p>نام تگ HTML را می‌نویسید. همه آن تگ‌ها تحت تأثیر قرار می‌گیرند:</p>
    <div class="code-box"><code>p {
  color: red;
}
h1 {
  font-size: 32px;
}</code></div>
    <h2>انتخاب‌گر کلاس</h2>
    <p>با نقطه شروع می‌شود. روی عناصری اعمال می‌شود که آن class را دارند:</p>
    <div class="code-box"><code>.center {
  text-align: center;
}
/* در HTML: &lt;p class="center"&gt;متن وسط&lt;/p&gt; */</code></div>
    <h2>انتخاب‌گر آی‌دی</h2>
    <p>با # شروع می‌شود. معمولاً برای یک عنصر یکتا استفاده می‌شود:</p>
    <div class="code-box"><code>#header {
  background-color: black;
  color: white;
}
/* در HTML: &lt;div id="header"&gt;...&lt;/div&gt; */</code></div>
    <h2>انتخاب‌گر گروهی</h2>
    <p>چند انتخاب‌گر را با کاما جدا می‌کنید تا یک استایل مشترک بگیرند:</p>
    <div class="code-box"><code>h1, h2, p {
  text-align: center;
  color: #333;
}</code></div>
    <div class="note">کلاس را می‌توان روی چند عنصر گذاشت. آی‌دی باید در هر صفحه یکتا باشد.</div>
''')

L["comments"] = ("selectors", "colors", '''
    <h1>توضیحات در CSS</h1>
    <p>توضیحات (کامنت) برای یادداشت خودتان است و مرورگر آن‌ها را اجرا نمی‌کند. برای توضیح دادن بخش‌های پیچیده یا غیرفعال کردن موقت یک قانون مفید است.</p>
    <div class="code-box"><code>/* این یک توضیح است */
p {
  color: red;  /* رنگ قرمز برای پاراگراف */
}

/*
  توضیح چندخطی
  هم امکان‌پذیر است
*/</code></div>
''')

L["colors"] = ("comments", "background", '''
    <h1>رنگ‌ها در CSS</h1>
    <p>رنگ را می‌توانید به چند شکل بنویسید: نام انگلیسی، کد هگزادسیمال، rgb یا hsl. همه این‌ها معتبر هستند.</p>
    <h2>نام رنگ</h2>
    <div class="code-box"><code>h1 { color: red; }
p { color: blue; }</code></div>
    <h2>کد هگز (#)</h2>
    <p>شش رقم بعد از # نشان‌دهنده میزان قرمز، سبز و آبی است:</p>
    <div class="code-box"><code>h1 { color: #ff0000; }  /* قرمز */
h1 { color: #00ff00; }  /* سبز */
h1 { color: #0000ff; }  /* آبی */
h1 { color: #333333; }  /* خاکستری تیره */</code></div>
    <h2>rgb و rgba</h2>
    <p>سه عدد از ۰ تا ۲۵۵ برای قرمز، سبز و آبی. در rgba عدد چهارم شفافیت است (از ۰ تا ۱):</p>
    <div class="code-box"><code>h1 { color: rgb(255, 0, 0); }
h1 { color: rgba(255, 0, 0, 0.5); }  /* نیمه‌شفاف */</code></div>
    <h2>کجا رنگ اعمال می‌شود؟</h2>
    <ul>
      <li><code>color</code> — رنگ متن</li>
      <li><code>background-color</code> — رنگ پس‌زمینه</li>
      <li><code>border-color</code> — رنگ حاشیه</li>
    </ul>
''')

L["background"] = ("colors", "background-image", '''
    <h1>پس‌زمینه (Background)</h1>
    <p>با ویژگی‌های پس‌زمینه می‌توانید رنگ یا تصویر پشت عناصر را تنظیم کنید.</p>
    <h2>رنگ پس‌زمینه</h2>
    <div class="code-box"><code>body {
  background-color: lightblue;
}
div {
  background-color: #0d1117;
}</code></div>
    <h2>چند ویژگی با هم</h2>
    <p>می‌توانید رنگ، تصویر، تکرار و موقعیت را با هم بنویسید:</p>
    <div class="code-box"><code>body {
  background-color: #0f1419;
  background-image: url("bg.jpg");
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
}</code></div>
    <p><code>background-size: cover</code> باعث می‌شود تصویر کل فضا را بپوشاند بدون اینکه کش بیاید بد.</p>
''')

L["background-image"] = ("background", "text", '''
    <h1>تصویر پس‌زمینه</h1>
    <p>با <code>background-image</code> یک عکس پشت عنصر می‌گذارید. مسیر فایل را داخل url می‌نویسید.</p>
    <div class="code-box"><code>body {
  background-image: url("paper.gif");
}
div {
  background-image: url("images/photo.jpg");
}</code></div>
    <h2>تکرار تصویر</h2>
    <div class="code-box"><code>background-repeat: repeat;     /* تکرار افقی و عمودی */
background-repeat: repeat-x;   /* فقط افقی */
background-repeat: repeat-y;   /* فقط عمودی */
background-repeat: no-repeat;  /* بدون تکرار */</code></div>
    <h2>ثابت ماندن هنگام اسکرول</h2>
    <div class="code-box"><code>background-attachment: fixed;</code></div>
''')

L["text"] = ("background-image", "fonts", '''
    <h1>استایل متن</h1>
    <p>CSS کنترل کاملی روی ظاهر متن دارد: رنگ، تراز، زیرخط، فاصله حروف و ارتفاع خط.</p>
    <div class="code-box"><code>h1 {
  color: #58a6ff;
  text-align: center;
  text-decoration: underline;
  text-transform: uppercase;
  letter-spacing: 2px;
  line-height: 1.8;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}</code></div>
    <h2>معنی هر ویژگی</h2>
    <ul>
      <li><code>text-align</code> — چپ، راست، وسط یا justify</li>
      <li><code>text-decoration</code> — زیرخط، روی خط، خط وسط</li>
      <li><code>text-transform</code> — همه حروف بزرگ یا کوچک</li>
      <li><code>letter-spacing</code> — فاصله بین حروف</li>
      <li><code>line-height</code> — فاصله بین خطوط</li>
    </ul>
''')

L["fonts"] = ("text", "icons", '''
    <h1>فونت در CSS</h1>
    <p>با font-family نوع قلم را مشخص می‌کنید. اگر فونت اول روی سیستم کاربر نباشد، مرورگر سراغ بعدی می‌رود.</p>
    <div class="code-box"><code>p {
  font-family: "Vazirmatn", Tahoma, Arial, sans-serif;
  font-size: 16px;
  font-weight: bold;
  font-style: italic;
}</code></div>
    <h2>اندازه فونت</h2>
    <p>می‌توانید با px، em، rem یا درصد بنویسید. برای واکنش‌گرایی اغلب rem بهتر است.</p>
    <div class="code-box"><code>h1 { font-size: 2rem; }
p { font-size: 1rem; }
small { font-size: 0.875rem; }</code></div>
    <div class="note">برای فارسی فونت‌هایی مثل Vazirmatn، IRANSans یا Tahoma مناسب‌اند. می‌توانید از Google Fonts هم استفاده کنید.</div>
''')

L["icons"] = ("fonts", "links", '''
    <h1>آیکون‌ها</h1>
    <p>برای آیکون معمولاً از فونت آیکون (مثل Font Awesome) یا SVG استفاده می‌شود. در HTML آیکون را می‌گذارید و با CSS اندازه و رنگش را عوض می‌کنید.</p>
    <div class="code-box"><code>/* مثال با کلاس آیکون */
.icon {
  font-size: 24px;
  color: #58a6ff;
}</code></div>
''')

L["links"] = ("icons", "box-model", '''
    <h1>استایل لینک‌ها</h1>
    <p>لینک‌ها حالت‌های مختلفی دارند: معمولی، هاور (وقتی موس روی آن است)، ویزیت‌شده و فعال. برای هر کدام می‌توانید استایل جدا بنویسید.</p>
    <div class="code-box"><code>a {
  color: #58a6ff;
  text-decoration: none;
}
a:hover {
  color: #79b8ff;
  text-decoration: underline;
}
a:visited {
  color: #a371f7;
}
a:active {
  color: #ff7b72;
}</code></div>
''')

# ===== BOX MODEL - VERY DETAILED =====
L["box-model"] = ("links", "borders", '''
    <h1>باکس‌مدل چیست؟</h1>
    <p>در CSS هر عنصر HTML مثل یک <strong>جعبه مستطیلی</strong> در نظر گرفته می‌شود. به این مدل فکری می‌گویند <strong>Box Model</strong> یا باکس‌مدل.</p>
    <p>فهمیدن باکس‌مدل برای کنترل فاصله‌ها، اندازه و چیدمان صفحه ضروری است. اگر باکس‌مدل را خوب یاد بگیرید، خیلی از مشکلات چیدمان برایتان حل می‌شود.</p>

    <h2>چهار لایه جعبه</h2>
    <p>هر جعبه از داخل به بیرون این چهار قسمت را دارد:</p>
    <ol>
      <li><strong>Content (محتوا):</strong> خود متن، تصویر یا هر چیزی که داخل عنصر است. عرض و ارتفاع اصلی معمولاً به این بخش اشاره دارد.</li>
      <li><strong>Padding (پدینگ):</strong> فاصله خالی بین محتوا و حاشیه. رنگ پس‌زمینه عنصر تا پدینگ ادامه دارد.</li>
      <li><strong>Border (حاشیه):</strong> خط دور جعبه. می‌تواند ضخامت، رنگ و استایل (مثلاً solid یا dashed) داشته باشد.</li>
      <li><strong>Margin (مارجین):</strong> فاصله بیرون از حاشیه تا عناصر همسایه. مارجین شفاف است و رنگ پس‌زمینه عنصر را ندارد.</li>
    </ol>

    <h2>شکل ذهنی</h2>
    <p>تصور کنید یک عکس داخل قاب است:</p>
    <ul>
      <li>خود عکس = content</li>
      <li>فاصله بین عکس و قاب = padding</li>
      <li>خود قاب چوبی = border</li>
      <li>فاصله قاب تا دیوار یا قاب کناری = margin</li>
    </ul>

    <h2>مثال کامل</h2>
    <p>در کد زیر یک جعبه با عرض ۳۰۰ پیکسل می‌سازیم، ۲۰ پیکسل پدینگ، حاشیه ۵ پیکسلی خاکستری و ۱۰ پیکسل مارجین:</p>
    <div class="code-box"><code>div {
  width: 300px;
  padding: 20px;
  border: 5px solid gray;
  margin: 10px;
  box-sizing: border-box;
}</code></div>

    <h2>عرض واقعی جعبه چقدر می‌شود؟</h2>
    <p>اینجا یک نکته مهم است. به‌طور پیش‌فرض (وقتی box-sizing برابر content-box باشد)، مقدار width فقط به بخش content تعلق دارد. پس عرض کل جعبه می‌شود:</p>
    <p><strong>عرض کل = width + padding چپ و راست + border چپ و راست</strong></p>
    <p>در مثال بالا اگر box-sizing را ننویسیم:</p>
    <ul>
      <li>content: 300px</li>
      <li>padding چپ و راست: 20 + 20 = 40px</li>
      <li>border چپ و راست: 5 + 5 = 10px</li>
      <li><strong>عرض نهایی روی صفحه: 350px</strong></li>
    </ul>
    <p>به همین دلیل خیلی‌ها از <code>box-sizing: border-box</code> استفاده می‌کنند تا width شامل padding و border هم بشود و محاسبه راحت‌تر شود.</p>

    <h2>چرا باکس‌مدل مهم است؟</h2>
    <ul>
      <li>برای اینکه دو ستون دقیقاً کنار هم قرار بگیرند باید فاصله و حاشیه را درست حساب کنید</li>
      <li>برای طراحی کارت، دکمه و منو باید بدانید پدینگ و مارجین چه فرقی دارند</li>
      <li>در طراحی واکنش‌گرا، اشتباه در فهم باکس‌مدل باعث بیرون زدن عناصر از صفحه می‌شود</li>
    </ul>
    <div class="note">در درس‌های بعدی border، margin، padding و box-sizing را جداگانه و با مثال بیشتر بررسی می‌کنیم.</div>
''')

L["borders"] = ("box-model", "margin", '''
    <h1>حاشیه (Border)</h1>
    <p>حاشیه خطی است که دور جعبه عنصر کشیده می‌شود. می‌توانید ضخامت، استایل و رنگ آن را جداگانه یا یکجا تنظیم کنید.</p>
    <h2>نوشتن کوتاه</h2>
    <div class="code-box"><code>p {
  border: 2px solid red;
}</code></div>
    <p>ترتیب معمولاً این است: ضخامت، استایل، رنگ.</p>
    <h2>استایل‌های رایج</h2>
    <ul>
      <li><code>solid</code> — خط یکدست</li>
      <li><code>dashed</code> — خط‌چین</li>
      <li><code>dotted</code> — نقطه‌چین</li>
      <li><code>double</code> — دو خط</li>
      <li><code>none</code> — بدون حاشیه</li>
    </ul>
    <h2>فقط یک طرف</h2>
    <div class="code-box"><code>p {
  border-top: 5px solid blue;
  border-bottom: 1px dashed gray;
}</code></div>
    <h2>گوشه‌های گرد</h2>
    <div class="code-box"><code>div {
  border: 2px solid #58a6ff;
  border-radius: 12px;
}</code></div>
    <p>با border-radius گوشه‌ها گرد می‌شوند. اگر مقدار را 50% بگذارید و عرض و ارتفاع برابر باشد، شکل دایره می‌شود.</p>
''')

L["margin"] = ("borders", "padding", '''
    <h1>فاصله بیرونی (Margin)</h1>
    <p>مارجین فاصله بین لبه بیرونی حاشیه عنصر و عناصر اطراف است. مارجین رنگ ندارد و شفاف است.</p>
    <h2>نوشتن یک مقدار</h2>
    <div class="code-box"><code>p {
  margin: 20px;  /* هر چهار طرف 20 پیکسل */
}</code></div>
    <h2>چهار مقدار (بالا، راست، پایین، چپ)</h2>
    <div class="code-box"><code>p {
  margin: 10px 20px 10px 20px;
}</code></div>
    <h2>دو مقدار (عمودی افقی)</h2>
    <div class="code-box"><code>p {
  margin: 10px 20px;  /* بالا و پایین 10، چپ و راست 20 */
}</code></div>
    <h2>وسط‌چین کردن افقی</h2>
    <p>اگر عنصر عرض مشخص داشته باشد، با مارجین چپ و راست auto وسط صفحه قرار می‌گیرد:</p>
    <div class="code-box"><code>div {
  width: 300px;
  margin: 0 auto;
}</code></div>
    <div class="note">مارجین‌های عمودی دو عنصر همسایه ممکن است «ادغام» شوند (margin collapse). یعنی به‌جای جمع دو مارجین، بزرگ‌تر آن‌ها اعمال شود.</div>
''')

L["padding"] = ("margin", "width-height", '''
    <h1>فاصله داخلی (Padding)</h1>
    <p>پدینگ فاصله بین محتوا و حاشیه است. برخلاف مارجین، پدینگ داخل جعبه است و رنگ پس‌زمینه عنصر تا انتهای پدینگ ادامه دارد.</p>
    <h2>مثال</h2>
    <div class="code-box"><code>div {
  padding: 20px;
  background-color: #161b22;
  border: 1px solid #30363d;
}</code></div>
    <p>متن داخل این div از لبه‌ها ۲۰ پیکسل فاصله می‌گیرد و آن فضای خالی هم همان رنگ پس‌زمینه را دارد.</p>
    <h2>چهار طرف جدا</h2>
    <div class="code-box"><code>div {
  padding-top: 10px;
  padding-right: 20px;
  padding-bottom: 10px;
  padding-left: 20px;
}
/* یا کوتاه: */
div {
  padding: 10px 20px;
}</code></div>
    <h2>فرق پدینگ و مارجین</h2>
    <ul>
      <li>پدینگ داخل جعبه است و رنگ پس‌زمینه دارد</li>
      <li>مارجین بیرون جعبه است و شفاف است</li>
      <li>پدینگ روی اندازه کلی جعبه (در حالت content-box) اثر می‌گذارد</li>
    </ul>
''')

L["width-height"] = ("padding", "box-sizing", '''
    <h1>عرض و ارتفاع</h1>
    <p>با width و height اندازه جعبه محتوا را مشخص می‌کنید. می‌توانید از پیکسل، درصد یا واحدهای نسبی استفاده کنید.</p>
    <div class="code-box"><code>div {
  width: 300px;
  height: 200px;
}
div {
  width: 50%;   /* نصف عرض والد */
  max-width: 600px;
  min-height: 100px;
}</code></div>
    <p><code>max-width</code> جلوی بزرگ شدن بیش از حد را می‌گیرد و برای واکنش‌گرایی خیلی مفید است. <code>min-height</code> حداقل ارتفاع را تضمین می‌کند.</p>
''')

L["box-sizing"] = ("width-height", "display", '''
    <h1>box-sizing</h1>
    <p>این ویژگی مشخص می‌کند width و height شامل padding و border بشوند یا نه.</p>
    <h2>content-box (پیش‌فرض)</h2>
    <p>width فقط محتوا را اندازه می‌گیرد. پدینگ و حاشیه اضافه می‌شوند و جعبه بزرگ‌تر از عدد width می‌شود.</p>
    <h2>border-box (پیشنهادی)</h2>
    <p>width شامل محتوا + پدینگ + حاشیه است. محاسبه ساده‌تر می‌شود و برای چیدمان‌های دقیق بهتر است.</p>
    <div class="code-box"><code>* {
  box-sizing: border-box;
}
div {
  width: 300px;
  padding: 20px;
  border: 5px solid gray;
  /* عرض کل همان 300px می‌ماند */
}</code></div>
    <div class="note">خیلی از پروژه‌ها در ابتدای CSS این قانون را برای همه عناصر می‌گذارند: * { box-sizing: border-box; }</div>
''')

L["display"] = ("box-sizing", "position", '''
    <h1>ویژگی display</h1>
    <p>display مشخص می‌کند عنصر چگونه در جریان صفحه قرار بگیرد و آیا مثل بلوک کل عرض را بگیرد یا مثل متن در یک خط بماند.</p>
    <h2>مقادیر مهم</h2>
    <div class="code-box"><code>div { display: block; }         /* بلوک کامل */
span { display: inline; }        /* در جریان متن */
div { display: inline-block; }   /* ترکیبی */
div { display: none; }           /* مخفی کامل */
div { display: flex; }           /* فلکس */
div { display: grid; }           /* گرید */</code></div>
    <ul>
      <li><strong>block:</strong> از خط جدید شروع می‌شود و تا جایی که ممکن است عرض می‌گیرد (مثل div و p)</li>
      <li><strong>inline:</strong> در همان خط می‌ماند و width/height معمولاً اثر ندارد (مثل span و a)</li>
      <li><strong>inline-block:</strong> در خط می‌ماند ولی می‌توانید عرض و ارتفاع بدهید</li>
      <li><strong>none:</strong> عنصر اصلاً در صفحه نیست (فضا هم اشغال نمی‌کند)</li>
    </ul>
''')

L["position"] = ("display", "z-index", '''
    <h1>موقعیت (Position)</h1>
    <p>با position می‌توانید عنصر را از جریان عادی صفحه خارج کنید یا نسبت به موقعیت عادی‌اش جابه‌جا کنید.</p>
    <div class="code-box"><code>div { position: static; }    /* پیش‌فرض */
div { position: relative; top: 10px; left: 20px; }
div { position: absolute; top: 0; right: 0; }
div { position: fixed; bottom: 0; left: 0; }
div { position: sticky; top: 0; }</code></div>
    <ul>
      <li><strong>relative:</strong> نسبت به جای عادی خودش جابه‌جا می‌شود، فضای قبلی‌اش حفظ می‌شود</li>
      <li><strong>absolute:</strong> نسبت به نزدیک‌ترین والد دارای position غیر static قرار می‌گیرد</li>
      <li><strong>fixed:</strong> نسبت به پنجره مرورگر ثابت می‌ماند (مثلاً منوی چسبان)</li>
      <li><strong>sticky:</strong> تا وقتی اسکرول به آستانه نرسیده عادی است، بعد مثل fixed می‌چسبد</li>
    </ul>
''')

L["z-index"] = ("position", "overflow", '''
    <h1>z-index</h1>
    <p>وقتی عناصر روی هم می‌افتند، z-index مشخص می‌کند کدام رو و کدام زیر باشد. عدد بزرگ‌تر بالاتر دیده می‌شود. فقط روی عناصری که position غیر static دارند اثر دارد.</p>
    <div class="code-box"><code>.box1 {
  position: absolute;
  z-index: 1;
}
.box2 {
  position: absolute;
  z-index: 2;  /* روی box1 می‌آید */
}</code></div>
''')

L["overflow"] = ("z-index", "float", '''
    <h1>overflow</h1>
    <p>وقتی محتوا از اندازه جعبه بیشتر شود، overflow می‌گوید چه اتفاقی بیفتد.</p>
    <div class="code-box"><code>div {
  width: 200px;
  height: 100px;
  overflow: visible;  /* بیرون بزند (پیش‌فرض) */
  overflow: hidden;   /* بریده شود */
  overflow: scroll;   /* همیشه اسکرول */
  overflow: auto;     /* در صورت نیاز اسکرول */
}</code></div>
''')

L["float"] = ("overflow", "flexbox", '''
    <h1>float</h1>
    <p>float عنصر را به چپ یا راست می‌چسباند و متن دورش می‌پیچد. در گذشته برای چیدمان ستون‌ها استفاده می‌شد؛ امروز بیشتر Flexbox و Grid جایگزین آن شده‌اند، ولی هنوز برای قرار دادن تصویر کنار متن کاربرد دارد.</p>
    <div class="code-box"><code>img {
  float: left;
  margin-right: 16px;
}</code></div>
''')

L["flexbox"] = ("float", "flex-container", '''
    <h1>Flexbox چیست؟</h1>
    <p>Flexbox یک روش مدرن برای چیدن عناصر در یک ردیف یا ستون است. برای وسط‌چین کردن، توزیع فضای خالی و هم‌تراز کردن آیتم‌ها بسیار قوی است.</p>
    <p>والد را display: flex می‌کنید؛ فرزندان می‌شوند آیتم‌های فلکس.</p>
    <div class="code-box"><code>.container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}
.item {
  flex: 1;
}</code></div>
    <p><code>justify-content</code> تراز در محور اصلی (معمولاً افقی) و <code>align-items</code> تراز در محور عمود است. <code>gap</code> فاصله بین آیتم‌ها را می‌دهد.</p>
''')

L["flex-container"] = ("flexbox", "flex-item", '''
    <h1>کانتینر Flex</h1>
    <p>ویژگی‌های مهم روی خود والد (کانتینر):</p>
    <div class="code-box"><code>.container {
  display: flex;
  flex-direction: row;       /* یا column */
  flex-wrap: wrap;           /* اگر جا نشد برود خط بعد */
  justify-content: space-between;
  align-items: stretch;
  gap: 12px;
}</code></div>
    <ul>
      <li><code>flex-direction</code> — ردیف یا ستون</li>
      <li><code>flex-wrap</code> — آیا آیتم‌ها به خط بعد بروند</li>
      <li><code>justify-content</code> — توزیع در محور اصلی</li>
      <li><code>align-items</code> — تراز در محور متقاطع</li>
    </ul>
''')

L["flex-item"] = ("flex-container", "grid", '''
    <h1>آیتم Flex</h1>
    <p>روی هر فرزند می‌توانید بگویید چقدر از فضا را بگیرد:</p>
    <div class="code-box"><code>.item {
  flex: 1;           /* رشد برابر */
  flex-grow: 2;      /* دو برابر بقیه رشد کند */
  flex-shrink: 0;    /* جمع نشود */
  flex-basis: 200px; /* اندازه پایه */
  align-self: center;
}</code></div>
''')

L["grid"] = ("flex-item", "grid-container", '''
    <h1>CSS Grid</h1>
    <p>Grid برای چیدمان دوبعدی (ردیف و ستون با هم) ساخته شده است. برای صفحه کامل یا بخش‌های پیچیده مثل گالری و داشبورد عالی است.</p>
    <div class="code-box"><code>.container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}
.item {
  grid-column: span 2;  /* دو ستون را بگیرد */
}</code></div>
    <p><code>1fr</code> یعنی یک سهم از فضای آزاد. سه تا 1fr یعنی سه ستون برابر.</p>
''')

L["grid-container"] = ("grid", "media", '''
    <h1>کانتینر Grid</h1>
    <div class="code-box"><code>.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto;
  gap: 16px 24px;
  justify-items: center;
  align-items: start;
}</code></div>
    <p><code>repeat(3, 1fr)</code> همان سه ستون برابر است. gap اول فاصله ردیف و دومی فاصله ستون است.</p>
''')

L["media"] = ("grid-container", "units", '''
    <h1>Media Query — طراحی واکنش‌گرا</h1>
    <p>با Media Query می‌توانید برای عرض‌های مختلف صفحه استایل متفاوت بنویسید. مثلاً در موبایل منو زیر هم باشد و در دسکتاپ کنار هم.</p>
    <div class="code-box"><code>/* پیش‌فرض (موبایل اول) */
.container {
  flex-direction: column;
}

/* از عرض 768 پیکسل به بالا */
@media (min-width: 768px) {
  .container {
    flex-direction: row;
  }
}

/* تا عرض 600 پیکسل */
@media (max-width: 600px) {
  body {
    font-size: 14px;
  }
}</code></div>
    <div class="note">رویکرد Mobile First یعنی اول برای موبایل بنویسید و بعد با min-width برای صفحه‌های بزرگ‌تر اضافه کنید.</div>
''')

L["units"] = ("media", "transition", '''
    <h1>واحدهای اندازه</h1>
    <ul>
      <li><code>px</code> — پیکسل ثابت</li>
      <li><code>%</code> — نسبت به والد</li>
      <li><code>em</code> — نسبت به فونت همان عنصر</li>
      <li><code>rem</code> — نسبت به فونت ریشه (html)</li>
      <li><code>vw / vh</code> — درصد عرض / ارتفاع پنجره مرورگر</li>
    </ul>
    <div class="code-box"><code>html { font-size: 16px; }
p { font-size: 1rem; }     /* 16px */
h1 { font-size: 2rem; }    /* 32px */
.box { width: 50%; }
.hero { height: 100vh; }</code></div>
''')

L["transition"] = ("units", "animation", '''
    <h1>Transition</h1>
    <p>Transition تغییر ویژگی را نرم و تدریجی می‌کند. مثلاً وقتی رنگ دکمه عوض می‌شود، ناگهانی نباشد.</p>
    <div class="code-box"><code>button {
  background-color: #58a6ff;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #388bfd;
}</code></div>
''')

L["animation"] = ("transition", "transform", '''
    <h1>Animation</h1>
    <p>با @keyframes مسیر انیمیشن را تعریف می‌کنید و با animation آن را به عنصر می‌چسبانید.</p>
    <div class="code-box"><code>@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.box {
  animation: fadeIn 1s ease forwards;
}</code></div>
''')

L["transform"] = ("animation", "shadow", '''
    <h1>Transform</h1>
    <p>عنصر را جابه‌جا، بچرخانید، بزرگ یا کج کنید بدون اینکه روی جریان بقیه صفحه اثر زیاد بگذارد.</p>
    <div class="code-box"><code>div {
  transform: translateX(20px);
  transform: rotate(15deg);
  transform: scale(1.2);
  transform: skewX(10deg);
}</code></div>
''')

L["shadow"] = ("transform", None, '''
    <h1>سایه</h1>
    <p>با box-shadow سایه دور جعبه و با text-shadow سایه متن می‌سازید.</p>
    <div class="code-box"><code>div {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
h1 {
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4);
}</code></div>
    <p>ترتیب معمول box-shadow: جابه‌جایی افقی، جابه‌جایی عمودی، محو شدن، گسترش، رنگ.</p>
''')


def main():
    order = []
    for _, items in SIDEBAR:
        for slug, _ in items:
            order.append(slug)

    for i, slug in enumerate(order):
        prev_s = order[i - 1] if i > 0 else None
        next_s = order[i + 1] if i < len(order) - 1 else None
        if slug in L:
            p, n, body = L[slug]
            # use chain from order for nav consistency
            prev_s = prev_s
            next_s = next_s
        else:
            body = f'''
    <h1>{slug}</h1>
    <p>این بخش از آموزش CSS است. توضیحات و مثال‌ها بر اساس ساختار W3Schools و به زبان ساده نوشته شده‌اند.</p>
    <p>از منوی کناری درس‌های مرتبط را دنبال کنید تا با باکس‌مدل، فلکس، گرید و طراحی واکنش‌گرا آشنا شوید.</p>
'''
        title = slug.replace("-", " ")
        if slug in L:
            # extract h1 from body if possible
            title = "آموزش CSS"
        html = page(slug, title, body if slug in L else body, prev_s, next_s)
        # fix: use correct body
        if slug in L:
            _, _, body = L[slug]
            html = page(slug, "آموزش CSS", body, prev_s, next_s)
        fname = "css.html" if slug == "index" else f"{slug}.html"
        (BASE / fname).write_text(html, encoding="utf-8")
        print(fname)
    print(f"Total CSS lessons: {len(order)}")


if __name__ == "__main__":
    main()

var EXERCISES = [
  {
    id: "py-1",
    language: "python",
    title: "اولین چاپ",
    difficulty: "easy",
    topic: "شروع و print",
    description:
      'می‌خواهم روی صفحه (یا در خروجی) یک جملهٔ ساده از خودت ببینی. با print همان جمله‌ای را بنویس که دوست داری؛ فقط یادت باشد متن را داخل " (دابل‌کوتیشن) بگذاری.',
    exampleInput: "",
    exampleOutput: "",
    hints: [
      'اول فقط یک خط با print بنویس و اجرا کن. اگر چیزی ندیدی، ببین خطایت دربارهٔ پرانتز است یا دربارهٔ " (دابل‌کوتیشن).',
      'متن را بین دو تا " بگذار؛ اگر یکی‌شان جا بیفتد پایتون گیج می‌شود و خطا می‌دهد.',
      "نگران قشنگ بودن جمله نباش. هدف این تمرین فقط این است که خروجی را با چشم خودت ببینی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["print"],
  },
  {
    id: "py-2",
    language: "python",
    title: "چند چیز با هم",
    difficulty: "easy",
    topic: "شروع و print",
    description:
      "حالا یک قدم جلوتر: هم یک عدد و هم یک متن را نشان بده. می‌توانی با یک print چند چیز را پشت‌سرهم چاپ کنی، یا از دو print جدا استفاده کنی — هر طور برایت روشن‌تر است.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      'می‌توانی بنویسی print(10, "سیب") تا عدد و متن کنار هم بیایند.',
      "اگر دوست داری مرتب‌تر باشد، دو بار print جدا هم کاملاً درست است.",
      "فرقی ندارد کدام روش را انتخاب کنی؛ مهم این است که هر دو مقدار را واقعاً در خروجی ببینی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["print"],
  },
  {
    id: "py-3",
    language: "python",
    title: "اسم من در متغیر",
    difficulty: "easy",
    topic: "متغیرها",
    description:
      "یک اسم (مثلاً اسم خودت) را در یک متغیر نگه دار و بعد همان را چاپ کن. ایده این است که یک‌بار بنویسی و هر وقت لازم شد فقط نام متغیر را صدا بزنی.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      'اول یک نام انتخاب کن، مثلاً name، بعد با = مقدار بده: name = "سارا".',
      'برای دیدن مقدار، کافی است print(name) بنویسی — بدون " دور خودِ name، چون name متغیر است نه متن ثابت.',
      'اگر اشتباهاً print("name") بنویسی، خودِ کلمهٔ name چاپ می‌شود نه مقداری که ذخیره کردی.',
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["متغیرها"],
  },
  {
    id: "py-4",
    language: "python",
    title: "سن که عوض می‌شود",
    difficulty: "easy",
    topic: "متغیرها",
    description:
      "سن را در یک متغیر بگذار. بعد همان متغیر را یکی زیاد کن و دوباره چاپ کن. می‌خواهم ببینی متغیر یعنی چیزی که می‌توانی بعداً عوضش کنی.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "مثلاً age = 20 بگذار. بعد در خط بعد بنویس age = age + 1 تا یکی به آن اضافه شود.",
      "اگر بنویسی age + 1 ولی نتیجه را دوباره در age ذخیره نکنی، متغیر همان مقدار قبلی می‌ماند.",
      "در پایان print(age) را بگذار تا عدد جدید را ببینی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["متغیرها"],
  },
  {
    id: "py-5",
    language: "python",
    title: "بفهمم چه نوعی است",
    difficulty: "easy",
    topic: "انواع داده",
    description:
      'چهار مقدار مختلف را با type بررسی کن: یک عدد صحیح، یک عدد اعشاری، یک متن داخل "، و True. خروجی type را چاپ کن تا ببینی پایتون به هر کدام چه می‌گوید.',
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "type را مثل یک برچسب‌خوان در نظر بگیر: type(10) می‌گوید این مقدار از نظر پایتون چیست.",
      'برای متن حتماً " بگذار؛ وگرنه پایتون فکر می‌کند نام یک متغیر را نوشته‌ای.',
      "True را با T بزرگ بنویس؛ true کوچک در پایتون همان معنی را نمی‌دهد.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["نوع داده ها"],
  },
  {
    id: "py-6",
    language: "python",
    title: "رشته را به عدد تبدیل کن",
    difficulty: "easy",
    topic: "انواع داده",
    description:
      'فرض کن مقدار "20" را به‌صورت متن داری. آن را به عدد تبدیل کن، با ۵ جمع بزن و نتیجه را چاپ کن. اگر تبدیل نکنی، جمع مثل چسباندن متن می‌شود نه حساب واقعی.',
    exampleInput: "",
    exampleOutput: "",
    hints: [
      '"20" ظاهرش عدد است ولی نوعش متن است. برای حساب، اول int("20") را در یک متغیر بریز.',
      'بعد آن متغیر را با ۵ جمع کن. اگر مستقیم "20" + 5 بنویسی معمولاً خطا می‌گیری.',
      "وقتی نتیجه را چاپ کردی، باید ۲۵ ببینی نه چیزی شبیه چسباندن متن.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["تبدیل نوع داده"],
  },
  {
    id: "py-7",
    language: "python",
    title: "جمع دو عددی که کاربر می‌دهد",
    difficulty: "easy",
    topic: "عملگرها و input",
    description:
      "از کاربر دو عدد بگیر و حاصل جمعشان را نشان بده. یادت باشد input همیشه متن برمی‌گرداند؛ برای جمع باید هر کدام را به عدد تبدیل کنی.",
    exampleInput: "5\n3",
    exampleOutput: "8",
    hints: [
      "هر بار input یک خط از کاربر می‌گیرد و آن را به‌صورت متن برمی‌گرداند — حتی اگر کاربر رقم زده باشد.",
      'پس برای هر عدد بنویس int(input("...")) تا قابل جمع شدن شود.',
      "اگر یکی را int نکنی، با + ممکن است به‌جای جمع، چسباندن عجیب یا خطا ببینی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["عملگرهای حسابی", "input"],
  },
  {
    id: "py-8",
    language: "python",
    title: "فرق تقسیم معمولی و صحیح",
    difficulty: "easy",
    topic: "عملگرهای حسابی",
    description:
      "عددهای ۷ و ۲ را یک‌بار با / و یک‌بار با // تقسیم کن و هر دو نتیجه را چاپ کن. می‌خواهم خودت ببینی خروجی‌ها یکی نیستند و هرکدام به چه درد می‌خورد.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "یک‌بار print(7 / 2) و یک‌بار print(7 // 2) را جدا اجرا کن و دو خروجی را کنار هم مقایسه کن.",
      "اسلش تنها معمولاً جواب اعشاری می‌دهد؛ دو اسلش بیشتر به «چند تا کامل جا می‌شود» نزدیک است.",
      "این تمرین حفظ کردن تعریف نیست؛ دیدن فرق با چشم خودت است.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["عملگرهای حسابی"],
  },
  {
    id: "py-9",
    language: "python",
    title: "باقی‌مانده و توان",
    difficulty: "easy",
    topic: "عملگرهای حسابی",
    description:
      "با % بگو باقی‌ماندهٔ ۱۰ بر ۳ چیست، و با ** بگو ۲ به توان ۸ چند می‌شود. هر دو را چاپ کن.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "باقی‌مانده یعنی بعد از تقسیم، چه چیزی می‌ماند. برای ۱۰ و ۳ بنویس 10 % 3.",
      "توان یعنی چند بار در خودش ضرب شود: 2 ** 8 یعنی ۲ را هشت‌بار در خودش ضرب کنی.",
      "هر کدام را در یک print جدا بگذار تا قاطی نشوند.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["عملگرهای حسابی"],
  },
  {
    id: "py-10",
    language: "python",
    title: "امتیاز را کم‌کم زیاد کن",
    difficulty: "easy",
    topic: "عملگرهای انتسابی",
    description:
      "یک متغیر score از صفر شروع کن. سه بار، هر بار ۵ تا با += به آن اضافه کن و در پایان امتیاز نهایی را چاپ کن. این همان کار score = score + 5 است، فقط کوتاه‌تر.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "score = 0 را اول بنویس تا شروع مشخص باشد.",
      "هر بار score += 5 یعنی «همان امتیاز قبلی را بردار، ۵ تا اضافه کن، دوباره بگذار جای score».",
      "اگر هنوز حلقه نخوانده‌ای، سه بار نوشتن score += 5 کاملاً قابل قبول است.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["عملگرهای انتسابی"],
  },
  {
    id: "py-11",
    language: "python",
    title: "آیا این دو عدد برابرند؟",
    difficulty: "easy",
    topic: "عملگرهای مقایسه",
    description:
      "دو عدد در متغیر بگذار و با == بپرس آیا برابرند. نتیجه True یا False است؛ همان را چاپ کن. بعد با != نابرابری را هم یک‌بار ببین.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "یک = مقدار را ذخیره می‌کند. دو تا == می‌پرسد «آیا برابرند؟».",
      "نتیجهٔ مقایسه همیشه True یا False است؛ همان را print کن.",
      "برای نابرابری از != استفاده کن و همان دو عدد را دوباره بپرس.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["عملگرهای مقایسه ای"],
  },
  {
    id: "py-12",
    language: "python",
    title: "بالغ یا نه؟",
    difficulty: "easy",
    topic: "شرط",
    description:
      "سن را از کاربر بگیر. اگر ۱۸ یا بیشتر بود پیام «بالغ» و در غیر این صورت «نابالغ» چاپ کن. این تمرین برای این است که if و else را در یک تصمیم واقعی ببینی.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "سن را با int(input(...)) بگیر تا عدد باشد، نه متن.",
      "شرط را ساده بنویس: if age >= 18: و در تورفتگیِ زیرش پیام «بالغ» را print کن.",
      "else برای همهٔ حالت‌های باقی‌مانده است؛ لازم نیست شرط را دوباره پیچیده کنی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["شرط‌ها", "عملگرهای مقایسه ای"],
  },
  {
    id: "py-13",
    language: "python",
    title: "زوج یا فرد",
    difficulty: "easy",
    topic: "شرط",
    description:
      "یک عدد بگیر. اگر بر ۲ بخش‌پذیر بود «زوج»، وگرنه «فرد» چاپ کن. باقی‌مانده با % به‌دست می‌آید.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "ایدهٔ زوج بودن این است که باقی‌مانده بر ۲ صفر باشد: n % 2 == 0.",
      "این را داخل if بگذار و در شاخهٔ else پیام فرد را بنویس.",
      "عدد را از کاربر بگیر تا بتوانی چند مقدار مختلف را خودت آزمایش کنی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["شرط‌ها"],
  },
  {
    id: "py-14",
    language: "python",
    title: "ورود با دو شرط",
    difficulty: "medium",
    topic: "عملگرهای منطقی",
    description:
      "سن را عدد بگیر و یک متغیر has_id هم True یا False بگذار. فقط وقتی سن حداقل ۱۸ است و has_id هم True است، پیام «ورود مجاز» بده؛ وگرنه «ورود غیرمجاز».",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "دو چیز را جدا آماده کن: سن عددی، و has_id که True یا False است.",
      "and وقتی True می‌شود که سمت چپ و راست هر دو True باشند.",
      "پیام را طوری بنویس که اگر یکی از دو شرط برقرار نبود، کاربر بفهمد ورود مجاز نیست.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["عملگرهای منطقی", "شرط‌ها"],
  },
  {
    id: "py-15",
    language: "python",
    title: "چاپ عددهای ۱ تا ۵",
    difficulty: "easy",
    topic: "حلقه",
    description:
      "با یک حلقه for عددهای ۱،۲،۳،۴،۵ را زیر هم چاپ کن. هدف این است که تکرار را به پایتون بسپاری، نه اینکه پنج بار print جدا بنویسی.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "range(1, 6) عددهای ۱ تا ۵ را می‌دهد؛ خود ۶ را شامل نمی‌شود.",
      "حلقه را این‌طور بخوان: «برای هر i در این دامنه، یک‌بار print کن».",
      "تورفتگی زیر for را فراموش نکن؛ در پایتون تورفتگی معنا دارد.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["حلقه‌ها"],
  },
  {
    id: "py-16",
    language: "python",
    title: "مجموع از ۱ تا n",
    difficulty: "medium",
    topic: "حلقه",
    description:
      "عدد n را از کاربر بگیر و مجموع عددهای ۱ تا n را حساب کن. مثلاً اگر n برابر ۵ باشد، باید ۱+۲+۳+۴+۵ یعنی ۱۵ را ببینی.",
    exampleInput: "5",
    exampleOutput: "15",
    hints: [
      "قبل از حلقه total = 0 بگذار. این ظرف خالیِ جمع است.",
      "داخل حلقه بنویس total = total + i تا هر عدد به مجموع قبلی اضافه شود.",
      "print را بعد از تمام شدن حلقه بگذار؛ اگر داخل حلقه باشد هر مرحله چاپ می‌شود.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["حلقه‌ها"],
  },
  {
    id: "py-17",
    language: "python",
    title: "طول یک جمله",
    difficulty: "easy",
    topic: "رشته",
    description:
      'یک جملهٔ ثابت داخل " بگذار و با len بگو چند نویسه دارد. فاصله و علائم هم شمرده می‌شوند.',
    exampleInput: "",
    exampleOutput: "",
    hints: [
      'یک متغیر متنی بساز، مثلاً s = "سلام دنیا".',
      "len(s) تعداد نویسه‌ها را می‌شمارد؛ فاصله هم یک نویسه حساب می‌شود.",
      "اگر خواستی، یک‌بار متن کوتاه و یک‌بار متن بلند را امتحان کن تا فرق عدد را ببینی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["رشته ها"],
  },
  {
    id: "py-18",
    language: "python",
    title: "اولین حرف",
    difficulty: "easy",
    topic: "رشته",
    description:
      "یک متن ثابت انتخاب کن و فقط اولین نویسه‌اش را چاپ کن. شمارش از صفر است؛ پس اولین خانه می‌شود [0].",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "نویسه‌ها مثل خانه‌های شماره‌گذاری‌شده‌اند و از صفر شروع می‌شوند.",
      "پس اولین حرف می‌شود s[0]. دومین حرف s[1] است.",
      "اگر شماره را از خودِ طول رشته بزرگ‌تر بدهی، خطا می‌گیری؛ از آن نترس، فقط محدوده‌ات را درست کن.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["رشته ها"],
  },
  {
    id: "py-19",
    language: "python",
    title: "لیست خرید کوچک",
    difficulty: "easy",
    topic: "لیست",
    description:
      "یک لیست سه آیتمی (مثلاً سه میوه) بساز. اولی را جدا چاپ کن، بعد خود لیست را هم یک‌بار کامل چاپ کن.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      'لیست را با قلاب می‌سازی: fruits = ["سیب", "گلابی", "موز"].',
      "برای عضو اول: fruits[0]. برای دیدن همه: print(fruits).",
      "ترتیب مهم است؛ همان چیزی که اول نوشتی، خانهٔ صفر می‌شود.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["لیست ها"],
  },
  {
    id: "py-20",
    language: "python",
    title: "اضافه کردن به لیست",
    difficulty: "easy",
    topic: "لیست",
    description:
      "یک لیست خالی بساز. با append دو چیز به آن اضافه کن و در پایان لیست را چاپ کن تا ببینی ترتیب همان ترتیب اضافه‌شدن است.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "با items = [] یک لیست خالی بساز.",
      "هر append یک عضو به انتها اضافه می‌کند؛ انگار ته صف می‌ایستد.",
      "دو بار append کن و بعد یک‌بار کل لیست را چاپ کن تا ترتیب را ببینی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["لیست ها"],
  },
  {
    id: "py-21",
    language: "python",
    title: "پیمایش لیست",
    difficulty: "easy",
    topic: "لیست",
    description:
      "یک لیست چند کلمه‌ای بساز و با for هر عضو را در یک خط جدا چاپ کن. این الگو بعداً خیلی تکرار می‌شود.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "حلقهٔ for روی لیست یعنی: «هر بار یکی از عضو را بردار و با آن کاری بکن».",
      "بنویس for x in items: و زیرش print(x).",
      "نام x را هر چه دوست داری بگذار؛ مهم این است که داخل حلقه از همان نام استفاده کنی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["لیست ها"],
  },
  {
    id: "py-22",
    language: "python",
    title: "دفترچهٔ کوچک با دیکشنری",
    difficulty: "easy",
    topic: "دیکشنری",
    description:
      "یک دیکشنری با دو کلید name و city بساز و مقدار name را چاپ کن. اینجا برخلاف لیست، با نام کلید سراغ مقدار می‌روی نه با شماره.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      'دیکشنری جفتِ «کلید تا مقدار» است: {"name": "سارا", "city": "تهران"}.',
      'برای خواندن مقدار name بنویس user["name"]؛ کلید را داخل " بگذار.',
      "اگر کلید را غلط بنویسی KeyError می‌گیری؛ املای کلید را با همان چیزی که ساختی یکی کن.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["دیکشنری ها"],
  },
  {
    id: "py-23",
    language: "python",
    title: "تابع سلام",
    difficulty: "easy",
    topic: "توابع",
    description:
      "تابعی به نام greet بنویس که وقتی صدا زده می‌شود فقط یک پیام خوش‌آمد چاپ کند. بعد همان تابع را یک‌بار فراخوانی کن.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "تعریف تابع با def شروع می‌شود و یک نام و پرانتز دارد: def greet():",
      "خط‌های داخل تابع باید تورفتگی داشته باشند. آنجا print پیام را بگذار.",
      "تعریفِ تنها کافی نیست؛ بعد از آن یک خط greet() بنویس تا اجرا شود.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["توابع"],
  },
  {
    id: "py-24",
    language: "python",
    title: "تابع جمع",
    difficulty: "medium",
    topic: "توابع",
    description:
      "تابعی بنویس که دو عدد بگیرد، جمعشان را با return برگرداند. بعد نتیجه را در یک متغیر بریز یا مستقیم چاپ کن. می‌خواهم فرق print داخل تابع با return را حس کنی.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "وقتی می‌خواهی نتیجه را «ببری بیرون»، از return استفاده کن نه فقط print.",
      "مثلاً return a + b مقدار را به جایی که تابع را صدا زدی برمی‌گرداند.",
      "می‌توانی بنویسی result = add(2, 3) و بعد print(result) تا برگشت مقدار را ببینی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["توابع"],
  },
  {
    id: "py-25",
    language: "python",
    title: "مواظب تقسیم بر صفر",
    difficulty: "medium",
    topic: "مدیریت خطا",
    description:
      "دو عدد بگیر و تقسیم را انجام بده. اگر کاربر دوم را صفر داد، برنامه نباید بترکد؛ با try/except پیام آرام و خوانا نشان بده.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "کدِ خطرناک (تقسیم) را داخل try بگذار تا اگر خطا شد، برنامه راه دیگری داشته باشد.",
      "except ZeroDivisionError: جایی است که پیام آرام خودت را print می‌کنی.",
      "پیام را جوری بنویس که کاربر بفهمد چه کار اشتباهی کرده، نه فقط یک کلمهٔ فنی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["try...except"],
  },
  {
    id: "html-1",
    language: "html",
    title: "اولین صفحه",
    difficulty: "easy",
    topic: "پایه",
    description:
      "یک فایل HTML خیلی ساده بساز که اسکلت درست داشته باشد: DOCTYPE، html با زبان فارسی و راست‌به‌چپ، head با charset، و body. داخل body فقط یک عنوان کوتاه بگذار تا در مرورگر چیزی ببینی.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "از یک فایل با پسوند .html شروع کن و همان اسکلتی را بنویس که در درس پایه دیدی.",
      "در head حداقل charset را UTF-8 بگذار تا فارسی خراب نشود.",
      "یک h1 کوچک داخل body کافی است تا مطمئن شوی صفحه در مرورگر باز می‌شود.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["پایه ها"],
  },
  {
    id: "html-2",
    language: "html",
    title: "عنوان تب و عنوان صفحه",
    difficulty: "easy",
    topic: "پایه و متن",
    description:
      "صفحه‌ای بساز که تب مرورگر متن «تمرین من» را نشان دهد و داخل خود صفحه هم یک h1 معنی‌دار داشته باشی. این دو تا یکی نیستند: یکی برای تب است، یکی برای خود محتوا.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "متن تب مرورگر از تگ title می‌آید؛ آن را داخل head بگذار.",
      "عنوانی که وسط صفحه می‌بینی معمولاً h1 است و جایش داخل body است.",
      "عمداً دو متن متفاوت برای title و h1 بگذار تا فرق‌شان را حس کنی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["پایه ها", "متن"],
  },
  {
    id: "html-3",
    language: "html",
    title: "یک بخش کوتاه دربارهٔ خودت",
    difficulty: "easy",
    topic: "متن",
    description:
      "یک h1، یک h2 و دو بند p بنویس — مثلاً دربارهٔ اینکه چرا برنامه‌نویسی یاد می‌گیری. لازم نیست طولانی باشد؛ مهم این است که ساختار عنوان و بند درست باشد.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "h1 برای موضوع اصلی صفحه است؛ h2 برای یک بخش زیر آن.",
      "هر ایدهٔ جدا را در p خودش بگذار؛ Enter خالی در ادیتور به‌تنهایی بند درست نمی‌سازد.",
      "اگر می‌خواهی یک کلمه مهم باشد، همان را داخل strong بگذار.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["متن و قالب‌بندی"],
  },
  {
    id: "html-4",
    language: "html",
    title: "فهرست کارها",
    difficulty: "easy",
    topic: "فهرست",
    description:
      "یک فهرست بدون شماره با سه کار واقعی که امروز می‌خواهی انجام بدهی بساز. از ul و li استفاده کن تا معنا «فهرست» باشد، نه فقط سه خط جدا.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "ul یعنی فهرست بدون شماره. هر مورد یک li است.",
      "سه کار واقعی بنویس تا تمرین برایت معنادار باشد، نه فقط «آیتم ۱».",
      "اگر در مرورگر گلوله ندیدی، ببین تگ‌ها را درست بسته‌ای یا نه.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["فهرست ها"],
  },
  {
    id: "html-5",
    language: "html",
    title: "لینک به بیرون و داخل",
    difficulty: "easy",
    topic: "لینک",
    description:
      "دو لینک بگذار: یکی به یک سایت واقعی (مثلاً example.com) و یکی به بخش پایین همین صفحه با #. برای بخش پایین یک id بگذار تا لینک جایی برای پریدن داشته باشد.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "برای لینک خارجی، آدرس کامل را در href بگذار و متن قابل‌کلیک را بین تگ a بنویس.",
      "برای پرش داخل صفحه، یک id روی مقصد بگذار و لینک را به #همان_id وصل کن.",
      "اگر لینک داخلی کار نکرد، املای id و href را حرف‌به‌حرف یکی کن.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["لینک ها"],
  },
  {
    id: "html-6",
    language: "html",
    title: "تصویر با توضیح",
    difficulty: "easy",
    topic: "تصویر",
    description:
      "یک تصویر با src فرضی (یا مسیر واقعی اگر داری) بگذار و حتماً alt معنی‌دار بنویس. alt برای وقتی است که تصویر لود نشود یا صفحه‌خوان بخواهد توضیح بدهد.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "src می‌گوید تصویر از کجا لود شود؛ alt می‌گوید اگر تصویر نبود چه توضیحی خوانده شود.",
      "alt را شبیه توضیح کوتاه برای یک دوست بنویس، نه کلمهٔ بی‌معنی.",
      "اگر مسیر تصویر واقعی نداری، همان ساختار درست را بنویس و alt را جدی بگیر.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["تصاویر"],
  },
  {
    id: "html-7",
    language: "html",
    title: "جدول دو نفره",
    difficulty: "easy",
    topic: "جدول",
    description:
      "یک جدول کوچک با ستون‌های «نام» و «شهر» بساز و دو ردیف داده برای دو نفر بنویس. سرستون‌ها را با th مشخص کن تا معلوم باشد عنوان‌اند نه دادهٔ معمولی.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "جدول را ردیف‌به‌ردیف فکر کن: هر tr یک ردیف است.",
      "ردیف اول را با th برای عنوان ستون‌ها بساز؛ ردیف‌های بعد td برای داده.",
      "قبل از پیچیده کردن، همان دو ستون و دو نفر را تمیز و کامل بنویس.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["جدول ها"],
  },
  {
    id: "html-8",
    language: "html",
    title: "فرم نام ساده",
    difficulty: "easy",
    topic: "فرم",
    description:
      "فرمی بساز که یک فیلد نام داشته باشد، label درست به آن وصل باشد، و دکمهٔ ارسال هم دیده شود. روی input حتماً name بگذار تا اگر فرم ارسال شد، داده اسم داشته باشد.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "label را با for به id همان input وصل کن تا کلیک روی متن هم فیلد را فعال کند.",
      "name روی input برای این است که داده در ارسال، اسم داشته باشد.",
      "دکمه را type=submit بگذار اگر می‌خواهی نقش «ارسال» داشته باشد.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["فرم ها"],
  },
  {
    id: "html-9",
    language: "html",
    title: "فرم تماس کوچیک",
    difficulty: "medium",
    topic: "فرم",
    description:
      "یک فرم تماس با سه بخش بساز: نام، ایمیل، و پیام چندخطی. دکمهٔ ارسال هم داشته باشد. لازم نیست واقعاً به سرور وصل شود؛ فقط ساختار درست و مرتب مهم است.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "سه فیلد را با label جدا و مرتب زیر هم بچین تا فرم شلوغ نشود.",
      "برای متن بلند از textarea استفاده کن؛ برای ایمیل type=email مناسب‌تر است.",
      "لازم نیست واقعاً جایی ارسال شود؛ تمرکز روی ساختار درست و قابل‌فهم است.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["فرم ها"],
  },
  {
    id: "html-10",
    language: "html",
    title: "صفحهٔ معرفی یک‌صفحه‌ای",
    difficulty: "medium",
    topic: "ترکیبی",
    description:
      "یک صفحهٔ خیلی کوتاه دربارهٔ خودت بساز: عنوان، دو بند، یک فهرست مهارت‌ها، و یک لینک به پروژه‌ای که دوست داری (حتی اگر هنوز نساختی). هدف این است که چیزهایی را که تا اینجای HTML خواندی کنار هم ببینی.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "اول اسکلت صفحه را درست کن، بعد محتوا را تکه‌تکه اضافه کن.",
      "فهرست مهارت‌ها را با ul بنویس و لینک را با a و href واقعی یا آزمایشی.",
      "در پایان صفحه را در مرورگر باز کن و از خودت بپرس: بدون توضیح اضافه، کسی می‌فهمد دربارهٔ چیست؟",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["متن", "فهرست ها", "لینک ها"],
  },
  {
    id: "css-1",
    language: "css",
    title: "خوانا کردن متن",
    difficulty: "easy",
    topic: "رنگ و متن",
    description:
      "برای بندهای صفحه یک رنگ متن تیره و یک فاصلهٔ خط راحت (مثلاً حدود ۱.۷) بگذار. هدف زیبایی شلوغ نیست؛ فقط خواندن آسان‌تر شود.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "یک قانون برای p بنویس و color را روی یک رنگ تیره بگذار تا روی پس‌زمینه خوانا باشد.",
      "line-height را کمی بیشتر از حالت پیش‌فرض بگذار تا خط‌ها به هم نچسبند.",
      "اگر فرقی ندیدی، ببین فایل CSS به HTML وصل شده یا انتخاب‌گر p درست است.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["رنگ ها", "متن"],
  },
  {
    id: "css-2",
    language: "css",
    title: "پس‌زمینهٔ ملایم",
    difficulty: "easy",
    topic: "پس‌زمینه",
    description:
      "برای body یک رنگ پس‌زمینهٔ خیلی ملایم انتخاب کن تا با متن تیره تضاد داشته باشد. اگر متن و پس‌زمینه هر دو خاکستری متوسط باشند، خواندن سخت می‌شود.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "background-color را روی body بگذار، نه فقط روی یک کلمه.",
      "رنگ خیلی تیره با متن تیره، یا خیلی روشن با متن روشن، چشم را خسته می‌کند.",
      "بعد از ذخیره، صفحه را رفرش کن؛ گاهی مرورگر نسخهٔ قبلی را نگه می‌دارد.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["پس زمینه"],
  },
  {
    id: "css-3",
    language: "css",
    title: "کارت با کلاس",
    difficulty: "easy",
    topic: "انتخاب‌گر و جعبه",
    description:
      "یک کلاس به نام card بساز که padding داخلی، لبهٔ نازک و گوشهٔ کمی گرد داشته باشد. بعد همان کلاس را روی یک جعبه در HTML بگذار تا اثرش را ببینی.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "در CSS بنویس .card { ... } — نقطه یعنی class.",
      'در HTML همان عنصر باید class="card" داشته باشد؛ اگر اسم‌ها یکی نباشند هیچ اتفاقی نمی‌افتد.',
      "padding نفس داخل کارت است؛ border لبه است؛ radius گوشه را نرم می‌کند.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["انتخاب گرها", "جعبه"],
  },
  {
    id: "css-4",
    language: "css",
    title: "لینک وقتی نشانگر روی آن است",
    difficulty: "easy",
    topic: "انتخاب‌گر",
    description:
      "برای لینک‌ها حالت hover بگذار؛ مثلاً رنگ عوض شود یا زیرخط پیدا کند. این بازخورد کوچک به کاربر می‌گوید «اینجا کلیک‌پذیر است».",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "a:hover فقط وقتی اعمال می‌شود که نشانگر روی لینک باشد.",
      "تغییر را کوچک و واضح نگه دار: رنگ یا زیرخط کافی است.",
      "اگر hover کار نکرد، اول ببین استایل a معمولی‌ات قوی‌تر نوشته نشده باشد.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["انتخاب گرها"],
  },
  {
    id: "css-5",
    language: "css",
    title: "سه جعبه در یک ردیف",
    difficulty: "easy",
    topic: "فلکس",
    description:
      "یک ظرف با display:flex بساز و سه فرزند کنار هم بگذار. بینشان فاصلهٔ یکنواخت با gap بده. یادت باشد flex را روی والد می‌گذاری، نه روی هر فرزند جداگانه برای این کار پایه.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "display: flex را روی ظرف والد بگذار؛ فرزندان خودشان ردیف می‌شوند.",
      "gap فاصلهٔ بین آیتم‌ها را بدون دردسر margin تکی مدیریت می‌کند.",
      "اگر زیر هم ماندند، ببین عرض صفحه خیلی کم نیست یا flex-direction عوض نشده باشد.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["فلکس"],
  },
  {
    id: "css-6",
    language: "css",
    title: "دکمهٔ مرتب",
    difficulty: "medium",
    topic: "جعبه و رنگ",
    description:
      "یک دکمه یا لینک شبیه دکمه طراحی کن: padding کافی، گوشه گرد، رنگ مشخص، و بدون ظاهر شلخته. اگر خواستی در hover کمی تغییرش بده تا زنده به نظر برسد.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "دکمه باید هم دیده شود هم کلیکش راحت باشد؛ padding را خیلی کم نگذار.",
      "یک رنگ پس‌زمینه و یک رنگ متن با تضاد خوب انتخاب کن.",
      "اگر خواستی، در :hover کمی روشن‌تر یا کمی برجسته‌ترش کن تا بازخورد داشته باشد.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["جعبه", "رنگ ها"],
  },
  {
    id: "css-7",
    language: "css",
    title: "صفحه با عرض محدود",
    difficulty: "medium",
    topic: "جعبه",
    description:
      "محتوای اصلی را طوری محدود کن که در صفحه‌های خیلی عریض کش نیاید (مثلاً max-width) و اگر ممکن است وسط بچین. خواندن خط‌های خیلی بلند سخت است.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "روی ظرف اصلی max-width بگذار تا در مانیتور عریض، خط‌ها بی‌نهایت طولانی نشوند.",
      "برای وسط آمدن افقی، گاهی margin-left و margin-right را auto می‌گذارند.",
      "اول روی دسکتاپ چک کن، بعد عرض پنجره را کم کن و ببین رفتار منطقی است یا نه.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["جعبه"],
  },
  {
    id: "css-8",
    language: "css",
    title: "از ردیف به ستون در عرض کم",
    difficulty: "hard",
    topic: "فلکس و واکنش‌گرا",
    description:
      "همان ردیف سه ستونه را طوری تنظیم کن که در عرض‌های کوچک‌تر (مثلاً زیر ۶۰۰ پیکسل) زیر هم قرار بگیرد. اگر media query را خوانده‌ای، اینجا جایش است.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "در حالت عادی می‌توانی flex را ردیفی نگه داری.",
      "داخل @media (max-width: 600px) بگو ستون شود: flex-direction: column.",
      "عرض پنجره را دستی کوچک کن و ببین آیا واقعاً از آن نقطه به بعد چیدمان عوض می‌شود.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["فلکس", "RWD"],
  },
  {
    id: "js-1",
    language: "javascript",
    title: "سلام در Console",
    difficulty: "easy",
    topic: "شروع",
    description:
      'در Console مرورگر یک پیام متنی چاپ کن. متن را داخل " (دابل‌کوتیشن) بگذار. این ساده‌ترین راه است تا مطمئن شوی کد جاوااسکریپت‌ات اجرا می‌شود.',
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "Console را باز کن (معمولاً F12) تا خروجی log را ببینی؛ این با متن وسط صفحه فرق دارد.",
      'بنویس console.log("سلام") و Enter بزن یا اسکریپت را در صفحه اجرا کن.',
      "اگر ReferenceError دیدی، املای console.log را چک کن.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["خروجی"],
  },
  {
    id: "js-2",
    language: "javascript",
    title: "متغیری که عوض می‌شود",
    difficulty: "easy",
    topic: "متغیر",
    description:
      "با let یک امتیاز از صفر بساز، بعد آن را زیاد کن و هر بار در Console ببین. می‌خواهم فرق متغیر ثابت‌مانده با متغیرِ در حال تغییر برایت روشن شود.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "let برای مقداری است که قرار است عوض شود.",
      "بعد از تغییر، دوباره console.log را صدا بزن تا مقدار جدید را ببینی.",
      "اگر اشتباهاً const گذاشتی و دوباره مقدار دادی، خطا طبیعی است؛ همان را با let درست کن.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["Let"],
  },
  {
    id: "js-3",
    language: "javascript",
    title: "مقایسهٔ سخت و سست",
    difficulty: "easy",
    topic: "عملگرها",
    description:
      'در Console این دو را جداگانه ببین: 5 === "5" و 5 == "5". نتیجه را نگاه کن و برای خودت یک جمله بنویس که چرا یکی‌شان ممکن است فریب‌ده باشد.',
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "هر دو عبارت را جدا log کن و خروجی True/False را کنار هم بگذار.",
      "=== سخت‌گیرتر است و برای کارهای روزمره انتخاب امن‌تری است.",
      "== ممکن است نوع را پنهانی عوض کند؛ برای همین گاهی نتیجه عجیب به نظر می‌رسد.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["مقایسه ها", "عملگرها"],
  },
  {
    id: "js-4",
    language: "javascript",
    title: "تصمیم ساده",
    difficulty: "easy",
    topic: "شرط",
    description:
      "یک عدد در متغیر بگذار. اگر بزرگ‌تر از صفر بود پیام «مثبت» وگرنه پیام دیگری چاپ کن. این همان if/else است که بعداً در دکمه‌ها و فرم‌ها هم می‌آید.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "شرط را داخل پرانتز if بگذار و بلوک را با { } مشخص کن.",
      "اگر فقط یک شاخه می‌نویسی هم اشکالی ندارد، ولی else کمک می‌کند حالت مخالف روشن باشد.",
      "قبل از پیچیده کردن، با یک عدد مثبت و یک عدد منفی یا صفر امتحان کن.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["شرط ها"],
  },
  {
    id: "js-5",
    language: "javascript",
    title: "عددهای ۱ تا ۵",
    difficulty: "easy",
    topic: "حلقه",
    description:
      "با یک حلقه، عددهای ۱ تا ۵ را در Console چاپ کن. هدف این است که تکرار را خودت دستی کپی نکنی.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "حلقه for سه قسمت دارد: شروع، شرط ادامه، و گام افزایش.",
      "از 1 تا 5 یعنی شرط را i <= 5 بگذار و هر دور i++.",
      "log را داخل حلقه بگذار تا هر عدد یک‌بار چاپ شود.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["حلقه for"],
  },
  {
    id: "js-6",
    language: "javascript",
    title: "اولین عضو آرایه",
    difficulty: "easy",
    topic: "آرایه",
    description:
      "یک آرایه از چند اسم بساز و فقط اسم اول را چاپ کن. یادت باشد شمارهٔ اولین خانه صفر است.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "آرایه را با [ ... ] بساز و عضو اول را با [0] بخوان.",
      "اگر undefined دیدی، یا آرایه خالی است یا ایندکس را اشتباه داده‌ای.",
      "یک‌بار هم length را log کن تا تعداد عضو را ببینی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["آرایه ها"],
  },
  {
    id: "js-7",
    language: "javascript",
    title: "اضافه کردن به آرایه",
    difficulty: "easy",
    topic: "آرایه",
    description:
      "یک آرایه بساز و با push یک عضو جدید به انتهایش اضافه کن. بعد length را هم چاپ کن تا ببینی تعداد عوض شده.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "push دقیقاً به ته آرایه اضافه می‌کند و خودِ آرایه را تغییر می‌دهد.",
      "بعد از push دوباره length را چاپ کن؛ باید یکی بیشتر شده باشد.",
      "اگر آرایه را const تعریف کرده‌ای، push معمولاً مجاز است چون خودِ جعبه عوض نشده، محتوا عوض شده.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["آرایه ها"],
  },
  {
    id: "js-8",
    language: "javascript",
    title: "دکمه حرف می‌زند",
    difficulty: "easy",
    topic: "DOM",
    description:
      "در صفحه یک دکمه با id مشخص بگذار. با جاوااسکریپت طوری بنویس که وقتی کلیک شد، متن دکمه عوض شود. اسکریپت را جایی بگذار که دکمه قبلش در صفحه وجود داشته باشد.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "اول در HTML به دکمه یک id بده تا با querySelector پیدا شود.",
      "اگر null گرفتی، یا id غلط است یا اسکریپت قبل از وجود دکمه اجرا شده.",
      "داخل تابع کلیک، textContent را عوض کن تا تغییر را روی خود دکمه ببینی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["رویدادها", "DOM"],
  },
  {
    id: "js-9",
    language: "javascript",
    title: "خواندن چیزی که کاربر نوشت",
    difficulty: "medium",
    topic: "DOM",
    description:
      "یک input و یک دکمه بگذار. با کلیک دکمه، متنی را که کاربر نوشته بخوان و در Console یا داخل یک عنصر صفحه نشان بده. اگر خالی بود، یک پیام مهربان بده که «اول چیزی بنویس».",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "مقدار تایپ‌شده در input.value است؛ آن را در یک متغیر بریز و همان را نشان بده.",
      "قبل از نمایش، خالی بودن را با if چک کن تا پیام واضح بدهی.",
      "value همیشه رشته است؛ اگر بعداً خواستی حساب کنی باید به عدد تبدیلش کنی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["DOM", "رویدادها"],
  },
  {
    id: "js-10",
    language: "javascript",
    title: "لیست پویا",
    difficulty: "medium",
    topic: "DOM و آرایه",
    description:
      "یک input و دکمه «افزودن» بساز. با هر بار کلیک، متن input به‌صورت یک آیتم جدید به یک فهرست در صفحه اضافه شود. این تمرین کوچک، همان الگوی خیلی از کارها و فروشگاه‌هاست.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "با هر کلیک یک li جدید بساز و متنش را از input بردار.",
      "li را به ul موجود در صفحه append کن تا در لیست دیده شود.",
      "اگر خواستی تجربه بهتر شود، بعد از افزودن مقدار input را خالی کن تا آمادهٔ مورد بعدی باشد.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["DOM", "آرایه ها"],
  },
  {
    id: "php-1",
    language: "php",
    title: "اولین echo",
    difficulty: "easy",
    topic: "شروع",
    description:
      'یک فایل PHP بنویس که با echo یک جملهٔ فارسی چاپ کند. متن را داخل " (دابل‌کوتیشن) بگذار و یادت باشد این کد روی سرور اجرا می‌شود، نه با دوبارکلیک ساده مثل یک صفحهٔ فقط‌HTML.',
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "فایل را با <?php شروع کن و دستور را با ; تمام کن.",
      'echo "سلام"; همان چیزی است که در خروجی صفحه می‌بینی.',
      "اگر فقط فایل را مثل HTML باز کردی و چیزی ندیدی، احتمالاً به اجرای سرور نیاز داری.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["مقدمه"],
  },
  {
    id: "php-2",
    language: "php",
    title: "متغیر با $",
    difficulty: "easy",
    topic: "متغیر",
    description:
      "نامی را در یک متغیر بگذار و همان را echo کن. در PHP نام متغیر با $ شروع می‌شود؛ اگر $ را فراموش کنی معمولاً به خطا می‌خوری.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      'اسم متغیر را با $ بنویس: $name = "سارا";',
      "برای چاپ همان مقدار، echo $name; کافی است.",
      "اگر $ را جا انداختی، PHP آن را مثل متغیر نمی‌فهمد و خطا یا رفتار عجیب می‌بینی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["متغیرها"],
  },
  {
    id: "php-3",
    language: "php",
    title: "چسباندن دو تکه متن",
    difficulty: "easy",
    topic: "رشته",
    description:
      "دو رشته بساز (مثلاً نام و نام‌خانوادگی) و با نقطه (.) به‌هم بچسبان و چاپ کن. در PHP برای چسباندن متن از + استفاده نکن؛ + برای عدد است.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "نقطه (.) دو رشته را به هم می‌چسباند.",
      'اگر بین نام و نام‌خانوادگی فاصله می‌خواهی، یک " " هم وسطشان بگذار.',
      "علامت + را برای متن در PHP استفاده نکن؛ برای عدد است.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["رشته ها"],
  },
  {
    id: "php-4",
    language: "php",
    title: "زوج یا فرد در PHP",
    difficulty: "easy",
    topic: "شرط",
    description:
      "یک عدد در متغیر بگذار و مثل قبل بگو زوج است یا فرد. منطق همان است؛ فقط نحو PHP را رعایت کن.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "منطق زوج/فرد مثل پایتون است: باقی‌مانده بر ۲.",
      "نحو PHP را رعایت کن: شرط داخل if () و بلوک داخل { }.",
      "با چند عدد مختلف امتحان کن تا هر دو شاخه را ببینی.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["شرط ها"],
  },
  {
    id: "php-5",
    language: "php",
    title: "آرایه و foreach",
    difficulty: "easy",
    topic: "آرایه",
    description:
      "یک آرایه از چند عدد یا نام بساز و با foreach هر عضو را چاپ کن. این روش برای وقتی که تعداد اعضا را از قبل دقیق نمی‌دانی خیلی راحت است.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "آرایه را با [1, 2, 3] بساز.",
      "foreach ($arr as $item) هر دور یک عضو در $item می‌گذارد.",
      "echo را داخل حلقه بگذار و اگر خواستی بعد از هر مورد یک فاصله یا خط جدید هم چاپ کن.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["آرایه ها"],
  },
  {
    id: "php-6",
    language: "php",
    title: "دفترچه با آرایهٔ انجمنی",
    difficulty: "easy",
    topic: "آرایه",
    description:
      'یک آرایه با کلیدهای name و city بساز و مقدار name را چاپ کن. کلید متنی را داخل " بگذار.',
    exampleInput: "",
    exampleOutput: "",
    hints: [
      'کلید متنی را با => به مقدار وصل کن: "name" => "سارا".',
      'برای خواندن بنویس $user["name"]؛ املای کلید مهم است.',
      "اگر کلید را اشتباه بنویسی ممکن است Notice ببینی؛ همان لحظه املا را درست کن.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["آرایه ها"],
  },
  {
    id: "php-7",
    language: "php",
    title: "خواندن امن از URL",
    difficulty: "medium",
    topic: "فرم و امنیت",
    description:
      "پارامتر q را از آدرس صفحه بخوان (مثلاً ?q=test). اگر نبود، رشتهٔ خالی در نظر بگیر. قبل از چاپ در HTML حتماً htmlspecialchars را استفاده کن تا ورودی خام، صفحه را خراب نکند.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      'مقدار را با $_GET["q"] ?? "" بخوان تا اگر نبود، خطا نگیری.',
      "قبل از echo داخل HTML از htmlspecialchars استفاده کن.",
      "عمداً یک‌بار ورودی عجیب مثل <b> را تست کن و ببین خروجی امن دیگر آن را اجرا نمی‌کند.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["GET", "فیلترها"],
  },
  {
    id: "php-8",
    language: "php",
    title: "فرم جستجوی خیلی کوچک",
    difficulty: "medium",
    topic: "فرم",
    description:
      "یک صفحه با فرم method=get و یک فیلد q بساز. وقتی کاربر چیزی نوشت و ارسال کرد، همان مقدار را پایین صفحه به‌صورت امن نشان بده. لازم نیست هنوز دیتابیس داشته باشی.",
    exampleInput: "",
    exampleOutput: "",
    hints: [
      "در فرم، method=get و name=q را درست بگذار تا مقدار در آدرس صفحه پیدا شود.",
      "همان صفحه می‌تواند فرم را نشان بدهد و پایین‌تر نتیجه را چاپ کند.",
      "نتیجه را خام چاپ نکن؛ همان عادت امن درس قبل را اینجا هم نگه دار.",
    ],
    solution: "",
    explanation: "",
    relatedLessons: ["فرم ها", "GET"],
  },
];
var QUIZ = {
  python: [
    {
      q: "خروجی این کد چیست؟",
      code: "print(2 ** 3)",
      opts: ["5", "6", "8", "9"],
      a: 2,
      e: "** توان است؛ ۲ به توان ۳ = ۸.",
    },
    {
      q: "کدام نام متغیر درست است؟",
      opts: ["1name", "my-name", "my_name", "class"],
      a: 2,
      e: "نام نباید با عدد شروع شود و خط تیره مجاز نیست.",
    },
    {
      q: "نوع خروجی input()؟",
      opts: ["int", "str", "bool", "list"],
      a: 1,
      e: "input همیشه رشته برمی‌گرداند.",
    },
    {
      q: "برای تساوی کدام درست است؟",
      opts: ["=", "==", "===", ":="],
      a: 1,
      e: "مقایسه با == انجام می‌شود.",
    },
    {
      q: "خروجی؟",
      code: "print([1,2,3][-1])",
      opts: ["1", "2", "3", "خطا"],
      a: 2,
      e: "ایندکس ۱- آخرین عضو است.",
    },
    {
      q: "range(3) چند دور؟",
      opts: ["2", "3", "4", "0"],
      a: 1,
      e: "۰ و ۱ و ۲ → سه دور.",
    },
    {
      q: "دیکشنری کدام است؟",
      opts: ["{1,2}", "[1,2]", "{'a':1}", "(1,2)"],
      a: 2,
      e: "کلید و مقدار داخل {}.",
    },
    {
      q: "تابع بدون return؟",
      opts: ["0", "False", "None", "خطا"],
      a: 2,
      e: "خروجی پیش‌فرض None است.",
    },
    {
      q: "مدیریت خطا؟",
      opts: ["if/else", "try/except", "for/while", "import"],
      a: 1,
      e: "try/except برای خطاست.",
    },
    {
      q: "خروجی؟",
      code: "print('A','B',sep='-')",
      opts: ["A B", "A-B", "AB", "خطا"],
      a: 1,
      e: "sep بین موارد می‌آید.",
    },
  ],
  html: [
    {
      q: "محتوای دیدنی صفحه کجاست؟",
      opts: ["head", "body", "meta", "title"],
      a: 1,
      e: "داخل body.",
    },
    {
      q: "تگ لینک؟",
      opts: ["link", "a", "href", "url"],
      a: 1,
      e: "تگ a با href.",
    },
    {
      q: "تگ تصویر؟",
      opts: ["img", "image", "pic", "src"],
      a: 0,
      e: "img و src.",
    },
    {
      q: "عنوان تب مرورگر؟",
      opts: ["h1", "title", "header", "name"],
      a: 1,
      e: "title در head.",
    },
    {
      q: "لیست شماره‌دار؟",
      opts: ["ul", "ol", "li", "dl"],
      a: 1,
      e: "ol شماره‌دار است.",
    },
    {
      q: "متن جایگزین تصویر؟",
      opts: ["title", "alt", "label", "name"],
      a: 1,
      e: "ویژگی alt.",
    },
    {
      q: "تگ فرم؟",
      opts: ["form", "input", "field", "submit"],
      a: 0,
      e: "form ظرف فیلدهاست.",
    },
    {
      q: "پاراگراف؟",
      opts: ["para", "p", "text", "paragraph"],
      a: 1,
      e: "تگ p.",
    },
  ],
  css: [
    {
      q: "انتخاب‌گر کلاس؟",
      opts: ["#box", ".box", "box", "*box"],
      a: 1,
      e: "نقطه = کلاس.",
    },
    {
      q: "رنگ متن؟",
      opts: ["background", "color", "font-color", "text"],
      a: 1,
      e: "ویژگی color.",
    },
    {
      q: "وسط‌چین متن؟",
      opts: [
        "align:center",
        "text-align:center",
        "margin:center",
        "float:center",
      ],
      a: 1,
      e: "text-align.",
    },
    {
      q: "فاصله داخل جعبه؟",
      opts: ["margin", "padding", "border", "gap"],
      a: 1,
      e: "padding داخلی است.",
    },
    {
      q: "flex برای؟",
      opts: ["انیمیشن", "چیدمان ردیف/ستون", "فونت", "سایه"],
      a: 1,
      e: "چیدمان یک‌بعدی.",
    },
    {
      q: "واحد وابسته به فونت؟",
      opts: ["px", "em", "vw", "cm"],
      a: 1,
      e: "em نسبت به فونت.",
    },
    {
      q: "پنهان با حفظ فضا؟",
      opts: ["display:none", "visibility:hidden", "حذف تگ", "float"],
      a: 1,
      e: "visibility:hidden.",
    },
    {
      q: "معمولاً اولویت بالاتر؟",
      opts: ["تگ", "کلاس", "id", "مرورگر"],
      a: 2,
      e: "id قوی‌تر است.",
    },
  ],
  javascript: [
    { q: "ثابت؟", opts: ["var", "let", "const", "static"], a: 2, e: "const." },
    { q: "مقایسه سخت؟", opts: ["=", "==", "===", "!="], a: 2, e: "===." },
    {
      q: "اضافه ته آرایه؟",
      opts: ["push", "pop", "shift", "slice"],
      a: 0,
      e: "push.",
    },
    {
      q: "گرفتن با id؟",
      opts: ["querySelectorAll", "getElementById", "createElement", "write"],
      a: 1,
      e: "getElementById.",
    },
    {
      q: "تابع پیکانی؟",
      opts: ["function=>{}", "()=>{}", "=>(){}", "var=>"],
      a: 1,
      e: "()=>{}",
    },
    {
      q: "JSON.parse؟",
      opts: ["شیء به رشته", "رشته به شیء", "مرتب‌سازی", "رویداد"],
      a: 1,
      e: "رشته JSON به مقدار.",
    },
    { q: "کدام falsy؟", opts: ["'0'", "[]", "0", "{}"], a: 2, e: "عدد صفر." },
    {
      q: "setTimeout؟",
      opts: ["حلقه ابدی", "اجرای تأخیری", "سرور", "CSS"],
      a: 1,
      e: "یک‌بار با تأخیر.",
    },
  ],
  php: [
    {
      q: "شروع کد PHP؟",
      opts: ["<?php", "<php>", "<?=php", "<!php>"],
      a: 0,
      e: "<?php",
    },
    { q: "شروع متغیر؟", opts: ["@", "$", "#", "%"], a: 1, e: "با $." },
    {
      q: "چاپ رایج؟",
      opts: ["console.log", "print_r", "echo", "alert"],
      a: 2,
      e: "echo.",
    },
    {
      q: "آرایه کلیدی؟",
      opts: ["list", "associative", "split", "object"],
      a: 1,
      e: "آرایه انجمنی.",
    },
    {
      q: "اتصال دیتابیس؟",
      opts: ["fetch", "PDO/mysqli", "json_encode", "session"],
      a: 1,
      e: "PDO یا mysqli.",
    },
    {
      q: "$_GET از؟",
      opts: ["POST body", "URL", "cookie", "file"],
      a: 1,
      e: "پارامتر URL.",
    },
    {
      q: "session؟",
      opts: ["استایل", "داده کاربر در سرور", "فشرده‌سازی", "DNS"],
      a: 1,
      e: "وضعیت بین درخواست‌ها.",
    },
    {
      q: "== در PHP؟",
      opts: ["فقط نوع", "مقدار با تبدیل نوع", "مرجع", "همیشه false"],
      a: 1,
      e: "با تبدیل نوع.",
    },
  ],
};

(function () {
  var EX_LANGS = [
    { id: "python", name: "Python", fa: "پایتون", icon: "🐍" },
    { id: "html", name: "HTML", fa: "اچ‌تی‌ام‌ال", icon: "📄" },
    { id: "css", name: "CSS", fa: "سی‌اس‌اس", icon: "🎨" },
    { id: "javascript", name: "JavaScript", fa: "جاوااسکریپت", icon: "⚡" },
    { id: "php", name: "PHP", fa: "پی‌اچ‌پی", icon: "🐘" },
  ];
  var LEVEL_FA = {
    easy: "آسان",
    medium: "متوسط",
    hard: "سخت",
    challenge: "چالشی",
  };
  var currentExLang = null;

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function showView(id) {
    ["exLangSelect", "exListView", "exDetailView", "quizArea"].forEach(
      function (x) {
        var el = document.getElementById(x);
        if (el) el.style.display = "none";
      },
    );
    var el = document.getElementById(id);
    if (el) el.style.display = "block";
  }

  function renderExLangButtons() {
    var container = document.getElementById("tamrinLangs");
    if (!container) return;
    container.innerHTML = "";
    EX_LANGS.forEach(function (L) {
      var count = EXERCISES.filter(function (e) {
        return e.language === L.id;
      }).length;
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "lang";
      btn.innerHTML =
        '<span class="ic">' +
        L.icon +
        "</span><b>" +
        L.name +
        "</b><small>" +
        L.fa +
        " · " +
        count +
        " تمرین</small>";
      btn.onclick = function () {
        openExList(L.id);
      };
      container.appendChild(btn);
    });
  }

  function openExList(langId) {
    currentExLang = langId;
    var langInfo = EX_LANGS.find(function (L) {
      return L.id === langId;
    });
    showView("exListView");
    document.getElementById("exListTitle").textContent =
      "تمرین‌های " + (langInfo ? langInfo.fa : langId);
    var topics = {};
    EXERCISES.filter(function (e) {
      return e.language === langId;
    }).forEach(function (e) {
      topics[e.topic] = true;
    });
    var topicSelect = document.getElementById("exFilterTopic");
    topicSelect.innerHTML = '<option value="all">همه موضوعات</option>';
    Object.keys(topics)
      .sort()
      .forEach(function (t) {
        var opt = document.createElement("option");
        opt.value = t;
        opt.textContent = t;
        topicSelect.appendChild(opt);
      });
    document.getElementById("exFilterLevel").value = "all";
    document.getElementById("exSearch").value = "";
    renderExList();
  }

  function renderExList() {
    var level = document.getElementById("exFilterLevel").value;
    var topic = document.getElementById("exFilterTopic").value;
    var q = (document.getElementById("exSearch").value || "")
      .trim()
      .toLowerCase();
    var list = EXERCISES.filter(function (e) {
      if (e.language !== currentExLang) return false;
      if (level !== "all" && e.difficulty !== level) return false;
      if (topic !== "all" && e.topic !== topic) return false;
      if (q) {
        var hay = (e.title + " " + e.topic + " " + e.description).toLowerCase();
        if (hay.indexOf(q) === -1) return false;
      }
      return true;
    });
    var root = document.getElementById("exListRoot");
    root.innerHTML = "";
    if (list.length === 0) {
      root.innerHTML =
        '<div class="ex-empty">تمرینی با این فیلتر پیدا نشد.</div>';
      return;
    }
    list.forEach(function (ex) {
      var div = document.createElement("div");
      div.className = "ex-item";
      div.innerHTML =
        "<h3>" +
        escapeHtml(ex.title) +
        "</h3>" +
        '<div class="ex-meta">' +
        '<span class="ex-badge ' +
        ex.difficulty +
        '">' +
        (LEVEL_FA[ex.difficulty] || ex.difficulty) +
        "</span><span>" +
        escapeHtml(ex.topic) +
        "</span></div>";
      div.onclick = function () {
        openExDetail(ex.id);
      };
      root.appendChild(div);
    });
  }

  function openExDetail(exId) {
    var ex = EXERCISES.find(function (e) {
      return e.id === exId;
    });
    if (!ex) return;
    showView("exDetailView");
    var html = "<h2>" + escapeHtml(ex.title) + "</h2>";
    html +=
      '<div class="ex-meta" style="margin-bottom:14px">' +
      '<span class="ex-badge ' +
      ex.difficulty +
      '">' +
      (LEVEL_FA[ex.difficulty] || ex.difficulty) +
      "</span><span>موضوع: " +
      escapeHtml(ex.topic) +
      "</span></div>";
    html +=
      '<div class="ex-section"><h3>توضیح مسئله</h3>' +
      '<p style="color:#b1bac4;line-height:1.9">' +
      escapeHtml(ex.description) +
      "</p></div>";
    if (ex.exampleInput || ex.exampleOutput) {
      html += '<div class="ex-section"><h3>نمونه ورودی و خروجی</h3>';
      if (ex.exampleInput) {
        html +=
          '<p style="color:#8b949e;font-size:13px;margin-bottom:4px">ورودی:</p>' +
          '<div class="ex-io">' +
          escapeHtml(ex.exampleInput) +
          "</div>";
      }
      if (ex.exampleOutput) {
        html +=
          '<p style="color:#8b949e;font-size:13px;margin:10px 0 4px">خروجی:</p>' +
          '<div class="ex-io">' +
          escapeHtml(ex.exampleOutput) +
          "</div>";
      }
      html += "</div>";
    }
    if (ex.hints && ex.hints.length) {
      html += '<div class="ex-section"><h3>راهنمای حل (مرحله‌به‌مرحله)</h3>';
      ex.hints.forEach(function (h, i) {
        html +=
          '<div class="ex-hint"><strong>راهنمای ' +
          (i + 1) +
          ":</strong> " +
          escapeHtml(h) +
          "</div>";
      });
      html += "</div>";
    }
    html +=
      '<div class="ex-section"><h3>پاسخ</h3>' +
      '<div class="note">پاسخ آماده نشان داده نمی‌شود. با راهنما و درس‌های مرتبط خودت حل کن.</div></div>';
    if (ex.relatedLessons && ex.relatedLessons.length) {
      html +=
        '<div class="ex-section"><h3>درس‌های مرتبط</h3><p class="rel">' +
        escapeHtml(ex.relatedLessons.join(" · ")) +
        "</p></div>";
    }
    document.getElementById("exDetailCard").innerHTML = html;
  }

  function startQuiz(key) {
    var list = QUIZ[key] || [];
    var root = document.getElementById("quizRoot");
    var score = document.getElementById("scoreBox");
    showView("quizArea");
    root.innerHTML = "";
    var ok = 0;
    var total = list.length;
    function upd() {
      score.innerHTML =
        'نتیجه: <b style="color:#58a6ff">' +
        ok +
        "</b> از <b>" +
        total +
        "</b>";
    }
    upd();
    list.forEach(function (item, qi) {
      var art = document.createElement("article");
      art.className = "qcard";
      var h = document.createElement("h3");
      h.textContent = qi + 1 + ". " + item.q;
      art.appendChild(h);
      if (item.code) {
        var c = document.createElement("div");
        c.className = "qcode";
        c.textContent = item.code;
        art.appendChild(c);
      }
      var fb = document.createElement("p");
      fb.className = "qfb";
      fb.textContent = item.e;
      item.opts.forEach(function (opt, oi) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "qopt";
        b.textContent = opt;
        b.onclick = function () {
          if (art.getAttribute("data-done")) return;
          art.setAttribute("data-done", "1");
          art.querySelectorAll(".qopt").forEach(function (x, xi) {
            x.disabled = true;
            if (xi === item.a) x.classList.add("ok");
          });
          if (oi === item.a) {
            b.classList.add("ok");
            ok++;
          } else {
            b.classList.add("bad");
          }
          fb.classList.add("on");
          upd();
        };
        art.appendChild(b);
      });
      art.appendChild(fb);
      root.appendChild(art);
    });
  }

  function bind() {
    renderExLangButtons();
    var backLang = document.getElementById("backToExLangs");
    if (backLang) {
      backLang.onclick = function () {
        showView("exLangSelect");
      };
    }
    var backList = document.getElementById("backToExList");
    if (backList) {
      backList.onclick = function () {
        showView("exListView");
        renderExList();
      };
    }
    var fl = document.getElementById("exFilterLevel");
    var ft = document.getElementById("exFilterTopic");
    var fs = document.getElementById("exSearch");
    if (fl) fl.onchange = renderExList;
    if (ft) ft.onchange = renderExList;
    if (fs) fs.oninput = renderExList;
    var btnQuiz = document.getElementById("btnShowQuiz");
    if (btnQuiz) {
      btnQuiz.onclick = function () {
        var choice = prompt(
          "کدام زبان؟\npython / html / css / javascript / php",
          "python",
        );
        if (!choice) return;
        choice = choice.trim().toLowerCase();
        if (QUIZ[choice]) startQuiz(choice);
        else alert("زبان پشتیبانی‌شده نیست.");
      };
    }
    var backQ = document.getElementById("backTamrin");
    if (backQ) {
      backQ.onclick = function () {
        showView("exLangSelect");
      };
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
})();

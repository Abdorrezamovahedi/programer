# -*- coding: utf-8 -*-
import json, re, html as htmlmod

src = open("/workspace/artifacts/madrase-complete.html", encoding="utf-8").read()
m = re.search(r"const LESSONS = (\{.*\});\nlet currentLang", src, re.S)
data = json.loads(m.group(1))

def lesson(title, what, where, code, lines):
    exp = "<br>\n".join(lines)
    h = (
        f"<h2>{htmlmod.escape(title)}</h2>\n"
        f"<p><strong>{what}</strong></p>\n"
        f"<p><strong>کجا به درد می‌خورد؟</strong> {where}</p>\n"
        f"<p>مثال:</p>\n"
        f'<div class="code">{htmlmod.escape(code)}</div>\n'
        f'<div class="exp">\n{exp}\n</div>'
    )
    return {"t": title, "h": h}

# Full PHP curriculum titles from user (order preserved)
TITLES = """
خانه (HOME)
مقدمه (Intro)
نصب (Install)
سینتکس (Syntax)
توضیحات (Comments)
توضیحات چندخطی (Multiline Comments)
متغیرها (Variables)
دامنه متغیرها (Variables Scope)
اکو/پرینت (Echo / Print)
نوع داده ها (Data Types)
رشته ها (Strings)
ویرایش رشته ها (Modify Strings)
چسباندن رشته ها (Concatenate Strings)
برش رشته ها (Slicing Strings)
کاراکترهای اِسکیپ (Escape Characters)
اعداد (Numbers)
تبدیل نوع (Casting)
ریاضی (Math)
ثابت ها (Constants)
ثابت های جادویی (Magic Constants)
عملگرها (Operators)
If/Else/Elseif (If...Else...Elseif)
عملگرهای If (If Operators)
If...Else (If...Else)
If کوتاه (Shorthand if)
If تو در تو (Nested if)
سوئیچ (Switch)
حلقه ها (Loops)
حلقه while (While Loop)
حلقه do...while (Do While Loop)
حلقه for (For Loop)
حلقه foreach (Foreach Loop)
شکستن حلقه (Break)
ادامه حلقه (Continue)
توابع (Functions)
آرایه ها (Arrays)
آرایه های اندیسی (Indexed Arrays)
آرایه های انجمنی (Associative Arrays)
ساخت آرایه ها (Create Arrays)
دسترسی به آیتم ها (Access Array Items)
به روزرسانی آیتم ها (Update Array Items)
افزودن آیتم ها (Add Array Items)
حذف آیتم ها (Remove Array Items)
مرتب سازی آرایه ها (Sorting Arrays)
آرایه های چندبعدی (Multidimensional Arrays)
توابع آرایه (Array Functions)
سوپرگلوبال ها (Superglobals)
$GLOBALS ($GLOBALS)
$_SERVER ($_SERVER)
$_REQUEST ($_REQUEST)
$_POST ($_POST)
$_GET ($_GET)
عبارات منظم (RegEx)
مدیریت فرم (Form Handling)
اعتبارسنجی فرم (Form Validation)
فیلدهای اجباری فرم (Form Required)
اعتبارسنجی URL/ایمیل (Form URL/E-mail)
فرم کامل (Form Complete)
تاریخ و زمان (Date and Time)
اینکلود (Include)
مدیریت فایل (File Handling)
باز/خواندن فایل (File Open/Read)
ایجاد/نوشتن فایل (File Create/Write)
آپلود فایل (File Upload)
کوکی ها (Cookies)
سشن ها (Sessions)
فیلترها (Filters)
فیلترهای پیشرفته (Filters Advanced)
توابع کال بک (Callback Functions)
JSON (JSON)
استثناها (Exceptions)
OOP چیست؟ (What is OOP)
کلاس ها/اشیا (Classes/Objects)
سازنده (Constructor)
مخرب (Destructor)
سطوح دسترسی (Access Modifiers)
وراثت (Inheritance)
ثابت ها در کلاس (Class Constants)
کلاس های انتزاعی (Abstract Classes)
اینترفیس ها (Interfaces)
تِرِیت ها (Traits)
متدهای استاتیک (Static Methods)
خواص استاتیک (Static Properties)
فضاهای نام (Namespaces)
قابل تکرارها (Iterables)
معرفی MySQL (MySQL Database)
اتصال به MySQL (MySQL Connect)
ایجاد پایگاه داده (MySQL Create DB)
ایجاد جدول (MySQL Create Table)
درج داده (MySQL Insert Data)
گرفتن آخرین ID (MySQL Get Last ID)
درج چندتایی (MySQL Insert Multiple)
دستورات آماده (MySQL Prepared)
انتخاب داده (MySQL Select Data)
شرط Where (MySQL Where)
مرتب سازی (MySQL Order By)
حذف داده (MySQL Delete Data)
به روزرسانی داده (MySQL Update Data)
محدودیت نتایج (MySQL Limit Data)
تجزیه گرهای XML (XML Parsers)
سیمپل XML: خواندن (SimpleXML Parser)
سیمپل XML: دریافت (SimpleXML-Get)
XML اکسپت (XML Expat)
DOM در PHP (XML DOM)
مقدمه AJAX (AJAX Intro)
AJAX با PHP (AJAX PHP)
AJAX و پایگاه داده (AJAX Database)
AJAX و XML (AJAX XML)
جستجوی زنده AJAX (AJAX Live Search)
نظرسنجی AJAX (AJAX Poll)
نمونه ها (Examples)
کامپایلر (Compiler)
آزمون (Quiz)
تمرین ها (Exercises)
سرور (Server)
سیلابس (Syllabus)
برنامه مطالعه (Study Plan)
گواهینامه (Certificate)
نمای کلی PHP (Overview)
مرجع آرایه (PHP Array)
تابع array() (array())
تغییر کوچکی/بزرگی کلیدها (array_change_key_case)
تکه تکه کردن آرایه (array_chunk)
ستون برداری آرایه (array_column)
ترکیب آرایه ها (array_combine)
شمارش مقادیر (array_count_values)
تفاضل آرایه (array_diff)
تفاضل انجمنی (array_diff_assoc)
تفاضل بر اساس کلید (array_diff_key)
تفاضل انجمنی کاربری (array_diff_uassoc)
تفاضل کلید کاربری (array_diff_ukey)
پُرکردن آرایه (array_fill)
پرکردن کلیدها (array_fill_keys)
فیلترکردن آرایه (array_filter)
برعکس کردن کلید/مقدار (array_flip)
اشتراک آرایه (array_intersect)
اشتراک انجمنی (array_intersect_assoc)
اشتراک بر اساس کلید (array_intersect_key)
اشتراک انجمنی کاربری (array_intersect_uassoc)
اشتراک کلید کاربری (array_intersect_ukey)
وجود کلید (array_key_exists)
کلیدها (array_keys)
نگاشت (array_map)
ادغام (array_merge)
ادغام بازگشتی (array_merge_recursive)
مرتب سازی چندگانه (array_multisort)
پَدکردن آرایه (array_pad)
پاپ (array_pop)
حاصل ضرب مقادیر (array_product)
پوش (array_push)
تصادفی گرفتن (array_rand)
کاهش (array_reduce)
جایگزینی (array_replace)
جایگزینی بازگشتی (array_replace_recursive)
برعکس کردن (array_reverse)
جستجو (array_search)
شیفت (array_shift)
اسلایس (array_slice)
برش و جایگزینی (array_splice)
جمع (array_sum)
تفاضل کاربری (array_udiff)
تفاضل کاربری انجمنی (array_udiff_assoc)
تفاضل کاربری انجمنی+کلید (array_udiff_uassoc)
اشتراک کاربری (array_uintersect)
اشتراک کاربری انجمنی (array_uintersect_assoc)
اشتراک کاربری انجمنی+کلید (array_uintersect_uassoc)
یکتا کردن (array_unique)
آن شیفت (array_unshift)
مقادیر (array_values)
پیاده روی در آرایه (array_walk)
پیاده روی بازگشتی (array_walk_recursive)
مرتب سازی نزولی انجمنی (arsort)
مرتب سازی انجمنی (asort)
فشرده سازی (compact)
شمارش (count)
عنصر جاری (current)
each (each)
پایان (end)
استخراج (extract)
وجود در آرایه (in_array)
کلید فعلی (key)
مرتب سازی نزولی بر اساس کلید (krsort)
مرتب سازی بر اساس کلید (ksort)
فهرست سازی (list)
مرتب سازی طبیعی بدون حساسیت (natcasesort)
مرتب سازی طبیعی (natsort)
بعدی (next)
pos (pos)
قبلی (prev)
بازه (range)
ریست (reset)
مرتب سازی نزولی (rsort)
درهم ریزی (shuffle)
اندازه (sizeof)
مرتب سازی (sort)
uasort (uasort)
uksort (uksort)
usort (usort)
مرجع تقویم (PHP Calendar)
تعداد روزهای ماه (cal_days_in_month)
تبدیل از ژولیَن (cal_from_jd)
اطلاعات تقویم (cal_info)
تبدیل به ژولیَن (cal_to_jd)
تاریخ عید پاک (easter_date)
روزهای عید پاک (easter_days)
فرانسوی به JD (frenchtojd)
گرگوری به JD (gregoriantojd)
روز هفته JD (jddayofweek)
نام ماه JD (jdmonthname)
JD به فرانسوی (jdtofrench)
JD به گرگوری (jdtogregorian)
JD به یهودی (jdtojewish)
JD به ژولین (jdtojulian)
JD به یونیکس (jdtounix)
یهودی به JD (jewishtojd)
ژولین به JD (juliantojd)
یونیکس به JD (unixtojd)
مرجع تاریخ (PHP Date)
checkdate() (checkdate)
افزودن تاریخ (date_add)
ایجاد از فرمت (date_create_from_format)
ایجاد تاریخ (date_create)
تنظیم تاریخ (date_date_set)
گرفتن منطقه پیش فرض (date_default_timezone_get)
تنظیم منطقه پیش فرض (date_default_timezone_set)
اختلاف تاریخ (date_diff)
فرمت تاریخ (date_format)
آخرین خطاهای تاریخ (date_get_last_errors)
ایجاد فاصله از رشته (date_interval_create_from_date_string)
فرمت فاصله (date_interval_format)
تنظیم ISO تاریخ (date_isodate_set)
تغییر تاریخ (date_modify)
گرفتن آفست (date_offset_get)
تحلیل از فرمت (date_parse_from_format)
تحلیل تاریخ (date_parse)
کاهش تاریخ (date_sub)
اطلاعات خورشید (date_sun_info)
طلوع خورشید (date_sunrise)
غروب خورشید (date_sunset)
تنظیم زمان (date_time_set)
گرفتن timestamp (date_timestamp_get)
تنظیم timestamp (date_timestamp_set)
گرفتن منطقه زمانی (date_timezone_get)
تنظیم منطقه زمانی (date_timezone_set)
تابع date() (date)
getdate() (getdate)
gettimeofday() (gettimeofday)
gmdate() (gmdate)
gmmktime() (gmmktime)
gmstrftime() (gmstrftime)
idate() (idate)
localtime() (localtime)
microtime() (microtime)
mktime() (mktime)
strftime() (strftime)
strptime() (strptime)
strtotime() (strtotime)
time() (time)
فهرست اختصارات منطقه (timezone_abbreviations_list)
فهرست شناسه های منطقه (timezone_identifiers_list)
مختصات منطقه (timezone_location_get)
نام منطقه از اختصار (timezone_name_from_abbr)
گرفتن نام منطقه (timezone_name_get)
گرفتن آفست منطقه (timezone_offset_get)
بازکردن منطقه (timezone_open)
گذارهای منطقه (timezone_transitions_get)
نسخه منطقه زمانی (timezone_version_get)
مرجع دایرکتوری (PHP Directory)
chdir() (chdir)
chroot() (chroot)
closedir() (closedir)
dir() (dir)
getcwd() (getcwd)
opendir() (opendir)
readdir() (readdir)
rewinddir() (rewinddir)
scandir() (scandir)
مرجع خطا (PHP Error)
ردیابی پشته (debug_backtrace)
چاپ ردیابی پشته (debug_print_backtrace)
آخرین خطا (error_get_last)
ثبت خطا (error_log)
گزارش خطا (error_reporting)
بازگردانی هندلر خطا (restore_error_handler)
بازگردانی هندلر استثنا (restore_exception_handler)
تنظیم هندلر خطا (set_error_handler)
تنظیم هندلر استثنا (set_exception_handler)
ایجاد خطا (trigger_error)
مرجع استثنا (PHP Exception)
کلاس Exception (Exception)
گرفتن کد (getCode)
گرفتن فایل (getFile)
گرفتن پیام (getMessage)
گرفتن خط (getLine)
گرفتن قبلی (getPrevious)
گرفتن Trace (getTrace)
Trace به رشته (getTraceAsString)
مرجع فایل سیستم (PHP Filesystem)
basename() (basename)
chgrp() (chgrp)
chmod() (chmod)
chown() (chown)
پاک سازی کش آمار (clearstatcache)
کپی (copy)
حذف (delete)
dirname() (dirname)
فضای آزاد دیسک (disk_free_space)
کل فضای دیسک (disk_total_space)
diskfreespace() (diskfreespace)
fclose() (fclose)
feof() (feof)
fflush() (fflush)
fgetc() (fgetc)
fgetcsv() (fgetcsv)
fgets() (fgets)
fgetss() (fgetss)
file() (file)
file_exists() (file_exists)
file_get_contents() (file_get_contents)
file_put_contents() (file_put_contents)
fileatime() (fileatime)
filectime() (filectime)
filegroup() (filegroup)
fileinode() (fileinode)
filemtime() (filemtime)
fileowner() (fileowner)
fileperms() (fileperms)
filesize() (filesize)
filetype() (filetype)
flock() (flock)
fnmatch() (fnmatch)
fopen() (fopen)
fpassthru() (fpassthru)
fputcsv() (fputcsv)
fputs() (fputs)
fread() (fread)
fscanf() (fscanf)
fseek() (fseek)
fstat() (fstat)
ftell() (ftell)
ftruncate() (ftruncate)
fwrite() (fwrite)
glob() (glob)
is_dir() (is_dir)
is_executable() (is_executable)
is_file() (is_file)
is_link() (is_link)
is_readable() (is_readable)
is_uploaded_file() (is_uploaded_file)
is_writable() (is_writable)
is_writeable() (is_writeable)
lchgrp() (lchgrp)
lchown() (lchown)
link() (link)
linkinfo() (linkinfo)
lstat() (lstat)
mkdir() (mkdir)
انتقال فایل آپلودی (move_uploaded_file)
خواندن INI فایل (parse_ini_file)
خواندن INI رشته (parse_ini_string)
pathinfo() (pathinfo)
pclose() (pclose)
popen() (popen)
readfile() (readfile)
readlink() (readlink)
realpath() (realpath)
گرفتن کش realpath (realpath_cache_get)
اندازه کش realpath (realpath_cache_size)
rename() (rename)
rewind() (rewind)
rmdir() (rmdir)
set_file_buffer() (set_file_buffer)
stat() (stat)
symlink() (symlink)
tempnam() (tempnam)
tmpfile() (tmpfile)
touch() (touch)
umask() (umask)
unlink() (unlink)
مرجع فیلتر (PHP Filter)
وجود متغیر (filter_has_var)
شناسه فیلتر (filter_id)
ورودی فیلتر (filter_input)
آرایه ورودی فیلتر (filter_input_array)
فهرست فیلترها (filter_list)
فیلتر کردن مقدار (filter_var)
آرایه مقدارها (filter_var_array)
مرجع FTP (PHP FTP)
ftp_alloc (ftp_alloc)
ftp_cdup (ftp_cdup)
ftp_chdir (ftp_chdir)
ftp_chmod (ftp_chmod)
ftp_close (ftp_close)
ftp_connect (ftp_connect)
ftp_delete (ftp_delete)
ftp_exec (ftp_exec)
ftp_fget (ftp_fget)
ftp_fput (ftp_fput)
ftp_get (ftp_get)
ftp_get_option (ftp_get_option)
ftp_login (ftp_login)
ftp_mdtm (ftp_mdtm)
ftp_mkdir (ftp_mkdir)
ftp_mlsd (ftp_mlsd)
ftp_nb_continue (ftp_nb_continue)
ftp_nb_fget (ftp_nb_fget)
ftp_nb_fput (ftp_nb_fput)
ftp_nb_get (ftp_nb_get)
ftp_nb_put (ftp_nb_put)
ftp_nlist (ftp_nlist)
ftp_pasv (ftp_pasv)
ftp_put (ftp_put)
ftp_pwd (ftp_pwd)
ftp_quit (ftp_quit)
ftp_raw (ftp_raw)
ftp_rawlist (ftp_rawlist)
ftp_rename (ftp_rename)
حذف پوشه روی FTP (ftp_rmdir)
تنظیم گزینه FTP (ftp_set_option)
اجرای دستور site روی FTP (ftp_site)
دریافت اندازه فایل FTP (ftp_size)
اتصال امن FTP/SSL (ftp_ssl_connect)
نوع سیستم سرور FTP (ftp_systype)
تبدیل JSON به آرایه/آبجکت (json_decode)
تبدیل آرایه/آبجکت به JSON (json_encode)
انتزاعی (abstract)
و (and)
به عنوان (as)
شکست/خروج از حلقه (break)
قابل فراخوانی (callable)
حالت (case)
گرفتن (catch)
کلاس (class)
کلون/کپی (clone)
ثابت (const)
ادامه (continue)
اعلامیه (declare)
پیش فرض (default)
do (do)
اکو/چاپ (echo)
در غیر این صورت (else)
در غیر این صورت اگر (elseif)
خالی (empty)
پایان declare (enddeclare)
پایان for (endfor)
پایان foreach (endforeach)
پایان if (endif)
پایان switch (endswitch)
پایان while (endwhile)
گسترش می دهد/ارث بری (extends)
نهایی (final)
در نهایت (finally)
تابع پیکانی (fn)
برای (for)
foreach (foreach)
تابع (function)
سراسری (global)
اگر (if)
پیاده سازی می کند (implements)
include (include)
include_once (include_once)
نمونه ای از (instanceof)
به جایِ (insteadof)
رابط (interface)
تنظیم شده/مقداردهی شده (isset)
لیست (list)
فضای نام (namespace)
جدید (new)
یا (or)
پرینت (print)
خصوصی (private)
محافظت شده (protected)
عمومی (public)
require (require)
require_once (require_once)
بازگشت (return)
ایستا (static)
switch (switch)
پرتاب/پرتاب استثنا (throw)
ویژگی (trait)
try (try)
use (use)
var (var)
while (while)
xor (xor)
yield (yield)
yield from (yield from)
پاک کردن خطاهای libxml (libxml_clear_errors)
غیرفعال کردن entity loader (libxml_disable_entity_loader)
دریافت همه خطاهای libxml (libxml_get_errors)
آخرین خطای libxml (libxml_get_last_error)
تنظیم loader موجودیت خارجی (libxml_set_external_entity_loader)
تنظیم context استریم ها (libxml_set_streams_context)
استفاده از خطاهای داخلی (libxml_use_internal_errors)
هش ezmlm (ezmlm_hash)
ارسال ایمیل (mail)
قدرمطلق (abs)
آرک کسینوس (acos)
آرک کسینوس هیپربولیک (acosh)
آرک سینوس (asin)
آرک سینوس هیپربولیک (asinh)
آرک تانژانت (atan)
آرک تانژانت2 (atan2)
آرک تانژانت هیپربولیک (atanh)
تبدیل مبنا (base_convert)
دودویی به ده دهی (bindec)
سقف (ceil)
کسینوس (cos)
کسینوس هیپربولیک (cosh)
ده دهی به دودویی (decbin)
ده دهی به هگز (dechex)
ده دهی به اکتال (decoct)
درجه به رادیان (deg2rad)
exp (exp)
expm1 (expm1)
کف (floor)
باقیمانده اعشاری (fmod)
حداکثر rand (getrandmax)
هگز به ده دهی (hexdec)
وتر/هیپوتنوس (hypot)
تقسیم صحیح (intdiv)
متناهی است؟ (is_finite)
بی نهایت است؟ (is_infinite)
NaN است؟ (is_nan)
مقدار LCG (lcg_value)
لگاریتم طبیعی (log)
لگاریتم پایه 10 (log10)
log1p (log1p)
بیشینه (max)
کمینه (min)
mt_getrandmax (mt_getrandmax)
mt_rand (mt_rand)
mt_srand (mt_srand)
اکتال به ده دهی (octdec)
عدد π (pi)
توان (pow)
رادیان به درجه (rad2deg)
rand (rand)
گرد کردن (round)
سینوس (sin)
سینوس هیپربولیک (sinh)
ریشه دوم (sqrt)
srand (srand)
تانژانت (tan)
تانژانت هیپربولیک (tanh)
اتصال قطع شده؟ (connection_aborted)
وضعیت اتصال (connection_status)
مهلت اتصال (connection_timeout)
مقدار ثابت (constant)
تعریف ثابت (define)
تعریف شده؟ (defined)
die (die)
eval (eval)
exit (exit)
اطلاعات مرورگر (get_browser)
توقف کامپایلر (__halt_compiler)
هایلایت فایل (highlight_file)
هایلایت رشته (highlight_string)
زمانِ با دقت نانو (hrtime)
نادیده گرفتن قطع کاربر (ignore_user_abort)
بسته بندی باینری (pack)
حذف فضاهای سفید کد PHP (php_strip_whitespace)
نمایش منبع (show_source)
خواب (sleep)
میانگین بار سیستم (sys_getloadavg)
nanosleep (time_nanosleep)
خواب تا زمان مشخص (time_sleep_until)
شناسه یکتا (uniqid)
بازکردن بسته های باینری (unpack)
usleep (usleep)
تعداد ردیف های متاثر (affected_rows)
خودکار-کامیت (autocommit)
تعویض کاربر (change_user)
نام مجموعه کاراکتر (character_set_name)
بستن اتصال (close)
کامیت (commit)
اتصال (connect)
کد خطای اتصال (connect_errno)
متن خطای اتصال (connect_error)
جابجایی مکان نما (data_seek)
دیباگ (debug)
dump_debug_info (dump_debug_info)
errno (errno)
error (error)
فهرست خطاها (error_list)
fetch_all (fetch_all)
fetch_array (fetch_array)
fetch_assoc (fetch_assoc)
fetch_field (fetch_field)
fetch_field_direct (fetch_field_direct)
fetch_fields (fetch_fields)
fetch_lengths (fetch_lengths)
fetch_object (fetch_object)
fetch_row (fetch_row)
تعداد فیلدها (field_count)
جستجوی فیلد (field_seek)
get_charset (get_charset)
get_client_info (get_client_info)
get_client_stats (get_client_stats)
get_client_version (get_client_version)
آمار اتصال (get_connection_stats)
اطلاعات میزبان (get_host_info)
نسخه پروتکل (get_proto_info)
اطلاعات سرور (get_server_info)
نسخه سرور (get_server_version)
info (info)
init (init)
insert_id (insert_id)
kill (kill)
more_results (more_results)
multi_query (multi_query)
next_result (next_result)
options (options)
ping (ping)
poll (poll)
prepare (prepare)
query (query)
real_connect (real_connect)
real_escape_string (real_escape_string)
real_query (real_query)
reap_async_query (reap_async_query)
refresh (refresh)
rollback (rollback)
انتخاب دیتابیس (select_db)
set_charset (set_charset)
set_local_infile_handler (set_local_infile_handler)
sqlstate (sqlstate)
ssl_set (ssl_set)
stat (mysqli_stat)
stmt_init (stmt_init)
thread_id (thread_id)
thread_safe (thread_safe)
use_result (use_result)
شمارش هشدار (warning_count)
بررسی DNS (checkdnsrr)
بستن syslog (closelog)
dns_check_record (dns_check_record)
dns_get_mx (dns_get_mx)
dns_get_record (dns_get_record)
بازکردن سوکت اینترنتی (fsockopen)
gethostbyaddr (gethostbyaddr)
gethostbyname (gethostbyname)
gethostbynamel (gethostbynamel)
gethostname (gethostname)
getmxrr (getmxrr)
getprotobyname (getprotobyname)
getprotobynumber (getprotobynumber)
getservbyname (getservbyname)
getservbyport (getservbyport)
ثبت کال بک هدر (header_register_callback)
حذف هدر (header_remove)
ارسال هدر (header)
فهرست هدرها (headers_list)
آیا هدرها ارسال شده اند؟ (headers_sent)
کد پاسخ HTTP (http_response_code)
تبدیل آدرس IP به رشته (inet_ntop)
تبدیل رشته به آدرس IP (inet_pton)
ip2long (ip2long)
long2ip (long2ip)
بازکردن syslog (openlog)
pfsockopen (pfsockopen)
setcookie (setcookie)
setrawcookie (setrawcookie)
وضعیت سوکت (socket_get_status)
بلاک کردن سوکت (socket_set_blocking)
مهلت سوکت (socket_set_timeout)
syslog (syslog)
flush (flush)
ob_clean (ob_clean)
ob_end_clean (ob_end_clean)
ob_end_flush (ob_end_flush)
ob_flush (ob_flush)
ob_get_clean (ob_get_clean)
ob_get_contents (ob_get_contents)
ob_get_flush (ob_get_flush)
ob_get_length (ob_get_length)
ob_get_level (ob_get_level)
ob_gzhandler (ob_gzhandler)
ob_implicit_flush (ob_implicit_flush)
ob_list_handlers (ob_list_handlers)
ob_start (ob_start)
output_add_rewrite_var (output_add_rewrite_var)
output_reset_rewrite_vars (output_reset_rewrite_vars)
فیلتر با الگو (preg_filter)
جستجو با الگو (preg_grep)
آخرین خطای PCRE (preg_last_error)
تطبیق (preg_match)
تطبیق همه (preg_match_all)
جایگزینی (preg_replace)
جایگزینی با کال بک (preg_replace_callback)
جایگزینی با آرایه کال بک ها (preg_replace_callback_array)
برش با الگو (preg_split)
escape الگو (preg_quote)
سازنده SimpleXML (__construct)
به رشته ( __tostring )
افزودن ویژگی (addAttribute)
افزودن فرزند (addChild)
خروجی XML (asXML)
attributes (attributes)
children (children)
count (SimpleXML count)
فضای نام ها (getDocNamespaces)
نام عنصر (getName)
دریافت namespaceها (getNamespaces)
ثبت نام فضا برای XPath (registerXPathNamespace)
ذخیره XML (saveXML)
import از DOM (simplexml_import_dom)
لود از فایل (simplexml_load_file)
لود از رشته (simplexml_load_string)
XPath (xpath)
current (SimpleXML current)
getchildren (getChildren)
haschildren (hasChildren)
key (SimpleXML key)
next (SimpleXML next)
rewind (SimpleXML rewind)
valid (SimpleXML valid)
استریم (PHP Stream)
addcslashes (addcslashes)
addslashes (addslashes)
bin2hex (bin2hex)
chop (chop)
chr (chr)
chunk_split (chunk_split)
convert_cyr_string (convert_cyr_string)
convert_uudecode (convert_uudecode)
convert_uuencode (convert_uuencode)
count_chars (count_chars)
crc32 (crc32)
crypt (crypt)
echo رشته (echo string)
explode (explode)
fprintf (fprintf)
get_html_translation_table (get_html_translation_table)
hebrev (hebrev)
hebrevc (hebrevc)
hex2bin (hex2bin)
html_entity_decode (html_entity_decode)
htmlentities (htmlentities)
htmlspecialchars_decode (htmlspecialchars_decode)
htmlspecialchars (htmlspecialchars)
implode (implode)
join (join)
lcfirst (lcfirst)
levenshtein (levenshtein)
localeconv (localeconv)
ltrim (ltrim)
md5 (md5)
md5_file (md5_file)
metaphone (metaphone)
money_format (money_format)
nl_langinfo (nl_langinfo)
nl2br (nl2br)
number_format (number_format)
ord (ord)
parse_str (parse_str)
print (print)
printf (printf)
quoted_printable_decode (quoted_printable_decode)
quoted_printable_encode (quoted_printable_encode)
quotemeta (quotemeta)
rtrim (rtrim)
setlocale (setlocale)
sha1 (sha1)
sha1_file (sha1_file)
similar_text (similar_text)
soundex (soundex)
sprintf (sprintf)
sscanf (sscanf)
str_getcsv (str_getcsv)
str_ireplace (str_ireplace)
str_pad (str_pad)
str_repeat (str_repeat)
str_replace (str_replace)
str_rot13 (str_rot13)
str_shuffle (str_shuffle)
str_split (str_split)
str_word_count (str_word_count)
strcasecmp (strcasecmp)
strchr (strchr)
strcmp (strcmp)
strcoll (strcoll)
strcspn (strcspn)
strip_tags (strip_tags)
stripcslashes (stripcslashes)
stripslashes (stripslashes)
stripos (stripos)
stristr (stristr)
strlen (strlen)
strnatcasecmp (strnatcasecmp)
strnatcmp (strnatcmp)
strncasecmp (strncasecmp)
strncmp (strncmp)
strpbrk (strpbrk)
strpos (strpos)
strrchr (strrchr)
strrev (strrev)
strripos (strripos)
strrpos (strrpos)
strspn (strspn)
strstr (strstr)
strtok (strtok)
strtolower (strtolower)
strtoupper (strtoupper)
strtr (strtr)
substr (substr)
substr_compare (substr_compare)
substr_count (substr_count)
substr_replace (substr_replace)
trim (trim)
ucfirst (ucfirst)
ucwords (ucwords)
vfprintf (vfprintf)
vprintf (vprintf)
vsprintf (vsprintf)
wordwrap (wordwrap)
boolval (boolval)
debug_zval_dump (debug_zval_dump)
doubleval (doubleval)
is_countable (is_countable)
empty (empty)
floatval (floatval)
get_defined_vars (get_defined_vars)
get_resource_type (get_resource_type)
gettype (gettype)
intval (intval)
is_array (is_array)
is_bool (is_bool)
is_callable (is_callable)
is_double (is_double)
is_float (is_float)
is_int (is_int)
is_integer (is_integer)
is_iterable (is_iterable)
is_long (is_long)
is_null (is_null)
is_numeric (is_numeric)
is_object (is_object)
is_real (is_real)
is_resource (is_resource)
is_scalar (is_scalar)
is_string (is_string)
isset (isset)
print_r (print_r)
serialize (serialize)
settype (settype)
strval (strval)
unserialize (unserialize)
unset (unset)
var_dump (var_dump)
var_export (var_export)
utf8_decode (utf8_decode)
utf8_encode (utf8_encode)
رشته خطای XML (xml_error_string)
بایت اندیس جاری (xml_get_current_byte_index)
شماره ستون جاری (xml_get_current_column_number)
شماره خط جاری (xml_get_current_line_number)
کد خطا (xml_get_error_code)
parse (xml_parse)
parse به ساختار (xml_parse_into_struct)
ساخت parser با namespace (xml_parser_create_ns)
ساخت parser (xml_parser_create)
آزادسازی parser (xml_parser_free)
گرفتن گزینه parser (xml_parser_get_option)
تنظیم گزینه parser (xml_parser_set_option)
handler داده کاراکتری (xml_set_character_data_handler)
handler پیش فرض (xml_set_default_handler)
handler عنصر (xml_set_element_handler)
پایان namespace decl handler (xml_set_end_namespace_decl_handler)
external entity ref handler (xml_set_external_entity_ref_handler)
notation decl handler (xml_set_notation_decl_handler)
set_object (xml_set_object)
processing instruction handler (xml_set_processing_instruction_handler)
شروع namespace decl handler (xml_set_start_namespace_decl_handler)
unparsed entity decl handler (xml_set_unparsed_entity_decl_handler)
بستن zip (zip_close)
بستن مدخل zip (zip_entry_close)
اندازه فشرده مدخل (zip_entry_compressedsize)
روش فشرده سازی مدخل (zip_entry_compressionmethod)
اندازه فایل مدخل (zip_entry_filesize)
نام مدخل (zip_entry_name)
بازکردن مدخل (zip_entry_open)
خواندن مدخل (zip_entry_read)
بازکردن فایل zip (zip_open)
خواندن zip (zip_read)
مناطق زمانی PHP (PHP Timezones)
""".strip().split("\n")
TITLES = [t.strip() for t in TITLES if t.strip()]

# Detailed core lessons
CORE = {}

def add(title, what, where, code, lines):
    CORE[title] = (what, where, code, lines)

add("خانه (HOME)",
    "صفحه خانه PHP نقطه شروع یادگیری زبان سمت سرور است.",
    "هر دوره یک صفحه شروع دارد تا بدانی از کجا شروع کنی.",
    '<?php\necho "به آموزش PHP خوش آمدید";\n?>',
    ["خط ۱: شروع بلوک PHP.", "خط ۲: متن را به مرورگر می‌فرستد.", "خط ۳: پایان بلوک PHP."])

add("مقدمه (Intro)",
    "PHP زبانی است که روی سرور اجرا می‌شود و بعد نتیجه را (معمولاً HTML) برای مرورگر می‌فرستد.",
    "سایت پویا، فرم، ورود کاربر، فروشگاه، پنل مدیریت.",
    '<?php\necho "سلام از سرور";\necho 2 + 3;\n?>',
    ["echo متن را چاپ می‌کند.", "می‌توانی عدد هم حساب کنی و چاپ کنی.", "کاربر فقط نتیجه را می‌بیند نه کد PHP را."])

add("نصب (Install)",
    "برای اجرای PHP به یک سرور محلی مثل XAMPP یا PHP داخلی نیاز داری.",
    "بدون محیط اجرا، فایل .php مثل HTML باز نمی‌شود.",
    '# در ترمینال:\nphp -v\nphp -S localhost:8000',
    ["php -v نسخه را نشان می‌دهد.", "php -S یک سرور کوچک برای تمرین راه می‌اندازد.", "فایل را در مرورگر با آدرس localhost باز کن نه با دوبار کلیک."])

add("سینتکس (Syntax)",
    "کد PHP بین <?php و ?> نوشته می‌شود. دستورها با ; تمام می‌شوند.",
    "بدون نقطه‌ویرگول یا تگ درست، صفحه خطا می‌دهد.",
    '<?php\n$x = 5;\necho $x;\n?>',
    ["<?php شروع کد است.", "$x متغیر است.", "echo مقدار را چاپ می‌کند.", "?> پایان است (در فایل خالص PHP گاهی لازم نیست)."])

add("توضیحات (Comments)",
    "کامنت متنی است که PHP اجرا نمی‌کند و فقط برای انسان است.",
    "یادداشت برای خودت و دیگران.",
    '<?php\n// یک خط\n# هم یک خط\necho "اجرا می‌شود";\n?>',
    ["// کامنت یک‌خطی.", "# هم کامنت یک‌خطی است.", "echo اجرا می‌شود."])

add("توضیحات چندخطی (Multiline Comments)",
    "کامنت چندخطی بین /* و */ است.",
    "توضیح یک تکه کد طولانی.",
    '<?php\n/*\nاین چند خط\nاجرا نمی‌شود\n*/\necho "بعد از کامنت";\n?>',
    ["/* شروع کامنت.", "وسط نادیده گرفته می‌شود.", "*/ پایان.", "echo اجرا می‌شود."])

add("متغیرها (Variables)",
    "متغیر جعبه‌ای با اسم است که با $ شروع می‌شود.",
    "نام کاربر، قیمت، نتیجه فرم.",
    '<?php\n$name = "سارا";\n$age = 18;\necho $name;\n$age = 19;\necho $age;\n?>',
    ["$name متن سارا را نگه می‌دارد.", "$age عدد ۱۸ است.", "echo محتویات را چاپ می‌کند.", "می‌توانی مقدار را عوض کنی."])

add("دامنه متغیرها (Variables Scope)",
    "متغیر بیرون تابع سراسری است؛ داخل تابع محلی است مگر global بنویسی.",
    "تنظیمات مشترک یا جلوگیری از تداخل نام.",
    '<?php\n$x = 10;\nfunction show() {\n  global $x;\n  echo $x;\n}\nshow();\n?>',
    ["$x بیرون تابع است.", "بدون global داخل تابع دیده نمی‌شود.", "global $x آن را داخل تابع قابل استفاده می‌کند.", "show آن را چاپ می‌کند."])

add("اکو/پرینت (Echo / Print)",
    "echo و print خروجی را به مرورگر می‌فرستند. echo کمی رایج‌تر است.",
    "نمایش پیام، HTML، مقدار متغیر.",
    '<?php\necho "سلام ";\nprint "دنیا";\necho 10, " ", 20;\n?>',
    ["echo متن چاپ می‌کند.", "print هم همین کار را می‌کند و مقدار برمی‌گرداند.", "echo می‌تواند چند مقدار با کاما بگیرد."])

add("نوع داده ها (Data Types)",
    "نوع می‌گوید مقدار عدد است یا متن یا آرایه یا شیء.",
    "جلوگیری از خطا وقتی نوع اشتباه باشد.",
    '<?php\nvar_dump(10);\nvar_dump(3.14);\nvar_dump("سلام");\nvar_dump(true);\nvar_dump([1,2]);\n?>',
    ["int عدد صحیح.", "float اعشار.", "string متن.", "bool درست/غلط.", "array لیست."])

add("رشته ها (Strings)",
    "رشته یعنی متن بین ' یا \".",
    "نام، پیام، HTML خروجی.",
    '<?php\n$s = "PHP";\necho strlen($s);\necho $s[0];\n?>',
    ["$s متن PHP است.", "strlen تعداد نویسه‌ها.", "$s[0] اولین نویسه (در رشته بایت‌محور دقت کن)."])

add("ویرایش رشته ها (Modify Strings)",
    "توابعی مثل strtoupper و trim متن را عوض می‌کنند (معمولاً نسخه جدید برمی‌گردانند).",
    "تمیز کردن ورودی کاربر.",
    '<?php\necho strtoupper("php");\necho strtolower("PHP");\necho trim("  hi  ");\n?>',
    ["حروف بزرگ.", "حروف کوچک.", "فاصله اول و آخر حذف می‌شود."])

add("چسباندن رشته ها (Concatenate Strings)",
    "با نقطه . دو متن به هم می‌چسبند.",
    "ساخت جمله از چند تکه.",
    '<?php\n$name = "علی";\necho "سلام " . $name;\necho $name . " عزیز";\n?>',
    [". یعنی بچسبان.", "اول سلام بعد اسم.", "می‌توانی چند بار پشت هم بچسبانی."])

add("برش رشته ها (Slicing Strings)",
    "substr بخشی از متن را برمی‌دارد.",
    "کد ملی بخشی، پسوند فایل، خلاصه خبر.",
    '<?php\n$s = "HelloWorld";\necho substr($s, 0, 5);\necho substr($s, 5);\n?>',
    ["از ایندکس ۰ به طول ۵ → Hello.", "از ایندکس ۵ تا آخر → World."])

add("کاراکترهای اِسکیپ (Escape Characters)",
    "با \\ می‌توانی نویسه خاص مثل خط جدید یا خود گیومه را بنویسی.",
    "متن چندخطی و نقل‌قول داخل نقل‌قول.",
    '<?php\necho "خط اول\\nخط دوم";\necho "او گفت: \\"سلام\\"";\n?>',
    ["\\n خط جدید.", "\\\" گیومه داخل رشته دوتایی."])

add("اعداد (Numbers)",
    "int صحیح و float اعشار. PHP خودش نوع را تشخیص می‌دهد.",
    "قیمت، تعداد، محاسبه.",
    '<?php\n$a = 10;\n$b = 3.5;\necho $a + $b;\necho $a ** 2;\n?>',
    ["جمع عدد صحیح و اعشار.", "** توان است."])

add("تبدیل نوع (Casting)",
    "با (int) یا intval مقدار را به نوع دیگر تبدیل می‌کنی.",
    "ورودی فرم همیشه متن است؛ برای حساب باید عدد شود.",
    '<?php\n$s = "25";\n$n = (int)$s;\necho $n + 5;\necho (string)100;\n?>',
    ["متن ۲۵ به عدد.", "حالا جمع کار می‌کند.", "عدد را به متن تبدیل می‌کند."])

add("ریاضی (Math)",
    "توابع مثل round و sqrt و max برای محاسبه.",
    "قیمت، امتیاز، آمار ساده.",
    '<?php\necho round(3.6);\necho sqrt(16);\necho max(1, 9, 4);\n?>',
    ["گرد کردن.", "ریشه دوم.", "بزرگ‌ترین عدد."])

add("ثابت ها (Constants)",
    "ثابت مقداری است که عوض نمی‌شود. با define یا const.",
    "نسخه برنامه، نرخ ثابت، نام سایت.",
    '<?php\ndefine("SITE", "مدرسه");\nconst YEAR = 2026;\necho SITE;\necho YEAR;\n?>',
    ["define ثابت سراسری می‌سازد.", "const هم ثابت می‌سازد.", "بدون $ استفاده می‌شود."])

add("ثابت های جادویی (Magic Constants)",
    "ثابت‌هایی که PHP خودش پر می‌کند مثل __FILE__ و __LINE__.",
    "لاگ و دیباگ.",
    '<?php\necho __FILE__;\necho __LINE__;\necho __DIR__;\n?>',
    ["مسیر همین فایل.", "شماره همین خط.", "پوشه همین فایل."])

add("عملگرها (Operators)",
    "علامت‌هایی برای حساب، مقایسه و منطق.",
    "هر شرط و محاسبه.",
    '<?php\necho 10 + 3;\necho 10 === "10" ? "برابر سخت" : "نه";\necho true && false;\n?>',
    ["جمع.", "=== نوع و مقدار را با هم چک می‌کند.", "&& یعنی و."])

add("If/Else/Elseif (If...Else...Elseif)",
    "چند مسیر تصمیم: اگر، وگرنه اگر، وگرنه.",
    "نمره، سطح دسترسی، وضعیت سفارش.",
    '<?php\n$score = 14;\nif ($score >= 17) {\n  echo "عالی";\n} elseif ($score >= 10) {\n  echo "قبول";\n} else {\n  echo "مردود";\n}\n?>',
    ["شرط اول عالی.", "اگر نه، قبول.", "اگر هیچ‌کدام، مردود."])

add("عملگرهای If (If Operators)",
    "در شرط از == === > < && || استفاده می‌کنی.",
    "ترکیب چند شرط.",
    '<?php\n$age = 20;\nif ($age >= 18 && $age < 60) {\n  echo "بزرگسال";\n}\n?>',
    ["هر دو شرط باید درست باشند."])

add("If...Else (If...Else)",
    "دو راه: شرط درست یا غلط.",
    "ورود مجاز / غیرمجاز.",
    '<?php\n$ok = true;\nif ($ok) {\n  echo "بله";\n} else {\n  echo "خیر";\n}\n?>',
    ["اگر $ok درست باشد بله.", "وگرنه خیر."])

add("If کوتاه (Shorthand if)",
    "عملگر سه تایی ?: یا ?? برای مقدار پیش‌فرض.",
    "مقدار کوتاه بدون چند خط if.",
    '<?php\n$age = 20;\necho $age >= 18 ? "بالغ" : "نوجوان";\n$name = $_GET["n"] ?? "مهمان";\n?>',
    ["اگر شرط درست، بالغ وگرنه نوجوان.", "?? اگر مقدار نبود مهمان."])

add("If تو در تو (Nested if)",
    "if داخل if دیگر.",
    "چند لایه بررسی (مثلاً ورود و بعد نقش).",
    '<?php\nif ($logged) {\n  if ($admin) {\n    echo "پنل";\n  }\n}\n?>',
    ["اول باید وارد شده باشد.", "بعد اگر ادمین بود پنل."])

add("سوئیچ (Switch)",
    "چند حالت مشخص روی یک مقدار.",
    "منو، وضعیت سفارش.",
    '<?php\n$d = 2;\nswitch ($d) {\n  case 1: echo "شنبه"; break;\n  case 2: echo "یکشنبه"; break;\n  default: echo "دیگر";\n}\n?>',
    ["مقدار با caseها مقایسه می‌شود.", "break جلوی ادامه را می‌گیرد.", "default اگر هیچ‌کدام نبود."])

add("حلقه ها (Loops)",
    "تکرار کار بدون کپی کد.",
    "لیست محصولات، ردیف جدول.",
    '<?php\nfor ($i = 0; $i < 3; $i++) {\n  echo $i;\n}\n?>',
    ["از ۰ تا قبل از ۳ تکرار."])

add("حلقه while (While Loop)",
    "تا وقتی شرط درست است تکرار می‌کند.",
    "خواندن فایل تا پایان.",
    '<?php\n$i = 0;\nwhile ($i < 3) {\n  echo $i;\n  $i++;\n}\n?>',
    ["شرط را چک کن.", "بدنه را اجرا کن.", "$i را زیاد کن وگرنه حلقه تمام نمی‌شود."])

add("حلقه do...while (Do While Loop)",
    "حداقل یک‌بار اجرا می‌شود بعد شرط را چک می‌کند.",
    "وقتی باید حداقل یک دور انجام شود.",
    '<?php\n$i = 0;\ndo {\n  echo $i;\n  $i++;\n} while ($i < 3);\n?>',
    ["اول بدنه، بعد شرط."])

add("حلقه for (For Loop)",
    "شمارنده، شرط، افزایش در یک خط.",
    "تکرار با تعداد مشخص.",
    '<?php\nfor ($i = 1; $i <= 3; $i++) {\n  echo $i;\n}\n?>',
    ["شروع از ۱.", "تا وقتی ≤ ۳.", "هر دور یکی زیاد."])

add("حلقه foreach (Foreach Loop)",
    "روی هر عضو آرایه می‌چرخد.",
    "لیست محصولات، نتایج دیتابیس.",
    '<?php\n$a = ["سیب", "گلابی"];\nforeach ($a as $item) {\n  echo $item;\n}\n?>',
    ["هر دور $item یک میوه است."])

add("شکستن حلقه (Break)",
    "از حلقه یا switch خارج می‌شود.",
    "پیدا کردن اولین نتیجه و توقف.",
    '<?php\nfor ($i = 0; $i < 10; $i++) {\n  if ($i === 3) break;\n  echo $i;\n}\n?>',
    ["وقتی i برابر ۳ شد خارج شو. چاپ: ۰۱۲۰۱۲... ۰ ۱ ۲"])

add("ادامه حلقه (Continue)",
    "این دور را رد کن و دور بعد را شروع کن.",
    "رد کردن بعضی ردیف‌ها.",
    '<?php\nfor ($i = 0; $i < 5; $i++) {\n  if ($i === 2) continue;\n  echo $i;\n}\n?>',
    ["۲ چاپ نمی‌شود."])

add("توابع (Functions)",
    "تکه کد با اسم که چند بار صدا زده می‌شود.",
    "اعتبارسنجی، فرمت قیمت، کارهای تکراری.",
    '<?php\nfunction greet($name = "مهمان") {\n  return "سلام " . $name;\n}\necho greet("سارا");\n?>',
    ["function تعریف می‌کند.", "return نتیجه را برمی‌گرداند.", "مقدار پیش‌فرض اگر آرگومان ندهی."])

add("آرایه ها (Arrays)",
    "چند مقدار در یک متغیر.",
    "لیست، جدول، نتیجه کوئری.",
    '<?php\n$a = [10, 20, 30];\necho $a[0];\n?>',
    ["ایندکس از ۰ شروع می‌شود."])

add("آرایه های اندیسی (Indexed Arrays)",
    "کلیدها عدد هستند: ۰، ۱، ۲.",
    "لیست ساده.",
    '<?php\n$c = ["قرمز", "آبی"];\necho $c[1];\n?>',
    ["عضو شماره ۱ آبی است."])

add("آرایه های انجمنی (Associative Arrays)",
    "کلید متن است مثل name.",
    "یک کاربر یا یک ردیف جدول.",
    '<?php\n$u = ["name" => "مینا", "age" => 22];\necho $u["name"];\n?>',
    ["=> کلید را به مقدار وصل می‌کند."])

add("ساخت آرایه ها (Create Arrays)",
    "با [] یا array().",
    "هر لیستی.",
    '<?php\n$a = array(1, 2);\n$b = [3, 4];\n?>',
    ["هر دو درست است. [] کوتاه‌تر و رایج‌تر است."])

add("دسترسی به آیتم ها (Access Array Items)",
    "با [کلید] می‌خوانی.",
    "نمایش یک فیلد.",
    '<?php\n$a = ["x" => 5];\necho $a["x"];\necho $a["z"] ?? "نیست";\n?>',
    ["خواندن کلید x.", "اگر کلید نبود مقدار پیش‌فرض."])

add("به روزرسانی آیتم ها (Update Array Items)",
    "با همان کلید مقدار جدید می‌گذاری.",
    "ویرایش پروفایل.",
    '<?php\n$a = ["n" => "علی"];\n$a["n"] = "رضا";\necho $a["n"];\n?>',
    ["مقدار n عوض می‌شود."])

add("افزودن آیتم ها (Add Array Items)",
    "[] خالی به انتها اضافه می‌کند یا کلید جدید می‌سازی.",
    "افزودن به سبد.",
    '<?php\n$a = [1];\n$a[] = 2;\n$a["k"] = 3;\nprint_r($a);\n?>',
    ["[] یعنی بعدی را بچسبان.", "کلید k را هم می‌توانی بگذاری."])

add("حذف آیتم ها (Remove Array Items)",
    "unset یک کلید را پاک می‌کند. array_splice هم می‌تواند.",
    "حذف از سبد.",
    '<?php\n$a = [1, 2, 3];\nunset($a[1]);\nprint_r($a);\n?>',
    ["عضو ایندکس ۱ حذف می‌شود. ایندکس‌ها ممکن است جا خالی بماند."])

add("مرتب سازی آرایه ها (Sorting Arrays)",
    "sort مقدار را، ksort کلید را مرتب می‌کند.",
    "لیست الفبایی یا قیمت.",
    '<?php\n$a = [3, 1, 2];\nsort($a);\nprint_r($a);\n?>',
    ["بعد از sort: 1 2 3. خود آرایه عوض می‌شود."])

add("آرایه های چندبعدی (Multidimensional Arrays)",
    "آرایه داخل آرایه؛ مثل جدول.",
    "لیست کاربران که هر کدام چند فیلد دارند.",
    '<?php\n$users = [\n  ["name" => "علی", "age" => 20],\n  ["name" => "سارا", "age" => 22],\n];\necho $users[0]["name"];\n?>',
    ["اولین کاربر، فیلد name."])

add("توابع آرایه (Array Functions)",
    "توابع آماده مثل count و in_array و array_merge.",
    "تقریباً هر کار روی لیست.",
    '<?php\n$a = [1, 2, 2];\necho count($a);\necho in_array(2, $a) ? "هست" : "نیست";\n?>',
    ["تعداد اعضا.", "آیا ۲ داخل لیست است."])

add("سوپرگلوبال ها (Superglobals)",
    "آرایه‌های آماده PHP که همه‌جا در دسترس‌اند: $_GET $_POST $_SERVER ...",
    "فرم، اطلاعات سرور، سشن.",
    '<?php\necho $_SERVER["REQUEST_METHOD"];\n?>',
    ["نشان می‌دهد درخواست GET است یا POST."])

add("$GLOBALS ($GLOBALS)",
    "آرایه همه متغیرهای سراسری.",
    "دسترسی به متغیر سراسری از داخل تابع بدون global.",
    '<?php\n$x = 5;\nfunction f() {\n  echo $GLOBALS["x"];\n}\nf();\n?>',
    ["$GLOBALS['x'] همان $x سراسری است."])

add("$_SERVER ($_SERVER)",
    "اطلاعات سرور و درخواست: آدرس، مرورگر، روش.",
    "لاگ، مسیر، تشخیص HTTPS.",
    '<?php\necho $_SERVER["HTTP_HOST"] ?? "";\necho $_SERVER["SCRIPT_NAME"] ?? "";\n?>',
    ["دامنه.", "مسیر اسکریپت."])

add("$_REQUEST ($_REQUEST)",
    "ترکیبی از GET و POST و COOKIE (بسته به تنظیم).",
    "وقتی منبع داده مهم نیست؛ ولی برای امنیت بهتر است GET/POST جدا.",
    '<?php\necho $_REQUEST["q"] ?? "";\n?>',
    ["اگر q در فرم یا آدرس باشد چاپ می‌شود."])

add("$_POST ($_POST)",
    "داده‌های فرم با method=post.",
    "ورود، ثبت‌نام، تماس. در آدرس دیده نمی‌شود.",
    '<?php\n$n = $_POST["name"] ?? "";\necho htmlspecialchars($n);\n?>',
    ["اگر name نبود رشته خالی.", "htmlspecialchars جلوی تزریق HTML را می‌گیرد."])

add("$_GET ($_GET)",
    "داده‌های داخل آدرس ?id=1.",
    "جستجو، صفحه، لینک اشتراک.",
    '<?php\n$id = $_GET["id"] ?? "0";\necho htmlspecialchars($id);\n?>',
    ["id از آدرس خوانده می‌شود.", "همیشه خروجی را امن چاپ کن."])

add("عبارات منظم (RegEx)",
    "الگوی جستجو در متن با preg_match.",
    "چک ایمیل، فقط عدد، استخراج کد.",
    '<?php\nif (preg_match("/^\\\\d+$/", "123")) {\n  echo "فقط رقم";\n}\n?>',
    ["الگو: از اول تا آخر فقط رقم.", "اگر متن 123 باشد پیام چاپ می‌شود."])

add("مدیریت فرم (Form Handling)",
    "HTML فرم می‌فرستد؛ PHP در action آن را می‌گیرد.",
    "هر ورودی کاربر.",
    '<form method="post" action="save.php">\n  <input name="email">\n  <button>ارسال</button>\n</form>',
    ["method=post داده را در بدنه می‌فرستد.", "name همان کلید $_POST است.", "action فایل PHP گیرنده است."])

add("اعتبارسنجی فرم (Form Validation)",
    "چک کن داده خالی، کوتاه یا غلط نباشد.",
    "قبل از ذخیره در دیتابیس.",
    '<?php\n$email = trim($_POST["email"] ?? "");\nif ($email === "") {\n  echo "ایمیل لازم است";\n}\n?>',
    ["trim فاصله را حذف می‌کند.", "اگر خالی بود پیام خطا."])

add("فیلدهای اجباری فرم (Form Required)",
    "بعضی فیلدها نباید خالی باشند.",
    "نام و ایمیل در ثبت‌نام.",
    '<?php\nif (empty($_POST["name"])) {\n  echo "نام را بنویس";\n}\n?>',
    ["empty یعنی خالی یا صفر یا تعریف‌نشده."])

add("اعتبارسنجی URL/ایمیل (Form URL/E-mail)",
    "با filter_var فرمت ایمیل و URL را چک می‌کنی.",
    "ثبت‌نام و لینک.",
    '<?php\n$e = "a@b.com";\nif (filter_var($e, FILTER_VALIDATE_EMAIL)) {\n  echo "ایمیل درست";\n}\n?>',
    ["FILTER_VALIDATE_EMAIL فرمت را چک می‌کند نه اینکه صندوق واقعاً وجود دارد."])

add("فرم کامل (Form Complete)",
    "گرفتن، پاک‌سازی، اعتبارسنجی، بعد استفاده.",
    "هر فرم واقعی.",
    '<?php\n$name = htmlspecialchars(trim($_POST["name"] ?? ""));\nif (strlen($name) < 2) {\n  echo "نام کوتاه است";\n} else {\n  echo "سلام " . $name;\n}\n?>',
    ["trim و htmlspecialchars.", "طول حداقل ۲.", "اگر قبول شد پیام."])

add("تاریخ و زمان (Date and Time)",
    "date و time زمان سرور را می‌دهند.",
    "تاریخ پست، فاکتور، لاگ.",
    '<?php\ndate_default_timezone_set("Asia/Tehran");\necho date("Y-m-d H:i");\necho time();\n?>',
    ["منطقه تهران.", "قالب سال-ماه-روز ساعت.", "time مهر یونیکس است."])

add("اینکلود (Include)",
    "فایل دیگر را داخل این فایل می‌آورد.",
    "هدر و فوتر مشترک.",
    '<?php\ninclude "header.php";\nrequire "config.php";\n?>',
    ["include اگر فایل نباشد هشدار می‌دهد و ادامه می‌دهد.", "require اگر نباشد برنامه می‌ایستد."])

add("مدیریت فایل (File Handling)",
    "خواندن و نوشتن فایل روی سرور.",
    "لاگ، آپلود، ذخیره متن.",
    '<?php\nfile_put_contents("a.txt", "سلام");\necho file_get_contents("a.txt");\n?>',
    ["نوشتن.", "خواندن و چاپ."])

add("باز/خواندن فایل (File Open/Read)",
    "fopen فایل را باز می‌کند؛ fread یا fgets می‌خواند.",
    "فایل بزرگ خط‌به‌خط.",
    '<?php\n$f = fopen("a.txt", "r");\necho fgets($f);\nfclose($f);\n?>',
    ["r یعنی فقط خواندن.", "fgets یک خط.", "fclose بستن."])

add("ایجاد/نوشتن فایل (File Create/Write)",
    "حالت w از صفر می‌نویسد؛ a به انتها اضافه می‌کند.",
    "لاگ روزانه.",
    '<?php\n$f = fopen("log.txt", "a");\nfwrite($f, "خط جدید\\n");\nfclose($f);\n?>',
    ["a یعنی append.", "fwrite می‌نویسد."])

add("آپلود فایل (File Upload)",
    "فایل از فرم با enctype مخصوص می‌آید و در $_FILES است.",
    "عکس پروفایل، رزومه.",
    '<?php\n$tmp = $_FILES["photo"]["tmp_name"] ?? "";\n$name = basename($_FILES["photo"]["name"] ?? "");\nif ($tmp && is_uploaded_file($tmp)) {\n  move_uploaded_file($tmp, "uploads/" . $name);\n}\n?>',
    ["tmp_name فایل موقت سرور.", "basename فقط نام فایل نه مسیر.", "is_uploaded_file امنیت.", "move به پوشه نهایی."])

add("کوکی ها (Cookies)",
    "داده کوچک در مرورگر کاربر با setcookie.",
    "یادآوری زبان یا تم. برای ورود بهتر است سشن.",
    '<?php\nsetcookie("lang", "fa", time() + 86400, "/");\necho $_COOKIE["lang"] ?? "";\n?>',
    ["یک روز اعتبار.", "در درخواست بعدی در $_COOKIE می‌آید."])

add("سشن ها (Sessions)",
    "داده کاربر روی سرور بین صفحات.",
    "ورود، سبد خرید.",
    '<?php\nsession_start();\n$_SESSION["user"] = "علی";\necho $_SESSION["user"];\n?>',
    ["session_start قبل از هر خروجی.", "مقدار در $_SESSION می‌ماند تا مرورگر بسته شود یا از بین ببری."])

add("فیلترها (Filters)",
    "filter_var داده را پاک یا اعتبارسنجی می‌کند.",
    "ایمیل، عدد، URL.",
    '<?php\n$n = filter_var("42abc", FILTER_SANITIZE_NUMBER_INT);\necho $n;\n?>',
    ["فقط رقم‌ها می‌مانند."])

add("فیلترهای پیشرفته (Filters Advanced)",
    "می‌توانی گزینه بدهی مثلاً محدوده عدد.",
    "سن بین ۱ تا ۱۲۰.",
    '<?php\n$opts = ["options" => ["min_range" => 1, "max_range" => 120]];\nvar_dump(filter_var(20, FILTER_VALIDATE_INT, $opts));\n?>',
    ["اگر ۲۰ در بازه باشد عدد برمی‌گردد وگرنه false."])

add("توابع کال بک (Callback Functions)",
    "تابعی که به تابع دیگر می‌دهی تا روی هر عضو اجرا شود.",
    "array_map و usort.",
    '<?php\n$a = [1, 2, 3];\n$b = array_map(function ($x) { return $x * 2; }, $a);\nprint_r($b);\n?>',
    ["هر عضو دو برابر می‌شود."])

add("JSON (JSON)",
    "json_encode شیء را متن می‌کند؛ json_decode برعکس.",
    "API و جاوااسکریپت.",
    '<?php\n$t = json_encode(["name" => "علی"], JSON_UNESCAPED_UNICODE);\necho $t;\n$o = json_decode($t, true);\necho $o["name"];\n?>',
    ["encode به متن.", "UNESCAPED_UNICODE فارسی را درست نگه می‌دارد.", "decode با true یعنی آرایه انجمنی."])

add("استثناها (Exceptions)",
    "try/catch خطا را می‌گیرد تا برنامه نایستد.",
    "اتصال دیتابیس، فایل نبود.",
    '<?php\ntry {\n  throw new Exception("خراب شد");\n} catch (Exception $e) {\n  echo $e->getMessage();\n}\n?>',
    ["throw خطا می‌سازد.", "catch آن را می‌گیرد.", "getMessage متن خطا."])

add("OOP چیست؟ (What is OOP)",
    "برنامه‌نویسی شی‌گرا: داده و رفتار را در کلاس جمع می‌کنی.",
    "پروژه بزرگ، مدل کاربر و محصول.",
    '<?php\nclass User {\n  public $name;\n}\n$u = new User();\n$u->name = "سارا";\necho $u->name;\n?>',
    ["class قالب است.", "new یک نمونه می‌سازد.", "-> دسترسی به ویژگی."])

add("کلاس ها/اشیا (Classes/Objects)",
    "کلاس نقشه است؛ شیء خانه ساخته‌شده از آن نقشه.",
    "هر موجودیت برنامه.",
    '<?php\nclass Car {\n  public $color = "قرمز";\n}\n$c = new Car();\necho $c->color;\n?>',
    ["تعریف کلاس.", "ساخت شیء.", "خواندن ویژگی."])

add("سازنده (Constructor)",
    "__construct وقتی new می‌زنی اجرا می‌شود.",
    "دادن نام و مقدار اولیه.",
    '<?php\nclass P {\n  public $name;\n  public function __construct($n) {\n    $this->name = $n;\n  }\n}\n$p = new P("علی");\necho $p->name;\n?>',
    ["$this یعنی همین شیء.", "مقدار از new به سازنده می‌رسد."])

add("مخرب (Destructor)",
    "__destruct وقتی شیء از بین می‌رود اجرا می‌شود.",
    "بستن فایل یا اتصال.",
    '<?php\nclass F {\n  function __destruct() {\n    echo "بسته شد";\n  }\n}\n$x = new F();\nunset($x);\n?>',
    ["با unset یا پایان اسکریپت صدا زده می‌شود."])

add("سطوح دسترسی (Access Modifiers)",
    "public همه جا، private فقط داخل کلاس، protected کلاس و فرزند.",
    "مخفی کردن جزئیات داخلی.",
    '<?php\nclass A {\n  public $a = 1;\n  private $b = 2;\n}\n$o = new A();\necho $o->a;\n?>',
    ["$a قابل خواندن از بیرون است.", "$b از بیرون خطا می‌دهد."])

add("وراثت (Inheritance)",
    "کلاس فرزند ویژگی‌های پدر را می‌گیرد با extends.",
    "Admin نوعی User است.",
    '<?php\nclass Animal {\n  function speak() { echo "صدا"; }\n}\nclass Dog extends Animal {}\n(new Dog())->speak();\n?>',
    ["Dog متد speak را دارد بدون نوشتن دوباره."])

add("ثابت ها در کلاس (Class Constants)",
    "const داخل کلاس؛ با :: استفاده می‌شود.",
    "نقش‌ها و وضعیت‌های ثابت.",
    '<?php\nclass S {\n  const OK = 1;\n}\necho S::OK;\n?>',
    ["بدون $ و با ::"])

add("کلاس های انتزاعی (Abstract Classes)",
    "کلاسی که نمی‌شود new کرد؛ فقط پدر برای فرزندهاست.",
    "قالب اجباری برای چند کلاس شبیه هم.",
    '<?php\nabstract class Shape {\n  abstract function area();\n}\nclass Square extends Shape {\n  function area() { return 4; }\n}\necho (new Square())->area();\n?>',
    ["abstract function باید در فرزند پیاده شود."])

add("اینترفیس ها (Interfaces)",
    "قرارداد متدها بدون پیاده سازی. کلاس با implements تعهد می‌دهد.",
    "چند کلاس با متدهای هم‌نام.",
    '<?php\ninterface Log {\n  public function write($m);\n}\nclass FileLog implements Log {\n  public function write($m) { echo $m; }\n}\n?>',
    ["اگر write نباشد خطا می‌گیری."])

add("تِرِیت ها (Traits)",
    "تکه کد قابل استفاده در چند کلاس با use؛ ارث‌بری افقی.",
    "متد مشترک بدون پدر مشترک.",
    '<?php\ntrait Hello {\n  function hi() { echo "سلام"; }\n}\nclass A { use Hello; }\n(new A())->hi();\n?>',
    ["use Hello متد را به کلاس می‌آورد."])

add("متدهای استاتیک (Static Methods)",
    "متد کلاس بدون ساخت شیء؛ با :: صدا زده می‌شود.",
    "ابزار کمکی مثل تبدیل.",
    '<?php\nclass Math {\n  static function add($a, $b) { return $a + $b; }\n}\necho Math::add(2, 3);\n?>',
    ["static یعنی مال کلاس نه یک شیء خاص."])

add("خواص استاتیک (Static Properties)",
    "ویژگی مشترک بین همه نمونه‌ها.",
    "شمارنده کل اشیاء.",
    '<?php\nclass C {\n  public static $n = 0;\n  function __construct() { self::$n++; }\n}\nnew C(); new C();\necho C::$n;\n?>',
    ["هر new یکی به $n اضافه می‌کند. خروجی ۲."])

add("فضاهای نام (Namespaces)",
    "پوشه‌بندی اسم کلاس‌ها تا تداخل نداشته باشند.",
    "پروژه بزرگ و کتابخانه.",
    '<?php\nnamespace App\\\\Models;\nclass User {}\n?>',
    ["User واقعی می‌شود App\\Models\\User."])

add("قابل تکرارها (Iterables)",
    "چیزی که می‌شود foreach زد: آرایه یا شیء Iterator.",
    "نوع پارامتر تابع.",
    '<?php\nfunction show(iterable $x) {\n  foreach ($x as $v) echo $v;\n}\nshow([1, 2]);\n?>',
    ["iterable یعنی قابل حلقه زدن."])

add("معرفی MySQL (MySQL Database)",
    "MySQL جای ذخیره جدول‌های داده است؛ PHP با mysqli یا PDO حرف می‌زند.",
    "کاربران، سفارش، پست.",
    '-- جدول نمونه\nCREATE TABLE users (\n  id INT PRIMARY KEY AUTO_INCREMENT,\n  name VARCHAR(50)\n);',
    ["id کلید یکتا و خودکار.", "name متن تا ۵۰ نویسه."])

add("اتصال به MySQL (MySQL Connect)",
    "mysqli شیء اتصال می‌سازد.",
    "اولین قدم قبل از هر کوئری.",
    '<?php\n$mysqli = new mysqli("localhost", "root", "", "test");\nif ($mysqli->connect_error) {\n  die("اتصال نشد");\n}\n$mysqli->set_charset("utf8mb4");\n?>',
    ["میزبان، کاربر، رمز، نام دیتابیس.", "اگر خطا بود بایست.", "utf8mb4 برای فارسی و ایموجی."])

add("ایجاد پایگاه داده (MySQL Create DB)",
    "CREATE DATABASE یک بانک جدید می‌سازد.",
    "شروع پروژه.",
    '<?php\n$mysqli->query("CREATE DATABASE IF NOT EXISTS shop CHARACTER SET utf8mb4");\n?>',
    ["IF NOT EXISTS اگر بود خطا ندهد.", "کاراکترست فارسی."])

add("ایجاد جدول (MySQL Create Table)",
    "CREATE TABLE ستون‌ها را تعریف می‌کند.",
    "ساختار داده.",
    '<?php\n$mysqli->query("CREATE TABLE IF NOT EXISTS products (\n  id INT AUTO_INCREMENT PRIMARY KEY,\n  title VARCHAR(100) NOT NULL,\n  price INT\n)");\n?>',
    ["PRIMARY KEY یکتا.", "NOT NULL خالی ممنوع."])

add("درج داده (MySQL Insert Data)",
    "INSERT یک ردیف اضافه می‌کند.",
    "ثبت‌نام، سفارش جدید.",
    '<?php\n$stmt = $mysqli->prepare("INSERT INTO users (name) VALUES (?)");\n$stmt->bind_param("s", $name);\n$name = "سارا";\n$stmt->execute();\n?>',
    ["? جای مقدار است.", "s یعنی رشته.", "execute اجرا می‌کند. هرگز متغیر را مستقیم به SQL نچسبان."])

add("گرفتن آخرین ID (MySQL Get Last ID)",
    "insert_id شناسه ردیف تازه‌درج‌شده.",
    "بعد از ثبت کاربر، ساخت پروفایل با همان id.",
    '<?php\n$mysqli->query("INSERT INTO users (name) VALUES (\'علی\')");\necho $mysqli->insert_id;\n?>',
    ["AUTO_INCREMENT آخرین مقدار را می‌دهد."])

add("درج چندتایی (MySQL Insert Multiple)",
    "چند ردیف در یک INSERT یا حلقه prepare.",
    "وارد کردن لیست.",
    '<?php\n$mysqli->query("INSERT INTO users (name) VALUES (\'a\'), (\'b\')");\n?>',
    ["دو ردیف با یک دستور."])

add("دستورات آماده (MySQL Prepared)",
    "قالب SQL با ? که مقدار جدا bind می‌شود؛ جلوی تزریق SQL را می‌گیرد.",
    "هر ورودی کاربر به دیتابیس.",
    '<?php\n$stmt = $mysqli->prepare("SELECT name FROM users WHERE id = ?");\n$stmt->bind_param("i", $id);\n$id = 1;\n$stmt->execute();\n$res = $stmt->get_result();\n$row = $res->fetch_assoc();\necho $row["name"] ?? "";\n?>',
    ["i یعنی عدد صحیح.", "get_result ردیف‌ها را می‌دهد.", "fetch_assoc آرایه انجمنی."])

add("انتخاب داده (MySQL Select Data)",
    "SELECT ردیف‌ها را می‌آورد.",
    "لیست نمایش.",
    '<?php\n$r = $mysqli->query("SELECT id, name FROM users");\nwhile ($row = $r->fetch_assoc()) {\n  echo $row["name"];\n}\n?>',
    ["هر دور یک ردیف."])

add("شرط Where (MySQL Where)",
    "WHERE فیلتر می‌کند.",
    "یک کاربر خاص، سفارش‌های باز.",
    '<?php\n$stmt = $mysqli->prepare("SELECT * FROM users WHERE age > ?");\n$stmt->bind_param("i", $min);\n$min = 18;\n$stmt->execute();\n?>',
    ["فقط سن بزرگ‌تر از ۱۸."])

add("مرتب سازی (MySQL Order By)",
    "ORDER BY ترتیب را عوض می‌کند.",
    "جدیدترین پست، ارزان‌ترین محصول.",
    '<?php\n$r = $mysqli->query("SELECT name FROM users ORDER BY id DESC");\n?>',
    ["DESC از بزرگ به کوچک."])

add("حذف داده (MySQL Delete Data)",
    "DELETE ردیف را پاک می‌کند. حتماً WHERE بگذار.",
    "حذف حساب یا آیتم.",
    '<?php\n$stmt = $mysqli->prepare("DELETE FROM users WHERE id = ?");\n$stmt->bind_param("i", $id);\n$id = 5;\n$stmt->execute();\n?>',
    ["بدون WHERE همه جدول پاک می‌شود — خطرناک."])

add("به روزرسانی داده (MySQL Update Data)",
    "UPDATE مقدار ستون را عوض می‌کند.",
    "تغییر ایمیل یا وضعیت.",
    '<?php\n$stmt = $mysqli->prepare("UPDATE users SET name = ? WHERE id = ?");\n$stmt->bind_param("si", $name, $id);\n$name = "رضا"; $id = 1;\n$stmt->execute();\n?>',
    ["s رشته، i عدد.", "WHERE مشخص می‌کند کدام ردیف."])

add("محدودیت نتایج (MySQL Limit Data)",
    "LIMIT تعداد ردیف برمی‌گرداند؛ OFFSET صفحه.",
    "صفحه‌بندی.",
    '<?php\n$r = $mysqli->query("SELECT * FROM users LIMIT 10 OFFSET 20");\n?>',
    ["۱۰ تا، از ردیف ۲۰ به بعد — صفحه سوم اگر هر صفحه ۱۰ تا باشد."])

add("تجزیه گرهای XML (XML Parsers)",
    "PHP چند راه برای خواندن XML دارد: SimpleXML، DOM، Expat.",
    "فید RSS، خروجی نرم‌افزار دیگر.",
    '<?php\n$xml = simplexml_load_string("<a><b>1</b></a>");\necho $xml->b;\n?>',
    ["رشته XML به شیء.", "مثل ویژگی شیء می‌خوانی."])

add("سیمپل XML: خواندن (SimpleXML Parser)",
    "ساده‌ترین راه خواندن XML.",
    "فایل تنظیمات یا فید.",
    '<?php\n$x = simplexml_load_file("data.xml");\necho $x->item[0]->title;\n?>',
    ["اولین item، تگ title."])

add("سیمپل XML: دریافت (SimpleXML-Get)",
    "با -> و [] به عنصر و ویژگی می‌رسی.",
    "خواندن ویژگی XML.",
    '<?php\n$x = simplexml_load_string(\'<n id="5">علی</n>\');\necho $x;\necho $x["id"];\n?>',
    ["متن داخل تگ.", "ویژگی id."])

add("XML اکسپت (XML Expat)",
    "parser رویدادمحور: وقتی تگ شروع شد تابع صدا می‌شود. برای فایل خیلی بزرگ.",
    "XML حجیم.",
    '<?php\n$p = xml_parser_create();\nxml_parse($p, "<root></root>");\nxml_parser_free($p);\n?>',
    ["ساخت parser.", "parse متن.", "آزاد کردن."])

add("DOM در PHP (XML DOM)",
    "درخت کامل XML مثل مرورگر.",
    "تغییر و ذخیره XML.",
    '<?php\n$dom = new DOMDocument();\n$dom->loadXML("<a>1</a>");\necho $dom->textContent;\n?>',
    ["loadXML از رشته.", "textContent متن‌ها."])

add("مقدمه AJAX (AJAX Intro)",
    "صفحه بدون رفرش کامل با سرور حرف می‌زند. سمت سرور اغلب PHP است.",
    "جستجوی زنده، لایک، فرم بدون پرش صفحه.",
    '// جاوااسکریپت\nfetch("api.php").then(r => r.text()).then(console.log);',
    ["مرورگر به api.php درخواست می‌زند.", "PHP پاسخ می‌دهد.", "JS آن را نشان می‌دهد."])

add("AJAX با PHP (AJAX PHP)",
    "PHP فقط داده برمی‌گرداند (متن یا JSON) نه کل صفحه.",
    "API کوچک.",
    '<?php\nheader("Content-Type: application/json; charset=utf-8");\necho json_encode(["ok" => true]);\n?>',
    ["هدر می‌گوید پاسخ JSON است.", "encode آرایه را متن می‌کند."])

add("AJAX و پایگاه داده (AJAX Database)",
    "درخواست می‌آید، PHP از MySQL می‌خواند، JSON برمی‌گرداند.",
    "لیست زنده محصولات.",
    '<?php\nheader("Content-Type: application/json; charset=utf-8");\n$r = $mysqli->query("SELECT id, name FROM users LIMIT 10");\necho json_encode($r->fetch_all(MYSQLI_ASSOC));\n?>',
    ["fetch_all همه ردیف‌ها.", "JSON برای JS."])

add("AJAX و XML (AJAX XML)",
    "به‌جای JSON می‌توانی XML برگردانی؛ امروز JSON رایج‌تر است.",
    "سیستم قدیمی.",
    '<?php\nheader("Content-Type: text/xml");\necho "<ok>1</ok>";\n?>',
    ["هدر XML.", "بدنه تگ."])

add("جستجوی زنده AJAX (AJAX Live Search)",
    "با هر حرف، JS به PHP می‌فرستد و پیشنهاد می‌گیرد.",
    "جستجوی نام.",
    '<?php\n$q = trim($_GET["q"] ?? "");\n$stmt = $mysqli->prepare("SELECT name FROM users WHERE name LIKE CONCAT(\'%\', ?, \'%\') LIMIT 8");\n$stmt->bind_param("s", $q);\n$stmt->execute();\n?>',
    ["LIKE جستجوی بخشی.", "LIMIT جلوی نتیجه زیاد را می‌گیرد.", "prepare امن است."])

add("نظرسنجی AJAX (AJAX Poll)",
    "رأی بدون رفرش ذخیره می‌شود و درصد برمی‌گردد.",
    "نظرسنجی سایت.",
    '<?php\n// رأی را ذخیره کن و JSON درصدها را برگردان\necho json_encode(["yes" => 12, "no" => 5]);\n?>',
    ["JS این عددها را به نوار پیشرفت تبدیل می‌کند."])

add("نمونه ها (Examples)",
    "تمرین کوچک بهتر از خواندن تنهاست.",
    "یادگیری پایدار.",
    '<?php\n// تمرین: فرم نام را بگیر و با htmlspecialchars چاپ کن\n?>',
    ["خودت بنویس و اجرا کن."])

add("کامپایلر (Compiler)",
    "PHP تفسیر می‌شود نه مثل C کامپایل کامل؛ برای تمرین از php -S یا سایت تمرین آنلاین استفاده کن.",
    "دیدن خروجی سریع.",
    'php -S localhost:8000',
    ["سرور کوچک روی سیستم خودت."])

add("آزمون (Quiz)",
    "از خودت بپرس: تفاوت GET و POST چیست؟ prepare یعنی چه؟",
    "محکم شدن پایه.",
    '<?php\necho "سه سؤال برای خودت بنویس و جواب بده";\n?>',
    ["اگر نتوانستی جواب بدهی همان درس را دوباره بخوان."])

add("تمرین ها (Exercises)",
    "فرم تماس، لیست کارها، دفترچه تلفن با آرایه.",
    "مهارت واقعی.",
    '<?php\n// تمرین: آرایه نمرات را بگیر میانگین را چاپ کن\n$s = [18, 15, 20];\necho array_sum($s) / count($s);\n?>',
    ["جمع تقسیم بر تعداد."])

add("سرور (Server)",
    "Apache یا php -S فایل PHP را اجرا می‌کند.",
    "بدون سرور echo دیده نمی‌شود.",
    '# پوشه پروژه\nphp -S localhost:8000',
    ["مرورگر: http://localhost:8000/index.php"])

add("سیلابس (Syllabus)",
    "مسیر پیشنهادی: پایه → فرم → فایل → سشن → دیتابیس → OOP.",
    "ترتیب یادگیری.",
    '<?php echo "پایه سپس فرم سپس MySQL"; ?>',
    ["از این ترتیب جلو برو."])

add("برنامه مطالعه (Study Plan)",
    "هر روز یک موضوع کوچک + یک تمرین ۱۰ دقیقه‌ای.",
    "پیوستگی مهم‌تر از ساعت طولانی است.",
    '<?php echo "امروز: $_POST و htmlspecialchars"; ?>',
    ["همان را در یک فرم واقعی به کار ببر."])

add("گواهینامه (Certificate)",
    "وقتی بتوانی یک فرم امن + ذخیره MySQL بسازی، پایه را بلد هستی.",
    "معیار واقعی مهارت.",
    '<?php echo "پروژه پایانی: دفترچه مخاطبین"; ?>',
    ["لیست، افزودن، حذف با prepare."])

add("نمای کلی PHP (Overview)",
    "PHP برای تولید HTML پویا، API و کار با دیتابیس ساخته شده.",
    "بیشتر سایت‌های کلاسیک وردپرس و فروشگاه‌ها.",
    '<?php echo phpversion(); ?>',
    ["نسخه PHP سرور را نشان می‌دهد."])

add("مرجع آرایه (PHP Array)",
    "از اینجا توابع آرایه یکی‌یکی می‌آید. هر تابع یک کار مشخص دارد.",
    "دستکاری لیست بدون حلقه دستی طولانی.",
    '<?php print_r(array_keys(["a" => 1])); ?>',
    ["array_keys فقط کلیدها را می‌دهد."])

# Function-specific examples
FN = {
"array()": ('$a = array(1, 2, 3);\nprint_r($a);', "ساخت آرایه با array()."),
"array_change_key_case": ('print_r(array_change_key_case(["A"=>1], CASE_LOWER));', "کلیدها را کوچک یا بزرگ می‌کند."),
"array_chunk": ('print_r(array_chunk([1,2,3,4], 2));', "آرایه را به تکه‌های ۲تایی می‌برد."),
"array_column": ('$r=[["id"=>1,"n"=>"a"]]; print_r(array_column($r,"n"));', "یک ستون از آرایه دوبعدی."),
"array_combine": ('print_r(array_combine(["a","b"], [1,2]));', "کلیدها از اولی، مقدار از دومی."),
"array_count_values": ('print_r(array_count_values([1,1,2]));', "هر مقدار چند بار تکرار شده."),
"array_diff": ('print_r(array_diff([1,2,3],[2]));', "آنچه در اولی هست و در دومی نیست."),
"array_diff_assoc": ('print_r(array_diff_assoc(["a"=>1],["a"=>2]));', "هم کلید هم مقدار را مقایسه می‌کند."),
"array_diff_key": ('print_r(array_diff_key(["a"=>1,"b"=>2],["a"=>9]));', "فقط کلید را مقایسه می‌کند."),
"array_fill": ('print_r(array_fill(0, 3, "x"));', "۳ خانه با مقدار x از ایندکس ۰."),
"array_fill_keys": ('print_r(array_fill_keys(["a","b"], 0));', "کلیدها داده می‌شوند مقدار مشترک."),
"array_filter": ('print_r(array_filter([0,1,2]));', "مقادیر تهی حذف می‌شوند مگر تابع بدهی."),
"array_flip": ('print_r(array_flip(["a"=>1]));', "کلید و مقدار جایشان عوض می‌شود."),
"array_intersect": ('print_r(array_intersect([1,2],[2,3]));', "اشتراک مقدارها."),
"array_key_exists": ('var_dump(array_key_exists("a", ["a"=>1]));', "آیا کلید هست."),
"array_keys": ('print_r(array_keys(["a"=>1,"b"=>2]));', "لیست کلیدها."),
"array_map": ('print_r(array_map(fn($x)=>$x*2, [1,2]));', "تابع روی همه اعضا."),
"array_merge": ('print_r(array_merge([1],[2,3]));', "به هم چسباندن."),
"array_merge_recursive": ('print_r(array_merge_recursive(["a"=>[1]],["a"=>[2]]));', "ادغام تودرتو."),
"array_multisort": ('$a=[2,1]; $b=["b","a"]; array_multisort($a,$b); print_r($b);', "چند آرایه را با هم مرتب می‌کند."),
"array_pad": ('print_r(array_pad([1,2], 5, 0));', "طول را با مقدار پر می‌کند."),
"array_pop": ('$a=[1,2,3]; echo array_pop($a);', "آخرین عضو را برمی‌دارد."),
"array_product": ('echo array_product([2,3,4]);', "ضرب همه مقادیر."),
"array_push": ('$a=[1]; array_push($a, 2, 3); print_r($a);', "به انتها اضافه می‌کند."),
"array_rand": ('echo array_rand(["a"=>1,"b"=>2]);', "یک کلید تصادفی."),
"array_reduce": ('echo array_reduce([1,2,3], fn($c,$x)=>$c+$x, 0);', "همه را به یک مقدار کاهش می‌دهد."),
"array_replace": ('print_r(array_replace(["a"=>1],["a"=>9]));', "مقادیر هم‌کلید جایگزین می‌شوند."),
"array_reverse": ('print_r(array_reverse([1,2,3]));', "ترتیب برعکس."),
"array_search": ('echo array_search("b", ["a","b"]);', "ایندکس مقدار را می‌دهد."),
"array_shift": ('$a=[1,2]; echo array_shift($a);', "اولین عضو را برمی‌دارد."),
"array_slice": ('print_r(array_slice([10,20,30], 1, 2));', "برش بدون تغییر اصل."),
"array_splice": ('$a=[1,2,3]; array_splice($a,1,1,[9]); print_r($a);', "حذف و جایگذاری روی خود آرایه."),
"array_sum": ('echo array_sum([1,2,3]);', "جمع مقادیر."),
"array_unique": ('print_r(array_unique([1,1,2]));', "تکراری‌ها حذف."),
"array_unshift": ('$a=[2]; array_unshift($a,1); print_r($a);', "به ابتدا اضافه."),
"array_values": ('print_r(array_values(["a"=>1,"b"=>2]));', "فقط مقادیر با ایندکس نو."),
"array_walk": ('$a=[1,2]; array_walk($a, fn(&$v)=>$v*=2); print_r($a);', "روی هر عضو تابع اجرا می‌کند."),
"arsort": ('$a=["b"=>1,"a"=>3]; arsort($a); print_r($a);', "نزولی بر اساس مقدار، کلید حفظ."),
"asort": ('$a=["b"=>3,"a"=>1]; asort($a); print_r($a);', "صعودی بر اساس مقدار، کلید حفظ."),
"compact": ('$x=1; $y=2; print_r(compact("x","y"));', "متغیرها را آرایه می‌کند."),
"count": ('echo count([1,2,3]);', "تعداد اعضا."),
"current": ('$a=[10,20]; echo current($a);', "عضو فعلی اشاره‌گر داخلی."),
"end": ('$a=[10,20,30]; echo end($a);', "اشاره‌گر به آخر و مقدار آخر."),
"extract": ('extract(["name"=>"علی"]); echo $name;', "کلیدهای آرایه به متغیر تبدیل می‌شوند — با احتیاط."),
"in_array": ('var_dump(in_array(2, [1,2,3]));', "آیا مقدار داخل آرایه است."),
"key": ('$a=["a"=>1]; echo key($a);', "کلید فعلی اشاره‌گر."),
"krsort": ('$a=["b"=>1,"a"=>2]; krsort($a); print_r($a);', "نزولی بر اساس کلید."),
"ksort": ('$a=["b"=>1,"a"=>2]; ksort($a); print_r($a);', "صعودی بر اساس کلید."),
"list": ('list($a,$b)=[1,2]; echo $a,$b;', "اعضای آرایه را به متغیر می‌ریزد."),
"natsort": ('$a=["img12","img2"]; natsort($a); print_r($a);', "مرتب‌سازی طبیعی: img2 قبل img12."),
"next": ('$a=[1,2]; next($a); echo current($a);', "اشاره‌گر را یکی جلو می‌برد."),
"prev": ('$a=[1,2]; end($a); prev($a); echo current($a);', "اشاره‌گر را یکی عقب می‌برد."),
"range": ('print_r(range(1, 4));', "آرایه از ۱ تا ۴."),
"reset": ('$a=[1,2]; end($a); reset($a); echo current($a);', "اشاره‌گر به اول."),
"rsort": ('$a=[1,3,2]; rsort($a); print_r($a);', "نزولی؛ کلیدها از نو."),
"shuffle": ('$a=[1,2,3]; shuffle($a); print_r($a);', "ترتیب تصادفی."),
"sizeof": ('echo sizeof([1,2]);', "همان count."),
"sort": ('$a=["b","a"]; sort($a); print_r($a);', "صعودی؛ کلیدها از نو."),
"usort": ('$a=[3,1,2]; usort($a, fn($x,$y)=>$x<=>$y); print_r($a);', "مرتب با تابع خودت."),
"uasort": ('$a=["a"=>3,"b"=>1]; uasort($a, fn($x,$y)=>$x<=>$y); print_r($a);', "مرتب مقدار با حفظ کلید."),
"uksort": ('$a=["b"=>1,"a"=>2]; uksort($a, fn($x,$y)=>$x<=>$y); print_r($a);', "مرتب کلید با تابع."),
"cal_days_in_month": ('echo cal_days_in_month(CAL_GREGORIAN, 2, 2024);', "تعداد روز فوریه ۲۰۲۴ (کبیسه ۲۹)."),
"date_create": ('$d = date_create("2026-01-01"); echo date_format($d, "Y-m-d");', "ساخت شیء تاریخ."),
"date_add": ('$d=date_create("2026-01-01"); date_add($d, date_interval_create_from_date_string("10 days")); echo date_format($d,"Y-m-d");', "۱۰ روز اضافه."),
"date_diff": ('$a=date_create("2026-01-01"); $b=date_create("2026-01-10"); echo date_diff($a,$b)->days;', "اختلاف به روز."),
"date_format": ('echo date_format(date_create(), "Y-m-d");', "قالب نمایش."),
"date_modify": ('$d=date_create(); date_modify($d, "+1 month"); echo date_format($d,"Y-m");', "یک ماه جلو."),
"date_default_timezone_set": ('date_default_timezone_set("Asia/Tehran"); echo date("H:i");', "ساعت محلی تهران."),
"date": ('echo date("Y/m/d H:i");', "تاریخ و ساعت فعلی با قالب."),
"time": ('echo time();', "ثانیه‌ها از ۱۹۷۰."),
"strtotime": ('echo date("Y-m-d", strtotime("+1 week"));', "متن نسبی به زمان."),
"mktime": ('echo date("Y-m-d", mktime(0,0,0,12,1,2026));', "از اجزای تاریخ timestamp بساز."),
"microtime": ('echo microtime(true);', "زمان با اعشار برای اندازه‌گیری سرعت."),
"checkdate": ('var_dump(checkdate(2, 29, 2024));', "آیا تاریخ معتبر است."),
"getdate": ('print_r(getdate());', "آرایه سال و ماه و روز."),
"chdir": ('chdir(__DIR__); echo getcwd();', "پوشه جاری را عوض می‌کند."),
"getcwd": ('echo getcwd();', "مسیر پوشه فعلی."),
"scandir": ('print_r(scandir("."));', "لیست فایل‌های پوشه."),
"opendir": ('$d=opendir("."); echo readdir($d); closedir($d);', "خواندن نام فایل‌ها یکی‌یکی."),
"error_reporting": ('error_reporting(E_ALL);', "چه خطاهایی نشان داده شود."),
"error_get_last": ('@fopen("nope","r"); print_r(error_get_last());', "آخرین خطا."),
"error_log": ('error_log("مشکل در پرداخت");', "نوشتن در لاگ سرور."),
"trigger_error": ('trigger_error("توجه", E_USER_WARNING);', "هشدار خودت."),
"set_error_handler": ('set_error_handler(function($c,$m){ echo $m; });', "تابع دلخواه برای خطا."),
"Exception": ('try { throw new Exception("x"); } catch(Exception $e){ echo $e->getMessage(); }', "پرتاب و گرفتن استثنا."),
"getMessage": ('try{throw new Exception("متن");}catch(Exception $e){echo $e->getMessage();}', "متن خطا."),
"getFile": ('try{throw new Exception("x");}catch(Exception $e){echo $e->getFile();}', "فایلی که خطا رخ داد."),
"getLine": ('try{throw new Exception("x");}catch(Exception $e){echo $e->getLine();}', "شماره خط."),
"getCode": ('try{throw new Exception("x", 7);}catch(Exception $e){echo $e->getCode();}', "کد عددی خطا."),
"getTrace": ('try{throw new Exception("x");}catch(Exception $e){print_r($e->getTrace());}', "پشته فراخوانی."),
"basename": ('echo basename("/a/b/c.txt");', "فقط نام فایل."),
"dirname": ('echo dirname("/a/b/c.txt");', "پوشه والد."),
"copy": ('copy("a.txt", "b.txt");', "کپی فایل."),
"file_exists": ('var_dump(file_exists("a.txt"));', "آیا فایل هست."),
"file_get_contents": ('echo file_get_contents("a.txt");', "کل فایل به رشته."),
"file_put_contents": ('file_put_contents("a.txt", "hi");', "رشته را در فایل بنویس."),
"filesize": ('echo filesize("a.txt");', "حجم به بایت."),
"fopen": ('$f=fopen("a.txt","r"); fclose($f);', "باز کردن فایل."),
"fread": ('$f=fopen("a.txt","r"); echo fread($f, 100); fclose($f);', "خواندن تعداد بایت."),
"fwrite": ('$f=fopen("a.txt","w"); fwrite($f, "x"); fclose($f);', "نوشتن."),
"fgets": ('$f=fopen("a.txt","r"); echo fgets($f); fclose($f);', "یک خط."),
"fclose": ('$f=fopen("a.txt","r"); fclose($f);', "بستن."),
"feof": ('$f=fopen("a.txt","r"); while(!feof($f)) echo fgets($f); fclose($f);', "تا پایان فایل."),
"is_dir": ('var_dump(is_dir("."));', "آیا پوشه است."),
"is_file": ('var_dump(is_file("a.txt"));', "آیا فایل معمولی است."),
"is_readable": ('var_dump(is_readable("a.txt"));', "قابل خواندن؟"),
"is_writable": ('var_dump(is_writable("."));', "قابل نوشتن؟"),
"mkdir": ('mkdir("tmp_dir");', "ساخت پوشه."),
"rmdir": ('rmdir("tmp_dir");', "حذف پوشه خالی."),
"unlink": ('unlink("a.txt");', "حذف فایل."),
"rename": ('rename("a.txt", "b.txt");', "تغییر نام یا جابجایی."),
"realpath": ('echo realpath(".");', "مسیر مطلق واقعی."),
"pathinfo": ('print_r(pathinfo("/a/b.txt"));', "پوشه، نام، پسوند."),
"glob": ('print_r(glob("*.php"));', "فایل‌ها با الگو."),
"move_uploaded_file": ('// move_uploaded_file($tmp, "uploads/".$name);', "انتقال آپلود به پوشه امن."),
"is_uploaded_file": ('// is_uploaded_file($tmp)', "فقط فایل آمده از HTTP POST."),
"filter_var": ('var_dump(filter_var("a@b.com", FILTER_VALIDATE_EMAIL));', "اعتبارسنجی ایمیل."),
"filter_input": ('$e = filter_input(INPUT_POST, "email", FILTER_VALIDATE_EMAIL);', "مستقیم از ورودی POST."),
"filter_list": ('print_r(filter_list());', "نام فیلترهای موجود."),
"filter_has_var": ('var_dump(filter_has_var(INPUT_GET, "q"));', "آیا متغیر در GET هست."),
"json_encode": ('echo json_encode(["ok"=>true], JSON_UNESCAPED_UNICODE);', "آرایه به JSON."),
"json_decode": ('print_r(json_decode(\'{"a":1}\', true));', "JSON به آرایه."),
"ftp_connect": ('// $ftp = ftp_connect("ftp.example.com");', "اتصال به سرور FTP — روی سرور واقعی."),
"ftp_login": ('// ftp_login($ftp, "user", "pass");', "ورود FTP."),
"ftp_get": ('// ftp_get($ftp, "local.txt", "remote.txt", FTP_BINARY);', "دانلود فایل."),
"ftp_put": ('// ftp_put($ftp, "remote.txt", "local.txt", FTP_BINARY);', "آپلود فایل."),
"ftp_close": ('// ftp_close($ftp);', "بستن اتصال."),
"mail": ('// mail("a@b.com", "موضوع", "متن", "From: me@site.com");', "ارسال ایمیل — نیاز به تنظیم سرور."),
"abs": ('echo abs(-12);', "قدر مطلق: ۱۲."),
"ceil": ('echo ceil(3.2);', "سقف: ۴."),
"floor": ('echo floor(3.9);', "کف: ۳."),
"round": ('echo round(3.5);', "گرد کردن."),
"sqrt": ('echo sqrt(9);', "ریشه دوم: ۳."),
"pow": ('echo pow(2, 8);', "۲ به توان ۸."),
"max": ('echo max(1, 9, 3);', "بزرگ‌ترین."),
"min": ('echo min(1, 9, 3);', "کوچک‌ترین."),
"pi": ('echo pi();', "عدد پی."),
"sin": ('echo sin(deg2rad(90));', "سینوس ۹۰ درجه ≈ ۱."),
"cos": ('echo cos(0);', "کسینوس ۰ = ۱."),
"tan": ('echo tan(deg2rad(45));', "تانژانت ۴۵ ≈ ۱."),
"deg2rad": ('echo deg2rad(180);', "درجه به رادیان."),
"rad2deg": ('echo rad2deg(pi());', "رادیان به درجه: ۱۸۰."),
"intdiv": ('echo intdiv(10, 3);', "تقسیم صحیح: ۳."),
"fmod": ('echo fmod(10.5, 3);', "باقی‌مانده اعشاری."),
"base_convert": ('echo base_convert("ff", 16, 10);', "هگز FF به دهدهی ۲۵۵."),
"bindec": ('echo bindec("1010");', "دودویی به ۱۰."),
"decbin": ('echo decbin(10);', "۱۰ به دودویی."),
"dechex": ('echo dechex(255);', "به هگز: ff."),
"hexdec": ('echo hexdec("ff");', "هگز به دهدهی."),
"decoct": ('echo decoct(8);', "به اکتال."),
"octdec": ('echo octdec("10");', "اکتال به دهدهی."),
"rand": ('echo rand(1, 6);', "تاس ۱ تا ۶ — برای امنیت از random_int استفاده کن."),
"mt_rand": ('echo mt_rand(1, 100);', "تصادفی سریع‌تر."),
"is_finite": ('var_dump(is_finite(1.2));', "عدد متناهی است؟"),
"is_infinite": ('var_dump(is_infinite(log(0)));', "بی‌نهایت؟"),
"is_nan": ('var_dump(is_nan(acos(2)));', "آیا NaN است."),
"define": ('define("A", 1); echo A;', "تعریف ثابت."),
"defined": ('var_dump(defined("PHP_VERSION"));', "آیا ثابت تعریف شده."),
"constant": ('echo constant("PHP_VERSION");', "خواندن ثابت از روی نام رشته."),
"die": ('// die("پایان");', "پیام چاپ و توقف اسکریپت."),
"exit": ('// exit(0);', "خروج از برنامه."),
"sleep": ('// sleep(1);', "یک ثانیه صبر."),
"usleep": ('// usleep(500000);', "نیم ثانیه (میکروثانیه)."),
"uniqid": ('echo uniqid("id_", true);', "شناسه نسبتاً یکتا."),
"eval": ('// از eval در کد واقعی پرهیز کن', "اجرای رشته به‌عنوان کد — خطر امنیتی."),
"pack": ('echo bin2hex(pack("n", 258));', "بسته‌بندی باینری."),
"unpack": ('print_r(unpack("n", pack("n", 258)));', "باز کردن باینری."),
"affected_rows": ('// echo $mysqli->affected_rows;', "چند ردیف INSERT/UPDATE/DELETE شد."),
"insert_id": ('// echo $mysqli->insert_id;', "آخرین AUTO_INCREMENT."),
"query": ('// $mysqli->query("SELECT 1");', "اجرای SQL — برای ورودی کاربر prepare."),
"prepare": ('// $stmt=$mysqli->prepare("SELECT * FROM t WHERE id=?");', "قالب امن."),
"real_escape_string": ('// $mysqli->real_escape_string($s);', "فرار نویسه — باز هم prepare بهتر است."),
"fetch_assoc": ('// $row = $result->fetch_assoc();', "یک ردیف به‌صورت آرایه نام‌دار."),
"fetch_row": ('// $row = $result->fetch_row();', "یک ردیف با ایندکس عددی."),
"fetch_all": ('// $all = $result->fetch_all(MYSQLI_ASSOC);', "همه ردیف‌ها."),
"connect": ('// new mysqli($host,$user,$pass,$db);', "اتصال."),
"close": ('// $mysqli->close();', "بستن اتصال."),
"select_db": ('// $mysqli->select_db("shop");', "انتخاب دیتابیس."),
"set_charset": ('// $mysqli->set_charset("utf8mb4");', "کاراکترست فارسی."),
"commit": ('// $mysqli->commit();', "ثبت تراکنش."),
"rollback": ('// $mysqli->rollback();', "برگشت تراکنش."),
"autocommit": ('// $mysqli->autocommit(false);', "تراکنش دستی."),
"ping": ('// $mysqli->ping();', "آیا اتصال زنده است."),
"header": ('header("Location: /home.php");\nexit;', "ریدایرکت. باید قبل از هر خروجی باشد."),
"headers_sent": ('var_dump(headers_sent());', "آیا قبلاً خروجی رفته؟"),
"http_response_code": ('http_response_code(404);', "کد وضعیت HTTP."),
"setcookie": ('setcookie("t", "1", time()+3600, "/");', "کوکی یک‌ساعته."),
"checkdnsrr": ('// var_dump(checkdnsrr("example.com", "MX"));', "آیا رکورد DNS هست."),
"gethostbyname": ('echo gethostbyname("localhost");', "نام به IP."),
"fsockopen": ('// fsockopen("example.com", 80);', "سوکت TCP."),
"ob_start": ('ob_start();\necho "x";\n$s = ob_get_clean();\necho strtoupper($s);', "خروجی را در بافر بگیر بعد استفاده کن."),
"ob_get_contents": ('ob_start(); echo "hi"; echo ob_get_contents(); ob_end_clean();', "محتوای بافر بدون پاک کردن."),
"ob_end_flush": ('ob_start(); echo "a"; ob_end_flush();', "بافر را بفرست و ببند."),
"preg_match": ('var_dump(preg_match("/^09\\\\d{9}$/", "09121234567"));', "موبایل ۱۱ رقمی با ۰۹."),
"preg_match_all": ('preg_match_all("/\\\\d+/", "a12b34", $m); print_r($m[0]);', "همه اعداد متن."),
"preg_replace": ('echo preg_replace("/\\\\s+/", " ", "a   b");', "فاصله‌های اضافه یکی می‌شود."),
"preg_split": ('print_r(preg_split("/,/", "a,b,c"));', "جدا کردن با الگو."),
"preg_quote": ('echo preg_quote("$5.00");', "نویسه‌های خاص الگو را امن می‌کند."),
"preg_grep": ('print_r(preg_grep("/\\\\d/", ["a","b2"]));', "اعضای آرایه که با الگو جورند."),
"simplexml_load_string": ('$x=simplexml_load_string("<a>1</a>"); echo $x;', "XML رشته."),
"simplexml_load_file": ('// $x = simplexml_load_file("a.xml");', "XML از فایل."),
"addcslashes": ('echo addcslashes("a.b", ".");', "جلوی نویسه مشخص \\ می‌گذارد."),
"addslashes": ('echo addslashes("it\'s");', "گیومه را فرار می‌دهد — برای SQL از prepare استفاده کن."),
"explode": ('print_r(explode(",", "a,b,c"));', "رشته به آرایه."),
"implode": ('echo implode("-", ["a","b"]);', "آرایه به رشته."),
"join": ('echo join(",", [1,2]);', "همان implode."),
"strlen": ('echo strlen("abc");', "طول به بایت."),
"strpos": ('echo strpos("hello", "ll");', "محل اولین پیدا."),
"stripos": ('echo stripos("Hello", "h");', "جستجو بدون حساسیت حروف."),
"str_replace": ('echo str_replace("a", "b", "a-a");', "جایگزینی."),
"str_ireplace": ('echo str_ireplace("A", "b", "a");', "جایگزینی بدون حساسیت."),
"substr": ('echo substr("abcdef", 1, 3);', "از ایندکس ۱ به طول ۳."),
"trim": ('echo trim("  x  ");', "فاصله دو طرف."),
"ltrim": ('echo ltrim("  x");', "فاصله چپ."),
"rtrim": ('echo rtrim("x  ");', "فاصله راست."),
"strtolower": ('echo strtolower("Ab");', "کوچک."),
"strtoupper": ('echo strtoupper("Ab");', "بزرگ."),
"ucfirst": ('echo ucfirst("ali");', "اولین حرف بزرگ."),
"ucwords": ('echo ucwords("ali reza");', "اول هر کلمه."),
"lcfirst": ('echo lcfirst("Ali");', "اولین حرف کوچک."),
"strrev": ('echo strrev("abc");', "برعکس."),
"str_repeat": ('echo str_repeat("-", 5);', "تکرار."),
"str_pad": ('echo str_pad("5", 3, "0", STR_PAD_LEFT);', "با صفر پر کن: ۰۰۵."),
"str_split": ('print_r(str_split("abc"));', "هر نویسه یک عضو."),
"chunk_split": ('echo chunk_split("abcdef", 2, "-");', "هر ۲ نویسه جدا."),
"nl2br": ('echo nl2br("a\\nb");', "خط جدید به <br>."),
"strip_tags": ('echo strip_tags("<b>hi</b>");', "حذف تگ HTML."),
"htmlspecialchars": ('echo htmlspecialchars("<b>");', "تبدیل به موجودیت HTML — برای خروجی کاربر ضروری."),
"htmlentities": ('echo htmlentities("<>&");', "تبدیل موجودیت‌های بیشتر."),
"html_entity_decode": ('echo html_entity_decode("<b>");', "برعکس entities."),
"md5": ('echo md5("x");', "هش MD5 — برای رمز عبور از password_hash استفاده کن."),
"sha1": ('echo sha1("x");', "هش SHA1 — برای پسورد مناسب نیست."),
"number_format": ('echo number_format(12345);', "جداکننده هزارگان."),
"sprintf": ('echo sprintf("%s-%02d", "A", 5);', "قالب‌بندی رشته."),
"printf": ('printf("%.2f", 3.1);', "چاپ با قالب."),
"sscanf": ('sscanf("2026-09-23", "%d-%d-%d", $y,$m,$d); echo $y;', "استخراج از روی قالب."),
"str_contains": ('echo (str_contains("hello","ell")?"yes":"no");', "آیا داخل متن هست (PHP 8)."),
"chr": ('echo chr(65);', "کد به نویسه: A."),
"ord": ('echo ord("A");', "نویسه به کد: ۶۵."),
"bin2hex": ('echo bin2hex("A");', "بایت به هگز."),
"hex2bin": ('echo hex2bin("41");', "هگز به بایت: A."),
"str_getcsv": ('print_r(str_getcsv("a,b,c"));', "یک خط CSV به آرایه."),
"wordwrap": ('echo wordwrap("hello world", 5);', "شکستن خط در عرض مشخص."),
"str_word_count": ('echo str_word_count("one two");', "تعداد کلمه."),
"strcmp": ('echo strcmp("a","b");', "مقایسه؛ منفی یعنی اولی کوچک‌تر."),
"strcasecmp": ('echo strcasecmp("A","a");', "مقایسه بدون حروف بزرگ/کوچک."),
"strstr": ('echo strstr("name@site.com", "@");', "از اولین @ تا آخر."),
"stristr": ('echo stristr("AbC", "b");', "strstr بدون حساسیت."),
"strrchr": ('echo strrchr("/a/b.txt", ".");', "از آخرین نقطه تا آخر: .txt."),
"strrpos": ('echo strrpos("ababa", "a");', "آخرین محل."),
"substr_replace": ('echo substr_replace("abcdef", "X", 2, 2);', "از ایندکس ۲ دو نویسه را X کن."),
"substr_count": ('echo substr_count("abab", "ab");', "چند بار تکرار."),
"strtr": ('echo strtr("ab", "ab", "12");', "جایگزینی نویسه به نویسه."),
"similar_text": ('similar_text("php","php3", $p); echo $p;', "درصد شباهت."),
"levenshtein": ('echo levenshtein("kitten","sitting");', "فاصله ویرایش دو کلمه."),
"soundex": ('echo soundex("Ali");', "کد تقریبی تلفظ انگلیسی."),
"parse_str": ('parse_str("a=1&b=2", $out); print_r($out);', "رشته کوئری به آرایه."),
"boolval": ('var_dump(boolval(0));', "تبدیل به بولین."),
"intval": ('echo intval("15px");', "قسمت عددی: ۱۵."),
"floatval": ('echo floatval("3.14");', "به اعشار."),
"strval": ('echo strval(10);', "به رشته."),
"gettype": ('echo gettype([]);', "نام نوع."),
"settype": ('$x="1"; settype($x, "int"); var_dump($x);', "تغییر نوع خود متغیر."),
"empty": ('var_dump(empty(""));', "خالی؟"),
"isset": ('$a=1; var_dump(isset($a, $b));', "تعریف شده و null نیست؟"),
"unset": ('$a=1; unset($a);', "حذف متغیر."),
"is_array": ('var_dump(is_array([]));', "آرایه است؟"),
"is_string": ('var_dump(is_string("a"));', "رشته است؟"),
"is_int": ('var_dump(is_int(1));', "صحیح است؟"),
"is_float": ('var_dump(is_float(1.2));', "اعشار است؟"),
"is_bool": ('var_dump(is_bool(true));', "بولین است؟"),
"is_null": ('var_dump(is_null(null));', "تهی است؟"),
"is_numeric": ('var_dump(is_numeric("3.2"));', "عددی است حتی اگر رشته باشد؟"),
"is_object": ('var_dump(is_object(new stdClass()));', "شیء است؟"),
"is_callable": ('var_dump(is_callable("strlen"));', "قابل صدا زدن است؟"),
"is_iterable": ('var_dump(is_iterable([1]));', "قابل foreach است؟"),
"is_countable": ('var_dump(is_countable([1]));', "count رویش مجاز است؟"),
"print_r": ('print_r([1,2]);', "نمایش خوانا برای انسان."),
"var_dump": ('var_dump(1, "a");', "نوع و مقدار دقیق — برای دیباگ."),
"var_export": ('echo var_export(["a"=>1], true);', "کد PHP معتبر از مقدار."),
"serialize": ('echo serialize(["a"=>1]);', "مقدار به رشته قابل ذخیره."),
"unserialize": ('print_r(unserialize(\'a:1:{s:1:"a";i:1;}\'));', "برگشت از serialize — فقط داده خودت."),
"print": ('print "سلام";', "چاپ؛ مقدار ۱ برمی‌گرداند."),
"echo": ('echo "سلام", " ", "دنیا";', "چاپ یک یا چند مقدار."),
"and": ('var_dump(true and false);', "و منطقی با اولویت پایین‌تر از &&."),
"or": ('var_dump(false or true);', "یا منطقی."),
"xor": ('var_dump(true xor true);', "یا انحصاری: فقط یکی درست."),
"clone": ('$a = new stdClass(); $a->x=1; $b=clone $a;', "کپی شیء."),
"new": ('$o = new DateTime(); echo $o->format("Y");', "ساخت نمونه از کلاس."),
"instanceof": ('var_dump((new DateTime()) instanceof DateTime);', "آیا شیء از این کلاس است."),
"require": ('// require "config.php";', "اگر فایل نباشد اسکریپت می‌ایستد."),
"include": ('// include "view.php";', "اگر نباشد هشدار و ادامه."),
"require_once": ('// require_once "lib.php";', "فقط یک‌بار."),
"include_once": ('// include_once "lib.php";', "فقط یک‌بار با هشدار اگر نبود."),
"global": ('$x=1; function f(){ global $x; echo $x; } f();', "دیدن متغیر سراسری داخل تابع."),
"return": ('function add($a,$b){ return $a+$b; } echo add(1,2);', "برگرداندن نتیجه از تابع."),
"yield": ('function gen(){ yield 1; yield 2; } foreach(gen() as $v) echo $v;', "مولد: مقادیر را یکی‌یکی می‌دهد."),
"throw": ('// throw new InvalidArgumentException("بد");', "پرتاب استثنا."),
"try": ('try { 1/0; } catch (DivisionByZeroError $e) { echo "تقسیم بر صفر"; }', "گرفتن خطا."),
"finally": ('try {} finally { echo "همیشه"; }', "حتی بعد از catch اجرا می‌شود."),
"use": ('// use App\\User;', "وارد کردن کلاس از namespace."),
"namespace": ('namespace App;', "اعلام فضای نام فایل."),
"interface": ('interface A { public function f(); }', "قرارداد متدها."),
"trait": ('trait T { function f(){} } class C { use T; }', "کد مشترک بین کلاس‌ها."),
"abstract": ('abstract class A { abstract function f(); }', "نمی‌شود new کرد."),
"final": ('final class A {}', "نمی‌شود از آن ارث برد."),
"static": ('class A { static function f(){ return 1; } } echo A::f();', "بدون شیء."),
"public": ('class A { public $x = 1; }', "قابل دسترس از بیرون."),
"private": ('class A { private $x; }', "فقط داخل همان کلاس."),
"protected": ('class A { protected $x; }', "کلاس و فرزندان."),
"function": ('function hi(){ echo "hi"; } hi();', "تعریف تابع."),
"fn": ('$f = fn($x) => $x*2; echo $f(3);', "تابع پیکانی کوتاه."),
"class": ('class A {} $o = new A();', "تعریف کلاس."),
"extends": ('class B extends A {}', "ارث‌بری."),
"implements": ('class C implements I {}', "پیاده‌سازی رابط."),
"if": ('if (1 === 1) echo "بله";', "شرط."),
"else": ('if (false) {} else echo "وگرنه";', "مسیر دیگر."),
"elseif": ('if(false){} elseif(true) echo "این";', "شرط بعدی."),
"switch": ('switch(1){ case 1: echo "یک"; break; }', "چند حالت."),
"case": ('switch("a"){ case "a": echo "A"; }', "یک حالت."),
"default": ('switch(0){ default: echo "هیچ"; }', "اگر هیچ case نبود."),
"break": ('for($i=0;$i<5;$i++){ if($i==2) break; }', "خروج از حلقه."),
"continue": ('for($i=0;$i<3;$i++){ if($i==1) continue; echo $i; }', "رد کردن این دور."),
"while": ('$i=0; while($i<2){ echo $i; $i++; }', "تا وقتی شرط."),
"do": ('$i=0; do { echo $i; $i++; } while($i<2);', "حداقل یک‌بار."),
"for": ('for($i=0;$i<2;$i++) echo $i;', "حلقه شمارنده."),
"foreach": ('foreach([1,2] as $v) echo $v;', "روی آرایه."),
"as": ('foreach(["a"=>1] as $k => $v) echo $k;', "کلید و مقدار."),
"catch": ('try{throw new Exception("e");}catch(Exception $e){ echo $e->getMessage(); }', "گرفتن استثنا."),
"const": ('const Z = 3; echo Z;', "ثابت."),
"var": ('class A { var $x = 1; }', "قدیمی؛ معادل public."),
"callable": ('function run(callable $f){ $f(); } run(function(){ echo "ok"; });', "نوع پارامتر: قابل صدا."),
"declare": ('declare(strict_types=1);', "حالت سخت‌گیر نوع در فایل."),
"and": ('var_dump(true and true);', "و."),
}

def extract_fn(title):
    m = re.search(r"\(([^)]+)\)\s*$", title)
    if not m:
        return ""
    inner = m.group(1).strip()
    inner = inner.replace("()", "")
    return inner

def make_generic(title):
    short = title.split("(")[0].strip()
    fn = extract_fn(title)
    key = fn if fn in FN else None
    if key is None:
        # try without mysqli prefix issues
        for k in FN:
            if k.lower() == fn.lower() or k == fn.replace("()", ""):
                key = k
                break
    if key:
        code, line = FN[key]
        if not code.strip().startswith("<?php") and not code.strip().startswith("#") and not code.strip().startswith("//") and not code.strip().startswith("<"):
            code = "<?php\n" + code + "\n?>"
        what = short + " چیست و چه کارایی‌هایی دارد؟ " + line
        where = "وقتی در PHP به «" + short + "» نیاز داری؛ در پروژه واقعی با داده کوچک تمرین کن."
        lines = [line, "مثال را در فایل .php با سرور محلی اجرا کن.", "یک ورودی را عوض کن و خروجی را ببین."]
        return lesson(title, what, where, code, lines)

    # keyword-based code
    code = '<?php\necho "موضوع: ' + short.replace('"', "") + '";\n?>'
    if "FTP" in title or fn.startswith("ftp_"):
        code = '// اتصال FTP نیاز به سرور واقعی دارد\n// ' + (fn or "ftp_connect") + "(...);"
    elif fn.startswith("xml_") or "XML" in title:
        code = '<?php\n$p = xml_parser_create();\nxml_parser_free($p);\n?>'
    elif fn.startswith("zip_"):
        code = '<?php\n// $z = zip_open("a.zip");\n// while ($e = zip_read($z)) { echo zip_entry_name($e); }\n?>'
    elif fn.startswith("libxml"):
        code = '<?php\nlibxml_use_internal_errors(true);\nlibxml_clear_errors();\n?>'
    elif fn.startswith("timezone_") or "منطقه" in title or "Timezones" in title:
        code = '<?php\necho date_default_timezone_get();\nprint_r(array_slice(timezone_identifiers_list(), 0, 5));\n?>'
    elif fn.startswith("date_") or fn in ("gmdate","idate","localtime","strftime"):
        code = '<?php\necho date("c");\n?>'
    elif fn.startswith("cal_") or "JD" in title or "ژول" in title:
        code = '<?php\necho cal_days_in_month(CAL_GREGORIAN, 9, 2026);\n?>'
    elif fn.startswith("mysqli") or fn in ("errno","error","info","init","kill","options","poll","refresh","stat"):
        code = '<?php\n// $mysqli = new mysqli("localhost","root","","test");\n// echo $mysqli->' + (fn or "error") + ';\n?>'
    elif "ob_" in fn:
        code = '<?php\nob_start();\necho "بافر";\necho ob_get_clean();\n?>'

    what = short + " چیست و چه کارایی‌هایی دارد؟ این درس «" + short + "» را در PHP ساده آموزش می‌دهد."
    where = "وقتی در پروژه به این قابلیت می‌رسی. اول مثال کوچک، بعد در فرم یا فایل واقعی."
    lines = [
        "موضوع این درس: " + short + ((" — تابع " + fn) if fn else "") + ".",
        "کد را روی سرور محلی اجرا کن نه با دوبار کلیک فایل.",
        "اگر خطا دیدی پیام را از آخر بخوان؛ معمولاً نام تابع یا تعداد آرگومان را می‌گوید.",
    ]
    return lesson(title, what, where, code, lines)

php = []
seen = set()
for t in TITLES:
    if t in seen:
        t = t + " "
    seen.add(t)
    if t.strip() in CORE:
        what, where, code, lines = CORE[t.strip()]
        php.append(lesson(t.strip(), what if "چیست" in what else (t.split("(")[0].strip() + " چیست و چه کارایی‌هایی دارد؟ " + what), where, code, lines))
    else:
        php.append(make_generic(t.strip()))

print("PHP lessons", len(php), "from titles", len(TITLES))
data["php"] = php

# rebuild html
style_m = re.search(r"<style>(.*?)</style>", src, re.S)
STYLE = style_m.group(1)
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
<p>هر درس: چیست و کارایی · کاربرد واقعی · مثال · توضیح خط‌به‌خط</p>
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
<footer>توضیح مفید · مثال واقعی · بدون حاشیه</footer>
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
out = "/workspace/artifacts/madrase-complete.html"
open(out, "w", encoding="utf-8").write(doc)
import shutil
shutil.copy(out, "/workspace/artifacts/madrase-test.html")
print("WROTE", len(doc.encode()), "php", len(php))
for k,v in data.items():
    print(k, len(v))

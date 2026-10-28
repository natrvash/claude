# راهنمای نصب هوم‌پیج جدید natrvash.com روی Squarespace

**Navid Atrvash × Ava Izadpanah** · Squarespace 7.1 · پلن Business

## داخل این پوشه

| فایل | کجا می‌رود |
|---|---|
| `custom.css` | Website › Pages › Website Tools › Custom Code › **Custom CSS** |
| `code-injection-footer.html` | Website › Pages › Website Tools › Custom Code › **Code Injection › Footer** |
| `blocks/1-hero-code-block.html` | یک **Code Block** در بخش اول صفحه (ویدیو) |
| `blocks/3-about-code-block.html` | یک **Code Block** در بخش سوم صفحه (About) |
| `assets/na-sign-black.png` | لوگوی هدر |
| `assets/na-sign-magenta.png` | لوگوی فوتر |
| `assets/na-sign-white.png` | برای جاهای دیگر (روی پس‌زمینه‌ی تیره) |
| `na-hero-01.mp4` … `na-hero-10.mp4` | فایل zip جدا: ۱۰ کلیپ صفحه‌ی اول |

> تمام کدها فقط روی صفحه‌ای فعال می‌شوند که Code Block ویدیو (بخش اول) را داشته باشد. صفحه‌های دیگر دست نمی‌خورند. تنها استثنا **هدر** است. هدر در Squarespace بین همه‌ی صفحه‌ها مشترک است، پس ظاهر جدیدش (سفید، فقط ساین، منوی همبرگری) روی کل سایت اعمال می‌شود.

---

## ۰. قبل از شروع: یک نسخه‌ی تستی

برای اینکه سایت فعلی وسط کار به‌هم نریزد، روی کپی کار کن:

1. **Website › Pages**: روی صفحه‌ی **Portfolio** بزن، آیکون چرخ‌دنده، بعد **Duplicate**.
2. اسم کپی را بگذار **Home New**. این کپی همان گالری Masonry فعلی را دارد که بخش چهارم (آخر) صفحه‌ی جدید می‌شود.
3. **Home New** را به قسمت **Not Linked** ببر تا در منو دیده نشود.

---

## ۱. آپلود فایل‌ها در فضای خود سایت

Squarespace فایل‌ها را از طریق لینک آپلود می‌کند و برای هر فایل یک آدرس روی دامنه‌ی خودت می‌سازد، مثل `natrvash.com/s/na-hero-01.mp4`.

1. در هر صفحه‌ای یک Text Block موقت بساز و یک کلمه بنویس.
2. کلمه را انتخاب کن، آیکون **Link** را بزن، بعد **File** و **Upload File**.
3. این فایل‌ها را یکی‌یکی آپلود کن. **اسم فایل‌ها را عوض نکن**، چون کد با همین اسم‌ها کار می‌کند:
   - `na-hero-01.mp4` تا `na-hero-10.mp4`
   - `na-duo.jpg` (عکس دونفره)
   - `na-pub-1.jpg`، `na-pub-2.jpg`، `na-pub-3.jpg` (اسکرین‌شات پروژه‌های منتشرشده، هر وقت آماده شد)
4. بعد از آپلود، Text Block موقت را پاک کن. فایل‌ها در فضای سایت می‌مانند.

---

## ۲. هدر (Edit Site Header)

روی هدر سایت بزن و **Edit Site Header** را باز کن:

1. **Layout**: چیدمانی که منو فقط به‌صورت آیکون همبرگری سمت راست است (لوگو سمت چپ).
2. **Style**:
   - **Solid** را انتخاب کن.
   - پس‌زمینه: **White**.
   - رنگ منو: **Black**.
   - **Transparent Header** را خاموش کن.
3. **Fixed Position**: روشن، با حالت **Basic**.
4. **Mobile Styles › Menu Icon**: آیکون سه‌خطی، نه بعلاوه (+).
5. **Logo**:
   - برای **Logo** و **Mobile Logo** فایل `na-sign-black.png` را آپلود کن.
   - **Site Title** را خاموش کن.

نوار مگنتای سمت چپ، ارتفاع ۴۴ پیکسلی و پنل کوچک منو را CSS می‌سازد (مرحله‌ی ۶).

---

## ۳. ساختن صفحه‌ی Home New (چهار بخش، از بالا به پایین)

### بخش ۱: ویدیو
1. **Add Section** › یک بخش خالی (Blank). آن را به **بالای** صفحه ببر.
2. داخلش یک **Code Block** بگذار و تمام محتوای `blocks/1-hero-code-block.html` را در آن paste کن.
3. **Section Theme**: Black. ارتفاع بخش مهم نیست، CSS آن را تمام‌صفحه می‌کند.

**انتخاب ترتیب ویدیوها** (فقط همین یک خط بالای Code Block را عوض کن):
```
data-mode="shuffle"              همه تصادفی، هر بار از یک کلیپ متفاوت
data-mode="fixed"                دقیقاً به ترتیب لیست
data-mode="first-then-shuffle"   اول چند کلیپ اولِ لیست به ترتیب، بعد بقیه تصادفی
data-first="2"                   تعداد کلیپ‌های اول، برای first-then-shuffle
```
- **عوض کردن ترتیب:** خط‌های `<li>` را جابجا کن.
- **اضافه کردن ویدیو:** یک خط `<li>/s/اسم-فایل.mp4</li>` اضافه کن.
- **حذف ویدیو:** خطش را پاک کن.

### بخش ۲: عکاسی (گالری خود Squarespace)
1. **Add Section** › **Gallery** › **Slideshow: Simple**.
2. **Edit Section** › **Design**:
   - **Controls**: Side
   - **Thumbnails**: خاموش
   - **Captions**: روشن
   - **Transition**: Fade (یا هر چه دوست داری)
   - **Autoplay**: دلخواه
3. **Section Theme**: White.
4. **Edit Gallery**: عکس‌ها را اضافه، حذف یا جابجا کن. اسم پروژه را در **کپشن** هر عکس بنویس. سایت خودش جلویش «Project : » و زیرش خط مگنتا می‌گذارد.

> عوض کردن آلبوم یعنی فقط عوض کردن عکس‌های همین گالری. هیچ کدی لازم نیست.

### بخش ۳: About
1. **Add Section** › Blank › یک **Code Block**.
2. محتوای `blocks/3-about-code-block.html` را paste کن.
3. فقط متن‌های داخل `[ ... ]` و لینک‌ها (`href="..."`) را عوض کن:
   - معرفی، ایمیل، تلفن و اینستاگرام نوید و آوا
   - جایزه‌ها: هر مسابقه در هر سال یک بلوک `<div class="na-org">` است (سال و اسم مسابقه در `<h3>`). برای جایزه‌ی جدید یک خط `<li>` را کپی کن: `<b>`رتبه، `<i>`اسم پروژه، `<span>`دسته. برای مسابقه‌ی جدید کل بلوک `na-org` را کپی کن.
   - پروژه‌های منتشرشده: برای هر کدام یک `<a>`، با لینک مقاله و اسکرین‌شات

### بخش ۴: Portfolio
گالری **Masonry** فعلی (همان که از Portfolio کپی شد) را **پایین‌ترین** بخش نگه دار. عکس‌ها و تنظیماتش مثل قبل در دست خودت است.

---

## ۴. فوتر (Edit Site Footer)

فوتر هم بین همه‌ی صفحه‌ها مشترک است. در آن بگذار:
1. یک **Image Block** با `na-sign-magenta.png` (کوچک، حدود ۳۰ پیکسل).
2. یک **Text Block**: `© 2026 · All rights reserved`
3. یک **Social Links Block**. لینک‌ها را در **Settings › Social Links** اضافه کن: Instagram، YouTube، Behance، Telegram و WhatsApp. برای واتساپ، لینک `https://wa.me/` و بعدش شماره با کد کشور (بدون + و صفر) را بگذار.
4. **Section Theme**: Black.

---

## ۵. فونت (اختیاری)

برای هم‌خوانی کامل با برند، در **Site Styles › Fonts** فونت متن را **Source Sans** بگذار. متن‌های Code Blockها خودشان Source Sans 3 را بارگذاری می‌کنند.

---

## ۶. CSS

**Website › Pages › Website Tools › Custom Code › Custom CSS**: تمام محتوای `custom.css` را paste کن و **Save** بزن.

## ۷. Code Injection

**Website › Pages › Website Tools › Custom Code › Code Injection**: تمام محتوای `code-injection-footer.html` را در کادر **Footer** paste کن و **Save** بزن.

> افکت‌ها (قاب مگنتا، زوم، پخش ویدیوها، کادر پرسپکتیو، ظاهر شدن هدر) در **ویرایشگر** Squarespace اجرا نمی‌شوند. برای دیدنشان صفحه را در **Preview** یا در یک تب جدا باز کن.

---

## ۸. تست و جایگزینی

1. صفحه‌ی **Home New** را روی دسکتاپ و گوشی باز کن و بررسی کن:
   - ویدیوها پخش می‌شوند.
   - قاب مگنتا و زوم درست کار می‌کنند.
   - اسکرول صفحه‌به‌صفحه است.
   - هدر با اسکرول ظاهر می‌شود.
   - منو باز و بسته می‌شود.
2. وقتی همه‌چیز درست بود: آیکون چرخ‌دنده‌ی **Home New** › **Set as Homepage**. بعد آن را از Not Linked به منو برگردان (به اسم Portfolio یا هر اسمی که می‌خواهی) و صفحه‌ی Portfolio قدیمی را بردار.

---

## چیزی خراب شد؟

- **ویدیو پخش نمی‌شود:** اسم فایل آپلودشده باید دقیقاً با خط `<li>` یکی باشد. آدرس `natrvash.com/s/na-hero-01.mp4` را در مرورگر باز کن. باید ویدیو را نشان دهد.
- **هدر هنوز مشکی است یا منو کامل باز است:** تنظیمات مرحله‌ی ۲ را دوباره چک کن، به‌خصوص Solid، White و خاموش بودن Transparent.
- **همه‌ی افکت‌ها را خاموش کن:** کادر Code Injection › Footer را خالی کن. صفحه با ظاهر ساده سر جایش می‌ماند.

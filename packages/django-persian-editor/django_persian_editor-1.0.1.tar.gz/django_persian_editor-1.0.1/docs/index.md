# مستندات ویرایشگر فارسی برای جنگو

<div dir="rtl" align="center">
  <h2>ویرایشگر متن پیشرفته فارسی برای جنگو</h2>
</div>

## معرفی

ویرایشگر فارسی یک کتابخانه جنگو است که یک ویرایشگر متن غنی (WYSIWYG) با پشتیبانی کامل از زبان فارسی و قابلیت‌های پیشرفته ارائه می‌دهد. این ویرایشگر برای استفاده در وب‌سایت‌ها و اپلیکیشن‌های جنگو که نیاز به ویرایش متن فارسی دارند، طراحی شده است.

## نصب

### پیش‌نیازها

- پایتون 3.8 یا بالاتر
- جنگو 3.2 یا بالاتر

### نصب با pip

```bash
pip install django-persian-editor
```

### پیکربندی

1. **اضافه کردن به INSTALLED_APPS**

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'persian_editor',
    # ...
]
```

2. **اضافه کردن URL‌ها**

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    # ...
    path('persian-editor/', include('persian_editor.urls')),
    # ...
]
```

3. **تنظیمات رسانه (Media)**

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

```python
# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

4. **اجرای مایگریشن‌ها**

```bash
python manage.py migrate
```

## استفاده

### در فرم‌ها

```python
from django import forms
from persian_editor.widgets import PersianEditorWidget

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=PersianEditorWidget())
```

### در مدل‌ها

```python
from django.db import models
from persian_editor.fields import PersianEditorField

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = PersianEditorField()
```

### در ادمین جنگو

```python
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
```

## تنظیمات

### تنظیمات پیش‌فرض

می‌توانید تنظیمات پیش‌فرض ویرایشگر را در فایل `settings.py` خود تغییر دهید:

```python
# تنظیمات ویرایشگر فارسی
PERSIAN_EDITOR_CONFIG = {
    'height': '400px',
    'toolbar_buttons': [
        'bold', 'italic', 'underline', 'strikeThrough',
        'justifyRight', 'justifyCenter', 'justifyLeft', 'justifyFull',
        'insertUnorderedList', 'insertOrderedList',
        'link', 'image', 'table', 'html', 'fullscreen'
    ],
    'enable_sound': True,
    'enable_autosave': True,
    'autosave_interval': 60000,  # میلی‌ثانیه
    'enable_dark_mode': True,
    'default_direction': 'rtl',
    'upload_image_path': 'persian_editor/uploads/',
}
```

### شخصی‌سازی ویجت

می‌توانید تنظیمات را به صورت موردی برای هر ویجت تغییر دهید:

```python
from persian_editor.widgets import PersianEditorWidget

content = forms.CharField(
    widget=PersianEditorWidget(
        config={
            'height': '300px',
            'enable_sound': False,
            'toolbar_buttons': ['bold', 'italic', 'link']
        }
    )
)
```

## ویژگی‌های امنیتی

### پاکسازی HTML

برای جلوگیری از حملات XSS، ویرایشگر فارسی به طور خودکار محتوای HTML را پاکسازی می‌کند:

```python
from persian_editor.security import clean_html

# پاکسازی محتوای HTML
cleaned_content = clean_html(content)
```

### امنیت آپلود فایل

برای اطمینان از امنیت آپلود فایل‌ها، ویرایشگر فارسی از بررسی‌های امنیتی زیر استفاده می‌کند:

```python
from persian_editor.security import validate_image_file

# بررسی امنیتی فایل تصویر
validate_image_file(uploaded_file)
```

### هدرهای امنیتی

برای بهبود امنیت، ویرایشگر فارسی هدرهای امنیتی مانند Content-Security-Policy را اضافه می‌کند:

```python
# اضافه کردن میدل‌ور امنیتی
MIDDLEWARE = [
    # ...
    'persian_editor.middleware.SecurityHeadersMiddleware',
    # ...
]
```

## API جاوااسکریپت

ویرایشگر فارسی دارای API جاوااسکریپت قدرتمندی است که می‌توانید از آن برای تعامل با ویرایشگر استفاده کنید:

```javascript
// دسترسی به نمونه ویرایشگر
const editor = PersianEditor.getInstance('element_id');

// دریافت محتوا
const content = editor.getContent();

// تنظیم محتوا
editor.setContent('<p>محتوای جدید</p>');

// افزودن محتوا به انتهای متن
editor.appendContent('<p>متن اضافه شده</p>');

// پاک کردن محتوا
editor.clear();

// فعال/غیرفعال کردن ویرایشگر
editor.enable();
editor.disable();

// گوش دادن به رویدادها
editor.on('change', function(content) {
    console.log('محتوا تغییر کرد:', content);
});

editor.on('focus', function() {
    console.log('ویرایشگر فوکوس شد');
});

editor.on('blur', function() {
    console.log('ویرایشگر فوکوس را از دست داد');
});
```

## حالت تاریک

ویرایشگر فارسی به طور خودکار از حالت تاریک پشتیبانی می‌کند و با تنظیمات سیستم کاربر هماهنگ می‌شود. این ویژگی با استفاده از media query در CSS پیاده‌سازی شده است:

```css
@media (prefers-color-scheme: dark) {
    .persian-editor {
        background-color: #2d2d2d;
        color: #f0f0f0;
    }
    
    .persian-editor-toolbar {
        background-color: #333;
        border-color: #444;
    }
}
```

## واکنش‌گرایی

ویرایشگر فارسی برای استفاده در دستگاه‌های موبایل بهینه‌سازی شده است:

```css
@media (max-width: 768px) {
    .persian-editor-toolbar {
        flex-wrap: wrap;
    }
    
    .persian-editor-toolbar button {
        padding: 6px;
    }
}
```

## عیب‌یابی

### مشکل: تصاویر آپلود نمی‌شوند

اطمینان حاصل کنید که:
1. تنظیمات `MEDIA_URL` و `MEDIA_ROOT` به درستی پیکربندی شده‌اند
2. URL‌های استاتیک به درستی در `urls.py` تعریف شده‌اند
3. دسترسی‌های لازم برای پوشه‌ی `media` وجود دارد

### مشکل: ویرایشگر در ادمین نمایش داده نمی‌شود

اطمینان حاصل کنید که:
1. `persian_editor` در `INSTALLED_APPS` قرار دارد
2. از `PersianEditorField` در مدل استفاده کرده‌اید
3. فایل‌های استاتیک به درستی جمع‌آوری شده‌اند (`python manage.py collectstatic`)

## مشارکت

از مشارکت شما در توسعه ویرایشگر فارسی استقبال می‌کنیم! برای مشارکت، به فایل [CONTRIBUTING.md](../CONTRIBUTING.md) مراجعه کنید.

## مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای اطلاعات بیشتر، به فایل [LICENSE](../LICENSE) مراجعه کنید.

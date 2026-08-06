# برنامج إدارة المهام (Django)

تطبيق ويب بسيط لإدارة المهام مبني بـ Django، بواجهة قوالب تقليدية (بدون تسجيل دخول، مستخدم واحد).

## المزايا
- إضافة مهمة جديدة (عنوان + وصف اختياري)
- تعديل مهمة موجودة
- حذف مهمة
- تعليم المهمة كمكتملة / إلغاء ذلك
- عرض إحصائيات سريعة (الإجمالي، المكتملة، المتبقية)
- واجهة عربية بالكامل (RTL) باستخدام Bootstrap 5

## هيكل المشروع
```
taskmanager_project/
├── manage.py
├── requirements.txt
├── taskmanager/          # إعدادات المشروع
│   ├── settings.py
│   └── urls.py
└── tasks/                # تطبيق المهام
    ├── models.py         # نموذج Task
    ├── forms.py          # نموذج الإدخال
    ├── views.py           # المنطق (CRUD)
    ├── urls.py
    ├── admin.py
    ├── templates/tasks/  # القوالب (list, form, base)
    └── static/tasks/     # ملف CSS
```

## طريقة التشغيل

1. **تثبيت المتطلبات** (يفضل داخل بيئة افتراضية):
   ```bash
   python -m venv venv
   source venv/bin/activate      # على Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **إنشاء قاعدة البيانات (SQLite تُنشأ تلقائيًا)**:
   ```bash
   python manage.py migrate
   ```

3. **تشغيل الخادم**:
   ```bash
   python manage.py runserver
   ```

4. افتح المتصفح على: http://127.0.0.1:8000/

## لوحة تحكم الأدمن (اختياري)
لإدارة المهام من لوحة تحكم Django الجاهزة:
```bash
python manage.py createsuperuser
```
ثم افتح: http://127.0.0.1:8000/admin/

## رفع المشروع على GitHub

```bash
cd taskmanager_project
git init
git add .
git commit -m "أول نسخة من مشروع إدارة المهام"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git push -u origin main
```

> ملاحظة: ملف `.gitignore` جاهز بالفعل، فمش هيترفع `db.sqlite3` ولا مجلدات `__pycache__` ولا البيئة الافتراضية.

## تشغيله فعليًا (Deployment)

**GitHub نفسه بيخزّن الكود فقط، مش سيرفر بيشغّل تطبيقات Backend.** يعني لو حد فتح الرابط بتاع الـ repo هيشوف الكود بس، مش هيلاقي موقع شغال. عشان يشتغل فعليًا على الإنترنت، عندك خيارين:

1. **استضافة مجانية سهلة** (الأنسب للمبتدئين): [Render](https://render.com) أو [Railway](https://railway.app) أو [PythonAnywhere](https://www.pythonanywhere.com) — بتوصل بالـ GitHub repo مباشرة وتشغّله تلقائيًا.
2. **GitHub Codespaces**: لتجربة سريعة داخل المتصفح بدون تثبيت أي حاجة على جهازك (مناسب للتطوير/التجربة، مش للنشر العام).

لو حابب أجهزلك المشروع تحديدًا لاستضافة معينة (Render مثلًا، وهو الأسهل والمجاني)، قولي وأضيف ملفات الإعداد المطلوبة (زي `Procfile` و `gunicorn`).

## النشر على Azure App Service

المشروع جاهز للنشر على Azure مع ملف `.github/workflows/azure-deploy.yml` (بيبني وينشر تلقائيًا مع كل push على `main`).

### الخطوات

1. **أنشئ Azure App Service**:
   - من [Azure Portal](https://portal.azure.com) → Create a resource → Web App
   - اختر **Runtime stack: Python 3.12**
   - اختر **Publish: Code**، ونوع Linux

2. **نزّل ملف الـ Publish Profile**:
   - من صفحة الـ App Service اللي أنشأتها → **Overview** → زرار **Download publish profile**

3. **أضف الملف كـ Secret في GitHub**:
   - في الـ repo بتاعك → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
   - الاسم: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - القيمة: محتوى ملف الـ publish profile اللي نزلته (افتحه بأي محرر نصوص وانسخ كل المحتوى)

4. **عدّل اسم التطبيق في ملف الـ workflow**:
   - افتح `.github/workflows/azure-deploy.yml`
   - غيّر `your-app-name` لاسم الـ App Service الحقيقي بتاعك

5. **اضبط متغيرات البيئة على Azure** (Configuration → Application settings):
   - `SECRET_KEY` = قيمة عشوائية قوية (استخدم [هذا المولّد](https://djecrety.ir) مثلًا)
   - `DEBUG` = `False`
   - `SCM_DO_BUILD_DURING_DEPLOYMENT` = `true`

6. **اضبط أمر التشغيل (Startup Command)** في Configuration → General settings → Startup Command:
   ```
   gunicorn --bind=0.0.0.0 --timeout 600 taskmanager.wsgi:application
   ```

7. **ادفع الكود** لـ `main` وتابع تقدم النشر من تبويب **Actions** في الـ repo.

> ملاحظة: قاعدة البيانات SQLite على Azure App Service **مؤقتة وممكن تتمسح** عند إعادة تشغيل التطبيق. لو المشروع هيستخدم فعليًا، الأفضل تستخدم **Azure Database for PostgreSQL** بدل SQLite.

## أفكار للتوسعة لاحقًا
- إضافة تصنيفات/أولويات وتواريخ استحقاق
- نظام مستخدمين متعدد (كل مستخدم يرى مهامه فقط)
- فلترة وبحث في المهام
- تحويل الواجهة إلى REST API (باستخدام Django REST Framework)

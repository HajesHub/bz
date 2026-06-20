# 📱 دليل بناء APK - حاسبة المحمودية

> **ملاحظة مهمة:** Buildozer لا يعمل على Windows مباشرةً.
> يجب استخدام إحدى الطرق الثلاث التالية.

---

## 🥇 الطريقة الأولى (الأسهل): WSL2 على Windows

### الخطوة 1: تثبيت WSL2 + Ubuntu
افتح PowerShell كـ Administrator وشغّل:
```powershell
wsl --install -d Ubuntu-22.04
```
بعد الانتهاء أعد تشغيل الجهاز، ثم افتح **Ubuntu** من قائمة Start.

---

### الخطوة 2: تثبيت التبعيات داخل Ubuntu
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    git zip unzip python3-pip python3-setuptools \
    libssl-dev libffi-dev build-essential \
    libltdl-dev libpq-dev default-jdk \
    autoconf libtool pkg-config cmake \
    libncurses5:i386 libstdc++6:i386 libgtk2.0-0:i386 \
    openjdk-17-jdk

pip3 install --user buildozer cython==0.29.37
```

---

### الخطوة 3: الانتقال إلى مجلد المشروع
```bash
# المسار في WSL2 يكون هكذا:
cd /mnt/e/msharea/تطبيقات\ الجوال/
```

---

### الخطوة 4: تنفيذ أمر البناء 🚀
```bash
buildozer android debug
```
> ⏳ **الوقت المتوقع:** 20-60 دقيقة في أول مرة (تحميل Android SDK/NDK)
> في المرات التالية: 5-10 دقائق فقط

---

### الخطوة 5: موقع ملف APK
بعد انتهاء البناء، ستجد الملف في:
```
E:\msharea\تطبيقات الجوال\bin\
```
الاسم سيكون على صورة:
```
mahmoudia_calc-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

---

## 🐳 الطريقة الثانية: Docker Desktop

### المتطلب الأساسي
- تثبيت [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### الأمر (افتحه في PowerShell من مجلد المشروع)
```powershell
docker run --rm -v "${PWD}:/home/user/hostcwd" `
    kivy/buildozer android debug
```
> ✅ لا حاجة لتثبيت أي شيء آخر - Docker يتكفل بكل شيء

---

## ☁️ الطريقة الثالثة: GitHub Actions (بناء سحابي مجاني)

أنشئ ملف `.github/workflows/build.yml` بالمحتوى التالي:
```yaml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install buildozer cython==0.29.37
          sudo apt-get install -y \
            zip unzip libssl-dev libffi-dev \
            build-essential libltdl-dev default-jdk
      - name: Build APK
        run: buildozer android debug
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: AlMahmoudia-APK
          path: bin/*.apk
```

---

## 📂 هيكل الملفات النهائي

```
تطبيقات الجوال/
├── AlMahmoudia_Calc.html   ← الحاسبة (مضمّنة في APK)
├── main.py                  ← محرك Kivy
├── buildozer.spec           ← إعدادات البناء
├── BUILD_GUIDE.md           ← هذا الدليل
└── bin/
    └── mahmoudia_calc-1.0-...-debug.apk  ← الناتج النهائي
```

---

## 🔍 استكشاف الأخطاء الشائعة

| الخطأ | الحل |
|-------|------|
| `SDK license not accepted` | تأكد من وجود `android.accept_sdk_license = True` في spec |
| `Java not found` | `sudo apt install default-jdk` |
| `Cython version error` | `pip install cython==0.29.37` |
| `Permission denied` | أعد تشغيل الأمر بـ `sudo` |

---

## 📲 نقل APK عبر تيليجرام

بعد الانتهاء:
1. افتح مجلد `bin\` في Windows Explorer
2. ابحث عن الملف المنتهي بـ `.apk`
3. أرسله مباشرة عبر تيليجرام (Telegram) كملف

---

*تم إنشاء هذا الدليل لتطبيق حاسبة المحمودية - مزرعة المحمودية © 2025*

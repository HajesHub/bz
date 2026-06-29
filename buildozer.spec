[app]

# ═══════════════════════════════════════════════════════
#  معلومات التطبيق الأساسية
# ═══════════════════════════════════════════════════════
title = AlMahmoudia
package.name = mahmoudia_calc
package.domain = org.almahmoudia
version = 1.0

# ═══════════════════════════════════════════════════════
#  الملفات المصدرية
# ═══════════════════════════════════════════════════════
source.dir = .
source.include_exts = py,png,jpg,jpeg,gif,ttf,kv,json,html,js,css
source.include_patterns = AlMahmoudia_Calc.html

# ملفات يجب استبعادها لتقليل حجم الـ APK
source.exclude_dirs = tests, bin, .buildozer, __pycache__
source.exclude_exts = spec

# ═══════════════════════════════════════════════════════
#  التبعيات
# ═══════════════════════════════════════════════════════
requirements = python3,kivy,pyjnius

# ═══════════════════════════════════════════════════════
#  واجهة المستخدم
# ═══════════════════════════════════════════════════════
orientation = portrait
fullscreen = 1

# ═══════════════════════════════════════════════════════
#  إعدادات أندرويد
# ═══════════════════════════════════════════════════════
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# الحد الأدنى لإصدار أندرويد المستهدف (Android 7+)
android.minapi = 24
android.api = 33
android.ndk = 25b

# SDK & NDK
android.accept_sdk_license = True

# Architecture - arm64 is standard for all modern devices
android.archs = arm64-v8a

# ── وضع النشاط ────────────────────────────────────────
android.entrypoint = org.kivy.android.PythonActivity

# ── إعدادات gradle ────────────────────────────────────
android.gradle_dependencies =

# السماح بـ Backup لبيانات التطبيق
android.allow_backup = True

# السماح بـ hardware acceleration
android.manifest.application_attributes = android:usesCleartextTraffic="true" android:hardwareAccelerated="true"

# ═══════════════════════════════════════════════════════
#  Buildozer
# ═══════════════════════════════════════════════════════
log_level = 2
warn_on_root = 1

[buildozer]
# مجلد مؤقت لملفات البناء
build_dir = ./.buildozer

# مجلد الناتج النهائي (ملف APK)
bin_dir = ./bin

"""
AlMahmoudia Calc - Android APK Entry Point
حاسبة المحمودية - نقطة الدخول للتطبيق الأندرويد
"""

import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

# ─── تحقق من بيئة التشغيل ───────────────────────────────────────────
try:
    from android.runnable import run_on_ui_thread
    from jnius import autoclass, cast
    ANDROID = True
except ImportError:
    ANDROID = False




# ════════════════════════════════════════════════════════════════════
#  Android WebView Wrapper
# ════════════════════════════════════════════════════════════════════
if ANDROID:
    # Java classes
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    WebView        = autoclass('android.webkit.WebView')
    WebViewClient  = autoclass('android.webkit.WebViewClient')
    View           = autoclass('android.view.View')
    WebSettings    = autoclass('android.webkit.WebSettings')
    # نستخدم FrameLayout$LayoutParams بدلاً من ViewGroup$LayoutParams لأن الأندرويد يحتاج MarginLayoutParams وتجنباً لـ ClassCastException
    LayoutParams   = autoclass('android.widget.FrameLayout$LayoutParams')

    class AndroidWebView(Widget):
        """Widget يلف Android WebView Native"""

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self._webview = None
            self._setup_webview()

        @run_on_ui_thread
        def _setup_webview(self):
            """إعداد WebView وتحميل صفحة HTML المحلية"""
            activity = PythonActivity.mActivity
            context  = activity.getApplicationContext()

            # إنشاء WebView
            wv = WebView(context)
            self._webview = wv

            # ─── إعدادات WebSettings ──────────────────────────────
            settings = wv.getSettings()
            settings.setJavaScriptEnabled(True)          # تفعيل JavaScript
            settings.setDomStorageEnabled(True)           # DOM Storage
            settings.setAllowFileAccess(True)             # الوصول للملفات المحلية
            settings.setAllowContentAccess(True)          # الوصول للمحتوى
            settings.setAllowFileAccessFromFileURLs(True) # JS يقرأ ملفات محلية
            settings.setAllowUniversalAccessFromFileURLs(True)
            
            settings.setUseWideViewPort(True)             # ملء العرض
            settings.setLoadWithOverviewMode(True)        # نظرة عامة
            settings.setBuiltInZoomControls(False)        # تعطيل ازرار التكبير
            settings.setDisplayZoomControls(False)
            settings.setSupportZoom(True)                 # السماح بالـ Pinch-to-zoom
            settings.setTextZoom(100)                     # حجم النص الافتراضي
            settings.setCacheMode(WebSettings.LOAD_DEFAULT)
            settings.setMediaPlaybackRequiresUserGesture(False)

            # ─── WebViewClient (يمنع فتح المتصفح الخارجي) ────────
            wv.setWebViewClient(WebViewClient())

            # ─── شاشة كاملة ───────────────────────────────────────
            params = LayoutParams(
                LayoutParams.MATCH_PARENT,
                LayoutParams.MATCH_PARENT
            )
            wv.setLayoutParams(params)

            # ─── إخفاء شريط النظام لتجربة Immersive ──────────────
            decorView = activity.getWindow().getDecorView()
            visibility = (
                View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
            )
            decorView.setSystemUiVisibility(visibility)

            # ─── تحديد مسار ملف HTML وتشغيله ──────────────────────
            # ملفات Kivy يتم فك ضغطها ووضعها بجوار main.py، وليس في مجلد assets الداخلي مباشرة
            current_dir = os.path.dirname(os.path.abspath(__file__))
            html_path = os.path.join(current_dir, 'AlMahmoudia_Calc.html')
            
            html_url = 'file://' + html_path
            wv.loadUrl(html_url)

            # إضافة WebView إلى layout النشاط
            activity.addContentView(wv, params)

        def on_size(self, *args):
            if self._webview:
                self._resize_webview()

        @run_on_ui_thread
        def _resize_webview(self):
            if self._webview:
                params = LayoutParams(
                    LayoutParams.MATCH_PARENT,
                    LayoutParams.MATCH_PARENT
                )
                self._webview.setLayoutParams(params)


# ════════════════════════════════════════════════════════════════════
#  Fallback Desktop Preview (للاختبار على الكمبيوتر)
# ════════════════════════════════════════════════════════════════════
else:
    from kivy.uix.label import Label
    from kivy.graphics import Color, Rectangle

    class AndroidWebView(Widget):
        """محاكي بسيط لاختبار الهيكل على سطح المكتب"""
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            with self.canvas:
                Color(0.06, 0.17, 0.37, 1)  # لون الـ header - #0f2b5e
                self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_rect, size=self._update_rect)

            lbl = Label(
                text='[b]حاسبة المحمودية[/b]\n\nسيتم تحميل الحاسبة عند تثبيتها على الأندرويد',
                markup=True,
                font_size='18sp',
                color=(1, 1, 1, 1),
                halign='center',
                valign='middle'
            )
            self.add_widget(lbl)

        def _update_rect(self, *args):
            self.rect.pos  = self.pos
            self.rect.size = self.size


# ════════════════════════════════════════════════════════════════════
#  Kivy Application
# ════════════════════════════════════════════════════════════════════
class AlMahmoudiaApp(App):
    """التطبيق الرئيسي - حاسبة المحمودية"""

    def build(self):
        self.title = 'AlMahmoudia'
        return AndroidWebView()

    def on_pause(self):
        return True   # السماح بالتوقف المؤقت

    def on_resume(self):
        pass


if __name__ == '__main__':
    AlMahmoudiaApp().run()

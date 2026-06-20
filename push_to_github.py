"""
سكريبت رفع ملفات AlMahmoudia إلى GitHub
يستخدم فقط مكتبات Python المدمجة - لا تثبيت لأي شيء
"""

import urllib.request
import urllib.error
import json
import base64
import os

# ─── الإعدادات ────────────────────────────────────────────────────
TOKEN   = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
REPO    = "bz"
API     = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Python",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github.v3+json"
}

# ─── الملفات المطلوب رفعها ─────────────────────────────────────────
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = [
    "AlMahmoudia_Calc.html",
    "main.py",
    "buildozer.spec",
    ".github/workflows/build.yml",
]

# ══════════════════════════════════════════════════════════════════
def api_request(url, data=None, method=None):
    """إرسال طلب لـ GitHub API"""
    body = json.dumps(data).encode() if data else None
    req  = urllib.request.Request(url, data=body, headers=HEADERS,
                                   method=method or ("PUT" if body else "GET"))
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read()), res.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read()), e.code

def get_user():
    """جلب اسم المستخدم"""
    data, code = api_request(f"{API}/user")
    if code == 200:
        print(f"Success: Welcome {data['login']}!")
        return data['login']
    print(f"Error checking token: {code}")
    return None

def create_repo(username):
    """إنشاء المستودع - يتجاوز إذا كان موجوداً"""
    # تحقق إذا كان المستودع موجوداً
    data, code = api_request(f"{API}/repos/{username}/{REPO}")
    if code == 200:
        print(f"Repo exists info: {data['html_url']}")
        return data['html_url']

    # إنشاء مستودع جديد
    payload = {
        "name": REPO,
        "description": "حاسبة المحمودية - Android APK",
        "private": False,
        "auto_init": False
    }
    data, code = api_request(f"{API}/user/repos", data=payload, method="POST")
    if code in (201, 200):
        print(f"Success: Repo created: {data['html_url']}")
        return data['html_url']
    print(f"Error creating repo: {code} - {data}")
    return None

def upload_file(username, file_rel_path):
    """رفع ملف واحد إلى GitHub"""
    local_path = os.path.join(PROJECT_DIR, file_rel_path.replace("/", os.sep))

    if not os.path.exists(local_path):
        print(f"  Warning: File not found: {local_path}")
        return False

    with open(local_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()

    # تحقق إذا كان الملف موجوداً (للحصول على SHA للتحديث)
    url   = f"{API}/repos/{username}/{REPO}/contents/{file_rel_path}"
    existing, code = api_request(url)
    sha   = existing.get("sha") if code == 200 else None

    payload = {
        "message": f"Add {os.path.basename(file_rel_path)}",
        "content": content_b64,
    }
    if sha:
        payload["sha"] = sha

    _, code = api_request(url, data=payload, method="PUT")
    if code in (200, 201):
        print(f"  Done: {file_rel_path}")
        return True
    print(f"  Error: Failed to upload {file_rel_path} - Code: {code}")
    return False

# ══════════════════════════════════════════════════════════════════
def main():
    print("=" * 50)
    print("   رفع حاسبة المحمودية إلى GitHub")
    print("=" * 50)

    # 1. التحقق من المستخدم
    username = get_user()
    if not username:
        return

    # 2. المستودع موجود مسبقاً
    repo_url = f"https://github.com/{username}/{REPO}"
    print(f"Uploading to: {repo_url}")

    # 3. رفع الملفات
    print("\nUploading files...")
    success = 0
    for f in FILES:
        if upload_file(username, f):
            success += 1

    # 4. النتيجة النهائية
    print(f"\n{'=' * 50}")
    print(f"Success: Upload complete: {success}/{len(FILES)} files")
    print(f"Link: {repo_url}")
    print(f"Actions link:  {repo_url}/actions")
    print(f"{'=' * 50}")
    print("\nStarting build automatically in 1 minute...")
    print("Download APK from Actions > Artifacts in 30-40 minutes.")

if __name__ == "__main__":
    main()

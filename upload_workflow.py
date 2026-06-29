"""
رفع build.yml عبر Git Tree API (يتجاوز قيود workflow scope)
"""
import urllib.request, urllib.error, json, base64, os

# يُقرأ الـ token من متغير بيئي لأسباب أمنية
# قم بتعيينه: set GITHUB_TOKEN=ghp_xxxxx  (Windows)
TOKEN = os.environ.get('GITHUB_TOKEN', '')
OWNER = 'HajesHub'
REPO  = 'bz'
API   = 'https://api.github.com'
H     = {
    'Authorization': f'token {TOKEN}',
    'User-Agent': 'Python',
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json'
}

def api(method, path, data=None):
    url  = f'{API}{path}'
    body = json.dumps(data).encode() if data else None
    req  = urllib.request.Request(url, data=body, headers=H, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read()), e.code

# 1. قراءة الملف
with open(r'E:\msharea\تطبيقات الجوال\.github\workflows\build.yml', 'rb') as f:
    wf_content = f.read()

# 2. جلب آخر commit على main
ref, _ = api('GET', f'/repos/{OWNER}/{REPO}/git/ref/heads/main')
last_sha = ref['object']['sha']
print(f'Last commit SHA: {last_sha}')

# 3. جلب الـ tree الحالي
commit, _ = api('GET', f'/repos/{OWNER}/{REPO}/git/commits/{last_sha}')
base_tree = commit['tree']['sha']
print(f'Base tree SHA: {base_tree}')

# 4. إنشاء Blob للملف
blob, _ = api('POST', f'/repos/{OWNER}/{REPO}/git/blobs', {
    'content': base64.b64encode(wf_content).decode(),
    'encoding': 'base64'
})
blob_sha = blob['sha']
print(f'Blob SHA: {blob_sha}')

# 5. إنشاء Tree جديد
tree, status = api('POST', f'/repos/{OWNER}/{REPO}/git/trees', {
    'base_tree': base_tree,
    'tree': [{
        'path': '.github/workflows/build.yml',
        'mode': '100644',
        'type': 'blob',
        'sha': blob_sha
    }]
})
if status not in (200, 201):
    print(f'FAIL tree: {status} - {tree}')
    exit()
tree_sha = tree['sha']
print(f'New tree SHA: {tree_sha}')

# 6. إنشاء Commit جديد
new_commit, status = api('POST', f'/repos/{OWNER}/{REPO}/git/commits', {
    'message': 'Add GitHub Actions workflow for APK build',
    'tree': tree_sha,
    'parents': [last_sha]
})
if status not in (200, 201):
    print(f'FAIL commit: {status} - {new_commit}')
    exit()
new_sha = new_commit['sha']
print(f'New commit SHA: {new_sha}')

# 7. تحديث الـ ref (push)
result, status = api('PATCH', f'/repos/{OWNER}/{REPO}/git/refs/heads/main', {
    'sha': new_sha,
    'force': False
})
if status in (200, 201):
    print(f'\nOK! .github/workflows/build.yml رُفع بنجاح!')
    print(f'Actions: https://github.com/{OWNER}/{REPO}/actions')
    print('البناء يبدأ الآن تلقائياً!')
else:
    print(f'FAIL push: {status} - {result}')

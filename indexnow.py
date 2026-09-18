"""公開後に sitemap.xml の全 URL を IndexNow（Bing 等）へ送信する。GitHub Actions の deploy 後に実行。"""
import json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))
base = CONFIG["base_url"].rstrip("/")
host = base.split("//", 1)[1].split("/", 1)[0]
key = open(os.path.join(ROOT, ".indexnow_key"), encoding="utf-8").read().strip()

sitemap = urllib.request.urlopen(f"{base}/sitemap.xml", timeout=30).read().decode("utf-8")
urls = re.findall(r"<loc>(.*?)</loc>", sitemap)
if not urls:
    sys.exit("sitemap に URL がありません")
payload = {"host": host, "key": key, "keyLocation": f"{base}/{key}.txt", "urlList": urls[:10000]}
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8"},
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow", r.status, len(urls), "urls")
except urllib.error.HTTPError as e:
    print("IndexNow HTTP", e.code, e.read().decode("utf-8", "ignore")[:300])

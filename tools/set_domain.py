#!/usr/bin/env python3
"""Replace the placeholder domain everywhere. Usage:  python3 tools/set_domain.py https://www.yourdomain.com"""
import sys, os, glob
if len(sys.argv) != 2 or not sys.argv[1].startswith("http"):
    sys.exit("Usage: python3 tools/set_domain.py https://www.yourdomain.com")
new = sys.argv[1].rstrip("/")
old = "https://YOUR-DOMAIN.com"
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = 0
for pattern in ("*.html", "*.xml", "*.txt", "js/site-config.js", "tools/generate.py"):
    for f in glob.glob(os.path.join(root, pattern)):
        s = open(f, encoding="utf-8").read()
        if old in s:
            open(f, "w", encoding="utf-8").write(s.replace(old, new)); n += 1
print(f"Updated {n} files to {new}")

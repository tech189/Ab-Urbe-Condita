#!/usr/local/bin/python3
import datetime
import subprocess
import urllib.request
import json



time = datetime.datetime.now()
romanjson = json.loads(urllib.request.urlopen("https://www.tech189.duckdns.org/auc?json=true").read().decode("utf-8"))

print(time.strftime("%a %-d %b"))
print("---")
print(time.strftime("%A, %-d %B %Y| href=\"https://github.com/tech189/Ab-Urbe-Condita\""))
print(romanjson["roman"]["time"] + "| href=\"https://github.com/tech189/Ab-Urbe-Condita\"")
print(romanjson["roman"]["day"] + "| href=\"https://github.com/tech189/Ab-Urbe-Condita\"")
print(romanjson["roman"]["date"] + "| href=\"https://github.com/tech189/Ab-Urbe-Condita\"")
print(romanjson["roman"]["year"] + "| href=\"https://github.com/tech189/Ab-Urbe-Condita\"")
print("---")
print("About")
print("--Ab Urbe Condita (click for info)| href=\"https://github.com/tech189/Ab-Urbe-Condita\"")
print("--Made by tech189")
print("--Written in Python")
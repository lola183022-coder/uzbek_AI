
[app]
title = OzbekAI 10.0 ULTIMATE
package.name = ozbekai
package.domain = uz.ozbekai
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 10.0
requirements = python3,kivy,requests,pyjnius
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[android]
android.permissions = INTERNET,RECORD_AUDIO
android.api = 35
android.minapi = 23
android.accept_sdk_license = True

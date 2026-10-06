[app]

title = Veljano
package.name = veljano
package.domain = org.veljano

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt
source.exclude_dirs = .git,.github,__pycache__,bin,.buildozer,venv,.venv,dist

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

android.permissions = INTERNET

android.debug_artifact = True
android.release_artifact = apk

[buildozer]

log_level = 2
warn_on_root = 1

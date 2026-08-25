[app]
title = Road Combat
package.name = roadcombat
package.domain = org.josscreations
source.dir = .
source.exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,pygame,sdl2_image,sdl2_mixer,sdl2_ttf,sdl2
orientation = portrait
fullscreen = 1
android.permissions = WAKE_LOCK
android.api = 31
android.minapi = 21
android.ndk = 23b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.skip_update = False

[buildozer]
log_level = 2
warn_on_root = 1

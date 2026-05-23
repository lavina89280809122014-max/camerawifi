[app]

# (str) Title of your application
title = Камера WiFi

# (str) Package name
package.name = camerawifi

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (source.dir) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy,android

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions needed
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 23b

# (bool) Copy library templates into the libs_collections directory
android.copy_libs = 1

# (str) The Android arch to build for
android.archs = arm64-v8a,armeabi-v7a

# (bool) enable AndroidX support
android.enable_androidx = True

# (list) Pattern to whitelist
android.whitelist = lib-dynload/termios.so

# (bool) enables Android auto backup feature
android.allow_backup = True

# (bool) Indicate that the application should use cleartext traffic
android.usesCleartextTraffic = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warnings (1) or not (0)
warn_on_root = 1

# (str) Path to build artifact storage
build_dir = .buildozer

# (str) Path to build output
bin_dir = ./bin

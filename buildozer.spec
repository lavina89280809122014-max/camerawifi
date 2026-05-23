[app]

# (str) Title of your application
title = Камера

# (str) Package name
package.name = cameraapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (source.dir) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,android,pyjnius

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash of the application (image or drawable resource string).
# presplash.filename = %(source.dir)s/data/presplash.png

# (list) Permissions
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 23b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library templates into the libs_collections directory
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) Indicate that the application should use the SecureRandom.getInstance("SHA1PRNG")
#android.use_sha1 = False

# (bool) enable AndroidX support
android.enable_androidx = True

# (list) Pattern to whitelist for the whole project
android.whitelist = lib-dynload/termios.so

# (str) Path to a Java keystore containing a private key and certificate for signing your application.
# This requires jarsigner, and keytool from the jdk to sign in debug mode with the given alias.
# OUPUT FILENAME CONVENTION : {keystore}__{alias}.keystore
# the last part is ".keystore" because ANDROID_KEYSTORE environment variable needs it.
#android.keystore_path = my-release-key.keystore

# (str) Alias to use when signing; android.keystore_alias = myalias

# (passfile) Filename for the keystore password. For example, to use the environment
# variable KEYSTORE_PASS you can use either method1 (dynamic path) or method2 (env var referenced as a string).
# (str) should be dollar-delimited, e.g. $KEYSTORE_PASS
# or you can fallback on a (filename) mode, e.g. seek my.keystore_pass file in the project.
# android.keystore_alias_password = $KEYSTORE_ALIAS_PASS

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching with *.
# OUPUT FILENAME CONVENTION :
#android.add_src =

# (list) List of Java files to add to the libs sources so that pyjnius can access
# their classes. Don't add files that you do not exclude, since the extra files can
# slow down the build process.
#android.add_src =

# (bool) Copy library templates into the libs_collections directory
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
#android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup scheme, see the documentation for details.
# android.backup_policies =

# (bool) Indicate that the application should use cleartext traffic
#android.usesCleartextTraffic = False

# (bool) Copies user library to the application libs directory when user_private_storage is True
#android.copy_libs_src = True

# (str) modules used from python-for-android
# python for android is a project to compile python for android
# android.p4a_options = --use-legacy-toolchain

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warnings (1) or not (0)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file.
build_dir = .buildozer

# (str) Path to build output (i.e. where the built APK will be).
# This is only used if not invoked from the command line ourselves.
bin_dir = ./bin

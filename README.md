android_onscreenbutton_enabler
==============================

Enables NavigationBar for Android >=4.0 by patching framework-res.apk

    usage: patch-framework.py [-h] [-d] [-w WIDTH] [-s HEIGHT]
                              [-sl HEIGHT_LANDSCAPE]
                              framework frameworkNew

    enable/disable NavigationBar and change their size.

    positional arguments:
      framework
      frameworkNew

    optional arguments:
      -h, --help            show this help message and exit
      -d                    Disable NavigationBar instead of enabling
      -w WIDTH              Set NavigationBar-width to WIDTH
      -s HEIGHT             Set NavigationBar-height to HEIGHT
      -sl HEIGHT_LANDSCAPE  Set NavigationBar-height to HEIGHT_LANDSCAPE
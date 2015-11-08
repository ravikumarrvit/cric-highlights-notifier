import platform

from MacNotifier import MacNotifier

class PlatformDetector:

    def get_platform_notifier(self):

        plat_name = platform.platform()

        if plat_name.startswith("Darwin"):
            return MacNotifier()
        elif plat_name.startswith("Linux"):
            pass
        elif plat_name.startswith("Windows"):
            pass
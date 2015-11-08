from Foundation import NSUserNotification
from Foundation import NSUserNotificationCenter
from Foundation import NSUserNotificationDefaultSoundName

class MacNotifier:

    def notify(self, title, message, sound):

        notification = NSUserNotification.alloc().init()
        notification.setTitle_(title)
        notification.setInformativeText_(message)
        if sound:
            notification.setSoundName_(NSUserNotificationDefaultSoundName)

        center = NSUserNotificationCenter.defaultUserNotificationCenter()
        center.deliverNotification_(notification)
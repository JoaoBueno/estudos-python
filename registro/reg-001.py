from winreg import *
key = OpenKey(HKEY_LOCAL_MACHINE, r'Software\Microsoft\Outlook Express', 0, KEY_ALL_ACCESS)
QueryValueEx(key, "InstallRoot")
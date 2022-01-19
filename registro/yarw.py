from winreg import EnumKey, HKEY_USERS
 
try:
    i = 0
    while True:
        subkey = EnumKey(HKEY_USERS, i)
        print(subkey)
        i += 1
except WindowsError:
    # WindowsError: [Errno 259] No more data is available    
    pass

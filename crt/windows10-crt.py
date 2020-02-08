def _windows_write_string(s, out):
    """ Returns True if the string was written using special methods,
    False if it has yet to be written out."""
    # Adapted from http://stackoverflow.com/a/3259271/35070
    # https://github.com/ytdl-org/youtube-dl/issues/15758

    from ctypes import byref, POINTER, windll, WINFUNCTYPE
    from ctypes.wintypes import BOOL, DWORD, HANDLE, LPWSTR, LPVOID

    FILE_TYPE_CHAR = 0x0002
    FILE_TYPE_REMOTE = 0x8000
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

    GetStdHandle = compat_ctypes_WINFUNCTYPE(
        HANDLE,
        DWORD)(('GetStdHandle', windll.kernel32))

    GetFileType = compat_ctypes_WINFUNCTYPE(
        DWORD,
        HANDLE)(('GetFileType', windll.kernel32))

    GetConsoleMode = compat_ctypes_WINFUNCTYPE(
        BOOL,
        HANDLE,
        POINTER(DWORD))(('GetConsoleMode', windll.kernel32))

    SetConsoleMode = compat_ctypes_WINFUNCTYPE(
        BOOL,
        HANDLE,
        DWORD)(('SetConsoleMode', windll.kernel32))

    WriteConsoleW = compat_ctypes_WINFUNCTYPE(
        BOOL,
        HANDLE,
        LPWSTR,
        DWORD,
        POINTER(DWORD),
        LPVOID)(('WriteConsoleW', windll.kernel32))

    try:
        fileno = out.fileno()
    except AttributeError:
        # If the output stream doesn't have a fileno, it's virtual
        return False
    except io.UnsupportedOperation:
        # Some strange Windows pseudo files?
        return False

    if fileno == 1:
        h = GetStdHandle(-11)
    elif fileno == 2:
        h = GetStdHandle(-12)
    else:
        return False

    if h is None or h == HANDLE(-1):
        return False

    if (GetFileType(h) & ~FILE_TYPE_REMOTE) != FILE_TYPE_CHAR:
        return False

    mode = DWORD()
    if not GetConsoleMode(h, byref(mode)):
        return False

    if (mode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING) == 0:
        SetConsoleMode(h, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)

    def next_nonbmp_pos(s):
        try:
            return next(i for i, c in enumerate(s) if ord(c) > 0xffff)
        except StopIteration:
            return len(s)

    written = DWORD(0)
    while s:
        count = min(next_nonbmp_pos(s), 1024)

        ret = WriteConsoleW(
            h, s, count if count else 2, byref(written), None)
        if ret == 0:
            raise OSError('Failed to write string')
        if not count:  # We just wrote a non-BMP character
            assert written.value == 2
            s = s[1:]
        else:
            assert written.value > 0
            s = s[written.value:]
    return True


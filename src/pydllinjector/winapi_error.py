import ctypes


def LPVOID_errcheck(result, func, args):
    if not result:
        raise ctypes.WinError()
    return result


def Win32API_errcheck(result, func, args):
    if not result:
        raise ctypes.WinError()

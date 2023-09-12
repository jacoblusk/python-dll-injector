from ctypes.wintypes import *
from pydllinjector.wintypes_extended import *
from pydllinjector.winapi_error import *

import ctypes
import enum


class OpenFileNameFlags(enum.IntFlag):
    PATHMUSTEXIST = 0x00000800
    FILEMUSTEXIST = 0x00001000


class OPENFILENAMEA(ctypes.Structure):
    _fields_ = [
        ("lStructSize", DWORD),
        ("hwndOwner", HWND),
        ("hInstance", HINSTANCE),
        ("lpstrFilter", LPCSTR),
        ("lpstrCustomFilter", LPSTR),
        ("nMaxCustFilter", DWORD),
        ("nFilterIndex", DWORD),
        ("lpstrFile", LPSTR),
        ("nMaxFile", DWORD),
        ("lpstrFileTitle", LPSTR),
        ("nMaxFileTitle", DWORD),
        ("lpstrInitialDir", LPCSTR),
        ("lpstrTitle", LPCSTR),
        ("Flags", DWORD),
        ("nFileOffset", WORD),
        ("nFileExtension", WORD),
        ("lpstrDefExt", LPCSTR),
        ("lCustData", LPARAM),
        ("lpfnHook", ctypes.c_void_p),
        ("lpTemplateName", LPCSTR),
        ("pvReserved", ctypes.c_void_p),
        ("dwReserved", DWORD),
        ("FlagsEx", DWORD),
    ]


LPOPENFILENAMEA = ctypes.POINTER(OPENFILENAMEA)

GetOpenFileNameA = ctypes.windll.comdlg32.GetOpenFileNameA
GetOpenFileNameA.argtypes = [LPOPENFILENAMEA]
GetOpenFileNameA.restype = BOOL

CommDlgExtendedError = ctypes.windll.comdlg32.CommDlgExtendedError
CommDlgExtendedError.argtypes = None
CommDlgExtendedError.restype = DWORD

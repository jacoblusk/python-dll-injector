from ctypes.wintypes import *
from pydllinjector.wintypes_extended import *
from pydllinjector.winapi_error import *

import ctypes
import enum

MAX_PATH = 260
CW_USEDEFAULT = 0x80000000


def MAKELONG(wLow, wHigh):
    return ctypes.c_long(wLow | wHigh << 16)


def MAKELPARAM(l, h):
    return LPARAM(MAKELONG(l, h).value)


def LOWORD(l):
    return WORD(l & 0xFFFF)


def HIWORD(l):
    return WORD((l >> 16) & 0xFFFF)


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", LONG),
        ("top", LONG),
        ("right", LONG),
        ("bottom", LONG),
    ]


LPRECT = ctypes.POINTER(RECT)


class ICONINFO(ctypes.Structure):
    _fields_ = [
        ("fIcon", BOOL),
        ("xHotspot", DWORD),
        ("yHotspot", DWORD),
        ("hbmMask", HBITMAP),
        ("hbmColor", HBITMAP),
    ]


PICONINFO = ctypes.POINTER(ICONINFO)


class LOGFONTA(ctypes.Structure):
    LF_FACESIZE = 32
    _fields_ = [
        ("lfHeight", LONG),
        ("lfWidth", LONG),
        ("lfEscapement", LONG),
        ("lfOrientation", LONG),
        ("lfWeight", LONG),
        ("lfItalic", BYTE),
        ("lfUnderline", BYTE),
        ("lfStrikeOut", BYTE),
        ("lfCharSet", BYTE),
        ("lfOutPrecision", BYTE),
        ("lfClipPrecision", BYTE),
        ("lfQuality", BYTE),
        ("lfPitchAndFamily", BYTE),
        ("lfFaceName", CHAR * LF_FACESIZE),
    ]


LPLOGFONTA = ctypes.POINTER(LOGFONTA)


class NONCLIENTMETRICSA(ctypes.Structure):
    _fields_ = [
        ("cbSize", UINT),
        ("iBorderWidth", ctypes.c_int),
        ("iScrollWidth", ctypes.c_int),
        ("iScrollHeight", ctypes.c_int),
        ("iCaptionWidth", ctypes.c_int),
        ("iCaptionHeight", ctypes.c_int),
        ("lfCaptionFont", LOGFONTA),
        ("iSmCaptionWidth", ctypes.c_int),
        ("iSmCaptionHeight", ctypes.c_int),
        ("lfSmCaptionFont", LOGFONTA),
        ("iMenuWidth", ctypes.c_int),
        ("iMenuHeight", ctypes.c_int),
        ("lfMenuFont", LOGFONTA),
        ("lfStatusFont", LOGFONTA),
        ("lfMessageFont", LOGFONTA),
        ("iPaddedBorderWidth", ctypes.c_int),
    ]


LPNONCLIENTMETRICSA = ctypes.POINTER(NONCLIENTMETRICSA)


class POINT(ctypes.Structure):
    _fields_ = [("x", LONG), ("y", LONG)]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", HWND),
        ("message", UINT),
        ("wParam", WPARAM),
        ("lParam", LPARAM),
        ("time", DWORD),
        ("pt", POINT),
        ("lPrivate", DWORD),
    ]


LPMSG = ctypes.POINTER(MSG)


class WNDCLASSA(ctypes.Structure):
    _fields_ = [
        ("style", UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", HINSTANCE),
        ("hIcon", HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", HBRUSH),
        ("lpszMenuName", LPCSTR),
        ("lpszClassName", LPCSTR),
    ]


LPWNDCLASSA = ctypes.POINTER(WNDCLASSA)


class ShowWindowCommand(enum.IntEnum):
    HIDE = 0
    SHOW = 5
    SHOWDEFAULT = 10


class SystemParametersInfoAcessibilityParameter(enum.IntFlag):
    GETNONCLIENTMETRICS = 0x0029


class LoadImageFlags(enum.IntFlag):
    LOADFROMFILE = 0x00000010
    VGACOLOR = 0x00000080


class ClassStyle(enum.IntFlag):
    VREDRAW = 0x0001
    HREDRAW = 0x0002
    DBLCLKS = 0x0008
    OWNDC = 0x0020
    CLASSDC = 0x0040
    PARENTDC = 0x0080
    NOCLOSE = 0x0200
    SAVEBITS = 0x0800
    BYTEALIGNCLIENT = 0x1000
    BYTEALIGNWINDOW = 0x2000
    GLOBALCLASS = 0x4000


class WindowStyle(enum.IntFlag):
    BORDER = 0x00800000
    CAPTION = 0x00C00000
    CHILD = 0x40000000
    CHILDWINDOW = 0x40000000
    CLIPCHILDREN = 0x02000000
    CLIPSIBLINGS = 0x04000000
    DISABLED = 0x08000000
    DLGFRAME = 0x00400000
    GROUP = 0x00020000
    HSCROLL = 0x00100000
    ICONIC = 0x20000000
    MAXIMIZE = 0x01000000
    MAXIMIZEBOX = 0x00010000
    MINIMIZE = 0x20000000
    MINIMIZEBOX = 0x00020000
    OVERLAPPED = 0x00000000
    POPUP = 0x80000000
    SIZEBOX = 0x00040000
    SYSMENU = 0x00080000
    TABSTOP = 0x00010000
    THICKFRAME = 0x00040000
    TILED = 0x00000000
    VISIBLE = 0x10000000
    VSCROLL = 0x00200000
    LVS_EX_FULLROWSELECT = 0x00000020
    OVERLAPPEDWINDOW = (
        OVERLAPPED | CAPTION | SYSMENU | THICKFRAME | MINIMIZEBOX | MAXIMIZEBOX
    )
    TILEDWINDOW = OVERLAPPEDWINDOW
    POPUPWINDOW = POPUP | BORDER | SYSMENU


class GetWindowLong(enum.IntEnum):
    EXSTYLE = -20
    HINSTANCE = -6
    HWNDPARENT = -8
    ID = -12
    STYLE = -16
    USERDATA = -21
    WNDPROC = -4


class WindowMessage(enum.IntEnum):
    SETFOCUS = 0x0007
    KILLFOCUS = 0x0006
    ENABLE = 0x000A
    SETREDRAW = 0x000B
    SETTEXT = 0x000C
    SETFONT = 0x0030
    GETFONT = 0x0031
    GETTEXT = 0x000D
    GETTEXTLENGTH = 0x000E
    PAINT = 0x000F
    CLOSE = 0x00010
    QUIT = 0x0012
    SHOWWINDOW = 0x0018
    NULL = 0x0000
    CREATE = 0x0001
    DESTROY = 0x0002
    MOVE = 0x0003
    SIZE = 0x0005
    ACTIVATE = 0x0006
    COMMAND = 0x0111
    NOTIFY = 0x004E


class ButtonStyle(enum.IntFlag):
    PUSHBUTTON = 0x00000000
    DEFPUSHBUTTON = 0x00000001
    CHECKBOX = 0x00000002
    AUTOCHECKBOX = 0x00000003
    RADIOBUTTON = 0x00000004
    _3STATE = 0x00000005
    AUTO3STATE = 0x00000006
    GROUPBOX = 0x00000007
    USERBUTTON = 0x00000008
    AUTORADIOBUTTON = 0x00000009
    PUSHBOX = 0x0000000A
    OWNERDRAW = 0x0000000B
    TYPEMASK = 0x0000000F
    LEFTTEXT = 0x00000020
    TEXT = 0x00000000
    ICON = 0x00000040
    BITMAP = 0x00000080
    LEFT = 0x00000100
    RIGHT = 0x00000200
    CENTER = 0x00000300
    TOP = 0x00000400
    BOTTOM = 0x00000800
    VCENTER = 0x00000C00
    PUSHLIKE = 0x00001000
    MULTILINE = 0x00002000
    NOTIFY = 0x00004000
    FLAT = 0x00008000
    RIGHTBUTTON = LEFTTEXT


class ListBoxStyle(enum.IntFlag):
    NOTIFY = 0x0001
    SORT = 0x0002
    NOREDRAW = 0x0004
    MULTIPLESEL = 0x0008
    OWNERDRAWFIXED = 0x0010
    OWNERDRAWVARIABLE = 0x0020
    HASSTRINGS = 0x0040
    USETABSTOPS = 0x0080
    NOINTEGRALHEIGHT = 0x0100
    MULTICOLUMN = 0x0200
    WANTKEYBOARDINPUT = 0x0400
    EXTENDEDSEL = 0x0800
    DISABLENOSCROLL = 0x1000
    NODATA = 0x2000
    NOSEL = 0x4000
    COMBOBOX = 0x8000
    STANDARD = NOTIFY | SORT | WindowStyle.VSCROLL | WindowStyle.BORDER


GetDlgItem = ctypes.windll.user32.GetDlgItem
GetDlgItem.argtypes = [HWND, ctypes.c_int]
GetDlgItem.restype = HWND
GetDlgItem.errcheck = LPVOID_errcheck

RegisterClassA = ctypes.windll.user32.RegisterClassA
RegisterClassA.argtypes = [LPWNDCLASSA]
RegisterClassA.restype = ATOM
RegisterClassA.errcheck = LPVOID_errcheck

DefWindowProcA = ctypes.windll.user32.DefWindowProcA
DefWindowProcA.argtypes = [HWND, UINT, WPARAM, LPARAM]
DefWindowProcA.restype = LRESULT

CreateWindowExA = ctypes.windll.user32.CreateWindowExA
CreateWindowExA.argtypes = [
    DWORD,
    LPCSTR,
    LPCSTR,
    DWORD,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    HWND,
    HMENU,
    HINSTANCE,
    LPVOID,
]
CreateWindowExA.restype = HWND
CreateWindowExA.errcheck = LPVOID_errcheck

ShowWindow = ctypes.windll.user32.ShowWindow
ShowWindow.argtypes = [HWND, ctypes.c_int]
ShowWindow.restype = BOOL

GetMessageA = ctypes.windll.user32.GetMessageA
GetMessageA.argtypes = [LPMSG, HWND, UINT, UINT]
GetMessageA.restype = BOOL

TranslateMessage = ctypes.windll.user32.TranslateMessage
TranslateMessage.argtypes = [LPMSG]
TranslateMessage.restype = BOOL

DispatchMessageA = ctypes.windll.user32.DispatchMessageA
DispatchMessageA.argtypes = [LPMSG]
DispatchMessageA.restype = BOOL

PostQuitMessage = ctypes.windll.user32.PostQuitMessage
PostQuitMessage.argtypes = [ctypes.c_int]
PostQuitMessage.restype = None

DestroyWindow = ctypes.windll.user32.DestroyWindow
DestroyWindow.argtypes = [HWND]
DestroyWindow.restype = BOOL
DestroyWindow.errcheck = Win32API_errcheck

try:
    GetWindowLongPtrA = ctypes.windll.user32.GetWindowLongPtrA
except:
    GetWindowLongPtrA = ctypes.windll.user32.GetWindowLongA
GetWindowLongPtrA.argtypes = [HWND, ctypes.c_int]
GetWindowLongPtrA.restype = LONG_PTR
GetWindowLongPtrA.errcheck = LPVOID_errcheck

try:
    SetWindowLongPtrA = ctypes.windll.user32.SetWindowLongPtrA
except:
    SetWindowLongPtrA = ctypes.windll.user32.SetWindowLongA
SetWindowLongPtrA.argtypes = [HWND, ctypes.c_int, LONG_PTR]
SetWindowLongPtrA.restype = LONG_PTR
GetWindowLongPtrA.errcheck = LPVOID_errcheck

EnumChildWindows = ctypes.windll.user32.EnumChildWindows
EnumChildWindows.argtypes = [HWND, WNDENUMPROC, LPARAM]
EnumChildWindows.restype = BOOL

SystemParametersInfoA = ctypes.windll.user32.SystemParametersInfoA
SystemParametersInfoA.argtypes = [UINT, UINT, LPVOID, UINT]
SystemParametersInfoA.restype = BOOL
SystemParametersInfoA.errcheck = Win32API_errcheck

SendMessageA = ctypes.windll.user32.SendMessageA
SendMessageA.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessageA.restype = LRESULT

GetClientRect = ctypes.windll.user32.GetClientRect
GetClientRect.argtypes = [HWND, LPRECT]
GetClientRect.restype = BOOL
GetClientRect.errcheck = Win32API_errcheck

LoadImageA = ctypes.windll.user32.LoadImageA
LoadImageA.argtypes = [HINSTANCE, LPCSTR, UINT, INT, INT, UINT]
LoadImageA.restype = HANDLE
LoadImageA.errcheck = LPVOID_errcheck

LoadIconA = ctypes.windll.user32.LoadIconA
LoadIconA.argtypes = [HINSTANCE, LPCSTR]
LoadIconA.restype = HICON
LoadIconA.errcheck = LPVOID_errcheck

GetIconInfo = ctypes.windll.user32.GetIconInfo
GetIconInfo.argtypes = [HICON, PICONINFO]
GetIconInfo.restype = BOOL
GetIconInfo.errcheck = Win32API_errcheck

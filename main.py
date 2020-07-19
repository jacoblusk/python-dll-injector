from ctypes.wintypes import *

import ctypes
import enum
import os

LONG_PTR               = LPARAM
HCURSOR                = HANDLE
LRESULT                = ctypes.c_long
SIZE_T                 = ctypes.c_size_t
FARPROC                = ctypes.CFUNCTYPE(ctypes.c_int, LPVOID)
LPTHREAD_START_ROUTINE = ctypes.CFUNCTYPE(DWORD, LPVOID)
WNDPROC                = ctypes.WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)
WNDENUMPROC            = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
PFNLVCOMPARE           = ctypes.WINFUNCTYPE(ctypes.c_int, LPARAM, LPARAM, LPARAM)

INVALID_HANDLE_VALUE = -1
INFINITE             = ctypes.c_uint(-1)
MAX_PATH             = 260
CW_USEDEFAULT        = 0x80000000

INJECT_BUTTON    = 100
PROCESS_LISTVIEW = 101
SEARCH_BUTTON    = 102
FILEPATH_EDIT    = 103

def MAKELONG(wLow, wHigh):
    return ctypes.c_long(wLow | wHigh << 16)

def MAKELPARAM(l, h):
    return LPARAM(MAKELONG(l, h).value)

def LOWORD(l):
    return WORD(l & 0xFFFF)

def HIWORD(l):
    return WORD((l >> 16) & 0xFFFF)

class ListViewMessage(enum.IntEnum):
    FIRST = 0x1000
    GETITEMA    = FIRST + 5
    INSERTITEMA = FIRST + 7
    GETNEXTITEM = FIRST + 12
    GETITEMTEXTA = FIRST + 45
    INSERTITEMW = FIRST + 77
    INSERTCOLUMNA = FIRST + 27
    INSERTCOLUMNW = FIRST + 97
    SETIMAGELIST = FIRST + 3
    SETITEMTEXTA = FIRST + 46
    SETITEMTEXTW = FIRST + 116
    SORTITEMS = FIRST + 48

def ListView_InsertItemA(hwnd, pitem):
    return SendMessageA(hwnd, ListViewMessage.INSERTITEMA, WPARAM(0),
                        LPARAM(ctypes.cast(pitem, ctypes.c_void_p).value))

def ListView_InsertColumnA(hwnd, iCol, pcol):
    return SendMessageA(hwnd, ListViewMessage.INSERTCOLUMNA, WPARAM(iCol),
                        LPARAM(ctypes.cast(pcol, ctypes.c_void_p).value))

def ListView_SetImageList(hwnd, himl, iImageList):
    return ctypes.cast(
        SendMessageA(hwnd, ListViewMessage.SETIMAGELIST, WPARAM(iImageList),
                     LPARAM(ctypes.cast(himl, ctypes.c_void_p).value)),
        ctypes.c_void_p)

def ListView_GetNextItem(hwnd, i, flags):
    return SendMessageA(hwnd, ListViewMessage.GETNEXTITEM, WPARAM(i), MAKELPARAM((flags), 0))

def ListView_GetItemA(hwnd, pitem):
    return SendMessageA(hwnd, ListViewMessage.GETITEMA, WPARAM(0),
                        LPARAM(ctypes.cast(pitem, ctypes.c_void_p).value))

def ListView_GetItemTextA(hwndLV, i, iSubItem_, pszText_, cchTextMax_):
    _macro_lvi = LVITEMA()
    _macro_lvi.iSubItem = iSubItem_
    _macro_lvi.cchTextMax = cchTextMax_
    _macro_lvi.pszText = pszText_
    SendMessageA((hwndLV), ListViewMessage.GETITEMTEXTA, WPARAM(i),
                 LPARAM(ctypes.cast(ctypes.byref(_macro_lvi), ctypes.c_void_p).value))


def ListView_SetItemTextA(hwnd, i, iSubItem, pszText):
    lvitem = LVITEMA()
    lvitem.iSubItem = iSubItem
    lvitem.pszText = pszText
    SendMessageA(hwnd, ListViewMessage.SETITEMTEXTA, WPARAM(i),
                 LPARAM(ctypes.cast(ctypes.byref(lvitem), ctypes.c_void_p).value))

def ListView_SortItems(hwndLV, _pfnCompare, _lPrm): 
    return SendMessageA(hwndLV, ListViewMessage.SORTITEMS,
                        WPARAM(_lPrm),
                        LPARAM(ctypes.cast(_pfnCompare, ctypes.c_void_p).value))

def ImageList_AddIcon(himl, hicon):
    ImageList_ReplaceIcon(himl, -1, hicon)

class OPENFILENAMEA(ctypes.Structure):
    _fields_ = [
        ('lStructSize', DWORD),
        ('hwndOwner', HWND),
        ('hInstance', HINSTANCE),
        ('lpstrFilter', LPCSTR),
        ('lpstrCustomFilter', LPSTR),
        ('nMaxCustFilter', DWORD),
        ('nFilterIndex', DWORD),
        ('lpstrFile', LPSTR),
        ('nMaxFile', DWORD),
        ('lpstrFileTitle', LPSTR),
        ('nMaxFileTitle', DWORD),
        ('lpstrInitialDir', LPCSTR),
        ('lpstrTitle', LPCSTR),
        ('Flags', DWORD),
        ('nFileOffset', WORD),
        ('nFileExtension', WORD),
        ('lpstrDefExt', LPCSTR),
        ('lCustData', LPARAM),
        ('lpfnHook', ctypes.c_void_p),
        ('lpTemplateName', LPCSTR),
        ('pvReserved', ctypes.c_void_p),
        ('dwReserved', DWORD),
        ('FlagsEx', DWORD)
    ]

LPOPENFILENAMEA = ctypes.POINTER(OPENFILENAMEA)

class RECT(ctypes.Structure):
    _fields_ = [
        ('left', LONG),
        ('top', LONG),
        ('right', LONG),
        ('bottom', LONG),
    ]

LPRECT = ctypes.POINTER(RECT)

class LVITEMA(ctypes.Structure):
    _fields_ = [
        ('mask', UINT),
        ('iItem', ctypes.c_int),
        ('iSubItem', ctypes.c_int),
        ('state', UINT),
        ('stateMask', UINT),
        ('pszText', LPCSTR),
        ('cchTextMax', ctypes.c_int),
        ('iImage', ctypes.c_int),
        ('lParam', LPARAM),
        ('iIndent', ctypes.c_int),
        ('iGroupId', ctypes.c_int),
        ('cColumns', UINT),
        ('puColumns', ctypes.POINTER(UINT)),
        ('piColFmt', ctypes.POINTER(ctypes.c_int)),
        ('iGroup', ctypes.c_int)
    ]

LPLVITEMA = ctypes.POINTER(LVITEMA)

class ICONINFO(ctypes.Structure):
    _fields_ = [
        ('fIcon', BOOL),
        ('xHotspot', DWORD),
        ('yHotspot', DWORD),
        ('hbmMask', HBITMAP),
        ('hbmColor', HBITMAP),
    ]

PICONINFO = ctypes.POINTER(ICONINFO)

class NMHDR(ctypes.Structure):
    _fields_ = [
        ('hwndFrom', HWND),
        ('idFrom', ctypes.POINTER(UINT)),
        ('code', UINT)
    ]

class LV_DISPINFOA(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('item', LVITEMA)
    ]

LPLV_DISPINFOA = ctypes.POINTER(LV_DISPINFOA)

class NM_LISTVIEW(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('iItem', ctypes.c_int),
        ('iSubItem', ctypes.c_int),
        ('uNewState', UINT),
        ('uOldState', UINT),
        ('uChanged', UINT),
        ('ptAction', POINT),
        ('lParam', LPARAM ),
    ]

LPNM_LISTVIEW = ctypes.POINTER(NM_LISTVIEW)

class LVCOLUMNA(ctypes.Structure):
    _fields_ = [
        ('mask', UINT),
        ('fmt', ctypes.c_int),
        ('cx', ctypes.c_int),
        ('pszText', LPCSTR),
        ('cchTextMax', ctypes.c_int),
        ('iSubItem', ctypes.c_int),
        ('iImage', ctypes.c_int),
        ('iOrder', ctypes.c_int),
        ('cxMin', ctypes.c_int),
        ('cxDefault', ctypes.c_int),
        ('cxIdeal', ctypes.c_int),
    ]

LPLVCOLUMNA = ctypes.POINTER(LVCOLUMNA)

class LOGFONTA(ctypes.Structure):
    LF_FACESIZE = 32
    _fields_ = [
        ('lfHeight', LONG),
        ('lfWidth', LONG),
        ('lfEscapement', LONG),
        ('lfOrientation', LONG),
        ('lfWeight', LONG),
        ('lfItalic', BYTE),
        ('lfUnderline', BYTE),
        ('lfStrikeOut', BYTE),
        ('lfCharSet', BYTE),
        ('lfOutPrecision', BYTE),
        ('lfClipPrecision', BYTE),
        ('lfQuality', BYTE),
        ('lfPitchAndFamily', BYTE),
        ('lfFaceName', CHAR * LF_FACESIZE)
    ]

LPLOGFONTA = ctypes.POINTER(LOGFONTA)

class NONCLIENTMETRICSA(ctypes.Structure):
    _fields_ = [
        ('cbSize', UINT),
        ('iBorderWidth', ctypes.c_int),
        ('iScrollWidth', ctypes.c_int),
        ('iScrollHeight', ctypes.c_int),
        ('iCaptionWidth', ctypes.c_int),
        ('iCaptionHeight', ctypes.c_int),
        ('lfCaptionFont', LOGFONTA),
        ('iSmCaptionWidth', ctypes.c_int),
        ('iSmCaptionHeight', ctypes.c_int),
        ('lfSmCaptionFont', LOGFONTA),
        ('iMenuWidth', ctypes.c_int),
        ('iMenuHeight', ctypes.c_int),
        ('lfMenuFont', LOGFONTA),
        ('lfStatusFont', LOGFONTA),
        ('lfMessageFont', LOGFONTA),
        ('iPaddedBorderWidth', ctypes.c_int)
    ]

LPNONCLIENTMETRICSA = ctypes.POINTER(NONCLIENTMETRICSA)

class POINT(ctypes.Structure):
    _fields_ = [
        ('x', LONG),
        ('y', LONG)
    ]

class MSG(ctypes.Structure):
    _fields_ = [
        ('hwnd', HWND),
        ('message', UINT),
        ('wParam', WPARAM),
        ('lParam', LPARAM),
        ('time', DWORD),
        ('pt', POINT),
        ('lPrivate', DWORD)
    ]

LPMSG = ctypes.POINTER(MSG)

class WNDCLASSA(ctypes.Structure):
    _fields_ = [
        ('style', UINT),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', ctypes.c_int),
        ('cbWndExtra', ctypes.c_int),
        ('hInstance', HINSTANCE),
        ('hIcon', HICON),
        ('hCursor', HCURSOR),
        ('hbrBackground', HBRUSH),
        ('lpszMenuName', LPCSTR),
        ('lpszClassName', LPCSTR)
    ]

LPWNDCLASSA = ctypes.POINTER(WNDCLASSA)

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('cntUsage', DWORD),
        ('th32ProcessID', DWORD),
        ('th32DefaultHeapID', ctypes.POINTER(ctypes.c_ulong)),
        ('th32ModuleID', DWORD),
        ('cntThreads', DWORD),
        ('th32ParentProcessID', DWORD),
        ('pcPriClassBase', LONG),
        ('dwFlags', DWORD),
        ('szExeFile', CHAR * MAX_PATH)
    ]

LPPROCESSENTRY32 = ctypes.POINTER(PROCESSENTRY32)

class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ('nLength', DWORD),
        ('lpSecurityDescriptor', LPVOID),
        ('bInheritHandle', BOOL)
    ]

LPSECURITY_ATTRIBUTES = ctypes.POINTER(SECURITY_ATTRIBUTES)

class INITCOMMONCONTROLSEX(ctypes.Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('dwICC', DWORD)
    ]

LPINITCOMMONCONTROLSEX = ctypes.POINTER(INITCOMMONCONTROLSEX)

class Process(enum.IntFlag):
    CREATE_PROCESS            = 0x0080
    CREATE_THREAD             = 0x0002
    DUP_HANDLE                = 0x0002
    QUERY_INFORMATION         = 0x0400
    QUERY_LIMITED_INFORMATION = 0x1000
    SET_INFORMATION           = 0x0200
    SET_QUOTA                 = 0x0100
    SUSPEND_RESUME            = 0x0800
    TERMINATE                 = 0x0001
    VM_OPERATION              = 0x0008
    VM_READ                   = 0x0010
    VM_WRITE                  = 0x0020
    SYNCHRONIZE               = 0x00100000

class AllocationType(enum.IntFlag):
    COMMIT      = 0x00001000
    RESERVE     = 0x00002000
    RESET       = 0x00080000
    RESET_UNDO  = 0x1000000
    LARGE_PAGES = 0x20000000
    PHYSICAL    = 0x00400000
    TOP_DOWN    = 0x00100000

class FreeType(enum.IntFlag):
    COALESCE_PLACEHOLDERS = 0x1
    PRESERVE_PLACEHOLDER = 0x2
    DECOMMIT = 0x4000
    RELEASE = 0x8000

class PageProtection(enum.IntFlag):
    EXECUTE           = 0x10
    EXECUTE_READ      = 0x20
    EXECUTE_READWRITE = 0x40
    EXECUTE_WRITECOPY = 0x80
    NOACCESS          = 0x01
    READONLY          = 0x02
    READWRITE         = 0x04
    WRITECOPY         = 0x08
    TARGETS_INVALID   = 0x40000000
    TARGETS_NO_UPDATE = 0x40000000
    GUARD             = 0x100
    NOCACHE           = 0x200
    WRITECOMBINE      = 0x400
    # LoadEnclaveData
    # ENCLAVE_THREAD_CONTROL
    # ENCLDAVE_UNVALIDATED

class SnapshotInclude(enum.IntFlag):
    INHERIT = 0x80000000
    HEAPLIST = 0x00000001
    MODULE = 0x00000008
    MODULE32 = 0x00000010
    PROCESS = 0x00000002
    THREAD = 0x00000004
    ALL = HEAPLIST | MODULE | PROCESS | THREAD

class Wait(enum.IntEnum):
    ABANDONED = 0x00000080
    OBJECT_0  = 0x00000000
    TIMEOUT   = 0x00000102
    FAILED    = 0xFFFFFFFF

class ClassStyle(enum.IntFlag):
    VREDRAW         = 0x0001
    HREDRAW         = 0x0002
    DBLCLKS         = 0x0008
    OWNDC           = 0x0020
    CLASSDC         = 0x0040
    PARENTDC        = 0x0080
    NOCLOSE         = 0x0200
    SAVEBITS        = 0x0800
    BYTEALIGNCLIENT = 0x1000
    BYTEALIGNWINDOW = 0x2000
    GLOBALCLASS     = 0x4000

class WindowStyle(enum.IntFlag):
    BORDER = 0x00800000
    CAPTION =  0x00C00000
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
    OVERLAPPEDWINDOW = OVERLAPPED | CAPTION | SYSMENU | THICKFRAME \
                    | MINIMIZEBOX | MAXIMIZEBOX
    TILEDWINDOW = OVERLAPPEDWINDOW
    POPUPWINDOW = POPUP | BORDER | SYSMENU

class ButtonStyle(enum.IntFlag):
    PUSHBUTTON      = 0x00000000
    DEFPUSHBUTTON   = 0x00000001
    CHECKBOX        = 0x00000002
    AUTOCHECKBOX    = 0x00000003
    RADIOBUTTON     = 0x00000004
    _3STATE         = 0x00000005
    AUTO3STATE      = 0x00000006
    GROUPBOX        = 0x00000007
    USERBUTTON      = 0x00000008
    AUTORADIOBUTTON = 0x00000009
    PUSHBOX         = 0x0000000A
    OWNERDRAW       = 0x0000000B
    TYPEMASK        = 0x0000000F
    LEFTTEXT        = 0x00000020
    TEXT            = 0x00000000
    ICON            = 0x00000040
    BITMAP          = 0x00000080
    LEFT            = 0x00000100
    RIGHT           = 0x00000200
    CENTER          = 0x00000300
    TOP             = 0x00000400
    BOTTOM          = 0x00000800
    VCENTER         = 0x00000C00
    PUSHLIKE        = 0x00001000
    MULTILINE       = 0x00002000
    NOTIFY          = 0x00004000
    FLAT            = 0x00008000
    RIGHTBUTTON     = LEFTTEXT

class ListBoxStyle(enum.IntFlag):
    NOTIFY            = 0x0001
    SORT              = 0x0002
    NOREDRAW          = 0x0004
    MULTIPLESEL       = 0x0008
    OWNERDRAWFIXED    = 0x0010
    OWNERDRAWVARIABLE = 0x0020
    HASSTRINGS        = 0x0040
    USETABSTOPS       = 0x0080
    NOINTEGRALHEIGHT  = 0x0100
    MULTICOLUMN       = 0x0200
    WANTKEYBOARDINPUT = 0x0400
    EXTENDEDSEL       = 0x0800
    DISABLENOSCROLL   = 0x1000
    NODATA            = 0x2000
    NOSEL             = 0x4000
    COMBOBOX          = 0x8000
    STANDARD          = NOTIFY | SORT | WindowStyle.VSCROLL | WindowStyle.BORDER  

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

class GetWindowLong(enum.IntEnum):
    EXSTYLE = -20
    HINSTANCE = -6
    HWNDPARENT = -8
    ID = -12
    STYLE = -16
    USERDATA = -21
    WNDPROC = -4

def LPVOID_errcheck(result, func, args):
    if not result:
        raise ctypes.WinError()
    return result

def Win32API_errcheck(result, func, args):
    if not result:
        raise ctypes.WinError()

def CreateToolhelp32Snapshot_errcheck(result, func, args):
    if result == INVALID_HANDLE_VALUE:
        raise ctypes.WinError()
    return result

def WaitForSingleObject(result, func, args):
    wait_result = Wait(result)
    if wait_result == Wait.FAILED:
        raise ctypes.WinError()
    else:
        return wait_result

class InitCommonControlsExError(Exception):
    pass

def InitCommonControlsEx_errcheck(result, func, args):
    if result == 0:
        raise InitCommonControlsExError("InitCommonControlsEx failed.")
    
VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
VirtualAllocEx.argtypes = [HANDLE, LPVOID, SIZE_T, DWORD, DWORD]
VirtualAllocEx.restype = LPVOID
VirtualAllocEx.errcheck = LPVOID_errcheck

VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
VirtualFreeEx.argtypes = [HANDLE, LPVOID, SIZE_T, DWORD]
VirtualFreeEx.restype = BOOL
VirtualFreeEx.errcheck = Win32API_errcheck

WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
WriteProcessMemory.argtypes = [HANDLE, LPVOID, LPCVOID, SIZE_T, ctypes.POINTER(SIZE_T)]
WriteProcessMemory.restype = BOOL
WriteProcessMemory.errcheck = Win32API_errcheck

GetProcAddress = ctypes.windll.kernel32.GetProcAddress
GetProcAddress.argtypes = [HMODULE, LPCSTR]
GetProcAddress.restype = FARPROC

OpenProcess = ctypes.windll.kernel32.OpenProcess
OpenProcess.argtypes = [DWORD, BOOL, DWORD]
OpenProcess.restype = HANDLE
OpenProcess.errcheck = LPVOID_errcheck

GetModuleHandleA = ctypes.windll.kernel32.GetModuleHandleA
GetModuleHandleA.argtypes = [LPCSTR]
GetModuleHandleA.restype = HMODULE
GetModuleHandleA.errcheck = LPVOID_errcheck

CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.argtypes = [DWORD, DWORD]
CreateToolhelp32Snapshot.restype = HANDLE
CreateToolhelp32Snapshot.errcheck = CreateToolhelp32Snapshot_errcheck

Process32First = ctypes.windll.kernel32.Process32First
Process32First.argtypes = [HANDLE, LPPROCESSENTRY32]
Process32First.restype = BOOL

Process32Next = ctypes.windll.kernel32.Process32Next
Process32Next.argtypes = [HANDLE, LPPROCESSENTRY32]
Process32Next.restype = BOOL

CloseHandle = ctypes.windll.kernel32.CloseHandle
CloseHandle.argtypes = [HANDLE]
CloseHandle.restype = BOOL
CloseHandle.errcheck = Win32API_errcheck

CreateRemoteThread = ctypes.windll.kernel32.CreateRemoteThread
CreateRemoteThread.argtypes = [HANDLE, LPSECURITY_ATTRIBUTES, SIZE_T,
                               LPTHREAD_START_ROUTINE, LPVOID, DWORD, LPDWORD]
CreateRemoteThread.restype = HANDLE
CreateRemoteThread.errcheck = LPVOID_errcheck

WaitForSingleObject = ctypes.windll.kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = [HANDLE, DWORD]
WaitForSingleObject.restype = DWORD

GetExitCodeThread = ctypes.windll.kernel32.GetExitCodeThread
GetExitCodeThread.argtypes = [HANDLE, LPDWORD]
GetExitCodeThread.restype = BOOL
GetExitCodeThread.errcheck = Win32API_errcheck

RegisterClassA = ctypes.windll.user32.RegisterClassA
RegisterClassA.argtypes = [LPWNDCLASSA]
RegisterClassA.restype = ATOM
RegisterClassA.errcheck = LPVOID_errcheck

DefWindowProcA = ctypes.windll.user32.DefWindowProcA
DefWindowProcA.argtypes = [HWND, UINT, WPARAM, LPARAM]
DefWindowProcA.restype = LRESULT

CreateWindowExA = ctypes.windll.user32.CreateWindowExA
CreateWindowExA.argtypes = [DWORD, LPCSTR, LPCSTR, DWORD, ctypes.c_int,
                            ctypes.c_int, ctypes.c_int, ctypes.c_int,
                            HWND, HMENU, HINSTANCE, LPVOID]
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
#TranslateMessage.errcheck = Win32API_errcheck

DispatchMessageA = ctypes.windll.user32.DispatchMessageA
DispatchMessageA.argtypes = [LPMSG]
DispatchMessageA.restype = BOOL
#DispatchMessageA.errcheck = Win32API_errcheck

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

CreateFontIndirectA = ctypes.windll.gdi32.CreateFontIndirectA
CreateFontIndirectA.argtypes = [LPLOGFONTA]
CreateFontIndirectA.restype = HFONT
CreateFontIndirectA.errcheck = LPVOID_errcheck

DeleteObject = ctypes.windll.gdi32.DeleteObject
DeleteObject.argtypes = [LPVOID]
DeleteObject.restype = BOOL

SendMessageA = ctypes.windll.user32.SendMessageA
SendMessageA.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessageA.restype = LRESULT

GetStockObject = ctypes.windll.gdi32.GetStockObject
GetStockObject.argtypes = [ctypes.c_int]
GetStockObject.restype = HANDLE
GetStockObject.errcheck = LPVOID_errcheck

GetDlgItem = ctypes.windll.user32.GetDlgItem
GetDlgItem.argtypes = [HWND, ctypes.c_int]
GetDlgItem.restype = HWND
GetDlgItem.errcheck = LPVOID_errcheck

InitCommonControlsEx = ctypes.windll.comctl32.InitCommonControlsEx
InitCommonControlsEx.argtypes = [LPINITCOMMONCONTROLSEX]
InitCommonControlsEx.restype = BOOL
InitCommonControlsEx.errcheck = InitCommonControlsEx_errcheck

GetClientRect = ctypes.windll.user32.GetClientRect
GetClientRect.argtypes = [HWND, LPRECT]
GetClientRect.restype = BOOL
GetClientRect.errcheck = Win32API_errcheck

GetObjectA = ctypes.windll.gdi32.GetObjectA
GetObjectA.argtypes = [HANDLE, ctypes.c_int, LPVOID]
GetObjectA.restype = ctypes.c_int

IsWow64Process2 = ctypes.windll.kernel32.IsWow64Process2
IsWow64Process2.argtypes = [HANDLE, ctypes.POINTER(USHORT), ctypes.POINTER(USHORT)]
IsWow64Process2.restype = BOOL
IsWow64Process2.errcheck = Win32API_errcheck

GetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess
GetCurrentProcess.argtypes = None
GetCurrentProcess.restype = HANDLE

GetOpenFileNameA = ctypes.windll.comdlg32.GetOpenFileNameA
GetOpenFileNameA.argtypes = [LPOPENFILENAMEA]
GetOpenFileNameA.restype = BOOL

CommDlgExtendedError = ctypes.windll.comdlg32.CommDlgExtendedError
CommDlgExtendedError.argtypes = None
CommDlgExtendedError.restype = DWORD

ExtractIconExA = ctypes.windll.shell32.ExtractIconExA
ExtractIconExA.argtypes = [LPCSTR, ctypes.c_int, ctypes.POINTER(HICON), ctypes.POINTER(HICON), UINT]
ExtractIconExA.restype = UINT

QueryFullProcessImageNameA = ctypes.windll.kernel32.QueryFullProcessImageNameA
QueryFullProcessImageNameA.argtypes = [HANDLE, DWORD, LPSTR, PDWORD]
QueryFullProcessImageNameA.restype = BOOL
QueryFullProcessImageNameA.errcheck = Win32API_errcheck

ImageList_Create = ctypes.windll.comctl32.ImageList_Create
ImageList_Create.argtypes = [ctypes.c_int, ctypes.c_int, UINT, ctypes.c_int, ctypes.c_int]
ImageList_Create.restype = ctypes.c_void_p
ImageList_Create.errcheck = LPVOID_errcheck

ImageList_ReplaceIcon = ctypes.windll.comctl32.ImageList_ReplaceIcon
ImageList_ReplaceIcon.argtypes = [ctypes.c_void_p, ctypes.c_int, HICON]
ImageList_ReplaceIcon.restype = ctypes.c_int

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

def CreateListView(hwnd_parent, control_id, x, y, width, height, processes, icons, paths):
    ICC_LISTVIEW_CLASSES = 0x00000001
    LVS_REPORT = 0x0001
    LVS_EDITLABELS = 0x0200
    LVS_SHOWSELALWAYS = 0x0008
    
    icex = INITCOMMONCONTROLSEX()
    icex.dwSize = ctypes.sizeof(INITCOMMONCONTROLSEX)
    icex.dwICC = ICC_LISTVIEW_CLASSES
    result = InitCommonControlsEx(ctypes.byref(icex))

    hwnd_listview = CreateWindowExA(0, b"SysListView32", b"",
        WindowStyle.VISIBLE | WindowStyle.CHILD | LVS_REPORT | LVS_SHOWSELALWAYS \
        | WindowStyle.BORDER,
        x, y,
        width, height,
        hwnd_parent,
        HMENU(control_id),
        ctypes.cast(GetWindowLongPtrA(hwnd_parent, GetWindowLong.HINSTANCE), HINSTANCE),
        None
    )

    hsmall = ImageList_Create(16, 16, 0x00000020 | 0x00020000, len(processes), 0)
    hlarge = ImageList_Create(32, 32, 0x00000020 | 0x00020000, len(processes), 0)

    for i in range(len(processes)):
        if ImageList_AddIcon(hsmall, icons[i][0]) == -1 or \
           ImageList_AddIcon(hlarge, icons[i][1]) == -1:
            raise Exception("Error adding Icons.")

    ListView_SetImageList(hwnd_listview, hsmall, 1)
    ListView_SetImageList(hwnd_listview, hlarge, 0)

    column_names = [(b"Process Name", 160),
                    (b"PID", 50),
                    (b"Parent PID", 70),
                    (b"Threads", 60),
                    (b"Absolute Path", 500)]

    lvcolumn = LVCOLUMNA()
    lvcolumn.mask = 0x0001 | 0x0002 | 0x0004 | 0x0008
    lvcolumn.cx = 75
    lvcolumn.fmt = 0x0000

    for i in range(len(column_names)):
        lvcolumn.iSubItem = i
        lvcolumn.pszText = ctypes.cast(column_names[i][0], ctypes.c_char_p)
        lvcolumn.cx = column_names[i][1]
        if ListView_InsertColumnA(hwnd_listview, i, ctypes.byref(lvcolumn)) == -1:
            raise Exception("ListView_InsertColumnA")

    lvitem = LVITEMA()
    lvitem.mask = 0x00000001 | 0x00000002 | 0x00000004 | 0x00000008
    lvitem.state = 0
    lvitem.stateMask = 0

    LPSTR_TEXTCALLBACK = LPSTR(-1)
    
    for i in range(len(processes)):
        lvitem.iItem = i
        lvitem.iSubItem = 0
        lvitem.pszText = processes[i].szExeFile
        lvitem.cchTextMax = 64
        lvitem.iImage = i
        lvitem.lParam = LPARAM(ctypes.cast(ctypes.byref(processes[i]), ctypes.c_void_p).value)

        if ListView_InsertItemA(hwnd_listview, ctypes.byref(lvitem)) == -1:
            raise Exception("ListView_InsertItem")

        
        ListView_SetItemTextA(hwnd_listview, i, 1, b"%d" % processes[i].th32ProcessID)
        ListView_SetItemTextA(hwnd_listview, i, 2, b"%d" % processes[i].th32ParentProcessID)
        ListView_SetItemTextA(hwnd_listview, i, 3, b"%d" % processes[i].cntThreads)
        ListView_SetItemTextA(hwnd_listview, i, 4, ctypes.cast(paths[i], ctypes.c_char_p))
    
    return hwnd_listview, processes

def CreateButton(hwnd_parent, control_id, x, y, width, text, height=23):
    hwnd_button = CreateWindowExA(0,
        b"BUTTON",
        text,
        WindowStyle.TABSTOP | WindowStyle.VISIBLE \
        | WindowStyle.CHILD | ButtonStyle.TEXT,
        x, y,
        width, height,
        hwnd_parent, HMENU(control_id),
        ctypes.cast(GetWindowLongPtrA(hwnd_parent, GetWindowLong.HINSTANCE), HINSTANCE),
        None
    )

    return hwnd_button

def CreateEdit(hwnd_parent, control_id, x, y, width, height):
    hwnd_edit = CreateWindowExA(0,
        b"EDIT",
        b"",
        WindowStyle.TABSTOP | WindowStyle.VISIBLE | WindowStyle.CHILD
        | WindowStyle.BORDER,
        x, y,
        width, height,
        hwnd_parent, HMENU(control_id),
        ctypes.cast(GetWindowLongPtrA(hwnd_parent, GetWindowLong.HINSTANCE), HINSTANCE),
        None
    )

    return hwnd_edit

def SetView(hwnd_listview, dw_view):
    LVS_TYPEMASK = 0x0003
    dw_style = GetWindowLongPtrA(hwnd_listview, GetWindowLong.STYLE)
    if (dw_style & LVS_TYPEMASK) != dw_view:
        SetWindowLongPtrA(hwnd_listview, GetWindowLong.STYLE,
                          (dw_style & ~LVS_TYPEMASK) | dw_view)

def GetProcessEntries():
    entries = []
    icons = []
    full_paths = []
    entry = PROCESSENTRY32()
    entry.dwSize = ctypes.sizeof(PROCESSENTRY32)

    current_process_machine = USHORT(0)
    native_machine          = USHORT(0)
    
    current_process_handle = GetCurrentProcess()
    IsWow64Process2(current_process_handle, ctypes.byref(current_process_machine),
                    ctypes.byref(native_machine))
    
    snapshot = CreateToolhelp32Snapshot(SnapshotInclude.PROCESS, 0)
    if Process32First(snapshot, ctypes.byref(entry)):
        while Process32Next(snapshot, ctypes.byref(entry)):
            try:
                process_handle = OpenProcess(Process.QUERY_LIMITED_INFORMATION,
                                             False, entry.th32ProcessID)

                process_machine = USHORT(0)
                IsWow64Process2(process_handle, ctypes.byref(process_machine),
                                ctypes.byref(native_machine))
                if process_machine.value == current_process_machine.value:
                    entry_copy = PROCESSENTRY32()
                    
                    full_process_image_name = ctypes.create_string_buffer(MAX_PATH)
                    full_process_image_name_length = DWORD(MAX_PATH)
                    QueryFullProcessImageNameA(process_handle, 0,
                                               ctypes.cast(full_process_image_name, ctypes.c_char_p),
                                               ctypes.byref(full_process_image_name_length))

                    small_icon = HICON()
                    large_icon = HICON()
                    result = ExtractIconExA(ctypes.cast(full_process_image_name, ctypes.c_char_p),
                                   0, ctypes.byref(small_icon), ctypes.byref(large_icon), 1)
                    
                    ctypes.memmove(ctypes.byref(entry_copy), ctypes.byref(entry),
                                   ctypes.sizeof(PROCESSENTRY32))

                    icon = (small_icon, large_icon)
                    entries.append(entry_copy)
                    full_paths.append(full_process_image_name)
                    icons.append(icon)
                CloseHandle(process_handle)
            except OSError:
                pass

    CloseHandle(snapshot)
    return entries, icons, full_paths
                      
def InjectDLL(target_pid, filename_dll):
    
    target_handle = OpenProcess(Process.CREATE_THREAD \
                        | Process.VM_OPERATION | Process.VM_READ \
                        | Process.VM_WRITE, False, target_pid)
    
    dll_path_addr = VirtualAllocEx(target_handle, None, len(filename_dll),
                        AllocationType.COMMIT | AllocationType.RESERVE,
                        PageProtection.READWRITE)

    WriteProcessMemory(target_handle, dll_path_addr,
        filename_dll, len(filename_dll), None)

    module_handle = GetModuleHandleA(b"Kernel32")
    target_LoadLibraryA = GetProcAddress(module_handle, b"LoadLibraryA")

    thread_handle = CreateRemoteThread(target_handle, None, 0,
                        ctypes.cast(target_LoadLibraryA, LPTHREAD_START_ROUTINE),
                        dll_path_addr, 0, None)

    WaitForSingleObject(thread_handle, INFINITE)

    exit_code = DWORD()
    GetExitCodeThread(thread_handle, ctypes.byref(exit_code))

    try:
        CloseHandle(thread_handle)
        VirtualFreeEx(thread_handle, dll_path_addr, 0, FreeType.RELEASE)
        CloseHandle(target_handle)
    except OSError:
        pass

def EnumChildProc(hwnd, lParam):
    result = SendMessageA(hwnd, WindowMessage.SETFONT, WPARAM(lParam),
        MAKELPARAM(1, 0))
    return True

def ListViewCompareProc(lparam1, lparam2, lparamSort):
    if lparam1 and lparam2:
        process1 = ctypes.cast(lparam1, LPPROCESSENTRY32).contents
        process2 = ctypes.cast(lparam2, LPPROCESSENTRY32).contents
        
        if lparamSort == 0 or lparamSort == 4:
            return process1.szExeFile > process2.szExeFile
        if lparamSort == 1:
            return process1.th32ProcessID > process2.th32ProcessID
        if lparamSort == 2:
            return process1.th32ParentProcessID > process2.th32ParentProcessID
        if lparamSort == 3:
            return process1.cntThreads > process2.cntThreads

def NotifyHandler(hwnd, uMsg, wParam, lParam):
    LVN_FIRST = 4294967196
    LVN_GETDISPINFOA = LVN_FIRST - 50
    LVN_COLUMNCLICK = LVN_FIRST - 8
    lv_displayinfo = ctypes.cast(lParam, LPLV_DISPINFOA).contents
    nm_listview = ctypes.cast(lParam, LPNM_LISTVIEW).contents

    if wParam != PROCESS_LISTVIEW:
        return False
    
    if nm_listview.hdr.code == LVN_COLUMNCLICK:
        ListView_SortItems(nm_listview.hdr.hwndFrom,
                           PFNLVCOMPARE(ListViewCompareProc),
                           nm_listview.iSubItem)
    return False

def WindowProc(hwnd, uMsg, wParam, lParam):
    if uMsg == WindowMessage.DESTROY:
        PostQuitMessage(0) 
    if uMsg == WindowMessage.CLOSE:
        DestroyWindow(hwnd)
    if uMsg == WindowMessage.NOTIFY:
        NotifyHandler(hwnd, uMsg, wParam, lParam)
    if uMsg == WindowMessage.COMMAND:
        control_id = LOWORD(wParam).value
        notification_code = HIWORD(wParam).value
        control_hwnd = lParam

        if control_id == INJECT_BUTTON:
            hwnd_listview = GetDlgItem(hwnd, PROCESS_LISTVIEW)
            # LVNI_SELECTED           0x0002
            selected = ListView_GetNextItem(hwnd_listview, -1, 0x0002)
            print("Button clicked! %d" % selected)
            
            lvitem = LVITEMA()
            lvitem.mask = 0x00000001 | 0x00000002 | 0x00000004 | 0x00000008
            lvitem.state = 0
            lvitem.stateMask = 0
            lvitem.iItem = selected
            lvitem.iSubItem = 0

            ListView_GetItemA(hwnd_listview, ctypes.byref(lvitem))
            process = ctypes.cast(lvitem.lParam, LPPROCESSENTRY32).contents
            target_pid = process.th32ProcessID
            
            dll_path = ctypes.create_string_buffer(MAX_PATH)
            hwnd_edit = GetDlgItem(hwnd, FILEPATH_EDIT)
            
            result = SendMessageA(hwnd_edit, WindowMessage.GETTEXT, WPARAM(MAX_PATH),
                                  LPARAM(ctypes.cast(dll_path, ctypes.c_void_p).value))

            print("Injecting into PID %d, process at %s" % (target_pid, dll_path))
            InjectDLL(target_pid, dll_path)
            ctypes.windll.user32.MessageBoxA(hwnd, \
                b"Injecting into PID %d, process at %s" % (target_pid, dll_path), b"Success!", 0)
                

        if control_id == SEARCH_BUTTON:
            text_buffer = ctypes.create_string_buffer(MAX_PATH)
            
            openfilename = OPENFILENAMEA()
            openfilename.lStructSize = ctypes.sizeof(OPENFILENAMEA)
            openfilename.hwndOwner = None
            openfilename.lpstrFile = ctypes.cast(text_buffer, ctypes.c_char_p)
            openfilename.nMaxFile = ctypes.sizeof(text_buffer)
            openfilename.lpstrFilter = b"All Files (*.*)\0*.*\0Dynamically Linked Library (*.dll)\0*.DLL\0"
            openfilename.nFilterIndex = 2
            openfilename.lpstrFileTitle = None
            openfilename.nMaxFileTitle =  0
            openfilename.lpstrInitialDir = None
            openfilename.Flags = 0x00000800 | 0x00001000
            result = GetOpenFileNameA(ctypes.byref(openfilename))
            if not result:
                print("CommDlgExtendedError: ", CommDlgExtendedError())
            else:
                hwnd_edit = GetDlgItem(hwnd, FILEPATH_EDIT)
                SendMessageA(hwnd_edit, WindowMessage.SETTEXT, WPARAM(0), LPARAM(ctypes.cast(text_buffer, ctypes.c_void_p).value))
                print(text_buffer.value)
        
        print("%s, %s, %s" % (control_id, notification_code, control_hwnd))
        
    return DefWindowProcA(hwnd, uMsg, wParam, lParam)

"""
def CreateIconFromBytes(dc, width, height, icon_bytes) {
        hIcon = HICON(0)

        ICONINFO iconInfo = {
            TRUE, // fIcon, set to true if this is an icon, set to false if this is a cursor
            NULL, // xHotspot, set to null for icons
            NULL, // yHotspot, set to null for icons
            NULL, // Monochrome bitmap mask, set to null initially
            NULL  // Color bitmap mask, set to null initially
        };

        uint32* rawBitmap = new uint32[width * height];

        ULONG uWidth = (ULONG)width;
        ULONG uHeight = (ULONG)height;
        uint32* bitmapPtr = rawBitmap;
        for (ULONG y = 0; y < uHeight; y++) {
            for (ULONG x = 0; x < uWidth; x++) {
                // Bytes are expected to be in RGB order (8 bits each)
                // Swap G and B bytes, so that it is in BGR order for windows
                uint32 byte = bytes[x + y * width];
                uint8 A = (byte & 0xff000000) >> 24;
                uint8 R = (byte & 0xff0000) >> 16;
                uint8 G = (byte & 0xff00) >> 8;
                uint8 B = (byte & 0xff);
                *bitmapPtr = (A << 24) | (R << 16) | (G << 8) | B;
                bitmapPtr++;
            }
        }

        iconInfo.hbmColor = CreateBitmap(width, height, 1, 32, rawBitmap);
        if (iconInfo.hbmColor) {
            iconInfo.hbmMask = CreateCompatibleBitmap(DC, width, height);
            if (iconInfo.hbmMask) {
                hIcon = CreateIconIndirect(&iconInfo);
                if (hIcon == NULL) {
                    Log::Warning("Failed to create icon.");
                }
                DeleteObject(iconInfo.hbmMask);
            } else {
                Log::Warning("Failed to create color mask.");
            }
            DeleteObject(iconInfo.hbmColor);
        } else {
            Log::Warning("Failed to create bitmap mask.");
        }

        delete[] rawBitmap;

        return hIcon;
}
"""

if __name__ == "__main__":
    processes, icons, paths = GetProcessEntries()
    print("Processes found:", len(processes))
    
    hinstance = GetModuleHandleA(None)

    try:
        icon = LoadImageA(hinstance, b"gear_icon.ico", 1, 32, 32, 0x00000010 | 0x00000080)
    except:
        icon = LoadIconA(None, LPSTR(32512))

    class_name = b"Hello world!"
    
    window_class = WNDCLASSA()
    window_class.style = ClassStyle.VREDRAW | ClassStyle.HREDRAW
    window_class.lpfnWndProc = WNDPROC(WindowProc)
    window_class.hInstance = hinstance
    window_class.lpszClassName = class_name
    window_class.hbrBackground = HBRUSH(5)
    window_class.hIcon = icon
    RegisterClassA(ctypes.byref(window_class))

    hwnd_main = CreateWindowExA(
        0,
        class_name,
        b"DLL Injector",
        WindowStyle.OVERLAPPED | WindowStyle.CAPTION \
        | WindowStyle.SYSMENU | WindowStyle.MINIMIZEBOX,
        CW_USEDEFAULT, CW_USEDEFAULT, 600, 480,
        None,
        None,
        hinstance,
        None
    )

    client_rect = RECT()
    GetClientRect(hwnd_main, ctypes.byref(client_rect))

    inject_button_width = 80
    inject_button_height = 23
    hwnd_inject_button = CreateButton(hwnd_main, INJECT_BUTTON,
                                      client_rect.right - 10 - inject_button_width,
                                      client_rect.bottom - 10 - inject_button_height,
                                      inject_button_width, b"Inject")


    search_button_width = 100
    search_button_height = 23
    hwnd_search_button = CreateButton(hwnd_main, SEARCH_BUTTON,
                                      client_rect.right - 10 - search_button_width,
                                      client_rect.top + 10,
                                      search_button_width, b'Browse DLL...')

    CreateEdit(hwnd_main, FILEPATH_EDIT,
               client_rect.left + 10,
               client_rect.top + 10,
               client_rect.right - 10 - search_button_width - 20,
               23
    )

    hwnd_listview, processes = CreateListView(hwnd_main, PROCESS_LISTVIEW,
                                   client_rect.left + 10,
                                   client_rect.top + 10 + 32,
                                   client_rect.right - client_rect.left - 20,
                                   client_rect.bottom - client_rect.top - 20 - 23 - 10 - 32,
                                   processes, icons, paths
    )

    ShowWindow(hwnd_main, 5)
    
    metrics = NONCLIENTMETRICSA()
    metrics.cbSize = ctypes.sizeof(NONCLIENTMETRICSA)
    # SPI_GETNONCLIENTMETRICS = 0x0029
    SystemParametersInfoA(0x0029, metrics.cbSize, ctypes.byref(metrics), 0)
    font = CreateFontIndirectA(ctypes.byref(metrics.lfMenuFont))

    EnumChildWindows(hwnd_main, WNDENUMPROC(EnumChildProc),
                     LPARAM(ctypes.cast(font, ctypes.c_void_p).value))

    # DeleteObject(font)

    msg = MSG()
    while (bRet := GetMessageA(ctypes.byref(msg), None, 0, 0)) != 0:
        if bRet == -1:
            break
        TranslateMessage(ctypes.byref(msg))
        DispatchMessageA(ctypes.byref(msg))

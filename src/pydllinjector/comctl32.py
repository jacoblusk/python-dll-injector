from ctypes.wintypes import *
from pydllinjector.wintypes_extended import *
from pydllinjector.winapi_error import *
from pydllinjector.user32 import *

import ctypes


class InitCommonControlsFlag(enum.IntFlag):
    LISTVIEWCLASSES = 0x01


class ListViewNotifyCode(enum.IntEnum):
    FIRST = 4294967196
    GetDispInfoA = FIRST - 50
    COLUMNCLICK = FIRST - 8


class ListViewNextItem(enum.IntFlag):
    SELECTED = 0x0002


class ListViewStyle(enum.IntFlag):
    REPORT = 0x0001
    EDITABLES = 0x0200
    SHOWSELALWAYS = 0x0008
    TYPEMASK = 0x0003


class ListViewMessage(enum.IntEnum):
    FIRST = 0x1000
    GETITEMA = FIRST + 5
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
    LVM_SETEXTENDEDLISTVIEWSTYLE = FIRST + 54
    LVM_GETEXTENDEDLISTVIEWSTYLE = FIRST + 55


def ListView_GetStyle(hwnd):
    return SendMessageA(
        hwnd, ListViewMessage.LVM_GETEXTENDEDLISTVIEWSTYLE, WPARAM(0), 0
    )


def ListView_SetStyle(hwnd, style):
    return SendMessageA(
        hwnd, ListViewMessage.LVM_SETEXTENDEDLISTVIEWSTYLE, WPARAM(0), style
    )


def ListView_InsertItemA(hwnd, pitem):
    return SendMessageA(
        hwnd,
        ListViewMessage.INSERTITEMA,
        WPARAM(0),
        LPARAM(ctypes.cast(pitem, ctypes.c_void_p).value),
    )


def ListView_InsertColumnA(hwnd, iCol, pcol):
    return SendMessageA(
        hwnd,
        ListViewMessage.INSERTCOLUMNA,
        WPARAM(iCol),
        LPARAM(ctypes.cast(pcol, ctypes.c_void_p).value),
    )


def ListView_SetImageList(hwnd, himl, iImageList):
    return ctypes.cast(
        SendMessageA(
            hwnd,
            ListViewMessage.SETIMAGELIST,
            WPARAM(iImageList),
            LPARAM(ctypes.cast(himl, ctypes.c_void_p).value),
        ),
        ctypes.c_void_p,
    )


def ListView_GetNextItem(hwnd, i, flags):
    return SendMessageA(
        hwnd, ListViewMessage.GETNEXTITEM, WPARAM(i), MAKELPARAM((flags), 0)
    )


def ListView_GetItemA(hwnd, pitem):
    return SendMessageA(
        hwnd,
        ListViewMessage.GETITEMA,
        WPARAM(0),
        LPARAM(ctypes.cast(pitem, ctypes.c_void_p).value),
    )


def ListView_GetItemTextA(hwndLV, i, iSubItem_, pszText_, cchTextMax_):
    _macro_lvi = LVITEMA()
    _macro_lvi.iSubItem = iSubItem_
    _macro_lvi.cchTextMax = cchTextMax_
    _macro_lvi.pszText = pszText_
    SendMessageA(
        (hwndLV),
        ListViewMessage.GETITEMTEXTA,
        WPARAM(i),
        LPARAM(ctypes.cast(ctypes.byref(_macro_lvi), ctypes.c_void_p).value),
    )


def ListView_SetItemTextA(hwnd, i, iSubItem, pszText):
    lvitem = LVITEMA()
    lvitem.iSubItem = iSubItem
    lvitem.pszText = pszText
    SendMessageA(
        hwnd,
        ListViewMessage.SETITEMTEXTA,
        WPARAM(i),
        LPARAM(ctypes.cast(ctypes.byref(lvitem), ctypes.c_void_p).value),
    )


def ListView_SortItems(hwndLV, _pfnCompare, _lPrm):
    return SendMessageA(
        hwndLV,
        ListViewMessage.SORTITEMS,
        WPARAM(_lPrm),
        LPARAM(ctypes.cast(_pfnCompare, ctypes.c_void_p).value),
    )


def ImageList_AddIcon(himl, hicon):
    return ImageList_ReplaceIcon(himl, -1, hicon)


class LVITEMA(ctypes.Structure):
    _fields_ = [
        ("mask", UINT),
        ("iItem", ctypes.c_int),
        ("iSubItem", ctypes.c_int),
        ("state", UINT),
        ("stateMask", UINT),
        ("pszText", LPCSTR),
        ("cchTextMax", ctypes.c_int),
        ("iImage", ctypes.c_int),
        ("lParam", LPARAM),
        ("iIndent", ctypes.c_int),
        ("iGroupId", ctypes.c_int),
        ("cColumns", UINT),
        ("puColumns", ctypes.POINTER(UINT)),
        ("piColFmt", ctypes.POINTER(ctypes.c_int)),
        ("iGroup", ctypes.c_int),
    ]


LPLVITEMA = ctypes.POINTER(LVITEMA)


class NMHDR(ctypes.Structure):
    _fields_ = [("hwndFrom", HWND), ("idFrom", ctypes.POINTER(UINT)), ("code", UINT)]


class LV_DISPINFOA(ctypes.Structure):
    _fields_ = [("hdr", NMHDR), ("item", LVITEMA)]


LPLV_DISPINFOA = ctypes.POINTER(LV_DISPINFOA)


class NM_LISTVIEW(ctypes.Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("iItem", ctypes.c_int),
        ("iSubItem", ctypes.c_int),
        ("uNewState", UINT),
        ("uOldState", UINT),
        ("uChanged", UINT),
        ("ptAction", POINT),
        ("lParam", LPARAM),
    ]


LPNM_LISTVIEW = ctypes.POINTER(NM_LISTVIEW)


class LVCOLUMNA(ctypes.Structure):
    _fields_ = [
        ("mask", UINT),
        ("fmt", ctypes.c_int),
        ("cx", ctypes.c_int),
        ("pszText", LPCSTR),
        ("cchTextMax", ctypes.c_int),
        ("iSubItem", ctypes.c_int),
        ("iImage", ctypes.c_int),
        ("iOrder", ctypes.c_int),
        ("cxMin", ctypes.c_int),
        ("cxDefault", ctypes.c_int),
        ("cxIdeal", ctypes.c_int),
    ]


LPLVCOLUMNA = ctypes.POINTER(LVCOLUMNA)


class INITCOMMONCONTROLSEX(ctypes.Structure):
    _fields_ = [("dwSize", DWORD), ("dwICC", DWORD)]


LPINITCOMMONCONTROLSEX = ctypes.POINTER(INITCOMMONCONTROLSEX)


class InitCommonControlsExError(Exception):
    pass


def InitCommonControlsEx_errcheck(result, func, args):
    if result == 0:
        raise InitCommonControlsExError("InitCommonControlsEx failed.")


ImageList_Create = ctypes.windll.comctl32.ImageList_Create
ImageList_Create.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
    UINT,
    ctypes.c_int,
    ctypes.c_int,
]
ImageList_Create.restype = ctypes.c_void_p
ImageList_Create.errcheck = LPVOID_errcheck

ImageList_ReplaceIcon = ctypes.windll.comctl32.ImageList_ReplaceIcon
ImageList_ReplaceIcon.argtypes = [ctypes.c_void_p, ctypes.c_int, HICON]
ImageList_ReplaceIcon.restype = ctypes.c_int

InitCommonControlsEx = ctypes.windll.comctl32.InitCommonControlsEx
InitCommonControlsEx.argtypes = [LPINITCOMMONCONTROLSEX]
InitCommonControlsEx.restype = BOOL
InitCommonControlsEx.errcheck = InitCommonControlsEx_errcheck

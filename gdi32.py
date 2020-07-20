from ctypes.wintypes import *
from wintypes_extended import *
from winapi_error import *
from user32 import *

import ctypes

CreateFontIndirectA = ctypes.windll.gdi32.CreateFontIndirectA
CreateFontIndirectA.argtypes = [LPLOGFONTA]
CreateFontIndirectA.restype = HFONT
CreateFontIndirectA.errcheck = LPVOID_errcheck

DeleteObject = ctypes.windll.gdi32.DeleteObject
DeleteObject.argtypes = [LPVOID]
DeleteObject.restype = BOOL

GetStockObject = ctypes.windll.gdi32.GetStockObject
GetStockObject.argtypes = [ctypes.c_int]
GetStockObject.restype = HANDLE
GetStockObject.errcheck = LPVOID_errcheck

GetObjectA = ctypes.windll.gdi32.GetObjectA
GetObjectA.argtypes = [HANDLE, ctypes.c_int, LPVOID]
GetObjectA.restype = ctypes.c_int

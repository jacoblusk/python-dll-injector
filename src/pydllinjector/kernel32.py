from ctypes.wintypes import *
from pydllinjector.wintypes_extended import *
from pydllinjector.winapi_error import *

import ctypes
import enum

INVALID_HANDLE_VALUE = ctypes.c_void_p(-1)
INFINITE = ctypes.c_uint(-1)


class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("nLength", DWORD),
        ("lpSecurityDescriptor", LPVOID),
        ("bInheritHandle", BOOL),
    ]


LPSECURITY_ATTRIBUTES = ctypes.POINTER(SECURITY_ATTRIBUTES)


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("cntUsage", DWORD),
        ("th32ProcessID", DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
        ("th32ModuleID", DWORD),
        ("cntThreads", DWORD),
        ("th32ParentProcessID", DWORD),
        ("pcPriClassBase", LONG),
        ("dwFlags", DWORD),
        ("szExeFile", CHAR * MAX_PATH),
    ]


LPPROCESSENTRY32 = ctypes.POINTER(PROCESSENTRY32)


class Process(enum.IntFlag):
    CREATE_PROCESS = 0x0080
    CREATE_THREAD = 0x0002
    DUP_HANDLE = 0x0002
    QUERY_INFORMATION = 0x0400
    QUERY_LIMITED_INFORMATION = 0x1000
    SET_INFORMATION = 0x0200
    SET_QUOTA = 0x0100
    SUSPEND_RESUME = 0x0800
    TERMINATE = 0x0001
    VM_OPERATION = 0x0008
    VM_READ = 0x0010
    VM_WRITE = 0x0020
    SYNCHRONIZE = 0x00100000


class AllocationType(enum.IntFlag):
    COMMIT = 0x00001000
    RESERVE = 0x00002000
    RESET = 0x00080000
    RESET_UNDO = 0x1000000
    LARGE_PAGES = 0x20000000
    PHYSICAL = 0x00400000
    TOP_DOWN = 0x00100000


class FreeType(enum.IntFlag):
    COALESCE_PLACEHOLDERS = 0x1
    PRESERVE_PLACEHOLDER = 0x2
    DECOMMIT = 0x4000
    RELEASE = 0x8000


class PageProtection(enum.IntFlag):
    EXECUTE = 0x10
    EXECUTE_READ = 0x20
    EXECUTE_READWRITE = 0x40
    EXECUTE_WRITECOPY = 0x80
    NOACCESS = 0x01
    READONLY = 0x02
    READWRITE = 0x04
    WRITECOPY = 0x08
    TARGETS_INVALID = 0x40000000
    TARGETS_NO_UPDATE = 0x40000000
    GUARD = 0x100
    NOCACHE = 0x200
    WRITECOMBINE = 0x400
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
    OBJECT_0 = 0x00000000
    TIMEOUT = 0x00000102
    FAILED = 0xFFFFFFFF


def CreateToolhelp32Snapshot_errcheck(result, func, args):
    if result == INVALID_HANDLE_VALUE:
        raise ctypes.WinError()
    return result


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
CreateRemoteThread.argtypes = [
    HANDLE,
    LPSECURITY_ATTRIBUTES,
    SIZE_T,
    LPTHREAD_START_ROUTINE,
    LPVOID,
    DWORD,
    LPDWORD,
]
CreateRemoteThread.restype = HANDLE
CreateRemoteThread.errcheck = LPVOID_errcheck

WaitForSingleObject = ctypes.windll.kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = [HANDLE, DWORD]
WaitForSingleObject.restype = DWORD

GetExitCodeThread = ctypes.windll.kernel32.GetExitCodeThread
GetExitCodeThread.argtypes = [HANDLE, LPDWORD]
GetExitCodeThread.restype = BOOL
GetExitCodeThread.errcheck = Win32API_errcheck

IsWow64Process2 = ctypes.windll.kernel32.IsWow64Process2
IsWow64Process2.argtypes = [HANDLE, ctypes.POINTER(USHORT), ctypes.POINTER(USHORT)]
IsWow64Process2.restype = BOOL
IsWow64Process2.errcheck = Win32API_errcheck

GetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess
GetCurrentProcess.argtypes = None
GetCurrentProcess.restype = HANDLE

QueryFullProcessImageNameA = ctypes.windll.kernel32.QueryFullProcessImageNameA
QueryFullProcessImageNameA.argtypes = [HANDLE, DWORD, LPSTR, PDWORD]
QueryFullProcessImageNameA.restype = BOOL
QueryFullProcessImageNameA.errcheck = Win32API_errcheck

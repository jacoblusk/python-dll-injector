from ctypes.wintypes import *
from pydllinjector.wintypes_extended import *
from pydllinjector.kernel32 import *
from pydllinjector.user32 import *
from pydllinjector.comdlg32 import *
from pydllinjector.gdi32 import *
from pydllinjector.comctl32 import *

import ctypes

INJECT_BUTTON = 100
PROCESS_LISTVIEW = 101
SEARCH_BUTTON = 102
FILEPATH_EDIT = 103

ExtractIconExA = ctypes.windll.shell32.ExtractIconExA
ExtractIconExA.argtypes = [
    LPCSTR,
    ctypes.c_int,
    ctypes.POINTER(HICON),
    ctypes.POINTER(HICON),
    UINT,
]
ExtractIconExA.restype = UINT


def CreateListView(
    hwnd_parent, control_id, x, y, width, height, processes, icons, paths
):
    icex = INITCOMMONCONTROLSEX()
    icex.dwSize = ctypes.sizeof(INITCOMMONCONTROLSEX)
    icex.dwICC = InitCommonControlsFlag.LISTVIEWCLASSES
    result = InitCommonControlsEx(ctypes.byref(icex))

    hwnd_listview = CreateWindowExA(
        0,
        b"SysListView32",
        b"",
        WindowStyle.VISIBLE
        | WindowStyle.CHILD
        | ListViewStyle.REPORT
        | ListViewStyle.SHOWSELALWAYS
        | WindowStyle.BORDER,
        x,
        y,
        width,
        height,
        hwnd_parent,
        HMENU(control_id),
        ctypes.cast(GetWindowLongPtrA(hwnd_parent, GetWindowLong.HINSTANCE), HINSTANCE),
        None,
    )

    child_ex_style = ListView_GetStyle(hwnd_listview)
    child_ex_style |= WindowStyle.LVS_EX_FULLROWSELECT
    ListView_SetStyle(hwnd_listview, WindowStyle.LVS_EX_FULLROWSELECT)

    hsmall = ImageList_Create(16, 16, 0x00000020 | 0x00020000, len(processes), 0)
    hlarge = ImageList_Create(32, 32, 0x00000020 | 0x00020000, len(processes), 0)

    null_icon = LoadIconA(None, LPSTR(32512))

    for i in range(len(processes)):
        if (
            ImageList_AddIcon(hsmall, icons[i][0]) == -1
            or ImageList_AddIcon(hlarge, icons[i][1]) == -1
        ):
            # raise Exception("Error adding Icons.")
            ImageList_AddIcon(hsmall, null_icon)

    ListView_SetImageList(hwnd_listview, hsmall, 1)
    ListView_SetImageList(hwnd_listview, hlarge, 0)

    column_names = [
        (b"Process Name", 160),
        (b"PID", 80),
        (b"Parent PID", 90),
        (b"Threads", 80),
        (b"Absolute Path", 500),
    ]

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
        lvitem.lParam = LPARAM(
            ctypes.cast(ctypes.byref(processes[i]), ctypes.c_void_p).value
        )

        if ListView_InsertItemA(hwnd_listview, ctypes.byref(lvitem)) == -1:
            raise Exception("ListView_InsertItem")

        ListView_SetItemTextA(hwnd_listview, i, 1, b"%d" % processes[i].th32ProcessID)
        ListView_SetItemTextA(
            hwnd_listview, i, 2, b"%d" % processes[i].th32ParentProcessID
        )
        ListView_SetItemTextA(hwnd_listview, i, 3, b"%d" % processes[i].cntThreads)
        ListView_SetItemTextA(
            hwnd_listview, i, 4, ctypes.cast(paths[i], ctypes.c_char_p)
        )

    return hwnd_listview, processes


def CreateButton(hwnd_parent, control_id, x, y, width, text, height=23):
    hwnd_button = CreateWindowExA(
        0,
        b"BUTTON",
        text,
        WindowStyle.TABSTOP
        | WindowStyle.VISIBLE
        | WindowStyle.CHILD
        | ButtonStyle.TEXT,
        x,
        y,
        width,
        height,
        hwnd_parent,
        HMENU(control_id),
        ctypes.cast(GetWindowLongPtrA(hwnd_parent, GetWindowLong.HINSTANCE), HINSTANCE),
        None,
    )

    return hwnd_button


def CreateEdit(hwnd_parent, control_id, x, y, width, height):
    hwnd_edit = CreateWindowExA(
        0,
        b"EDIT",
        b"",
        WindowStyle.TABSTOP
        | WindowStyle.VISIBLE
        | WindowStyle.CHILD
        | WindowStyle.BORDER,
        x,
        y,
        width,
        height,
        hwnd_parent,
        HMENU(control_id),
        ctypes.cast(GetWindowLongPtrA(hwnd_parent, GetWindowLong.HINSTANCE), HINSTANCE),
        None,
    )

    return hwnd_edit


def SetView(hwnd_listview, dw_view):
    dw_style = GetWindowLongPtrA(hwnd_listview, GetWindowLong.STYLE)
    if (dw_style & ListViewStyle.TYPEMASK) != dw_view:
        SetWindowLongPtrA(
            hwnd_listview,
            GetWindowLong.STYLE,
            (dw_style & ~ListViewStyle.TYPEMASK) | dw_view,
        )


def GetProcessEntries():
    entries = []
    icons = []
    full_paths = []
    entry = PROCESSENTRY32()
    entry.dwSize = ctypes.sizeof(PROCESSENTRY32)

    current_process_machine = USHORT(0)
    native_machine = USHORT(0)

    current_process_handle = GetCurrentProcess()
    IsWow64Process2(
        current_process_handle,
        ctypes.byref(current_process_machine),
        ctypes.byref(native_machine),
    )

    snapshot = CreateToolhelp32Snapshot(SnapshotInclude.PROCESS, 0)
    if Process32First(snapshot, ctypes.byref(entry)):
        while Process32Next(snapshot, ctypes.byref(entry)):
            try:
                process_handle = OpenProcess(
                    Process.QUERY_LIMITED_INFORMATION, False, entry.th32ProcessID
                )

                process_machine = USHORT(0)
                IsWow64Process2(
                    process_handle,
                    ctypes.byref(process_machine),
                    ctypes.byref(native_machine),
                )
                if process_machine.value == current_process_machine.value:
                    entry_copy = PROCESSENTRY32()

                    full_process_image_name = ctypes.create_string_buffer(MAX_PATH)
                    full_process_image_name_length = DWORD(MAX_PATH)
                    QueryFullProcessImageNameA(
                        process_handle,
                        0,
                        ctypes.cast(full_process_image_name, ctypes.c_char_p),
                        ctypes.byref(full_process_image_name_length),
                    )

                    small_icon = HICON()
                    large_icon = HICON()
                    result = ExtractIconExA(
                        ctypes.cast(full_process_image_name, ctypes.c_char_p),
                        0,
                        ctypes.byref(small_icon),
                        ctypes.byref(large_icon),
                        1,
                    )

                    ctypes.memmove(
                        ctypes.byref(entry_copy),
                        ctypes.byref(entry),
                        ctypes.sizeof(PROCESSENTRY32),
                    )

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
    target_handle = OpenProcess(
        Process.CREATE_THREAD
        | Process.VM_OPERATION
        | Process.VM_READ
        | Process.VM_WRITE,
        False,
        target_pid,
    )

    dll_path_addr = VirtualAllocEx(
        target_handle,
        None,
        len(filename_dll),
        AllocationType.COMMIT | AllocationType.RESERVE,
        PageProtection.READWRITE,
    )

    WriteProcessMemory(
        target_handle, dll_path_addr, filename_dll, len(filename_dll), None
    )

    module_handle = GetModuleHandleA(b"Kernel32")
    target_LoadLibraryA = GetProcAddress(module_handle, b"LoadLibraryA")

    thread_handle = CreateRemoteThread(
        target_handle,
        None,
        0,
        ctypes.cast(target_LoadLibraryA, LPTHREAD_START_ROUTINE),
        dll_path_addr,
        0,
        None,
    )

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
    result = SendMessageA(hwnd, WindowMessage.SETFONT, WPARAM(lParam), MAKELPARAM(1, 0))
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
    lv_displayinfo = ctypes.cast(lParam, LPLV_DISPINFOA).contents
    nm_listview = ctypes.cast(lParam, LPNM_LISTVIEW).contents

    if wParam != PROCESS_LISTVIEW:
        return False

    if nm_listview.hdr.code == ListViewNotifyCode.COLUMNCLICK:
        ListView_SortItems(
            nm_listview.hdr.hwndFrom,
            PFNLVCOMPARE(ListViewCompareProc),
            nm_listview.iSubItem,
        )
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
            selected = ListView_GetNextItem(
                hwnd_listview, -1, ListViewNextItem.SELECTED
            )
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

            result = SendMessageA(
                hwnd_edit,
                WindowMessage.GETTEXT,
                WPARAM(MAX_PATH),
                LPARAM(ctypes.cast(dll_path, ctypes.c_void_p).value),
            )

            print("Injecting into PID %d, process at %s" % (target_pid, dll_path))
            InjectDLL(target_pid, dll_path)
            ctypes.windll.user32.MessageBoxA(
                hwnd,
                b"Injecting into PID %d, process at %s" % (target_pid, dll_path),
                b"Success!",
                0,
            )

        if control_id == SEARCH_BUTTON:
            text_buffer = ctypes.create_string_buffer(MAX_PATH)

            openfilename = OPENFILENAMEA()
            openfilename.lStructSize = ctypes.sizeof(OPENFILENAMEA)
            openfilename.hwndOwner = None
            openfilename.lpstrFile = ctypes.cast(text_buffer, ctypes.c_char_p)
            openfilename.nMaxFile = ctypes.sizeof(text_buffer)
            openfilename.lpstrFilter = (
                b"All Files (*.*)\0*.*\0Dynamically Linked Library (*.dll)\0*.DLL\0"
            )
            openfilename.nFilterIndex = 2
            openfilename.lpstrFileTitle = None
            openfilename.nMaxFileTitle = 0
            openfilename.lpstrInitialDir = None
            openfilename.Flags = (
                OpenFileNameFlags.PATHMUSTEXIST | OpenFileNameFlags.FILEMUSTEXIST
            )
            result = GetOpenFileNameA(ctypes.byref(openfilename))
            if not result:
                print("CommDlgExtendedError: ", CommDlgExtendedError())
            else:
                hwnd_edit = GetDlgItem(hwnd, FILEPATH_EDIT)
                SendMessageA(
                    hwnd_edit,
                    WindowMessage.SETTEXT,
                    WPARAM(0),
                    LPARAM(ctypes.cast(text_buffer, ctypes.c_void_p).value),
                )
                print(text_buffer.value)

        print("%s, %s, %s" % (control_id, notification_code, control_hwnd))

    return DefWindowProcA(hwnd, uMsg, wParam, lParam)


def main():
    processes, icons, paths = GetProcessEntries()
    print("Processes found:", len(processes))

    hinstance = GetModuleHandleA(None)

    try:
        icon = LoadImageA(
            hinstance,
            b"gear_icon.ico",
            1,
            32,
            32,
            LoadImageFlags.LOADFROMFILE | LoadImageFlags.VGACOLOR,
        )
    except:
        icon = LoadIconA(None, LPSTR(32512))

    class_name = b"DLL Injector!"

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
        WindowStyle.OVERLAPPED
        | WindowStyle.CAPTION
        | WindowStyle.SYSMENU
        | WindowStyle.MINIMIZEBOX,
        CW_USEDEFAULT,
        CW_USEDEFAULT,
        600,
        480,
        None,
        None,
        hinstance,
        None,
    )

    client_rect = RECT()
    GetClientRect(hwnd_main, ctypes.byref(client_rect))

    inject_button_width = 100
    inject_button_height = 25
    hwnd_inject_button = CreateButton(
        hwnd_main,
        INJECT_BUTTON,
        client_rect.right - 10 - inject_button_width,
        client_rect.bottom - 10 - inject_button_height,
        inject_button_width,
        b"Inject",
        height=inject_button_height,
    )

    search_button_width = 100
    search_button_height = 25
    hwnd_search_button = CreateButton(
        hwnd_main,
        SEARCH_BUTTON,
        client_rect.right - 10 - search_button_width,
        client_rect.top + 10,
        search_button_width,
        b"Browse DLL...",
        height=search_button_height,
    )

    CreateEdit(
        hwnd_main,
        FILEPATH_EDIT,
        client_rect.left + 10,
        client_rect.top + 10,
        client_rect.right - 10 - search_button_width - 20,
        25,
    )

    hwnd_listview, processes = CreateListView(
        hwnd_main,
        PROCESS_LISTVIEW,
        client_rect.left + 10,
        client_rect.top + 10 + 32,
        client_rect.right - client_rect.left - 20,
        client_rect.bottom - client_rect.top - 20 - 23 - 10 - 32,
        processes,
        icons,
        paths,
    )

    ShowWindow(hwnd_main, ShowWindowCommand.SHOW)

    metrics = NONCLIENTMETRICSA()
    metrics.cbSize = ctypes.sizeof(NONCLIENTMETRICSA)
    SystemParametersInfoA(
        SystemParametersInfoAcessibilityParameter.GETNONCLIENTMETRICS,
        metrics.cbSize,
        ctypes.byref(metrics),
        0,
    )
    font = CreateFontIndirectA(ctypes.byref(metrics.lfMenuFont))

    EnumChildWindows(
        hwnd_main,
        WNDENUMPROC(EnumChildProc),
        LPARAM(ctypes.cast(font, ctypes.c_void_p).value),
    )

    # DeleteObject(font)

    msg = MSG()
    while (bRet := GetMessageA(ctypes.byref(msg), None, 0, 0)) != 0:
        if bRet == -1:
            break
        TranslateMessage(ctypes.byref(msg))
        DispatchMessageA(ctypes.byref(msg))


if __name__ == "__main__":
    main()

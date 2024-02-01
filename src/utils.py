from ctypes import WinDLL, wintypes, Structure, c_long, byref
import ctypes
from ctypes.wintypes import HWND, BOOL, DWORD, RECT, LPARAM

# SystemParametersInfoW Constants
SPI_GETWORKAREA = 0x0030

# Load DLLs
user32 = WinDLL('user32.dll')
dwmapi = WinDLL('dwmapi.dll')

def get_work_dir_dimensions():
    desktopWorkingArea = wintypes.RECT()
    _ = user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, byref(desktopWorkingArea), 0)
    return desktopWorkingArea.left, desktopWorkingArea.top, desktopWorkingArea.right, desktopWorkingArea.bottom

def get_active_window_dimensions():
    hwnd = user32.GetForegroundWindow()
    rect = RECT()
    DMWA_EXTENDED_FRAME_BOUNDS = 9
    dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(DMWA_EXTENDED_FRAME_BOUNDS), byref(rect), ctypes.sizeof(rect))
    return rect.left, rect.top, rect.right, rect.bottom

def get_fullscreen_dimensions():
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def get_taskbar_dimensions():
    left, top, right, bottom = get_work_dir_dimensions()
    x, y = get_fullscreen_dimensions()
    return x - (right - left), bottom, x, y

def get_window_text(hwnd):
    length = user32.GetWindowTextLengthW(hwnd) + 1
    buffer = ctypes.create_unicode_buffer(length)
    user32.GetWindowTextW(hwnd, buffer, length)
    return buffer.value

def get_all_open_windows():
    window_rects = []

    def enum_windows_proc(hwnd, lParam):
        if user32.IsWindowVisible(hwnd):
            rect = RECT()
            user32.GetWindowRect(hwnd, byref(rect))
            title = get_window_text(hwnd)
            window_rects.append(((hwnd, title), (rect.left, rect.top, rect.right, rect.bottom)))
        return True

    enum_windows_callback = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)(enum_windows_proc)
    user32.EnumWindows(enum_windows_callback, 0)
    return window_rects

def get_filtered_windows():
    windows = get_all_open_windows()
    screen_width, screen_height = get_fullscreen_dimensions()
    filtered_windows = [window for window in windows if not (
        window[0][1] in ["Program Manager", "Microsoft Text Input Application", 
                        "Microsoft Store", "Settings", "WinSprites", "Setup", ""] or
        window[1][0] > screen_width or window[1][1] > screen_height or
        window[1][2] < 0 or window[1][3] < 0
    )]
    return filtered_windows

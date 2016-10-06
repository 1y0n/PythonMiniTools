#coding:utf-8

#code from <Black Hat Python>

from ctypes import *
import pyHook
import pythoncom

user32 = windll.user32

def onMouseEvent(event):
    #获取前台PID
    hwnd = user32.GetForegroundWindow()
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd,byref(pid))
    print 'MessageName:',event.MessageName
    print "Message:", event.Message
    print "Time:", event.Time
    print "Window:", event.Window
    print "WindowPid&Name:", str(pid.value) +'  &   '+ event.WindowName
    print "Injected:", event.Injected
    print "---"
    return True  #重要的 return True

#创建钩子管理器，注册，循环执行
hm = pyHook.HookManager()
hm.MouseAllButtons = onMouseEvent
hm.HookMouse()
pythoncom.PumpMessages()
#coding:utf-8

import win32file
import threading
import win32con

dirs = [r'd:\test']
action_dir = {1: 'New', 2: 'Delete', 3: 'Change', 4: 'Unknown', 5: 'Rename'}
def start_monitor(path_to_watch):
    h_directory = win32file.CreateFile(path_to_watch, win32con.GENERIC_READ, win32con.FILE_SHARE_DELETE|win32con.FILE_SHARE_READ
                                       |win32con.FILE_SHARE_WRITE, None, win32con.OPEN_EXISTING, win32con.FILE_FLAG_BACKUP_SEMANTICS, None)
    while True:
        try:
            results = win32file.ReadDirectoryChangesW(h_directory, 1024, True, win32con.FILE_NOTIFY_CHANGE_FILE_NAME
                                                      |win32con.FILE_NOTIFY_CHANGE_DIR_NAME|win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES|
                                                      win32con.FILE_NOTIFY_CHANGE_SIZE|win32con.FILE_NOTIFY_CHANGE_LAST_WRITE|
                                                      win32con.FILE_NOTIFY_CHANGE_SECURITY, None)
            for action, filename in results:
                print action_dir[action] + ' --> ' + filename
        except:
            pass

for path in dirs:
    t = threading.Thread(target=start_monitor, args=(path,))
    t.start()
from time import sleep
import pyautogui as pag
import pywinctl as pwc
from sxhkd_parser import *
import os

class SkynixWm:
    def __init__(self):
        self._get_sxhkd_binds()
        self.windows = [{"app": i.getAppName(), "window": i} for i in pwc.getAllWindows()]
    
    def open(self, app: str):
        if not self._run_app(app):
            sleep(2)
            try:
                window_title = pwc.getAllAppsWindowsTitles()[app][0]
            except KeyError:
                window_title = pwc.getAllAppsWindowsTitles()[app.title()][0]
            app_window = pwc.getWindowsWithTitle(window_title)[0]
            window = {"app": app, "window": app_window}
            self.windows.append(window) 
            return 0
        else:
            return 1 
    
    def close(self, app: str):
        while True:
            for i in self.windows:
                if i["app"] == app:
                    i["window"].close()
                    self.windows.remove(i)
                    return 0
            if app.islower():
                app = app.title()
            else:
                return 1
        
    
    def show(self, app: str):
        while True:
            for i in self.windows:
                if i["app"] == app:
                    i["window"].show()
                    return 0
            if app.islower():
                app = app.title()
            else:
                return 1
    
    def hide(self, app: str):
        while True:
            for i in self.windows:
                if i["app"] == app:
                    i["window"].hide()
                    return 0
            if app.islower():
                app = app.title()
            else:
                return 1
    
    def focus(self, app: str):
        while True:
            for i in self.windows:
                if i["app"] == app:
                    i["window"].activate()
                    return 0
            if app.islower():
                app = app.title()
            else:
                return 1
    
    def get_opened_apps(self):
        return [i["app"] for i in self.windows]
    
    
    def _get_sxhkd_binds(self):
        self.keybinds = []
        for bind_or_err in read_sxhkdrc(f'/home/{os.getlogin()}/.config/sxhkd/sxhkdrc'):
            if isinstance(bind_or_err, SXHKDParserError):
                continue
            keybind = bind_or_err
            app = keybind.command.raw[0].strip()
            keys = keybind.hotkey.raw[0].replace("super", "win")
            keys = [i.strip() for i in keys.split("+")]
            self.keybinds.append({"app": app, "keys": keys})
    
    def _run_app(self, app_name):
        for i in self.keybinds:
            if app_name in i["app"]:
                pag.hotkey(*i["keys"])
                return 0
        else:
            return 1


if __name__ == "__main__":
    wm = SkynixWm()
    wm.open("alacritty")
    sleep(2)
    wm.hide("alacritty")
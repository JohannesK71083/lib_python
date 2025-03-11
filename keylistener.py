# V1.1

from typing import Any, Callable
from pynput import keyboard
import threading

_Key = keyboard.Key
_KeyCode = keyboard.KeyCode


__key_printout_active = False
__listener = None

def __on_press(key: _Key | _KeyCode | None) -> None:
    if __key_printout_active:
        print(f"+ {key}")

def __on_release(key: _Key | _KeyCode | None) -> None:
    if __key_printout_active:
        print(f"- {key}")


def start_key_printout() -> None:
    """starts printing out the pressed and released Keys"""
    global __listener
    global __key_printout_active
    __listener = keyboard.Listener(on_press=__on_press, on_release=__on_release)
    __listener.start()
    __key_printout_active = True

def stop_key_printout() -> None:
    """stops printing out the pressed and released Keys"""
    global __listener
    global __key_printout_active
    __key_printout_active = False
    if __listener != None:
        __listener.stop()
        __listener = None
    

class KeyListener:
    def __init__(self, callback: Callable[..., Any], combination: set[_Key | _KeyCode | None], unless_combination: set[_Key | _KeyCode | None] = set()):
        self.enabled = True
        self.__combination = combination
        self.__unless_combination = unless_combination
        self.__current: set[_Key |
                            _KeyCode | None] = set()
        self.__event_funct = callback
        self.__listener = keyboard.Listener(
            on_press=self.__on_press, on_release=self.__on_release)
        self.__listener.start()

    def __del__(self):
        if self.__listener.is_alive():
            self.__listener.stop()
        if not threading.current_thread() == self.__listener:
            self.__listener.join()

    def __on_press(self, key: _Key | _KeyCode | None):      
        if key in self.__combination or key in self.__unless_combination:
            self.__current.add(key)
            if all(k in self.__current for k in self.__combination) and not any(k in self.__current for k in self.__unless_combination) and self.enabled:
                self.__event_funct()

    def __on_release(self, key: _Key | _KeyCode | None):
        if key in self.__current:
            self.__current.remove(key)

if __name__ == "__main__":
    def callback():
        print("PRESSED")
    
    kl = KeyListener(callback, {keyboard.Key.alt_l, keyboard.KeyCode(char="a")})
    
    start_key_printout()

    while input("enter X to quit\n") != "X":
        pass
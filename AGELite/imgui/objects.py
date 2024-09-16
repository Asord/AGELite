from typing import Callable
from imgui_bundle import imgui

class UI_Object:
    """ meta class for UI objects related to imgui """
    def __init__(self, name: str):
        self.name = name
    
    def ui(self):
        raise NotImplementedError("This class should not be instantiated")

class UI_Window(UI_Object):
    """ class for windows related to imgui """
    def __init__(self, name: str, configurables: list = None):
        super().__init__(name)
        self.configurables = configurables or []
        self.show = False
        
    def add_configurable(self, configurable: object):
        """ configurable is an object with a ui() method that uses imgui """
        self.configurables.append(configurable)

    def toggle(self):
        self.show = not self.show

    def ui(self):
        if self.show:
            is_expand, self.show = imgui.begin(self.name, True)
            if is_expand:
                for configurable in self.configurables:
                    configurable.ui()
            imgui.end()

class UI_Menu(UI_Object):
    """ class for menus related to imgui """
    def __init__(self, name: str, entries: list[tuple[tuple, Callable]] = None):
        super().__init__(name)
        self.entries = entries or []
        
    def ui(self):
        if imgui.begin_menu(self.name, True):
            callbacks = []
            for entry_args, entry_callback in self.entries:
                clicked, _ = imgui.menu_item(*entry_args)
                if clicked:
                    callbacks.append(entry_callback)
            imgui.end_menu()
        
            for callback in callbacks:
                callback()

    def add_entry(self, entry_args: tuple, entry_callback: Callable):
        """ add an entry to the menu """
        """ entry_args: (name, hotkey, is_shortcut, is_checked) entry_callback: callable """
        self.entries.append((entry_args, entry_callback))

class UI_Multiline(UI_Object):
    """ class for multiline related to imgui """
    def __init__(self, name: str, text: list[str]=None, height: int=16):
        super().__init__(name)
        self.text = text if text is not None else []
        self.height = height
        
    def add_line(self, line: str):
        line = line.replace("\n", "")
        self.text.append(line)

    def add_lines(self, lines: list[str]):
        for line in lines:
            self.add_line(line)

    def remove_line(self, line_idx: int):
        if 0 <= line_idx < len(self.text):
            del self.text[line_idx]
    
    def clear(self):
        self.text.clear()

    def ui(self):
        changed, text = imgui.input_text_multiline(self.name, "\n".join(self.text), -1, 500, 300)

        if changed:
            split_input = text.split("\n")
            for i in range(len(split_input)):
                if i >= len(self.text):
                    self.add_line(split_input[i])
                else:
                    self.text[i] = split_input[i]

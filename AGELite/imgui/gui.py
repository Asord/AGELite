from typing import Callable, TYPE_CHECKING

from imgui_bundle.python_backends.opengl_backend import ProgrammablePipelineRenderer
from imgui_bundle import imgui

import pygame.event
import pygame.time
import pygame

from .objects import UI_Menu, UI_Window

if TYPE_CHECKING:
    from ...main import Main

################ imgui.integration #############################
"""
This class is provided by the  module but inherits from ProgrammablePipelineRenderer 
insteed of FixedPipelineRenderer. It is necessary to use a ProgrammablePipelineRenderer
in order to render with custom shaders and programmed pipelines. 
"""
class PygameRenderer(ProgrammablePipelineRenderer):
    key_map: dict[int, imgui.Key]
    modifier_map: dict[int, imgui.Key]

    def __init__(self):
        super(PygameRenderer, self).__init__()

        self._gui_time = None
        self._map_keys()

    def _map_keys(self):
        self.key_map = {
            pygame.K_LEFT: imgui.Key.left_arrow,
            pygame.K_RIGHT: imgui.Key.right_arrow,
            pygame.K_UP: imgui.Key.up_arrow,
            pygame.K_DOWN: imgui.Key.down_arrow,
            pygame.K_PAGEUP: imgui.Key.page_up,
            pygame.K_PAGEDOWN: imgui.Key.page_down,
            pygame.K_HOME: imgui.Key.home,
            pygame.K_END: imgui.Key.end,
            pygame.K_INSERT: imgui.Key.insert,
            pygame.K_DELETE: imgui.Key.delete,
            pygame.K_BACKSPACE: imgui.Key.backspace,
            pygame.K_SPACE: imgui.Key.space,
            pygame.K_RETURN: imgui.Key.enter,
            pygame.K_ESCAPE: imgui.Key.escape,
            pygame.K_KP_ENTER: imgui.Key.keypad_enter,

            pygame.K_LCTRL: imgui.Key.left_ctrl,
            pygame.K_RCTRL: imgui.Key.right_ctrl,
            pygame.K_LALT: imgui.Key.left_alt,
            pygame.K_RALT: imgui.Key.right_alt,
            pygame.K_RSHIFT: imgui.Key.right_shift,
            pygame.K_LSHIFT: imgui.Key.left_shift,
            pygame.K_LSUPER: imgui.Key.left_super,
            pygame.K_RSUPER: imgui.Key.right_super,

            # pygame.K_a: imgui.Key.a,
            # pygame.K_c: imgui.Key.c,
            # pygame.K_v: imgui.Key.v,
            # pygame.K_x: imgui.Key.x,
            # pygame.K_y: imgui.Key.y,
            # pygame.K_z: imgui.Key.z,
        }

        self.modifier_map = {
            pygame.K_LCTRL: imgui.Key.im_gui_mod_ctrl,
            pygame.K_RCTRL: imgui.Key.im_gui_mod_ctrl,
            pygame.K_LSHIFT: imgui.Key.im_gui_mod_shift,
            pygame.K_RSHIFT: imgui.Key.im_gui_mod_shift,
            pygame.K_LALT: imgui.Key.im_gui_mod_alt,
            pygame.K_RALT: imgui.Key.im_gui_mod_alt,
            pygame.K_LSUPER: imgui.Key.im_gui_mod_super,
            pygame.K_RSUPER: imgui.Key.im_gui_mod_super,
        }

    def process_event(self, event):
        # perf: local for faster access
        io = self.io

        if event.type == pygame.MOUSEMOTION:
            io.add_mouse_pos_event(event.pos[0], event.pos[1])
            return True

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            down = event.type == pygame.MOUSEBUTTONDOWN
            imgui_button = event.button - 1
            io.add_mouse_button_event(imgui_button, down)
            return True

        if event.type == pygame.MOUSEWHEEL:
            k = 0.5
            io.add_mouse_wheel_event(event.x * k, event.y * k)
            return True

        processed_special_key = False
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            is_down = event.type == pygame.KEYDOWN
            if event.key in self.key_map.keys():
                io.add_key_event(self.key_map[event.key], down=is_down)
                processed_special_key = True
            if event.key in self.modifier_map.keys():
                io.add_key_event(self.modifier_map[event.key], down=is_down)
                processed_special_key = True

        if event.type == pygame.KEYDOWN and not processed_special_key:
            for char in event.unicode:
                code = ord(char)
                if 0 < code < 0x10000:
                    io.add_input_character(code)

            return True

        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.get_surface()
            # note: pygame does not modify existing surface upon resize,
            #       we need to do it ourselves.
            pygame.display.set_mode(
                (event.w, event.h),
                flags=surface.get_flags(),
            )
            # existing font texure is no longer valid, so we need to refresh it
            self.refresh_font_texture()

            # notify imgui about new window size
            io.display_size = event.size

            # delete old surface, it is no longer needed
            del surface

            return True

    def process_inputs(self):
        io = imgui.get_io()

        current_time = pygame.time.get_ticks() / 1000.0

        if self._gui_time:
            io.delta_time = current_time - self._gui_time
        else:
            io.delta_time = 1.0 / 60.0
        if io.delta_time <= 0.0:
            io.delta_time = 1.0 / 1000.0
        self._gui_time = current_time
###############################################################################



class UI:
    """ imgui manager """
    def __init__(self, app: 'Main'):
        self.app = app

        imgui.create_context()
        
        self.imgui = PygameRenderer()

        self.imgui_io = imgui.get_io()
        self.imgui_io.display_size = self.app.f2_window_size

        self.show = False

        self.windows: dict[str, UI_Window] = {}
        self.menus: dict[str, UI_Menu] = {}

        self.add_menu("File", UI_Menu("File"))
        self.add_menu_entry("File", "Quit", self.app.exit, "Cmd+Q")

    def add_window(self, window_name: str, window: UI_Window):
        """ Add a new imgui window"""
        if window_name not in self.windows:
            self.windows[window_name] = window
        else:
            print(f"Window '{window_name}' already registered")

    def add_menu(self, menu_name: str, menu: UI_Menu):
        """ Add a new imgui menu"""
        if menu_name not in self.menus:
            self.menus[menu_name] = menu
        else:
            print(f"Menu '{menu_name}' already registered")

    def add_menu_entry(self, menu_name: str, entry_name: str, entry_callback: Callable, hotkey: str = "", is_selected: bool = False, is_enabled: bool = True):
        """ Add a new imgui menu entry"""
        if menu_name in self.menus:
            self.menus[menu_name].add_entry((entry_name, hotkey, is_selected, is_enabled), entry_callback)
        else:
            print(f"Menu '{menu_name}' not registered")

    def add_window_configurable(self, window_name: str, configurable: object):
        """ Add a new configurable to a window """
        if window_name in self.windows:
            if hasattr(configurable, "ui"):
                self.windows[window_name].add_configurable(configurable)
            else:
                print(f"Window '{window_name}' has no ui method")
        else:
            print(f"Window '{window_name}' not registered")

    def toggle_window(self, window_name: str):
        """ Show a window """
        if window_name in self.windows:
            self.windows[window_name].toggle()


    def render(self):
        """ render the imgui. Called at each frame """
        imgui.new_frame()

        if self.show:
            if imgui.begin_main_menu_bar():
                for _, menu in self.menus.items():
                    menu.ui()
                imgui.end_main_menu_bar()
            for _, window in self.windows.items():
                window.ui()  


        imgui.render()
        self.imgui.render(imgui.get_draw_data())

            

    
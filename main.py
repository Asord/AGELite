from tkinter import Tk

import pygame as pg
import glm

from AGELite import *
from AGELite.imgui.logging import UI_Logger
from AGELite.imgui.gui import UI_Menu, UI_Window
from AGELite.imgui.arrow import GUI_Arrow

from ui import UI_SceneWindow, UI_ToolsWindow
from scene import Scene


class Main(Window):
    """ Example a main window object """
    def __init__(self, win_size: tuple[int, int]=(1920, 1080)):
        super().__init__(win_size=win_size)

        # load and init a scene
        self.scene = Scene(self)
        self.scene.init()

        ### IMGUI UTILS ###
        # creating all custom imgui windows and componants
        self.gui_arrow = GUI_Arrow(self.scene, glm.vec3(0))
        self.ui_tools = UI_ToolsWindow(self.scene)
        self.ui_scene = UI_SceneWindow(self)

        # setting up the windows and componants for imgui
        self.gui.add_window("Settings", UI_Window("Settings"))
        self.gui.add_window_configurable("Settings", self)
        self.gui.add_window_configurable("Settings", UI_Logger)
        self.gui.add_menu_entry("File", "Open settings", lambda: self.gui.toggle_window("Settings"))

        self.gui.add_menu("Edit", UI_Menu("Edit"))

        self.gui.add_window("Tools", UI_Window("Tools"))
        self.gui.add_window_configurable("Tools", self.ui_tools)
        self.gui.add_menu_entry("Edit", "Tools", lambda: self.gui.toggle_window("Tools"))

        self.gui.add_window("Scene", UI_Window("Scene"))
        self.gui.add_window_configurable("Scene", self.ui_scene)
        self.gui.add_menu_entry("Edit", "Scene", lambda: self.gui.toggle_window("Scene"))

        # setting defaults for imgui 
        self.gui.toggle_window("Settings")
        self.gui.toggle_window("Tools")
        self.gui.toggle_window("Scene")
        self.gui.show = True
        self.b_mouse_visible = self.gui.show
        pg.mouse.set_visible(self.b_mouse_visible)
        pg.event.set_grab(not self.b_mouse_visible)

        # custom default program uniform
        Program.get("default").set("smooth_normals", self.ui_tools.doSmoothNormals)


    def update(self):
        """ called at each frame before rendering"""
        super().update()   
        self.ui_tools.textures.run_all()
        self.gui_arrow.update_from_lc(self.scene.directional_light, self.scene.camera)

    def render(self):
        """ called at each frame """
        self.gui_arrow.redraw()
        super().render()

if __name__ == '__main__':
    app = Main()
    Tk().wm_withdraw() # Creating a headless Tk window for file dialog use
    app.run() # run the main loop

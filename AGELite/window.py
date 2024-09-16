import sys

from imgui_bundle import imgui
import OpenGL.GL as gl
import moderngl as mgl
import pygame as pg
import glm

from .imgui.gui import UI

from typing import TYPE_CHECKING
if TYPE_CHECKING: from scene import Scene

class Window:
    """ Main window class """
    def __init__(self, win_size: tuple[int, int]=(1600, 900)):

        """ Setting up pygame """
        pg.init()
        self.f2_window_size = self.f_window_width, self.f_window_height = win_size

        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.f2_window_size, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        self.ctx = mgl.create_context()

        """ Initializing GUI """
        self.gui = UI(self)

        """ Setting up time """
        self.clock = pg.time.Clock()
        self.f_time: float         = 0.0 # total time from start in seconds
        self.f_elapsed_time: float = 0.0 # total time from start in ms
        self.f_deltatime: float    = 0.0 # time of last frame in ms
        
        """ Configuring the mouse """
        pg.event.set_grab(True)
        self.b_mouse_visible = False
        pg.mouse.set_visible(self.b_mouse_visible)

        self.scene: 'Scene' = None

    """ Event handlers """
    def show_gui(self):
        self.gui.show = True
        self.release_mouse()

    def hide_gui(self):
        self.gui.show = False
        self.grab_mouse()

    def grab_mouse(self):
        pg.event.set_grab(True)
        self.b_mouse_visible = False
        pg.mouse.set_visible(self.b_mouse_visible)

    def release_mouse(self):
        pg.event.set_grab(False)
        self.b_mouse_visible = True
        pg.mouse.set_visible(self.b_mouse_visible)

    def mouse_move(self, rel_x, rel_y):
        if rel_x != 0 or rel_y != 0:
            self.scene.camera.set_rotation(self.scene.camera.v2_rotation + glm.vec2(rel_x, -rel_y)*0.1)

    """ Input handlers """
    def on_key_press(self, key):
        if key == pg.K_F1: # toggle gui
            self.show_gui() if not self.gui.show else self.hide_gui()
        if key == pg.K_F2: # toggle mouse
            self.grab_mouse() if self.b_mouse_visible else self.release_mouse()

    def on_keys_hold(self, keys):
        velocity = 0.005 * self.f_deltatime

        inputs = glm.vec3(velocity *     (keys[pg.K_d] - keys[pg.K_q]),
                          velocity *     (keys[pg.K_z] - keys[pg.K_s]),
                          velocity * (keys[pg.K_SPACE] - keys[pg.K_LSHIFT]))

        if inputs != glm.vec3(0, 0, 0):
            if self.scene.camera.camera_mode == self.scene.camera.MODE_LOCK:
                translation  = self.scene.camera.v3_forward * inputs.z
                translation += self.scene.camera.v3_right   * inputs.x
                translation += self.scene.camera.v3_up      * inputs.y

            elif self.scene.camera.camera_mode == self.scene.camera.MODE_FREE:
                translation  = self.scene.camera.v3_forward * inputs.y
                translation += self.scene.camera.v3_right   * inputs.x
                translation += self.scene.camera.v3_up      * inputs.z

            if translation != glm.vec3(0, 0, 0):
                self.scene.camera.set_translation(translation)

    def on_quit(self):
        pass

    def check_events(self):
        """ Check for events """
        events: list = pg.event.get()
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.on_quit()
                self.exit()

            if (event.type==pg.MOUSEMOTION) and (self.scene.camera.camera_mode==self.scene.camera.MODE_FREE) and (not self.b_mouse_visible):
                self.mouse_move(*event.rel)

            elif event.type == pg.KEYDOWN:
                self.on_key_press(event.key)

            self.gui.imgui.process_event(event)
        self.gui.imgui.process_inputs()

        self.on_keys_hold(pg.key.get_pressed())
    

    def render(self):
        """ Render the scene """
        self.ctx.screen.use()
        self.ctx.clear(color=(0.01, 0.2, 0.18))            
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        gl.glShadeModel(gl.GL_SMOOTH)
        self.scene.render()
        self.ctx.disable(mgl.DEPTH_TEST | mgl.CULL_FACE)

    def update(self):
        """ Update the scene """
        pass

    def run(self):
        """ Main loop """
        while True:
            self.check_events()

            self.update()
            self.scene.update()

            self.render()
            self.gui.render()

            pg.display.flip()

            self.f_time = self.f_elapsed_time * 0.001
            self.f_deltatime = self.clock.tick(60)
            self.f_elapsed_time += self.f_deltatime

    def exit(self):
        pg.quit()
        sys.exit()

    def ui(self):
        imgui.separator()
        imgui.text(f"FPS : {self.clock.get_fps() :.2f} fps | ")
        imgui.same_line()
        imgui.text(f"Window size : {self.f_window_width}x{self.f_window_height} pixels | ")
        imgui.same_line()
        imgui.text(f"Current delta time : {self.f_deltatime :.2f} ms | ")
        imgui.same_line()
        imgui.text(f"Current time : {self.f_time :.2f} s | ")
            

from pathlib import Path

import glm
import numpy as np
from imgui_bundle import imgui

from AGELite import *

from typing import TYPE_CHECKING
if TYPE_CHECKING: from main import Main

class Scene:
    """ Example of a scene """
    def __init__(self, window: 'Main'):
        self.win = window
    
        ### CAMERA ###
        self.camera = Camera(position=glm.vec3(0, 0, 0), rotation=glm.vec2(0, 0), aspect=self.win.f_window_width / self.win.f_window_height)
        self.camera.set_position(self.camera.v3_position - self.camera.v3_forward * 3)
        self.camera.set_rotation(glm.vec2(270, 0))
        
        ### LIGHTS ###
        self.directional_light = DirectionalLight()
        self.directional_light.rotate(glm.vec3(0, 0, 270))

        ### OBJECTS ###
        self.program = Program.create("default", self.win.ctx) # default shader (will look for a default.vert and default.frag from the shaders folder)
        self.object = None
        self.cube_vbo = None
        self.sphere_vbo = None
        self.object_vao = None
        self.object_kind = ""

        ### SKYBOX ###
        self.skybox_texture = Texture.cube_map(self.win.ctx, Path("res/Textures/skybox"))
        self.skybox = Skybox(self.camera, self.skybox_texture)
        self.skybox_shader = Program.create("skybox", ctx=self.win.ctx, vertex_shader_path=Program.SKYBOX_VERTEX_PATH, fragment_shader_path=Program.SKYBOX_FRAGMENT_PATH, formats=Program.SKYBOX_FMTS, attrs=Program.SKYBOX_ATTRS)
        self.skybox_vbo = self.win.ctx.buffer(new_triangle_screen())
        self.skybox_vao = self.win.ctx.vertex_array(self.skybox_shader.program, [(self.skybox_vbo, self.skybox_shader.formats, *self.skybox_shader.attrs)], skip_errors=True)

        # set default object
        self.set_sphere()

    def set_cube(self):
        """ set the cube object """
        with UniformContext(self.program): # saving uniforms values

            # releasing old vao
            if self.object_vao is not None:
                self.object_vao.release()

            # creating new vbo if it doesn't exist yet
            if self.cube_vbo is None:
                cube_primitive: np.ndarray = new_cube() 
                vertex_data = cube_primitive.tobytes()
                self.cube_vbo = self.win.ctx.buffer(vertex_data)
            
            # setting new vao and disabling smooth normals
            self.object_kind = "cube"
            self.object_vao = self.win.ctx.vertex_array(self.program.program, [(self.cube_vbo, self.program.formats, *self.program.attrs)] , skip_errors=True)
            self.program.set("smooth_normals", False)

    def set_sphere(self):
        """ set the sphere object """
        with UniformContext(self.program): # saving uniforms values
            
            # releasing old vao
            if self.object_vao is not None:
                self.object_vao.release()

            # creating new vbo if it doesn't exist yet
            if self.sphere_vbo is None:
                sphere_primitive: np.ndarray = new_sphere()
                vertex_data = sphere_primitive.tobytes()
                self.sphere_vbo = self.win.ctx.buffer(vertex_data)

            # setting new vao and enabling smooth normals
            self.object_kind = "sphere"
            self.object_vao = self.win.ctx.vertex_array(self.program.program, [(self.sphere_vbo, self.program.formats, *self.program.attrs)], skip_errors=True) 
            self.program.set("smooth_normals", True)
        

    def init(self):
        """ called at the start of the scene """
        self.program.set("v2_resolution", self.win.f2_window_size)
        self.object = Model(position=glm.vec3(0, 0, 0))

    def update(self):
        """ called at each frame before rendering"""
        self.camera.update("default")
        self.directional_light.update("default")
        if self.object is not None:
            self.object.update("default")
        self.skybox.update("skybox")

    def render(self):
        """ called at each frame """
        self.object_vao.render()
        self.skybox_vao.render()



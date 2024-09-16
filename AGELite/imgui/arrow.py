from pathlib import Path
from typing import TYPE_CHECKING

import glm
import moderngl as mgl
from imgui_bundle import imgui

from ..core.geometry import new_arrow, bake_tangants
from ..core.program import Program
from ..entity.renderable import Model
from .objects import UI_Object

if TYPE_CHECKING:
    from ...main import Scene
    from ..entity.lighting import DirectionalLight
    from ..entity.camera import Camera

# CAUTION: this code is not optimized and is not meant to be used in production. It is just made for easy debugging.

class GUI_Arrow(UI_Object): 
    """ Arrow GUI object to create a simple 3d arrow for vector visualization """

    # only one instance (for now)
    instance: ('GUI_Arrow|None') = None

    def __init__(self, scene: 'Scene', vector: glm.vec3, color: glm.vec3 = glm.vec3(0.4, 0.6, 0.0), size: tuple[int, int]=(175, 175)) -> None:
        # singleton check
        if GUI_Arrow.instance is not None:
            raise Exception("Only one instance of GUI_Arrow can exist at a time")
        
        super().__init__("#gui_arrow")
        GUI_Arrow.instance = self

        # vector that represents the model "direction"
        self.vector = vector
        
        self.scene = scene
        self.ctx = self.scene.win.ctx
        self.size = size

        # mgl elements
        self.blank_program = Program.create("blank", self.ctx, vertex_shader_path=Program.SHADER_FOLDER.joinpath("blank.vert"), fragment_shader_path=Program.SHADER_FOLDER.joinpath("blank.frag"), formats=Program.DEFAULT_FMTS, attrs=Program.DEFAULT_ATTRS)
        self.vbo = self.ctx.buffer(new_arrow())
        self.vao = self.ctx.vertex_array(self.blank_program.program, [(self.vbo, self.blank_program.formats, *self.blank_program.attrs)], skip_errors=True)
        self.output = self.ctx.texture(size, 4)
        self.depth = self.ctx.depth_texture(size)
        self.fbo = self.ctx.framebuffer(color_attachments=self.output, depth_attachment=self.depth)

        self.model = Model()

        self.color = color
        self.background_color = glm.vec4(0.0, 0.0, 0.0, 0.0)

        self.init()

    def init(self):
        """ Initializes the program """
        self.blank_program.write("m_proj", glm.perspective(glm.radians(60.0), 1.0, 0.1, 100.0))
        self.blank_program.write("m_view", glm.lookAt(glm.vec3(0, 0, 8), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0)))


    def redraw(self) -> None:   
        """ Redraw the arrow """  
        self.blank_program.write("color", self.color)
        self.fbo.use()
        self.fbo.clear(color=self.background_color.to_tuple())
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.vao.render()
        self.ctx.disable(mgl.DEPTH_TEST | mgl.CULL_FACE)

    def release(self) -> None:
        """ Releases the mgl elements """
        self.fbo.release()
        self.vao.release()
        self.output.release()
        self.depth.release()
        self.vbo.release()

    def update_from_lc(self, light: 'DirectionalLight', camera: 'Camera') -> None:
        """ Updates the arrow based on the light and the camera """
        if self.vector != light.v3_direction:
            self.vector = glm.normalize(light.v3_direction)
            self.model.rotation = -glm.vec3(0, 0, 90) -glm.vec3(light.v3_rotation.y, 0.0, light.v3_rotation.z)
            self.model.m_model = self.model.get_model_matrix()

        camera_m_view = glm.lookAt(glm.normalize(camera.v3_position)*8, camera.v3_position + camera.v3_forward, camera.v3_up)
        self.blank_program.write("m_view", camera_m_view)
        self.model.update("blank")
        self.redraw()

    def ui(self):
        imgui.begin_group()
        is_color_picked, color_picked = imgui.color_edit3("Arrow color", self.color.to_tuple(), flags=imgui.ColorEditFlags_.no_inputs)
        is_background_picked, background_picked = imgui.color_edit4("Arrow background", self.background_color.to_tuple(), flags=imgui.ColorEditFlags_.no_inputs)
        imgui.end_group()
        imgui.image(self.output.glo, self.size)

        if is_color_picked:
            self.color = glm.vec3(*color_picked)
        if is_background_picked:
            self.background_color = glm.vec4(*background_picked)




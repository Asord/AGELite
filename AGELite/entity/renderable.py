from typing import TYPE_CHECKING

import moderngl as mgl
import glm

from ..imgui.utils.pretty import imgui, UI_GLM_Pretty
from ..core.texture import TEXTURE
from ..core.program import Program

if TYPE_CHECKING:
    from AGELite import Camera
    

class Renderable:
    """ Renderable abstract class """
    def __init__(self): raise NotImplementedError("This class should not be instantiated")
    def update(self): ...

class Model(Renderable):
    """ Model class """
    def __init__(self, position: glm.vec3=glm.vec3(0, 0, 0), scale: glm.vec3=glm.vec3(1, 1, 1), rotation: glm.vec3=glm.vec3(0, 0, 0)):
        self.position = position
        self.scale = scale
        self.rotation = rotation

        self.m_model = self.get_model_matrix()

    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.position)
        m_model = glm.rotate(m_model, glm.radians(self.rotation.z), glm.vec3(0, 0, 1)) 
        m_model = glm.rotate(m_model, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        m_model = glm.scale(m_model, self.scale)
        return m_model
    
    def update(self, program_name: str):
        Program.get(program_name).write("m_model", self.m_model)

    def ui(self):
        b_position_updated, v3_position = imgui.drag_float3(label="Model position", v=self.position.to_tuple())
        b_rotation_updated, v3_rotation = imgui.drag_float3(label="Model rotation", v=self.rotation.to_tuple(), v_min=0, v_max=360, flags=imgui.SliderFlags_.wrap_around)
        b_scale_updated, v3_scale = imgui.drag_float3(label="Model scale", v=self.scale.to_tuple())
        imgui.separator()
        imgui.text("Model matrix:")
        UI_GLM_Pretty.mat4f(self.m_model)

        if b_position_updated:
            self.position = glm.vec3(*v3_position)
            self.m_model = self.get_model_matrix()
        if b_scale_updated:
            self.scale = glm.vec3(*v3_scale)
            self.m_model = self.get_model_matrix()
        if b_rotation_updated:
            self.rotation = glm.vec3(*v3_rotation)
            self.m_model = self.get_model_matrix()



class Skybox(Renderable):
    """ Skybox class """
    def __init__(self, camera: 'Camera', skybox_texture: mgl.Texture):
        self.camera = camera

        self.m_view = glm.mat4(glm.mat3(camera.m_view))
        self.skybox_texture = skybox_texture

    def update(self, program_name: str):
        self.skybox_texture.use(location=TEXTURE.LOCATION.CUBEMAP.value)
        Program.get(program_name).set("cubemap", TEXTURE.LOCATION.CUBEMAP.value)
        self.m_view = glm.mat4(glm.mat3(self.camera.m_view))
        Program.get(program_name).write("m_invProjView", glm.inverse(self.camera.m_projection * self.camera.m_view))

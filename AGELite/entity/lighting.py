import glm

from ..imgui.utils.pretty import imgui, UI_GLM_Pretty
from ..imgui.arrow import GUI_Arrow
from ..imgui.logging import UI_Logger as Log
from ..core.program import Program


class Light:
    """ Light class (generic object) """
    def __init__(self, position: glm.vec3=glm.vec3(0, 0, 0), color: glm.vec3=glm.vec3(1, 1, 1), ambient: float=0.06, diffuse: float=0.8, specular: float=1.0):
        self.v3_position = position

        self.f_ambient  = ambient
        self.f_diffuse  = diffuse
        self.f_specular = specular

        self.v3_color = color
        self.v3_Ia = self.f_ambient  * self.v3_color
        self.v3_Id = self.f_diffuse  * self.v3_color
        self.v3_Is = self.f_specular * self.v3_color

    def update(self, program_name: str, uniform_base_name: str):
            self.v3_Ia = self.f_ambient * self.v3_color
            Program.get(program_name).write(f"{uniform_base_name}.Ia", self.v3_Ia)
            self.v3_Id = self.f_diffuse * self.v3_color
            Program.get(program_name).write(f"{uniform_base_name}.Id", self.v3_Id)
            self.v3_Is = self.f_specular * self.v3_color
            Program.get(program_name).write(f"{uniform_base_name}.Is", self.v3_Is)

    
    def ui(self):
        update_light_pos, lpos = imgui.drag_float3(label="Light position", v=self.v3_position.to_tuple())
        imgui.separator()
        update_light_color, lcolor = imgui.color_edit3("Light color", col=self.v3_color.to_tuple(), flags=imgui.ColorEditFlags_.hdr)
        updated_amb, amb = imgui.slider_float(label="Light ambient", v=self.f_ambient, v_min=0.0, v_max=1.0) 
        updated_diff, diff = imgui.slider_float(label="Light diffuse", v=self.f_diffuse, v_min=0.0, v_max=1.0)
        updated_spec, spec = imgui.slider_float(label="Light specular", v=self.f_specular, v_min=0.0, v_max=1.0)

        if update_light_pos: 
            self.v3_position = glm.vec3(*lpos)

        if update_light_color: 
            self.v3_color = glm.vec3(*lcolor)
        else:
            if updated_amb: 
                self.f_ambient = amb

            if updated_diff: 
                self.f_diffuse = diff

            if updated_spec: 
                self.f_specular = spec



class DirectionalLight(Light):
    """ Directional light class """

    def __init__(self, rotation: glm.vec3=glm.vec3(0, 0, 0), color: glm.vec3=glm.vec3(1, 1, 1), ambient: float=0.06, diffuse: float=0.8, specular: float=1.0, shadowcaster: bool=False):
        Light.__init__(self, glm.vec3(0, 0, 0), color, ambient, diffuse, specular)
        
        self.b_shadowcaster = shadowcaster

        self.v3_rotation = rotation
        self.v3_direction = glm.vec3(1, 0, 0)

        self.m_view_light = glm.lookAt(self.v3_position, self.v3_direction, glm.vec3(0, 1, 0)) # shadow view matrix
    
    def rotate(self, rotation: glm.vec3):
        self.v3_rotation = rotation
        self.v3_direction = glm.rotate(glm.vec3(1.0, 0.0, 0.0), glm.radians(self.v3_rotation.x), glm.vec3(1, 0, 0))
        self.v3_direction = glm.rotate(self.v3_direction, glm.radians(self.v3_rotation.y), glm.vec3(0, 1, 0))
        self.v3_direction = glm.rotate(self.v3_direction, glm.radians(self.v3_rotation.z), glm.vec3(0, 0, 1))

    def update(self, program_name: str, shadow_program_name: str=None):
        Light.update(self, program_name, "directional_light.light")
        Program.get(program_name).set("directional_light.direction", self.v3_direction)
        #Program.get(program_name).set("directional_light.shadowable", self.b_shadowcaster)

        if self.b_shadowcaster and shadow_program_name is not None and Program.exists(shadow_program_name):
            self.m_view_light = glm.lookAt(self.v3_position, self.v3_direction, glm.vec3(0, 1, 0))
            Program.get(program_name).write("directional_light.m_view_light", self.m_view_light)


    def ui(self):
        imgui.begin_table("#light_data", 2, imgui.TableFlags_.row_bg | imgui.TableFlags_.sizing_fixed_fit)
        imgui.table_next_row()
        imgui.table_next_column()

        imgui.begin_group()
        Light.ui(self) 
        imgui.end_group()

        imgui.separator()
        imgui.begin_group()
        imgui.text("Light direction:")
        imgui.same_line()
        UI_GLM_Pretty.vec3f(self.v3_direction, inline=False)
        b_update_rotation, rotation = imgui.drag_float3(label="Light rotation", v=self.v3_rotation.to_tuple(), v_min=0.0, v_max=360.0, flags=imgui.SliderFlags_.wrap_around)
        imgui.end_group()

        imgui.begin_group()
        b_update_shadowcaster, is_shadow_caster = imgui.checkbox("Is shadowcaster ?", self.b_shadowcaster)
        if self.b_shadowcaster:
            imgui.text(f" Light View matrix:")
            UI_GLM_Pretty.mat4f(self.m_view_light)
        imgui.end_group()

        imgui.table_next_column()
        if GUI_Arrow.instance is not None: 
            GUI_Arrow.instance.ui()

        imgui.end_table()

        

        if b_update_shadowcaster:
            self.b_shadowcaster = is_shadow_caster

        if b_update_rotation: 
            self.rotate(glm.vec3(*rotation))
        

class PointLight(Light):
    """ Point light class """
    _MAX_POINT_LIGHTS = 3
    _POINT_LIGHTS = [None] * _MAX_POINT_LIGHTS

    @staticmethod
    def _addPointLight(pointLight: 'PointLight') -> int:
        for i in range(PointLight._MAX_POINT_LIGHTS):
            if PointLight._POINT_LIGHTS[i] is None:
                PointLight._POINT_LIGHTS[i] = pointLight
                return i
        return -1

    def __init__(self, position: glm.vec3=glm.vec3(0, 0, 0), color: glm.vec3=glm.vec3(1, 1, 1), ambient: float=0.06, diffuse: float=0.8, specular: float=1.0, constant: float=1.0, linear: float=0.09, quadratic: float=0.032):
        Light.__init__(self, position, color, ambient, diffuse, specular)
        self.f_constant = constant
        self.f_linear = linear
        self.f_quadratic = quadratic

        # do not destroy the point light but do not add it to the renderer
        self.n_index = PointLight._addPointLight(self)
        if self.n_index == -1:
            Log.print("Too many point lights; max is %d" % PointLight._MAX_POINT_LIGHTS)
    

    def enable(self, program_name: str):
        if self.n_index == -1:
            self.n_index = PointLight._addPointLight(self)
        if self.n_index == -1:
            Log.print("Too many point lights; max is %d" % PointLight._MAX_POINT_LIGHTS)
            return
        
        Program.get(program_name).set(f'point_lights[{self.n_index}].enabled', 1)
        
    def disable(self, program_name: str):
        if self.n_index != -1 and Program.exists(program_name):
            Program.get(program_name).set(f'point_lights[{self.n_index}].enabled', 0)
            PointLight._POINT_LIGHTS[self.n_index] = None
            self.n_index = -1

    def update(self, program_name: str):
            Program.get(program_name).write(f'point_lights[{self.n_index}].light.position', self.v3_position)
            Program.get(program_name).set(f'point_lights[{self.n_index}].constant', self.f_constant)
            Program.get(program_name).set(f'point_lights[{self.n_index}].linear', self.f_linear)
            Program.get(program_name).set(f'point_lights[{self.n_index}].quadratic', self.f_quadratic)
            Light.update(self, program_name, f'point_lights[{self.n_index}].light')

    def ui(self):
        Light.ui(self)
        imgui.separator()
        b_update_constant,  f_constant  = imgui.slider_float(label="Constant",  v=self.f_constant,  v_min=0.0, v_max=1.0)
        b_update_linear,    f_linear    = imgui.slider_float(label="Linear",    v=self.f_linear,    v_min=0.0, v_max=1.0)
        b_update_quadratic, f_quadratic = imgui.slider_float(label="Quadratic", v=self.f_quadratic, v_min=0.0, v_max=1.0)

        if b_update_constant: 
            self.f_constant = f_constant

        if b_update_linear: 
            self.f_linear = f_linear

        if b_update_quadratic: 
            self.f_quadratic = f_quadratic
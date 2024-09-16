import glm

from ..imgui.utils.pretty import imgui, UI_GLM_Pretty, UI_Text_Pretty
from ..core.program import Program

class CAMERA:
    """ Global camera parameters """
    FOV = 80
    NEAR = 0.1
    FAR = 1000


class Camera:
    """ Camera class """
    MODE_LOCK = 0
    MODE_FREE = 1

    def __init__(self, position: glm.vec3, rotation: glm.vec2, near: float=CAMERA.NEAR, far: float=CAMERA.FAR, fov: float=CAMERA.FOV, aspect: float=1):
        
        self.v3_position = position
        
        self.v3_up = glm.vec3(0, 1, 0)
        self.v3_right = glm.vec3(1, 0, 0)
        self.v3_forward = glm.vec3(0, 0, -1)

        self.v2_rotation = rotation # only yaw and pitch

        self.f_fov = fov
        self.f_near = near
        self.f_far = far
        self.f_aspect = aspect

        self.n_pitch_max = 89
        self.n_pitch_min = -89
        
        self.camera_mode = Camera.MODE_LOCK

        self.m_view = self.get_view_matrix()
        self.m_projection = self.get_projection_matrix()


    def update(self, program_name: str, shadow_program_name: str=None):
        if self.camera_mode == Camera.MODE_LOCK:
            self.update_camera_vectors_lock()
        else:
            self.update_camera_vectors_freecam()

        Program.get(program_name).write("v3_camera_position", self.v3_position)
        Program.get(program_name).write("m_proj", self.m_projection)
        Program.get(program_name).write("m_view", self.m_view)

        if shadow_program_name is not None and Program.exists(shadow_program_name):
            Program.get(shadow_program_name).write("m_proj", self.m_projection)

    def update_camera_vectors_freecam(self):
        """update the camera vectors"""
        f_yaw, f_pitch = glm.radians(self.v2_rotation).to_tuple()

        self.v3_forward.x = glm.cos(f_yaw) * glm.cos(f_pitch)
        self.v3_forward.y = glm.sin(f_pitch)
        self.v3_forward.z = glm.sin(f_yaw) * glm.cos(f_pitch)

        self.v3_forward = glm.normalize(self.v3_forward)
        self.v3_right = glm.normalize(glm.cross(self.v3_forward, glm.vec3(0, 1, 0)))
        self.v3_up = glm.normalize(glm.cross(self.v3_right, self.v3_forward))

        self.m_view = self.get_view_matrix()

    def update_camera_vectors_lock(self):
        """update the camera vectors"""
        self.v3_forward = glm.normalize(-self.v3_position)
        self.v3_right = glm.normalize(glm.cross(self.v3_forward, glm.vec3(0, 1, 0)))
        self.v3_up = glm.normalize(glm.cross(self.v3_right, self.v3_forward))

        self.m_view = self.get_view_matrix()
    
    def get_view_matrix(self):
        return glm.lookAt(self.v3_position, self.v3_position + self.v3_forward, self.v3_up)
    
    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.f_fov), self.f_aspect, self.f_near, self.f_far)

    def set_position(self, position: glm.vec3) -> None:
        if self.camera_mode == Camera.MODE_LOCK: 
            if abs(position.x) < 1 and abs(position.z) < 1: 
                position.x = -1 if position.x < 0 else 1
                position.z = -1 if position.z < 0 else 1
                return
            
        self.v3_position = position

    def set_translation(self, translation: glm.vec3):
        self.set_position(self.v3_position + translation)

    def set_rotation(self, rotation: glm.vec2):
        if self.camera_mode == Camera.MODE_LOCK: return
        self.v2_rotation = glm.vec2(rotation.x, max(self.n_pitch_min, min(self.n_pitch_max, rotation.y)))

    def set_frustum(self, fov: float, aspect: float, near: float, far: float):
        self.f_fov = fov
        self.f_near = near
        self.f_far = far
        self.f_aspect = aspect
        self.m_projection = self.get_projection_matrix()

    def ui(self):
        b_position_updated, v3_position = imgui.drag_float3(label="Camera position", v=self.v3_position.to_tuple())
        b_rotation_updated, v2_rotation = imgui.drag_float2(label="Camera rotation", v=self.v2_rotation.to_tuple()[:2], v_min=-360, v_max=360, flags=imgui.SliderFlags_.wrap_around)

        imgui.separator()

        imgui.begin_table("#camera_data", 2, imgui.TableFlags_.row_bg | imgui.TableFlags_.sizing_fixed_fit)
        imgui.table_next_row()
        imgui.table_next_column()
        col_width = imgui.get_column_width()

        imgui.begin_group()
        b_fov_updated, f_fov = imgui.slider_float(label="Fov", v=self.f_fov, v_min=10, v_max=180)
        b_near_updated, f_near = imgui.slider_float(label="Near", v=self.f_near, v_min=0.1, v_max=100)
        b_far_updated, f_far = imgui.slider_float(label="Far", v=self.f_far, v_min=0.1, v_max=1000)
        imgui.end_group()

        UI_Text_Pretty.centered("Forward", col_width)
        UI_GLM_Pretty.vec3f(self.v3_forward, inline=False)
        UI_Text_Pretty.centered("Right", col_width)
        UI_GLM_Pretty.vec3f(self.v3_right, inline=False)
        UI_Text_Pretty.centered("Up", col_width)
        UI_GLM_Pretty.vec3f(self.v3_up, inline=False)

        imgui.table_next_column()
        col_width = (imgui.get_window_width() - col_width) * 2

        UI_Text_Pretty.centered("View Matrix", col_width)
        UI_GLM_Pretty.mat4f(self.m_view)
        UI_Text_Pretty.centered("Projection Matrix", col_width)
        UI_GLM_Pretty.mat4f(self.m_projection)

        imgui.end_table()

        if b_position_updated:
            self.set_position(glm.vec3(*v3_position))
        if b_rotation_updated:
            self.set_rotation(glm.vec2(*v2_rotation))
        if any([b_fov_updated, b_near_updated, b_far_updated]):
            f_fov  = f_fov  if b_fov_updated  else self.f_fov
            f_near = f_near if b_near_updated else self.f_near
            f_far  = f_far  if b_far_updated  else self.f_far
            self.set_frustum(f_fov, self.f_aspect, f_near, f_far)


from typing import TYPE_CHECKING
from imgui_bundle import imgui

from AGELite import *
from textureSwitcher import TextureSwitcher, TEXTURE

if TYPE_CHECKING: 
    from scene import Scene
    from main import Main

class UI_ToolsWindow:
    """ imgui window for tools (mostly program uniforms editor) """
    def __init__(self, scene: 'Scene'):
        self.scene = scene
        self.textures = TextureSwitcher(self.scene)

        self.doSwitchTexture = False
        self.doSwitchCubemap = False
        self.doSwitchPBR = False
        
        self.doToggleNormals = False
        self.doSmoothNormals = True

        self.cameraMode = 0
        self.object = 0

        self._objects = [self.scene.set_sphere, self.scene.set_cube]
        self._camera_modes = [Camera.MODE_LOCK, Camera.MODE_FREE]

        self._initialized = False

    @staticmethod
    def _radio_button(name: str, keys: list[str], initial_value: int=0) -> int:
        result = initial_value 
        changed = False

        imgui.text(name)
        nb_keys = len(keys)
        for i, key in enumerate(keys):
            if imgui.radio_button(key, result == i):
                result = i
                changed = True
            if i < nb_keys - 1:
                imgui.same_line()

        return changed, result

    def ui(self):
        imgui.separator_text("Shaders")
        b_reload_shaders = imgui.button("Reload shaders")                                                               # Button - Reload shaders
        b_switch_pbr, self.doSwitchPBR = imgui.checkbox("Switch PBR mode", self.doSwitchPBR)                            # Checkbox - Switch PBR

        imgui.separator_text("Textures")
        b_switch_cubemap, self.doSwitchCubemap = imgui.checkbox("Switch cubemap", self.doSwitchCubemap)                 # Checkbox - Switch cubemap
        b_switch_texture, self.doSwitchTexture = imgui.checkbox("Switch textures", self.doSwitchTexture)                # Checkbox - Switch textures
        
        if imgui.tree_node("Change textures"):                                                                          # Tree node - Change textures
            self.textures.ui()
            imgui.tree_pop()

        imgui.separator_text("Debug")
        b_toggle_normals, self.doToggleNormals = imgui.checkbox("Toggle normals", self.doToggleNormals)                 # Checkbox - Toggle normals
        b_smooth_normals, self.doSmoothNormals = imgui.checkbox("Smooth normals", self.doSmoothNormals)                 # Checkbox - Smooth normals

        imgui.separator_text("Toggles")
        b_toggle_camera_mode, self.cameraMode = UI_ToolsWindow._radio_button("Camera:", ("locked", "freecam"), self.cameraMode)  # Radio button - Camera mode
        imgui.same_line
        b_toggle_object, self.object = UI_ToolsWindow._radio_button("Object:", ("sphere", "cube"), self.object)                  # Radio button - Object 

        if b_switch_texture:
            if self.doSwitchTexture: self.textures.enable_all()
            else:                    self.textures.disable_all()

        if b_switch_cubemap:
            if self.doSwitchCubemap: TEXTURE.enableTexture(self.scene, "cubemap", self.scene.skybox_texture)
            else:                    TEXTURE.disableTexture(self.scene, "cubemap")
        
        if b_switch_pbr:
            if self.doSwitchPBR: self.scene.program.swap(Program.DEFAULT_VERTEX_PATH, Program.PBR_FRAGMENT_PATH)
            else:                self.scene.program.swap(Program.DEFAULT_VERTEX_PATH, Program.DEFAULT_FRAGMENT_PATH)

        if b_toggle_normals:
            Program.get("default").set("debug_show_normal", self.doToggleNormals)

        if b_smooth_normals:
            self.scene.program.set("smooth_normals", self.doSmoothNormals)

        if b_toggle_camera_mode:
            self.scene.camera.camera_mode = self._camera_modes[self.cameraMode]

        if b_toggle_object:
            self._objects[self.object]()
        
        if b_reload_shaders:
            self.scene.program.swap(Program.DEFAULT_VERTEX_PATH, Program.DEFAULT_FRAGMENT_PATH)


class UI_SceneWindow:
    """ imgui window for the scene elements """
    def __init__(self, app: 'Main'):
        self.app = app

    def ui(self):
        if imgui.collapsing_header("Camera"):
            self.app.scene.camera.ui()

        if imgui.collapsing_header("Light"):
            self.app.scene.directional_light.ui()

        if imgui.collapsing_header("Model"):
            self.app.scene.object.ui()

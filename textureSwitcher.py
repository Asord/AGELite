from typing import TYPE_CHECKING
if TYPE_CHECKING: from scene import Scene
from tkinter.filedialog import askopenfilename
from pathlib import Path

from imgui_bundle import imgui

from AGELite import Texture, TEXTURE
from AGELite.core.deferable import Deferable


class TextureSwitcher(Deferable):
    """ Utility class for switching textures dynamically using imgui """
    def __init__(self, scene: 'Scene'):
        super().__init__(["disable", "release", "load", "enable"]) # four deferred functions that can't be called during imgui drawing
        # Note: order is important. we disable textures, then release them, then load new ones, then enable them

        self.scene = scene
        self.ctx = self.scene.win.ctx

        # self.textures = {typeName: (texture, path), ...}
        self.textures: dict[str, tuple[Texture, Path]] = {}

        """ DEFAULT TEXTURES """
        self.load_texture("albedo"   , Path("res/Textures/Kintsugi/Kintsugi_001_basecolor.png"))
        self.load_texture("normal"   , Path("res/Textures/Kintsugi/Kintsugi_001_normal.png"))
        self.load_texture("metallic" , Path("res/Textures/Kintsugi/Kintsugi_001_metallic.png"))
        self.load_texture("roughness", Path("res/Textures/Kintsugi/Kintsugi_001_roughness.png"))
        self.load_texture("ao"       , Path("res/Textures/Kintsugi/Kintsugi_001_ambientOcclusion.png"))

        # self.enabled: [typeName, ...]
        self.enabled: list[str] = []
    
    # defered functions that will be called after imgui drawing
    @Deferable.defer("load")
    def load_texture(self, key: str, path: Path):
        if key in self.textures: raise ValueError(f"key {key} already in self.textures. Please release it first.")
        self.textures[key] = (Texture.from_file(self.ctx, path), path)

    @Deferable.defer("enable")
    def enable_texture(self, key: str):
        if key not in self.textures or key in self.enabled: return        
        TEXTURE.enableTexture(self.scene, key, self.textures[key][0])
        self.enabled.append(key)

    @Deferable.defer("disable")
    def disable_texture(self, key: str):
        if key not in self.textures or key not in self.enabled: return
        self._disable_texture(key)

    @Deferable.defer("release")
    def release_texture(self, key: str):
        if key not in self.textures: return
        self._disable_texture(key)
        self.textures[key][0].texture.release()

    # non-defered version of the disable texture for usage in defered functions
    def _disable_texture(self, key: str):
        if key not in self.enabled: return
        TEXTURE.disableTexture(self.scene, key)
        self.enabled.remove(key)

    # batch functions
    def enable_all(self):  [self.enable_texture(key)  for key in self.textures.keys()]
    def disable_all(self): [self.disable_texture(key) for key in self.textures.keys()]
    def release_all(self): [self.release_texture(key) for key in self.textures.keys()]

    def ui(self): 
        # imgui drawings

        imgui.begin_group()
        for key, value in self.textures.items():
            changed, val = imgui.checkbox(f"{key}", key in self.enabled)
            if changed: 
                if val: self.enable_texture(key)
                else:   self.disable_texture(key)

            imgui.same_line()
            if imgui.button(f"#{key}"):

                _new_path_result = askopenfilename(title = "Select file") # tkinter.filedialog.askopenfilename
                if _new_path_result is not None:
                    new_path = Path(_new_path_result)
                    if new_path is not None and new_path.exists() and new_path.is_file() and new_path.suffix in (".png", ".jpg", ".jpeg", ".bmp"):
                        if key in self.enabled:
                            self.release_texture(key)
                            self.enable_texture(key)
                        self.load_texture(key, new_path)
            
            imgui.set_item_tooltip("Path: " + str(value[1]))

        imgui.end_group()

            


from typing import TYPE_CHECKING
from pathlib import Path
import enum

import PIL.Image as Image
import moderngl as mgl
import glm

if TYPE_CHECKING: 
    from scene import Scene

class TEXTURE:
    """ Texture globals """

    class LOCATION(enum.Enum):
        CUBEMAP = 0
        ALBEDO = 1
        METALLIC = 2
        SPECULAR = 3
        ROUGHNESS = 4
        NORMAL = 5
        EMMISIVE = 6
        AO = 7

    class FLAGS(enum.IntFlag):
        CUBEMAP = 1
        ALBEDO = 2
        METALLIC = 4
        SPECULAR = 8
        ROUGHNESS = 16
        NORMAL = 32
        EMMISIVE = 64
        AO = 128

    LOCATION_BY_NAME = {
        "cubemap"  : LOCATION.CUBEMAP,
        "albedo"   : LOCATION.ALBEDO,
        "metallic" : LOCATION.METALLIC,
        "specular" : LOCATION.SPECULAR,
        "roughness": LOCATION.ROUGHNESS,
        "normal"   : LOCATION.NORMAL,
        "emmision" : LOCATION.EMMISIVE,
        "ao"       : LOCATION.AO
    }

    FLAG_BY_NAME = {
        "cubemap"  : FLAGS.CUBEMAP,
        "albedo"   : FLAGS.ALBEDO,
        "metallic" : FLAGS.METALLIC,
        "specular" : FLAGS.SPECULAR,
        "roughness": FLAGS.ROUGHNESS,
        "normal"   : FLAGS.NORMAL,
        "emmision" : FLAGS.EMMISIVE,
        "ao"       : FLAGS.AO
    }

    FLAG_ENABLED = 0 # flags

    CUBEMAP_FACES = ["right", "left", "top", "bottom", "back", "front"]

    @staticmethod
    def enableTexture(scene: 'Scene', key: str, texture: 'Texture'):
        """ Enable a texture in the shader """
        TEXTURE.FLAG_ENABLED |= TEXTURE.FLAG_BY_NAME[key].value
        scene.program.set("enabled_maps", TEXTURE.FLAG_ENABLED)

        _LID = TEXTURE.LOCATION_BY_NAME[key]
        texture.use(_LID.value)
        scene.program.set(f"map_{key}", _LID.value)

    @staticmethod
    def disableTexture(scene: 'Scene', key: str):
        """ Disable a texture in the shader """
        TEXTURE.FLAG_ENABLED &= ~TEXTURE.FLAG_BY_NAME[key].value
        scene.program.set("enabled_maps", TEXTURE.FLAG_ENABLED)


class Texture:
    """ Texture class """
    @classmethod
    def cube_map(cls, ctx: mgl.Context, dir_path: Path):
        """ Create a cubemap from a directory of images 
        names should be "right", "left", "top", "bottom", "back", "front" """
        textures: list[Image.Image] = []

        for face in TEXTURE.CUBEMAP_FACES:
            path = dir_path.joinpath(face).with_suffix(".png")
            img = Image.open(path).convert('RGBA')
            if face in ["top", "bottom"]:
                img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            else:
                img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            textures.append(img)

        texture_cube = ctx.texture_cube(textures[0].size, components=4)
        for i, img in enumerate(textures):
            texture_cube.write(face=i, data=img.tobytes())

        return cls(ctx, texture_cube)
    
    @classmethod
    def depth_texture(cls, ctx: mgl.Context, size: glm.vec2):
        """ Create a depth texture """
        texture = ctx.depth_texture(size)
        texture.repeat_x = False
        texture.repeat_y = False
        return cls(ctx, texture)
        
    @classmethod
    def from_file(cls, ctx: mgl.Context, path: Path):
        """ Create a texture from a file """
        img = Image.open(path).convert('RGBA')
        img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        texture = ctx.texture(img.size, components=4, data=img.tobytes())

        return cls(ctx, texture)

    def __init__(self, ctx: mgl.Context, texture: mgl.Texture):
        self.ctx = ctx
        self.texture = texture
        
    
    def use(self, location: int = 0):
        """ Use the texture in the shader """
        if isinstance(location, enum.Enum):
            location = location.value
        self.texture.use(location=location)
    
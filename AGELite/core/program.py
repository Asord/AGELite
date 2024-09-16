from pathlib import Path
from os import walk
import re

import moderngl as mgl

from .debug import fmt_program_exception_on_build
from ..imgui.logging import UI_Logger as Log



class UniformContext:
    """
    Retreive all uniforms values when entering the context and set them when exiting

    Usage:
        with UniformContext(AGEProgram: Program):
            ...
    """
    def __init__(self, program: 'Program'):
        self.program = program
        self.uniforms = []

    def __enter__(self):
        """ Retreive all uniforms values """
        for elem in [self.program.program.get(k, None) for k in self.program.program]:
            if isinstance(elem, mgl.Uniform):
                self.uniforms.append((elem.name, elem.value))

    def __exit__(self, err_type, err_value, err_traceback):
        """ Set all uniforms values """
        if err_type is None: 
            for uniform in self.uniforms:
                self.program.set(uniform[0], uniform[1])



class Program:
    """ Program object to store and manage mgl.program objects"""

    # defaults
    SHADER_FOLDER = Path("res/shaders")

    DEFAULT_VERTEX_PATH   = SHADER_FOLDER.joinpath("default.vert")
    DEFAULT_FRAGMENT_PATH = SHADER_FOLDER.joinpath("default.frag")
    PBR_FRAGMENT_PATH     = SHADER_FOLDER.joinpath("pbr.frag")
    DEFAULT_FMTS = "2f 3f 3f 3f 3f"
    DEFAULT_ATTRS = ("in_uv", "in_bitangent","in_tangent", "in_normal", "in_vertex",)
    
    SKYBOX_VERTEX_PATH   = SHADER_FOLDER.joinpath("skybox.vert")
    SKYBOX_FRAGMENT_PATH = SHADER_FOLDER.joinpath("skybox.frag")
    SKYBOX_FMTS = "3f"
    SKYBOX_ATTRS = ("in_vertex",)

    SHADER_INCLUDE_DIRECTORY = "common"
    SHADER_INCLUDE_PATH = SHADER_FOLDER.joinpath(SHADER_INCLUDE_DIRECTORY)

    List: dict[str, 'Program'] = {}
    
    @staticmethod
    def load_shader_file(path: Path):
        """ load string file from path """
        if path.exists():
            return path.read_text()
        return None

    @staticmethod
    def get(name: str) -> 'Program':
        """ get program by name """
        if name in Program.List:
            return Program.List[name]
        else:
            return None
        
    @staticmethod
    def get_name(program: 'Program') -> str:
        """ get name of the program """
        for name, prog in Program.List.items():
            if prog == program:
                return name
        return None
    
    @staticmethod
    def exists(name: str) -> bool:
        """ check if program exists by name """
        return name in Program.List
    
    @staticmethod
    def create(name: str, ctx: mgl.Context, vertex_shader_path: str=DEFAULT_VERTEX_PATH, fragment_shader_path: str=DEFAULT_FRAGMENT_PATH, formats: str=DEFAULT_FMTS, attrs: tuple[str, ...]=DEFAULT_ATTRS):
        """ create new program """
        Program.List[name] = Program(ctx, vertex_shader_path, fragment_shader_path, formats, attrs)
        return Program.List[name]
    
    @staticmethod
    def _load_include_files(ctx: mgl.Context) -> str:
        """ load include files declared with the #include directive """
        if len(ctx.includes) > 0: return #includes already loaded
        common_path = Program.SHADER_INCLUDE_PATH
        for _,_,files in walk(common_path):
            for file in files:
                include_key = str(Path(Program.SHADER_INCLUDE_DIRECTORY).joinpath(file).as_posix())
                data        = common_path.joinpath(file).read_text()
                ctx.includes[include_key] = f"// INCLUDED FROM {file}\n{data}\n// EOI"

    @staticmethod
    def resolve_includes(ctx: mgl.Context, source: str):
        """ Extracted from moderngl.py source as-is. All copyrights belong to their respective owners. """
        def include(match: re.Match):
            name = match.group(1)
            content = ctx.includes.get(name)
            if content is None:
                raise KeyError(f'cannot include "{name}"')
            return content
        source = re.sub(r'#include\s+"([^"]+)"', include, source)
        return source


    def __init__(self, ctx: mgl.Context, vertex_shader_path: Path=DEFAULT_VERTEX_PATH, fragment_shader_path: Path=DEFAULT_FRAGMENT_PATH, formats: str=DEFAULT_FMTS, attrs: tuple[str, ...]=DEFAULT_ATTRS):
        self._load_include_files(ctx)
        self.ctx = ctx
        self.vertex_shader = Program.load_shader_file(vertex_shader_path)
        self.fragment_shader = Program.load_shader_file(fragment_shader_path)

        self.vertex_shader = Program.resolve_includes(self.ctx, self.vertex_shader)
        self.fragment_shader = Program.resolve_includes(self.ctx, self.fragment_shader)

        try:
            self.program = self.ctx.program(self.vertex_shader, self.fragment_shader)
        except Exception as e:
            raise fmt_program_exception_on_build(self.vertex_shader, self.fragment_shader, e)

        self.formats = formats
        self.attrs = attrs


    def swap(self, vertex_shader_path: Path|None=None, fragment_shader_path: Path|None=None):
        """ swap vertex and fragment shaders """
        if vertex_shader_path is not None:
            self.vertex_shader   = Program.load_shader_file(vertex_shader_path) or self.vertex_shader
            self.vertex_shader = Program.resolve_includes(self.ctx, self.vertex_shader)

        if fragment_shader_path is not None:
            self.fragment_shader = Program.load_shader_file(fragment_shader_path) or self.fragment_shader
            self.fragment_shader = Program.resolve_includes(self.ctx, self.fragment_shader)

        try:                                                                                            #
            _program = self.ctx.program(self.vertex_shader, self.fragment_shader)                       #
            _program.release()                                                                          #
        except Exception as e:                                                                          #  see notes.md -> Program shader hotswap
            raise fmt_program_exception_on_build(self.vertex_shader, self.fragment_shader, e)           # 
        else:                                                                                           #
            with UniformContext(self):                                                                  #
                self.program.release()                                                                  #                                   
                self.program = self.ctx.program(self.vertex_shader, self.fragment_shader)               #


    def getu(self, program_key: str, default=None):
        """ get uniform by key """
        if program_key in self.program:
            return self.program[program_key]
        else:
            Log.print(f"Unknown program key to get: '{program_key}' for Program '{Program.get_name(self)}'")
            return default

    def set(self, program_key, value):
        """ set uniform by key """
        if program_key in self.program:
            self.program[program_key] = value
        else:
            Log.print(f"Unknown program key to set: '{program_key}' for Program '{Program.get_name(self)}'")
        
    def write(self, program_key, value):
        """ write uniform by key """
        if program_key in self.program:
            self.program[program_key].write(value)
        else:
            Log.print(f"Unknown program key to write: '{program_key}' for Program '{Program.get_name(self)}'")

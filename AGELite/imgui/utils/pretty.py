from imgui_bundle import imgui
import glm

class UI_GLM_Pretty:
    """ static class (encapsulated methods set) for pretty printing of glm """

    @staticmethod
    def vec2f(v: 'glm.vec2', inline: bool = True):
        imgui.text("(")                                                         ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(1.0, 0.0, 0.0, 1.0), f"{v.x: 3.3f}")    ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(0.0, 1.0, 0.0, 1.0), f"{v.y: 3.3f}")    ; imgui.same_line(spacing=0)
        imgui.text(")")
        if inline: imgui.same_line()
    
    @staticmethod
    def vec2i(v: 'glm.vec2', inline: bool = True):
        imgui.text("(")                                                         ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(1.0, 0.0, 0.0, 1.0), f"{v.x: 6i}")      ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(0.0, 1.0, 0.0, 1.0), f"{v.y: 6i}")      ; imgui.same_line(spacing=0)
        imgui.text(")")
        if inline: imgui.same_line()

    @staticmethod
    def vec3f(v: 'glm.vec3', inline: bool = True):
        imgui.text("(")                                                         ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(1.0, 0.0, 0.0, 1.0), f"{v.x: 3.3f}")    ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(0.0, 1.0, 0.0, 1.0), f"{v.y: 3.3f}")    ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(0.0, 0.0, 1.0, 1.0), f"{v.z: 3.3f}")    ; imgui.same_line(spacing=0)
        imgui.text(")")
        if inline: imgui.same_line()
    
    @staticmethod
    def vec3i(v: 'glm.vec3', inline: bool = True):
        imgui.text("(")                                                         ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(1.0, 0.0, 0.0, 1.0), f"{v.x: 6i}")      ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(0.0, 1.0, 0.0, 1.0), f"{v.y: 6i}")      ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(0.0, 0.0, 1.0, 1.0), f"{v.z: 6i}")      ; imgui.same_line(spacing=0)
        imgui.text(")")
        if inline: imgui.same_line()
    
    @staticmethod
    def vec4f(v: 'glm.vec4', inline: bool = True):
        imgui.text("(")                                                         ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(1.0, 0.0, 0.0, 1.0), f"{v.x: 3.3f}")    ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(0.0, 1.0, 0.0, 1.0), f"{v.y: 3.3f}")    ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(0.0, 0.0, 1.0, 1.0), f"{v.z: 3.3f}")    ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(1.0, 0.0, 1.0, 1.0), f"{v.w: 3.3f}")    ; imgui.same_line(spacing=0)
        imgui.text(")")
        if inline: imgui.same_line()
    
    @staticmethod
    def vec4i(v: 'glm.vec4', inline: bool = True):
        imgui.text("(")                                                         ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(1.0, 0.0, 0.0, 1.0), f"{v.x: 6i}")      ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(0.0, 1.0, 0.0, 1.0), f"{v.y: 6i}")      ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(0.0, 0.0, 1.0, 1.0), f"{v.z: 6i}")      ; imgui.same_line(spacing=0)
        imgui.text(", ")                                                        ; imgui.same_line(spacing=0)
        imgui.text_colored(imgui.ImVec4(1.0, 0.0, 1.0, 1.0), f"{v.w: 6i}")      ; imgui.same_line(spacing=0)
        imgui.text(")")
        if inline: imgui.same_line()
    
    @staticmethod
    def mat2f(m: 'glm.mat2'):
        imgui.text("(")                                                          ; imgui.same_line(spacing=0)
        UI_GLM_Pretty.vec2f(m[0])                                                ; imgui.same_line(spacing=0)
        imgui.text(",")
        imgui.text(" ")                                                          ; imgui.same_line(spacing=0)
        UI_GLM_Pretty.vec2f(m[1])                                                ; imgui.same_line(spacing=0)
        imgui.text(")")
    
    @staticmethod
    def mat3f(m: 'glm.mat3'):
        imgui.text("(")                                                          ; imgui.same_line(spacing=0)
        UI_GLM_Pretty.vec3f(m[0])                                                ; imgui.same_line(spacing=0)
        imgui.text(",")
        imgui.text(" ")                                                          ; imgui.same_line(spacing=0)
        UI_GLM_Pretty.vec3f(m[1])                                                ; imgui.same_line(spacing=0)
        imgui.text(",")
        imgui.text(" ")                                                          ; imgui.same_line(spacing=0)
        UI_GLM_Pretty.vec3f(m[2])                                                ; imgui.same_line(spacing=0)
        imgui.text(")")
    
    @staticmethod
    def mat4f(m: 'glm.mat4'):
        imgui.text("(")                                                          ; imgui.same_line(spacing=0)
        UI_GLM_Pretty.vec4f(m[0])                                                ; imgui.same_line(spacing=0)
        imgui.text(",")
        imgui.text(" ")                                                          ; imgui.same_line(spacing=0)
        UI_GLM_Pretty.vec4f(m[1])                                                ; imgui.same_line(spacing=0)
        imgui.text(",")
        imgui.text(" ")                                                          ; imgui.same_line(spacing=0)
        UI_GLM_Pretty.vec4f(m[2])                                                ; imgui.same_line(spacing=0)
        imgui.text(",")
        imgui.text(" ")                                                          ; imgui.same_line(spacing=0)
        UI_GLM_Pretty.vec4f(m[3])                                                ; imgui.same_line(spacing=0)
        imgui.text(")")
    
class UI_Text_Pretty:
    """ imgui text utils """
    
    @staticmethod
    def centered(text: str, parent_width: int=-1):
        parent_width = parent_width if parent_width > 0 else imgui.get_window_width()
        text_width = imgui.calc_text_size(text).x
        imgui.set_cursor_pos_x((parent_width - text_width) * 0.5)
        imgui.text(text)

    @staticmethod
    def calc_width(labels: list[str], parent_width: int=-1) -> int:
        """ calculate the width of a set of elements in a row """
        parent_width = parent_width if parent_width > 0 else imgui.get_window_width()
        avaliable_width = parent_width - sum(len(label) for label in labels) - 2 # assuming spacing between labels and elements
        elem_width = avaliable_width // len(labels)
        return elem_width


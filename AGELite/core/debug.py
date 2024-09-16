import re

DEBUG = True

def fmt_program_exception_on_build(vertex_shader: str, fragment_shader: str, exc:Exception, range:int=4) -> str:
    """ Format mgl.program exception """
    if not DEBUG: 
        return exc

    for _type in re.findall(r"(.*)\n======*\n.*", str(exc)):
        s_error = ""
        
        if _type == "vertex_shader":
            lines = vertex_shader.splitlines()

        elif _type == "fragment_shader":
            lines = fragment_shader.splitlines()

        for line, error in re.findall(r"0\((\d*)\)\s:\s(.*)", str(exc)):
            line = int(line)-1 # error line marker starts at 1

            lines[line] = f"\033[91m{lines[line]}\033[0m" # colorize errored line
            scope = "\n".join(lines[ max(0,line-range) : min(len(lines),line+range) ]) # get lines before and after to a certain range and join them 
            s_error += f"{_type} @ {line+1}\n{scope}\n\n{error}\n==============\n" # format the error message

    return type(exc)(s_error)



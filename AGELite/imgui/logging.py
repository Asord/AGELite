from .objects import imgui, UI_Object

class UI_Logger(UI_Object):
    """ UI object to log messages to a console """
    def __init__(self):
        raise NotImplementedError("Cannot instantiate static class UI_Logger")

    buffer: dict[str, int] = {}
    buffer_idx: list[str] = []
    
    @staticmethod
    def print(message: str) -> int:
        """ print a message to the console and return the message index """

        if message in UI_Logger.buffer:
            if UI_Logger.buffer[message] < 99:
                UI_Logger.buffer[message] += 1
            return UI_Logger.buffer_idx.index(message)
        
        UI_Logger.buffer[message] = 1
        UI_Logger.buffer_idx.append(message)
        return len(UI_Logger.buffer_idx)-1

    @staticmethod
    def print_at(message: str, index: int=-1) -> int | None:
        """ print a message to the console and return the message index """
        if index == -1:
            return UI_Logger.print(message)
        else:
            if 0 <= index < len(UI_Logger.buffer_idx):
                UI_Logger.buffer[UI_Logger.buffer_idx[index]] = message
                UI_Logger.buffer[index] = message
                return index
            
        return None

    @staticmethod
    def ui():
        """ Show the log buffer """
        multiline = ""
        for message, count in UI_Logger.buffer.items():
            if count == 1:
                multiline += f"{message}\n"
            elif count < 99:
                multiline += f"{message} ({count})\n"
            else:
                multiline += f"{message} (99+)\n"

        imgui.input_text_multiline("##log", multiline, (-1, 300), imgui.InputTextFlags_.none)
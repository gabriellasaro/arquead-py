from platform import system

class TypeDir:

    def bar_type(self):
        if system() == "Linux" or system() == "Darwin":
            return "/"
        return "\\"
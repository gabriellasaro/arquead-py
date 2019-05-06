from platform import system

def bar_type():
    if system() == "Linux" or system() == "Darwin":
        return "/"
    return "\\"
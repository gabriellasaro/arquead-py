from platform import system

def bar_type():
    if system() == "Windows":
        return "\\"
    return "/"
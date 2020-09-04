class Error:

    def __init__(self, message = "Success", err = True):
        self.__message = message

        if message == "Success":
            self.__err = False
        else:
            self.__err = err
    
    def __str__(self):
        return self.__message
    
    def get_message(self):
        return self.__message
    
    def err(self):
        return self.__err
    
    def success(self):
        return not self.__err

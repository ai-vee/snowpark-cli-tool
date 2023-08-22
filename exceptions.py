class Exception_(Exception):
    CODE = -32 #? research standard error code
    MESSAGE = "Error"

    def data(self):
        return {
            "type": self.__class__.__name__,
            "message": str(self),
        }



class ValidationError(Exception_):
    CODE = 1
    HEADER = 'Validation Error'

class ContentError(Exception_):
    CODE = 2
    HEADER = 'Content Error'

class ParsingError(Exception_):
    CODE = 3
    HEADER = 'Parsing Error'
    
class RuntimeError(Exception_):
    CODE = 4
    HEADER = 'Runtime Error'
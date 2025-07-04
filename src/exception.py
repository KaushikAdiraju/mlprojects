import sys

def error_details(error,error_detail:sys):
    _,_,exc_inf = error_detail.exc_info()  # All the execution information will be here
    file_name = exc_inf.tb_frame.f_code.co_filename   #From that execution info retreive the file name
    error_message  = "Error ocured in python script [{0}] in line number [{1}] and the error is  [{2}]".format(file_name,exc_inf.tb_lineno,str(error))
    #tb_lineno tells us in which line is the error occuring.
    return error_message


class CustomException(Exception):    #Creating a class called custom exception and this can be used in all the scripts
    def __init__(self, error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_details(error_message,error_detail=error_detail)
    def __str__(self):
        return self.error_message
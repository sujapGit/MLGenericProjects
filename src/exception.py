##The sys module in Python provides access to variables and functions that interact strongly with the Python runtime environment.
## It allows developers to manipulate various aspects of program execution, such as handling command-line arguments, 
## managing input/output streams, and accessing interpreter-specific details. 
import sys 
from src.logger import logging

def error_message_details(error,error_detail:sys):
    ## first two return are not important but the thrid exc_tb has all info needed
    print('sfsdfsdf')
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
   
    error_message =("Error occured in python script name [{0}]"
        "line number [{1}] error message[{2}]").format(
        file_name,exc_tb.tb_lineno,str(error)
    )
    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):        
        super().__init__(error_message) 
        self.error_message=error_message_details(
            error_message,
            error_detail=error_detail)

    def __str__(self): 
        return self.error_message
    

if __name__=="__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("Divide by Zero")
        raise CustomException(e,sys)
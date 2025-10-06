import  logging
from logging import exception


class Invalidmarkserror(Exception):
    pass
def checkmarks(marks):
    if marks<0 or marks>100 :
        raise Invalidmarkserror("marks must be between 0 and 100")
try:
    checkmarks(123)
except Invalidmarkserror as e:
    logging.error(e)
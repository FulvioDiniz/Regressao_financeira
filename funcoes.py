
from msgTelegram import *

def taxa_acerto(y, y2,tendencia):
    if tendencia == 1:
        if y2 < y:
            return True
        else:
            return False
    else:
        if y2 > y:
            return True
        else:
            return False

    
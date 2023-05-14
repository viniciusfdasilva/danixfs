import os

def is_root():
    return True if os.geteuid() == 0 else False
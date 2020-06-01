import os
import argparse
from pathlib import Path


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-dns', action="store", dest="dns")

def file_doesnt_exist(file_name):
    file_exists = os.path.exists(file_name)
    if file_exists == False :
        return True
    else :
        return False

if __name__ == '__main__':
    home_dir = str(Path.home())
    file_doesnt_exist("{}/{}".format(home_dir,"fault_test"))
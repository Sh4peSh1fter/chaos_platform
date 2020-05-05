import argparse
from pathlib import Path
from datetime import datetime


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-dns', action="store", dest="dns")

def create_file(file_name):
    try :
        with open(file_name,'w+') as file :
            now = datetime.now()
            file.write("this file was created at {}".format(now))
            return True
    except :
        return False


if __name__ == '__main__':
    home_dir = str(Path.home())
    result = create_file("{}/{}".format(home_dir,"fault_test"))
    print(result)
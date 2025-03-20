

from guacenc.guacenc_parse import GuacamoleParser
from guacenc_instruction import *
from guacenc_types import *

max_read_size = 1024*8
    
def parse_file(file_path):
    display = Display(GUACENC_DEFAULT_WIDTH, GUACENC_DEFAULT_HEIGHT)
    with open(file_path, "r") as fd:
        parser = GuacamoleParser()
        read_all = False
        while True:
            read = ""
            if not read_all:
                read = fd.read(max_read_size)
                if not read or len(read) < max_read_size:
                    read_all = True
            for item in parser.parse(read):
                inst = Instruction(item[0], *item[1:])
                guacenc_handle_instruction(display, inst)
            if read_all and parser.buffer == "":
                print("End of parse file")
                break



if __name__ == "__main__":
    import sys, os
    if len(sys.argv) < 2:
        print('Usage: python guacamole_parse.py <file_path>')
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print('File not found')
        sys.exit(1)
    parse_file(file_path)

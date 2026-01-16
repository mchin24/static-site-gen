from textnode import TextNode, TextType
from utils import copy_static_files, generate_page
import os
import sys

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'

    src_directory = os.path.abspath('./static')
    dest_directory = os.path.abspath('./docs')
    
    copy_static_files(src_directory, dest_directory)
    print(f"Static files copied from {src_directory} to {dest_directory}")

    generate_page('./content', './template.html', './docs', basepath)

if __name__ == "__main__":
    main()
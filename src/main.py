from textnode import TextNode, TextType
from utils import copy_static_files
import os

def main():
    src_directory = os.path.abspath('./static')
    dest_directory = os.path.abspath('./public')
    
    copy_static_files(src_directory, dest_directory)
    print(f"Static files copied from {src_directory} to {dest_directory}")

if __name__ == "__main__":
    main()
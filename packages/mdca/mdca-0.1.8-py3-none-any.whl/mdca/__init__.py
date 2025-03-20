import os.path
import sys

cur_file_path = os.path.abspath(__file__)
cur_dir_path = os.path.dirname(cur_file_path)

sys.path.append(cur_dir_path)
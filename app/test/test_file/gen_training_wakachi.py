import sys
sys.path.append("../../")

from spec2test.wakachi import Wakachi

PATH_FILE = "./txt/"
PATH_RESOURSE = "./wakachi/"


wakachi = Wakachi(input_path=PATH_FILE, output_path=PATH_RESOURSE)

wakachi.generate(is_force=False)

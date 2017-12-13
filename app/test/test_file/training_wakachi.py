import sys
sys.path.append("../../")

from spec2test.wakachi import Wakachi

PATH_FILE = "./"
PATH_RESOURSE = "./"


wakachi = Wakachi(input_path=PATH_FILE, output_path=PATH_RESOURSE)

wakachi.generate_all(is_force=False)

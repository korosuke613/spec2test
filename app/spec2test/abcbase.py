from abc import ABC
from .directory import Directory


class AbcBase(ABC):
    def __init__(self,
                 input_dir_path_,
                 output_dir_path_,
                 input_extension_,
                 output_extension_):
        self.input = Directory(input_dir_path_, input_extension_)
        self.output = Directory(output_dir_path_, output_extension_)
        self.import_io_files()

    def import_io_files(self):
        self.input.import_files()
        self.output.import_files()

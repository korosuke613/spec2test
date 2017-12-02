import os
from .file import File


class Directory:
    def __init__(self,
                 path_,
                 default_extension_=None):
        self.path = path_
        self.default_extension = default_extension_
        self.file_dict = {}

    def append_file(self,
                    file_name,
                    extension=None):
        if extension is None:
            extension = self.default_extension
        if not File.is_same_extension(file_name, extension):
            return
        file = File(file_name, extension)
        self.file_dict[file_name] = file

    def import_files(self, extension=None):
        for file in os.listdir(self.path):
            self.append_file(file, extension)

    def get_file_path(self, file_name):
        return self.file_dict[file_name].full_name


if __name__ == '__main__':
    directory = Directory("./", ".py")
    directory.import_files(".py")

class File:
    def __init__(self,
                 file_name_,
                 extension_):
        self.name = file_name_[:len(extension_)]
        self.extension = extension_
        self.full_name = file_name_

    @staticmethod
    def is_same_extension(file_name, extension):
        return file_name[-len(extension):] == extension

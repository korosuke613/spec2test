from directory import Directory
from iomanager import IOManagerDirectory


class Evaluation(IOManagerDirectory):
    def __init__(self,
                 input_dir_: Directory,
                 output_dir_: Directory):
        super().__init__(input_dir_, output_dir_)

    def generate(self):
        raise NotImplementedError


def main():
    input_dir = Directory("./", ".txt")
    output_dir = Directory("./", ".txt")
    evaluation = Evaluation(input_dir, output_dir)
    print(evaluation)


if __name__ == '__main__':
    main()

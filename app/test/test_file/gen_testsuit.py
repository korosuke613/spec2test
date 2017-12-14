import os
import shutil
import pytest
from spec2test import WakachiMeishi, Imporwords, Tfidf, Model, TestSuite


def main():
    testsuite = TestSuite(input_path="./",
                          output_path="./",
                          units_=10,
                          learn_result_="./model_iter_72306")

    for _ in range(10):
        testsuite.generate("パソコン")


if __name__ == '__main__':
    main()

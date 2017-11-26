# content of conftest.py
import pytest
import os


def pytest_addoption(parser):
    parser.addoption("--Work", action="store", default=".",
        help="Change current working dir before running the collected tests.")


def pytest_sessionstart(session):
    os.chdir(session.config.getoption('--Work'))
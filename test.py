import pytest
from my_parser import check_file


def test_ok():
    assert check_file('tests/test1.txt')


def test_no_dot():
    assert not check_file('tests/test2.txt')


def test_no_dot_2():
    assert not check_file('tests/test3.txt')


def test_no_head():
    assert not check_file('tests/test4.txt')


def test_no_body():
    assert not check_file('tests/test5.txt')


def test_not_enough_args():
    assert not check_file('tests/test6.txt')


def test_empty_file():
    assert check_file('tests/test7.txt')


def test_no_balance():
    assert not check_file('tests/test8.txt')


def test_unknown_symbol():
    assert not check_file('tests/test9.txt')


def test_long_names():
    assert check_file('tests/test10.txt')


def test_wrong_file():
    assert not check_file('tests/wrong_file.txt')
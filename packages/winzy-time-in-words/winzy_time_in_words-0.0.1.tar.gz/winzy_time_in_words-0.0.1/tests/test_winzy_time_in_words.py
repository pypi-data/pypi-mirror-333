import pytest
import winzy_time_in_words as w
from winzy_time_in_words.time_in_words import time_in_words, mainrun

from argparse import Namespace, ArgumentParser

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

@pytest.mark.parametrize("hour, minute, expected", [
    # o'clock test
    (1, 0, "one o'clock"),
    (12, 0, "twelve o'clock"),
    
    # past the hour tests (minutes < 30)
    (3, 1, "One minute past three"),
    (5, 10, "ten minutes past five"),
    (8, 15, "Quarter past eight"),
    (7, 29, "twenty nine minutes past seven"),
    
    # exact half past test
    (9, 30, "Half past nine"),
    
    # to the hour tests (minutes > 30)
    (10, 45, "Quarter to eleven"),
    (4, 40, "twenty minutes to five"),
    (11, 59, "One minute to twelve"),
])
def test_time_in_words(hour, minute, expected):
    # Adjust hour to 12-hour format as required by function
    formatted = time_in_words(hour % 12, minute)
    # The function for minute == 1 uses "One minute..." with One capitalized, so match that.
    assert formatted == expected

def test_edge_cases():
    # Test midnight (0:00) should be "twelve o'clock" because 0 % 12 == 0 -> num_to_words[0] is "twelve".
    assert time_in_words(0, 0) == "twelve o'clock"
    
    # Test one minute past midnight
    assert time_in_words(0, 1) == "One minute past twelve"
    
    # Test one minute to one (12:59)
    assert time_in_words(12 % 12, 59) == "One minute to one"
    
    # Test for quarter to hour with wrapping hour (23:45 should be "Quarter to twelve")
    # Compute hour modulo manually for consistency with our function usage.
    hour = 23 % 12  # 11 in 12-hour format
    assert time_in_words(hour, 45) == "Quarter to twelve"

def test_mainrun(capsys):
    mainrun()
    captured = capsys.readouterr().out
    assert "The time is" in captured

def test_plugin(capsys):
    w.time_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import regex_matching as rm


def test_examples():
    assert rm.is_match('aa', 'a') is False
    assert rm.is_match('aa', 'a*') is True
    assert rm.is_match('ab', '.*') is True
    assert rm.is_match('aab', 'c*a*b') is True
    assert rm.is_match('mississippi', 'mis*is*p*.') is False

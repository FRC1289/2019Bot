import pytest
from pytest import approx

from VisionUtils import getDistance, getMidPoint

def test_getSomeDistance():
    assert getDistance(2, 3, 10, 9) == 10

def test_getAnotherDistance():
    assert getDistance(4, 6, -3, 5) == approx(7.071, abs=1e-3)

def test_getSomeMidPoint():
    assert getMidPoint(2, 3, 10, 9) == (6, 6)

def test_getAnotherMidPoint():
    assert getMidPoint(6, 12, 2, -4) == (4, 4)

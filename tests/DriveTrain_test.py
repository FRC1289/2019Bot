import pytest
from pytest import approx

@pytest.fixture
def DriveTrainFixture():
    from wpilib.command.subsystem import Subsystem
    from subsystems.DriveTrain import DriveTrain
    return DriveTrain(0)


def test_deadband(DriveTrainFixture):
    assert DriveTrainFixture.deadBand(0.05) == 0.0

def test_positiveInput(DriveTrainFixture):
    assert DriveTrainFixture.deadBand(0.9) == approx(0.3206, abs=1e-3)

def test_negativeInput(DriveTrainFixture):
    assert DriveTrainFixture.deadBand(-0.7) == approx(-0.0490, abs=1e-3)

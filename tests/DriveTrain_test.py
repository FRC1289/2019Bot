import pytest
from pytest import approx

@pytest.fixture
def DriveTrainFixture():
    from wpilib.command.subsystem import Subsystem
    from subsystems.DriveTrain import DriveTrain
    from subsystems.ParameterManager import ParameterManager
    pm = ParameterManager(0)
    return DriveTrain(0,pm)


def test_deadband(DriveTrainFixture):
    assert DriveTrainFixture.deadBand(0.05) == 0.0

def test_positiveInput(DriveTrainFixture):
    assert DriveTrainFixture.deadBand(0.9) == approx(0.6141, abs=1e-3)

def test_negativeInput(DriveTrainFixture):
    assert DriveTrainFixture.deadBand(-0.7) == approx(-0.2746, abs=1e-3)

import pytest
from DataReader import DataReader
from HRM_Processor import HRM_Processor


@pytest.fixture
def dr():
    """Create a basic DataReader object using test_file.csv
     """
    dr = DataReader("test_file.csv")
    return dr


@pytest.fixture
def hrm(dr):
    """Create a basic HRM_Processor from the dr object"""

    hrm = HRM_Processor(dr)
    return hrm
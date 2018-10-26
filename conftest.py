import pytest
from DataReader import DataReader
from HRM_Processor import HRM_Processor
from DataWriter import DataWriter

"""This file containing fixtures creating variables that are used throughout
the testing functions for the DataReader, HRM_Processor, and DataWriter.
"""


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


@pytest.fixture
def dw():
    """Create a basic DataWriter object"""
    dr_for_DW = DataReader('test_data1.csv')
    hrm_for_DW = HRM_Processor(dr_for_DW)
    dw = DataWriter(hrm_for_DW)
    return dw

from DataReader import DataReader
import pytest


def test_data_reader_default_duration():
    """Tests that data reader assigns a default value to the duration parameter
     if one is not assigned during
    construction.

    Returns
    -------

    """
    DR = DataReader("test_file.csv")
    assert DR.duration == (0, 10)


def test_data_reader_assigned_duration():
    """Tests the DataReader overrides the default value if a duration is
     assigned during construction

    Returns
    -------

    """
    DR = DataReader("test_file.csv", (10, 20))
    assert DR.duration == (10, 20)

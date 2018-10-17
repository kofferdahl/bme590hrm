from DataReader import DataReader
import pytest
import numpy as np


def test_data_reader_default_duration():
    """Tests that data reader assigns a default value to the duration parameter
     if one is not assigned during construction.

    Returns
    -------
    None
    """
    dr = DataReader("test_file.csv")
    assert dr.duration == (0, 10)


def test_data_reader_assigned_duration():
    """Tests the DataReader overrides the default value if a duration is
     assigned during construction

    Returns
    -------
    None
    """
    dr = DataReader("test_file.csv", (10, 20))
    assert dr.duration == (10, 20)


def test_read_csv_time():
    """Tests the read_csv function of the data reader for reading in the
    time numpy array from the csv file.

    Returns
    -------
    None
    """
    dr = DataReader("test_file.csv")
    expected_time = np.array([0, 1, 2])
    assert np.array_equal(dr.output_dict["time"], expected_time)


def test_read_csv_voltage():
    """Tests the read_csv function of the data reader for reading in the
    voltage numpy array from the csv file.

    Returns
    -------
    None
    """
    dr = DataReader("test_file.csv")
    expected_voltage = np.array([10, 15, 20])
    assert np.array_equal(dr.output_dict["voltage"], expected_voltage)


def test_validate_csv_file_bad_file_name():
    """Tests the validate_csv_file for raising an exception when a
    file that
    does not exist is inputted for the csv_file_name argument in DataReader.

    Returns
    -------
    None
    """
    with pytest.raises(FileNotFoundError):
        dr = DataReader("random_file_name.csv")
        dr.validate_csv_file("random_file_name.csv")


def test_validate_csv_file_bad_file_extension():
    """Tests the validate_csv_file function for raising a ValueError when
    there is a bad file extension (i.e. one that is not .csv)

    Returns
    -------
    None
    """
    with pytest.raises(ValueError):
        dr = DataReader("BadExtensionTest.txt")
        dr.validate_csv_file("BadExtensionTest.txt")

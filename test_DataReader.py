from DataReader import DataReader
import pytest
import numpy as np


def test_data_reader_default_duration():
    """Tests that data reader assigns a default value to the duration parameter
     if one is not assigned during construction. Default value should be min
     max values from the time array.

    Returns
    -------
    None
    """
    dr = DataReader("test_file.csv")
    assert dr.duration == (0, 2)


def test_data_reader_assigned_duration():
    """Tests the DataReader overrides the default value if a duration is
     assigned during construction

    Returns
    -------
    None
    """
    dr = DataReader("test_file.csv", (0, 2))
    assert dr.duration == (0, 2)


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


@pytest.mark.parametrize("duration_tuple", [
    (0, 3),  # min duration too short
    (2, 5),  # max duration too long
    (0, 5),  # both min and max exceed range of time_array
])
def test_validate_duration(duration_tuple):
    """Tests the validate_duration function, which ensures that a user
    specified duration in the construction of the data reader object is
    within the range of time values read in from the CSV file.

    Returns
    -------
    None
    """
    dr = DataReader("test_file.csv")
    time_array = np.array([1, 2, 3, 4])

    with pytest.raises(ValueError):
        dr.validate_duration(time_array, duration_tuple)

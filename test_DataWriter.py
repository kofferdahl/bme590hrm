import json
import numpy as np
import os
from DataReader import DataReader
from HRM_Processor import HRM_Processor
from DataWriter import DataWriter
import pytest


def test_DataWriter_init_valid_case():
    """Tests the initialization of the DataWriter object, and that it
    successfully gets the output_dict from the input_dict and stores it as
    metrics.

    Returns
    -------
    None

    """

    dr = DataReader("test_data1.csv")
    hrm = HRM_Processor(dr)
    dw = DataWriter(hrm)
    assert dw.metrics == hrm.output_dict


def test_DataWriter_init_invalid_case(hrm):
    """Tests the initialization of the DataWriter object for a case where
    the data from the HRM_Processor object is not valid.

    Parameters
    ----------
    hrm:    HRM_Processor
            Generic HRM_Processor made from a DataReader with test_file.csv
    capsys: Pytest fixture
            A decorator for getting outputs printed to the console
    Returns
    -------
    None

    """
    hrm.isValid = False  # Force invalidity for testing case
    with pytest.raises(ValueError):
        dw = DataWriter(hrm)


def test_DataWriter_init_write_to_dict():
    """Tests that the construction of a DataWriter object creates a .json
    file with the base file name that is the same as the file name of the
    .csv file passed into the original DataReader.

    Returns
    -------
    None
    """
    dr = DataReader("test_data1.csv")
    hrm = HRM_Processor(dr)
    dw = DataWriter(hrm)

    assert os.path.isfile("test_data1.json")
    os.remove("test_data1.json")


def test_write_to_json():
    """Tests the write_to_json function of the DataWriter, which should be
    able to take in an dictionary and output file path, and write that
    dictionary to the specified output file.

    Returns
    -------
    None
    """
    dr = DataReader("test_data1.csv")
    hrm = HRM_Processor(dr)
    dw = DataWriter(hrm)

    metrics = {"test": 5,
               "another word": 18.5}
    output_file = "test.json"
    dw.write_to_json(metrics, output_file)

    with open(output_file) as infile:
        written_data = json.load(infile)

    assert written_data == metrics


def test_convert_np_arrays(dw):
    """Tests that the convert_np_arrays function finds the beats entry in
    teh dictionary and converts it from a numpy array to a python list.

    Parameters
    ----------
    dw:     DataWriter
            A generic DataWriter object made from an original DataReader /
            HRM_Processor with the file test_data1.csv.

    Returns
    -------
    None
    """
    metrics_dict = {}
    metrics_dict["beats"] = np.array([1, 2, 3, 4])
    serializable_dict = dw.convert_np_arrays(metrics_dict)

    assert isinstance(serializable_dict["beats"], list)

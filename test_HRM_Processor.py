import pytest
from DataReader import DataReader
from HRM_Processor import HRM_Processor
import numpy as np


def test_HRM_Processor_init(dr):
    """

    Parameters
    ----------
    dr:     DataReader
            A basic data reader object created from the file test_file.csv
            with a default BPM duration.

    Returns
    -------

    """
    hrm_proc = HRM_Processor(dr)
    assert dr.output_dict == hrm_proc.input_data


def test_voltage_extremes(hrm):

    voltage = np.array([-1.502, -7.9, 3.5, 2.1, 8.7, 4.0])

    voltage_extremes = hrm.determine_voltage_extremes(voltage)

    assert voltage_extremes == (-7.9, 8.7)


def test_write_outputs_to_dict_voltage_extremes(hrm):

    assert hrm.output_dict["voltage_extremes"] == (10.0, 20.0)

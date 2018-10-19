import pytest
from DataReader import DataReader
from HRM_Processor import HRM_Processor


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

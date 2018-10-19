import pytest
from DataReader import DataReader
from HRM_Processor import HRM_Processor


def test_HRM_Processor_init():
    dr = DataReader("test_file.csv")

    hrm_proc = HRM_Processor(dr)

    assert dr.output_dict == hrm_proc.input_data

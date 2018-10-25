from DataWriter import DataWriter
import json


def test_DataWriter_init(hrm):
    """Tests the initialization of the DataWriter object, and that it
    successfully gets the output_dict from the input_dict and stores it as
    metrics.

    Parameters
    ----------
    hrm:    HRM_Processor
            Generic HRM_Procesor made from test_file.csv

    Returns
    -------
    None

    """
    dw = DataWriter(hrm)
    assert dw.metrics == hrm.output_dict


def test_write_to_json(hrm):
    """Tests the write_to_json function of the DataWriter, which should be
    able to take in an dictionary and output file path, and write that
    dictionary to the specified output file.

    Parameters
    ----------
    hrm:    HRM_Processor
            A generic HRM_Processor made from test_file.csv

    Returns
    -------
    None
    """

    dw = DataWriter(hrm)
    metrics = {"test": 5,
               "another word": 18.5}
    output_file = "test.json"
    dw.write_to_json(metrics, output_file)

    with open(output_file) as infile:
        written_data = json.load(infile)

    assert written_data == metrics

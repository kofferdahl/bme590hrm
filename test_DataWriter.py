from DataWriter import DataWriter


def test_DataWriter_init(hrm):
    dw = DataWriter(hrm)
    assert dw.metrics == hrm.output_dict

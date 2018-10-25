import pytest
from DataReader import DataReader
from HRM_Processor import HRM_Processor
import numpy as np


def test_HRM_Processor_init(dr):
    """Tests the initialization of the HRM_Processor

    Upon initialization, the HRM_Processor should read in the output_dict
    from the DataReader, and store it as a input_data property.

    Parameters
    ----------
    dr:     DataReader
            A basic HRM_Processor created from the file test_file.csv
            with a default BPM duration.

    Returns
    -------
    None
    """
    hrm_proc = HRM_Processor(dr)
    assert dr.output_dict == hrm_proc.input_data


def test_voltage_extremes(hrm):
    """Tests the determine_voltage_extremes function to ensure that it
    returns the max and minimum of a voltage numpy array as a tuple in the
    form (max, min).

    Parameters
    ----------
    hrm:    HRM_Processor
            A basic HRM_Processor made from a DataReader with test_file.csv

    Returns
    -------
    None
    """

    voltage = np.array([-1.502, -7.9, 3.5, 2.1, 8.7, 4.0])

    voltage_extremes = hrm.determine_voltage_extremes(voltage)

    assert voltage_extremes == (-7.9, 8.7)


def test_write_outputs_to_dict_voltage_extremes(hrm):
    """Tests that the voltage extremes was written to the output_dict of the
    HRM_Processor object from the voltage data. The comparision is to the
    'voltage' extremes of test_file.csv

    Parameters
    ----------
    hrm:    HRM_Processor
            A basic HRM_Processor made from a DataReader with test_file.csv

    Returns
    -------
    None
    """

    assert hrm.output_dict["voltage_extremes"] == (10.0, 20.0)


def test_determine_ecg_strip_duration(hrm):
    """Checks that the determine_ecg_strip duration function the max value
    of the time numpy array that it is given.

    Parameters
    ----------
    hrm: HRM_Processor
         Basic HRM_Processor object made from a DataReader with test_file.csv

    Returns
    -------
    None
    """
    time = np.array([0, 2.2, 5, 7.5])

    strip_duration = hrm.determine_ecg_strip_duration(time)

    assert strip_duration == 7.5


def test_write_strip_duration(hrm):
    """Tests that the max value of the time numpy array was written to the
    "duration" entry of the output_dict upon construction of hrm. The max
    time value in test_file.csv is 2.

    Parameters
    ----------
    hrm:    HRM_Processor
            Basic HRM_Processor made from a DataReader with test_file.csv

    Returns
    -------
    None
    """

    assert hrm.output_dict["duration"] == 2


def test_determine_threshold(hrm):
    """Checks that the determine_threshold function returns 90% of the
    highest value in a numpy array

    Parameters
    ----------
    hrm:    HRM_Processor
            Basic HRM_Processor object made from a DataReader with
            test_file.csv
    Returns
    -------
    None
    """

    voltage = np.array([1, 2, 4, 10, 5])
    threshold = hrm.determine_threshold(voltage)
    assert threshold == 7.5


def test_find_indices_above_threshold(hrm):
    """Tests that the find_indices_above_threshold function finds the
    indices where the voltage numpy array are above a specified threshold.

    Parameters
    ----------
    hrm:    HRM_Processor
            Basic HRM_Processor made from a DataReader with test_file.csv

    Returns
    -------
    None
    """

    threshold = 5
    voltage = np.array([1, 6, 4, 5, 2, 9.7])

    expected_indices = np.array([1, 5])
    calculated_indices = hrm.find_indices_above_threshold(voltage, threshold)

    assert np.array_equal(calculated_indices, expected_indices)


def test_find_beat_separation_points(hrm):
    """Tests the find_beat_separation_points function, which finds indices
    in an array of indices where there is a separation between consecutive
    indices greater than 2 (indicating the likely start of a new beat/QRS
    complex).

    Parameters
    ----------
    hrm:        HRM_Processor
                A basic HRM_Processor made from a DataReader with test_file.csv

    Returns
    -------
    None
    """
    indices = np.array([1, 2, 3, 4, 5, 10, 11, 12, 14, 30, 31, 32, 40, 41])
    expected_sep_inx = np.array([5, 14, 32])
    measured_sep_inx = hrm.find_beat_separation_points(indices)

    assert np.array_equal(measured_sep_inx, expected_sep_inx)


def test_find_qrs_peak_indices(hrm):
    """Tests the find_qrs_peak_indices function, which should be able to
    find the maximum value in a voltage array within a range specified by
    the beat_sep_inx array.

    Parameters
    ----------
    hrm:        HRM_Processor
                A basic HRM_Processor object made from input_file.csv

    Returns
    -------
    None
    """
    beat_sep_inx = np.array([3, 5, 10])
    voltage = np.array([0, 1, 6, 8, 12, 10, 18, 4, 29, 1, 8, 3, 5, 6])
    expected_beat_max = np.array([3, 4, 8, 12])
    measured_beat_max = hrm.find_qrs_peak_indices(voltage, beat_sep_inx)

    assert np.array_equal(expected_beat_max, measured_beat_max)


def test_index_beat_start_times(hrm):
    """Tests index_beat_start_times, which finds the start times of a beat
    in a numpy array based on indices specified by the qrs_peak_locations
    array.

    Parameters
    ----------
    hrm:    HRM_Processor
            A basic HRM_Processor made from a DataReader with test_file.csv

    Returns
    -------
    None
    """
    qrs_peak_locations = np.array([0, 3, 6, 8])
    time = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    expected_start_times = np.array([1, 4, 7, 9])
    measured_start_times = hrm.index_beat_start_times(time, qrs_peak_locations)

    assert np.array_equal(expected_start_times, measured_start_times)


def test_determine_num_beats(hrm):
    """Tests the most basic functionality of the determine_num_beats
    function, which simply returns the length of the start_times array that
    has been passed into it.

    Parameters
    ----------
    hrm:    HRM_Processor
            A basic HRM_Processor made from a DataReader with test_file.csv

    Returns
    -------
    None
    """

    start_times = np.array([1, 2, 3, 4])
    expected_num_beats = 4
    measured_num_beats = hrm.determine_num_beats(start_times)

    assert expected_num_beats == measured_num_beats


def test_determine_bpm(hrm):
    """

    Parameters
    ----------
    hrm:    HRM_Processor
            A basic HRM_Processor made from a DataReader with test_file.csv

    Returns
    -------
    None
    """

    start_times = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    duration = (3, 7)

    expected_bpm = 60
    calculated_bpm = hrm.determine_bpm(start_times, duration)

    assert expected_bpm == calculated_bpm


def test_determine_bpm2(hrm):
    """Tests the case where the end of the duration in the bpm of interest
    exceeds the beat start time.

    Parameters
    ----------
    hrm:    HRM_Processor
            A basic HRM_Processor made from a DataReader with test_file.csv

    Returns
    -------
    None
    """

    start_times = np.array([1, 2, 3, 4, 5, 6])
    duration = (5, 6)

    expected_bpm = 60
    calculated_bpm = hrm.determine_bpm(start_times, duration)

    assert expected_bpm == calculated_bpm

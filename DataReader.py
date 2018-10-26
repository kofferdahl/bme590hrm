import numpy as np
import os.path
from scipy import interpolate
import logging


class DataReader:
    """DataReader handles and formats the CSV file and duration inputs.

    This object validates the user inputs (file name and optional duration
    for BPM calculation), and creates a public dictionary, output_dict,
    containing the user specified duration or a default duration, and numpy
    arrays with the time and voltage data from the CSV file. The output_dict
    will be accessed by the HRM_Processor object for processing the ECG signal.

    Attributes
    ----------
    csv_file_path:  str
                    Path indicating the location of the CSV file with ECG data
    duration:       tuple (float, float)
                    A tuple containing the start and end times (in seconds) for
                    range over which the ECG data will be calculated
    output_dict:    dict
                    A dictionary containing the relevant output data for the
                    HRM_Processor - i.e. time and voltage numpy arrays,
                    and the user specified duration (or a default duration)
                    for BPM calculation.
    """
    def __init__(self, csv_file_path, duration=None):

        logging.basicConfig(filename="HRM_logs.txt",
                            format='%(asctime)s %(levelname)s:%(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        self.output_dict = {}
        try:
            self.validate_csv_file(csv_file_path)
            self.csv_file_path = csv_file_path

            try:
                self.read_csv_file()

                if duration is None:
                    self.duration = (
                        np.amin(self.output_dict["time"]),
                        np.amax(self.output_dict["time"]))
                    self.output_dict["duration"] = self.duration
                else:
                    try:
                        self.validate_duration(self.output_dict["time"],
                                               duration)
                        self.duration = duration
                        self.output_dict["duration"] = self.duration
                    except ValueError:
                        print(
                            "The duration specified is not valid. Using full"
                            "duration of ECG strip instead")

                        logging.error("The duration specified is not valid. "
                                      "Using full duration of ECG strip "
                                      "instead.")
                        self.duration = (
                            np.amin(self.output_dict["time"]),
                            np.amax(self.output_dict["time"]))
                        self.output_dict["duration"] = self.duration

            except TypeError:
                print("The csv file has blank or non-numerical values. "
                      "Please remove these and try again.")
                logging.error("The csv file has blank or non-numerical "
                              "values. Please remove these and try again.")
                raise TypeError

            except ValueError:
                print("the length of the time vector is not equal to the "
                      "length of the voltage vector. Please fix this problem"
                      "in the CSV file and try again.")
                logging.error("the length of the time vector is not equal to "
                              "the length of the voltage vector. Please fix "
                              "this problem in the CSV file and try again.")
                raise ValueError

        except FileNotFoundError:
            print("The input file cannot be found. Please try again.")
            logging.error("The input file cannot be found. Please try again")
            raise FileNotFoundError

        except ValueError:
            print("The input file does not have a .csv file extension. "
                  "Please try again with a CSV file.")
            logging.error("the input file does not have a .csv file "
                          "extension. Please try again with a CSV file.")
            raise ValueError

    def read_csv_file(self):
        """read_csv_file reads in the CSV file from the csv_file_path
        property, and writes numpy arrays for time and voltage to the output
        dictionary of the DataReader object.

        Returns
        -------
        None
        """

        time = np.genfromtxt(self.csv_file_path, delimiter=',', usecols=(0))

        voltage = np.genfromtxt(self.csv_file_path, delimiter=',', usecols=(1))

        if np.isnan(time).any():
            can_interp = self.can_interp(time)
            if can_interp:
                print("warning: interpolating missing time values.")
                logging.warning("Interpolating missing time values.")
                time = self.interp_time(time)

        self.validate_csv_data(time, voltage)

        self.output_dict["time"] = time
        self.output_dict["voltage"] = voltage

    def validate_csv_file(self, csv_file_path):
        """Checks to make sure that the csv file exists and has a csv file
        extension. Called by read_csv_file function.

        Parameters
        ----------
        csv_file_path:  str
                        Path of the csv file

        Returns
        -------
        None
        """
        if not os.path.isfile(csv_file_path):
            raise FileNotFoundError

        if not csv_file_path.lower().endswith(".csv"):
            raise ValueError

    def validate_csv_data(self, time_array, voltage_array):
        """Checks that the CSV data that has been read in does not have any
        NaNs and that the time_array and voltage_array are the same length.

        NaNs imply that there were strings or missing values in the original
        CSV file, and these values were not able to be interpolated. This
        function raises a TypeError or ValueError if the data is not valid.

        Parameters
        ----------
        time_array:     Numpy array
                        Time values read in from CSV file

        voltage_array:  Numpy array
                        Voltage values read in from CSV file

        Returns
        -------
        None
        """

        if np.isnan(time_array).any() or np.isnan(voltage_array).any():
            raise TypeError

        if time_array.size != voltage_array.size:
            raise ValueError

    def can_interp(self, time_array):
        """Checks to see if a time_array can be interpolated, which would
        mean that it has less than 10% missing values.

        Parameters
        ----------
        time_array: numpy array
                    Time values read in from CSV file
        Returns
        -------
        can_interp: boolean
                    Specifies if this array can be interpolated
        """

        is_finite = np.isfinite(time_array)
        num_defined_vals = sum(is_finite)

        frac_def_vals = num_defined_vals / time_array.size

        if frac_def_vals >= 0.9:
            can_interp = True
        else:
            can_interp = False

        return can_interp

    def interp_time(self, time_array):
        """Linearly interpolates missing time values in the time_array

        Parameters
        ----------
        time_array: numpy array
                    Numpy array containing time values from csv file,
                    with some missing values.

        Returns
        -------
        interp_time:    numpy array
                        A numpy array with the NaNs linearly interpolated.
        """
        defined_indicies = np.isfinite(time_array)
        indices = np.arange(0, time_array.size)
        interp_funct = interpolate.interp1d(indices[defined_indicies],
                                            time_array[defined_indicies])

        interp_time = interp_funct(indices)

        return interp_time

    def validate_duration(self, time_array, duration):
        """Checks that a user-specified duration for BPM calculation is valid.

        A valid duration is one that is within the range of possible time
        values from the time_array. This function raises a ValueError
        exception if the duration is not valid.

        Parameters
        ----------
        time_array: numpy array
                    Time values read in from the CSV file
        duration:   tuple(float, float)
                    Specifies the min and max times of the duration of interest
                    for BPM calculation in the format (min, max)

        Returns
        -------
        None
        """
        min_time = np.amin(time_array)
        max_time = np.amax(time_array)

        if duration[0] < min_time or duration[1] > max_time:
            raise ValueError

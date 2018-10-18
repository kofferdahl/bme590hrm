import numpy as np
import os.path


class DataReader:
    def __init__(self, csv_file_path, duration=None):
        """Constructor for DataReader object, which reads in and formats CSV data.

        Parameters
        ----------
        csv_file_path: str
            Path indicating the location of the CSV file with ECG data
        duration: tuple (float, float)
            A tuple containing the start and end times (in seconds) for range
            over which the ECG data will be calculated
        """
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
                else:
                    try:
                        self.validate_duration(self.output_dict["time"],
                                               duration)
                        self.duration = duration
                    except ValueError:
                        print(
                            "The duration specified is not valid. Please try "
                            "again.")
            except TypeError:
                print("The csv file has blank or non-numerical values. "
                      "Please remove these and try again.")
            except ValueError:
                print("the length of the time vector is not equal to the "
                      "length of the voltage vector. Please fix this problem"
                      "in the CSV file and try again.")

        except FileNotFoundError:
            print("The input file cannot be found. Please try again.")

        except ValueError:
            print("The input file does not have a .csv file extension. "
                  "Please try again with a CSV file.")

    def read_csv_file(self):
        """read_csv_file reads in the CSV file from the csv_file_path
        property, and outputs a numpy array with the contents of the csv file.

        Returns
        -------
        Nothing directly, but writes the time and voltage numpy arrays into
        the output_dict dictionary property of the DataReader.
        """

        time = np.genfromtxt(self.csv_file_path, delimiter=',', usecols=(0))

        voltage = np.genfromtxt(self.csv_file_path, delimiter=',', usecols=(1))

        self.validate_csv_data(time, voltage)

        self.output_dict["time"] = time
        self.output_dict["voltage"] = voltage

    def validate_csv_file(self, csv_file_path):
        """Checks to make sure that the csv file exists and has a CSV file
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
        """Checks that the csv data that has been read in does not have any
        nans (which implies missing or non-numerical values) and that the
        time_array and voltage_array are the same length.

        Parameters
        ----------
        time_array:     Numpy time array read in from CSV file (or specified
                        directly in testing cases)
        voltage_array:  Numpy voltage array read in from CSV file (or
                        specified directly for testing cases)

        Returns
        -------
        None, but raises value errors if invalid.
        """
        if np.isnan(time_array).any() or np.isnan(voltage_array).any():
            raise TypeError

        if time_array.size is not voltage_array.size:
            raise ValueError

    def validate_duration(self, time_array, duration):
        """Checks that a user-specified duration for BPM calculation is
        valid, i.e. within the range of possible time values from the
        time_array that was read in from the CSV file.

        Parameters
        ----------
        time_array: numpy array of time values (from CSV file, or directly
                    inserted for testing cases.
        duration:   tuple specifying the min and max times defining the
                    duration of interest, specified by user.

        Returns
        -------

        """
        min_time = np.amin(time_array)
        max_time = np.amax(time_array)

        if duration[0] < min_time or duration[1] > max_time:
            raise ValueError

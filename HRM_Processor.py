import numpy as np


class HRM_Processor:
    def __init__(self, DataReader):
        """Constructor for HRM_Processor

        Parameters
        ----------
        DataReader: DataReader
                    A DataReader object which had read in data from a CSV
                    file and created and output_dict with the relevant data
                    for the HRM_Processor
        """

        self.input_data = DataReader.output_dict
        self.output_dict = {}
        self.write_outputs_to_dict()

    def write_outputs_to_dict(self):
        """Writes all of the HRM_Processor's outputs to it's output
        dictionary by calling the relevant functions to generate those outputs.

        Returns
        -------
        None

        """
        voltage_extremes = self.determine_voltage_extremes(self.input_data[
                                                          "voltage"])
        self.output_dict["voltage_extremes"] = voltage_extremes

        ecg_strip_duration = self.determine_ecg_strip_duration(self.input_data[
                                                                   "time"])
        self.output_dict["duration"] = ecg_strip_duration

    def determine_voltage_extremes(self, voltage):
        """Determines the min and max values of the voltage data

        Parameters
        ----------
        voltage:    numpy array
                    Contains the voltage ad

        Returns
        -------
        voltage_extremes:   tuple(float, float)
                            A tuple containing the min and max values of the
                            voltage data in the format (min, max)

        """
        voltage_min = np.amin(voltage)
        voltage_max = np.amax(voltage)

        voltage_extremes = (voltage_min, voltage_max)

        return voltage_extremes

    def determine_ecg_strip_duration(self, time):
        """

        Parameters
        ----------
        time:       np array
                    Contains the time vector from the CSV file

        Returns
        -------
        strip_duration: float
                        The max time value of the ecg strip = strip duration
        """
        strip_duration = np.amax(time)
        return strip_duration

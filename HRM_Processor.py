import numpy as np


class HRM_Processor:
    """The HRM_Processer takes in time, voltage, and BPM duration from the
    DataReader and calculates the outputs for the heart rate monitor.

    Attributes
    ----------
    csv_file:   str
                A strain containing the path for the CSV file.
    input_data: dict
                A dictionary containing the data read in from the DataReader
                passed into the initialization function
    output_dict: dict
                A dictionary containing the heart rate metrics that will be
                written to the JSON file by the DataWriter.

    """
    def __init__(self, DataReader):
        """Constructor for HRM_Processor

        Parameters
        ----------
        DataReader: DataReader
                    A DataReader object which had read in data from a CSV
                    file and created and output_dict with the relevant data
                    for the HRM_Processor
        """
        self.csv_file = DataReader.csv_file_path
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

        beat_start_times = self.determine_beat_start_times(
            self.input_data["time"], self.input_data["voltage"])
        self.output_dict["beats"] = beat_start_times

        num_beats = self.determine_num_beats(beat_start_times)
        self.output_dict["num_beats"] = num_beats

        try:
            mean_hr_bpm = self.determine_bpm(beat_start_times, self.input_data[
                                                                "duration"])
            self.output_dict["mean_hr_bpm"] = mean_hr_bpm
        except ValueError:
            print("Invalid duration (no beats in that duration)")

    def determine_voltage_extremes(self, voltage):
        """Determines the min and max values of the voltage data

        Parameters
        ----------
        voltage:    numpy array
                    Contains the voltage data from the CSV file

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
        """Determines the length of the ECG strip

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

    def determine_beat_start_times(self, time, voltage):
        """Create a numpy array with the starting time for each beat.

        The starting time of a beat is defined as the peak of the QRS
        complex. This function essentially synthesizes the outputs of helper
        functions to implement a thresholding beat detection algorithm. This
        algorithm essentially identifies continuous regions where the voltage
        trace is continuously above the threshold (which should correspond to
        the QRS complex of a beat), finds maximum of the voltage trace within
        each continuous region, and then indexes the corresponding time value
        in the time array to determine the start time of each beat.

        Parameters
        ----------
        time:       Numpy array
                    Time values read in from CSV file
        voltage:    Numpy array
                    Voltages read in from CSV file

        Returns
        -------
        start_times:    Numpy array
                        Start times of each beat (defined as the time of the
                        peak of each QRS complex)
        """
        threshold = self.determine_threshold(voltage)
        inx_above_threshold = self.find_indices_above_threshold(voltage,
                                                                threshold)
        beat_sep_points = self.find_beat_separation_points(inx_above_threshold)
        qrs_peak_inx = self.find_beat_separation_points(beat_sep_points)
        start_times = self.index_beat_start_times(time, qrs_peak_inx)
        return start_times

    def determine_threshold(self, voltage):
        """Determines the threshold voltage for defining the start and end
        of the QRS complex.

        The threshold voltage is 75% of the peak voltage value.

        Parameters
        ----------
        voltage:    Numpy array
                    The voltage values from the CSV file

        Returns
        -------
        threshold:  float
                    The 'threshold' for the QRS complex, which occurs when
                    the voltage value is above 75% of its original value.
        """
        threshold = 0.75*np.amax(voltage)

        return threshold

    def find_indices_above_threshold(self, voltage, threshold):
        """Finds the indices of the voltage array where it is above the
        threshold value.

        Parameters
        ----------
        voltage:    Numpy array
                    The voltage values from the CSV file
        threshold:  float
                    The threshold for the QRS complex, determined by the
                    determine_threshold function.

        Returns
        -------
        indices:    Numpy array
                    The indices for which the voltage data exceeds the
                    threshold value.
        """
        indices = np.argwhere(voltage > threshold).flatten()
        return indices

    def find_beat_separation_points(self, indices_array):
        """Finds the indices where the QRS complex of each beat goes below
        the threshold.

        Separation points are points where the difference between
        neighboring elements in the indices array (=the indices where the
        voltage is above threshold) is greater than 2. This indicates that
        there is a 'jump' in indices above the threshold, implying that a
        significant amount of time passed. My code interprets this
        significant amount of time passing as a separation between beats.
        This function indexes the indices_array at the locations where there is
        a jump/separation, which results in the indices in the original
        voltage array where the QRS complex goes below the threshold for
        each beat.

        Parameters
        ----------
        indices_array:  numpy array
                        The indices of the voltage array where the voltage
                        values are above the threshold values.

        Returns
        -------
        beat_sep_inx:   numpy array
                        The indices in the voltage array where there is a
                        discontinuity b/w voltage indices above the
                        threshold. So, these represent the points at which
                        the QRS complex goes below the threshold for each
                        beat (i.e. the beat separations)
        """

        diff_array = np.diff(indices_array)
        beat_seps = np.argwhere(diff_array > 2).flatten()
        beat_sep_inx = indices_array[beat_seps]
        return beat_sep_inx

    def find_qrs_peak_indices(self, voltage, beat_sep_inx):
        """Indexes the voltage array during the QRS complex of each beat
        (determined by the indices specified in beat_sep_inx), finds the max
        value in each range, and finds the index of the peak of the QRS
        complex.

        Parameters
        ----------
        voltage:    numpy array
                    Voltage values read in from CSV file
        beat_sep_inx:   Numpy array
                        Indices where the voltage goes below the threshold
                        value at the end of the QRS complex

        Returns
        -------
        qrs_peak_locations:  numpy array
                            The locations of the peak of the QRS complex for
                            each beat
        """
        start_inx = 0
        qrs_peak_locations = np.array([])
        for beat_sep in beat_sep_inx:
            temp = voltage[start_inx:beat_sep+1]
            qrs_max_loc = start_inx + np.asscalar(np.where(temp == np.amax(
                temp))[0])
            qrs_peak_locations = np.append(qrs_peak_locations, qrs_max_loc)
            start_inx = beat_sep
        temp = voltage[beat_sep+1:np.alen(voltage)]
        qrs_max_loc = start_inx + np.asscalar(np.where(temp == np.amax(
            temp))[0])
        qrs_peak_locations = np.append(qrs_peak_locations, qrs_max_loc)

        return qrs_peak_locations

    def index_beat_start_times(self, time, qrs_peak_locations):
        """Determines the beat start times by indexing the time array at the
        peak of each QRS complex, as determined by qrs_locations.

        Parameters
        ----------
        time:               numpy array
                            Time array read in from the CSV file.

        qrs_peak_locations: numpy array
                            Contains the indices where the peak of the QRS
                            complex for each beat is located.

        Returns
        -------
        beat_start_times:    numpy array
                            Contains the times where each beat starts (defined
                            as the time of the peak of the QRS complex)
        """

        beat_start_times = time[qrs_peak_locations].flatten()
        return beat_start_times

    def determine_num_beats(self, beat_start_times):
        """Determines the number of beats that occurred based on the number
        of elements in the beat_start_times array

        Parameters
        ----------
        beat_start_times:   numpy array
                            A numpy array containing the start times (time
                            of the peak of each QRS complex) fo reach beat

        Returns
        -------
        num_beats:          int
                            The number of beats
        """
        num_beats = np.size(beat_start_times)
        return num_beats

    def determine_bpm(self, beat_start_times, duration):
        """Determines the mean beats per minute (BPM) within a specified
        duration of time.

        Parameters
        ----------
        beat_start_times:   Numpy array
                            Specifies the starting time of each beat in the
                            ECG strip.
        duration:           tuple(float, float)
                            A tuple specifying the start and end of the
                            duration over which the BPM will be calculated.

        Returns
        -------
        mean_hr_bpm: float
                     The mean heart rate in BPM within the specified
                     duration.
        """
        start_inx = np.argmax(beat_start_times >= duration[0])
        end_inx = np.argmax(beat_start_times >= duration[1])

        if beat_start_times[-1] < duration[1]:
            end_inx = beat_start_times.size - 1

        num_beats_in_duration = end_inx - start_inx
        time_in_seconds = duration[1] - duration[0]
        if time_in_seconds == 0:
            raise ValueError
        time_in_minutes = time_in_seconds / 60

        mean_hr_bpm = num_beats_in_duration / time_in_minutes
        return mean_hr_bpm

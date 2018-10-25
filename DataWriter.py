import json
import os


class DataWriter:
    """Writes the output metrics from the HRM_Processor to a JSON file.

    Attributes
    ----------
    metrics:    dict
                A dictionary containing the heart rate metrics from the
                HRM_Processor

    csv_file:   str
                The name of the CSV file with the original ECG data
    """
    def __init__(self, hrm):
        """Constructor for DataWriter Object

        Parameters
        ----------
        hrm:    HRM_Processor
                An HRM_Processor which has an output_dict containing the
                relevant output parameters to be written to the JSON file.
        """

        self.metrics = self.convert_np_arrays(hrm.output_dict)
        self.csv_file = hrm.csv_file
        output_file = self.get_output_file_name(self.csv_file)
        self.write_to_json(self.metrics, output_file)

    def get_output_file_name(self, csv_file):
        """Finds the root file name (i.e. the file name without the .csv
        extension) and creates a file name that is equivalent but with a
        .json extension.

        Parameters
        ----------
        csv_file:   str
                    A string with the CSV file path

        Returns
        -------
        output_file str
                    The output file path, which is the same as the csv_file
                    name with a .json extension instead of a .csv extension

        """
        root_file_name = os.path.splitext(csv_file)[0]
        output_file = root_file_name + ".json"
        return output_file

    def convert_np_arrays(self, input_dict):
        """Converts numpy arrays in the input_dict to a regular,
        serializable python lists, so that the dictionary can be written to
        a JSON file.

        Parameters
        ----------
        input_dict: dict
                    Expecting a dictionary from the HRM_Processor that has a
                    numpy array in the 'beats' entry
        Returns
        -------
        serializable_dict:  dict
                            A dictionary that is equivalent to the
                            input_dict, but the "beats" entry has been
                            converted from a numpy array to a dictionary.

        """
        serializable_dict = input_dict
        serializable_dict["beats"] = input_dict["beats"].tolist()

        return serializable_dict

    def write_to_json(self, metrics, filename):
        """Writes the metrics dictionary to the specified filename as a JSON
        file.

        Parameters
        ----------
        metrics:    dict
                    A dictionary containing the relevant ECG output
                    parameters associated with the heart rate monitor.
        filename:   str
                    A string specifying the desired file output path

        Returns
        -------
        None
        """

        with open(filename, 'w') as outfile:
            json.dump(metrics, outfile)

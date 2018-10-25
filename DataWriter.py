import json
import os


class DataWriter:
    def __init__(self, hrm):
        """Constructor for DataWriter Object

        Parameters
        ----------
        hrm:    HRM_Processor
                An HRM_Processor which has an output_dict containing the
                relevant output parameters to be written to the JSON file.
        """

        self.metrics = hrm.output_dict
        self.csv_file = hrm.csv_file
        output_file = self.get_output_file_name(self.csv_file)

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

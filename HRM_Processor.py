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

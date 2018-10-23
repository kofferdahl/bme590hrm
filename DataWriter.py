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

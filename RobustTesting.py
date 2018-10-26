import os
import logging
from DataReader import DataReader
from DataWriter import DataWriter
from HRM_Processor import HRM_Processor

os.chdir("test_data")

for i in range(1, 33):
    base_file_name = "test_data" + str(i)
    file_name = base_file_name + ".csv"
    print(file_name)

    logging.basicConfig(filename=base_file_name + "_logs.txt",
                        format='%(asctime)s %(levelname)s:%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        dr = DataReader(file_name)
        hrm = HRM_Processor(dr)
        dw = DataWriter(hrm)
    except(FileNotFoundError, ValueError, TypeError):
        logging.info("Attempt to make process file was terminated.")
    # Remove all handlers associated with the root logger object.
    # this allows for the creation of a new log file for each test file
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

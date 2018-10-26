# bme590hrm
Heart rate monitor project for BME 590 (Medical Device Software Design)

To run this project, you will need to install the packages specified in requirements.txt.

This driver script for this project is HRM_Driver.py. This script prompts a user to enter a file path to a CSV file in the command window window, and optionally specify a duration for BPM calculation. There is also a RobustTesting script, which iterates through all of the files in test_data, and produces JSON files and logs for each .csv file. 

The 3 building blocks of this program are the DataReader, the HRM_Processor, and the DataWriter.
The DataReader handles getting the data from the csv file, basic validations, and passing that data to the HRM_Processor.
The HRM_Processor determines all the beat detection / heart rate monitor metrics, and passes them to the DataWriter.
The DataWriter writes the metrics dictionary from the HRM_Processor to a JSON file.

The beat detection algorithm uses a basic thresholding approach to detect QRS peaks. It essentially finds regions where the ECG signal is continuously above the threshold value. It takes the max voltage within that region (which should correspond to the peak of the QRS complex), and returns the corresponding time of that max voltage as the start time of that beat.

The criteria for rejecting a ECG signal is based on the heart rate for the strip. Values that are defined as physiologically unrealistic / unlike (BPM > 150 or BPM < 36) are considered to be more likely due to the algorithm failing rather than the actual values. In these cases, JSON files are not written, the user is appropriately informed, and the event is logged. 

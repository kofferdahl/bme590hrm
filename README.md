# bme590hrm
Heart rate monitor project for BME 590 (Medical Device Software Design)

This driver script for this project is HRM_Driver.py. This script prompts a user to enter a file path to a CSV file in the command window window, and optionally specify a duration for BPM calculation. 

The 3 building blocks of this program are the DataReader, the HRM_Processor, and the DataWriter.
The DataReader handles getting the data from the csv file, basic validations, and passing that data to the HRM_Processor.
The HRM_Processor determines all the beat detection / heart rate monitor metrics, and passes them to the DataWriter.
The DataWriter writes the metrics dictionary from the HRM_Processor to a JSON file.

The beat detection algorithm uses a basic thresholding approach to detect QRS peaks. It essentially finds regions where the ECG signal is continuously above the threshold value. It takes the max voltage within that region (which should correspond to the peak of the QRS complex), and returns the corresponding time of that max voltage as the start time of that beat.

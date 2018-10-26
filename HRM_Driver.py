from DataReader import DataReader
from DataWriter import DataWriter
from HRM_Processor import HRM_Processor


def get_file_name():
    file_name = input("Please enter a file name: ")
    return file_name


def get_wants_duration():
    wants_duration = input("Would you like to enter a duration for BPM "
                           "calculation? Enter 1 for yes, enter 0 for no")

    if wants_duration == "1":
        return True
    else:
        return False


def get_duration():
    min_duration = input("Please enter the start of the duration for BPM "
                         "calculation in seconds: ")
    max_duration = input("Please enter the end of the duration for BPM "
                         "calculation in seconds: ")
    duration = (float(min_duration), float(max_duration))
    return duration


def main():
    file_name = get_file_name()

    wants_duration = get_wants_duration()
    print(wants_duration)
    if wants_duration:
        print("wants duration!")
        duration = get_duration()
        dr = DataReader(file_name, duration)
    else:
        dr = DataReader(file_name)

    hrm = HRM_Processor(dr)
    dw = DataWriter(hrm)


if __name__ == "__main__":
    main()

import os
from src.edge_platform.raspberrypi.SensorDataCaptureAnalytics import SensorDataCapture
from src.edge_platform.raspberrypi.config import *
from data.config import DATAPARAMS

def get_header_fields(_file, delimiter=','):
    """
    Parses a data file to return the header fields based on the delimiter provided
    Input : Data file
    Output : List of Header files in the data file
    """
    header_line = ''
    with open(_file, 'r') as file_handle:
        header_line = file_handle.readline()

    print(header_line)
    result = header_line.split(delimiter)
    header = [i.strip() for i in result if i != '\n']
    return header


def capture_raw_data(_fieldnames, _data_parent_directory, _local_directory, _data_file_name):
    """
    wrapper function that captures raw data from a sensor platform using methods of the SensorDataCapture class
    :param _fieldnames: list containing fieldnames
    :param _data_parent_directory: parent directory where all experiments are stored e.g., data/
    :param _local_directory: sub-directory corresponding to the specific experiment
    :param _data_file_name: name of the data file
    :return:
    """
    print("Capturing Sensor Data")
    sdc = SensorDataCapture(_fieldnames, _data_parent_directory, _local_directory, _data_file_name, False)
    sdc.captureData()


def analyze(_fieldnames, _data_parent_directory, _local_directory, _data_file_name):
    """
    Analyzes the raw data and stores the FFT coefficients into the merged-training-*.csv file
    :param _fieldnames: list containing fieldnames
    :param _data_parent_directory: parent directory where all experiments are stored e.g., data/
    :param _local_directory: sub-directory corresponding to the specific experiment
    :param _data_file_name: name of the data file
    :return:
    """
    print("Analyzing Sensor Data")
    sdc = SensorDataCapture(_fieldnames, _data_parent_directory, _local_directory, _data_file_name, False)

    # Separating the fields into discrete_output_fields & analog_output_fields
    discrete_output_fields = [field.strip() for field in _fieldnames if 'Cout' in field]
    analog_output_fields = [field.strip() for field in _fieldnames if 'Aout' in field]
    print(discrete_output_fields, analog_output_fields)

    # Analysis for Multiple Window Lengths i.e., one file for each window size
    for w in PARAMS.window_lengths:
        # getDataStats contain both time domain and frequency domain analysis
        sdc.getDataStats(w, discrete_output_fields, analog_output_fields)

        # Reformatting file for input to the ML model
        for filename in os.listdir(os.path.join(_data_parent_directory, _local_directory)):
            if 'fft' in filename and str(w) in filename:
                sdc.reorganizecsv_file(filename, '-'.join(['merged-training', str(w)]) + '.csv')
            else:
                continue


if __name__ == "__main__":
    if PARAMS.capture_switch:
        data_parent_directory = str(DATAPARAMS.data_dir)  # os.getcwd() if data is to be stored in the same directory
        local_directory = ''  # enter the experiment sub-folder
        data_file_name = ''  # enter the name of the file containing the data
        capture_raw_data(PARAMS.list_of_fieldnames, data_parent_directory, local_directory, data_file_name)
    else:
        data_parent_directory = str(DATAPARAMS.data_dir) # os.getcwd() if data is in the same directory
        local_directory = 'fault_classification_classV_classIIIb_classIVb/20200406_134751_6hr_run'  # enter the experiment sub-folder
        data_file_name = 'pir_evm_raw_data.csv'  # enter the name of the file containing the data
        fieldnames = get_header_fields(os.path.join(data_parent_directory, local_directory, data_file_name))
        analyze(fieldnames, data_parent_directory, local_directory, data_file_name)

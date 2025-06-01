""" Helper for creating constant variables
    Found in: https://stackoverflow.com/questions/2682745/how-to-create-a-constant-in-python
"""


class MetaConst(type):
    def __getattr__(cls, key):
        return cls[key]

    def __setattr__(cls, key, value):
        raise TypeError


class Const(object, metaclass=MetaConst):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        raise TypeError


class PARAMS(Const):
    """
    This class stores all the configuration parameters
    EXPT_DURATION_IN_SECS : Capture Duration
    SERIAL_FLUSH_DURATION_IN_SECS : Flushing the serial device to remove garbage data esp in case of power loss
    serial_device : USB serial device depending on the deployment platform
    window_lengths : List of Window Lengths Used for Analysis, we use 1024 as it gives best accuracy in Fault Detection
                    Example : window_lengths = [512, 256, 128, 64, 32]
    capture_switch : Manually Toggling Data Capture/ Data Analysis Phase, capture_switch = True => capturing raw data
                        capture_switch = False => analyzing raw data
    list_of_fieldnames : Manually Maintaining List of Fields in the Data Capture.
                    Example : list_of_fieldnames = ['Sample (ms)', 'Cout (Sensor1)', 'Aout (Sensor1)',
                            'Cout (Sensor2)', 'Aout (Sensor2)',
                            'Cout (Sensor3)', 'Aout (Sensor3)',
                            'Cout (Sensor4)', 'Aout (Sensor4)',
                            'Cout (Sensor5)', 'Aout (Sensor5)',]
    """

    EXPT_DURATION_IN_SECS = 120
    SERIAL_FLUSH_DURATION_IN_SECS = 5
    serial_device = '/dev/cu.usbmodem1421'
    window_lengths = [1024]
    capture_switch = False
    list_of_fieldnames = ['Sample (ms)', 'Cout', 'Aout']


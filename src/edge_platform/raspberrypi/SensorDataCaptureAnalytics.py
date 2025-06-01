import csv, platform
import datetime, math, os, serial, subprocess, time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.edge_platform.raspberrypi.config import *
from matplotlib.ticker import FormatStrFormatter  # for controlling precision of axis ticks
from scipy.fftpack import rfft
from difflib import SequenceMatcher
from spectrum import Periodogram
from itertools import cycle

class SensorDataCapture:

    def __init__(self, _fieldnames, _data_parent_directory, _local_directory, _data_file_name, _plot_fft):
        """
        Constructor of SensorDataCapture class
        :param _fieldnames: list containing fieldnames
        :param _data_parent_directory: parent directory where all experiments are stored e.g., data/
        :param _local_directory: sub-directory corresponding to the specific experiment
        :param _data_file_name: name of the data file
        :param _plot_fft: boolean indicating if FFT would be plotted
        """
        self.list_of_fieldnames = _fieldnames
        self.data_parent_directory = _data_parent_directory
        self.local_directory = _local_directory
        self.filename = _data_file_name
        self.plot_fft = _plot_fft

    def captureData(self):
        """
        Function copying data from serial device to csv file
        :return:
        """
        self.data_capture_duration_in_secs = PARAMS.EXPT_DURATION_IN_SECS
        self.arduinoSerialData = serial.Serial(PARAMS.serial_device, 9600)
        self.arduinoSerialData.flushInput()
        time.sleep(PARAMS.SERIAL_FLfault_typeUSH_DURATION_IN_SECS)
        self.arduinoSerialData.flushInput()

        start_time = time.time()
        mydir = os.path.join(os.getcwd(), self.local_directory, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
        os.makedirs(mydir)
        f = open(os.path.join(mydir, self.filename), 'w')
        f.write(','.join(self.list_of_fieldnames) + '\n')

        while (time.time() - start_time) <= self.data_capture_duration_in_secs :
            # Copy Serial Terminal to CSV
            if self.arduinoSerialData.inWaiting():
                myData = self.arduinoSerialData.readline().decode().strip()
                # f.write(time.ctime(time.time()) + " -> " +  myData + '\n')
                f.write(myData+'\n')

        f.flush()
        f.close()
        self.arduinoSerialData.close()

    def getDataStats(self, window_length, cout_fields, aout_fields,
                     single_feature_file=True, plot_raw=False, plot_freq=False, window_analysis=False, fp_fn_analysis= True):
        """
        Function that aggregrates several statistics computed on raw data
        including both time and frequency domain analysis
        :param window_length:
        :param cout_fields:
        :param aout_fields:
        :param single_feature_file:
        :param plot_raw:
        :param plot_freq:
        :param window_analysis: Windows Analysis
        :param fp_fn_analysis: FalsePositives-FalseNegatives Analysis
        :return:
        """
        df = pd.read_csv(os.path.join(self.data_parent_directory, self.local_directory, self.filename))

        ########################
        # Timestamp Analysis
        ########################
        time_series = df.iloc[:, 0]  # Inter-sample Time for FFT Calculation
        time_diff = [float(t) - float(s) for s, t in zip(time_series, time_series[1:])]
        inter_sample_time_in_secs = math.ceil(np.mean(time_diff))/1e3
        print('Inter-sample time : %f'%inter_sample_time_in_secs,
              'Window time : %f'%(inter_sample_time_in_secs*window_length))

        # Write timestamp values to a file
        timestamps_file = os.path.join(self.data_parent_directory, self.local_directory,
                    '-'.join(['timestamps', str(window_length)]) + '.txt')
        if not os.path.exists(timestamps_file):
            final = [time_series[i: i + window_length] for i in range(0, len(time_series) - window_length + 1, window_length)]
            with open(timestamps_file, 'a') as timestamps_file_handle:
                ctr = 0
                for x in final:
                    # print(type(final))
                    timestamps_file_handle.write(str(pd.Series(np.array(x))[0]) + ',' +
                                                 str(pd.Series(np.array(x)).iloc[-1]) + '\n')
                    ctr += 1
                print("Number of chunks = ", ctr)  # This is the number of chunks
        #########################

        inter_sample_time_in_secs = 0.040
        data_file = None
        label_file = None

        if not single_feature_file:
            data_file = os.path.join(self.data_parent_directory, self.local_directory,
                                     '-'.join(['composite', str(window_length), self.filename.split('.')[0]]) + '.txt')
            label_file = os.path.join(self.data_parent_directory, self.local_directory,
                                      '-'.join(['label', str(window_length), self.filename.split('.')[0]]) + '.txt')

            if os.path.exists(data_file):
                os.remove(data_file)
            if os.path.exists(label_file):
                os.remove(label_file)

        #########################
        # Aout Field Analysis
        #########################
        for f in aout_fields:
            if single_feature_file:
                self.writeFFTCoeff(window_length, inter_sample_time_in_secs, df[f].values.tolist(), f)
            else:
                self.split_into_chunks(df[f].values.tolist(), f, window_length, window_length,
                                       inter_sample_time_in_secs, data_file, label_file)
                if platform.system() == 'Linux':
                    subprocess.call(["sed", "-i", 's/\[//g', str(data_file)])
                    subprocess.call(["sed", "-i", 's/\]//g', str(data_file)])
                    subprocess.call(["sed", "-i", 's/\,//g', str(data_file)])
                elif platform.system() == 'Darwin':
                    subprocess.call(["sed", "-i.bu", 's/\[//g', str(data_file)])
                    subprocess.call(["sed", "-i.bu", 's/\]//g', str(data_file)])
                    subprocess.call(["sed", "-i.bu", 's/\,//g', str(data_file)])
            if plot_freq:
                # self.plot_spectrogram(window_length, inter_sample_time_in_secs, df[f].values.tolist(), f)
                if window_analysis:
                    start_time = 100000
                    end_time = 150000
                    start = self.findIndex(time_series, start_time)
                    end = self.findIndex(time_series, end_time)
                    self.plot_FFT(window_length, inter_sample_time_in_secs, df[f].values.tolist()[start:end+1], f)
                else:
                    self.plot_FFT(window_length, inter_sample_time_in_secs, df[f].values.tolist(), f)

        #########################
        # Cout Field Analysis
        #########################
        if fp_fn_analysis:
            for f in cout_fields:
                self.failure_characterize(df[f].values.tolist(), f, window_length, window_length)

        # Plotting the raw data -- Cout, Aout for a single sensor
        if plot_raw:
            print(self.list_of_fieldnames)

            # Plotting with respect to Normal
            for f in self.list_of_fieldnames:
                if 'Cout' in f and 'Normal' not in f:
                    print("Ashish",f)
                    self.plotData(f, 'Cout (Normal)', df[f].values.tolist(), df['Cout (Normal)'].values.tolist(), False)
                if 'Aout' in f and 'Normal' not in f:
                    print("Ashish", f)
                    self.plotData(f, 'Aout (Normal)', df[f].values.tolist(), df['Aout (Normal)'].values.tolist(), False)
            '''
            # Plotting the raw data -- Cout, Aout across all the sensors
            for f,g in zip(self.list_of_fieldnames[1::2], self.list_of_fieldnames[2::2]):
                if 'Cout' in f and 'Aout' in g:
                    print("Plotting Cout, Aout data")
                    self.plotData(f, g, df[f].values.tolist(), df[g].values.tolist(), False)
                elif 'Aout' in f and 'Cout' in g:
                    print("Plotting Aout, Cout data")
                    self.plotData(g, f, df[g].values.tolist(), df[f].values.tolist(), False)

            # Plotting the raw data -- Cout across all the sensors
            print(cout_fields)
            for f,g in zip(cout_fields[0::2], cout_fields[1::2]):
                print("Plotting only Cout data")
                self.plotData(f, g, df[f].values.tolist(), df[g].values.tolist(), True)

            # Plotting the raw data -- Aout across all the sensors
            print(aout_fields)
            for f,g in zip(aout_fields[0::2], aout_fields[1::2]):
                print("Plotting only Aout data")
                self.plotData(f, g, df[f].values.tolist(), df[g].values.tolist(), False)
            '''

    def failure_characterize(self, data, sensor_type, chunk_size, overlap):
        """
        Function to write the chunks into a file
        :param data:
        :param sensor_type:
        :param chunk_size:
        :param overlap:
        :return:
        """
        final = [data[i: i + chunk_size] for i in range(0, len(data)-chunk_size+1, overlap)]
        label = sensor_type[sensor_type.find('(')+1:sensor_type.find(')')]

        cout_data_file = os.path.join(self.data_parent_directory, self.local_directory,
                         '-'.join(['Cout', str(chunk_size), str(label)]) + '.txt')

        with open(cout_data_file, 'a') as data_file_handle:
            print(cout_data_file)
            ctr = 0
            for x in final:
                # print(len(x), type(x))
                data_file_handle.write(str(sum(x)/len(x)) + '\n')
                ctr += 1
            print("Number of chunks = ", ctr)  # This is the number of chunks


    def split_into_chunks(self, data, sensor_type, chunk_size, overlap, inter_sample_time_in_secs,
                          data_file, label_file):
        """
        Function to split the data into windows (called chunks)
        :param data:
        :param sensor_type:
        :param chunk_size:
        :param overlap:
        :param inter_sample_time_in_secs:
        :param data_file:
        :param label_file:
        :return:
        """
        final = [data[i: i + chunk_size] for i in range(0, len(data)-chunk_size+1, overlap)]
        label = sensor_type[sensor_type.find('(')+1:sensor_type.find(')')]

        # Plotting the variance
        fig, ax = plt.subplots(1,1)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.ylabel(r'Std. Dev.')
        plt.xlabel(r'Time (secs)')

        std_dev = list()
        chunk_time = list()

        with open(data_file, 'a') as data_file_handle, open(label_file, 'a') as label_file_handle:
            print(data_file, label_file)
            ctr = 0
            for x in final:
                y = list(x - np.mean(x))
                sd = np.std(y)
                ct = (chunk_size * inter_sample_time_in_secs * ctr) + (chunk_size * inter_sample_time_in_secs)/2
                # print("{:.2f}".format(chunk_size * inter_sample_time_in_secs * ctr), "{:.2f}".format(sd), label)
                data_file_handle.write(str(y) + '\n')
                label_file_handle.write(label + '\n')
                std_dev.append(sd)
                chunk_time.append(ct)
                ctr += 1

        plt.bar(chunk_time, std_dev, linestyle='-', color='b', alpha=0.5)
        plt.savefig(os.path.join(self.data_parent_directory, self.local_directory,
                    '-'.join([self.filename.split('.')[0], 'Aout-Variance', label, str(chunk_size)]) + '.png'),
                    bbox_inches="tight")

    def plot_spectrogram(self, window_length, inter_sample_length, time_series, time_series_string):
        """
        Function to plot spectrogram
        :param window_length:
        :param inter_sample_length:
        :param time_series:
        :param time_series_string:
        :return:
        """
        sensor_type = time_series_string[time_series_string.find('(')+1:time_series_string.find(')')]

        '''
        CHUNK_SIZE = window_length
        OVERLAP = CHUNK_SIZE // 2
        FFT_POINT = CHUNK_SIZE

        x = np.array(time_series)
        f, t, Sxx = spectrogram(x,
                    fs=(1/inter_sample_length),
                    window='hamming',
                    nperseg=CHUNK_SIZE,
                    noverlap=OVERLAP,
                    nfft=FFT_POINT,
                    return_onesided=True,
                    mode='magnitude'
                    )

        plt.pcolormesh(t, f, Sxx)
        '''
        plt.close()
        # Plotting settings
        plt.rcdefaults()
        plt.rcParams["font.family"] = "Arial"
        plt.rcParams['font.size'] = 24
        plt.rcParams['legend.fontsize'] = 24
        plt.rcParams['axes.titlesize'] = 24
        plt.rcParams['ytick.labelsize'] = 24
        plt.rcParams['xtick.labelsize'] = 24
        plt.rcParams['figure.figsize'] = 8, 5
        plt.gcf().set_size_inches(10, 7)

        p = Periodogram(time_series, sampling=(1/inter_sample_length))
        p.run()
        p.plot()

        '''
        plt.title(sensor_type)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.ylim(bottom=0, top=10)
        '''
        plt.title(sensor_type)
        plt.xlim(left=0, right=10)
        plt.xlabel('Frequency (Hz)')
        plt.savefig(os.path.join(self.data_parent_directory, self.local_directory,
                            self.filename.split('.')[0] + '-Spectrogram' + str(window_length) + sensor_type + '.png'),
                            bbox_inches="tight")

        # plt.show()

    # This function is used for plotting FFT
    def plot_FFT (self, window_length, inter_sample_length, time_series, time_series_string):

        print("Inside plot_FFT, plotting %s" %(time_series_string))
        sensor_type = time_series_string[time_series_string.find('(')+1:time_series_string.find(')')]

        dt = inter_sample_length
        fa = 1/dt

        print('dt=%.5fs (Sample Time)' % dt)
        print('fa=%.2fHz (Frequency)' % fa)
        j=0

        plt.clf()
        # Plotting settings
        plt.rcdefaults()
        plt.rcParams["font.family"] = "Arial"
        plt.rcParams['font.size'] = 24
        plt.rcParams['legend.fontsize'] = 24
        plt.rcParams['axes.titlesize'] = 24
        plt.rcParams['ytick.labelsize'] = 24
        plt.rcParams['xtick.labelsize'] = 24
        plt.rcParams['figure.figsize'] = 8, 5
        plt.gcf().set_size_inches(10, 7)

        while j+window_length <= len(time_series):
            Y = np.fft.fft(time_series[j:j+window_length])
            N = len(Y) // 2
            X = np.linspace(0, fa / 2, N, endpoint=True)
            # plt.plot(X, time_series[j:j+window_length])
            plt.plot(X, np.abs(Y[:N])/N, color='k')
            plt.xlabel(r'Frequency ($Hz$)')
            plt.ylabel(r'Spectral Amplitude')
            plt.xlim(left=0, right=10)

            j += window_length

        plt.savefig(os.path.join(self.data_parent_directory, self.local_directory,  self.filename.split('.')[0] + '-FFT-' + str(window_length) + '-' + sensor_type + '.png'), bbox_inches = "tight")

        # plt.show()

    def writeFFTCoeff(self, window_length, inter_sample_time_in_secs, time_series, time_series_string):
        """
        Function to write FFT Coefficients to a file
        :param window_length:
        :param inter_sample_time_in_secs:
        :param time_series:
        :param time_series_string:
        :return:
        """

        j = 0
        plot_every = 20
        sqrt_num_subplots = math.ceil(math.sqrt(len(time_series)/(plot_every * window_length)))
        # print(sqrt_num_subplots)

        fig, ax = plt.subplots()

        if os.path.exists(os.path.join(self.data_parent_directory, self.local_directory, '-'.join(['fft', str(window_length), time_series_string]) + '.csv')):
            print("File already exists, opening in append mode")
            f = open(os.path.join(self.data_parent_directory, self.local_directory, '-'.join(['fft', str(window_length), time_series_string]) + '.csv'), 'a')
        else:
            print("File doesn't exist, opening in write mode")
            f = open(os.path.join(self.data_parent_directory, self.local_directory, '-'.join(['fft', str(window_length), time_series_string]) + '.csv'), 'w')
            f.write(time_series_string + '-FFT' + '\n')

        while (j + window_length) <= len(time_series):

            #################
            # FFT Parameters
            #################
            # number of sample points
            N = window_length
            # frequency of signal
            T = inter_sample_time_in_secs
            # create x-axis for time length of signal
            x = np.linspace(0, N * T, N)
            # create array that corresponds to values in signal
            y = np.array(time_series[j: (j + window_length)])
            # print(y)
            # print(np.mean(y)*N)

            '''
            To Do : cleanly take the last window samples too 
            if (i+window_length <= len(Cout_normal)):
                y = Cout_normal[i: (i+window_length)]
                print(type(y))
            else:
                print('ashish')
                y = Cout_normal[i:]
                print(len(y))
                y.append(pd.DataFrame([0]*(window_length-(len(Cout_normal)-i))))
                print(len(y))
            '''
            # create new x-axis: frequency from signal
            xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
            # print(len(xf))

            # perform FFT on signal
            yf = rfft(y)
            # print(yf[0]) # Sanity Check to see the first number is the DC Coefficient -> np.mean(y)*N

            writer = csv.writer(f)
            writer.writerow(abs(yf[:N//2]))

            # plot results
            if self.plot_fft and (j/window_length) % plot_every == 0:
                ax = fig.add_subplot(sqrt_num_subplots, sqrt_num_subplots, 1+(j/(plot_every * window_length)))
                ax.set_xlabel(r'Frequency (Hz)')
                ax.set_ylabel(r'Spectral Amplitude')
                ax.set_xlim(0, 1.0 / (2.0 * T))
                ax.set_ylim(0, window_length)

                ax.plot(xf, yf[0:N // 2])
                # ax.grid()

            # plt.legend(loc=1)
            j += window_length

        if self.plot_fft:
            # plt.tight_layout()
            # plt.show()
            plt.savefig(os.path.join(self.data_parent_directory, self.local_directory, self.filename.split('.')[0] + '-fft-separate-pic-' + time_series_string + '.png'), bbox_inches="tight")

    def reorganizecsv_file(self, input_csv_filename, output_csv_filename):
        """
        Function to clean up csv data files from "." and "]" symbols
        Depends on the OS of the edge platform
        :param input_csv_filename: raw csv file
        :param output_csv_filename: processed csv file
        :return:
        """
        input_csv_fh = csv.reader(open(os.path.join(self.data_parent_directory, self.local_directory, input_csv_filename), 'r'))
        csvfile_header_fh = next(input_csv_fh)
        output_csv_fh = csv.writer(open(os.path.join(self.data_parent_directory, self.local_directory, output_csv_filename), 'a'))

        for row in input_csv_fh:
            output_csv_fh.writerow(row + csvfile_header_fh)

        if platform.system() == 'Linux':
            subprocess.call(["sed", "-i", 's/\.\]//g', str(os.path.join(self.data_parent_directory, self.local_directory, output_csv_filename))])
            subprocess.call(["sed", "-i", 's/\[//g', str(os.path.join(self.data_parent_directory, self.local_directory, output_csv_filename))])

        elif platform.system() == 'Darwin':
            subprocess.call(["sed", "-i.bu", 's/\.\]//g', str(os.path.join(os.getcwd(), self.local_directory, output_csv_filename))])
            subprocess.call(["sed", "-i.bu", 's/\[//g', str(os.path.join(os.getcwd(), self.local_directory, output_csv_filename))])

    def plotDataConstrained(self, Cout_time_series_string, Aout_time_series_string, Cout_time_series, Aout_time_series,
                            start_time, finish_time, separate):
        """
        Function to plot Cout and Aouts within a start and end time window
        Wrapper around plotData()
        :param Cout_time_series_string:
        :param Aout_time_series_string:
        :param Cout_time_series:
        :param Aout_time_series:
        :param start_time:
        :param finish_time:
        :param separate:
        :return:
        """
        df = pd.read_csv(os.path.join(self.data_parent_directory, self.local_directory, self.filename))
        time_series = df.iloc[:, 0]  # Inter-sample Time for FFT Calculation
        start = self.findIndex(time_series, start_time)
        finish = self.findIndex(time_series, finish_time)
        self.plotData(Cout_time_series_string, Aout_time_series_string,
                      Cout_time_series[start:finish+1], Aout_time_series[start:finish+1], separate)

    def plotData(self, Cout_time_series_string, Aout_time_series_string, Cout_time_series, Aout_time_series,
                 separate=True):
        """
        Function to plot Cout and Aout's given a list of Cout and Aout, plotting in time domain
        :param Cout_time_series_string:
        :param Aout_time_series_string:
        :param Cout_time_series:
        :param Aout_time_series:
        :param separate:
        :return:
        """

        # This expects that the fieldnames are ordered like Cout (Sensor I), Aout (Sensor I)
        # -- which would give sensor_type as Sensor I
        type = self.identify_same_sensor_data(Cout_time_series_string, Aout_time_series_string)
        sensor_type = type[type.find('(')+1:type.find(')')]
        print(sensor_type)
        data = np.genfromtxt(os.path.join(self.data_parent_directory, self.local_directory, self.filename),
                             delimiter=',', dtype=int)

        # We need only offsets
        offset = data [1][0] # offset is the first element of sample time
        # print(offset) # This is the starting timestamp of the data
        times_in_ms = list()
        for x in data[1:, 0]:
            x = (x-offset)/1e3
            times_in_ms.append(x)

        # Plotting settings
        plt.rcdefaults()
        plt.rcParams["font.family"] = "Arial"
        plt.rcParams['font.size'] = 14 #24 #14 #24
        plt.rcParams['legend.fontsize'] = 14 #20 #14 #20
        plt.rcParams['axes.titlesize'] = 14 #24 #14 #24
        plt.rcParams['ytick.labelsize'] = 12 #24 #12 #24
        plt.rcParams['xtick.labelsize'] = 12 #24 #12 #24
        plt.rcParams['figure.figsize'] = 7, 2 #8, 6 #10, 11
        # plt.gcf().set_size_inches(10, 7)

        '''
        Plotting Cout and Aout in separate graphs
        '''
        if separate:
            NUM_ROWS = 2
            NUM_COLS = 1
            fig, ax = plt.subplots(nrows=NUM_ROWS, ncols=NUM_COLS, sharex='col', squeeze=False)
            # plt.subplots_adjust(left=0.15, bottom=0.15, right=0.96, top=0.95, wspace=0.20, hspace=0.20)
            for row in range(NUM_ROWS):
                for col in range(NUM_COLS):
                    ax[row, col].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
                    ax[row, col].set_ylim(bottom=0, top=5.0)
                    ax[row, col].set_ylabel(r'Voltage (V)')

            ax[NUM_ROWS-1, NUM_COLS-1].set_xlabel('Time (secs) ')

            # ax.text(0.60, 0.95,
            #          r'$C_{out}$ variance = ' + str(format(np.var(Cout_time_series, dtype=np.float32), '.2f')),
            #         transform=ax.transAxes)
            # ax.text(0.60, 0.90,
            #          r'$A_{out}$ variance = ' + str(format(np.var(Aout_time_series, dtype=np.float32), '.2f')),
            #         transform=ax.transAxes)
            plt.gcf().set_size_inches(7, 4)  # 8, 6 #10, 11

            ax[0, 0].plot(times_in_ms, [(i * 5.0)/1023 for i in Cout_time_series], label=Cout_time_series_string, linestyle='-', color='b', alpha=0.5)
            # ax[0,0].legend(loc='upper left', shadow=True)
            ax[0, 0].legend(bbox_to_anchor=(1.03, 1.08), loc="upper right", shadow=True)
            ax[1, 0].plot(times_in_ms, [(i * 5.0)/1023 for i in Aout_time_series], label=Aout_time_series_string, linestyle='-', color='g', alpha=0.5)
            # ax[1, 0].legend(loc='upper left', shadow=True)
            ax[1, 0].legend(bbox_to_anchor=(1.03, 1.08), loc="upper right", shadow=True)
            plt.savefig(os.path.join(self.data_parent_directory, self.local_directory,
                                     self.filename.split('.')[0] + '-'.join([Cout_time_series_string, Aout_time_series_string]) + sensor_type + '-separate' + '.png'), bbox_inches = "tight")
            # plt.show()
        else:
            fig, ax = plt.subplots(1,1)
            # plt.subplots_adjust(left=0.15, bottom=0.15, right=0.96, top=0.95, wspace=0.20, hspace=0.20)
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.ylim(bottom=0, top=5.0)
            plt.ylabel(r'Voltage (V)')

            # plt.ylabel(r'ADC Count of $A_{out}$, $C_{out}$')
            plt.xlabel(r'Time (secs) ')

            # ax.text(0.60, 0.95,
            #          r'$C_{out}$ variance = ' + str(format(np.var(Cout_time_series, dtype=np.float32), '.2f')),
            #         transform=ax.transAxes)
            # ax.text(0.60, 0.90,
            #          r'$A_{out}$ variance = ' + str(format(np.var(Aout_time_series, dtype=np.float32), '.2f')),
            #         transform=ax.transAxes)
            # sensor_type = ''

            # plt.plot(times_in_ms, Cout_time_series, label=r"Digital ($C_{out}$) " + sensor_type, linestyle='-',
            #          color='b', alpha=0.5)

            cb_color_cycle = ['g', 'k']
            color_cycler = cycle(cb_color_cycle)

            plt.plot(times_in_ms, [(i * 5.0)/1023 for i in Cout_time_series], label=Cout_time_series_string,
                     linestyle='-', color=next(color_cycler), alpha=0.5)
            plt.plot(times_in_ms, [(i * 5.0)/1023 for i in Aout_time_series], label=Aout_time_series_string,
                    linestyle='-', color=next(color_cycler), alpha=0.5)
            plt.legend(bbox_to_anchor=(1.02,1.03), loc='upper right', shadow=True, ncol=2)
            plt.savefig(os.path.join(self.data_parent_directory, self.local_directory,
                                     self.filename.split('.')[0] + '-'.join([Cout_time_series_string, Aout_time_series_string]) + sensor_type + '-unified' + '.png'), bbox_inches="tight")
            # plt.show()

    def identify_same_sensor_data(self, string1, string2):
        """
        Function to return the longest common substring using the difflib library in python
        :param s1: Input string 1
        :param s2: Input string 2
        :return:
        """
        seq_match = SequenceMatcher(None, string1, string2)
        match = seq_match.find_longest_match(0, len(string1), 0, len(string2))

        # return the longest substring
        if match.size != 0:
            return string1[match.a: match.a + match.size]
        else:
            return 'Longest common sub-string not present'

    def findIndex(self, mylist, myval):
        """
        Function to find index of a particular value myval in mylist
        :param mylist:
        :param myval:
        :return:
        """
        for i in range(len(mylist)):
            if mylist[i] == myval:
                return i


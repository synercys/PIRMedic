import csv, serial, time, os, datetime, itertools
import matplotlib.pyplot as plt
from collections import defaultdict
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from data.config import DATAPARAMS

data_capture_duration_in_secs = 3600*3
# list_of_fieldnames = ['Sample', 'A{}'.format('\u2092'), 'C{}'.format('\u2092')]
# list_of_fieldnames = ['Sample', 'Cout', 'Aout']
# list_of_fieldnames = ['Sample', 'Aout', 'Cout']
list_of_fieldnames = ['Sampling Time', 'Aout_normal', 'Cout_normal', 'Aout_window_covered', 'Cout_window_covered', 'Aout_lens_covered', 'Cout_lens_covered']
# filename = 'pir_evm_raw_data.csv'

# arduinoSerialData = serial.Serial('/dev/tty.usbmodem1411', 9600)
# start_time = time.time()
# arduinoSerialData.flushInput()
# time.sleep(5)
#
# mydir = os.path.join(os.getcwd() + '/data/CSL_Lobby_3_PIRs/', datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
# os.makedirs(mydir)
# f = open(os.path.join(mydir,filename), 'w')
# f.write(','.join(list_of_fieldnames) + '\n')
#
# while (time.time() - start_time) <= data_capture_duration_in_secs :
#     #Copy Serial Terminal to CSV
#     if arduinoSerialData.inWaiting():
#         myData = arduinoSerialData.readline().decode().strip()
#         f.write(myData+'\n')
#
# f.flush()
# f.close()
# arduinoSerialData.close()


xvalues = list()
yvalues = list()

mydir = os.path.join(DATAPARAMS.data_dir, 'characterization_inlinelens/20200330_044957_lens_line_vertical')
filename = 'PIR_EVM_Charac_WithObstacle.csv'

# mydir = os.path.join(DATAPARAMS.data_dir, 'characterization_roundlens/20200330_033009')
# filename = 'PIR_EVM_Charac_WithObstacle.csv'

csvFile = open(os.path.join(mydir, filename), 'r')

# Trick to find the number of fields in a csv file
reader1, reader = itertools.tee(csv.reader(csvFile))
columns = len(next(reader1))
del reader1
next(reader, None)

# Dictionary to store the csv column values
csvdict_analog = defaultdict(int)
csvdict_digital = defaultdict(int)


# Adjust to the csv files generated
if columns == 4:
    for sample, digital_out, analog_out, state in reader:
        csvdict_analog[int(sample)] = int(analog_out)
        csvdict_digital[int(sample)] = int(digital_out)
elif columns == 3:
    for sample, digital_out, analog_out in reader:
        csvdict_analog[int(sample)] = int(analog_out)
        csvdict_digital[int(sample)] = int(digital_out)


capture_inset = True #False

# Plotting settings
plt.rcdefaults()
plt.rcParams["font.family"] = "Arial"
plt.rcParams['font.size'] = 24
plt.rcParams['legend.fontsize'] = 20
plt.rcParams['axes.titlesize'] = 24
plt.rcParams['ytick.labelsize'] = 24
plt.rcParams['xtick.labelsize'] = 24
plt.rcParams['figure.figsize'] = 8, 5

# f, axarr = plt.subplots(2, sharex='row')
f, axarr = plt.subplots(1, 1)

# plt.gcf().set_size_inches(10, 7)

# Analog values
plt.ylim(bottom=0, top=5.0)
plt.xlim(left=30, right=90)
plt.ylabel(r'Voltage (V)')
plt.xlabel(r'Time (secs) ')
# plt.plot([i/1e3 for i in list(csvdict_analog.keys())], [(i * 5.0)/1023 for i in list(csvdict_analog.values())], linestyle='-', color='g', alpha=0.5)
# plt.plot([i/1e3 for i in list(csvdict_digital.keys())], [(i * 5.0)/1023 for i in list(csvdict_digital.values())], linestyle='-', color='b', alpha=0.5)

# For the powerpoint, Analog output in red and Discrete output in blue
plt.plot([i/1e3 for i in list(csvdict_analog.keys())], [(i * 5.0)/1023 for i in list(csvdict_analog.values())], linestyle='-', color='r')
plt.plot([i/1e3 for i in list(csvdict_digital.keys())], [(i * 5.0)/1023 for i in list(csvdict_digital.values())], linestyle='-', color='b')


if capture_inset:

    axins_top = zoomed_inset_axes(parent_axes=axarr, zoom=1.3,
                                  loc=1, bbox_to_anchor=(1.15, 1.15),
                                  bbox_transform=axarr.transAxes)


    # axins_top = inset_axes(parent_axes=axarr, width=1.5, height=1.5 , loc=1, bbox_to_anchor=(1, 1),bbox_transform=axarr.transAxes) # no zoom
    # Orignally in the paper
    # axins_top.plot([i/1e3 for i in list(csvdict_analog.keys())], [(i * 5.0)/1023 for i in list(csvdict_analog.values())],
    #                linestyle='-', color='g', alpha=0.5)
    axins_top.plot([i / 1e3 for i in list(csvdict_analog.keys())],
                   [(i * 5.0) / 1023 for i in list(csvdict_analog.values())],
                   linestyle='-', color='r')

    # specify the limits, this is where you wanna zoom
    # x1, x2, y1, y2 = 59.500, 62.500, 0, 3.5 # roundlens
    x1, x2, y1, y2 = 61.500, 66.500, 0, 3.5 # inlinelens

    axins_top.set_xlim(x1, x2)
    axins_top.set_ylim(y1, y2)
    plt.yticks(visible=True)
    plt.xticks(visible=True, rotation=45, fontsize=18)

    axins_top.set_xticks([x1, x2])
    axins_top.set_xticklabels([x1, x2])

    # plt.yticks(ticks=[600,800], visible=True)
    # plt.xticks(ticks=[60000,80000], visible=True)

    # mark_inset(axarr, axins_top, loc1=2, loc2=4, fc="none", ec="0.5")


# Digital values
# axarr[1].set_ylim(ymin=0, ymax=1024)
# axarr[1].set(xlabel='Time (ms)', ylabel=r'ADC Count for $C_{out}$')
# axarr[1].plot(list(csvdict_digital.keys()),list(csvdict_digital.values()), linestyle='-', color='b', alpha=0.5)


# plt.savefig(os.path.join(os.getcwd(), mydir, filename.split('.')[0] + 'fast-obstacle-withinset.png'), bbox_inches = "tight")
plt.savefig(os.path.join(mydir, filename.split('.')[0] + '-Aout-withoutinset.png'), bbox_inches = "tight")

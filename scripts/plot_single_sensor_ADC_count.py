import csv, serial,time, os, datetime
import matplotlib.pyplot as plt
from collections import defaultdict
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from data.config import DATAPARAMS

xvalues = list()
yvalues = list()
mydir = os.path.join(DATAPARAMS.data_dir, '20190719_181245')
filename = 'PIR_write_experiment_condition_raw_data.csv'
csvFile = open(os.path.join(mydir, filename), 'r')

reader = csv.reader(csvFile)
next(reader, None)

csvdict_analog = defaultdict(int)
csvdict_digital = defaultdict(int)

for sample, digital_out, analog_out in reader:
    csvdict_analog[int(sample)] = int(analog_out)
    csvdict_digital[int(sample)] = int(digital_out)


f, axarr = plt.subplots(2, sharex='row')

# Plotting settings
plt.rcdefaults()
plt.rcParams["font.family"] = "Arial"
plt.rcParams['font.size'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['figure.figsize'] = 8, 6

# Analog values
axarr[0].set_ylim(ymin=0, ymax=1024)
axarr[0].set_title('Title of Graph')
axarr[0].set(ylabel='ADC Count for A{} -----> '.format('\u2092'))
axarr[0].plot(list(csvdict_analog.keys()),list(csvdict_analog.values()), linestyle='-', color='b', alpha=0.5)

# Zoom into a particular region
# axins_top = zoomed_inset_axes(parent_axes=axarr[0], zoom=4.0, loc=1)
# axins_top.plot(list(csvdict_analog.keys()),list(csvdict_analog.values()), linestyle='-', color='b', alpha=0.5)
# x1, x2, y1, y2 = 10000, 20000, 600, 800 # specify the limits, this is where you wanna zoom
# axins_top.set_xlim(x1, x2)
# axins_top.set_ylim(y1, y2)
# plt.yticks(visible=False)
# plt.xticks(visible=False)
# # plt.yticks(ticks=[600,800], visible=True)
# # plt.xticks(ticks=[60000,80000], visible=True)
# mark_inset(axarr[0], axins_top, loc1=2, loc2=3, fc="none", ec="0.5")

# Digital values
axarr[1].set_ylim(ymin=0, ymax=1024)
axarr[1].set(xlabel='Samples ----> ', ylabel='ADC Count for C{} -----> '.format('\u2092'))
axarr[1].plot(list(csvdict_digital.keys()),list(csvdict_digital.values()), linestyle='-', color='b', alpha=0.5)

# Zoom into a particular region
# axins= zoomed_inset_axes(parent_axes=axarr[1], zoom=4.0, loc=1)
# axins.plot(list(csvdict_digital.keys()),list(csvdict_digital.values()), linestyle='-', color='b', alpha=0.5)
# x1, x2, y1, y2 = 10000, 20000, 600, 800 # specify the limits, this is where you wanna zoom
# axins.set_xlim(x1, x2)
# axins.set_ylim(y1, y2)
# plt.yticks(visible=False)
# plt.xticks(visible=False)
# # plt.yticks(ticks=[600,800], visible=True)
# # plt.xticks(ticks=[60000,80000], visible=True)
# mark_inset(axarr[1], axins, loc1=2, loc2=3, fc="none", ec="0.5")

# Show or Save the figure
# plt.show()
plt.savefig('filename.pdf', format='pdf', dpi=1000)





